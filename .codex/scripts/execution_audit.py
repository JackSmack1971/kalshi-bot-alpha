#!/usr/bin/env python3
"""Append a tamper-evident local causal audit ledger for one execution run.

The ledger records observable inputs, policy decisions, evidence and effects;
it never records or requires hidden chain-of-thought. Local files are not an
off-host authoritative audit store, so production deployments should export or
correlate these records with externally retained telemetry/audit systems.
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
STATE = ROOT / ".control-plane-state" / "runs"
SCHEMA = json.loads((ROOT / ".codex/control-plane/audit-event.schema.json").read_text(encoding="utf-8"))
ABSOLUTE = re.compile(r"^(?:[A-Za-z]:[\\/]|/|\\\\)")
SECRET = re.compile(r"(?i)(api[_-]?key|authorization|credential|password|secret|token|private[_-]?key|cookie|bearer\s+\S+|-----begin)")
DIGEST_ID = re.compile(r"^sha256:[a-f0-9]{64}$")


def _canonical_hash(record: dict[str, Any]) -> str:
    material = {k: v for k, v in record.items() if k != "event_hash"}
    return "sha256:" + hashlib.sha256(json.dumps(material, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _ledger(run_id: str) -> Path:
    return STATE / run_id / "audit.jsonl"


def _validate_ref(value: str) -> None:
    if not value or ABSOLUTE.match(value) or ".." in Path(value).parts or SECRET.search(value):
        raise ValueError(f"unsafe or non-portable audit reference: {value!r}")


def _state(run_id: str) -> tuple[int, str | None, str | None]:
    path = _ledger(run_id)
    if not path.exists():
        return 0, None, None
    seq = 0
    parent = None
    last_event = None
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"malformed audit JSONL at line {lineno}: {exc.msg}") from exc
        if rec.get("run_id") != run_id or rec.get("sequence") != seq + 1 or rec.get("parent_event_hash") != parent:
            raise ValueError(f"audit chain discontinuity at line {lineno}")
        if _canonical_hash(rec) != rec.get("event_hash"):
            raise ValueError(f"audit event hash mismatch at line {lineno}")
        seq = rec["sequence"]
        parent = rec["event_hash"]
        last_event = rec.get("event")
    return seq, parent, last_event


def append(
    run_id: str,
    event: str,
    *,
    actor_role: str,
    operation: str,
    outcome: str,
    reason_code: str,
    execution_snapshot_id: str | None = None,
    uow_id: str | None = None,
    policy_ref: str | None = None,
    approval_ref: str | None = None,
    evidence_refs: list[str] | None = None,
    effect_refs: list[str] | None = None,
) -> dict[str, Any]:
    if not isinstance(run_id, str) or not 1 <= len(run_id) <= 100 or "\n" in run_id or "\r" in run_id:
        raise ValueError("run_id must be a non-empty single-line string of at most 100 characters")
    if event not in SCHEMA["properties"]["event"]["enum"]:
        raise ValueError(f"unsupported audit event: {event}")
    if outcome not in SCHEMA["properties"]["outcome"]["enum"]:
        raise ValueError(f"unsupported audit outcome: {outcome}")
    if not re.fullmatch(r"[A-Z0-9_.-]{1,100}", reason_code):
        raise ValueError("reason_code must be uppercase machine-readable vocabulary")
    for value in [actor_role, operation, policy_ref, approval_ref]:
        if value and (SECRET.search(value) or "\n" in value or "\r" in value):
            raise ValueError("audit fields must not contain secrets or multiline content")
    if not actor_role or len(actor_role) > 100:
        raise ValueError("actor_role must be 1-100 characters")
    if not operation or len(operation) > 120:
        raise ValueError("operation must be 1-120 characters")
    for key, value in (("policy_ref", policy_ref), ("approval_ref", approval_ref)):
        if value is not None and len(value) > 200:
            raise ValueError(f"{key} must be at most 200 characters")
    for key, value in (("execution_snapshot_id", execution_snapshot_id), ("uow_id", uow_id)):
        if value is not None and not DIGEST_ID.fullmatch(value):
            raise ValueError(f"{key} must be a sha256 digest identifier")
    for ref in (evidence_refs or []) + (effect_refs or []):
        _validate_ref(ref)

    seq, parent, last_event = _state(run_id)
    if seq == 0:
        if event != "run.started" or outcome != "started":
            raise ValueError("an audit run must begin with run.started / started")
    else:
        if event == "run.started":
            raise ValueError("run.started is only valid as the first event in a run")
        if last_event == "run.completed":
            raise ValueError("audit run is already completed")
    if event == "run.completed" and outcome not in {"completed", "failed", "blocked", "unverified"}:
        raise ValueError("run.completed requires a terminal outcome")
    record: dict[str, Any] = {
        "schema_version": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "sequence": seq + 1,
        "parent_event_hash": parent,
        "event": event,
        "actor_role": actor_role,
        "operation": operation,
        "outcome": outcome,
        "reason_code": reason_code,
    }
    optional = {
        "execution_snapshot_id": execution_snapshot_id,
        "uow_id": uow_id,
        "policy_ref": policy_ref,
        "approval_ref": approval_ref,
        "evidence_refs": evidence_refs or None,
        "effect_refs": effect_refs or None,
    }
    record.update({k: v for k, v in optional.items() if v is not None})
    record["event_hash"] = _canonical_hash(record)
    path = _ledger(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    return record


def _common(parser: argparse.ArgumentParser, *, require_run: bool) -> None:
    parser.add_argument("event", choices=SCHEMA["properties"]["event"]["enum"])
    parser.add_argument("--run-id", required=require_run)
    parser.add_argument("--actor-role", required=True)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--outcome", required=True, choices=SCHEMA["properties"]["outcome"]["enum"])
    parser.add_argument("--reason-code", required=True)
    parser.add_argument("--execution-snapshot-id")
    parser.add_argument("--uow-id")
    parser.add_argument("--policy-ref")
    parser.add_argument("--approval-ref")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--effect", action="append", default=[])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    start = subs.add_parser("start")
    _common(start, require_run=False)
    emit = subs.add_parser("emit")
    _common(emit, require_run=True)
    finish = subs.add_parser("finish")
    _common(finish, require_run=True)
    args = parser.parse_args()
    run_id = args.run_id or str(uuid.uuid4())
    try:
        if args.command == "start" and args.event != "run.started":
            raise ValueError("start command requires event run.started")
        if args.command == "emit" and args.event in {"run.started", "run.completed"}:
            raise ValueError("emit command cannot create lifecycle boundary events")
        if args.command == "finish" and args.event != "run.completed":
            raise ValueError("finish command requires event run.completed")
        rec = append(
            run_id, args.event, actor_role=args.actor_role, operation=args.operation,
            outcome=args.outcome, reason_code=args.reason_code,
            execution_snapshot_id=args.execution_snapshot_id, uow_id=args.uow_id,
            policy_ref=args.policy_ref, approval_ref=args.approval_ref,
            evidence_refs=args.evidence, effect_refs=args.effect,
        )
        print(json.dumps(rec, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"audit error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
