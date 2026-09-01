#!/usr/bin/env python3
"""Static/mechanical validation for the repository Codex control plane."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
errors: list[str] = []
warnings: list[str] = []

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--pre-snapshot",
    action="store_true",
    help=(
        "validate the edited definition before regenerating release identity; "
        "the generated snapshot is build-checked but not required to match yet"
    ),
)
ARGS = parser.parse_args()


def err(x: str) -> None:
    errors.append(x)


def warn(x: str) -> None:
    warnings.append(x)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SENSITIVE = re.compile(r"(?i)(api[_-]?key|authorization|credential|password|secret|token|private[_-]?key|cookie)")
TELEMETRY_FIELDS = {
    "schema_version", "timestamp", "run_id", "sequence", "parent_event_hash", "event_hash",
    "skill", "skill_revision", "event", "outcome", "reason_code", "execution_snapshot_id", "uow_id",
    "duration_ms", "count", "matched", "failed", "skipped", "evidence_refs", "surface", "lens",
    "severity", "reviewer", "domain", "lane", "status", "authorized", "coverage", "confirmed",
    "refuted", "retries",
}

required = [
    "AGENTS.md",
    ".codex/config.toml",
    ".codex/control-plane/manifest.json",
    ".codex/control-plane/enforcement-contract.json",
    ".codex/control-plane/audit-event.schema.json",
    ".codex/control-plane/definition-snapshot.json",
    ".codex/control-plane/DEFINITION_HASHES.sha256",
    ".codex/scripts/resolve_policies.py",
    ".codex/scripts/build_definition_snapshot.py",
    ".codex/scripts/compile_effective_state.py",
    ".codex/scripts/verify_enforcement_contract.py",
    ".codex/scripts/capture_uow.py",
    ".codex/scripts/execution_audit.py",
    ".codex/scripts/initialize_runtime_state.py",
    ".codex/scripts/build_release_archive.py",
    ".codex/scripts/skill_telemetry.py",
]
for p in required:
    if not (ROOT / p).is_file():
        err(f"missing required file: {p}")
legacy_hash = ".codex/control-plane/" + "FILE_HASHES.sha256"
if (ROOT / legacy_hash).exists():
    err("legacy hash manifest must not be used; mutable runtime state must stay outside release identity")

# Config and custom-agent contracts.
try:
    tomllib.loads((ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
except Exception as exc:
    err(f"config TOML invalid: {exc}")

agent_names: set[str] = set()
agent_data: dict[str, dict] = {}
for p in sorted((ROOT / ".codex/agents").glob("*.toml")):
    try:
        d = tomllib.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        err(f"{p.relative_to(ROOT)} invalid TOML: {exc}")
        continue
    for k in ("name", "description", "developer_instructions"):
        if not d.get(k):
            err(f"{p.relative_to(ROOT)} missing {k}")
    n = d.get("name")
    if n in agent_names:
        err(f"duplicate agent name: {n}")
    agent_names.add(n)
    agent_data[n] = d
    if "model" in d:
        warn(f"{p.relative_to(ROOT)} pins a model; portability may be reduced")

for role in ("phase-router", "architecture-boundary-verifier", "security-finding-reviewer", "control-plane-verifier"):
    d = agent_data.get(role)
    if not d:
        err(f"required read-only role missing: {role}")
    elif d.get("sandbox_mode") != "read-only":
        err(f"{role} must declare sandbox_mode = read-only")
if "phase-integrator" in agent_names:
    err("legacy phase-integrator role remains; orchestration ownership must stay with the primary")
if "security-adversarial-reviewer" in agent_names:
    err("legacy combined security reviewer/test-author role remains")

phase_router = agent_data.get("phase-router", {}).get("developer_instructions", "")
if "sole supervisor" not in phase_router.lower() or "do not spawn" not in phase_router.lower():
    err("phase-router must explicitly preserve primary supervisor ownership and prohibit spawning")

# Skill discovery/routing and telemetry contracts.
skill_names: set[str] = set()
for d in sorted((ROOT / ".agents/skills").iterdir()):
    if not d.is_dir():
        continue
    p = d / "SKILL.md"
    if not p.is_file():
        err(f"{d.relative_to(ROOT)} missing SKILL.md")
        continue
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---\n"):
        err(f"{p.relative_to(ROOT)} missing frontmatter")
        continue
    fm = t.split("---", 2)[1]
    nm = re.search(r"^name:\s*(.+)$", fm, re.M)
    ds = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not nm or not ds:
        err(f"{p.relative_to(ROOT)} needs name and description")
        continue
    name = nm.group(1).strip().strip("\"'")
    if name in skill_names:
        err(f"duplicate skill name: {name}")
    skill_names.add(name)
    if len(ds.group(1).strip()) < 50:
        warn(f"{p.relative_to(ROOT)} routing description is unusually short")
    if not re.search(r"(?im)^##? .*completion|completion", t):
        err(f"{p.relative_to(ROOT)} does not declare observable completion")
    if not re.search(r"(?im)failure|blocked|indeterminate", t):
        err(f"{p.relative_to(ROOT)} does not declare a failure branch")
    if "Never generate a new run ID for each event" not in t:
        err(f"{p.relative_to(ROOT)} does not require invocation-scoped telemetry run_id reuse")

    telemetry = d / "telemetry"
    schema = telemetry / "schema.json"
    ignore = telemetry / ".gitignore"
    if not schema.is_file():
        err(f"{telemetry.relative_to(ROOT)} missing schema.json")
    if not ignore.is_file() or "events.jsonl" not in ignore.read_text(encoding="utf-8"):
        err(f"{telemetry.relative_to(ROOT)} must ignore events.jsonl")
    if schema.is_file():
        try:
            sd = json.loads(schema.read_text(encoding="utf-8"))
            props = sd.get("properties", {})
            if props.get("skill", {}).get("const") != name:
                err(f"{schema.relative_to(ROOT)} skill does not match {name}")
            if props.get("schema_version", {}).get("const") != 2:
                err(f"{schema.relative_to(ROOT)} must use telemetry schema_version 2")
            events = props.get("event", {}).get("enum", [])
            if "invocation_started" not in events or "invocation_finished" not in events:
                err(f"{schema.relative_to(ROOT)} lacks invocation lifecycle events")
            required_fields = set(sd.get("required", []))
            for field in ("run_id", "sequence", "parent_event_hash", "event_hash"):
                if field not in required_fields:
                    err(f"{schema.relative_to(ROOT)} must require {field}")
            if set(props) - TELEMETRY_FIELDS:
                err(f"{schema.relative_to(ROOT)} contains undeclared telemetry fields: {sorted(set(props)-TELEMETRY_FIELDS)}")
            if any(SENSITIVE.search(k) for k in props):
                err(f"{schema.relative_to(ROOT)} contains sensitive field name")
        except Exception as exc:
            err(f"{schema.relative_to(ROOT)} invalid JSON: {exc}")

# Manifest and lifecycle classification.
try:
    m = json.loads((ROOT / ".codex/control-plane/manifest.json").read_text(encoding="utf-8"))
    if m.get("schema_version") != 2 or m.get("version") != "1.1.1":
        err("manifest must identify control plane schema 2 / version 1.1.1")
    for n in m.get("orchestration_skills", []):
        if n not in skill_names:
            err(f"manifest orchestration skill missing: {n}")
    if m.get("orchestration_owner") != "primary-agent-or-orchestration-skill":
        err("manifest must declare one primary orchestration owner")
    mutable = set(m.get("artifact_classes", {}).get("mutable_runtime_state", []))
    for required_mutable in (".codex/memory/**", ".agents/skills/**/telemetry/events.jsonl", ".control-plane-state/**"):
        if required_mutable not in mutable:
            err(f"manifest does not classify mutable runtime state: {required_mutable}")
    seed = m.get("runtime_state_seed", {})
    if seed.get("root") != ".codex/control-plane/runtime-seed" or seed.get("overwrite_existing") is not False:
        err("manifest must declare immutable runtime-state seed and non-overwrite initialization")
    if m.get("release_archive_builder") != ".codex/scripts/build_release_archive.py":
        err("manifest must declare deterministic definition-only release archive builder")
except Exception as exc:
    err(f"manifest invalid: {exc}")

# Runtime-state seed is immutable definition and must not contain historical
# swarm entries. Live `.codex/memory/**` belongs to the target checkout, not a
# release archive.
seed_memory = ROOT / ".codex/control-plane/runtime-seed/memory"
for required_seed in ["PROTOCOL.md", "INDEX.md"]:
    if not (seed_memory / required_seed).is_file():
        err(f"runtime-state seed missing {required_seed}")
seed_domains = seed_memory / "domains"
if not seed_domains.is_dir():
    err("runtime-state seed missing domains directory")
else:
    for p in sorted(seed_domains.glob("*.md")):
        if re.search(r"(?m)^## 20\d\d-", p.read_text(encoding="utf-8")):
            err(f"runtime-state seed contains historical runtime entry: {p.relative_to(ROOT)}")

# Enforcement contract structure.
try:
    c = json.loads((ROOT / ".codex/control-plane/enforcement-contract.json").read_text(encoding="utf-8"))
    needed = {
        "project_trust", "approval_policy", "permission_profile", "unrestricted_mode",
        "production_kalshi_credentials_present", "codex_has_kalshi_execution_credentials",
        "production_kalshi_network_enabled",
    }
    missing = needed - set(c.get("required", {}))
    if missing:
        err(f"enforcement contract missing required external state: {sorted(missing)}")
    if "does not grant" not in c.get("statement", "").lower():
        err("enforcement contract must state that it does not grant authority")
except Exception as exc:
    err(f"enforcement contract invalid: {exc}")

# Policy frontmatter must have paths and no empty pattern set.
for p in sorted((ROOT / ".codex/policies").rglob("*.md")):
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---\npaths:\n"):
        err(f"{p.relative_to(ROOT)} lacks paths frontmatter")
    if not re.search(r'^\s+-\s+"?.+"?$', t.split("---", 2)[1], re.M):
        err(f"{p.relative_to(ROOT)} has no paths")

# No live Claude harness paths in operational artifacts. Migration report is exempt.
for base in [ROOT / "AGENTS.md", ROOT / ".agents", ROOT / ".codex/agents", ROOT / ".codex/memory"]:
    files = [base] if base.is_file() else list(base.rglob("*"))
    for p in files:
        if not p.is_file():
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if ".claude/" in t or "CLAUDE.md" in t:
            err(f"live Claude harness reference remains: {p.relative_to(ROOT)}")
        if re.search(r"(?<![A-Za-z0-9_-])(?:[a-z0-9-]+-(?:engineer|reviewer|verifier|router|author))\.md\b", t):
            err(f"stale markdown agent path remains: {p.relative_to(ROOT)}")

# Explicit local references must resolve.
for p in [ROOT / ".agents/skills", ROOT / ".codex/agents", ROOT / ".codex/memory", ROOT / ".codex/scripts"]:
    for f in p.rglob("*"):
        if not f.is_file() or f.suffix not in {".md", ".toml", ".py"}:
            continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        for ref in re.findall(r"(?<![\w./-])((?:\.agents|\.codex)/(?:scripts|agents|skills|memory|control-plane)/[A-Za-z0-9_./<>-]+)", t):
            if "<" in ref or ">" in ref:
                continue
            candidate = ROOT / ref.rstrip(".,:)`")
            if not candidate.exists():
                normalized_ref = ref.rstrip(".,:)`")
                if normalized_ref.startswith(".codex/memory/"):
                    seed_candidate = seed_memory / normalized_ref.removeprefix(".codex/memory/")
                    if seed_candidate.exists():
                        continue
                err(f"{f.relative_to(ROOT)} references missing path: {ref}")

# Status line values remain a conservative verified subset.
try:
    cfg = tomllib.loads((ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
    allowed = {
        "model", "model-name", "model-with-reasoning", "reasoning", "current-dir", "project", "project-root",
        "project-name", "hostname", "git-branch", "pull-request-number", "branch-changes", "run-state", "status",
        "permissions", "approval-mode", "approval", "context-remaining", "context-used", "context-usage",
        "five-hour-limit", "weekly-limit", "codex-version", "context-window-size", "used-tokens", "total-input-tokens",
        "total-output-tokens", "thread-credits", "estimated-thread-cost", "thread-id", "session-id", "fast-mode",
        "raw-output", "thread-title", "workspace-headline", "task-progress",
    }
    for item in cfg.get("tui", {}).get("status_line", []):
        if item not in allowed:
            err(f"unsupported status_line item in package validator: {item}")
except Exception:
    pass

# The generated immutable definition snapshot must verify mechanically for a
# release gate. During an intentional definition edit, --pre-snapshot validates
# that the current tree can be deterministically snapshotted without requiring
# the previous release identity to match the new definition.
try:
    snapshot = load_module("definition_snapshot", ROOT / ".codex/scripts/build_definition_snapshot.py")
    if ARGS.pre_snapshot:
        candidate = snapshot.build()
        if candidate.get("file_count", 0) <= 0 or not candidate.get("aggregate_digest"):
            err("pre-snapshot definition build did not produce a valid candidate identity")
    else:
        ok, problems = snapshot.verify()
        if not ok:
            for problem in problems:
                err(problem)
except Exception as exc:
    err(f"definition snapshot verification failed: {exc}")

# Runtime artifacts do not belong in a release archive; warn if present in an active checkout.
for p in ROOT.rglob("events.jsonl"):
    warn(f"runtime Skill telemetry present (excluded from definition identity): {p.relative_to(ROOT)}")
for p in ROOT.rglob("*.pyc"):
    warn(f"Python bytecode present (generated non-identity artifact): {p.relative_to(ROOT)}")
for p in ROOT.rglob(".pytest_cache"):
    if p.is_dir():
        warn(f"pytest cache present (generated non-identity artifact): {p.relative_to(ROOT)}")

print(f"control-plane validation: {len(errors)} error(s), {len(warnings)} warning(s)")
for x in errors:
    print("ERROR:", x)
for x in warnings:
    print("WARN:", x)
raise SystemExit(1 if errors else 0)
