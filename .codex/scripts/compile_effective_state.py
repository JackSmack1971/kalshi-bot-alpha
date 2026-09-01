#!/usr/bin/env python3
"""Compile a reproducible project execution-state snapshot from observable inputs.

The compiler records unresolved external state as UNVERIFIED. It never infers
permissions, approvals, credentials, tool availability, model identity, or
network authority from repository instructions.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / ".codex" / "control-plane"
COMPILER = "control-plane-compiler/v1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _json_file(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _git_state() -> dict[str, Any]:
    def run(*args: str) -> tuple[int, str]:
        p = subprocess.run(["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return p.returncode, p.stdout.strip()
    rc, top = run("rev-parse", "--show-toplevel")
    if rc != 0 or Path(top).resolve() != ROOT.resolve():
        return {"status": "UNAVAILABLE", "reason": "not a Git repository rooted at package root"}
    _, head = run("rev-parse", "HEAD")
    _, branch = run("branch", "--show-current")
    _, dirty = run("status", "--porcelain=v1")
    dirty_digest = hashlib.sha256(dirty.encode()).hexdigest()
    return {
        "status": "RESOLVED",
        "repository": "repo://.",
        "baseline_head": head,
        "branch": branch or None,
        "dirty_state_digest": f"sha256:{dirty_digest}",
    }


def _inventory_digests(base: Path, glob: str) -> list[dict[str, str]]:
    out = []
    for path in sorted(base.glob(glob)):
        if path.is_file():
            out.append({"id": f"repo://{path.relative_to(ROOT).as_posix()}", "digest": _sha256(path)})
    return out


def compile_snapshot(args: argparse.Namespace) -> dict[str, Any]:
    builder = _load_module("definition_snapshot", ROOT / ".codex/scripts/build_definition_snapshot.py")
    allow_unreleased = bool(getattr(args, "_allow_unreleased_definition", False))
    if allow_unreleased:
        # Internal test/pre-release use only. The CLI intentionally exposes no
        # switch for this because execution snapshots should normally bind to
        # a verified immutable release identity.
        definition = builder.build()
        definition_status = "UNRELEASED_CANDIDATE"
    else:
        ok, problems = builder.verify()
        if not ok:
            raise ValueError("definition snapshot invalid: " + "; ".join(problems))
        definition = json.loads((CONTROL / "definition-snapshot.json").read_text(encoding="utf-8"))
        definition_status = "VERIFIED_RELEASE"

    resolver = _load_module("policy_resolver", ROOT / ".codex/scripts/resolve_policies.py")
    policy = resolver.compile_policy_set(args.target_path) if args.target_path else {
        "compiler": resolver.COMPILER,
        "target_paths": [],
        "policies": [],
        "digest": "sha256:" + hashlib.sha256(b"empty-policy-set").hexdigest(),
    }

    authority = _json_file(args.authority_state)
    enforcement = _load_module("enforcement", ROOT / ".codex/scripts/verify_enforcement_contract.py")
    authority_check = enforcement.evaluate(authority or {})
    if authority is None:
        authority_check["status"] = "UNVERIFIED"
        authority_check["statement"] = "No external authority-state evidence supplied; nothing is inferred from repository policy."

    capability = _json_file(args.capability_state)
    environment = _json_file(args.environment_state)
    uow = _json_file(args.uow_state)
    if uow is not None:
        uow_compiler = _load_module("uow_capture", ROOT / ".codex/scripts/capture_uow.py")
        uow_ok, uow_problems = uow_compiler.verify(uow)
        if not uow_ok:
            raise ValueError("UoW state invalid: " + "; ".join(uow_problems))

    instruction_def = {
        "scope": "project-definition-only",
        "sources": [{"id": "repo://AGENTS.md", "digest": _sha256(ROOT / "AGENTS.md")}],
        "status": "RESOLVED",
        "note": "Platform, managed, developer, global, Skill-activation, and task instruction layers require runtime evidence and are not inferred here.",
    }
    instruction_def["digest"] = "sha256:" + hashlib.sha256(
        json.dumps(instruction_def, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()

    core = {
        "compiler": COMPILER,
        "control_plane": {
            "version": json.loads((CONTROL / "manifest.json").read_text(encoding="utf-8"))["version"],
            "definition_status": definition_status,
            "definition_digest": definition["aggregate_digest"],
            "definition_file_count": definition["file_count"],
        },
        "repository": _git_state(),
        "project_instructions": instruction_def,
        "path_policy": policy,
        "skills": {
            "status": "DEFINITION_INVENTORY",
            "items": _inventory_digests(ROOT / ".agents" / "skills", "*/SKILL.md"),
            "note": "Inventory is not activation state and grants no capability.",
        },
        "agents": {
            "status": "DEFINITION_INVENTORY",
            "items": _inventory_digests(ROOT / ".codex" / "agents", "*.toml"),
        },
        "model": {
            "status": "RESOLVED" if args.model else "UNVERIFIED",
            "resolved_model": args.model,
            "reasoning_effort": args.reasoning_effort,
        },
        "authority": {
            "status": authority_check["status"],
            "evidence": authority,
            "contract_result": authority_check,
            "contract_digest": _sha256(CONTROL / "enforcement-contract.json"),
        },
        "capabilities": capability if capability is not None else {
            "status": "UNVERIFIED",
            "note": "Registered/available/visible/authorized capability state was not supplied.",
        },
        "environment": environment if environment is not None else {
            "status": "UNVERIFIED",
            "note": "Runtime, network, and credential-state evidence was not supplied.",
        },
        "unit_of_work": uow if uow is not None else {
            "status": "UNVERIFIED",
            "note": "Capture a Git-grounded baseline with capture_uow.py when executing in the target repository.",
        },
    }
    snapshot_id = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**core, "snapshot_id": f"sha256:{snapshot_id}"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-path", action="append", default=[])
    parser.add_argument("--authority-state", type=Path)
    parser.add_argument("--capability-state", type=Path)
    parser.add_argument("--environment-state", type=Path)
    parser.add_argument("--uow-state", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--reasoning-effort")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        snapshot = compile_snapshot(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"effective-state compiler error: {exc}")
        return 2
    text = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
