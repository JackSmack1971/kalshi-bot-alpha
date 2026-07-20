from __future__ import annotations

import argparse
import concurrent.futures
import copy
import datetime as dt
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

import validate
from candidate_emitter import (
    artifact_identity,
    candidate_artifact_by_name,
    validate_candidate_authorization,
    validate_candidate_package,
)
from common import (
    REQUIRED_TERMINAL_ARTIFACTS,
    TRUSTED_VERIFIER_PATH,
    sha256_file,
    validate_change_plan_semantics,
    validate_terminal_artifact_hashes,
    validate_verifier_binding,
)
from new_run import canonical_hash, write_json_exclusive


SCRIPT_DIR = Path(__file__).resolve().parent
CONTROL_PLANE = SCRIPT_DIR.parent
SCHEMAS = CONTROL_PLANE / "schemas"
REPLAY_VERSION = "1"
HARNESS_VERSION = "replay.py/1"
TERMINAL = {"COMMITTED", "ROLLED_BACK", "FAILED"}
CLASSIFICATIONS = {"IMPROVED", "REGRESSED", "TIED", "INDETERMINATE"}


def _utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def _validate_shape(name: str, value: Any) -> None:
    schema = _load_json(SCHEMAS / name)
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.path))
    if errors:
        raise ValueError(f"{name}: {errors[0].message}")
    if name == "change-plan.schema.json":
        validate_change_plan_semantics(value)


def _canonical_json_hash(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _safe_parts(value: str) -> tuple[str, ...]:
    raw_parts = value.replace("\\", "/").split("/")
    identity = artifact_identity(value)
    parts = tuple(identity.split("/"))
    if (
        not identity
        or value.startswith(("/", "\\"))
        or ":" in parts[0]
        or any(part in {"", ".", ".."} for part in raw_parts)
    ):
        raise ValueError(f"Unsafe repository-relative path: {value!r}")
    return parts


def _parse_timestamp(value: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Terminal timestamp must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def _paths_overlap(left: str, right: str) -> bool:
    a, b = _safe_parts(left), _safe_parts(right)
    shorter = min(len(a), len(b))
    return a[:shorter] == b[:shorter]


def _inside(root: Path, relative: str) -> Path:
    _safe_parts(relative)
    root = root.resolve()
    path = (root / relative).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path escapes root: {relative}") from exc
    return path


def _event_chain(run_dir: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    events = []
    for line in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines():
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
        parent = event["event_hash"]
    return events, events[-1]


def _failure_paths(verification: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for assertion in verification.get("assertions", []):
        if assertion.get("result") not in {"FAIL", "INDETERMINATE"}:
            continue
        for value in assertion.get("evidence_locations", []):
            if isinstance(value, str):
                try:
                    _safe_parts(value)
                except ValueError:
                    continue
                paths.append(value)
    return paths


def _inspect_run(run_dir: Path, boundary: list[str]) -> dict[str, Any] | None:
    try:
        events, terminal = _event_chain(run_dir)
        if terminal["state"] not in TERMINAL:
            return None
        baseline = _load_json(run_dir / "baseline.json")
        plan = _load_json(run_dir / "plan.json")
        result = _load_json(run_dir / "result.json")
        verification = _load_json(run_dir / "verification.json")
        for schema, value in (
            ("baseline.schema.json", baseline),
            ("change-plan.schema.json", plan),
            ("result.schema.json", result),
            ("verification-result.schema.json", verification),
        ):
            _validate_shape(schema, value)
        if any(value.get("run_id") != run_dir.name for value in (baseline, plan, result, verification)):
            raise ValueError("Historical run ID mismatch")
        if result["status"] != terminal["state"]:
            raise ValueError("Terminal event and result disagree")
        validate_verifier_binding(run_dir, baseline, verification)
        validate_terminal_artifact_hashes(run_dir, terminal)
        scope = list(plan.get("read_artifacts", []))
        scope.extend(item["path"] for item in plan["artifacts"])
        scope.extend(item["path"] for item in result["changed_artifacts"])
        if terminal["state"] == "FAILED":
            scope.extend(_failure_paths(verification))
        if not any(_paths_overlap(candidate, historical) for candidate in boundary for historical in scope):
            return None
        return {
            "run_dir": run_dir,
            "run_id": run_dir.name,
            "terminal_status": terminal["state"],
            "timestamp": terminal["timestamp"],
            "sort_timestamp": _parse_timestamp(terminal["timestamp"]),
            "baseline": baseline,
            "plan": plan,
            "result": result,
            "verification": verification,
            "events": events,
        }
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError):
        return None


def select_corpus(runs_dir: Path, boundary: list[str], corpus_filter: list[str]) -> list[dict[str, Any]]:
    allowed = set(corpus_filter)
    selected = []
    for run_dir in runs_dir.iterdir() if runs_dir.is_dir() else ():
        if not run_dir.is_dir() or (allowed and run_dir.name not in allowed):
            continue
        item = _inspect_run(run_dir, boundary)
        if item:
            selected.append(item)
    return sorted(selected, key=lambda item: (item["sort_timestamp"], item["run_id"]))


def _source_files(item: dict[str, Any]) -> list[Path]:
    run_dir = item["run_dir"]
    files = [run_dir / name for name in ("baseline.json", "plan.json", "result.json", "verification.json", "events.jsonl")]
    for artifact in item["baseline"]["artifacts"]:
        snapshot = artifact.get("snapshot_path")
        if snapshot:
            files.append(_inside(run_dir, snapshot))
    return files


def _source_hash(item: dict[str, Any]) -> str:
    records = []
    for path in _source_files(item):
        relative = path.relative_to(item["run_dir"]).as_posix()
        records.append([relative, sha256_file(path) if path.is_file() else "MISSING"])
    return _canonical_json_hash(records)


def _symlink_resolution(root: Path, link_path: Path, link_target: str) -> Path:
    target = Path(link_target)
    if target.is_absolute():
        resolved = target.resolve(strict=False)
    else:
        resolved = (link_path.parent / target).resolve(strict=False)
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Baseline symlink escapes reconstructed workspace: {link_path.relative_to(root).as_posix()}") from exc
    return resolved


def _reconstruct(item: dict[str, Any], destination: Path) -> tuple[str, str]:
    records = []
    for artifact in item["baseline"]["artifacts"]:
        target = _inside(destination, artifact["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        if artifact["kind"] == "symlink":
            link_target = artifact.get("link_target")
            if not isinstance(link_target, str):
                raise ValueError(f"Missing replayable symlink target: {artifact['path']}")
            link_bytes = link_target.encode("utf-8")
            digest = hashlib.sha256(link_bytes).hexdigest()
            if digest != artifact["sha256"] or len(link_bytes) != artifact["size_bytes"]:
                raise ValueError(f"Baseline symlink hash mismatch: {artifact['path']}")
            _symlink_resolution(destination, target, link_target)
            target.symlink_to(link_target)
            records.append([artifact["path"], digest])
            continue
        if artifact["kind"] != "file" or not artifact.get("snapshot_path"):
            raise ValueError(f"Missing replayable file snapshot: {artifact['path']}")
        source = _inside(item["run_dir"], artifact["snapshot_path"])
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"Unsupported baseline snapshot: {artifact['path']}")
        snapshot_bytes = source.read_bytes()
        digest = hashlib.sha256(snapshot_bytes).hexdigest()
        if digest != artifact["sha256"] or digest != artifact["snapshot_sha256"]:
            raise ValueError(f"Baseline snapshot hash mismatch: {artifact['path']}")
        target.write_bytes(snapshot_bytes)
        records.append([artifact["path"], digest])
    return sha256_file(item["run_dir"] / "baseline.json"), _canonical_json_hash(records)


def _validation_errors(workspace: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    validate.validate_required_files(workspace, errors)
    validate.validate_agents(workspace, errors)
    validate.validate_manifest(workspace, errors, warnings)
    validate.validate_json_schema_files(workspace, errors, warnings)
    return len(errors)


EVALUATORS: dict[str, Callable[[Path], int]] = {
    "control-plane-validation-errors": _validation_errors,
}


def _classify_effect(effect: int, minimum_effect: int) -> str:
    if effect < 0:
        return "REGRESSED"
    if effect >= minimum_effect:
        return "IMPROVED"
    return "TIED"


def _within_boundary(path: str, boundary: list[str]) -> bool:
    parts = _safe_parts(path)
    return any(parts[: len(allowed)] == allowed for allowed in map(_safe_parts, boundary))


def _tree_identities(root: Path) -> dict[str, str]:
    identities = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            identities[relative] = f"link:{path.readlink()}"
        elif path.is_file():
            identities[relative] = f"file:{sha256_file(path)}"
    return identities


def _aggregate(results: list[dict[str, Any]], minimum_evidence_count: int) -> str:
    classes = [result["classification"] for result in results]
    evaluated = sum(value != "INDETERMINATE" for value in classes)
    if "INDETERMINATE" in classes or evaluated < minimum_evidence_count:
        return "INDETERMINATE"
    if "REGRESSED" in classes:
        return "REGRESSED"
    if "IMPROVED" in classes:
        return "IMPROVED"
    return "TIED"


def _error(code: str, stage: str, message: str, run_id: str | None = None) -> dict[str, Any]:
    value = {"code": code, "stage": stage, "message": message}
    if run_id:
        value["source_run_id"] = run_id
    return value


def _result(item: dict[str, Any], error: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "source_run_id": item["run_id"],
        "terminal_status": item["terminal_status"],
        "terminal_timestamp": item["timestamp"],
        "baseline_hash": None,
        "input_hash": None,
        "baseline_metric": None,
        "candidate_metric": None,
        "effect": None,
        "classification": "INDETERMINATE",
        "error": error,
    }


def _compare(
    item: dict[str, Any],
    patch_bytes: bytes,
    evaluator: Callable[[Path], int],
    minimum_effect: int,
    boundary: list[str],
) -> dict[str, Any]:
    run_id = item["run_id"]
    base = _result(item)
    try:
        before = _source_hash(item)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            private_patch = root / "candidate.patch"
            private_patch.write_bytes(patch_bytes)
            origin = root / "origin"
            origin.mkdir()
            base["baseline_hash"], base["input_hash"] = _reconstruct(item, origin)
            baseline_workspace = root / "baseline"
            candidate_workspace = root / "candidate"
            shutil.copytree(origin, baseline_workspace, symlinks=True)
            shutil.copytree(origin, candidate_workspace, symlinks=True)
            base["baseline_metric"] = evaluator(baseline_workspace)
            check = subprocess.run(
                ["git", "apply", "--check", str(private_patch)],
                cwd=candidate_workspace,
                shell=False,
                capture_output=True,
                text=True,
            )
            if check.returncode:
                base["candidate_metric"] = base["baseline_metric"] + 1
                base["effect"] = -1
                base["classification"] = "REGRESSED"
                base["error"] = _error("PATCH_INCOMPATIBLE", "candidate", "Candidate patch does not apply", run_id)
            else:
                applied = subprocess.run(
                    ["git", "apply", str(private_patch)],
                    cwd=candidate_workspace,
                    shell=False,
                    capture_output=True,
                    text=True,
                )
                if applied.returncode:
                    raise RuntimeError("git apply failed after successful check")
                before_tree = _tree_identities(baseline_workspace)
                after_tree = _tree_identities(candidate_workspace)
                changed = set(before_tree) | set(after_tree)
                changed = {path for path in changed if before_tree.get(path) != after_tree.get(path)}
                if not changed or any(not _within_boundary(path, boundary) for path in changed):
                    raise RuntimeError("Applied patch violates the declared candidate boundary")
                if any(after_tree.get(path, "").startswith("link:") for path in changed):
                    raise RuntimeError("Applied patch creates an unsupported symbolic link")
                base["candidate_metric"] = evaluator(candidate_workspace)
                base["effect"] = base["baseline_metric"] - base["candidate_metric"]
                base["classification"] = _classify_effect(base["effect"], minimum_effect)
        if before != _source_hash(item):
            raise RuntimeError("Historical source mutated during replay")
        return base
    except Exception as exc:
        base["classification"] = "INDETERMINATE"
        base["error"] = _error("REPLAY_INPUT_ERROR", "evaluation", str(exc), run_id)
        return base


def _counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"total": len(results), "evaluated": 0, "improved": 0, "regressed": 0, "tied": 0, "indeterminate": 0}
    for result in results:
        key = result["classification"].lower()
        counts[key] += 1
        if result["classification"] != "INDETERMINATE":
            counts["evaluated"] += 1
    return counts


def _verified_classification(result: dict[str, Any], minimum_effect: int) -> str:
    metrics = (result["baseline_metric"], result["candidate_metric"])
    complete = all(isinstance(value, int) and not isinstance(value, bool) for value in metrics)
    if complete:
        expected_effect = metrics[0] - metrics[1]
        if result["effect"] != expected_effect:
            raise ValueError("Replay effect does not match recorded metrics")
    elif any(value is not None for value in (*metrics, result["effect"])):
        raise ValueError("Replay metrics and effect must be complete or null")

    error = result["error"]
    if error is not None:
        if error["code"] == "PATCH_INCOMPATIBLE":
            if not complete or _classify_effect(result["effect"], minimum_effect) != "REGRESSED":
                raise ValueError("Incompatible patch evidence must prove a regression")
            return "REGRESSED"
        return "INDETERMINATE"
    if not complete:
        raise ValueError("Determinate replay evidence requires complete metrics")
    return _classify_effect(result["effect"], minimum_effect)


def validate_replay_result(value: dict[str, Any], output: Path | None = None) -> dict[str, Any]:
    _validate_shape("replay-result.schema.json", value)
    results = value["results"]
    ids = [result["source_run_id"] for result in results]
    if ids != value["source_run_ids"] or len(ids) != len(set(ids)):
        raise ValueError("Replay source IDs disagree or repeat")
    ordering = [(_parse_timestamp(result["terminal_timestamp"]), result["source_run_id"]) for result in results]
    if ordering != sorted(ordering):
        raise ValueError("Replay results are not ordered by terminal timestamp and run ID")
    verified = []
    for result in results:
        classification = _verified_classification(result, value["minimum_effect"])
        if result["classification"] != classification:
            raise ValueError("Replay classification does not match evidence")
        verified.append({"classification": classification})
    expected = _aggregate(verified, value["minimum_evidence_count"])
    if value["aggregate"] != {"classification": expected, "counts": _counts(verified)}:
        raise ValueError("Replay aggregate does not match evidence")
    if output and (output.name != "result.json" or output.parent.name != value["replay_id"]):
        raise ValueError("Replay path and embedded ID disagree")
    return value


def load_replay(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError("Replay attempt has no complete final marker")
    return validate_replay_result(_load_json(path), path)


def _candidate(candidate_run: Path) -> tuple[dict[str, Any], dict[str, Any], bytes]:
    package = _load_json(candidate_run / "candidate-package.json")
    _validate_shape("candidate-package.schema.json", package)
    validate_candidate_package(candidate_run, package)
    validate_candidate_authorization(candidate_run, package)
    policy_artifact = candidate_artifact_by_name(package, "hypothesis-policy.json")
    policy_path = _inside(candidate_run, policy_artifact["path"])
    policy_bytes = policy_path.read_bytes()
    if hashlib.sha256(policy_bytes).hexdigest() != package["hypothesis_policy_hash"]:
        raise ValueError("Candidate policy hash mismatch")
    policy = json.loads(policy_bytes.decode("utf-8"))
    if policy["hypothesis_id"] != package["hypothesis_id"]:
        raise ValueError("Candidate policy ID mismatch")
    evaluator = policy.get("evaluator")
    if evaluator not in EVALUATORS:
        raise ValueError("Candidate evaluator is not allowlisted")
    patch_artifact = candidate_artifact_by_name(package, "proposed.patch")
    patch_bytes = _inside(candidate_run, patch_artifact["path"]).read_bytes()
    if hashlib.sha256(patch_bytes).hexdigest() != package["patch_hash"]:
        raise ValueError("Candidate patch hash mismatch")
    return package, policy, patch_bytes


def _evidence(
    replay_id: str,
    package: dict[str, Any],
    policy: dict[str, Any],
    started: str,
    results: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    corpus_filter: list[str],
) -> dict[str, Any]:
    evidence: dict[str, Any] = {
        "schema_version": 1,
        "replay_version": REPLAY_VERSION,
        "harness_version": HARNESS_VERSION,
        "replay_id": replay_id,
        "candidate_id": package["candidate_id"],
        "candidate_run_id": package["run_id"],
        "hypothesis_id": package["hypothesis_id"],
        "candidate_package_hash": package["package_hash"],
        "candidate_patch_hash": package["patch_hash"],
        "hypothesis_policy_hash": package["hypothesis_policy_hash"],
        "source_run_ids": [result["source_run_id"] for result in results],
        "success_criterion": policy["success_criteria"],
        "evaluator": policy["evaluator"],
        "minimum_effect": policy["minimum_effect"],
        "minimum_evidence_count": policy["minimum_evidence_count"],
        "started_at": started,
        "finished_at": _utc_now(),
        "results": results,
        "aggregate": {
            "classification": _aggregate(results, policy["minimum_evidence_count"]),
            "counts": _counts(results),
        },
        "errors": errors,
    }
    if corpus_filter:
        evidence["corpus_filter"] = corpus_filter
    return evidence


def _fail_attempt(
    selected: list[dict[str, Any]],
    results: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    exc: Exception,
) -> None:
    failure = _error("ATTEMPT_FAILURE", "publication", str(exc) or type(exc).__name__)
    errors.append(failure)
    by_id = {result["source_run_id"]: result for result in results}
    for item in selected:
        result = by_id.get(item["run_id"])
        run_error = _error(failure["code"], failure["stage"], failure["message"], item["run_id"])
        if result is None:
            results.append(_result(item, run_error))
        else:
            result["classification"] = "INDETERMINATE"
            result["error"] = run_error


def replay(candidate_run: Path, corpus_filter: list[str] | None = None) -> Path:
    candidate_run = candidate_run.resolve()
    package, policy, patch_bytes = _candidate(candidate_run)
    corpus_filter = list(dict.fromkeys(corpus_filter or []))
    if any(not isinstance(run_id, str) or not run_id for run_id in corpus_filter):
        raise ValueError("Corpus filters must be non-empty run IDs")
    selected = select_corpus(candidate_run.parent, package["diff_boundary"]["allowed_paths"], corpus_filter)
    replay_id = f"replay-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(4)}"
    attempt = candidate_run / "replay" / replay_id
    attempt.mkdir(parents=True, exist_ok=False)
    started = _utc_now()
    errors: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    try:
        source_hashes = {}
        for item in selected:
            try:
                source_hashes[item["run_id"]] = _source_hash(item)
            except Exception as exc:
                error = _error("SOURCE_READ_ERROR", "corpus", str(exc), item["run_id"])
                results.append(_result(item, error))
                errors.append(error)
                continue
            result = _compare(
                item,
                patch_bytes,
                EVALUATORS[policy["evaluator"]],
                policy["minimum_effect"],
                package["diff_boundary"]["allowed_paths"],
            )
            results.append(result)
            if result["error"]:
                errors.append(result["error"])
        if not selected:
            errors.append(_error("NO_ELIGIBLE_HISTORY", "corpus", "No schema-valid terminal overlapping history"))
        current_package, current_policy, current_patch = _candidate(candidate_run)
        if current_package != package or current_policy != policy or current_patch != patch_bytes:
            raise ValueError("Candidate evidence mutated during replay")
        for item in selected:
            if item["run_id"] in source_hashes and _source_hash(item) != source_hashes[item["run_id"]]:
                raise ValueError(f"Historical source mutated: {item['run_id']}")
        evidence = _evidence(replay_id, package, policy, started, results, errors, corpus_filter)
        validate_replay_result(evidence, attempt / "result.json")
    except Exception as exc:
        _fail_attempt(selected, results, errors, exc)
        evidence = _evidence(replay_id, package, policy, started, results, errors, corpus_filter)
        validate_replay_result(evidence, attempt / "result.json")
    write_json_exclusive(attempt / "result.json", evidence)
    return attempt / "result.json"


def _fixture_replay_check() -> None:
    from candidate_emitter import _package_hash
    from unittest import mock

    def write_candidate(run_dir: Path, manifest: Path) -> tuple[dict[str, Any], Path]:
        run_dir.mkdir()
        policy = {
            "evaluator": "control-plane-validation-errors",
            "hypothesis_id": "hypothesis",
            "minimum_effect": 1,
            "minimum_evidence_count": 1,
            "success_criteria": "fewer validation errors",
        }
        plan = {
            "schema_version": 1,
            "run_id": run_dir.name,
            "owner": "workflow-specialist",
            "request": "self-check",
            "repository_root": str(manifest.parents[2]),
            "manifest_hash": sha256_file(manifest),
            "artifacts": [{
                "path": "x.txt",
                "operation": "update",
                "reason": "self-check",
                "risk": "low",
                "precondition_hash": hashlib.sha256(b"old\n").hexdigest(),
            }],
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
        payloads = {
            "plan.json": (json.dumps(plan) + "\n").encode(),
            "proposed.patch": (
                b"diff --git a/x.txt b/x.txt\n"
                b"--- a/x.txt\n+++ b/x.txt\n@@ -1 +1 @@\n-old\n+new\n"
            ),
            "diff-boundary.json": b'{"allowed_paths":["x.txt"]}',
            "hypothesis-policy.json": json.dumps(policy, sort_keys=True, separators=(",", ":")).encode(),
        }
        artifacts = []
        artifact_dir = run_dir / "candidate-artifacts"
        artifact_dir.mkdir()
        for name in ("plan.json", "proposed.patch", "diff-boundary.json", "hypothesis-policy.json"):
            digest = hashlib.sha256(payloads[name]).hexdigest()
            path = artifact_dir / f"{digest}-{name}"
            path.write_bytes(payloads[name])
            artifacts.append({"path": path.relative_to(run_dir).as_posix(), "sha256": digest})
        package = {
            "schema_version": 1,
            "candidate_id": "candidate",
            "run_id": run_dir.name,
            "hypothesis_id": "hypothesis",
            "patch_hash": artifacts[1]["sha256"],
            "hypothesis_policy_hash": artifacts[3]["sha256"],
            "package_hash": "",
            "diff_boundary": {"allowed_paths": ["x.txt"]},
            "artifacts": artifacts,
        }
        package["package_hash"] = _package_hash(package)
        (run_dir / "candidate-package.json").write_text(json.dumps(package), encoding="utf-8")
        return package, artifact_dir / f"{artifacts[3]['sha256']}-hypothesis-policy.json"

    def write_history(
        runs: Path,
        run_id: str,
        status: str,
        timestamp: str,
        content: bytes = b"old\n",
        snapshots: bool = True,
    ) -> Path:
        run_dir = runs / run_id
        run_dir.mkdir()
        digest = hashlib.sha256(content).hexdigest()
        verifier_bytes = b"""---
name: control-plane-verifier
description: self-check verifier
---
"""
        verifier_digest = hashlib.sha256(verifier_bytes).hexdigest()
        artifact = {
            "path": "x.txt",
            "sha256": digest,
            "size_bytes": len(content),
            "kind": "file",
            "source": "control-plane-tree",
            "reason_included": "self-check",
            "resolved_within_repository": True,
        }
        if snapshots:
            snapshot = run_dir / "baseline-artifacts" / digest
            snapshot.parent.mkdir()
            snapshot.write_bytes(content)
            artifact.update(snapshot_path=f"baseline-artifacts/{digest}", snapshot_sha256=digest)
            verifier_snapshot = run_dir / "baseline-artifacts" / verifier_digest
            verifier_snapshot.write_bytes(verifier_bytes)
            verifier_artifact = {
                "path": TRUSTED_VERIFIER_PATH,
                "sha256": verifier_digest,
                "size_bytes": len(verifier_bytes),
                "kind": "file",
                "source": "control-plane-tree",
                "reason_included": "self-check verifier binding",
                "snapshot_path": f"baseline-artifacts/{verifier_digest}",
                "snapshot_sha256": verifier_digest,
            }
        else:
            verifier_artifact = {
                "path": TRUSTED_VERIFIER_PATH,
                "sha256": verifier_digest,
                "size_bytes": len(verifier_bytes),
                "kind": "file",
                "source": "control-plane-tree",
                "reason_included": "self-check verifier binding",
            }
        baseline = {
            "schema_version": 1,
            "run_id": run_id,
            "repository_root": str(runs.parent),
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
            "artifacts": [artifact, verifier_artifact],
        }
        plan = {
            "schema_version": 1,
            "run_id": run_id,
            "owner": "workflow-specialist",
            "request": "self-check",
            "repository_root": str(runs.parent),
            "manifest_hash": "0" * 64,
            "artifacts": [{
                "path": "x.txt",
                "operation": "update",
                "reason": "self-check",
                "risk": "low",
                "precondition_hash": digest,
            }],
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
            "run_id": run_id,
            "verdict": "FAIL" if status == "FAILED" else "PASS",
            "verifier": "control-plane-verifier",
            "verified_at": timestamp,
            "assertions": [{
                "assertion_id": "SELF_CHECK",
                "result": "FAIL" if status == "FAILED" else "PASS",
                "explanation": "self-check evidence",
                "evidence_locations": ["x.txt"],
            }],
            "evidence": {
                "verifier_identity": {
                    "path": TRUSTED_VERIFIER_PATH,
                    "sha256": verifier_digest,
                }
            },
            "author_context_separate": True,
        }
        result = {
            "schema_version": 1,
            "run_id": run_id,
            "status": status,
            "owner": "workflow-specialist",
            "started_at": timestamp,
            "finished_at": timestamp,
            "changed_artifacts": [{"path": "x.txt", "final_hash": digest}],
            "verification_path": "verification.json",
            "rollback_performed": status == "ROLLED_BACK",
        }
        for name, value in (("baseline.json", baseline), ("plan.json", plan), ("verification.json", verification), ("result.json", result)):
            (run_dir / name).write_text(json.dumps(value), encoding="utf-8")
        event = {
            "schema_version": 1,
            "run_id": run_id,
            "sequence": 0,
            "timestamp": timestamp,
            "state": status,
            "actor": "self-check",
            "event_type": "terminal",
            "artifact_hashes": {
                artifact_name: sha256_file(run_dir / artifact_name)
                for artifact_name in REQUIRED_TERMINAL_ARTIFACTS
            },
            "parent_event_hash": None,
        }
        event["event_hash"] = canonical_hash(event)
        (run_dir / "events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
        return run_dir

    with tempfile.TemporaryDirectory() as temporary:
        repo_root = Path(temporary) / "repo"
        manifest = repo_root / ".claude" / "control-plane" / "manifest.yaml"
        manifest.parent.mkdir(parents=True)
        manifest.write_text(
            """schema_version: 1
control_plane_roots:
  - .claude/
  - AGENTS.md
forbidden_roots:
  - src/
  - .git/
  - secrets/
  - credentials/
owners:
  workflow-specialist:
    - x.txt
verification:
  independent_verifier_required: true
  rollback_on_failure: true
  fresh_session_behavioral_evals: true
  baseline_comparison_required_for_skills: true
budgets:
  max_concurrent_writers: 1
  max_nested_agent_depth: 0
experimental_features:
  agent_teams:
    default: disabled
    require_explicit_enablement: true
memory:
  accept_only_verified_runs: true
runs:
  directory: .claude/control-plane/runs
  append_only_events: true
  hash_chain_events: true
""",
            encoding="utf-8",
        )
        runs = repo_root / ".claude" / "control-plane" / "runs"
        runs.mkdir(parents=True)
        candidate_run = runs / "candidate-run"
        package, policy_path = write_candidate(candidate_run, manifest)

        empty = load_replay(replay(candidate_run))
        assert empty["aggregate"]["classification"] == "INDETERMINATE"
        assert empty["source_run_ids"] == []

        committed = write_history(runs, "cp-20260716-000003-aaaa", "COMMITTED", "2026-07-16T00:00:03+00:00")
        rolled = write_history(runs, "cp-20260716-000001-bbbb", "ROLLED_BACK", "2026-07-16T00:00:01+00:00")
        failed = write_history(runs, "cp-20260716-000002-cccc", "FAILED", "2026-07-16T00:00:02+00:00")
        cancelled = runs / "cp-20260716-000004-dddd"
        cancelled.mkdir()
        cancelled_event = {
            "schema_version": 1, "run_id": cancelled.name, "sequence": 0,
            "timestamp": "2026-07-16T00:00:04+00:00", "state": "CANCELLED",
            "actor": "self-check", "event_type": "terminal", "parent_event_hash": None,
        }
        cancelled_event["event_hash"] = canonical_hash(cancelled_event)
        (cancelled / "events.jsonl").write_text(json.dumps(cancelled_event) + "\n", encoding="utf-8")

        selected = select_corpus(runs, ["x.txt"], [])
        assert [item["run_id"] for item in selected] == [rolled.name, failed.name, committed.name]
        assert {item["terminal_status"] for item in selected} == TERMINAL
        filtered = load_replay(replay(candidate_run, [failed.name]))
        assert filtered["source_run_ids"] == [failed.name]
        assert filtered["aggregate"]["classification"] == "TIED"

        incompatible = write_history(
            runs, "cp-20260716-000005-eeee", "COMMITTED", "2026-07-16T00:00:05+00:00", b"other\n"
        )
        incompatible_result = load_replay(replay(candidate_run, [incompatible.name]))
        assert incompatible_result["aggregate"]["classification"] == "REGRESSED"
        assert incompatible_result["results"][0]["error"]["code"] == "PATCH_INCOMPATIBLE"

        legacy = write_history(
            runs, "cp-20260716-000006-ffff", "FAILED", "2026-07-16T00:00:06+00:00", snapshots=False
        )
        partial = load_replay(replay(candidate_run, [legacy.name]))
        assert partial["aggregate"]["classification"] == "INDETERMINATE"
        assert partial["source_run_ids"] == []
        assert any(error["code"] == "NO_ELIGIBLE_HISTORY" for error in partial["errors"])

        aliased = write_history(
            runs, "cp-20260716-000007-gggg", "COMMITTED", "2026-07-16T00:00:07+00:00"
        )
        aliased_plan = json.loads((aliased / "plan.json").read_text(encoding="utf-8"))
        aliased_plan["artifacts"].append(
            {
                "path": "x.txt",
                "operation": "delete",
                "reason": "duplicate identity",
                "risk": "low",
                "precondition_hash": aliased_plan["artifacts"][0]["precondition_hash"],
            }
        )
        (aliased / "plan.json").write_text(json.dumps(aliased_plan), encoding="utf-8")
        assert _inspect_run(aliased, ["x.txt"]) is None

        original_evidence_builder = _evidence
        evidence_calls = 0

        def fail_evidence_once(*args: Any, **kwargs: Any) -> dict[str, Any]:
            nonlocal evidence_calls
            evidence_calls += 1
            if evidence_calls == 1:
                raise RuntimeError("forced post-reservation assembly failure")
            return original_evidence_builder(*args, **kwargs)

        with mock.patch(f"{__name__}._evidence", fail_evidence_once):
            recovered_path = replay(candidate_run, [committed.name])
        recovered = load_replay(recovered_path)
        assert recovered["aggregate"]["classification"] == "INDETERMINATE"
        assert recovered["results"][0]["classification"] == "INDETERMINATE"
        assert any(error["code"] == "ATTEMPT_FAILURE" for error in recovered["errors"])

        before_attempts = set((candidate_run / "replay").iterdir())
        original_policy = policy_path.read_bytes()
        policy_path.write_bytes(b"{}")
        try:
            replay(candidate_run)
        except ValueError:
            pass
        else:
            raise AssertionError("Tampered policy must fail before replay publication")
        finally:
            policy_path.write_bytes(original_policy)
        assert set((candidate_run / "replay").iterdir()) == before_attempts

        package_path = candidate_run / "candidate-package.json"
        original_package = package_path.read_bytes()
        tampered = json.loads(original_package)
        tampered["package_hash"] = "f" * 64
        package_path.write_text(json.dumps(tampered), encoding="utf-8")
        try:
            replay(candidate_run)
        except ValueError:
            pass
        else:
            raise AssertionError("Tampered candidate must fail before replay publication")
        finally:
            package_path.write_bytes(original_package)

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            paths = list(pool.map(lambda _: replay(candidate_run, [committed.name]), range(2)))
        assert len({path.parent.name for path in paths}) == 2
        assert all(load_replay(path)["aggregate"]["classification"] == "TIED" for path in paths)
        assert not list(candidate_run.rglob("*.tmp"))

        item = _inspect_run(committed, ["x.txt"])
        assert item is not None
        snapshot_path = _source_files(item)[-1]
        original_read_bytes = Path.read_bytes
        snapshot_reads = 0

        def count_snapshot_reads(path: Path) -> bytes:
            nonlocal snapshot_reads
            if path == snapshot_path:
                snapshot_reads += 1
                if snapshot_reads > 1:
                    raise AssertionError("Snapshot must be read only once during reconstruction")
            return original_read_bytes(path)

        with tempfile.TemporaryDirectory() as destination, mock.patch.object(
            Path, "read_bytes", count_snapshot_reads
        ):
            _reconstruct(item, Path(destination))
        assert snapshot_reads == 1

        link_target = "target.txt"
        link_digest = hashlib.sha256(link_target.encode("utf-8")).hexdigest()
        symlink_item = {
            "run_dir": committed,
            "baseline": {
                "artifacts": [{
                    "path": ".claude/target.txt",
                    "sha256": hashlib.sha256(b"target").hexdigest(),
                    "snapshot_sha256": hashlib.sha256(b"target").hexdigest(),
                    "snapshot_path": f"baseline-artifacts/{hashlib.sha256(b'target').hexdigest()}",
                    "size_bytes": len(b"target"),
                    "kind": "file",
                }, {
                    "path": ".claude/target-link.txt",
                    "sha256": link_digest,
                    "size_bytes": len(link_target.encode("utf-8")),
                    "kind": "symlink",
                    "link_target": link_target,
                }]
            },
        }
        symlink_snapshot = committed / symlink_item["baseline"]["artifacts"][0]["snapshot_path"]
        symlink_snapshot.write_bytes(b"target")
        with tempfile.TemporaryDirectory() as destination:
            workspace = Path(destination)
            recreated = workspace / ".claude" / "target-link.txt"
            try:
                _reconstruct(symlink_item, workspace)
            except OSError as exc:
                if not (os.name == "nt" and getattr(exc, "winerror", None) == 1314):
                    raise
                assert _symlink_resolution(workspace, recreated, link_target) == (
                    recreated.parent / link_target
                ).resolve(strict=False)
            else:
                assert recreated.is_symlink()
                assert recreated.readlink().as_posix() == link_target
                assert recreated.resolve(strict=False).relative_to(workspace.resolve())
        escaping_item = copy.deepcopy(symlink_item)
        escaping_item["baseline"]["artifacts"][1]["link_target"] = "../../outside"
        escaping_item["baseline"]["artifacts"][1]["sha256"] = hashlib.sha256(b"../../outside").hexdigest()
        escaping_item["baseline"]["artifacts"][1]["size_bytes"] = len(b"../../outside")
        try:
            _reconstruct(escaping_item, Path(tempfile.mkdtemp()))
        except ValueError as exc:
            assert "escapes" in str(exc)
        else:
            raise AssertionError("Escaping symlink baseline must fail closed")

        _, _, immutable_patch = _candidate(candidate_run)
        live_patch = candidate_run / package["artifacts"][1]["path"]
        original_live_patch = live_patch.read_bytes()
        live_patch.write_bytes(b"invalid live mutation")
        try:
            private_copy_result = _compare(
                item, immutable_patch, _validation_errors, 1, ["x.txt"]
            )
            assert private_copy_result["classification"] == "TIED"
        finally:
            live_patch.write_bytes(original_live_patch)

        symlink_patch = (
            b"diff --git a/x.txt b/x.txt\n"
            b"old mode 100644\nnew mode 120000\n"
            b"index 3367afd..7b66d85\n"
            b"--- a/x.txt\n+++ b/x.txt\n@@ -1 +1 @@\n-old\n+../../outside\n"
        )
        with mock.patch.object(
            subprocess, "run", return_value=type("Completed", (), {"returncode": 0})()
        ), mock.patch(
            f"{__name__}._tree_identities",
            side_effect=[{"x.txt": "file:original"}, {"x.txt": "link:../../outside"}],
        ):
            symlink_result = _compare(
                item, symlink_patch, _validation_errors, 1, ["x.txt"]
            )
        assert symlink_result["classification"] == "INDETERMINATE"
        assert "symbolic link" in symlink_result["error"]["message"]

        original_baseline = (committed / "baseline.json").read_bytes()
        mutated = False

        def mutate_source(workspace: Path) -> int:
            nonlocal mutated
            if not mutated:
                mutated = True
                (committed / "baseline.json").write_bytes(original_baseline + b" ")
            return _validation_errors(workspace)

        try:
            mutation = _compare(item, immutable_patch, mutate_source, 1, ["x.txt"])
            assert mutation["classification"] == "INDETERMINATE"
        finally:
            (committed / "baseline.json").write_bytes(original_baseline)


def _self_check() -> None:
    assert _paths_overlap("a/b", "a") and _paths_overlap("A/b.", "a/b")
    assert not _paths_overlap("a/b", "a-b")
    assert _classify_effect(-1, 1) == "REGRESSED"
    assert _classify_effect(1, 2) == "TIED"
    assert _classify_effect(2, 2) == "IMPROVED"
    assert _aggregate([], 1) == "INDETERMINATE"
    assert _aggregate([{"classification": "IMPROVED"}, {"classification": "REGRESSED"}], 1) == "REGRESSED"
    assert _aggregate([{"classification": "IMPROVED"}], 2) == "INDETERMINATE"
    assert _aggregate([{"classification": "IMPROVED"}], 1) == "IMPROVED"
    assert _aggregate([{"classification": "TIED"}], 1) == "TIED"
    assert set(EVALUATORS) == {"control-plane-validation-errors"}
    try:
        _safe_parts("../escape")
    except ValueError:
        pass
    else:
        raise AssertionError("Traversal must fail closed")

    fixture = {
        "schema_version": 1,
        "replay_version": "1",
        "harness_version": HARNESS_VERSION,
        "replay_id": "replay-20260716T000000Z-abcdef",
        "candidate_id": "candidate",
        "candidate_run_id": "candidate-run",
        "hypothesis_id": "hypothesis",
        "candidate_package_hash": "0" * 64,
        "candidate_patch_hash": "1" * 64,
        "hypothesis_policy_hash": "2" * 64,
        "source_run_ids": [],
        "success_criterion": "fewer validation errors",
        "evaluator": "control-plane-validation-errors",
        "minimum_effect": 1,
        "minimum_evidence_count": 1,
        "started_at": "2026-07-16T00:00:00+00:00",
        "finished_at": "2026-07-16T00:00:01+00:00",
        "results": [],
        "aggregate": {"classification": "INDETERMINATE", "counts": _counts([])},
        "errors": [_error("NO_ELIGIBLE_HISTORY", "corpus", "none")],
    }
    validate_replay_result(fixture)
    forged = dict(fixture)
    forged["source_run_ids"] = ["run-forged"]
    forged["results"] = [{
        "source_run_id": "run-forged",
        "terminal_status": "COMMITTED",
        "terminal_timestamp": "2026-07-16T00:00:00+00:00",
        "baseline_hash": "3" * 64,
        "input_hash": "4" * 64,
        "baseline_metric": 0,
        "candidate_metric": 1,
        "effect": -1,
        "classification": "IMPROVED",
        "error": None,
    }]
    forged["aggregate"] = {
        "classification": "IMPROVED",
        "counts": _counts(forged["results"]),
    }
    try:
        validate_replay_result(forged)
    except ValueError as exc:
        assert "classification" in str(exc)
    else:
        raise AssertionError("Forged improvement evidence must fail closed")
    with tempfile.TemporaryDirectory() as temporary:
        attempt = Path(temporary) / fixture["replay_id"]
        attempt.mkdir()
        try:
            load_replay(attempt / "result.json")
        except ValueError as exc:
            assert "final marker" in str(exc)
        else:
            raise AssertionError("Interrupted attempt must not be readable")
        write_json_exclusive(attempt / "result.json", fixture)
        assert load_replay(attempt / "result.json")["aggregate"]["classification"] == "INDETERMINATE"
        assert not list(attempt.glob("*.tmp"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        ids = list(pool.map(lambda _: f"replay-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{secrets.token_hex(4)}", range(2)))
    assert len(set(ids)) == 2
    _fixture_replay_check()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay a candidate against terminal history.")
    parser.add_argument("candidate_run", nargs="?", type=Path)
    parser.add_argument("--corpus", action="append", default=[], help="Narrow replay to a source run ID; repeatable.")
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args(argv)
    if args.self_check:
        _self_check()
        print("replay self-check: ok")
        return 0
    if args.candidate_run is None:
        parser.error("candidate_run is required unless --self-check is used")
    print(replay(args.candidate_run, args.corpus))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
