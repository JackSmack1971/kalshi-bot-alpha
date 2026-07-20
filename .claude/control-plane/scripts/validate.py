from __future__ import annotations

import argparse
from pathlib import Path
import fnmatch
import json
import re
import sys
import tempfile
from typing import Any

from common import (
    build_inventory_document,
    find_repo_root,
    load_json,
    load_yaml,
    simple_frontmatter,
    stable_file_fingerprint,
)


def _parse_manifest_scalar(value: str) -> Any:
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None
    if value.startswith(('"', "'")) and value.endswith(('"', "'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def _next_content_line(lines: list[str], start: int) -> str | None:
    for candidate in lines[start:]:
        if candidate.strip() and not candidate.lstrip().startswith("#"):
            return candidate
    return None


def _parse_manifest_yaml_subset(text: str) -> dict[str, Any]:
    """Parse the deterministic YAML subset used by manifest.yaml.

    Supported constructs are enough for the control-plane manifest: nested
    mappings, scalar list items, integer/boolean/string scalars, blank lines,
    and full-line comments. Unsupported YAML syntax raises ValueError so the
    primary validator fails closed instead of silently skipping manifest checks.
    """
    lines = text.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    for index, raw in enumerate(lines):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("\t"):
            raise ValueError(f"line {index + 1}: tabs are not supported")
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2 != 0:
            raise ValueError(f"line {index + 1}: indentation must use two-space levels")
        stripped = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"line {index + 1}: invalid indentation")
        parent = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(parent, list):
                raise ValueError(f"line {index + 1}: list item without list parent")
            value = stripped[2:].strip()
            if not value or ":" in value:
                raise ValueError(f"line {index + 1}: only scalar list items are supported")
            parent.append(_parse_manifest_scalar(value))
            continue

        if ":" not in stripped:
            raise ValueError(f"line {index + 1}: expected key/value mapping")
        key, raw_value = stripped.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not key:
            raise ValueError(f"line {index + 1}: empty mapping key")
        if not isinstance(parent, dict):
            raise ValueError(f"line {index + 1}: mapping entry without mapping parent")

        if raw_value:
            parent[key] = _parse_manifest_scalar(raw_value)
            continue

        next_line = _next_content_line(lines, index + 1)
        child: list[Any] | dict[str, Any]
        child = [] if next_line and next_line.strip().startswith("- ") else {}
        parent[key] = child
        stack.append((indent, child))

    return root


def _load_manifest_yaml(path: Path, force_fallback: bool = False) -> dict[str, Any]:
    if not force_fallback:
        try:
            manifest = load_yaml(path)
        except RuntimeError:
            manifest = _parse_manifest_yaml_subset(path.read_text(encoding="utf-8"))
    else:
        manifest = _parse_manifest_yaml_subset(path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("manifest root must be a mapping")
    return manifest


def _require_manifest_value(
    manifest: dict[str, Any],
    dotted_key: str,
    expected: Any,
    errors: list[str],
    warnings: list[str],
    *,
    warn_on_mismatch: bool = False,
) -> None:
    current: Any = manifest
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            errors.append(f"manifest.yaml: missing required field {dotted_key}")
            return
        current = current[part]
    if current != expected:
        message = f"manifest.yaml: {dotted_key} must be {expected!r}"
        if warn_on_mismatch:
            warnings.append(message)
        else:
            errors.append(message)


def _manifest_string_list(manifest: dict[str, Any], key: str, errors: list[str]) -> list[str]:
    values = manifest.get(key)
    if not isinstance(values, list) or not values:
        errors.append(f"manifest.yaml: {key} must be a non-empty list")
        return []
    if not all(isinstance(item, str) and item for item in values):
        errors.append(f"manifest.yaml: {key} entries must be non-empty strings")
        return []
    return values


def _require_manifest_list_items(
    manifest: dict[str, Any], key: str, required: set[str], errors: list[str]
) -> None:
    values = _manifest_string_list(manifest, key, errors)
    missing = sorted(required.difference(values))
    if missing:
        errors.append(f"manifest.yaml: {key} must include {', '.join(missing)}")


def _validate_manifest_contract(manifest: dict[str, Any], errors: list[str], warnings: list[str]) -> None:
    _require_manifest_value(manifest, "schema_version", 1, errors, warnings)
    _require_manifest_list_items(manifest, "control_plane_roots", {".claude/", "AGENTS.md"}, errors)
    _require_manifest_list_items(
        manifest, "forbidden_roots", {".git/", "secrets/", "credentials/"}, errors
    )

    owners = manifest.get("owners")
    required_owners = {"skills-specialist", "rules-specialist", "workflow-specialist"}
    if not isinstance(owners, dict) or not owners:
        errors.append("manifest.yaml: owners must be a non-empty mapping")
    else:
        missing_owners = sorted(required_owners.difference(owners))
        if missing_owners:
            errors.append(f"manifest.yaml: owners must include {', '.join(missing_owners)}")
        for owner, patterns in owners.items():
            valid_owner = isinstance(owner, str) and bool(owner)
            valid_patterns = (
                isinstance(patterns, list)
                and bool(patterns)
                and all(isinstance(item, str) and item for item in patterns)
            )
            if not valid_owner or not valid_patterns:
                errors.append("manifest.yaml: each owners entry must be a non-empty list of paths")
    _require_manifest_value(manifest, "verification.independent_verifier_required", True, errors, warnings)
    _require_manifest_value(manifest, "verification.rollback_on_failure", True, errors, warnings)
    _require_manifest_value(manifest, "verification.fresh_session_behavioral_evals", True, errors, warnings)
    _require_manifest_value(manifest, "verification.baseline_comparison_required_for_skills", True, errors, warnings)
    _require_manifest_value(manifest, "budgets.max_concurrent_writers", 1, errors, warnings)
    _require_manifest_value(manifest, "budgets.max_nested_agent_depth", 0, errors, warnings, warn_on_mismatch=True)
    _require_manifest_value(manifest, "experimental_features.agent_teams.default", "disabled", errors, warnings)
    _require_manifest_value(
        manifest, "experimental_features.agent_teams.require_explicit_enablement", True, errors, warnings
    )
    _require_manifest_value(manifest, "memory.accept_only_verified_runs", True, errors, warnings)
    _require_manifest_value(manifest, "runs.directory", ".claude/control-plane/runs", errors, warnings)
    _require_manifest_value(manifest, "runs.append_only_events", True, errors, warnings)
    _require_manifest_value(manifest, "runs.hash_chain_events", True, errors, warnings)


REQUIRED_EVAL_FILES = (
    "routing-cases.yaml",
    "skills-cases.yaml",
    "rules-cases.yaml",
    "workflow-cases.yaml",
)


def _eval_cases_from_document(path: Path, document: Any, errors: list[str]) -> list[dict[str, Any]]:
    if isinstance(document, dict):
        cases = document.get("cases")
    else:
        cases = document
    if isinstance(cases, dict):
        cases = list(cases.values())
    if not isinstance(cases, list) or not cases:
        errors.append(f"{path}: eval cases must be a non-empty list or mapping")
        return []
    normalized = []
    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            errors.append(f"{path}: case {index} must be a mapping")
            continue
        normalized.append(case)
    return normalized


def _has_non_empty_string(case: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(isinstance(case.get(key), str) and bool(case.get(key).strip()) for key in keys)


def _has_non_empty_list(case: dict[str, Any], key: str) -> bool:
    value = case.get(key)
    return isinstance(value, list) and bool(value) and all(isinstance(item, str) and item for item in value)


def _validate_eval_case(path: Path, case: dict[str, Any], errors: list[str]) -> None:
    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id.strip():
        errors.append(f"{path}: each eval case must have a non-empty string id")
    elif case_id != case_id.strip() or " " in case_id:
        errors.append(f"{path}: eval case id {case_id!r} must be stable and whitespace-free")

    if not _has_non_empty_string(case, ("prompt", "input", "invocation")):
        errors.append(f"{path}: eval case {case_id!r} must define prompt, input, or invocation")

    has_expected_owner = "expected_owner" in case
    has_expected_outcome = _has_non_empty_string(case, ("expected_outcome",))
    has_assertions = _has_non_empty_list(case, "assertions")
    if not (has_expected_owner or has_expected_outcome or has_assertions):
        errors.append(
            f"{path}: eval case {case_id!r} must define expected_owner, "
            "expected_outcome, or non-empty assertions"
        )

    if path.name == "routing-cases.yaml":
        if "expected_abstention" not in case or not isinstance(case.get("expected_abstention"), bool):
            errors.append(f"{path}: routing case {case_id!r} must define boolean expected_abstention")
        if case.get("expected_abstention") is True and case.get("expected_owner") is not None:
            errors.append(f"{path}: abstention case {case_id!r} must set expected_owner to null")


def _validate_eval_document(path: Path, document: Any, errors: list[str], warnings: list[str]) -> None:
    cases = _eval_cases_from_document(path, document, errors)
    seen_ids: set[str] = set()
    has_negative_or_abstention = False
    for case in cases:
        case_id = case.get("id")
        if isinstance(case_id, str):
            if case_id in seen_ids:
                errors.append(f"{path}: duplicate eval case id {case_id!r}")
            seen_ids.add(case_id)
            if "NEGATIVE" in case_id or "ABSTAIN" in case_id:
                has_negative_or_abstention = True
        if case.get("expected_abstention") is True or _has_non_empty_list(case, "forbidden"):
            has_negative_or_abstention = True
        if _has_non_empty_list(case, "assertions") and any(
            item.startswith(("Do not", "Reject", "Exclude", "Fail")) for item in case["assertions"]
        ):
            has_negative_or_abstention = True
        _validate_eval_case(path, case, errors)

    if cases and not has_negative_or_abstention:
        warnings.append(f"{path}: no negative or abstention coverage was detected")


def validate_eval_files(root: Path, errors: list[str], warnings: list[str]) -> None:
    evals_dir = root / ".claude/control-plane/evals"
    for filename in REQUIRED_EVAL_FILES:
        path = evals_dir / filename
        if not path.exists():
            continue
        try:
            document = load_yaml(path)
        except Exception as exc:
            errors.append(f"{path}: invalid eval YAML: {exc}")
            continue
        _validate_eval_document(path, document, errors, warnings)

REQUIRED_AGENTS = {
    "skills-specialist.md": "skills-specialist",
    "rules-specialist.md": "rules-specialist",
    "workflow-specialist.md": "workflow-specialist",
    "control-plane-verifier.md": "control-plane-verifier",
}

REQUIRED_IDEA_AGENTS = {
    "mvp-orchestrator.md": "mvp-orchestrator",
    "product-strategist.md": "product-strategist",
    "market-researcher.md": "market-researcher",
    "product-manager.md": "product-manager",
    "ux-designer.md": "ux-designer",
    "ui-designer.md": "ui-designer",
    "ux-researcher.md": "ux-researcher",
    "solution-architect.md": "solution-architect",
    "backend-engineer.md": "backend-engineer",
    "frontend-engineer.md": "frontend-engineer",
    "integration-engineer.md": "integration-engineer",
    "technical-lead.md": "technical-lead",
    "security-engineer.md": "security-engineer",
    "qa-engineer.md": "qa-engineer",
    "devops-engineer.md": "devops-engineer",
    "data-analyst.md": "data-analyst",
    "workflow-state-manager.md": "workflow-state-manager",
}

REQUIRED_WORKFLOW_PAIRS = (
    ("idea-to-mvp.js", "idea-to-mvp.md"),
    ("discover-phase.js", "discover-phase.md"),
    ("define-phase.js", "define-phase.md"),
    ("design-phase.js", "design-phase.md"),
    ("build-phase.js", "build-phase.md"),
    ("test-phase.js", "test-phase.md"),
    ("change-impact-loop.js", "change-impact-loop.md"),
    ("launch-phase.js", "launch-phase.md"),
    ("feedback-loop.js", "feedback-loop.md"),
)

REQUIRED_RULES = {
    "workflow-governance.md": ("approval", "structured status"),
    "artifact-contracts.md": ("direct upstream dependencies", "schema-valid"),
    "evidence-policy.md": ("verified evidence", "re-entry status"),
    "decision-authority.md": ("human approval", "Release authorization is separate from deployment readiness"),
    "design-quality.md": ("approved MVP scope", "Usability findings"),
    "engineering-quality.md": ("approved MVP scope", "smallest correct diff"),
    "testing-policy.md": ("blocks launch", "Performance and security checks"),
    "security-policy.md": ("hard controls", "required human decisions"),
    "release-policy.md": ("analytics readiness", "one explicit decision"),
    "repository-boundaries.md": ("inside `.claude/`", "manifest.yaml"),
}

PHASE_WORKFLOW_CURSOR_FIELDS = {
    "discover-phase.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"discover"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\b(?:\s*:|\s*,)")),
        ("activeRisks", re.compile(r"\bactiveRisks\s*:")),
    ),
    "define-phase.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"define"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\s*:")),
        ("activeRisks", re.compile(r"\bactiveRisks\s*:")),
    ),
    "design-phase.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"design"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\s*:")),
        ("activeRisks", re.compile(r"\bactiveRisks\s*:")),
    ),
    "build-phase.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"build"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\s*:")),
        ("activeRisks", re.compile(r"\bactiveRisks\s*:")),
    ),
    "test-phase.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"test"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\s*:")),
        ("activeRisks", re.compile(r"\bactiveRisks\s*:")),
    ),
    "launch-phase.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"launch"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\b(?:\s*:|\s*,)")),
        ("activeRisks", re.compile(r"\bactiveRisks\b(?:\s*:|\s*,)")),
    ),
    "feedback-loop.js": (
        ("currentPhase", re.compile(r'currentPhase\s*:\s*"feedback"')),
        ("status", re.compile(r"\bstatus\s*:")),
        ("completedNodes", re.compile(r"\bcompletedNodes\s*:")),
        ("eligibleNodes", re.compile(r"\beligibleNodes\s*:")),
        ("blockedNodes", re.compile(r"\bblockedNodes\s*:")),
        ("artifacts", re.compile(r"\bartifacts\s*:")),
        ("requiredHumanDecisions", re.compile(r"\brequiredHumanDecisions\s*:")),
        ("activeRisks", re.compile(r"\bactiveRisks\s*:")),
    ),
}

REQUIRED_WORKFLOW_RUNTIME_SNIPPETS = {
    "idea-to-mvp.js": (
        "idea_to_mvp_state.py persist --state-dir",
        "Do not freehand-edit workflow-state.json, artifact-manifest.json, artifact markdown, handoff JSON, decision records, or gate results",
    ),
}

REQUIRED_WORKFLOW_CONTRACT_SECTIONS = (
    "## States and Legal Transitions",
    "## Input Contract",
    "## Output Contract",
    "## Read Set",
    "## Write Set",
    "## Success Criteria",
    "## Failure Criteria",
    "## Budgets",
    "## Resume and Rollback",
    "## Observability",
    "## Human Approval Points",
)

REQUIRED_HOOK_COMMANDS = {
    "UserPromptSubmit": [
        {
            "command": "python",
            "args": [
                "${CLAUDE_PROJECT_DIR}/.claude/control-plane/scripts/self_improvement_evidence.py",
                "--hook",
            ],
        }
    ],
    "PreToolUse": [
        {
            "matcher": "Edit|Write|Bash",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/guard_idea_to_mvp_tool_use.py"],
        }
    ],
    "PostToolUse": [
        {
            "matcher": "Edit|Write|Bash",
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_idea_to_mvp_state.py"],
        }
    ],
    "Stop": [
        {
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_idea_to_mvp_state.py"],
        }
    ],
    "SubagentStop": [
        {
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_idea_to_mvp_state.py"],
        }
    ],
    "StopFailure": [
        {
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_idea_to_mvp_state.py"],
        }
    ],
    "SessionEnd": [
        {
            "command": "python",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/validate_idea_to_mvp_state.py"],
        }
    ],
}

REQUIRED_HOOK_SCRIPT_SNIPPETS = {
    ".claude/hooks/guard_idea_to_mvp_tool_use.py": (
        "STATE_ROOT",
        "ARTIFACTS_ROOT",
        "EXEMPT_AGENT_TYPES",
        "PRODUCTION_AGENT_TYPES",
        "SENSITIVE_PATH_PATTERNS",
        "PRODUCTION_COMMAND_PATTERNS",
        "_active_nodes",
        "_artifact_portable_path",
        "_project_relative_path",
        "_active_handoff_paths",
        "_has_active_write_permission",
        "_delegated_path_violation",
        "_code_write_violation",
        "_state_write_violation",
        "_denied_sensitive_path",
        "_is_production_command",
        "_launch_authorized",
        "_production_command_authorized",
        'tool_name in {"Edit", "Write"}',
        'tool_name == "Bash"',
        "Invalid PreToolUse payload",
        "Authoritative artifact write blocked by idea-to-MVP hook",
        "Read-only authoritative artifact blocked by idea-to-MVP hook",
        "Code changes blocked by idea-to-MVP hook",
        "Canonical idea-to-MVP state write blocked by idea-to-MVP hook",
        "Sensitive file access blocked by idea-to-MVP hook",
        "Production deploy or migration command blocked by idea-to-MVP hook",
    ),
    ".claude/hooks/validate_idea_to_mvp_state.py": (
        "WATCH_PREFIXES",
        "ARTIFACT_PREFIXES",
        "PLACEHOLDER_PATTERN",
        "_workflow_state",
        "_active_nodes",
        "_missing_required_outputs",
        "_record_changed_paths",
        "_workflow_syntax_errors",
        "_python_syntax_errors",
        "_config_validation_errors",
        '"--paths", *relevant',
        "_mark_recoverable",
        'event_name in {"Stop", "SubagentStop", "StopFailure", "SessionEnd"}',
        'event_name == "PostToolUse" and tool_name == "Bash"',
        "developer decides",
        "citation needed",
        "Active idea-to-MVP handoffs are missing required outputs",
        '"interrupt"',
        '"validate"',
        '["node", "--check", str(path)]',
        '[sys.executable, "-m", "py_compile", str(path)]',
        "config validation failed",
        '".claude/control-plane/schemas/"',
        '".claude/control-plane/evals/"',
        "workflow syntax check failed",
        "python syntax check failed",
        "Invalid hook payload",
        "Authoritative idea-to-MVP artifacts still contain unresolved placeholders",
    ),
}

REQUIRED_AGENT_SNIPPETS = {
    "workflow-state-manager.md": (
        "idea_to_mvp_state.py bootstrap|persist|validate",
        "Persists and validates idea-to-MVP workflow state",
    ),
}

REQUIRED_IDEA_AGENT_BODY_SNIPPETS = (
    "## Responsibilities",
    "## Owned Outputs",
    "## Forbidden Actions",
    "## Constraints",
    "## Output",
)

WORKTREE_ISOLATED_AGENTS = {
    "backend-engineer.md",
    "frontend-engineer.md",
    "integration-engineer.md",
    "devops-engineer.md",
}

AGENT_REQUIRED_TOOLS = {
    "backend-engineer.md": {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"},
    "frontend-engineer.md": {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"},
    "integration-engineer.md": {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"},
    "devops-engineer.md": {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"},
}


def validate_rules(root: Path, errors: list[str]) -> None:
    rules_dir = root / ".claude/rules"
    for filename, required_snippets in REQUIRED_RULES.items():
        path = rules_dir / filename
        if not path.exists():
            errors.append(f"Missing required rule: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        frontmatter = simple_frontmatter(text)
        scoped_paths = frontmatter.get("paths")
        if not isinstance(scoped_paths, list) or not scoped_paths:
            errors.append(f"{path}: rules must declare non-empty paths frontmatter")
        elif not all(isinstance(item, str) and item for item in scoped_paths):
            errors.append(f"{path}: paths frontmatter entries must be non-empty strings")
        else:
            normalized_paths = [item.strip().strip('"').strip("'") for item in scoped_paths]
            positive_paths = [item for item in normalized_paths if not item.startswith("!")]
            negative_paths = [item for item in normalized_paths if item.startswith("!")]
            if not any(".claude/" in item for item in positive_paths):
                errors.append(f"{path}: paths frontmatter must stay scoped to .claude/ surfaces")
            if not negative_paths:
                errors.append(f"{path}: required rules must include at least one negative path boundary")
        if "# " not in text:
            errors.append(f"{path}: rule must include a markdown heading")
        lowered = text.lower()
        for snippet in required_snippets:
            if snippet.lower() not in lowered:
                errors.append(f"{path}: missing required rule anchor {snippet!r}")


def validate_workflow_files(root: Path, errors: list[str]) -> None:
    workflows_dir = root / ".claude/workflows"
    for js_name, md_name in REQUIRED_WORKFLOW_PAIRS:
        js_path = workflows_dir / js_name
        md_path = workflows_dir / md_name
        if not js_path.exists():
            errors.append(f"Missing required workflow runtime: {js_path}")
            continue
        if not md_path.exists():
            errors.append(f"Missing required workflow contract: {md_path}")
        else:
            md_text = md_path.read_text(encoding="utf-8")
            missing_sections = [
                snippet for snippet in REQUIRED_WORKFLOW_CONTRACT_SECTIONS if snippet not in md_text
            ]
            if missing_sections:
                errors.append(
                    f"{md_path}: workflow contract missing required sections {', '.join(missing_sections)}"
                )
        text = js_path.read_text(encoding="utf-8")
        if "export const meta" not in text:
            errors.append(f"{js_path}: workflow runtime must export a meta object")
        if 'name:' not in text and 'name"' not in text:
            errors.append(f"{js_path}: workflow meta must declare a name")
        if 'description:' not in text and 'description"' not in text:
            errors.append(f"{js_path}: workflow meta must declare a description")
        required_cursor_fields = PHASE_WORKFLOW_CURSOR_FIELDS.get(js_name)
        if required_cursor_fields is not None:
            missing_fields = [
                field_name for field_name, pattern in required_cursor_fields if pattern.search(text) is None
            ]
            if missing_fields:
                errors.append(
                    f"{js_path}: phase workflow must expose the standard resumable cursor fields; "
                    f"missing {', '.join(repr(field) for field in missing_fields)}"
                )
        required_snippets = REQUIRED_WORKFLOW_RUNTIME_SNIPPETS.get(js_name)
        if required_snippets is not None:
            for snippet in required_snippets:
                if snippet not in text:
                    errors.append(f"{js_path}: missing required workflow runtime snippet {snippet!r}")


def validate_scoped_workflow_files(root: Path, scoped_paths: list[str], errors: list[str]) -> None:
    workflows_dir = root / ".claude/workflows"
    workflow_pairs = {js_name: md_name for js_name, md_name in REQUIRED_WORKFLOW_PAIRS}
    contract_pairs = {md_name: js_name for js_name, md_name in REQUIRED_WORKFLOW_PAIRS}
    for relative in scoped_paths:
        name = Path(relative).name
        if name in workflow_pairs:
            js_path = workflows_dir / name
            if not js_path.exists():
                errors.append(f"Missing required workflow runtime: {js_path}")
                continue
            text = js_path.read_text(encoding="utf-8")
            if "export const meta" not in text:
                errors.append(f"{js_path}: workflow runtime must export a meta object")
            if 'name:' not in text and 'name"' not in text:
                errors.append(f"{js_path}: workflow meta must declare a name")
            if 'description:' not in text and 'description"' not in text:
                errors.append(f"{js_path}: workflow meta must declare a description")
            required_cursor_fields = PHASE_WORKFLOW_CURSOR_FIELDS.get(name)
            if required_cursor_fields is not None:
                missing_fields = [
                    field_name for field_name, pattern in required_cursor_fields if pattern.search(text) is None
                ]
                if missing_fields:
                    errors.append(
                        f"{js_path}: phase workflow must expose the standard resumable cursor fields; "
                        f"missing {', '.join(repr(field) for field in missing_fields)}"
                    )
            required_snippets = REQUIRED_WORKFLOW_RUNTIME_SNIPPETS.get(name)
            if required_snippets is not None:
                for snippet in required_snippets:
                    if snippet not in text:
                        errors.append(f"{js_path}: missing required workflow runtime snippet {snippet!r}")
            continue

        if name in contract_pairs:
            md_path = workflows_dir / name
            if not md_path.exists():
                errors.append(f"Missing required workflow contract: {md_path}")
                continue
            md_text = md_path.read_text(encoding="utf-8")
            if "# " not in md_text:
                errors.append(f"{md_path}: workflow contract must include a markdown heading")
            missing_sections = [
                snippet for snippet in REQUIRED_WORKFLOW_CONTRACT_SECTIONS if snippet not in md_text
            ]
            if missing_sections:
                errors.append(
                    f"{md_path}: workflow contract missing required sections {', '.join(missing_sections)}"
                )


def _validate_inventory_snapshot(root: Path, errors: list[str]) -> None:
    path = root / ".claude/control-plane/inventory.json"
    if not path.exists():
        errors.append(f"Missing inventory: {path}")
        return
    try:
        actual = load_json(path)
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return

    expected = build_inventory_document(root)
    if actual != expected:
        errors.append(f"{path}: stale inventory; run python .claude/control-plane/scripts/inventory.py")


def _validate_package_manifest(root: Path, errors: list[str]) -> None:
    path = root / "PACKAGE_MANIFEST.json"
    if not path.exists():
        errors.append(f"Missing package manifest: {path}")
        return
    try:
        manifest = load_json(path)
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return

    if not isinstance(manifest, dict):
        errors.append(f"{path}: manifest root must be an object")
        return

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        errors.append(f"{path}: files must be a non-empty array")
        return

    seen_paths: set[str] = set()
    actual_count = manifest.get("file_count")
    if actual_count != len(files):
        errors.append(f"{path}: file_count must match the number of tracked files")

    for index, entry in enumerate(files, start=1):
        if not isinstance(entry, dict):
            errors.append(f"{path}: file entry {index} must be an object")
            continue
        rel = entry.get("path")
        if not isinstance(rel, str) or not rel:
            errors.append(f"{path}: file entry {index} is missing a non-empty path")
            continue
        if rel in seen_paths:
            errors.append(f"{path}: duplicate tracked path {rel}")
            continue
        seen_paths.add(rel)

        target = root / rel
        if not target.is_file():
            errors.append(f"{path}: tracked file is missing: {rel}")
            continue

        fingerprint = stable_file_fingerprint(target)
        if entry.get("bytes") != fingerprint.size_bytes:
            errors.append(f"{path}: stale byte count for {rel}")
        if entry.get("sha256") != fingerprint.sha256:
            errors.append(f"{path}: stale sha256 for {rel}")


def validate_json_schema_files(root: Path, errors: list[str], warnings: list[str]) -> None:
    schemas = root / ".claude/control-plane/schemas"
    parsed = {}
    for path in schemas.glob("*.schema.json"):
        try:
            parsed[path.name] = load_json(path)
        except Exception as exc:
            errors.append(f"{path}: invalid JSON: {exc}")

    try:
        import jsonschema  # type: ignore
    except ImportError:
        warnings.append("jsonschema is not installed; schema meta-validation was skipped.")
        return

    for name, schema in parsed.items():
        try:
            jsonschema.Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"{name}: invalid JSON Schema: {exc}")

def _flatten_hook_commands(entries: Any) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        return []
    commands: list[dict[str, Any]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        matcher = entry.get("matcher")
        hooks = entry.get("hooks")
        if not isinstance(hooks, list):
            continue
        for hook in hooks:
            if not isinstance(hook, dict):
                continue
            commands.append(
                {
                    "matcher": matcher,
                    "type": hook.get("type"),
                    "command": hook.get("command"),
                    "args": hook.get("args"),
                }
            )
    return commands


def validate_settings_hooks(root: Path, errors: list[str]) -> None:
    path = root / ".claude/settings.json"
    if not path.exists():
        errors.append(f"Missing settings file: {path}")
        return
    try:
        settings = load_json(path)
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return
    if not isinstance(settings, dict):
        errors.append(f"{path}: settings root must be an object")
        return
    if settings.get("$schema") != "https://json.schemastore.org/claude-code-settings.json":
        errors.append(f"{path}: missing required Claude Code schema reference")
    worktree = settings.get("worktree")
    if not isinstance(worktree, dict):
        errors.append(f"{path}: worktree settings must be an object")
    elif worktree.get("baseRef") != "head":
        errors.append(f"{path}: worktree.baseRef must be 'head' for isolated idea-to-MVP parallel writers")
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        errors.append(f"{path}: hooks must be an object keyed by lifecycle event")
        return

    for event_name, required_entries in REQUIRED_HOOK_COMMANDS.items():
        commands = _flatten_hook_commands(hooks.get(event_name))
        if not commands:
            errors.append(f"{path}: missing required {event_name} hook registration")
            continue
        for required in required_entries:
            matched = False
            for command in commands:
                if command.get("type") != "command":
                    continue
                if required.get("matcher") is not None and command.get("matcher") != required["matcher"]:
                    continue
                if command.get("command") != required["command"]:
                    continue
                args = command.get("args")
                if not isinstance(args, list) or args != required["args"]:
                    continue
                matched = True
                break
            if not matched:
                description = f"{event_name} hook {required['command']} {' '.join(required['args'])}"
                if required.get("matcher"):
                    description += f" matcher={required['matcher']}"
                errors.append(f"{path}: missing required {description}")


def validate_hook_scripts(root: Path, errors: list[str]) -> None:
    for rel, required_snippets in REQUIRED_HOOK_SCRIPT_SNIPPETS.items():
        path = root / rel
        if not path.exists():
            errors.append(f"Missing required hook script: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in required_snippets:
            if snippet not in text:
                errors.append(f"{path}: missing required hook guardrail snippet {snippet!r}")


def validate_scoped_hook_scripts(root: Path, scoped_paths: list[str], errors: list[str]) -> None:
    scoped_set = {path.replace("\\", "/") for path in scoped_paths}
    for rel, required_snippets in REQUIRED_HOOK_SCRIPT_SNIPPETS.items():
        if rel not in scoped_set:
            continue
        path = root / rel
        if not path.exists():
            errors.append(f"Missing required hook script: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in required_snippets:
            if snippet not in text:
                errors.append(f"{path}: missing required hook guardrail snippet {snippet!r}")

def validate_agents(root: Path, errors: list[str]) -> None:
    agents_dir = root / ".claude/agents"
    seen_names: dict[str, str] = {}
    for filename, expected_name in {**REQUIRED_AGENTS, **REQUIRED_IDEA_AGENTS}.items():
        path = agents_dir / filename
        if not path.exists():
            errors.append(f"Missing required agent: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        fm = simple_frontmatter(text)
        if fm.get("name") != expected_name:
            errors.append(f"{path}: expected name {expected_name!r}, got {fm.get('name')!r}")
        if not fm.get("description"):
            errors.append(f"{path}: missing description")
        if filename in REQUIRED_IDEA_AGENTS:
            missing_sections = [snippet for snippet in REQUIRED_IDEA_AGENT_BODY_SNIPPETS if snippet not in text]
            if missing_sections:
                errors.append(f"{path}: missing required agent sections {', '.join(missing_sections)}")
        if fm.get("permissionMode") == "acceptEdits":
            errors.append(f"{path}: permissionMode acceptEdits is forbidden for control-plane agents")
        if filename in WORKTREE_ISOLATED_AGENTS and fm.get("isolation") != "worktree":
            errors.append(f"{path}: parallel-writing idea-to-MVP agents must declare isolation: worktree")
        tools = fm.get("tools", [])
        if filename in AGENT_REQUIRED_TOOLS:
            missing_tools = sorted(required for required in AGENT_REQUIRED_TOOLS[filename] if required not in tools)
            if missing_tools:
                errors.append(f"{path}: missing required tools {', '.join(missing_tools)}")
        if filename == "control-plane-verifier.md":
            for forbidden in ("Write", "Edit", "Bash", "Agent"):
                if forbidden in tools:
                    errors.append(f"{path}: verifier must not allow {forbidden}")
        required_snippets = REQUIRED_AGENT_SNIPPETS.get(filename)
        if required_snippets is not None:
            for snippet in required_snippets:
                if snippet not in text:
                    errors.append(f"{path}: missing required agent snippet {snippet!r}")
        name = str(fm.get("name", ""))
        if name:
            if name in seen_names:
                errors.append(f"Duplicate agent name {name}: {seen_names[name]} and {path}")
            seen_names[name] = str(path)


REQUIRED_SKILLS = {
    "brainstorm-product-opportunities": "brainstorm-product-opportunities",
    "validate-problem-hypotheses": "validate-problem-hypotheses",
    "research-market-and-competitors": "research-market-and-competitors",
    "define-target-users-and-jtbd": "define-target-users-and-jtbd",
    "form-value-proposition": "form-value-proposition",
    "select-core-problem": "select-core-problem",
    "ideate-features": "ideate-features",
    "prioritize-features": "prioritize-features",
    "design-user-flows": "design-user-flows",
    "design-information-architecture": "design-information-architecture",
    "produce-low-fidelity-wireframes": "produce-low-fidelity-wireframes",
    "create-high-fidelity-interface": "create-high-fidelity-interface",
    "define-design-system": "define-design-system",
    "build-interactive-prototype": "build-interactive-prototype",
    "conduct-usability-testing": "conduct-usability-testing",
    "prepare-design-handoff": "prepare-design-handoff",
    "define-mvp-scope-and-requirements": "define-mvp-scope-and-requirements",
    "define-solution-architecture": "define-solution-architecture",
    "bootstrap-project-and-tooling": "bootstrap-project-and-tooling",
    "implement-backend-capabilities": "implement-backend-capabilities",
    "implement-frontend-experience": "implement-frontend-experience",
    "integrate-product-components": "integrate-product-components",
    "review-code-and-architecture": "review-code-and-architecture",
    "prepare-minimal-implementation-record": "prepare-minimal-implementation-record",
    "create-test-plan": "create-test-plan",
    "execute-functional-testing": "execute-functional-testing",
    "conduct-uat-and-usability-validation": "conduct-uat-and-usability-validation",
    "diagnose-and-fix-defects": "diagnose-and-fix-defects",
    "validate-performance-and-security": "validate-performance-and-security",
    "prepare-test-record": "prepare-test-record",
    "prepare-release-record": "prepare-release-record",
    "deploy-mvp": "deploy-mvp",
    "configure-product-analytics": "configure-product-analytics",
    "release-mvp": "release-mvp",
    "monitor-and-synthesize-feedback": "monitor-and-synthesize-feedback",
    "plan-next-iteration": "plan-next-iteration",
    "manage-artifact-manifest": "manage-artifact-manifest",
    "record-decision": "record-decision",
    "assess-change-impact": "assess-change-impact",
    "validate-artifact-contract": "validate-artifact-contract",
    "verify-source-grounding": "verify-source-grounding",
    "create-traceability-matrix": "create-traceability-matrix",
    "prepare-specialist-handoff": "prepare-specialist-handoff",
    "run-phase-gate": "run-phase-gate",
    "maintain-risk-register": "maintain-risk-register",
}

SKILL_REQUIRED_ALLOWED_TOOLS = {
    "bootstrap-project-and-tooling": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"},
    "implement-backend-capabilities": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"},
    "implement-frontend-experience": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"},
    "integrate-product-components": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"},
    "deploy-mvp": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"},
}

REQUIRED_SKILL_BODY_SNIPPETS = (
    "when_to_use:",
    "allowed-tools:",
    "## Purpose",
    "## Entry Conditions",
    "## Required Inputs",
    "## Procedure",
    "## Permitted Tools",
    "## Required Evidence",
    "## Output Artifact Contract",
    "## Validation Checks",
    "## Failure Conditions",
    "## Handoff Destination",
    "## Explicit Non-Goals",
)


def validate_skills(root: Path, errors: list[str]) -> None:
    skills_dir = root / ".claude/skills"
    for folder, expected_name in REQUIRED_SKILLS.items():
        path = skills_dir / folder / "SKILL.md"
        if not path.exists():
            errors.append(f"Missing required skill: {path}")
            continue
        content = path.read_text(encoding="utf-8")
        fm = simple_frontmatter(content)
        if fm.get("name") != expected_name:
            errors.append(f"{path}: expected name {expected_name!r}, got {fm.get('name')!r}")
        if not fm.get("description"):
            errors.append(f"{path}: missing description")
        missing_snippets = [snippet for snippet in REQUIRED_SKILL_BODY_SNIPPETS if snippet not in content]
        if missing_snippets:
            errors.append(f"{path}: missing required skill sections {', '.join(missing_snippets)}")
        required_allowed_tools = SKILL_REQUIRED_ALLOWED_TOOLS.get(folder)
        if required_allowed_tools is not None:
            allowed_tools = fm.get("allowed-tools", "")
            if isinstance(allowed_tools, str):
                declared_tools = {tool for tool in allowed_tools.split() if tool}
            else:
                declared_tools = set()
            missing_tools = sorted(required_allowed_tools.difference(declared_tools))
            if missing_tools:
                errors.append(f"{path}: allowed-tools missing required entries {', '.join(missing_tools)}")


def validate_idea_state(root: Path, errors: list[str]) -> None:
    state_dir = root / ".claude/control-plane/state/idea-to-mvp"
    script = root / ".claude/control-plane/scripts/idea_to_mvp_state.py"
    if not state_dir.exists():
        errors.append(f"Missing idea-to-MVP state directory: {state_dir}")
        return
    if not script.exists():
        errors.append(f"Missing idea-to-MVP state script: {script}")
        return
    try:
        result = __import__("subprocess").run(
            ["python", str(script), "validate", "--state-dir", str(state_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        errors.append(f"idea_to_mvp_state.py validate failed to run: {exc}")
        return
    if result.returncode != 0:
        detail = (result.stdout or result.stderr).strip()
        errors.append(f"idea_to_mvp_state.py validate failed: {detail}")
    try:
        self_check = __import__("subprocess").run(
            ["python", str(script), "self-check"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        errors.append(f"idea_to_mvp_state.py self-check failed to run: {exc}")
        return
    if self_check.returncode != 0:
        detail = (self_check.stdout or self_check.stderr).strip()
        errors.append(f"idea_to_mvp_state.py self-check failed: {detail}")


def validate_hook_self_checks(root: Path, errors: list[str]) -> None:
    hooks = (
        ".claude/hooks/guard_idea_to_mvp_tool_use.py",
        ".claude/hooks/validate_idea_to_mvp_state.py",
        ".claude/control-plane/scripts/self_improvement_evidence.py",
        ".claude/control-plane/scripts/replay.py",
    )
    for rel in hooks:
        path = root / rel
        try:
            result = __import__("subprocess").run(
                ["python", str(path), "--self-check"],
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:
            errors.append(f"{path}: self-check failed to run: {exc}")
            continue
        if result.returncode != 0:
            detail = (result.stdout or result.stderr).strip()
            errors.append(f"{path}: self-check failed: {detail}")


def validate_behavioral_evals(root: Path, errors: list[str]) -> None:
    script = root / ".claude/control-plane/scripts/idea_to_mvp_behavioral_eval.py"
    try:
        result = __import__("subprocess").run(
            ["python", str(script), "--self-check"],
            capture_output=True,
            text=True,
            check=False,
        )
    except Exception as exc:
        errors.append(f"{script}: behavioral eval failed to run: {exc}")
        return
    if result.returncode != 0:
        detail = (result.stdout or result.stderr).strip()
        errors.append(f"{script}: behavioral eval failed: {detail}")

def validate_manifest(root: Path, errors: list[str], warnings: list[str]) -> dict:
    path = root / ".claude/control-plane/manifest.yaml"
    if not path.exists():
        errors.append(f"Missing manifest: {path}")
        return {}
    try:
        manifest = _load_manifest_yaml(path)
    except Exception as exc:
        errors.append(f"Invalid manifest YAML: {exc}")
        return {}

    _validate_manifest_contract(manifest, errors, warnings)
    return manifest

def validate_required_files(root: Path, errors: list[str]) -> None:
    required = [
        ".claude/control-plane/TRUST_MODEL.md",
        ".claude/control-plane/BOOTSTRAP.md",
        ".claude/control-plane/OPERATING_PROTOCOL.md",
        ".claude/control-plane/evals/routing-cases.yaml",
        ".claude/control-plane/evals/skills-cases.yaml",
        ".claude/control-plane/evals/rules-cases.yaml",
        ".claude/control-plane/evals/workflow-cases.yaml",
        ".claude/control-plane/schemas/baseline.schema.json",
        ".claude/control-plane/schemas/candidate-package.schema.json",
        ".claude/control-plane/schemas/change-plan.schema.json",
        ".claude/control-plane/schemas/hypothesis.schema.json",
        ".claude/control-plane/schemas/workflow-state.schema.json",
        ".claude/control-plane/schemas/artifact-manifest.schema.json",
        ".claude/control-plane/schemas/artifact-dependency-graph.schema.json",
        ".claude/control-plane/schemas/risk-register.schema.json",
        ".claude/control-plane/schemas/assumptions-register.schema.json",
        ".claude/control-plane/schemas/audit-report.schema.json",
        ".claude/control-plane/schemas/handoff.schema.json",
        ".claude/control-plane/schemas/gate-result.schema.json",
        ".claude/control-plane/schemas/decision-record.schema.json",
        ".claude/control-plane/schemas/verification-result.schema.json",
        ".claude/control-plane/schemas/run-event.schema.json",
        ".claude/control-plane/schemas/result.schema.json",
        ".claude/control-plane/schemas/replay-result.schema.json",
        ".claude/control-plane/scripts/idea_to_mvp_state.py",
        ".claude/control-plane/scripts/idea_to_mvp_behavioral_eval.py",
        ".claude/settings.json",
        ".claude/rules/workflow-governance.md",
        ".claude/rules/artifact-contracts.md",
        ".claude/rules/evidence-policy.md",
        ".claude/rules/decision-authority.md",
        ".claude/rules/design-quality.md",
        ".claude/rules/engineering-quality.md",
        ".claude/rules/testing-policy.md",
        ".claude/rules/security-policy.md",
        ".claude/rules/release-policy.md",
        ".claude/rules/repository-boundaries.md",
        ".claude/workflows/idea-to-mvp.js",
        ".claude/workflows/idea-to-mvp.md",
        ".claude/workflows/discover-phase.js",
        ".claude/workflows/discover-phase.md",
        ".claude/workflows/define-phase.js",
        ".claude/workflows/define-phase.md",
        ".claude/workflows/design-phase.js",
        ".claude/workflows/design-phase.md",
        ".claude/workflows/build-phase.js",
        ".claude/workflows/build-phase.md",
        ".claude/workflows/test-phase.js",
        ".claude/workflows/test-phase.md",
        ".claude/workflows/change-impact-loop.js",
        ".claude/workflows/change-impact-loop.md",
        ".claude/workflows/launch-phase.js",
        ".claude/workflows/launch-phase.md",
        ".claude/workflows/feedback-loop.js",
        ".claude/workflows/feedback-loop.md",
        ".claude/agents/mvp-orchestrator.md",
        ".claude/agents/product-strategist.md",
        ".claude/agents/market-researcher.md",
        ".claude/agents/product-manager.md",
        ".claude/agents/ux-designer.md",
        ".claude/agents/ui-designer.md",
        ".claude/agents/ux-researcher.md",
        ".claude/agents/solution-architect.md",
        ".claude/agents/backend-engineer.md",
        ".claude/agents/frontend-engineer.md",
        ".claude/agents/integration-engineer.md",
        ".claude/agents/technical-lead.md",
        ".claude/agents/security-engineer.md",
        ".claude/agents/qa-engineer.md",
        ".claude/agents/devops-engineer.md",
        ".claude/agents/data-analyst.md",
        ".claude/agents/workflow-state-manager.md",
        ".claude/hooks/validate_idea_to_mvp_state.py",
        ".claude/hooks/guard_idea_to_mvp_tool_use.py",
        ".claude/control-plane/state/idea-to-mvp/README.md",
        ".claude/control-plane/state/idea-to-mvp/workflow-state.json",
        ".claude/control-plane/state/idea-to-mvp/artifact-manifest.json",
        ".claude/control-plane/state/idea-to-mvp/artifact-dependency-graph.json",
        ".claude/control-plane/state/idea-to-mvp/risk-register.json",
        ".claude/control-plane/state/idea-to-mvp/assumptions-register.json",
        ".claude/control-plane/state/idea-to-mvp/gate-results.jsonl",
        ".claude/control-plane/state/idea-to-mvp/decision-records.jsonl",
        ".claude/skills/brainstorm-product-opportunities/SKILL.md",
        ".claude/skills/validate-problem-hypotheses/SKILL.md",
        ".claude/skills/research-market-and-competitors/SKILL.md",
        ".claude/skills/define-target-users-and-jtbd/SKILL.md",
        ".claude/skills/form-value-proposition/SKILL.md",
        ".claude/skills/select-core-problem/SKILL.md",
        ".claude/skills/ideate-features/SKILL.md",
        ".claude/skills/prioritize-features/SKILL.md",
        ".claude/skills/design-user-flows/SKILL.md",
        ".claude/skills/design-information-architecture/SKILL.md",
        ".claude/skills/produce-low-fidelity-wireframes/SKILL.md",
        ".claude/skills/create-high-fidelity-interface/SKILL.md",
        ".claude/skills/define-design-system/SKILL.md",
        ".claude/skills/build-interactive-prototype/SKILL.md",
        ".claude/skills/conduct-usability-testing/SKILL.md",
        ".claude/skills/prepare-design-handoff/SKILL.md",
        ".claude/skills/define-mvp-scope-and-requirements/SKILL.md",
        ".claude/skills/define-solution-architecture/SKILL.md",
        ".claude/skills/bootstrap-project-and-tooling/SKILL.md",
        ".claude/skills/implement-backend-capabilities/SKILL.md",
        ".claude/skills/implement-frontend-experience/SKILL.md",
        ".claude/skills/integrate-product-components/SKILL.md",
        ".claude/skills/review-code-and-architecture/SKILL.md",
        ".claude/skills/prepare-minimal-implementation-record/SKILL.md",
        ".claude/skills/create-test-plan/SKILL.md",
        ".claude/skills/execute-functional-testing/SKILL.md",
        ".claude/skills/conduct-uat-and-usability-validation/SKILL.md",
        ".claude/skills/diagnose-and-fix-defects/SKILL.md",
        ".claude/skills/validate-performance-and-security/SKILL.md",
        ".claude/skills/prepare-test-record/SKILL.md",
        ".claude/skills/prepare-release-record/SKILL.md",
        ".claude/skills/deploy-mvp/SKILL.md",
        ".claude/skills/configure-product-analytics/SKILL.md",
        ".claude/skills/release-mvp/SKILL.md",
        ".claude/skills/monitor-and-synthesize-feedback/SKILL.md",
        ".claude/skills/plan-next-iteration/SKILL.md",
        ".claude/skills/manage-artifact-manifest/SKILL.md",
        ".claude/skills/record-decision/SKILL.md",
        ".claude/skills/assess-change-impact/SKILL.md",
        ".claude/skills/validate-artifact-contract/SKILL.md",
        ".claude/skills/prepare-specialist-handoff/SKILL.md",
        ".claude/skills/run-phase-gate/SKILL.md",
        ".claude/skills/maintain-risk-register/SKILL.md",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")


def validate_self_checks(errors: list[str]) -> None:
    valid_manifest = """schema_version: 1
control_plane_roots:
  - .claude/
  - AGENTS.md
forbidden_roots:
  - .git/
  - secrets/
  - credentials/
owners:
  skills-specialist:
    - .claude/skills/**
  rules-specialist:
    - AGENTS.md
  workflow-specialist:
    - .claude/workflows/**
  control-plane-verifier:
    - .claude/control-plane/**
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
"""
    invalid_manifests = {
        "missing schema_version": valid_manifest.replace("schema_version: 1\n", ""),
        "missing control_plane_roots entry": valid_manifest.replace("  - AGENTS.md\n", "", 1),
        "missing forbidden_roots entry": valid_manifest.replace("  - credentials/\n", "", 1),
        "missing required owner": valid_manifest.replace(
            "  workflow-specialist:\n    - .claude/workflows/**\n", ""
        ),
        "empty required owner patterns": valid_manifest.replace(
            "  skills-specialist:\n    - .claude/skills/**\n", "  skills-specialist:\n"
        ),
        "enabled agent teams": valid_manifest.replace("    default: disabled\n", "    default: enabled\n"),
        "implicit agent teams": valid_manifest.replace(
            "    require_explicit_enablement: true\n", "    require_explicit_enablement: false\n"
        ),
        "unverified memory runs": valid_manifest.replace(
            "  accept_only_verified_runs: true\n", "  accept_only_verified_runs: false\n"
        ),
    }
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "manifest.yaml"
        path.write_text(valid_manifest, encoding="utf-8")
        parsed = _load_manifest_yaml(path, force_fallback=True)
        fallback_errors: list[str] = []
        fallback_warnings: list[str] = []
        _validate_manifest_contract(parsed, fallback_errors, fallback_warnings)
        if fallback_errors:
            errors.append(
                "validate.py self-check: fallback parser rejected valid manifest: "
                f"{fallback_errors}"
            )

        for name, invalid_manifest in invalid_manifests.items():
            path.write_text(invalid_manifest, encoding="utf-8")
            parsed = _load_manifest_yaml(path, force_fallback=True)
            fallback_errors = []
            fallback_warnings = []
            _validate_manifest_contract(parsed, fallback_errors, fallback_warnings)
            if not fallback_errors:
                errors.append(
                    "validate.py self-check: fallback parser silently passed invalid manifest: "
                    f"{name}"
                )

        evals_root = Path(tmp) / "repo" / ".claude" / "control-plane" / "evals"
        evals_root.mkdir(parents=True)
        valid_eval = """schema_version: 1
cases:
  - id: EVAL-VALID-001
    prompt: Route this control-plane request.
    expected_owner: workflow-specialist
    expected_abstention: false
  - id: EVAL-ABSTAIN-001
    prompt: Edit application code.
    expected_owner: null
    expected_abstention: true
"""
        invalid_evals = {
            "malformed YAML": """cases:
  - id: EVAL-BAD-001
    prompt: [unterminated
""",
            "empty eval file": "",
            "duplicate case IDs": valid_eval + """  - id: EVAL-VALID-001
    prompt: Duplicate.
    expected_owner: workflow-specialist
    expected_abstention: false
""",
        }
        for filename in REQUIRED_EVAL_FILES:
            (evals_root / filename).write_text(valid_eval, encoding="utf-8")
        eval_errors: list[str] = []
        eval_warnings: list[str] = []
        validate_eval_files(evals_root.parents[2], eval_errors, eval_warnings)
        if eval_errors:
            errors.append(f"validate.py self-check: eval validator rejected valid fixtures: {eval_errors}")

        for name, invalid_eval in invalid_evals.items():
            for filename in REQUIRED_EVAL_FILES:
                (evals_root / filename).write_text(valid_eval, encoding="utf-8")
            (evals_root / "routing-cases.yaml").write_text(invalid_eval, encoding="utf-8")
            eval_errors = []
            eval_warnings = []
            validate_eval_files(evals_root.parents[2], eval_errors, eval_warnings)
            if not eval_errors:
                errors.append(
                    "validate.py self-check: eval validator silently passed invalid fixture: "
                    f"{name}"
                )

        workflow_root = Path(tmp) / ".claude" / "workflows"
        workflow_root.mkdir(parents=True)
        valid_js = """export const meta = {
  name: "example-workflow",
  description: "Example workflow",
};
"""
        invalid_js = "export const notMeta = {};\n"
        valid_workflow_contract = """# Example Workflow Contract

## States and Legal Transitions

- pending -> complete

## Input Contract

- example inputs

## Output Contract

- example outputs

## Read Set

- workflow state

## Write Set

- artifact manifest

## Success Criteria

- contract is complete

## Failure Criteria

- block on missing evidence

## Budgets

- one writer

## Resume and Rollback

- resume from persisted state

## Observability

- record gate results

## Human Approval Points

- none
"""
        (workflow_root / "example.js").write_text(valid_js, encoding="utf-8")
        (workflow_root / "example.md").write_text(valid_workflow_contract, encoding="utf-8")
        pair_errors: list[str] = []
        original_pairs = REQUIRED_WORKFLOW_PAIRS
        try:
            globals()["REQUIRED_WORKFLOW_PAIRS"] = (("example.js", "example.md"),)
            validate_workflow_files(workflow_root.parents[1], pair_errors)
            if pair_errors:
                errors.append(f"validate.py self-check: workflow validator rejected valid runtime pair: {pair_errors}")

            (workflow_root / "example.js").write_text(invalid_js, encoding="utf-8")
            pair_errors = []
            validate_workflow_files(workflow_root.parents[1], pair_errors)
            if not pair_errors:
                errors.append("validate.py self-check: workflow validator silently passed invalid runtime metadata")
        finally:
            globals()["REQUIRED_WORKFLOW_PAIRS"] = original_pairs

        workflow_snippet_errors: list[str] = []
        original_pairs = REQUIRED_WORKFLOW_PAIRS
        original_runtime_snippets = REQUIRED_WORKFLOW_RUNTIME_SNIPPETS
        try:
            globals()["REQUIRED_WORKFLOW_PAIRS"] = (("example.js", "example.md"),)
            globals()["REQUIRED_WORKFLOW_RUNTIME_SNIPPETS"] = {
                "example.js": (
                    "idea_to_mvp_state.py persist --state-dir",
                    "Do not freehand-edit workflow-state.json",
                )
            }
            (workflow_root / "example.md").write_text(valid_workflow_contract, encoding="utf-8")
            (workflow_root / "example.js").write_text(
                valid_js
                + 'const instruction = "idea_to_mvp_state.py persist --state-dir";\n'
                + 'const guard = "Do not freehand-edit workflow-state.json";\n',
                encoding="utf-8",
            )
            validate_workflow_files(workflow_root.parents[1], workflow_snippet_errors)
            if workflow_snippet_errors:
                errors.append(
                    "validate.py self-check: workflow snippet validator rejected valid runtime: "
                    f"{workflow_snippet_errors}"
                )

            (workflow_root / "example.js").write_text(valid_js, encoding="utf-8")
            workflow_snippet_errors = []
            validate_workflow_files(workflow_root.parents[1], workflow_snippet_errors)
            if not workflow_snippet_errors:
                errors.append("validate.py self-check: workflow snippet validator silently passed invalid runtime")
        finally:
            globals()["REQUIRED_WORKFLOW_PAIRS"] = original_pairs
            globals()["REQUIRED_WORKFLOW_RUNTIME_SNIPPETS"] = original_runtime_snippets

        workflow_contract_errors: list[str] = []
        original_pairs = REQUIRED_WORKFLOW_PAIRS
        original_contract_sections = REQUIRED_WORKFLOW_CONTRACT_SECTIONS
        try:
            globals()["REQUIRED_WORKFLOW_PAIRS"] = (("example.js", "example.md"),)
            globals()["REQUIRED_WORKFLOW_CONTRACT_SECTIONS"] = (
                "## States and Legal Transitions",
                "## Human Approval Points",
            )
            (workflow_root / "example.js").write_text(valid_js, encoding="utf-8")
            (workflow_root / "example.md").write_text(
                "# Example Workflow Contract\n\n## States and Legal Transitions\n\n- pending -> complete\n\n## Human Approval Points\n\n- none\n",
                encoding="utf-8",
            )
            validate_workflow_files(workflow_root.parents[1], workflow_contract_errors)
            if workflow_contract_errors:
                errors.append(
                    "validate.py self-check: workflow contract validator rejected valid contract: "
                    f"{workflow_contract_errors}"
                )

            (workflow_root / "example.md").write_text(
                "# Example Workflow Contract\n\n## States and Legal Transitions\n\n- pending -> complete\n",
                encoding="utf-8",
            )
            workflow_contract_errors = []
            validate_workflow_files(workflow_root.parents[1], workflow_contract_errors)
            if not any("workflow contract missing required sections" in error for error in workflow_contract_errors):
                errors.append(
                    "validate.py self-check: workflow contract validator silently passed missing contract sections"
                )
        finally:
            globals()["REQUIRED_WORKFLOW_PAIRS"] = original_pairs
            globals()["REQUIRED_WORKFLOW_CONTRACT_SECTIONS"] = original_contract_sections

        rules_root = Path(tmp) / ".claude" / "rules"
        rules_root.mkdir(parents=True)
        valid_rule = """---
paths:
  - "**/.claude/workflows/example.*"
  - "!**/.claude/workflows/self-improvement.*"
---

# Example Rule

- Stop at explicit approval gates.
- Return structured status for blocked work.
"""
        invalid_rule = """---
paths:
  - "**/.claude/workflows/example.*"
---

# Example Rule

- Missing scoped frontmatter.
"""
        rule_errors: list[str] = []
        original_rules = REQUIRED_RULES
        try:
            globals()["REQUIRED_RULES"] = {"example.md": ("approval", "structured status")}
            (rules_root / "example.md").write_text(valid_rule, encoding="utf-8")
            validate_rules(rules_root.parents[1], rule_errors)
            if rule_errors:
                errors.append(f"validate.py self-check: rules validator rejected valid rule: {rule_errors}")

            (rules_root / "example.md").write_text(invalid_rule, encoding="utf-8")
            rule_errors = []
            validate_rules(rules_root.parents[1], rule_errors)
            if not rule_errors:
                errors.append("validate.py self-check: rules validator silently passed invalid rule")
        finally:
            globals()["REQUIRED_RULES"] = original_rules

        hooks_root = Path(tmp) / ".claude" / "hooks"
        hooks_root.mkdir(parents=True)
        valid_guard_hook = "\n".join(
            [
                "STATE_ROOT = None",
                "ARTIFACTS_ROOT = None",
                "EXEMPT_AGENT_TYPES = set()",
                "PRODUCTION_AGENT_TYPES = set()",
                "SENSITIVE_PATH_PATTERNS = ()",
                "PRODUCTION_COMMAND_PATTERNS = ()",
                "def _active_nodes(): pass",
                "def _artifact_portable_path(): pass",
                "def _project_relative_path(): pass",
                "def _active_handoff_paths(): pass",
                "def _has_active_write_permission(): pass",
                "def _delegated_path_violation(): pass",
                "def _code_write_violation(): pass",
                "def _state_write_violation(): pass",
                "def _denied_sensitive_path(): pass",
                "def _is_production_command(): pass",
                "def _launch_authorized(): pass",
                "def _production_command_authorized(): pass",
                'if tool_name in {"Edit", "Write"}: pass',
                'if tool_name == "Bash": pass',
                "Invalid PreToolUse payload",
                "Authoritative artifact write blocked by idea-to-MVP hook",
                "Read-only authoritative artifact blocked by idea-to-MVP hook",
                "Code changes blocked by idea-to-MVP hook",
                "Canonical idea-to-MVP state write blocked by idea-to-MVP hook",
                "Sensitive file access blocked by idea-to-MVP hook",
                "Production deploy or migration command blocked by idea-to-MVP hook",
            ]
        )
        valid_state_hook = "\n".join(
            [
                "WATCH_PREFIXES = ()",
                "ARTIFACT_PREFIXES = ()",
                "PLACEHOLDER_PATTERN = None",
                "def _workflow_state(): pass",
                "def _active_nodes(): pass",
                "def _missing_required_outputs(): pass",
                "def _record_changed_paths(): pass",
                "def _workflow_syntax_errors(): pass",
                "def _python_syntax_errors(): pass",
                "def _config_validation_errors(): pass",
                '"--paths", *relevant',
                "def _mark_recoverable(): pass",
                'if event_name in {"Stop", "SubagentStop", "StopFailure", "SessionEnd"}: pass',
                'if event_name == "PostToolUse" and tool_name == "Bash": pass',
                "developer decides",
                "citation needed",
                "Active idea-to-MVP handoffs are missing required outputs",
                '"interrupt"',
                '"validate"',
                '["node", "--check", str(path)]',
                '[sys.executable, "-m", "py_compile", str(path)]',
                "config validation failed",
                '".claude/control-plane/schemas/"',
                '".claude/control-plane/evals/"',
                "workflow syntax check failed",
                "python syntax check failed",
                "Invalid hook payload",
                "Authoritative idea-to-MVP artifacts still contain unresolved placeholders",
            ]
        )
        hook_errors: list[str] = []
        original_hook_snippets = REQUIRED_HOOK_SCRIPT_SNIPPETS
        try:
            globals()["REQUIRED_HOOK_SCRIPT_SNIPPETS"] = {
                ".claude/hooks/guard_idea_to_mvp_tool_use.py": original_hook_snippets[
                    ".claude/hooks/guard_idea_to_mvp_tool_use.py"
                ],
                ".claude/hooks/validate_idea_to_mvp_state.py": original_hook_snippets[
                    ".claude/hooks/validate_idea_to_mvp_state.py"
                ],
            }
            (hooks_root / "guard_idea_to_mvp_tool_use.py").write_text(valid_guard_hook, encoding="utf-8")
            (hooks_root / "validate_idea_to_mvp_state.py").write_text(valid_state_hook, encoding="utf-8")
            validate_hook_scripts(hooks_root.parents[1], hook_errors)
            if hook_errors:
                errors.append(f"validate.py self-check: hook script validator rejected valid hooks: {hook_errors}")

            (hooks_root / "guard_idea_to_mvp_tool_use.py").write_text(
                "def _launch_authorized():\n    return True\n",
                encoding="utf-8",
            )
            hook_errors = []
            validate_hook_scripts(hooks_root.parents[1], hook_errors)
            if not hook_errors:
                errors.append("validate.py self-check: hook script validator silently passed invalid hook drift")
        finally:
            globals()["REQUIRED_HOOK_SCRIPT_SNIPPETS"] = original_hook_snippets

        agents_root = Path(tmp) / ".claude" / "agents"
        agents_root.mkdir(parents=True, exist_ok=True)
        agent_errors: list[str] = []
        original_required_agents = REQUIRED_AGENTS
        original_required_idea_agents = REQUIRED_IDEA_AGENTS
        original_agent_snippets = REQUIRED_AGENT_SNIPPETS
        try:
            globals()["REQUIRED_AGENTS"] = {}
            globals()["REQUIRED_IDEA_AGENTS"] = {"workflow-state-manager.md": "workflow-state-manager"}
            globals()["REQUIRED_AGENT_SNIPPETS"] = {
                "workflow-state-manager.md": (
                    "idea_to_mvp_state.py bootstrap|persist|validate",
                    "Persists and validates idea-to-MVP workflow state",
                )
            }
            (agents_root / "workflow-state-manager.md").write_text(
                "---\nname: workflow-state-manager\ndescription: Persists and validates idea-to-MVP workflow state\ntools:\n  - Read\n---\n\n## Responsibilities\n\n1. Persist state.\n\n## Owned Outputs\n\n- Canonical state.\n\n## Forbidden Actions\n\n- Do not invent approvals.\n\n## Constraints\n\n- Use `python .claude/control-plane/scripts/idea_to_mvp_state.py bootstrap|persist|validate` as the canonical state-management path.\n\n## Output\n\nReturn persisted-state results.\n",
                encoding="utf-8",
            )
            validate_agents(agents_root.parents[1], agent_errors)
            if agent_errors:
                errors.append(f"validate.py self-check: agent snippet validator rejected valid agent: {agent_errors}")

            (agents_root / "workflow-state-manager.md").write_text(
                "---\nname: workflow-state-manager\ndescription: wrong\ntools:\n  - Read\n---\n",
                encoding="utf-8",
            )
            agent_errors = []
            validate_agents(agents_root.parents[1], agent_errors)
            if not agent_errors:
                errors.append("validate.py self-check: agent snippet validator silently passed invalid agent drift")

            (agents_root / "workflow-state-manager.md").write_text(
                "---\nname: workflow-state-manager\ndescription: Persists and validates idea-to-MVP workflow state\ntools:\n  - Read\n---\n",
                encoding="utf-8",
            )
            agent_errors = []
            validate_agents(agents_root.parents[1], agent_errors)
            if not any("missing required agent sections" in error for error in agent_errors):
                errors.append("validate.py self-check: agent validator silently passed missing agent execution sections")
        finally:
            globals()["REQUIRED_AGENTS"] = original_required_agents
            globals()["REQUIRED_IDEA_AGENTS"] = original_required_idea_agents
            globals()["REQUIRED_AGENT_SNIPPETS"] = original_agent_snippets

        isolated_agents_root = Path(tmp) / "isolated-agents" / ".claude" / "agents"
        isolated_agents_root.mkdir(parents=True, exist_ok=True)
        isolation_errors: list[str] = []
        original_required_agents = REQUIRED_AGENTS
        original_required_idea_agents = REQUIRED_IDEA_AGENTS
        original_worktree_isolated_agents = WORKTREE_ISOLATED_AGENTS
        original_agent_required_tools = AGENT_REQUIRED_TOOLS
        try:
            globals()["REQUIRED_AGENTS"] = {}
            globals()["REQUIRED_IDEA_AGENTS"] = {"backend-engineer.md": "backend-engineer"}
            globals()["WORKTREE_ISOLATED_AGENTS"] = {"backend-engineer.md"}
            globals()["AGENT_REQUIRED_TOOLS"] = {
                "backend-engineer.md": {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"}
            }
            (isolated_agents_root / "backend-engineer.md").write_text(
                "---\nname: backend-engineer\ndescription: Backend writer\ntools:\n  - Read\n  - Write\n  - Edit\n  - Bash\n  - Glob\n  - Grep\n  - Skill\nmodel: sonnet\nisolation: worktree\n---\n\n## Responsibilities\n\n1. Implement the bounded backend slice.\n\n## Owned Outputs\n\n- Backend implementation evidence.\n\n## Forbidden Actions\n\n- Do not expand scope.\n\n## Constraints\n\n- Stay within the approved MVP slice.\n\n## Output\n\nReturn backend implementation results.\n",
                encoding="utf-8",
            )
            validate_agents(isolated_agents_root.parents[1], isolation_errors)
            if isolation_errors:
                errors.append(
                    "validate.py self-check: agent validator rejected a valid worktree-isolated writer: "
                    f"{isolation_errors}"
                )

            (isolated_agents_root / "backend-engineer.md").write_text(
                "---\nname: backend-engineer\ndescription: Backend writer\ntools:\n  - Read\n  - Glob\n  - Grep\n  - Skill\nmodel: sonnet\nisolation: worktree\n---\n\n## Responsibilities\n\n1. Implement the bounded backend slice.\n\n## Owned Outputs\n\n- Backend implementation evidence.\n\n## Forbidden Actions\n\n- Do not expand scope.\n\n## Constraints\n\n- Stay within the approved MVP slice.\n\n## Output\n\nReturn backend implementation results.\n",
                encoding="utf-8",
            )
            isolation_errors = []
            validate_agents(isolated_agents_root.parents[1], isolation_errors)
            if not any("missing required tools" in error for error in isolation_errors):
                errors.append(
                    "validate.py self-check: agent validator silently passed missing writer tools"
                )
        finally:
            globals()["REQUIRED_AGENTS"] = original_required_agents
            globals()["REQUIRED_IDEA_AGENTS"] = original_required_idea_agents
            globals()["WORKTREE_ISOLATED_AGENTS"] = original_worktree_isolated_agents
            globals()["AGENT_REQUIRED_TOOLS"] = original_agent_required_tools

        isolated_skills_root = Path(tmp) / "isolated-skills" / ".claude" / "skills"
        isolated_skills_root.mkdir(parents=True, exist_ok=True)
        skill_errors: list[str] = []
        original_required_skills = REQUIRED_SKILLS
        original_skill_required_allowed_tools = SKILL_REQUIRED_ALLOWED_TOOLS
        try:
            globals()["REQUIRED_SKILLS"] = {"implement-backend-capabilities": "implement-backend-capabilities"}
            globals()["SKILL_REQUIRED_ALLOWED_TOOLS"] = {
                "implement-backend-capabilities": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"}
            }
            skill_dir = isolated_skills_root / "implement-backend-capabilities"
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: implement-backend-capabilities\n"
                "description: Backend implementation skill\n"
                "allowed-tools: Read Write Edit Bash Grep Glob\n"
                "when_to_use: Use for bounded backend implementation.\n"
                "---\n"
                "\n"
                "## Purpose\n"
                "\n"
                "Produce bounded backend implementation evidence.\n"
                "\n"
                "## Entry Conditions\n"
                "\n"
                "- The bounded backend slice is approved.\n"
                "\n"
                "## Required Inputs\n"
                "\n"
                "- Active handoff and validation command.\n"
                "\n"
                "## Procedure\n"
                "\n"
                "1. Implement the bounded backend slice.\n"
                "\n"
                "## Permitted Tools\n"
                "\n"
                "- `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`\n"
                "\n"
                "## Required Evidence\n"
                "\n"
                "- Backend validation results.\n"
                "\n"
                "## Output Artifact Contract\n"
                "\n"
                "Return:\n"
                "\n"
                "- `backend_implementation`\n"
                "\n"
                "## Validation Checks\n"
                "\n"
                "- Output matches the bounded backend slice.\n"
                "\n"
                "## Failure Conditions\n"
                "\n"
                "- Required inputs are missing.\n"
                "\n"
                "## Handoff Destination\n"
                "\n"
                "- Return results to the invoking workflow node.\n"
                "\n"
                "## Explicit Non-Goals\n"
                "\n"
                "- Do not expand scope.\n",
                encoding="utf-8",
            )
            validate_skills(isolated_skills_root.parents[1], skill_errors)
            if skill_errors:
                errors.append(
                    "validate.py self-check: skill validator rejected valid delegated writer tools: "
                    f"{skill_errors}"
                )

            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: implement-backend-capabilities\n"
                "description: Backend implementation skill\n"
                "allowed-tools: Read Grep Glob\n"
                "when_to_use: Use for bounded backend implementation.\n"
                "---\n"
                "\n"
                "## Purpose\n"
                "\n"
                "Produce bounded backend implementation evidence.\n"
                "\n"
                "## Entry Conditions\n"
                "\n"
                "- The bounded backend slice is approved.\n"
                "\n"
                "## Required Inputs\n"
                "\n"
                "- Active handoff and validation command.\n"
                "\n"
                "## Procedure\n"
                "\n"
                "1. Implement the bounded backend slice.\n"
                "\n"
                "## Permitted Tools\n"
                "\n"
                "- `Read`, `Grep`, `Glob`\n"
                "\n"
                "## Required Evidence\n"
                "\n"
                "- Backend validation results.\n"
                "\n"
                "## Output Artifact Contract\n"
                "\n"
                "Return:\n"
                "\n"
                "- `backend_implementation`\n"
                "\n"
                "## Validation Checks\n"
                "\n"
                "- Output matches the bounded backend slice.\n"
                "\n"
                "## Failure Conditions\n"
                "\n"
                "- Required inputs are missing.\n"
                "\n"
                "## Handoff Destination\n"
                "\n"
                "- Return results to the invoking workflow node.\n"
                "\n"
                "## Explicit Non-Goals\n"
                "\n"
                "- Do not expand scope.\n",
                encoding="utf-8",
            )
            skill_errors = []
            validate_skills(isolated_skills_root.parents[1], skill_errors)
            if not any("allowed-tools missing required entries" in error for error in skill_errors):
                errors.append(
                    "validate.py self-check: skill validator silently passed missing delegated writer tools"
                )
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: implement-backend-capabilities\n"
                "description: Backend implementation skill\n"
                "allowed-tools: Read Write Edit Bash Grep Glob\n"
                "---\n",
                encoding="utf-8",
            )
            skill_errors = []
            validate_skills(isolated_skills_root.parents[1], skill_errors)
            if not any("missing required skill sections" in error for error in skill_errors):
                errors.append(
                    "validate.py self-check: skill validator silently passed missing execution sections"
                )
        finally:
            globals()["REQUIRED_SKILLS"] = original_required_skills
            globals()["SKILL_REQUIRED_ALLOWED_TOOLS"] = original_skill_required_allowed_tools

        scoped_root = Path(tmp) / "scoped-repo"
        (scoped_root / ".claude").mkdir(parents=True, exist_ok=True)
        (scoped_root / ".claude" / "settings.json").write_text(
            json.dumps(
                {
                    "$schema": "https://json.schemastore.org/claude-code-settings.json",
                    "worktree": {
                        "baseRef": "head",
                    },
                    "hooks": {},
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        scoped_errors: list[str] = []
        scoped_warnings: list[str] = []
        validate_scoped_paths(scoped_root, [".claude/settings.json"], scoped_errors, scoped_warnings)
        if not scoped_errors:
            errors.append("validate.py self-check: scoped settings validation silently passed invalid hooks")

        (scoped_root / ".claude" / "settings.json").write_text(
            json.dumps(
                {
                    "$schema": "https://json.schemastore.org/claude-code-settings.json",
                    "worktree": {
                        "baseRef": "fresh",
                    },
                    "hooks": {
                        "PreToolUse": [],
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        scoped_errors = []
        scoped_warnings = []
        validate_scoped_paths(scoped_root, [".claude/settings.json"], scoped_errors, scoped_warnings)
        if not any("worktree.baseRef must be 'head'" in error for error in scoped_errors):
            errors.append("validate.py self-check: scoped settings validation silently passed invalid worktree.baseRef")

        scoped_agent_root = Path(tmp) / "scoped-agent-repo" / ".claude" / "agents"
        scoped_agent_root.mkdir(parents=True, exist_ok=True)
        scoped_agent_errors: list[str] = []
        scoped_agent_warnings: list[str] = []
        original_required_agents = REQUIRED_AGENTS
        original_required_idea_agents = REQUIRED_IDEA_AGENTS
        try:
            globals()["REQUIRED_AGENTS"] = {}
            globals()["REQUIRED_IDEA_AGENTS"] = {"backend-engineer.md": "backend-engineer"}
            (scoped_agent_root / "backend-engineer.md").write_text(
                "---\nname: wrong-name\ndescription: Broken scoped agent\n---\n",
                encoding="utf-8",
            )
            validate_scoped_paths(
                scoped_agent_root.parents[1],
                [".claude/agents/backend-engineer.md"],
                scoped_agent_errors,
                scoped_agent_warnings,
            )
            if not any("expected name 'backend-engineer'" in error for error in scoped_agent_errors):
                errors.append("validate.py self-check: scoped agent validation silently passed invalid agent")
        finally:
            globals()["REQUIRED_AGENTS"] = original_required_agents
            globals()["REQUIRED_IDEA_AGENTS"] = original_required_idea_agents

        scoped_skill_root = Path(tmp) / "scoped-skill-repo" / ".claude" / "skills" / "implement-backend-capabilities"
        scoped_skill_root.mkdir(parents=True, exist_ok=True)
        scoped_skill_errors: list[str] = []
        scoped_skill_warnings: list[str] = []
        original_required_skills = REQUIRED_SKILLS
        original_skill_required_allowed_tools = SKILL_REQUIRED_ALLOWED_TOOLS
        try:
            globals()["REQUIRED_SKILLS"] = {"implement-backend-capabilities": "implement-backend-capabilities"}
            globals()["SKILL_REQUIRED_ALLOWED_TOOLS"] = {
                "implement-backend-capabilities": {"Read", "Write", "Edit", "Bash", "Glob", "Grep"}
            }
            (scoped_skill_root / "SKILL.md").write_text(
                "---\n"
                "name: implement-backend-capabilities\n"
                "description: Broken scoped skill\n"
                "allowed-tools: Read Grep Glob\n"
                "when_to_use: Use for bounded backend implementation.\n"
                "---\n"
                "\n"
                "## Purpose\n"
                "\n"
                "Produce bounded backend implementation evidence.\n"
                "\n"
                "## Entry Conditions\n"
                "\n"
                "- The bounded backend slice is approved.\n"
                "\n"
                "## Required Inputs\n"
                "\n"
                "- Active handoff and validation command.\n"
                "\n"
                "## Procedure\n"
                "\n"
                "1. Implement the bounded backend slice.\n"
                "\n"
                "## Permitted Tools\n"
                "\n"
                "- `Read`, `Grep`, `Glob`\n"
                "\n"
                "## Required Evidence\n"
                "\n"
                "- Backend validation results.\n"
                "\n"
                "## Output Artifact Contract\n"
                "\n"
                "Return:\n"
                "\n"
                "- `backend_implementation`\n"
                "\n"
                "## Validation Checks\n"
                "\n"
                "- Output matches the bounded backend slice.\n"
                "\n"
                "## Failure Conditions\n"
                "\n"
                "- Required inputs are missing.\n"
                "\n"
                "## Handoff Destination\n"
                "\n"
                "- Return results to the invoking workflow node.\n"
                "\n"
                "## Explicit Non-Goals\n"
                "\n"
                "- Do not expand scope.\n",
                encoding="utf-8",
            )
            validate_scoped_paths(
                scoped_skill_root.parents[2],
                [".claude/skills/implement-backend-capabilities/SKILL.md"],
                scoped_skill_errors,
                scoped_skill_warnings,
            )
            if not any("allowed-tools missing required entries" in error for error in scoped_skill_errors):
                errors.append("validate.py self-check: scoped skill validation silently passed invalid allowed-tools")
        finally:
            globals()["REQUIRED_SKILLS"] = original_required_skills
            globals()["SKILL_REQUIRED_ALLOWED_TOOLS"] = original_skill_required_allowed_tools

        lf_file = Path(tmp) / "lf.txt"
        crlf_file = Path(tmp) / "crlf.txt"
        lf_file.write_text("alpha\nbeta\n", encoding="utf-8", newline="\n")
        crlf_file.write_text("alpha\nbeta\n", encoding="utf-8", newline="\r\n")
        if stable_file_fingerprint(lf_file) != stable_file_fingerprint(crlf_file):
            errors.append("validate.py self-check: stable fingerprint changed across LF/CRLF text")

        repo = Path(tmp) / "inventory-repo"
        (repo / ".git").mkdir(parents=True)
        (repo / ".claude" / "control-plane").mkdir(parents=True)
        (repo / "CLAUDE.md").write_text("root\n", encoding="utf-8")
        inventory_path = repo / ".claude" / "control-plane" / "inventory.json"
        inventory_path.write_text(json.dumps({"schema_version": 1, "files": []}), encoding="utf-8")
        inventory_errors: list[str] = []
        _validate_inventory_snapshot(repo, inventory_errors)
        if not inventory_errors:
            errors.append("validate.py self-check: stale inventory snapshot did not fail")


def validate_repo_hygiene(root: Path, errors: list[str]) -> None:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        errors.append(f"Missing gitignore file: {gitignore}")
        return
    lines = [line.strip() for line in gitignore.read_text(encoding="utf-8").splitlines()]
    if ".claude/worktrees/" not in lines:
        errors.append(f"{gitignore}: must ignore .claude/worktrees/ for Claude Code worktree isolation")

def validate_scoped_paths(
    root: Path,
    scoped_paths: list[str],
    errors: list[str],
    warnings: list[str],
) -> None:
    normalized = [path.replace("\\", "/") for path in scoped_paths]
    if any(path.startswith(".claude/agents/") for path in normalized):
        validate_agents(root, errors)
    if any(path.startswith(".claude/skills/") for path in normalized):
        validate_skills(root, errors)
    if any(path.startswith(".claude/rules/") for path in normalized):
        validate_rules(root, errors)
    if any(path.startswith(".claude/workflows/") for path in normalized):
        validate_scoped_workflow_files(
            root,
            [path for path in normalized if path.startswith(".claude/workflows/")],
            errors,
        )
    if any(path.startswith(".claude/hooks/") for path in normalized):
        validate_scoped_hook_scripts(root, [path for path in normalized if path.startswith(".claude/hooks/")], errors)
    if any(path == ".claude/settings.json" for path in normalized):
        validate_settings_hooks(root, errors)
    if any(path == ".claude/control-plane/manifest.yaml" for path in normalized):
        validate_manifest(root, errors, warnings)
    if any(path.startswith(".claude/control-plane/schemas/") for path in normalized):
        validate_json_schema_files(root, errors, warnings)
    if any(path.startswith(".claude/control-plane/evals/") for path in normalized):
        validate_eval_files(root, errors, warnings)
    if any(path.startswith(".claude/control-plane/state/idea-to-mvp/") for path in normalized):
        validate_idea_state(root, errors)
    if any(path == ".claude/control-plane/inventory.json" for path in normalized):
        _validate_inventory_snapshot(root, errors)
    if any(path == "PACKAGE_MANIFEST.json" for path in normalized):
        _validate_package_manifest(root, errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", nargs="+", help="Limit validation to the provided repo-relative paths.")
    args = parser.parse_args(argv)
    root = find_repo_root()
    errors: list[str] = []
    warnings: list[str] = []

    if args.paths:
        validate_scoped_paths(root, args.paths, errors, warnings)
    else:
        validate_required_files(root, errors)
        validate_agents(root, errors)
        validate_skills(root, errors)
        validate_manifest(root, errors, warnings)
        _validate_package_manifest(root, errors)
        _validate_inventory_snapshot(root, errors)
        validate_rules(root, errors)
        validate_workflow_files(root, errors)
        validate_settings_hooks(root, errors)
        validate_hook_scripts(root, errors)
        validate_idea_state(root, errors)
        validate_hook_self_checks(root, errors)
        validate_behavioral_evals(root, errors)
        validate_json_schema_files(root, errors, warnings)
        validate_eval_files(root, errors, warnings)
        validate_repo_hygiene(root, errors)
        validate_self_checks(errors)

    print("Claude Code control-plane validation")
    print(f"Repository: {root}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
