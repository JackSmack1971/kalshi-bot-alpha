from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

STATE_ROOT = Path(".claude/control-plane/state/idea-to-mvp")
ARTIFACTS_ROOT = STATE_ROOT / "artifacts"
EXEMPT_AGENT_TYPES = {
    "workflow-state-manager",
    # Control-plane specialists are governed by .claude/control-plane/manifest.yaml's
    # owners map, not by idea-to-mvp workflow handoffs. They never receive an
    # idea-to-mvp handoff, so without this exemption they are unconditionally
    # blocked from every Edit/Write/Bash call.
    "skills-specialist",
    "rules-specialist",
    "workflow-specialist",
}
PRODUCTION_AGENT_TYPES = {"devops-engineer"}

SENSITIVE_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env(\.|$)"),
    re.compile(r"(^|/).*\.pem$"),
    re.compile(r"(^|/).*\.key$"),
    re.compile(r"(^|/)id_rsa(\.|$)"),
    re.compile(r"(^|/).*\.p12$"),
    re.compile(r"(^|/).*\.crt$"),
)

PRODUCTION_COMMAND_PATTERNS = (
    re.compile(r"\bkubectl\s+(apply|delete|patch|rollout|scale)\b"),
    re.compile(r"\bhelm\s+(install|upgrade|rollback|uninstall)\b"),
    re.compile(r"\bterraform\s+apply\b"),
    re.compile(r"\b(prisma|alembic|flyway|liquibase)\b.*\b(migrate|upgrade|deploy)\b"),
    re.compile(r"\bvercel\b.*\s--prod\b"),
    re.compile(r"\bnetlify\b.*\s--prod\b"),
    re.compile(r"\b(fly|flyctl)\s+deploy\b"),
)


def _load_payload() -> dict:
    payload = json.load(sys.stdin)
    if not isinstance(payload, dict):
        raise ValueError("root must be an object")
    return payload


def _workflow_state(project_dir: Path) -> dict:
    path = project_dir / STATE_ROOT / "workflow-state.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _denied_sensitive_path(file_path: str) -> str | None:
    normalized = file_path.replace("\\", "/")
    for pattern in SENSITIVE_PATH_PATTERNS:
        if pattern.search(normalized):
            return normalized
    return None


def _is_production_command(command: str) -> bool:
    return any(pattern.search(command) for pattern in PRODUCTION_COMMAND_PATTERNS)


def _launch_authorized(state: dict) -> bool:
    return state.get("current_phase") == "launch" and not state.get("required_human_decisions")


def _production_command_authorized(agent_type: str | None) -> bool:
    return bool(agent_type and agent_type in (PRODUCTION_AGENT_TYPES | EXEMPT_AGENT_TYPES))


def _active_nodes(state: dict) -> set[int]:
    active = set()
    nodes = state.get("nodes")
    if not isinstance(nodes, list):
        return active
    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_id = node.get("node")
        status = node.get("status")
        if isinstance(node_id, int) and status in {"eligible", "in-progress", "recoverable", "rework"}:
            active.add(node_id)
    return active


def _artifact_portable_path(project_dir: Path, file_path: str) -> str | None:
    try:
        candidate = Path(file_path)
        if not candidate.is_absolute():
            candidate = (project_dir / candidate).resolve()
        else:
            candidate = candidate.resolve()
        artifact_root = (project_dir / ARTIFACTS_ROOT).resolve()
        relative = candidate.relative_to(artifact_root)
    except Exception:
        return None
    return "artifacts/" + relative.as_posix()


def _project_relative_path(project_dir: Path, file_path: str) -> str | None:
    try:
        candidate = Path(file_path)
        if not candidate.is_absolute():
            candidate = (project_dir / candidate).resolve()
        else:
            candidate = candidate.resolve()
        relative = candidate.relative_to(project_dir.resolve())
    except Exception:
        return None
    return relative.as_posix()


def _active_handoff_paths(project_dir: Path, agent_type: str, active_nodes: set[int]) -> tuple[set[str], set[str]]:
    owned_paths: set[str] = set()
    read_only_paths: set[str] = set()
    handoffs_dir = project_dir / STATE_ROOT / "handoffs"
    if not handoffs_dir.exists():
        return owned_paths, read_only_paths
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        if packet.get("assigned_agent") != agent_type:
            continue
        workflow_node = packet.get("workflow_node")
        if workflow_node not in active_nodes:
            continue
        allowed_paths = packet.get("allowed_paths")
        if not isinstance(allowed_paths, dict):
            continue
        owned = allowed_paths.get("owned_paths")
        read_only = allowed_paths.get("read_only_paths")
        if isinstance(owned, list):
            owned_paths.update(path for path in owned if isinstance(path, str))
        if isinstance(read_only, list):
            read_only_paths.update(path for path in read_only if isinstance(path, str))
    return owned_paths, read_only_paths


def _active_starting_branches(project_dir: Path, agent_type: str, active_nodes: set[int]) -> set[str]:
    branches: set[str] = set()
    handoffs_dir = project_dir / STATE_ROOT / "handoffs"
    if not handoffs_dir.exists():
        return branches
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        if packet.get("assigned_agent") != agent_type or packet.get("workflow_node") not in active_nodes:
            continue
        execution_contract = packet.get("execution_contract")
        if not isinstance(execution_contract, dict):
            continue
        starting_branch = execution_contract.get("starting_branch")
        if isinstance(starting_branch, str) and starting_branch.strip():
            branches.add(starting_branch.strip())
    return branches


def _current_branch(project_dir: Path) -> str | None:
    result = subprocess.run(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        branch = result.stdout.strip()
        if branch:
            return branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    branch = result.stdout.strip()
    return branch if branch and branch != "HEAD" else None


def _branch_ownership_violation(project_dir: Path, agent_type: str | None) -> str | None:
    if not agent_type or agent_type in EXEMPT_AGENT_TYPES:
        return None
    state = _workflow_state(project_dir)
    active_nodes = _active_nodes(state)
    if not active_nodes:
        return None
    expected_branches = _active_starting_branches(project_dir, agent_type, active_nodes)
    if not expected_branches:
        return None
    current_branch = _current_branch(project_dir)
    if current_branch is None or current_branch not in expected_branches:
        expected = ", ".join(sorted(expected_branches))
        observed = current_branch or "unknown"
        return (
            "Branch ownership blocked by idea-to-MVP hook: "
            f"agent {agent_type!r} must work from delegated branch {expected!r}, found {observed!r}."
        )
    return None


def _has_active_write_permission(project_dir: Path, agent_type: str | None) -> bool:
    return _has_active_tool_permission(project_dir, agent_type, {"Write", "Edit"})


def _has_active_tool_permission(project_dir: Path, agent_type: str | None, required_permissions: set[str]) -> bool:
    if not agent_type or agent_type in EXEMPT_AGENT_TYPES:
        return True
    state = _workflow_state(project_dir)
    active_nodes = _active_nodes(state)
    if not active_nodes:
        return False
    handoffs_dir = project_dir / STATE_ROOT / "handoffs"
    if not handoffs_dir.exists():
        return False
    for handoff_path in handoffs_dir.glob("*.json"):
        try:
            packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        if packet.get("assigned_agent") != agent_type or packet.get("workflow_node") not in active_nodes:
            continue
        tool_permissions = packet.get("tool_permissions")
        if isinstance(tool_permissions, list) and any(
            permission in required_permissions for permission in tool_permissions
        ):
            return True
    return False


def _delegated_path_violation(project_dir: Path, agent_type: str | None, file_path: str) -> str | None:
    if not agent_type or agent_type in EXEMPT_AGENT_TYPES:
        return None
    portable_path = _artifact_portable_path(project_dir, file_path)
    if portable_path is None:
        return None
    state = _workflow_state(project_dir)
    active_nodes = _active_nodes(state)
    if not active_nodes:
        return None
    owned_paths, read_only_paths = _active_handoff_paths(project_dir, agent_type, active_nodes)
    if not owned_paths and not read_only_paths:
        return (
            "Authoritative artifact write blocked by idea-to-MVP hook because "
            f"agent {agent_type!r} has no active delegated handoff for {portable_path}."
        )
    if portable_path in read_only_paths and portable_path not in owned_paths:
        return (
            "Read-only authoritative artifact blocked by idea-to-MVP hook: "
            f"{portable_path} is an authoritative input for agent {agent_type!r}."
        )
    if portable_path not in owned_paths:
        return (
            "Authoritative artifact write blocked by idea-to-MVP hook: "
            f"{portable_path} is outside delegated owned_paths for agent {agent_type!r}."
        )
    return None


def _code_write_violation(project_dir: Path, agent_type: str | None, file_path: str) -> str | None:
    relative_path = _project_relative_path(project_dir, file_path)
    if relative_path is None:
        return None
    if relative_path.startswith(".git/") or relative_path.startswith(STATE_ROOT.as_posix() + "/"):
        return None
    if _has_active_write_permission(project_dir, agent_type):
        return None
    return (
        "Code changes blocked by idea-to-MVP hook: "
        f"agent {agent_type!r} has no active handoff that permits repository code edits for {relative_path}."
    )


def _bash_permission_violation(project_dir: Path, agent_type: str | None) -> str | None:
    if not agent_type or agent_type in EXEMPT_AGENT_TYPES:
        return None
    if _has_active_tool_permission(project_dir, agent_type, {"Bash"}):
        return None
    return (
        "Bash blocked by idea-to-MVP hook: "
        f"agent {agent_type!r} has no active handoff that permits Bash tool use."
    )


def _state_write_violation(project_dir: Path, agent_type: str | None, file_path: str) -> str | None:
    relative_path = _project_relative_path(project_dir, file_path)
    if relative_path is None:
        return None
    state_prefix = STATE_ROOT.as_posix() + "/"
    if not relative_path.startswith(state_prefix):
        return None
    if agent_type in EXEMPT_AGENT_TYPES:
        return None
    artifact_path = _artifact_portable_path(project_dir, file_path)
    if artifact_path is not None:
        return None
    return (
        "Canonical idea-to-MVP state write blocked by idea-to-MVP hook: "
        f"agent {agent_type!r} must use workflow-state-manager for {relative_path}."
    )


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        assert _denied_sensitive_path(".env") == ".env"
        assert _denied_sensitive_path("config/app.pem") == "config/app.pem"
        assert _denied_sensitive_path("src/app.py") is None
        assert _is_production_command("kubectl apply -f deploy.yml")
        assert _is_production_command("terraform apply")
        assert not _is_production_command("python -m pytest")
        assert not _launch_authorized({"current_phase": "build", "required_human_decisions": []})
        assert _launch_authorized({"current_phase": "launch", "required_human_decisions": []})
        assert _production_command_authorized("devops-engineer")
        assert _production_command_authorized("workflow-state-manager")
        assert not _production_command_authorized("product-manager")
        assert _active_nodes({"nodes": [{"node": 12, "status": "eligible"}, {"node": 13, "status": "pending"}]}) == {12}
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            state_dir = project_dir / STATE_ROOT
            handoffs_dir = state_dir / "handoffs"
            handoffs_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init", "-q"], cwd=project_dir, capture_output=True, text=True, check=False)
            subprocess.run(
                ["git", "symbolic-ref", "HEAD", "refs/heads/parallel-slice"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            (state_dir / "workflow-state.json").write_text(
                json.dumps({"nodes": [{"node": 20, "status": "eligible"}]}),
                encoding="utf-8",
            )
            (handoffs_dir / "ho-20.json").write_text(
                json.dumps(
                    {
                        "workflow_node": 20,
                        "assigned_agent": "backend-engineer",
                        "tool_permissions": ["Read", "Grep", "Glob", "Write", "Edit", "Bash"],
                        "execution_contract": {"starting_branch": "parallel-slice"},
                    }
                ),
                encoding="utf-8",
            )
            assert _has_active_write_permission(project_dir, "backend-engineer") is True
            assert _has_active_write_permission(project_dir, "product-manager") is False
            assert _active_starting_branches(project_dir, "backend-engineer", {20}) == {"parallel-slice"}
            assert _branch_ownership_violation(project_dir, "backend-engineer") is None
            assert _current_branch(project_dir) == "parallel-slice"
            subprocess.run(
                ["git", "symbolic-ref", "HEAD", "refs/heads/wrong-branch"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            assert _branch_ownership_violation(project_dir, "backend-engineer")
            subprocess.run(
                ["git", "symbolic-ref", "HEAD", "refs/heads/parallel-slice"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            assert _code_write_violation(project_dir, "product-manager", str(project_dir / "src" / "app.ts"))
            assert _code_write_violation(project_dir, "backend-engineer", str(project_dir / "src" / "app.ts")) is None
            assert _has_active_tool_permission(project_dir, "backend-engineer", {"Bash"}) is True
            assert _has_active_tool_permission(project_dir, "product-manager", {"Bash"}) is False
            assert _bash_permission_violation(project_dir, "product-manager")
            assert _bash_permission_violation(project_dir, "backend-engineer") is None
            state_file = state_dir / "workflow-state.json"
            assert _state_write_violation(project_dir, "backend-engineer", str(state_file))
            assert _state_write_violation(project_dir, "product-manager", str(state_file))
            assert _state_write_violation(project_dir, "workflow-state-manager", str(state_file)) is None
            artifact_file = state_dir / "artifacts" / "backend-implementation.md"
            artifact_file.parent.mkdir(parents=True, exist_ok=True)
            assert _state_write_violation(project_dir, "backend-engineer", str(artifact_file)) is None
        return 0

    try:
        payload = _load_payload()
    except (json.JSONDecodeError, ValueError) as exc:
        sys.stderr.write(f"Invalid PreToolUse payload: {exc}\n")
        return 2

    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input", {})
    cwd = payload.get("cwd")
    project_dir = Path(cwd) if isinstance(cwd, str) and cwd else None
    agent_type = payload.get("agent_type") if isinstance(payload.get("agent_type"), str) else None

    if tool_name in {"Edit", "Write"} and isinstance(tool_input, dict):
        file_path = tool_input.get("file_path")
        if isinstance(file_path, str) and project_dir:
            branch_ownership_violation = _branch_ownership_violation(project_dir, agent_type)
            if branch_ownership_violation:
                sys.stderr.write(branch_ownership_violation + "\n")
                return 2
            denied = _denied_sensitive_path(file_path)
            if denied:
                sys.stderr.write(f"Sensitive file access blocked by idea-to-MVP hook: {denied}\n")
                return 2
            state_write_violation = _state_write_violation(project_dir, agent_type, file_path)
            if state_write_violation:
                sys.stderr.write(state_write_violation + "\n")
                return 2
            delegated_violation = _delegated_path_violation(project_dir, agent_type, file_path)
            if delegated_violation:
                sys.stderr.write(delegated_violation + "\n")
                return 2
            code_write_violation = _code_write_violation(project_dir, agent_type, file_path)
            if code_write_violation:
                sys.stderr.write(code_write_violation + "\n")
                return 2

    if tool_name == "Bash" and isinstance(tool_input, dict):
        command = tool_input.get("command")
        if project_dir:
            branch_ownership_violation = _branch_ownership_violation(project_dir, agent_type)
            if branch_ownership_violation:
                sys.stderr.write(branch_ownership_violation + "\n")
                return 2
            bash_permission_violation = _bash_permission_violation(project_dir, agent_type)
            if bash_permission_violation:
                sys.stderr.write(bash_permission_violation + "\n")
                return 2
        if isinstance(command, str) and _is_production_command(command):
            state = _workflow_state(project_dir) if project_dir else {}
            if not _launch_authorized(state):
                phase = state.get("current_phase", "unknown")
                sys.stderr.write(
                    "Production deploy or migration command blocked by idea-to-MVP hook "
                    f"while workflow phase is {phase!r} without launch authorization.\n"
                )
                return 2
            if not _production_command_authorized(agent_type):
                sys.stderr.write(
                    "Production deploy or migration command blocked by idea-to-MVP hook "
                    f"for unauthorized agent {agent_type!r}.\n"
                )
                return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
