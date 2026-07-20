from __future__ import annotations

import argparse
import concurrent.futures
import fnmatch
import hashlib
import json
import re
import tempfile
from pathlib import Path, PurePosixPath
from threading import Barrier
from typing import Any

import new_run
from common import sha256_file
from hypothesis_registry import normalize_record
from new_run import write_bytes_exclusive, write_json_exclusive
from validate import _load_manifest_yaml


ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
BOUNDARY_PATH_PATTERN = re.compile(
    r"^(?:[a-z0-9_.-]*[a-z0-9_-])"
    r"(?:/(?:[a-z0-9_.-]*[a-z0-9_-]))*$"
)
RESERVED_ARTIFACT_IDENTITIES = {"plan.json", "proposed.patch", "candidate-package.json"}
SNAPSHOT_DIR = "candidate-artifacts"
ARTIFACT_NAMES = ("plan.json", "proposed.patch", "diff-boundary.json", "hypothesis-policy.json")
ARTIFACT_PATH_PATTERN = re.compile(
    rf"^{SNAPSHOT_DIR}/([a-f0-9]{{64}})-({'|'.join(re.escape(name) for name in ARTIFACT_NAMES)})$"
)


def _is_safe_relative(value: str) -> bool:
    parts = value.split("/")
    return (
        bool(value)
        and "\\" not in value
        and not re.match(r"^[A-Za-z]:", value)
        and all(part not in {"", ".", ".."} for part in parts)
    )


def artifact_identity(value: str) -> str:
    return "/".join(
        part.rstrip(" .").casefold()
        for part in value.replace("\\", "/").split("/")
        if part not in {"", "."}
    )


def candidate_artifact_by_name(package: dict[str, Any], expected_name: str) -> dict[str, Any]:
    artifacts = package.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("Candidate package artifacts must be a list")
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        path = artifact.get("path")
        match = ARTIFACT_PATH_PATTERN.fullmatch(path) if isinstance(path, str) else None
        if match and match.group(2) == expected_name:
            return artifact
    raise ValueError(f"Candidate package is missing artifact {expected_name}")


def _is_canonical_boundary_path(value: str) -> bool:
    return bool(BOUNDARY_PATH_PATTERN.fullmatch(value))


def _inside(root: Path, path: Path) -> Path:
    root = root.resolve()
    path = path.resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Path must stay inside run directory: {path}") from exc
    return path


def _manifest_root(manifest_path: Path) -> str:
    return manifest_path.relative_to(manifest_path.parents[2]).parent.as_posix()


def _match_owner_pattern(path: str, pattern: str) -> bool:
    path = path.strip("/")
    pattern = pattern.strip("/")
    return bool(path and pattern and fnmatch.fnmatchcase(path, pattern))


def _matches_any_root(path: str, roots: list[str]) -> bool:
    parts = PurePosixPath(path).parts
    for root in roots:
        root_parts = PurePosixPath(root.rstrip("/")).parts
        if root_parts and parts[: len(root_parts)] == root_parts:
            return True
    return False


def _load_plan(package: dict[str, Any], run_dir: Path) -> dict[str, Any]:
    plan_path = _inside(run_dir, run_dir / package["artifacts"][0]["path"])
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Candidate plan must be valid UTF-8 JSON") from exc
    if not isinstance(plan, dict):
        raise ValueError("Candidate plan must be a JSON object")
    return plan


def _approval_evidence(run_dir: Path, plan: dict[str, Any]) -> None:
    approval = plan.get("human_approval")
    if approval is None:
        raise ValueError("Manifest or forbidden-root changes require human approval evidence")
    if not isinstance(approval, dict):
        raise ValueError("human_approval must be an object when approval is required")
    if approval.get("required") is not True:
        raise ValueError("human_approval.required must be true when approval is required")
    reason = approval.get("reason")
    evidence_path = approval.get("evidence_path")
    evidence_sha256 = approval.get("evidence_sha256")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("human_approval.reason must be a non-empty string")
    if not isinstance(evidence_path, str) or not _is_safe_relative(evidence_path):
        raise ValueError("human_approval.evidence_path must be a safe repository-relative path")
    if not isinstance(evidence_sha256, str) or not re.fullmatch(r"[a-f0-9]{64}", evidence_sha256):
        raise ValueError("human_approval.evidence_sha256 must be a SHA-256 hex digest")
    path = _inside(run_dir, run_dir / evidence_path)
    if not path.is_file():
        raise ValueError("human_approval.evidence_path must reference an existing run-local file")
    if sha256_file(path) != evidence_sha256:
        raise ValueError("human_approval evidence hash mismatch")


def validate_candidate_authorization(
    run_dir: Path,
    package: dict[str, Any],
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    plan = _load_plan(package, run_dir)
    owner = plan.get("owner")
    artifacts = plan.get("artifacts")
    manifest_hash = plan.get("manifest_hash")
    if not isinstance(owner, str) or not owner:
        raise ValueError("Candidate plan owner must be a non-empty string")
    if not isinstance(manifest_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", manifest_hash):
        raise ValueError("Candidate plan manifest_hash must be a SHA-256 hex digest")
    if not isinstance(artifacts, list) or not artifacts:
        raise ValueError("Candidate plan artifacts must be a non-empty list")

    manifest_path = (manifest_path or run_dir.parents[1] / "manifest.yaml").resolve()
    if not manifest_path.is_file():
        raise ValueError("Manifest-backed authorization requires .claude/control-plane/manifest.yaml")
    if sha256_file(manifest_path) != manifest_hash:
        raise ValueError("Candidate plan manifest_hash does not match current manifest.yaml")
    manifest = _load_manifest_yaml(manifest_path)
    owners = manifest.get("owners")
    if not isinstance(owners, dict) or owner not in owners or not isinstance(owners[owner], list):
        raise ValueError(f"Manifest does not authorize owner {owner!r}")
    owner_patterns = [pattern for pattern in owners[owner] if isinstance(pattern, str) and pattern]
    if not owner_patterns:
        raise ValueError(f"Manifest owner {owner!r} has no writable patterns")

    forbidden_roots = manifest.get("forbidden_roots")
    if not isinstance(forbidden_roots, list) or any(
        not isinstance(root, str) or not root for root in forbidden_roots
    ):
        raise ValueError("Manifest forbidden_roots must be a non-empty string list")
    manifest_relative = f"{_manifest_root(manifest_path)}/{manifest_path.name}"
    approval_required = False

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise ValueError("Candidate plan artifacts must contain only objects")
        path = artifact.get("path")
        if not isinstance(path, str) or not _is_canonical_boundary_path(path):
            raise ValueError("Candidate plan artifact path must be a canonical portable path")
        restricted_path = _matches_any_root(path, forbidden_roots) or path == manifest_relative
        if not restricted_path and not any(_match_owner_pattern(path, pattern) for pattern in owner_patterns):
            raise ValueError(f"Manifest owner {owner!r} cannot modify {path}")
        if restricted_path:
            approval_required = True
        rename_from = artifact.get("rename_from")
        if rename_from is not None:
            if not isinstance(rename_from, str) or not _is_canonical_boundary_path(rename_from):
                raise ValueError("Candidate plan rename_from must be a canonical portable path")
            restricted_rename = (
                _matches_any_root(rename_from, forbidden_roots) or rename_from == manifest_relative
            )
            if not restricted_rename and not any(
                _match_owner_pattern(rename_from, pattern) for pattern in owner_patterns
            ):
                raise ValueError(f"Manifest owner {owner!r} cannot rename from {rename_from}")
            if restricted_rename:
                approval_required = True

    boundary_paths = package["diff_boundary"]["allowed_paths"]
    for path in boundary_paths:
        if not any(path == artifact.get("path") for artifact in artifacts if isinstance(artifact, dict)):
            raise ValueError(f"Candidate diff boundary path is not declared in the change plan: {path}")
        if _matches_any_root(path, forbidden_roots) or path == manifest_relative:
            approval_required = True

    if approval_required:
        _approval_evidence(run_dir, plan)
    return plan


def _load_boundary(run_dir: Path, boundary_file: Path) -> tuple[dict[str, Any], str, bytes]:
    boundary_file = _inside(run_dir, boundary_file)
    boundary_path = boundary_file.relative_to(run_dir.resolve()).as_posix()
    if not _is_safe_relative(boundary_path):
        raise ValueError(f"Unsafe diff-boundary manifest path: {boundary_path!r}")
    boundary_bytes = boundary_file.read_bytes()
    boundary = json.loads(boundary_bytes.decode("utf-8"))
    if not isinstance(boundary, dict) or set(boundary) != {"allowed_paths"}:
        raise ValueError("Diff boundary must contain only allowed_paths")
    paths = boundary["allowed_paths"]
    if not isinstance(paths, list) or not paths or any(not isinstance(path, str) for path in paths):
        raise ValueError("allowed_paths must be a non-empty string list")
    for path in paths:
        if not _is_canonical_boundary_path(path):
            raise ValueError(f"Noncanonical diff-boundary path: {path!r}")
    if len(paths) != len({artifact_identity(path) for path in paths}):
        raise ValueError("allowed_paths must be unique by portable path identity")
    if artifact_identity(boundary_path) in RESERVED_ARTIFACT_IDENTITIES:
        raise ValueError(f"Reserved diff-boundary manifest path: {boundary_path}")
    return boundary, boundary_path, boundary_bytes


def _package_hash(package: dict[str, Any]) -> str:
    payload = dict(package)
    payload.pop("package_hash", None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _snapshot(run_dir: Path, name: str, data: bytes, digest: str) -> str:
    directory = _inside(run_dir, run_dir / SNAPSHOT_DIR)
    directory.mkdir(exist_ok=True)
    path = _inside(run_dir, directory / f"{digest}-{name}")
    write_bytes_exclusive(path, data)
    return path.relative_to(run_dir).as_posix()


def validate_candidate_package(run_dir: Path, package: dict[str, Any]) -> dict[str, Any]:
    """Validate replay-sensitive invariants that JSON Schema cannot express."""
    run_dir = run_dir.resolve()
    paths = package.get("diff_boundary", {}).get("allowed_paths")
    if (
        not isinstance(paths, list)
        or not paths
        or any(not isinstance(path, str) or not _is_canonical_boundary_path(path) for path in paths)
        or len(paths) != len(set(paths))
    ):
        raise ValueError("allowed_paths must use unique canonical portable paths")

    artifacts = package.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != len(ARTIFACT_NAMES):
        raise ValueError(
            "Candidate package must contain four fixed artifacts "
            f"({len(ARTIFACT_NAMES)} expected from ARTIFACT_NAMES: "
            f"{', '.join(ARTIFACT_NAMES)})"
        )
    for artifact, expected_name in zip(artifacts, ARTIFACT_NAMES):
        if not isinstance(artifact, dict):
            raise ValueError("Candidate artifact must be an object")
        path = artifact.get("path")
        digest = artifact.get("sha256")
        match = ARTIFACT_PATH_PATTERN.fullmatch(path) if isinstance(path, str) else None
        if not match or match.group(2) != expected_name:
            raise ValueError(f"Invalid candidate artifact path: {path!r}")
        if digest != match.group(1):
            raise ValueError(f"Candidate artifact path digest does not match sha256: {path}")
        artifact_path = _inside(run_dir, run_dir / path)
        if not artifact_path.is_file() or sha256_file(artifact_path) != digest:
            raise ValueError(f"Candidate artifact bytes do not match sha256: {path}")
    patch_artifact = candidate_artifact_by_name(package, "proposed.patch")
    if package.get("patch_hash") != patch_artifact["sha256"]:
        raise ValueError("patch_hash does not match proposed.patch")
    policy_artifact = candidate_artifact_by_name(package, "hypothesis-policy.json")
    if package.get("hypothesis_policy_hash") != policy_artifact["sha256"]:
        raise ValueError("hypothesis_policy_hash does not match hypothesis-policy.json")
    policy_bytes = (run_dir / policy_artifact["path"]).read_bytes()
    try:
        policy = json.loads(policy_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("hypothesis policy must be valid UTF-8 JSON") from exc
    required_policy_fields = {
        "hypothesis_id",
        "success_criteria",
        "evaluator",
        "minimum_effect",
        "minimum_evidence_count",
    }
    if not isinstance(policy, dict) or set(policy) != required_policy_fields:
        raise ValueError("hypothesis policy contains unexpected fields")
    canonical_policy = json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if canonical_policy != policy_bytes:
        raise ValueError("hypothesis policy bytes are not canonical")
    if policy["hypothesis_id"] != package.get("hypothesis_id"):
        raise ValueError("hypothesis policy ID does not match candidate package")
    if (
        not isinstance(policy.get("success_criteria"), str)
        or not policy["success_criteria"]
        or
        policy.get("evaluator") != "control-plane-validation-errors"
        or any(
            not isinstance(policy.get(key), int)
            or isinstance(policy.get(key), bool)
            or policy[key] < 1
            for key in ("minimum_effect", "minimum_evidence_count")
        )
    ):
        raise ValueError("hypothesis policy evaluator or thresholds are invalid")
    if package.get("package_hash") != _package_hash(package):
        raise ValueError("package_hash does not match candidate package")
    return package


def emit_candidate(
    run_dir: Path,
    hypothesis_id: str,
    candidate_id: str,
    boundary_file: Path,
    hypothesis_record: Any,
    manifest_path: Path | None = None,
) -> Path:
    run_dir = run_dir.resolve()
    if not run_dir.is_dir():
        raise ValueError(f"Run directory does not exist: {run_dir}")
    for label, value in (("hypothesis", hypothesis_id), ("candidate", candidate_id)):
        if not ID_PATTERN.fullmatch(value):
            raise ValueError(f"Invalid {label} id: {value!r}")
    normalized_hypothesis = normalize_record(hypothesis_record)
    if normalized_hypothesis["hypothesis_id"] != hypothesis_id:
        raise ValueError("Hypothesis record ID does not match requested hypothesis ID")
    evaluation = normalized_hypothesis["evaluation"]
    policy = {
        "hypothesis_id": hypothesis_id,
        "success_criteria": normalized_hypothesis["success_criteria"],
        "evaluator": evaluation["evaluator"],
        "minimum_effect": evaluation["minimum_effect"],
        "minimum_evidence_count": evaluation["minimum_evidence_count"],
    }
    policy_bytes = json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8")

    patch = _inside(run_dir, run_dir / "proposed.patch")
    plan = _inside(run_dir, run_dir / "plan.json")
    if not patch.is_file():
        raise ValueError("proposed.patch must exist and be non-empty before finalization")
    if not plan.is_file():
        raise ValueError("plan.json must exist before finalization")
    plan_bytes = plan.read_bytes()
    patch_bytes = patch.read_bytes()
    if not patch_bytes:
        raise ValueError("proposed.patch must exist and be non-empty before finalization")
    boundary, boundary_path, boundary_bytes = _load_boundary(run_dir, boundary_file)
    plan_digest = hashlib.sha256(plan_bytes).hexdigest()
    patch_digest = hashlib.sha256(patch_bytes).hexdigest()
    boundary_digest = hashlib.sha256(boundary_bytes).hexdigest()
    policy_digest = hashlib.sha256(policy_bytes).hexdigest()

    artifacts = [
        {
            "path": _snapshot(run_dir, "plan.json", plan_bytes, plan_digest),
            "sha256": plan_digest,
        },
        {
            "path": _snapshot(run_dir, "proposed.patch", patch_bytes, patch_digest),
            "sha256": patch_digest,
        },
        {
            "path": _snapshot(
                run_dir, "diff-boundary.json", boundary_bytes, boundary_digest
            ),
            "sha256": boundary_digest,
        },
        {
            "path": _snapshot(
                run_dir, "hypothesis-policy.json", policy_bytes, policy_digest
            ),
            "sha256": policy_digest,
        },
    ]
    if len(artifacts) != len({artifact_identity(artifact["path"]) for artifact in artifacts}):
        raise ValueError("Candidate artifact paths must be unique")

    package: dict[str, Any] = {
        "schema_version": 1,
        "candidate_id": candidate_id,
        "run_id": run_dir.name,
        "hypothesis_id": hypothesis_id,
        "patch_hash": patch_digest,
        "hypothesis_policy_hash": policy_digest,
        "package_hash": "",
        "diff_boundary": boundary,
        "artifacts": artifacts,
    }
    package["package_hash"] = _package_hash(package)
    validate_candidate_package(run_dir, package)
    validate_candidate_authorization(run_dir, package, manifest_path)
    output = _inside(run_dir, run_dir / "candidate-package.json")
    try:
        write_json_exclusive(output, package)
    except FileExistsError as exc:
        raise ValueError("candidate-package.json is already finalized") from exc
    return output


def _self_check() -> None:
    global write_json_exclusive
    from jsonschema import Draft202012Validator

    with tempfile.TemporaryDirectory() as temp_dir:
        repo_root = Path(temp_dir) / "repo"
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
    - .claude/control-plane/scripts/**
    - .claude/control-plane/schemas/**
    - .claude/control-plane/evals/workflow-*.yaml
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
        policy_run = repo_root / ".claude" / "control-plane" / "runs" / "policy"
        policy_run.mkdir(parents=True)
        policy_boundary = policy_run / "diff-boundary.json"
        policy_boundary.write_text(
            '{"allowed_paths":[".claude/control-plane/scripts/x.py"]}\n', encoding="utf-8"
        )
        approval_path = policy_run / "approval.txt"
        approval_path.write_text("approved\n", encoding="utf-8")
        (policy_run / "proposed.patch").write_text("x\n", encoding="utf-8")
        policy = {
            "hypothesis_id": "h-policy",
            "friction_key": "validation",
            "target_artifacts": ["x"],
            "success_criteria": "fewer validation errors",
            "evidence_refs": [".claude/control-plane/runs/run-1/result.json"],
            "recurrence_count": 1,
            "impact_score": 1,
            "priority_score": 1001,
            "evaluation": {
                "evaluator": "control-plane-validation-errors",
                "minimum_effect": 1,
                "minimum_evidence_count": 1,
            },
        }
        policy_plan = {
            "schema_version": 1,
            "run_id": "policy",
            "owner": "workflow-specialist",
            "request": "self-check",
            "repository_root": str(repo_root),
            "manifest_hash": sha256_file(manifest),
            "artifacts": [{
                "path": ".claude/control-plane/scripts/x.py",
                "operation": "update",
                "reason": "self-check",
                "risk": "low",
                "precondition_hash": None,
            }],
            "read_artifacts": [".claude/control-plane/scripts/x.py"],
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
        (policy_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
        policy_output = emit_candidate(
            policy_run,
            "h-policy",
            "c-policy",
            policy_boundary,
            hypothesis_record=policy,
            manifest_path=manifest,
        )
        policy_package = json.loads(policy_output.read_text(encoding="utf-8"))
        assert policy_package["hypothesis_policy_hash"] == policy_package["artifacts"][3]["sha256"]
        missing_artifact = json.loads(json.dumps(policy_package))
        missing_artifact["artifacts"] = missing_artifact["artifacts"][:-1]
        try:
            validate_candidate_package(policy_run, missing_artifact)
        except ValueError as exc:
            assert "four fixed artifacts" in str(exc)
            expected_count = str(len(ARTIFACT_NAMES))
            assert expected_count in str(exc)
            for expected_name in ARTIFACT_NAMES:
                assert expected_name in str(exc)
        else:
            raise AssertionError("Invalid artifact counts must report expected artifacts")
        policy_artifact = policy_run / policy_package["artifacts"][3]["path"]
        assert json.loads(policy_artifact.read_text(encoding="utf-8")) == {
            "hypothesis_id": "h-policy",
            "success_criteria": "fewer validation errors",
            "evaluator": "control-plane-validation-errors",
            "minimum_effect": 1,
            "minimum_evidence_count": 1,
        }

        mismatch_run = repo_root / ".claude" / "control-plane" / "runs" / "policy-mismatch"
        mismatch_run.mkdir()
        mismatch_boundary = mismatch_run / "diff-boundary.json"
        mismatch_boundary.write_text(
            '{"allowed_paths":[".claude/control-plane/scripts/x.py"]}\n', encoding="utf-8"
        )
        (mismatch_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
        (mismatch_run / "proposed.patch").write_text("x\n", encoding="utf-8")
        try:
            emit_candidate(
                mismatch_run, "different", "c-policy", mismatch_boundary, policy, manifest
            )
        except ValueError as exc:
            assert "record ID" in str(exc)
        else:
            raise AssertionError("Mismatched hypothesis IDs must fail closed")
        assert not (mismatch_run / "candidate-package.json").exists()

        tampered_policy_hash = json.loads(json.dumps(policy_package))
        tampered_policy_hash["hypothesis_policy_hash"] = "0" * 64
        try:
            validate_candidate_package(policy_run, tampered_policy_hash)
        except ValueError as exc:
            assert "hypothesis_policy_hash" in str(exc)
        else:
            raise AssertionError("Tampered policy hash must fail closed")
        malformed_criterion = json.loads(json.dumps(policy_package))
        malformed_policy = json.loads(policy_artifact.read_text(encoding="utf-8"))
        malformed_policy["success_criteria"] = {"not": "measurable"}
        malformed_bytes = json.dumps(
            malformed_policy, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        malformed_digest = hashlib.sha256(malformed_bytes).hexdigest()
        malformed_path = policy_run / SNAPSHOT_DIR / f"{malformed_digest}-hypothesis-policy.json"
        malformed_path.write_bytes(malformed_bytes)
        malformed_criterion["artifacts"][3] = {
            "path": malformed_path.relative_to(policy_run).as_posix(),
            "sha256": malformed_digest,
        }
        malformed_criterion["hypothesis_policy_hash"] = malformed_digest
        malformed_criterion["package_hash"] = _package_hash(malformed_criterion)
        try:
            validate_candidate_package(policy_run, malformed_criterion)
        except ValueError as exc:
            assert "criterion" in str(exc) or "evaluator" in str(exc)
        else:
            raise AssertionError("Object success criterion must fail closed")
        tampered_policy_path = json.loads(json.dumps(policy_package))
        tampered_policy_path["artifacts"][3]["path"] = (
            f"{SNAPSHOT_DIR}/{'0' * 64}-hypothesis-policy.json"
        )
        try:
            validate_candidate_package(policy_run, tampered_policy_path)
        except ValueError as exc:
            assert "path digest" in str(exc)
        else:
            raise AssertionError("Tampered policy path must fail closed")
        original_policy_bytes = policy_artifact.read_bytes()
        policy_artifact.write_bytes(b"{}")
        try:
            validate_candidate_package(policy_run, policy_package)
        except ValueError as exc:
            assert "bytes" in str(exc)
        else:
            raise AssertionError("Tampered policy bytes must fail closed")
        finally:
            policy_artifact.write_bytes(original_policy_bytes)

        durability_run = Path(temp_dir) / "durability"
        durability_run.mkdir()
        original_sync = new_run._sync_published_entry
        synced: list[Path] = []
        new_run._sync_published_entry = synced.append
        try:
            new_run.write_json_exclusive(durability_run / "evidence.json", {"ok": True})
            new_run.write_bytes_exclusive(durability_run / "evidence.bin", b"ok")
        finally:
            new_run._sync_published_entry = original_sync
        assert synced == [durability_run / "evidence.json", durability_run / "evidence.bin"]

        failed_run = Path(temp_dir) / "durability-failure"
        failed_run.mkdir()

        def fail_sync(_path: Path) -> None:
            raise OSError("forced durability failure")

        new_run._sync_published_entry = fail_sync
        try:
            try:
                new_run.write_json_exclusive(failed_run / "evidence.json", {"ok": True})
            except OSError as exc:
                assert "forced durability failure" in str(exc)
            else:
                raise AssertionError("Durability failure must fail closed")
        finally:
            new_run._sync_published_entry = original_sync
        assert not list(failed_run.glob(".evidence.json.*.tmp"))

        for name, boundary_name, boundary_content in (
            ("posix-root", "diff-boundary.json", '{"allowed_paths":["/root"]}\n'),
            ("windows-root", "diff-boundary.json", '{"allowed_paths":["\\\\root"]}\n'),
            ("windows-drive", "diff-boundary.json", '{"allowed_paths":["C:\\\\root"]}\n'),
            ("parent", "diff-boundary.json", '{"allowed_paths":["x/../y"]}\n'),
            ("reserved", "plan.json", '{"allowed_paths":["x"]}\n'),
        ):
            negative_run = repo_root / ".claude" / "control-plane" / "runs" / name
            negative_run.mkdir()
            negative_boundary = negative_run / boundary_name
            negative_boundary.write_text(boundary_content, encoding="utf-8")
            if boundary_name != "plan.json":
                (negative_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
            (negative_run / "proposed.patch").write_text(
                "diff --git a/x b/x\n", encoding="utf-8"
            )
            try:
                emit_candidate(negative_run, "h-policy", "c-1", negative_boundary, policy, manifest)
            except ValueError:
                pass
            else:
                raise AssertionError(f"{name} boundary must fail closed")
            assert not (negative_run / "candidate-package.json").exists()

        for boundary_name in ("C:\\root.json", "\\root.json", "a\\..\\b"):
            assert not _is_safe_relative(boundary_name)
            if Path(boundary_name).name != boundary_name:
                continue
            negative_run = repo_root / ".claude" / "control-plane" / "runs" / f"manifest-{len(boundary_name)}"
            negative_run.mkdir()
            negative_boundary = negative_run / boundary_name
            negative_boundary.write_text('{"allowed_paths":["x"]}\n', encoding="utf-8")
            (negative_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
            (negative_run / "proposed.patch").write_text(
                "diff --git a/x b/x\n", encoding="utf-8"
            )
            try:
                emit_candidate(negative_run, "h-policy", "c-1", negative_boundary, policy, manifest)
            except ValueError:
                pass
            else:
                raise AssertionError(f"{boundary_name!r} manifest path must fail closed")

        for alias in ("./x", ".\\x", "a\\b", "a//b", "a/./b", "a/"):
            assert not _is_safe_relative(alias)

        duplicate_run = repo_root / ".claude" / "control-plane" / "runs" / "duplicate-boundary"
        duplicate_run.mkdir()
        duplicate_boundary = duplicate_run / "diff-boundary.json"
        (duplicate_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
        (duplicate_run / "proposed.patch").write_text("x\n", encoding="utf-8")
        for aliases in (
            ["Dir/file", "dir/FILE"],
            ["dir/file", "dir/file."],
            ["dir/file", "dir/file "],
        ):
            duplicate_boundary.write_text(
                json.dumps({"allowed_paths": aliases}) + "\n", encoding="utf-8"
            )
            try:
                emit_candidate(duplicate_run, "h-policy", "c-1", duplicate_boundary, policy, manifest)
            except ValueError as exc:
                assert "Noncanonical" in str(exc)
            else:
                raise AssertionError("Portable allowed_paths aliases must fail closed")

        mutation_run = repo_root / ".claude" / "control-plane" / "runs" / "mutation"
        mutation_run.mkdir()
        mutation_boundary = mutation_run / "diff-boundary.json"
        mutation_boundary.write_text(
            '{"allowed_paths":[".claude/control-plane/scripts/x.py"]}\n', encoding="utf-8"
        )
        (mutation_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
        mutation_patch = mutation_run / "proposed.patch"
        mutation_patch.write_text("diff --git a/x b/x\n", encoding="utf-8")
        original_sha256 = hashlib.sha256
        hash_calls = 0

        def mutating_sha256(data: bytes = b""):
            nonlocal hash_calls
            digest = original_sha256(data)
            hash_calls += 1
            if hash_calls == 2:
                mutation_patch.write_text("diff --git a/y b/y\n", encoding="utf-8")
            return digest

        hashlib.sha256 = mutating_sha256
        try:
            mutation_output = emit_candidate(
                mutation_run, "h-policy", "c-1", mutation_boundary, policy, manifest
            )
        finally:
            hashlib.sha256 = original_sha256
        mutation_package = json.loads(mutation_output.read_text(encoding="utf-8"))
        assert mutation_package["patch_hash"] == mutation_package["artifacts"][1]["sha256"]
        assert mutation_package["patch_hash"] != sha256_file(mutation_patch)
        for artifact in mutation_package["artifacts"]:
            assert artifact["sha256"] == sha256_file(mutation_run / artifact["path"])

        run_dir = repo_root / ".claude" / "control-plane" / "runs" / "run-1"
        run_dir.mkdir()
        boundary = run_dir / "diff-boundary.json"
        boundary.write_text(
            '{"allowed_paths":[".claude/control-plane/scripts/foo..bar"]}\n', encoding="utf-8"
        )
        run_plan = dict(policy_plan)
        run_plan["artifacts"] = [{
            "path": ".claude/control-plane/scripts/foo..bar",
            "operation": "update",
            "reason": "self-check",
            "risk": "low",
            "precondition_hash": None,
        }]
        run_plan["read_artifacts"] = [".claude/control-plane/scripts/foo..bar"]
        (run_dir / "plan.json").write_text(json.dumps(run_plan) + "\n", encoding="utf-8")

        for patch_content in (None, ""):
            if patch_content is not None:
                (run_dir / "proposed.patch").write_text(patch_content, encoding="utf-8")
            try:
                emit_candidate(run_dir, "h-policy", "c-1", boundary, policy, manifest)
            except ValueError:
                pass
            else:
                raise AssertionError("Missing or empty proposed.patch must fail closed")

        (run_dir / "proposed.patch").write_text("diff --git a/x b/x\n", encoding="utf-8")
        output = emit_candidate(run_dir, "h-policy", "c-1", boundary, policy, manifest)
        emitted = json.loads(output.read_text(encoding="utf-8"))
        assert emitted["patch_hash"] == sha256_file(run_dir / "proposed.patch")
        for artifact in emitted["artifacts"]:
            assert artifact["sha256"] == sha256_file(run_dir / artifact["path"])
        try:
            emit_candidate(run_dir, "h-policy", "c-1", boundary, policy, manifest)
        except ValueError:
            pass
        else:
            raise AssertionError("A finalized candidate package must not be overwritten")

        concurrent_run = repo_root / ".claude" / "control-plane" / "runs" / "concurrent"
        concurrent_run.mkdir()
        concurrent_boundary = concurrent_run / "diff-boundary.json"
        concurrent_boundary.write_text(
            '{"allowed_paths":[".claude/control-plane/scripts/x.py"]}\n', encoding="utf-8"
        )
        (concurrent_run / "plan.json").write_text(json.dumps(policy_plan) + "\n", encoding="utf-8")
        (concurrent_run / "proposed.patch").write_text(
            "diff --git a/x b/x\n", encoding="utf-8"
        )

        barrier = Barrier(2)
        original_writer = write_json_exclusive

        def synchronized_writer(path: Path, data: dict) -> None:
            barrier.wait()
            original_writer(path, data)

        def finalize() -> str:
            try:
                return str(
                    emit_candidate(
                        concurrent_run, "h-policy", "c-1", concurrent_boundary, policy, manifest
                    )
                )
            except ValueError as exc:
                return str(exc)

        write_json_exclusive = synchronized_writer
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                futures = [executor.submit(finalize) for _ in range(2)]
                results = [future.result() for future in futures]
        finally:
            write_json_exclusive = original_writer

        concurrent_output = concurrent_run / "candidate-package.json"
        assert results.count(str(concurrent_output.resolve())) == 1
        assert results.count("candidate-package.json is already finalized") == 1
        assert not list(concurrent_run.glob(".candidate-package.json.*.tmp"))
        package = json.loads(concurrent_output.read_text(encoding="utf-8"))
        assert validate_candidate_package(concurrent_run, package) is package
        assert package["patch_hash"] == sha256_file(concurrent_run / "proposed.patch")
        assert package["package_hash"] == _package_hash(package)
        for artifact in package["artifacts"]:
            assert artifact["sha256"] == sha256_file(concurrent_run / artifact["path"])
        schema = json.loads(
            (
                Path(__file__).parent.parent
                / "schemas"
                / "candidate-package.schema.json"
            ).read_text(encoding="utf-8")
        )
        assert not list(Draft202012Validator(schema).iter_errors(package))
        for noncanonical in ("Dir/file", "dir/file.", "dir/file "):
            alias_package = dict(package)
            alias_package["diff_boundary"] = {"allowed_paths": [noncanonical]}
            assert list(Draft202012Validator(schema).iter_errors(alias_package))
        tampered_hash = json.loads(json.dumps(package))
        tampered_hash["artifacts"][0]["sha256"] = "0" * 64
        try:
            validate_candidate_package(concurrent_run, tampered_hash)
        except ValueError as exc:
            assert "path digest" in str(exc)
        else:
            raise AssertionError("Tampered artifact sha256 must fail closed")
        tampered_path = json.loads(json.dumps(package))
        tampered_path["artifacts"][0]["path"] = (
            f"{SNAPSHOT_DIR}/{'0' * 64}-plan.json"
        )
        try:
            validate_candidate_package(concurrent_run, tampered_path)
        except ValueError as exc:
            assert "path digest" in str(exc)
        else:
            raise AssertionError("Tampered artifact filename digest must fail closed")
        for alias in (
            "PLAN.JSON",
            "plan.json.",
            "Proposed.Patch ",
            "CANDIDATE-PACKAGE.JSON..",
            "./plan.json",
            ".\\plan.json",
        ):
            assert artifact_identity(alias) in RESERVED_ARTIFACT_IDENTITIES
            alias_package = dict(package)
            alias_package["artifacts"] = [dict(artifact) for artifact in package["artifacts"]]
            alias_package["artifacts"][2]["path"] = alias
            assert list(Draft202012Validator(schema).iter_errors(alias_package))

        forbidden_run = repo_root / ".claude" / "control-plane" / "runs" / "forbidden-approval"
        forbidden_run.mkdir()
        forbidden_boundary = forbidden_run / "diff-boundary.json"
        forbidden_boundary.write_text('{"allowed_paths":["src/blocked.py"]}\n', encoding="utf-8")
        forbidden_plan = dict(policy_plan)
        forbidden_plan["artifacts"] = [{
            "path": "src/blocked.py",
            "operation": "update",
            "reason": "self-check",
            "risk": "high",
            "precondition_hash": None,
        }]
        forbidden_plan["read_artifacts"] = ["src/blocked.py"]
        (forbidden_run / "plan.json").write_text(json.dumps(forbidden_plan) + "\n", encoding="utf-8")
        (forbidden_run / "proposed.patch").write_text("diff --git a/x b/x\n", encoding="utf-8")
        try:
            emit_candidate(forbidden_run, "h-policy", "c-1", forbidden_boundary, policy, manifest)
        except ValueError as exc:
            assert "approval evidence" in str(exc)
        else:
            raise AssertionError("Forbidden-root candidate must require approval evidence")

        approved_manifest_run = repo_root / ".claude" / "control-plane" / "runs" / "manifest-approved"
        approved_manifest_run.mkdir()
        approved_boundary = approved_manifest_run / "diff-boundary.json"
        approved_boundary.write_text(
            '{"allowed_paths":[".claude/control-plane/manifest.yaml"]}\n', encoding="utf-8"
        )
        approved_evidence = approved_manifest_run / "approval.txt"
        approved_evidence.write_text("approved\n", encoding="utf-8")
        approved_plan = dict(policy_plan)
        approved_plan["artifacts"] = [{
            "path": ".claude/control-plane/manifest.yaml",
            "operation": "update",
            "reason": "self-check",
            "risk": "high",
            "precondition_hash": sha256_file(manifest),
        }]
        approved_plan["read_artifacts"] = [".claude/control-plane/manifest.yaml"]
        approved_plan["human_approval"] = {
            "required": True,
            "reason": "manifest change approved",
            "evidence_path": "approval.txt",
            "evidence_sha256": sha256_file(approved_evidence),
        }
        (approved_manifest_run / "plan.json").write_text(json.dumps(approved_plan) + "\n", encoding="utf-8")
        (approved_manifest_run / "proposed.patch").write_text("diff --git a/x b/x\n", encoding="utf-8")
        approved_output = emit_candidate(
            approved_manifest_run,
            "h-policy",
            "c-approval",
            approved_boundary,
            policy,
            manifest,
        )
        approved_package = json.loads(approved_output.read_text(encoding="utf-8"))
        approval_file = approved_manifest_run / "approval.txt"
        original_approval = approval_file.read_bytes()
        approval_file.write_bytes(b"tampered\n")
        try:
            validate_candidate_authorization(approved_manifest_run, approved_package, manifest)
        except ValueError as exc:
            assert "hash mismatch" in str(exc)
        else:
            raise AssertionError("Tampered approval evidence must fail closed")
        finally:
            approval_file.write_bytes(original_approval)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Finalize a run-local candidate package.")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--hypothesis-id")
    parser.add_argument("--candidate-id")
    parser.add_argument("--boundary-file", type=Path)
    parser.add_argument("--hypothesis-file", type=Path)
    args = parser.parse_args(argv)
    if args.self_check:
        _self_check()
        print("PASS: candidate_emitter self-check")
        return 0
    if None in (
        args.run_dir,
        args.hypothesis_id,
        args.candidate_id,
        args.boundary_file,
        args.hypothesis_file,
    ):
        parser.error(
            "--run-dir, --hypothesis-id, --candidate-id, --boundary-file, and --hypothesis-file are required"
        )
    hypothesis_record = json.loads(args.hypothesis_file.read_text(encoding="utf-8"))
    emit_candidate(
        args.run_dir,
        args.hypothesis_id,
        args.candidate_id,
        args.boundary_file,
        hypothesis_record,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Backward-compatible aliases for older imports.
_artifact_identity = artifact_identity
