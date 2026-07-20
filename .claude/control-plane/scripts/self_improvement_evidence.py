from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import hashlib
import json
import re
import sys
import tempfile
import threading
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ModuleNotFoundError:  # keep hook usable in minimal bootstrap environments
    Draft202012Validator = None

from new_run import canonical_hash

from common import (
    find_repo_root,
    normalize_rel,
    sha256_file,
    validate_change_plan_semantics,
    validate_terminal_artifact_hashes,
    validate_verifier_binding,
)

IGNORED_RUN_FILES = {
    ".gitkeep",
    ".malformed-payload-diagnostics.lock",
    "malformed-payload-diagnostics.jsonl",
}
MALFORMED_PAYLOAD_DIAGNOSTICS = "malformed-payload-diagnostics.jsonl"
MALFORMED_PAYLOAD_DIAGNOSTICS_LOCK = ".malformed-payload-diagnostics.lock"
HOOK_NAME = "UserPromptSubmit"
REQUIRED_RUN_FILES = {
    "events.jsonl",
    "baseline.json",
    "plan.json",
    "verification.json",
    "result.json",
}
IGNORED_RUN_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
IGNORED_RUN_SUFFIXES = {".pyc", ".pyo", ".tmp", ".swp"}
IGNORED_RUN_CACHE_FILES = {".DS_Store"}
SCRIPT_DIR = Path(__file__).resolve().parent
CONTROL_PLANE = SCRIPT_DIR.parent
SCHEMAS = CONTROL_PLANE / "schemas"
TERMINAL_RUN_STATES = {"COMMITTED", "ROLLED_BACK", "FAILED", "CANCELLED"}
_THREAD_LOCK_GUARD = threading.Lock()
_THREAD_LOCKS: dict[str, threading.Lock] = {}

TRIGGER_TERMS = (
    ".claude/workflows/self-improvement.md",
    "self-improvement.md",
    "self-improvement",
    "self improvement",
    "recursive improvement",
    "recursive control-plane",
    "improve the control plane",
    "control-plane improvement",
)


@dataclass(frozen=True)
class RunEvidence:
    state: str
    runs_directory: str
    latest_run: str | None
    latest_run_sha256: str | None
    run_count: int
    ignored_entries: list[str]
    invalid_entries: list[str]
    evidence_generated_at: str


def _load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def _validate_minimal_schema(schema: dict[str, Any], value: Any, path: str = "$") -> None:
    """Validate the schema subset used by run-ledger schemas when jsonschema is absent."""
    if "allOf" in schema:
        for option in schema["allOf"]:
            _validate_minimal_schema(option, value, path)

    if "anyOf" in schema:
        errors = []
        for option in schema["anyOf"]:
            try:
                _validate_minimal_schema(option, value, path)
                return
            except ValueError as exc:
                errors.append(str(exc))
        raise ValueError(errors[0])

    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(_matches_json_type(value, item) for item in expected_type):
            raise ValueError(f"{path}: expected one of {expected_type}")
    elif expected_type and not _matches_json_type(value, expected_type):
        raise ValueError(f"{path}: expected {expected_type}")

    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{path}: expected {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path}: expected one of {schema['enum']}")

    if isinstance(value, dict):
        if "if" in schema:
            try:
                _validate_minimal_schema(schema["if"], value, path)
                condition_matched = True
            except ValueError:
                condition_matched = False
            if condition_matched and "then" in schema:
                _validate_minimal_schema(schema["then"], value, path)
            if not condition_matched and "else" in schema:
                _validate_minimal_schema(schema["else"], value, path)

        for key in schema.get("required", []):
            if key not in value:
                raise ValueError(f"{path}: missing required property {key!r}")
        for key, dependent_keys in schema.get("dependentRequired", {}).items():
            if key in value:
                for dependent_key in dependent_keys:
                    if dependent_key not in value:
                        raise ValueError(
                            f"{path}: property {key!r} requires {dependent_key!r}"
                        )
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = set(value) - set(properties)
            if extras:
                raise ValueError(f"{path}: unexpected property {sorted(extras)[0]!r}")
        for key, child in properties.items():
            if key in value:
                _validate_minimal_schema(child, value[key], f"{path}.{key}")
    elif isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ValueError(f"{path}: too few items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                _validate_minimal_schema(item_schema, item, f"{path}[{index}]")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValueError(f"{path}: string is too short")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, value) is None:
            raise ValueError(f"{path}: string does not match pattern {pattern!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema:
        if value < schema["minimum"]:
            raise ValueError(f"{path}: value is less than minimum {schema['minimum']!r}")

    if "not" in schema:
        try:
            _validate_minimal_schema(schema["not"], value, path)
        except ValueError:
            pass
        else:
            raise ValueError(f"{path}: matched forbidden schema")


def _matches_json_type(value: Any, expected: str) -> bool:
    return (
        (expected == "object" and isinstance(value, dict))
        or (expected == "array" and isinstance(value, list))
        or (expected == "string" and isinstance(value, str))
        or (expected == "integer" and isinstance(value, int) and not isinstance(value, bool))
        or (expected == "number" and isinstance(value, (int, float)) and not isinstance(value, bool))
        or (expected == "boolean" and isinstance(value, bool))
        or (expected == "null" and value is None)
    )


def _validate_shape(name: str, value: Any) -> None:
    """Validate a run artifact against the repository schema without side effects.

    This intentionally mirrors replay.py's schema validation helper while keeping
    self-improvement evidence collection read-only. In minimal bootstrap
    environments without jsonschema, it falls back to the schema subset needed to
    reject placeholders and malformed run-ledger artifacts.
    """
    schema = _load_json_object(SCHEMAS / name)
    if Draft202012Validator is None:
        _validate_minimal_schema(schema, value)
    else:
        errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda error: list(error.path))
        if errors:
            raise ValueError(f"{name}: {errors[0].message}")
    if name == "change-plan.schema.json":
        validate_change_plan_semantics(value)


def _parse_event_timestamp(value: str) -> datetime:
    """Return a timezone-aware UTC timestamp for run ordering."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Event timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def _event_chain(run_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Parse and validate the append-only event hash chain for a run directory."""
    events: list[dict[str, Any]] = []
    for line in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        _validate_shape("run-event.schema.json", event)
        events.append(event)
    if not events:
        raise ValueError("Empty event chain")

    parent = None
    for sequence, event in enumerate(events):
        if event["run_id"] != run_dir.name or event["sequence"] != sequence:
            raise ValueError("Event run ID or sequence mismatch")
        if event.get("parent_event_hash") != parent or event["event_hash"] != canonical_hash(event):
            raise ValueError("Event hash chain mismatch")
        _parse_event_timestamp(event["timestamp"])
        parent = event["event_hash"]
    return events, events[-1]


def terminal_event_timestamp(run_dir: Path) -> datetime:
    """Read a valid run's terminal event timestamp from events.jsonl.

    The append-only event chain is validated before the timestamp is trusted.
    Runs without a terminal event, or with missing, malformed, or timezone-naive
    event timestamps, are rejected by raising ValueError.
    """
    _, terminal = _event_chain(run_dir)
    if terminal["state"] not in TERMINAL_RUN_STATES:
        raise ValueError("Terminal event is absent")
    return _parse_event_timestamp(terminal["timestamp"])


def _accept_only_verified_runs(root: Path) -> bool:
    """Return manifest memory.accept_only_verified_runs, defaulting closed."""
    manifest = root / "manifest.yaml"
    try:
        import yaml

        data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        return bool((data or {}).get("memory", {}).get("accept_only_verified_runs", True))
    except Exception:
        in_memory = False
        for raw_line in manifest.read_text(encoding="utf-8").splitlines():
            line = raw_line.rstrip()
            if line.startswith("memory:"):
                in_memory = True
                continue
            if in_memory and line and not line.startswith(" "):
                in_memory = False
            if in_memory and line.strip().startswith("accept_only_verified_runs:"):
                return line.split(":", 1)[1].strip().lower() == "true"
    return True


def is_valid_run_entry(path: Path) -> bool:
    """Return True when a runs/ child is parseable, terminal, and accepted memory."""
    if not path.is_dir():
        return False
    if not all((path / required_file).is_file() for required_file in REQUIRED_RUN_FILES):
        return False

    try:
        _, terminal = _event_chain(path)
        terminal_event_timestamp(path)

        baseline = _load_json_object(path / "baseline.json")
        plan = _load_json_object(path / "plan.json")
        verification = _load_json_object(path / "verification.json")
        result = _load_json_object(path / "result.json")
        for schema, value in (
            ("baseline.schema.json", baseline),
            ("change-plan.schema.json", plan),
            ("verification-result.schema.json", verification),
            ("result.schema.json", result),
        ):
            _validate_shape(schema, value)

        if any(value.get("run_id") != path.name for value in (baseline, plan, verification, result)):
            return False
        if result["status"] != terminal["state"]:
            return False
        validate_verifier_binding(path, baseline, verification)
        validate_terminal_artifact_hashes(path, terminal)
        if _accept_only_verified_runs(CONTROL_PLANE) and verification.get("verdict") != "PASS":
            return False
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError):
        return False
    return True


def classify_run_entries(runs_dir: Path) -> tuple[list[Path], list[str], list[str]]:
    """Split runs/ children into valid evidence, ignored housekeeping, and invalid entries."""
    if not runs_dir.exists():
        return [], [], []

    valid_entries: list[Path] = []
    ignored_entries: list[str] = []
    invalid_entries: list[str] = []
    for path in runs_dir.iterdir():
        if path.name in IGNORED_RUN_FILES:
            ignored_entries.append(path.name)
        elif is_valid_run_entry(path):
            valid_entries.append(path)
        else:
            invalid_entries.append(path.name)

    return (
        sorted(valid_entries, key=lambda path: (terminal_event_timestamp(path), path.name)),
        sorted(ignored_entries),
        sorted(invalid_entries),
    )


def run_entries(runs_dir: Path) -> list[Path]:
    entries, _, _ = classify_run_entries(runs_dir)
    return entries


def directory_digest(path: Path) -> str:
    """Return a deterministic digest for a run directory.

    The digest covers each included file's relative path and bytes so renamed
    files produce a different value even when content is unchanged. Transient
    cache files are excluded to keep evidence stable across local tooling runs.
    """
    h = hashlib.sha256()
    for file_path in sorted(
        (
            candidate
            for candidate in path.rglob("*")
            if candidate.is_file() and not ignored_run_file(path, candidate)
        ),
        key=lambda candidate: candidate.relative_to(path).as_posix(),
    ):
        rel_path = file_path.relative_to(path).as_posix().encode("utf-8")
        h.update(rel_path)
        h.update(b"\0")
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        h.update(b"\0")
    return h.hexdigest()


def ignored_run_file(root: Path, path: Path) -> bool:
    if path.name in IGNORED_RUN_CACHE_FILES:
        return True
    if path.suffix.lower() in IGNORED_RUN_SUFFIXES:
        return True
    return any(part in IGNORED_RUN_DIRS for part in path.relative_to(root).parts[:-1])


def latest_run_digest(path: Path) -> str | None:
    if path.is_file():
        return sha256_file(path)
    if path.is_dir():
        return directory_digest(path)
    return None


def latest_run_evidence(root: Path) -> RunEvidence:
    runs_dir = root / ".claude/control-plane/runs"
    entries, ignored_entries, invalid_entries = classify_run_entries(runs_dir)
    latest = entries[-1] if entries else None
    return RunEvidence(
        state="first-run" if latest is None else "latest-run-found",
        runs_directory=normalize_rel(root, runs_dir),
        latest_run=normalize_rel(root, latest) if latest else None,
        latest_run_sha256=latest_run_digest(latest) if latest else None,
        run_count=len(entries),
        ignored_entries=ignored_entries,
        invalid_entries=invalid_entries,
        evidence_generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def prompt_triggers_workflow(prompt: str) -> bool:
    normalized = " ".join(prompt.lower().split())
    return any(term in normalized for term in TRIGGER_TERMS)


def malformed_payload_hash(raw_payload: str) -> str:
    return hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()


def malformed_payload_event(raw_payload: str, error: str) -> dict[str, str]:
    return {
        "event": "malformed-hook-payload",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "hook_name": HOOK_NAME,
        "error": error,
        "payload_sha256": malformed_payload_hash(raw_payload),
    }


def append_malformed_payload_diagnostic(root: Path, raw_payload: str, error: str) -> bool:
    """Append one diagnostic event for each distinct malformed hook payload.

    The diagnostic intentionally stores only a hash of stdin, never the raw
    prompt or payload contents. Repeated identical malformed payloads are
    treated as already diagnosed so hook retries do not grow an append loop.
    The read-check-append sequence is guarded by an interprocess lock so
    concurrent hook retries for the same payload preserve deterministic dedupe.
    """
    event = malformed_payload_event(raw_payload, error)
    runs_dir = root / ".claude/control-plane/runs"
    diagnostics_path = runs_dir / MALFORMED_PAYLOAD_DIAGNOSTICS
    lock_path = runs_dir / MALFORMED_PAYLOAD_DIAGNOSTICS_LOCK
    runs_dir.mkdir(parents=True, exist_ok=True)

    with _exclusive_lock(lock_path):
        try:
            if diagnostics_path.exists():
                with diagnostics_path.open("r", encoding="utf-8") as existing:
                    for line in existing:
                        try:
                            previous = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if previous.get("payload_sha256") == event["payload_sha256"]:
                            return False

            with diagnostics_path.open("a", encoding="utf-8") as diagnostics:
                diagnostics.write(json.dumps(event, sort_keys=True) + "\n")
            return True
        finally:
            pass


@contextmanager
def _exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_key = str(path.resolve())
    with _THREAD_LOCK_GUARD:
        thread_lock = _THREAD_LOCKS.setdefault(lock_key, threading.Lock())
    with thread_lock:
        with path.open("a+b") as lock_file:
            if lock_file.tell() == 0:
                lock_file.write(b"\0")
                lock_file.flush()
            lock_file.seek(0)
            if sys.platform == "win32":
                import msvcrt

                msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
                try:
                    yield
                finally:
                    lock_file.seek(0)
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                try:
                    yield
                finally:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def hook_response(payload: dict[str, object], evidence: RunEvidence) -> dict[str, object]:
    prompt = str(payload.get("prompt", ""))
    if not prompt_triggers_workflow(prompt):
        return {}
    context = (
        "Invoke workflow .claude/workflows/self-improvement.md for this request. "
        f"Run evidence: state={evidence.state}; run_count={evidence.run_count}; "
        f"latest_run={evidence.latest_run or 'none'}; runs_directory={evidence.runs_directory}. "
        "If candidate improvements require .claude/control-plane/manifest.yaml "
        "changes, stop and request explicit approval before editing it."
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }


def hook_response_for_payload(payload: dict[str, object], root: Path) -> dict[str, object]:
    prompt = str(payload.get("prompt", ""))
    if not prompt_triggers_workflow(prompt):
        return {}
    return hook_response(payload, latest_run_evidence(root))



def _self_check() -> None:
    def expect_minimal_schema_rejects(schema_name: str, candidate: Any, label: str) -> None:
        try:
            _validate_minimal_schema(_load_json_object(SCHEMAS / schema_name), candidate)
        except ValueError:
            return
        raise AssertionError(f"Minimal schema accepted invalid {label}")

    valid_hash = "a" * 64
    valid_baseline = {
        "schema_version": 1,
        "run_id": "cp-20260716-000000-test",
        "repository_root": "/workspace/ULTIMATE",
        "manifest_hash": valid_hash,
        "captured_at": "2026-07-16T00:00:00+00:00",
        "git_identity": {
            "commit_sha": "b" * 40,
            "branch": "main",
            "dirty": False,
            "dirty_summary": {
                "changed_paths": [],
                "staged_count": 0,
                "unstaged_count": 0,
                "untracked_count": 0,
                "diff_hash": valid_hash,
            },
        },
        "artifacts": [
            {
                "path": ".claude/control-plane/manifest.yaml",
                "sha256": valid_hash,
                "size_bytes": 1,
                "kind": "file",
                "source": "control-plane",
                "reason_included": "baseline",
                "snapshot_path": f"baseline-artifacts/{valid_hash}",
                "snapshot_sha256": valid_hash,
            }
        ],
    }
    _validate_minimal_schema(_load_json_object(SCHEMAS / "baseline.schema.json"), valid_baseline)

    bad_file_artifact = json.loads(json.dumps(valid_baseline))
    del bad_file_artifact["artifacts"][0]["snapshot_sha256"]
    expect_minimal_schema_rejects(
        "baseline.schema.json",
        bad_file_artifact,
        "file artifact without dependent snapshot_sha256",
    )

    bad_symlink_artifact = json.loads(json.dumps(valid_baseline))
    bad_symlink_artifact["artifacts"][0] = {
        "path": ".claude/link",
        "sha256": valid_hash,
        "size_bytes": 8,
        "kind": "symlink",
        "source": "control-plane",
        "reason_included": "baseline",
    }
    expect_minimal_schema_rejects(
        "baseline.schema.json",
        bad_symlink_artifact,
        "symlink artifact without link_target",
    )

    bad_directory_artifact = json.loads(json.dumps(valid_baseline))
    bad_directory_artifact["artifacts"][0] = {
        "path": ".claude",
        "sha256": valid_hash,
        "size_bytes": 0,
        "kind": "directory",
        "source": "control-plane",
        "reason_included": "baseline",
        "link_target": "target",
    }
    expect_minimal_schema_rejects(
        "baseline.schema.json",
        bad_directory_artifact,
        "non-symlink artifact with link_target",
    )

    bad_pattern_artifact = json.loads(json.dumps(valid_baseline))
    bad_pattern_artifact["artifacts"][0]["sha256"] = "not-a-sha"
    expect_minimal_schema_rejects(
        "baseline.schema.json",
        bad_pattern_artifact,
        "artifact with malformed sha256",
    )

    bad_minimum_artifact = json.loads(json.dumps(valid_baseline))
    bad_minimum_artifact["artifacts"][0]["size_bytes"] = -1
    expect_minimal_schema_rejects(
        "baseline.schema.json",
        bad_minimum_artifact,
        "artifact with negative size_bytes",
    )

    bad_min_length_artifact = json.loads(json.dumps(valid_baseline))
    bad_min_length_artifact["artifacts"][0]["path"] = ""
    expect_minimal_schema_rejects(
        "baseline.schema.json",
        bad_min_length_artifact,
        "artifact with empty path",
    )

    trigger_examples = {
        "Implement recursive control-plane self-improvement.": True,
        "Invoke .claude/workflows/self-improvement.md for this update.": True,
        "Run self-improvement.md before planning changes.": True,
        "Update README wording.": False,
        "Open .claude/workflows/release.md for packaging guidance.": False,
    }
    for prompt, expected in trigger_examples.items():
        actual = prompt_triggers_workflow(prompt)
        if actual != expected:
            raise AssertionError(
                f"Expected trigger={expected} for {prompt!r}, got {actual}"
            )

    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp) / ".claude/control-plane/runs/cp-20260718-000001-alias"
        run_dir.mkdir(parents=True)
        digest = hashlib.sha256(b"x\n").hexdigest()
        timestamp = "2026-07-18T00:00:00+00:00"
        baseline = {
            "schema_version": 1,
            "run_id": run_dir.name,
            "repository_root": str(run_dir.parents[3]),
            "manifest_hash": "0" * 64,
            "captured_at": timestamp,
            "git_identity": {
                "commit_sha": "0" * 40,
                "branch": "main",
                "dirty": False,
                "dirty_summary": {
                    "changed_paths": [],
                    "staged_count": 0,
                    "unstaged_count": 0,
                    "untracked_count": 0,
                    "diff_hash": "0" * 64,
                },
            },
            "artifacts": [{
                "path": "x.txt",
                "sha256": digest,
                "size_bytes": 2,
                "kind": "file",
                "source": "control-plane-tree",
                "reason_included": "self-check",
                "resolved_within_repository": True,
                "snapshot_path": f"baseline-artifacts/{digest}",
                "snapshot_sha256": digest,
            }],
        }
        plan = {
            "schema_version": 1,
            "run_id": run_dir.name,
            "owner": "workflow-specialist",
            "request": "self-check",
            "repository_root": str(run_dir.parents[3]),
            "manifest_hash": "0" * 64,
            "artifacts": [
                {
                    "path": "x.txt",
                    "operation": "update",
                    "reason": "self-check",
                    "risk": "low",
                    "precondition_hash": digest,
                },
                {
                    "path": "x.txt",
                    "operation": "delete",
                    "reason": "duplicate identity",
                    "risk": "low",
                    "precondition_hash": digest,
                },
            ],
            "read_artifacts": ["x.txt"],
            "interfaces": [],
            "verification": [{
                "assertion_id": "SELF_CHECK",
                "kind": "behavior",
                "description": "self-check",
                "required": True,
            }],
            "rollback": {"strategy": "restore-baseline", "baseline_path": "baseline.json"},
            "risk": "low",
        }
        verification = {
            "schema_version": 1,
            "run_id": run_dir.name,
            "verdict": "PASS",
            "verifier": "self-check",
            "verified_at": timestamp,
            "assertions": [{
                "assertion_id": "SELF_CHECK",
                "result": "PASS",
                "explanation": "self-check evidence",
                "evidence_locations": ["x.txt"],
            }],
            "evidence": {},
            "author_context_separate": True,
        }
        result = {
            "schema_version": 1,
            "run_id": run_dir.name,
            "status": "COMMITTED",
            "owner": "workflow-specialist",
            "started_at": timestamp,
            "finished_at": timestamp,
            "changed_artifacts": [{"path": "x.txt", "final_hash": digest}],
            "verification_path": "verification.json",
            "rollback_performed": False,
        }
        event = {
            "schema_version": 1,
            "run_id": run_dir.name,
            "sequence": 0,
            "timestamp": timestamp,
            "state": "COMMITTED",
            "actor": "self-check",
            "event_type": "terminal",
            "parent_event_hash": None,
        }
        event["event_hash"] = canonical_hash(event)
        snapshot = run_dir / "baseline-artifacts" / digest
        snapshot.parent.mkdir()
        snapshot.write_bytes(b"x\n")
        for name, value in (
            ("baseline.json", baseline),
            ("plan.json", plan),
            ("verification.json", verification),
            ("result.json", result),
        ):
            (run_dir / name).write_text(json.dumps(value), encoding="utf-8")
        (run_dir / "events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
        if is_valid_run_entry(run_dir):
            raise AssertionError("Aliased artifact paths must invalidate the run entry")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        if hook_response_for_payload({"prompt": "Update README wording."}, root) != {}:
            raise AssertionError("Unrelated prompts must return before run-ledger traversal")
        valid_response = hook_response_for_payload(
            {"prompt": "Implement recursive control-plane self-improvement."},
            root,
        )
        if valid_response.get("hookSpecificOutput", {}).get("hookEventName") != HOOK_NAME:
            raise AssertionError("Triggering prompts must produce hook context")

    raw_payload = '{"prompt": "unterminated"'
    error = "self-check malformed JSON"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        barrier = threading.Barrier(16)

        def append_once() -> bool:
            barrier.wait()
            return append_malformed_payload_diagnostic(root, raw_payload, error)

        with ThreadPoolExecutor(max_workers=16) as executor:
            results = list(executor.map(lambda _: append_once(), range(16)))

        diagnostics_path = root / ".claude/control-plane/runs" / MALFORMED_PAYLOAD_DIAGNOSTICS
        lines = diagnostics_path.read_text(encoding="utf-8").splitlines()
        if results.count(True) != 1 or results.count(False) != 15:
            raise AssertionError(f"Expected one append and fifteen duplicates, got {results}")
        if len(lines) != 1:
            raise AssertionError(f"Expected one diagnostic event, got {len(lines)}")
        event = json.loads(lines[0])
        if event.get("payload_sha256") != malformed_payload_hash(raw_payload):
            raise AssertionError("Diagnostic event did not record the payload hash")
        if raw_payload in lines[0] or "unterminated" in lines[0]:
            raise AssertionError("Diagnostic event leaked raw payload content")


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit recursive self-improvement run evidence.")
    parser.add_argument(
        "--hook",
        action="store_true",
        help="Read UserPromptSubmit JSON on stdin and emit hook JSON.",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Run the malformed-payload concurrent append self-check.",
    )
    args = parser.parse_args()

    if args.self_check:
        _self_check()
        return 0

    root = find_repo_root()
    if not args.hook:
        evidence = latest_run_evidence(root)
        print(json.dumps(asdict(evidence), indent=2, sort_keys=True))
        return 0

    raw_payload = sys.stdin.read()
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        error = str(exc)
        append_malformed_payload_diagnostic(root, raw_payload, error)
        print(json.dumps({"decision": "block", "reason": f"Invalid hook JSON: {error}"}))
        return 0
    print(json.dumps(hook_response_for_payload(payload, root), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
