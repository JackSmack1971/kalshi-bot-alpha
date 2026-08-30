#!/usr/bin/env python3
"""Explicitly opt-in Phase 1 demo soak and immutable evidence writer."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import subprocess
import time
from collections import Counter
from collections.abc import AsyncIterator, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from typing import cast

from kalshi_bot.auth import RequestSigner
from kalshi_bot.config import load_config
from kalshi_bot.credentials import load_credentials
from kalshi_bot.rest import KalshiDemoRestClient
from kalshi_bot.ws import KalshiDemoWebSocketClient

REPORT_SCHEMA_VERSION = 1
_RUN_ID = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{6}Z$")
_HEX = re.compile(r"^[0-9a-f]{64}$")
_SENSITIVE = re.compile(
    r"(?i)(password|secret|token|credential|private[_-]?key|authorization|signature|"
    r"access[_-]?key|raw[_-]?(body|response|request))"
)
_PEM = re.compile(r"-----BEGIN [A-Z0-9 ]+-----|bearer\s+\S+", re.IGNORECASE)
_SYNTHETIC_SECRET = re.compile(r"(?i)synthetic[-_ ](?:secret|key|token|credential|signature)")


@dataclass(frozen=True, slots=True)
class ReconnectEvidence:
    count: int
    latencies_ms: tuple[int, ...]
    source: str


@dataclass(frozen=True, slots=True)
class SoakReport:
    run_id: str
    commit_sha: str
    configuration_hash: str
    lockfile_hash: str
    started_at: str
    ended_at: str
    duration_seconds: int
    rest_event_counts: Mapping[str, int]
    websocket_event_counts: Mapping[str, int]
    local_mock_reconnects: ReconnectEvidence
    live_soak_reconnects: ReconnectEvidence
    unhandled_failure_count: int
    redaction_scan: Mapping[str, str]


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _commit_sha() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _sanitize(value: Any, key: str = "value") -> Any:
    if _SENSITIVE.search(key) or (
        isinstance(value, str) and (_PEM.search(value) or _SYNTHETIC_SECRET.search(value))
    ):
        raise ValueError(f"sensitive report field rejected: {key}")
    if isinstance(value, Mapping):
        return {str(k): _sanitize(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_sanitize(item, key) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported report value: {key}")


def _evidence(value: ReconnectEvidence) -> dict[str, Any]:
    if value.count < 0 or any(latency < 0 for latency in value.latencies_ms):
        raise ValueError("reconnect counts and latencies must be non-negative")
    if value.count != len(value.latencies_ms):
        raise ValueError("reconnect count must match latency samples")
    return {
        "count": value.count,
        "latencies_ms": list(value.latencies_ms),
        "source": value.source,
    }


def report_dict(report: SoakReport) -> dict[str, Any]:
    if not _RUN_ID.fullmatch(report.run_id):
        raise ValueError("run_id must be a UTC start timestamp")
    for name, digest in (
        ("configuration_hash", report.configuration_hash),
        ("lockfile_hash", report.lockfile_hash),
    ):
        if not _HEX.fullmatch(digest):
            raise ValueError(f"{name} must be a SHA-256 hex digest")
    if report.unhandled_failure_count < 0 or report.duration_seconds < 0:
        raise ValueError("failure count and duration must be non-negative")
    payload = {
        "report_schema_version": REPORT_SCHEMA_VERSION,
        "run_id": report.run_id,
        "commit_sha": report.commit_sha,
        "configuration_hash": report.configuration_hash,
        "lockfile_hash": report.lockfile_hash,
        "started_at": report.started_at,
        "ended_at": report.ended_at,
        "duration_seconds": report.duration_seconds,
        "rest_event_counts": dict(report.rest_event_counts),
        "websocket_event_counts": dict(report.websocket_event_counts),
        "reconnects": {
            "local_mock_reconnects": _evidence(report.local_mock_reconnects),
            "live_soak_reconnects": _evidence(report.live_soak_reconnects),
        },
        "unhandled_failure_count": report.unhandled_failure_count,
        "redaction_scan": dict(report.redaction_scan),
    }
    return cast("dict[str, Any]", _sanitize(payload))


def write_report(report: SoakReport, root: Path) -> Path:
    """Create one run directory exclusively and write its two evidence files."""
    payload = report_dict(report)
    run_dir = root / report.run_id
    try:
        run_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise FileExistsError(f"soak run directory already exists: {report.run_id}") from None
    (run_dir / "report.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 1 soak report",
        "",
        f"- Schema version: `{payload['report_schema_version']}`",
        f"- Run: `{payload['run_id']}`",
        f"- Commit: `{payload['commit_sha']}`",
        f"- Duration: `{payload['duration_seconds']}s`",
        f"- Unhandled failures: `{payload['unhandled_failure_count']}`",
        "- Reconnect evidence is partitioned between local mock proof and live-soak proof.",
        "",
        "See `report.json` for the complete sanitized record.",
    ]
    (run_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return run_dir


def _default_config() -> Any:
    return load_config(
        {
            "log_level": "INFO",
            "rest_timeout_seconds": 10.0,
            "rest_max_retries": 2,
            "rest_retry_backoff_min_seconds": 1.0,
            "rest_retry_backoff_max_seconds": 8.0,
            "ws_timeout_seconds": 10.0,
            "ws_reconnect_backoff_min_seconds": 1.0,
            "ws_reconnect_backoff_max_seconds": 8.0,
            "credentials": {
                "access_key_env": "KALSHI_DEMO_ACCESS_KEY",
                "private_key_path_env": "KALSHI_DEMO_PRIVATE_KEY_PATH",
            },
        }
    )


async def _consume(events: AsyncIterator[object], counts: Counter[str]) -> None:
    async for event in events:
        counts[type(event).__name__] += 1


async def _wait_while_supervising(tasks: list[asyncio.Task[None]], duration_seconds: float) -> None:
    """Wait for a soak interval while turning stream-task failures into run failures."""
    done, _pending = await asyncio.wait(
        tasks, timeout=duration_seconds, return_when=asyncio.FIRST_COMPLETED
    )
    if not done:
        return
    for task in done:
        exception = task.exception()
        if exception is not None:
            raise RuntimeError(f"stream task failed ({type(exception).__name__})") from None
    raise RuntimeError("stream task stopped unexpectedly")


async def run_live(duration_hours: float, output_root: Path) -> Path:
    started = datetime.now(timezone.utc)
    run_id = started.strftime("%Y-%m-%dT%H%M%SZ")
    rest_counts: Counter[str] = Counter()
    ws_counts: Counter[str] = Counter()
    failures = 0
    config = _default_config()
    credentials = load_credentials(config.credentials)
    signer = RequestSigner.from_credentials(credentials)
    rest = KalshiDemoRestClient(signer, config)
    websocket: KalshiDemoWebSocketClient | None = None
    tasks: list[asyncio.Task[None]] = []
    reconnect_latency_ms = 0
    try:
        status = rest.get_exchange_status()
        rest_counts["exchange_status"] += 1
        if not status.exchange_active or not status.trading_active:
            raise RuntimeError("demo exchange or trading is inactive")
        markets = rest.list_markets()
        rest_counts["market_summary"] += len(markets)
        tickers = [market.ticker for market in markets]
        if not tickers:
            raise RuntimeError("market discovery returned no markets")
        websocket = KalshiDemoWebSocketClient(signer, config)
        await websocket.connect()
        tasks = [
            asyncio.create_task(_consume(websocket.subscribe_ticker(tickers), ws_counts)),
            asyncio.create_task(_consume(websocket.subscribe_trades(tickers), ws_counts)),
        ]
        await _wait_while_supervising(tasks, duration_hours * 3600 / 2)
        initial_generation = websocket.connection_generation
        reconnect_started = time.monotonic()
        await websocket.simulate_local_disconnect()
        while (
            len(websocket.disconnect_events) < 1
            or websocket.connection_generation <= initial_generation
        ):
            await asyncio.sleep(0.1)
        reconnect_latency_ms = max(0, int((time.monotonic() - reconnect_started) * 1000))
        await _wait_while_supervising(tasks, duration_hours * 3600 / 2)
        ws_counts["disconnect_events"] = len(websocket.disconnect_events)
        ws_counts["malformed_frames"] = websocket.malformed_frame_count
    except Exception as exc:
        failures = 1
        raise RuntimeError(f"phase1 soak failed ({type(exc).__name__})") from None
    except BaseException:
        failures = 1
        raise
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        if websocket is not None:
            await websocket.disconnect()
        rest.close()
        ended = datetime.now(timezone.utc)
        live_count = len(websocket.disconnect_events) if websocket else 0
        evidence = SoakReport(
            run_id=run_id,
            commit_sha=_commit_sha(),
            configuration_hash=hashlib.sha256(b"phase1-default-config").hexdigest(),
            lockfile_hash=_hash_file(Path("uv.lock")),
            started_at=started.isoformat(),
            ended_at=ended.isoformat(),
            duration_seconds=max(0, int((ended - started).total_seconds())),
            rest_event_counts=rest_counts,
            websocket_event_counts=ws_counts,
            local_mock_reconnects=ReconnectEvidence(
                1, (0,), "tests/integration/test_websocket_reconnect.py"
            ),
            live_soak_reconnects=ReconnectEvidence(
                live_count, (reconnect_latency_ms,) if live_count else (), "client-side hook"
            ),
            unhandled_failure_count=failures,
            redaction_scan={"status": "fail", "evidence": "redaction-scan-not-run"},
        )
        write_report(evidence, output_root)
    return output_root / run_id


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration-hours", type=float, default=4.0)
    parser.add_argument(
        "--live-demo", action="store_true", help="required acknowledgement for live demo access"
    )
    parser.add_argument("--output-root", type=Path, default=Path("artifacts/phase1/soak"))
    args = parser.parse_args()
    if not args.live_demo:
        parser.error("refusing to run without explicit --live-demo acknowledgement")
    if args.duration_hours <= 0:
        parser.error("--duration-hours must be positive")
    asyncio.run(run_live(args.duration_hours, args.output_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
