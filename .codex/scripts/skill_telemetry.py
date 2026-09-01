#!/usr/bin/env python3
"""Append invocation-scoped, chained, redacted Skill quality telemetry.

Use `start` once to obtain a run_id, then reuse that run_id for every `emit`
and `finish` event in the same Skill invocation. This stream is lightweight
quality telemetry, not the authoritative execution audit ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SECRET_KEY = re.compile(r"(?i)(api[_-]?key|authorization|credential|password|secret|token|private[_-]?key|cookie|header)")
SECRET_VALUE = re.compile(r"(?i)(bearer\s+\S+|-----begin|sk-[A-Za-z0-9]{16,}|api[_-]?key\s*[:=]\s*\S+)")
SYNTHETIC_SECRET = re.compile(r"(?i)synthetic[-_ ](?:secret|key|token|credential|signature)")
ABSOLUTE = re.compile(r"^(?:[A-Za-z]:[\\/]|/|\\\\)")
DIGEST_ID = re.compile(r"^sha256:[a-f0-9]{64}$")
BASE_KEYS = {
    "schema_version", "timestamp", "run_id", "sequence", "parent_event_hash", "event_hash",
    "skill", "skill_revision", "event", "outcome", "reason_code", "execution_snapshot_id", "uow_id",
}
FIELD_KEYS = {
    "duration_ms", "count", "matched", "failed", "skipped", "evidence_refs", "surface", "lens",
    "severity", "reviewer", "domain", "lane", "status", "authorized", "coverage", "confirmed",
    "refuted", "retries",
}
ALLOWED_KEYS = BASE_KEYS | FIELD_KEYS


def _sanitize(value: Any, key: str) -> Any:
    if SECRET_KEY.search(key) or (
        isinstance(value, str) and (SECRET_VALUE.search(value) or SYNTHETIC_SECRET.search(value))
    ):
        raise ValueError(f"sensitive telemetry field rejected: {key}")
    if isinstance(value, dict):
        return {str(k): _sanitize(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize(v, key) for v in value]
    if isinstance(value, str):
        if len(value) > 200:
            raise ValueError(f"telemetry string too long: {key}")
        if ABSOLUTE.match(value) or "\n" in value or "\r" in value:
            raise ValueError(f"non-portable or multiline telemetry value: {key}")
    return value


def _schema(skill_dir: Path) -> dict[str, Any]:
    return json.loads((skill_dir / "telemetry" / "schema.json").read_text(encoding="utf-8"))


def _target(skill_dir: Path) -> Path:
    return skill_dir / "telemetry" / "events.jsonl"


def _canonical_hash(record: dict[str, Any]) -> str:
    material = {k: v for k, v in record.items() if k != "event_hash"}
    return "sha256:" + hashlib.sha256(
        json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _read_run_state(target: Path, run_id: str) -> tuple[int, str | None, str | None]:
    if not target.exists():
        return 0, None, None
    last_sequence = 0
    last_hash = None
    last_event = None
    for lineno, line in enumerate(target.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"malformed telemetry JSONL at {target}:{lineno}: {exc.msg}") from exc
        if record.get("run_id") != run_id:
            continue
        sequence = record.get("sequence")
        event_hash = record.get("event_hash")
        if not isinstance(sequence, int) or sequence <= last_sequence or not isinstance(event_hash, str):
            raise ValueError(f"invalid telemetry chain for run {run_id} at line {lineno}")
        if sequence != last_sequence + 1:
            raise ValueError(f"non-contiguous telemetry sequence for run {run_id} at line {lineno}")
        if record.get("parent_event_hash") != last_hash:
            raise ValueError(f"telemetry parent hash mismatch for run {run_id} at line {lineno}")
        if _canonical_hash(record) != event_hash:
            raise ValueError(f"telemetry event hash mismatch for run {run_id} at line {lineno}")
        last_sequence = sequence
        last_hash = event_hash
        last_event = record.get("event")
    return last_sequence, last_hash, last_event


def append_event(
    skill: str,
    event: str,
    *,
    outcome: str,
    reason_code: str = "none",
    run_id: str,
    evidence_refs: list[str] | None = None,
    execution_snapshot_id: str | None = None,
    uow_id: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    skill_dir = ROOT / ".agents" / "skills" / skill
    schema = _schema(skill_dir)
    if event not in schema["properties"]["event"]["enum"]:
        raise ValueError(f"event {event!r} is not declared by {skill}")
    if outcome not in {"started", "passed", "failed", "blocked", "skipped", "recovered", "not_applicable"}:
        raise ValueError(f"invalid telemetry outcome: {outcome}")
    if not re.fullmatch(r"[a-z0-9_.-]{1,80}", reason_code):
        raise ValueError("reason_code must be lowercase and machine-readable")
    if not isinstance(run_id, str) or not 1 <= len(run_id) <= 100:
        raise ValueError("run_id must be a non-empty string of at most 100 characters")
    unknown = set(fields) - FIELD_KEYS
    if unknown:
        raise ValueError(f"undeclared telemetry fields: {sorted(unknown)}")
    if any(SECRET_KEY.search(key) for key in fields):
        raise ValueError("sensitive telemetry field rejected")
    # Reject sensitive values before lifecycle validation as well. A malformed
    # or unstarted run must never provide a side channel that hides a secret
    # payload behind an unrelated state error.
    for key, value in fields.items():
        _sanitize(value, key)
    for key in ("duration_ms", "count", "matched", "failed", "skipped", "confirmed", "refuted", "retries"):
        if key in fields and (not isinstance(fields[key], int) or isinstance(fields[key], bool) or fields[key] < 0):
            raise ValueError(f"{key} must be a non-negative integer")
    if "coverage" in fields and (not isinstance(fields["coverage"], (int, float)) or not 0 <= fields["coverage"] <= 1):
        raise ValueError("coverage must be between 0 and 1")
    if "authorized" in fields and not isinstance(fields["authorized"], bool):
        raise ValueError("authorized must be boolean")
    if "severity" in fields and fields["severity"] not in {"low", "medium", "high", "critical"}:
        raise ValueError("severity must be one of low, medium, high, critical")
    for key in ("surface", "lens", "reviewer", "domain", "lane", "status"):
        if key in fields and (not isinstance(fields[key], str) or len(fields[key]) > 80):
            raise ValueError(f"{key} must be a string of at most 80 characters")
    for key, value in (("execution_snapshot_id", execution_snapshot_id), ("uow_id", uow_id)):
        if value is not None and (not isinstance(value, str) or not DIGEST_ID.fullmatch(value)):
            raise ValueError(f"{key} must be a sha256 digest identifier")
    refs = evidence_refs or []
    if any(ABSOLUTE.match(ref) or not ref or ".." in Path(ref).parts for ref in refs):
        raise ValueError("evidence_refs must be non-empty repository-relative paths")

    target = _target(skill_dir)
    last_sequence, parent_hash, last_event = _read_run_state(target, run_id)
    if last_sequence == 0:
        if event != "invocation_started" or outcome != "started":
            raise ValueError("a telemetry run must begin with invocation_started / started")
    else:
        if event == "invocation_started":
            raise ValueError("invocation_started is only valid as the first event in a run")
        if last_event == "invocation_finished":
            raise ValueError("telemetry run is already finished")
    if event == "invocation_finished" and outcome == "started":
        raise ValueError("invocation_finished must use a terminal outcome")
    revision = hashlib.sha256((skill_dir / "SKILL.md").read_bytes()).hexdigest()[:16]
    record: dict[str, Any] = {
        "schema_version": schema["properties"]["schema_version"]["const"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "sequence": last_sequence + 1,
        "parent_event_hash": parent_hash,
        "skill": skill,
        "skill_revision": revision,
        "event": event,
        "outcome": outcome,
        "reason_code": reason_code,
        **fields,
    }
    if execution_snapshot_id:
        record["execution_snapshot_id"] = execution_snapshot_id
    if uow_id:
        record["uow_id"] = uow_id
    if refs:
        record["evidence_refs"] = refs
    record = _sanitize(record, "record")
    record["event_hash"] = _canonical_hash(record)
    missing = set(schema["required"]) - record.keys()
    if missing:
        raise ValueError(f"missing telemetry fields: {sorted(missing)}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    return record


def _parse_fields(values: list[str]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"--field must be key=value: {item!r}")
        key, raw = item.split("=", 1)
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            value = raw
        fields[key] = value
    return fields


def _add_common(parser: argparse.ArgumentParser, *, run_id_required: bool) -> None:
    parser.add_argument("skill")
    parser.add_argument("event")
    parser.add_argument("--outcome", required=False)
    parser.add_argument("--reason-code", default="none")
    parser.add_argument("--run-id", required=run_id_required)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--execution-snapshot-id")
    parser.add_argument("--uow-id")
    parser.add_argument("--field", action="append", default=[])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    start = subs.add_parser("start", help="start a Skill invocation and return its run_id")
    _add_common(start, run_id_required=False)
    emit = subs.add_parser("emit", help="append a consequential event to an existing run")
    _add_common(emit, run_id_required=True)
    finish = subs.add_parser("finish", help="append the terminal event for an existing run")
    _add_common(finish, run_id_required=True)
    args = parser.parse_args()

    try:
        fields = _parse_fields(args.field)
        if args.command == "start":
            run_id = args.run_id or str(uuid.uuid4())
            outcome = args.outcome or "started"
            if args.event != "invocation_started":
                raise ValueError("start command requires event invocation_started")
            if outcome != "started":
                raise ValueError("start outcome must be 'started'")
        else:
            run_id = args.run_id
            outcome = args.outcome
            if not outcome:
                raise ValueError("--outcome is required for emit/finish")
            if args.command == "emit" and args.event in {"invocation_started", "invocation_finished"}:
                raise ValueError("emit command cannot create lifecycle boundary events")
            if args.command == "finish":
                if args.event != "invocation_finished":
                    raise ValueError("finish command requires event invocation_finished")
                if outcome == "started":
                    raise ValueError("finish outcome must be terminal, not 'started'")

        record = append_event(
            args.skill,
            args.event,
            outcome=outcome,
            reason_code=args.reason_code,
            run_id=run_id,
            evidence_refs=args.evidence,
            execution_snapshot_id=args.execution_snapshot_id,
            uow_id=args.uow_id,
            **fields,
        )
        print(json.dumps(record, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"telemetry error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
