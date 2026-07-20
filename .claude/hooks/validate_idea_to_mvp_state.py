from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


WATCH_PREFIXES = (
    ".claude/control-plane/state/idea-to-mvp/",
    ".claude/control-plane/scripts/",
    ".claude/control-plane/schemas/",
    ".claude/control-plane/evals/",
    ".claude/control-plane/manifest.yaml",
    ".claude/hooks/",
    ".claude/settings.json",
    ".claude/workflows/",
)
ARTIFACT_PREFIXES = (
    ".claude/control-plane/state/idea-to-mvp/artifacts/",
    ".claude/control-plane/state/idea-to-mvp/handoffs/",
)
PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:TODO|TBD)\b|\bdeveloper decides?\b|\[citation needed\]|\bcitation needed\b",
    re.IGNORECASE,
)
STATE_PREFIX = ".claude/control-plane/state/idea-to-mvp/"
REVIEW_READY_STATUSES = {"reviewed", "approved", "conditionally_approved", "still_valid"}


def _load_payload() -> dict:
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        raise ValueError("root must be an object")
    return payload


def _changed_paths(project_dir: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    changed = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip().replace("\\", "/")
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        changed.append(path)
    return changed


def _watched_paths_for_payload(payload: dict, project_dir: Path) -> list[str]:
    event_name = payload.get("hook_event_name")
    if event_name in {"Stop", "SubagentStop", "StopFailure", "SessionEnd"}:
        return [path for path in _changed_paths(project_dir) if any(path.startswith(prefix) for prefix in WATCH_PREFIXES)]

    tool_name = payload.get("tool_name")
    if event_name == "PostToolUse" and tool_name == "Bash":
        return [path for path in _changed_paths(project_dir) if any(path.startswith(prefix) for prefix in WATCH_PREFIXES)]

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if not isinstance(file_path, str):
        return []
    normalized = file_path.replace("\\", "/")
    project_prefix = str(project_dir).replace("\\", "/") + "/"
    if normalized.startswith(project_prefix):
        normalized = normalized[len(project_prefix) :]
    return [normalized] if any(normalized.startswith(prefix) for prefix in WATCH_PREFIXES) else []


def _placeholder_hits(project_dir: Path, watched_paths: list[str]) -> list[str]:
    hits = []
    for relative in watched_paths:
        if not any(relative.startswith(prefix) for prefix in ARTIFACT_PREFIXES):
            continue
        path = project_dir / relative
        if not path.exists() or path.suffix.lower() not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if PLACEHOLDER_PATTERN.search(text):
            hits.append(relative)
    return hits


def _workflow_syntax_errors(project_dir: Path, watched_paths: list[str]) -> list[str]:
    errors: list[str] = []
    for relative in watched_paths:
        if not relative.startswith(".claude/workflows/") or not relative.endswith(".js"):
            continue
        path = project_dir / relative
        if not path.exists():
            continue
        result = subprocess.run(
            ["node", "--check", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stdout or result.stderr).strip()
            errors.append(f"{relative}: workflow syntax check failed: {detail}")
    return errors


def _python_syntax_errors(project_dir: Path, watched_paths: list[str]) -> list[str]:
    errors: list[str] = []
    for relative in watched_paths:
        if not relative.endswith(".py"):
            continue
        if not (
            relative.startswith(".claude/control-plane/scripts/")
            or relative.startswith(".claude/hooks/")
        ):
            continue
        path = project_dir / relative
        if not path.exists():
            continue
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stdout or result.stderr).strip()
            errors.append(f"{relative}: python syntax check failed: {detail}")
    return errors


def _config_validation_errors(project_dir: Path, watched_paths: list[str]) -> list[str]:
    relevant = [
        path
        for path in watched_paths
        if path.startswith(".claude/agents/")
        or path.startswith(".claude/skills/")
        or path.startswith(".claude/rules/")
        or path.startswith(".claude/workflows/")
        or path.startswith(".claude/hooks/")
        or path == ".claude/settings.json"
        or path == ".claude/control-plane/manifest.yaml"
        or path.startswith(".claude/control-plane/state/idea-to-mvp/")
        or path.startswith(".claude/control-plane/schemas/")
        or path.startswith(".claude/control-plane/evals/")
    ]
    if not relevant:
        return []
    validator = project_dir / ".claude" / "control-plane" / "scripts" / "validate.py"
    result = subprocess.run(
        [sys.executable, str(validator), "--paths", *relevant],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    detail = (result.stdout or result.stderr).strip()
    joined_paths = ", ".join(relevant)
    return [f"{joined_paths}: config validation failed: {detail}"]


def _workflow_state(project_dir: Path) -> dict:
    path = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp" / "workflow-state.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _active_nodes(project_dir: Path) -> set[int]:
    state = _workflow_state(project_dir)
    active = set()
    nodes = state.get("nodes")
    if not isinstance(nodes, list):
        return active
    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_id = node.get("node")
        status = node.get("status")
        if isinstance(node_id, int) and status in {"eligible", "in-progress", "recoverable", "rework", "blocked"}:
            active.add(node_id)
    return active


def _missing_required_outputs(project_dir: Path) -> list[str]:
    active_nodes = _active_nodes(project_dir)
    if not active_nodes:
        return []
    handoffs_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp" / "handoffs"
    if not handoffs_dir.exists():
        return []
    missing = []
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        workflow_node = packet.get("workflow_node")
        if workflow_node not in active_nodes:
            continue
        required_output = packet.get("required_output")
        if not isinstance(required_output, dict):
            continue
        output_path = required_output.get("path")
        if not isinstance(output_path, str) or not output_path.strip():
            continue
        candidate = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp" / output_path
        if not candidate.exists():
            missing.append(output_path)
    return sorted(dict.fromkeys(missing))


def _required_outputs_not_review_ready(project_dir: Path) -> list[str]:
    active_nodes = _active_nodes(project_dir)
    if not active_nodes:
        return []
    state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
    handoffs_dir = state_dir / "handoffs"
    manifest_path = state_dir / "artifact-manifest.json"
    if not handoffs_dir.exists() or not manifest_path.exists():
        return []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = manifest.get("artifacts")
    if not isinstance(rows, list):
        return []
    status_by_path = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        path = row.get("path")
        status = row.get("status")
        if isinstance(path, str) and isinstance(status, str):
            status_by_path[path] = status
    incomplete = []
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        workflow_node = packet.get("workflow_node")
        if workflow_node not in active_nodes:
            continue
        required_output = packet.get("required_output")
        if not isinstance(required_output, dict):
            continue
        output_path = required_output.get("path")
        if not isinstance(output_path, str) or not output_path.strip():
            continue
        if status_by_path.get(output_path) not in REVIEW_READY_STATUSES:
            incomplete.append(output_path)
    return sorted(dict.fromkeys(incomplete))


def _handoffs_missing_completion_results(project_dir: Path) -> list[str]:
    active_nodes = _active_nodes(project_dir)
    if not active_nodes:
        return []
    handoffs_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp" / "handoffs"
    if not handoffs_dir.exists():
        return []
    missing = []
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        workflow_node = packet.get("workflow_node")
        if workflow_node not in active_nodes:
            continue
        completion_result = packet.get("completion_result")
        if not isinstance(completion_result, dict):
            missing.append(handoff_path.name)
    return sorted(dict.fromkeys(missing))


def _portable_handoff_changed_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith(STATE_PREFIX):
        normalized = normalized[len(STATE_PREFIX) :]
    return normalized


def _record_changed_paths(project_dir: Path, watched_paths: list[str]) -> None:
    if not watched_paths:
        return
    active_nodes = _active_nodes(project_dir)
    if not active_nodes:
        return
    handoffs_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp" / "handoffs"
    if not handoffs_dir.exists():
        return
    normalized_paths = sorted(
        dict.fromkeys(
            _portable_handoff_changed_path(path) for path in watched_paths if isinstance(path, str) and path
        )
    )
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        if packet.get("workflow_node") not in active_nodes:
            continue
        existing = packet.get("changed_paths")
        if isinstance(existing, list):
            merged = sorted(dict.fromkeys([path for path in existing if isinstance(path, str)] + normalized_paths))
        else:
            merged = normalized_paths
        packet["changed_paths"] = merged
        handoff_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")


def _artifact_ids_needing_change_impact(project_dir: Path, watched_paths: list[str]) -> list[str]:
    manifest_path = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp" / "artifact-manifest.json"
    if not manifest_path.exists():
        return []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return []
    rows = manifest.get("artifacts")
    if not isinstance(rows, list):
        return []
    artifact_ids: list[str] = []
    seen_ids: set[str] = set()
    watched = set(watched_paths)
    for row in rows:
        if not isinstance(row, dict):
            continue
        artifact_id = row.get("artifact_id")
        path = row.get("path")
        status = row.get("status")
        if (
            not isinstance(artifact_id, str)
            or not isinstance(path, str)
            or status not in REVIEW_READY_STATUSES
            or path not in watched
            or artifact_id in seen_ids
        ):
            continue
        artifact_ids.append(artifact_id)
        seen_ids.add(artifact_id)
    return artifact_ids


def _apply_change_impact(project_dir: Path, changed_artifact_ids: list[str]) -> tuple[bool, str]:
    if not changed_artifact_ids:
        return True, ""
    script = project_dir / ".claude" / "control-plane" / "scripts" / "idea_to_mvp_state.py"
    state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
    command = [
        sys.executable,
        str(script),
        "impact",
        "--state-dir",
        str(state_dir),
    ]
    for artifact_id in changed_artifact_ids:
        command.extend(["--changed-artifact", artifact_id])
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout or result.stderr


def _mark_recoverable(project_dir: Path, watched_paths: list[str]) -> tuple[bool, str]:
    if not watched_paths:
        return True, ""
    script = project_dir / ".claude" / "control-plane" / "scripts" / "idea_to_mvp_state.py"
    state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
    command = [
        sys.executable,
        str(script),
        "interrupt",
        "--state-dir",
        str(state_dir),
    ]
    for path in watched_paths:
        command.extend(["--changed-path", path])
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout or result.stderr


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        assert PLACEHOLDER_PATTERN.search("TODO")
        assert PLACEHOLDER_PATTERN.search("TBD")
        assert PLACEHOLDER_PATTERN.search("developer decides")
        assert PLACEHOLDER_PATTERN.search("[citation needed]")
        assert not PLACEHOLDER_PATTERN.search("done")
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            workflow_path = project_dir / ".claude" / "workflows" / "idea-to-mvp.js"
            workflow_path.parent.mkdir(parents=True, exist_ok=True)
            workflow_path.write_text("function () {}\n", encoding="utf-8")
            syntax_errors = _workflow_syntax_errors(project_dir, [".claude/workflows/idea-to-mvp.js"])
            assert syntax_errors
            assert any("workflow syntax check failed" in error for error in syntax_errors)
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            script_path = project_dir / ".claude" / "hooks" / "guard_idea_to_mvp_tool_use.py"
            script_path.parent.mkdir(parents=True, exist_ok=True)
            script_path.write_text("def broken(:\n", encoding="utf-8")
            syntax_errors = _python_syntax_errors(project_dir, [".claude/hooks/guard_idea_to_mvp_tool_use.py"])
            assert syntax_errors
            assert any("python syntax check failed" in error for error in syntax_errors)
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            validator_path = project_dir / ".claude" / "control-plane" / "scripts" / "validate.py"
            validator_path.parent.mkdir(parents=True, exist_ok=True)
            validator_path.write_text("raise SystemExit(1)\n", encoding="utf-8")
            config_errors = _config_validation_errors(project_dir, [".claude/settings.json"])
            assert config_errors
            assert any("config validation failed" in error for error in config_errors)
        with tempfile.TemporaryDirectory() as temp_dir:
            sample_payload = {"hook_event_name": "SessionEnd"}
            assert _watched_paths_for_payload(sample_payload, Path(temp_dir)) == []
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            workflow_path = project_dir / ".claude" / "workflows" / "idea-to-mvp.js"
            workflow_path.parent.mkdir(parents=True, exist_ok=True)
            workflow_path.write_text("// dirty\n", encoding="utf-8")
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True, text=True, check=False)
            payload = {"hook_event_name": "SubagentStop", "cwd": str(project_dir)}
            assert _watched_paths_for_payload(payload, project_dir) == [".claude/workflows/idea-to-mvp.js"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            workflow_path = project_dir / ".claude" / "workflows" / "idea-to-mvp.js"
            workflow_path.parent.mkdir(parents=True, exist_ok=True)
            workflow_path.write_text("// dirty\n", encoding="utf-8")
            subprocess.run(["git", "init"], cwd=project_dir, capture_output=True, text=True, check=False)
            payload = {"hook_event_name": "PostToolUse", "tool_name": "Bash"}
            assert _watched_paths_for_payload(payload, project_dir) == [".claude/workflows/idea-to-mvp.js"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
            (state_dir / "handoffs").mkdir(parents=True, exist_ok=True)
            (state_dir / "workflow-state.json").write_text(
                json.dumps(
                    {
                        "nodes": [
                            {"node": 12, "status": "eligible"},
                            {"node": 13, "status": "pending"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "handoffs" / "ho-12-test.json").write_text(
                json.dumps(
                    {
                        "workflow_node": 12,
                        "required_output": {"path": "artifacts/mvp-prd.md", "contract": "mvp-prd-v1"},
                    }
                ),
                encoding="utf-8",
            )
            assert _missing_required_outputs(project_dir) == ["artifacts/mvp-prd.md"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
            (state_dir / "handoffs").mkdir(parents=True, exist_ok=True)
            (state_dir / "workflow-state.json").write_text(
                json.dumps({"nodes": [{"node": 12, "status": "eligible"}]}),
                encoding="utf-8",
            )
            (state_dir / "artifact-manifest.json").write_text(
                json.dumps(
                    {
                        "artifacts": [
                            {
                                "artifact_id": "mvp-prd",
                                "path": "artifacts/mvp-prd.md",
                                "status": "draft",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "handoffs" / "ho-12-test.json").write_text(
                json.dumps(
                    {
                        "workflow_node": 12,
                        "required_output": {"path": "artifacts/mvp-prd.md", "contract": "mvp-prd-v1"},
                    }
                ),
                encoding="utf-8",
            )
            assert _required_outputs_not_review_ready(project_dir) == ["artifacts/mvp-prd.md"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
            (state_dir / "handoffs").mkdir(parents=True, exist_ok=True)
            (state_dir / "workflow-state.json").write_text(
                json.dumps({"nodes": [{"node": 12, "status": "eligible"}]}),
                encoding="utf-8",
            )
            (state_dir / "artifact-manifest.json").write_text(
                json.dumps(
                    {
                        "artifacts": [
                            {
                                "artifact_id": "mvp-prd",
                                "path": "artifacts/mvp-prd.md",
                                "status": "review_required",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "handoffs" / "ho-12-test.json").write_text(
                json.dumps(
                    {
                        "workflow_node": 12,
                        "required_output": {"path": "artifacts/mvp-prd.md", "contract": "mvp-prd-v1"},
                    }
                ),
                encoding="utf-8",
            )
            assert _required_outputs_not_review_ready(project_dir) == ["artifacts/mvp-prd.md"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
            (state_dir / "handoffs").mkdir(parents=True, exist_ok=True)
            (state_dir / "workflow-state.json").write_text(
                json.dumps({"nodes": [{"node": 12, "status": "eligible"}]}),
                encoding="utf-8",
            )
            (state_dir / "handoffs" / "ho-12-test.json").write_text(
                json.dumps(
                    {
                        "workflow_node": 12,
                        "required_output": {"path": "artifacts/mvp-prd.md", "contract": "mvp-prd-v1"},
                    }
                ),
                encoding="utf-8",
            )
            assert _handoffs_missing_completion_results(project_dir) == ["ho-12-test.json"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
            handoffs_dir = state_dir / "handoffs"
            handoffs_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "workflow-state.json").write_text(
                json.dumps(
                    {
                        "nodes": [
                            {"node": 12, "status": "eligible"},
                            {"node": 13, "status": "pending"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            handoff_path = handoffs_dir / "ho-12-test.json"
            handoff_path.write_text(json.dumps({"workflow_node": 12}, indent=2), encoding="utf-8")
            _record_changed_paths(project_dir, ["artifacts/mvp-prd.md", ".claude/workflows/idea-to-mvp.js"])
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
            assert packet["changed_paths"] == [".claude/workflows/idea-to-mvp.js", "artifacts/mvp-prd.md"]
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "artifact-manifest.json").write_text(
                json.dumps(
                    {
                        "artifacts": [
                            {
                                "artifact_id": "core-problem-decision",
                                "path": "artifacts/core-problem-decision.md",
                                "status": "approved",
                            },
                            {
                                "artifact_id": "value-proposition",
                                "path": "artifacts/value-proposition.md",
                                "status": "draft",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )
            assert _artifact_ids_needing_change_impact(
                project_dir,
                ["artifacts/core-problem-decision.md", "artifacts/value-proposition.md"],
            ) == ["core-problem-decision"]
        return 0

    try:
        payload = _load_payload()
    except (json.JSONDecodeError, ValueError) as exc:
        sys.stderr.write(f"Invalid hook payload: {exc}\n")
        return 2

    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        sys.stderr.write("Invalid hook payload: missing cwd\n")
        return 2

    project_dir = Path(cwd)
    event_name = payload.get("hook_event_name")
    watched_paths = _watched_paths_for_payload(payload, project_dir)
    if not watched_paths and event_name not in {"Stop", "SubagentStop"}:
        return 0

    if event_name in {"Stop", "StopFailure", "SessionEnd"}:
        interrupted, output = _mark_recoverable(project_dir, watched_paths)
        if not interrupted:
            sys.stderr.write(output)
            return 2
        if event_name != "Stop":
            return 0

    _record_changed_paths(project_dir, watched_paths)

    if event_name == "PostToolUse":
        changed_artifact_ids = _artifact_ids_needing_change_impact(project_dir, watched_paths)
        impact_applied, impact_output = _apply_change_impact(project_dir, changed_artifact_ids)
        if not impact_applied:
            sys.stderr.write(impact_output)
            return 2

    placeholder_hits = _placeholder_hits(project_dir, watched_paths)
    if placeholder_hits:
        sys.stderr.write(
            "Authoritative idea-to-MVP artifacts still contain unresolved placeholders: "
            + ", ".join(placeholder_hits)
            + "\n"
        )
        return 2
    workflow_syntax_errors = _workflow_syntax_errors(project_dir, watched_paths)
    if workflow_syntax_errors:
        sys.stderr.write("\n".join(workflow_syntax_errors) + "\n")
        return 2
    python_syntax_errors = _python_syntax_errors(project_dir, watched_paths)
    if python_syntax_errors:
        sys.stderr.write("\n".join(python_syntax_errors) + "\n")
        return 2
    config_validation_errors = _config_validation_errors(project_dir, watched_paths)
    if config_validation_errors:
        sys.stderr.write("\n".join(config_validation_errors) + "\n")
        return 2

    missing_outputs = _missing_required_outputs(project_dir)
    if missing_outputs:
        sys.stderr.write(
            "Active idea-to-MVP handoffs are missing required outputs: "
            + ", ".join(missing_outputs)
            + "\n"
        )
        return 2
    if event_name in {"Stop", "SubagentStop"}:
        incomplete_outputs = _required_outputs_not_review_ready(project_dir)
        if incomplete_outputs:
            sys.stderr.write(
                "Active idea-to-MVP handoffs still have non-review-ready required outputs: "
                + ", ".join(incomplete_outputs)
                + "\n"
            )
            return 2
        incomplete_results = _handoffs_missing_completion_results(project_dir)
        if incomplete_results:
            sys.stderr.write(
                "Active idea-to-MVP handoffs are missing structured completion results: "
                + ", ".join(incomplete_results)
                + "\n"
            )
            return 2

    script = project_dir / ".claude" / "control-plane" / "scripts" / "idea_to_mvp_state.py"
    state_dir = project_dir / ".claude" / "control-plane" / "state" / "idea-to-mvp"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "validate",
            "--state-dir",
            str(state_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return 0
    sys.stderr.write(result.stdout or result.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
