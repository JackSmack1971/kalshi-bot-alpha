#!/usr/bin/env python3
"""Append small, validated, redacted skill-quality events to local JSONL files."""

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
ALLOWED_KEYS = {
    "schema_version", "timestamp", "run_id", "skill", "skill_revision", "event",
    "outcome", "reason_code", "duration_ms", "count", "matched", "failed", "skipped",
    "evidence_refs", "surface", "lens", "severity", "reviewer", "domain", "lane",
    "status", "authorized", "coverage", "confirmed", "refuted", "retries",
}
FIELD_KEYS = ALLOWED_KEYS - {"schema_version", "timestamp", "run_id", "skill", "skill_revision", "event", "outcome", "reason_code"}


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


def append_event(skill: str, event: str, *, outcome: str, reason_code: str = "none",
                 run_id: str | None = None, evidence_refs: list[str] | None = None,
                 **fields: Any) -> dict[str, Any]:
    skill_dir = ROOT / ".agents" / "skills" / skill
    schema = _schema(skill_dir)
    if event not in schema["properties"]["event"]["enum"]:
        raise ValueError(f"event {event!r} is not declared by {skill}")
    sensitive_keys = {key for key in fields if SECRET_KEY.search(key)}
    if sensitive_keys:
        raise ValueError(f"sensitive telemetry field rejected: {sorted(sensitive_keys)[0]}")
    unknown = set(fields) - FIELD_KEYS
    if unknown:
        raise ValueError(f"undeclared telemetry fields: {sorted(unknown)}")
    if outcome not in {"started", "passed", "failed", "blocked", "skipped", "recovered", "not_applicable"}:
        raise ValueError(f"invalid telemetry outcome: {outcome}")
    if not re.fullmatch(r"[a-z0-9_.-]{1,80}", reason_code):
        raise ValueError("reason_code must be lowercase and machine-readable")
    for key in ("duration_ms", "count", "matched", "failed", "skipped", "confirmed", "refuted", "retries"):
        if key in fields and (not isinstance(fields[key], int) or isinstance(fields[key], bool) or fields[key] < 0):
            raise ValueError(f"{key} must be a non-negative integer")
    if "coverage" in fields and (not isinstance(fields["coverage"], (int, float)) or not 0 <= fields["coverage"] <= 1):
        raise ValueError("coverage must be between 0 and 1")
    refs = evidence_refs or []
    if any(ABSOLUTE.match(ref) or not ref or ".." in Path(ref).parts for ref in refs):
        raise ValueError("evidence_refs must be non-empty repository-relative paths")
    revision = hashlib.sha256((skill_dir / "SKILL.md").read_bytes()).hexdigest()[:16]
    record: dict[str, Any] = {
        "schema_version": schema["properties"]["schema_version"]["const"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id or str(uuid.uuid4()),
        "skill": skill,
        "skill_revision": revision,
        "event": event,
        "outcome": outcome,
        "reason_code": reason_code,
        **fields,
    }
    if refs:
        record["evidence_refs"] = refs
    record = _sanitize(record, "record")
    missing = set(schema["required"]) - record.keys()
    if missing:
        raise ValueError(f"missing telemetry fields: {sorted(missing)}")
    target = skill_dir / "telemetry" / "events.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill")
    parser.add_argument("event")
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--reason-code", default="none")
    parser.add_argument("--evidence", action="append", default=[])
    args = parser.parse_args()
    try:
        print(json.dumps(append_event(args.skill, args.event, outcome=args.outcome,
                                      reason_code=args.reason_code,
                                      evidence_refs=args.evidence), sort_keys=True))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"telemetry error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
