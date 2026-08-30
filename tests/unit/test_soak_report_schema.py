"""Offline proof for Phase 1 soak report generation and opt-in isolation."""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[2]))

from scripts.soak_phase1 import (
    ReconnectEvidence,
    SoakReport,
    _wait_while_supervising,
    report_dict,
    write_report,
)


def _report() -> SoakReport:
    return SoakReport(
        run_id="2026-08-30T210000Z",
        commit_sha="abc123",
        configuration_hash="a" * 64,
        lockfile_hash="b" * 64,
        started_at="2026-08-30T21:00:00+00:00",
        ended_at="2026-08-30T21:01:00+00:00",
        duration_seconds=60,
        rest_event_counts={"exchange_status": 1},
        websocket_event_counts={"TickerUpdate": 2},
        local_mock_reconnects=ReconnectEvidence(
            1, (12,), "tests/integration/test_websocket_reconnect.py"
        ),
        live_soak_reconnects=ReconnectEvidence(1, (34,), "client-side hook"),
        unhandled_failure_count=0,
        redaction_scan={"status": "pass", "evidence": "synthetic"},
    )


def test_report_shape_is_versioned_and_partitions_reconnect_proof() -> None:
    payload = report_dict(_report())
    assert payload["report_schema_version"] == 1
    assert payload["reconnects"]["local_mock_reconnects"]["count"] == 1
    assert payload["reconnects"]["live_soak_reconnects"]["count"] == 1
    assert "private_key" not in json.dumps(payload).lower()


def test_report_writer_refuses_second_write(tmp_path: Path) -> None:
    root = tmp_path / "soak"
    written = write_report(_report(), root)
    original = (written / "report.json").read_text(encoding="utf-8")
    with pytest.raises(FileExistsError):
        write_report(_report(), root)
    assert (written / "report.json").read_text(encoding="utf-8") == original


def test_report_preserves_failure_count_and_rejects_sensitive_fields() -> None:
    failed = replace(_report(), unhandled_failure_count=1)
    assert report_dict(failed)["unhandled_failure_count"] == 1
    with pytest.raises(ValueError):
        report_dict(replace(_report(), redaction_scan={"private_key": "x"}))


def test_report_rejects_secret_value_under_benign_field_name() -> None:
    secret = "SYNTHETIC-SECRET-MARKER-REPORT-EVIDENCE"
    with pytest.raises(ValueError):
        report_dict(replace(_report(), redaction_scan={"status": "pass", "evidence": secret}))


def test_writer_persists_failed_run_evidence(tmp_path: Path) -> None:
    run_dir = write_report(replace(_report(), unhandled_failure_count=1), tmp_path)
    payload = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
    assert payload["unhandled_failure_count"] == 1
    assert (run_dir / "report.md").exists()


def test_cli_is_opt_in_without_live_credentials_or_network(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/soak_phase1.py",
            "--duration-hours",
            "0.01",
            "--output-root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "--live-demo" in result.stderr
    assert not list(tmp_path.iterdir())


def test_soak_supervision_turns_stream_task_failure_into_run_failure() -> None:
    async def run() -> None:
        async def fail() -> None:
            raise RuntimeError("SYNTHETIC-SECRET-MARKER-STREAM")

        task = asyncio.create_task(fail())
        with pytest.raises(RuntimeError, match=r"stream task failed \(RuntimeError\)"):
            await _wait_while_supervising([task], 1.0)

    asyncio.run(run())
