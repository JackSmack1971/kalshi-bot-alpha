#!/usr/bin/env python3
"""Build or verify the immutable control-plane definition snapshot.

Mutable runtime state is intentionally excluded: `.codex/memory/**`, live
Skill telemetry, `.control-plane-state/**`, Python bytecode/cache files, and
the snapshot outputs themselves.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / ".codex" / "control-plane"
HASH_FILE = CONTROL / "DEFINITION_HASHES.sha256"
SNAPSHOT_FILE = CONTROL / "definition-snapshot.json"
BUILDER = "definition-snapshot/v1"
SCHEMA_VERSION = 1
MUTABLE_STATE_EXCLUDED = [
    ".codex/memory/**",
    ".agents/skills/**/telemetry/events.jsonl",
    ".control-plane-state/**",
    "**/__pycache__/**",
    "**/*.pyc",
    "**/.pytest_cache/**",
]


def _excluded(rel: str) -> bool:
    parts = Path(rel).parts
    if rel in {
        ".codex/control-plane/DEFINITION_HASHES.sha256",
        ".codex/control-plane/definition-snapshot.json",
    }:
        return True
    if rel.startswith(".codex/memory/") or rel == ".codex/memory":
        return True
    if rel.startswith(".control-plane-state/") or rel == ".control-plane-state":
        return True
    if rel.endswith("/telemetry/events.jsonl"):
        return True
    if "__pycache__" in parts or ".pytest_cache" in parts or rel.endswith(".pyc") or rel.endswith(".pyo"):
        return True
    return False


def definition_files() -> list[Path]:
    candidates: set[Path] = set()
    explicit = [ROOT / "AGENTS.md", ROOT / ".codex" / "README.md", ROOT / ".codex" / "MIGRATION_REPORT.md"]
    for path in explicit:
        if path.is_file():
            candidates.add(path)
    for base in [
        ROOT / ".codex" / "config.toml",
        ROOT / ".codex" / "agents",
        ROOT / ".codex" / "policies",
        ROOT / ".codex" / "scripts",
        ROOT / ".codex" / "tests",
        ROOT / ".codex" / "evals",
        ROOT / ".codex" / "control-plane",
        ROOT / ".agents" / "skills",
    ]:
        if base.is_file():
            candidates.add(base)
        elif base.is_dir():
            for path in base.rglob("*"):
                if path.is_file():
                    candidates.add(path)
    return sorted(
        (p for p in candidates if not _excluded(p.relative_to(ROOT).as_posix())),
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )


def _digest(path: Path) -> str:
    # Definition identity must be stable across Windows and Linux checkouts.
    # All definition files are text; canonicalize their line endings before
    # hashing so Git's working-tree conversion cannot change the identity.
    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def build() -> dict:
    rows = []
    lines = []
    for path in definition_files():
        rel = path.relative_to(ROOT).as_posix()
        digest = _digest(path)
        rows.append({"path": rel, "sha256": digest})
        lines.append(f"{digest}  {rel}\n")
    manifest_digest = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
    return {
        "schema_version": SCHEMA_VERSION,
        "builder": BUILDER,
        "mutable_state_excluded": MUTABLE_STATE_EXCLUDED,
        "file_count": len(rows),
        "files": rows,
        "aggregate_digest": f"sha256:{manifest_digest}",
    }


def write_snapshot() -> dict:
    snapshot = build()
    hash_text = "".join(f"{row['sha256']}  {row['path']}\n" for row in snapshot["files"])
    snapshot_text = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"
    with HASH_FILE.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(hash_text)
    with SNAPSHOT_FILE.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(snapshot_text)
    return snapshot


def verify() -> tuple[bool, list[str]]:
    problems: list[str] = []
    if not HASH_FILE.is_file() or not SNAPSHOT_FILE.is_file():
        return False, ["definition snapshot outputs are missing"]
    try:
        recorded = json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"definition snapshot JSON invalid: {exc}"]
    current = build()
    if recorded.get("schema_version") != SCHEMA_VERSION:
        problems.append("definition snapshot schema_version mismatch")
    if recorded.get("builder") != BUILDER:
        problems.append("definition snapshot builder version mismatch")
    if recorded.get("mutable_state_excluded") != MUTABLE_STATE_EXCLUDED:
        problems.append("definition snapshot mutable-state exclusion metadata mismatch")
    if recorded.get("file_count") != current["file_count"]:
        problems.append("definition snapshot file_count mismatch")
    if recorded.get("files") != current["files"]:
        recorded_map = {r["path"]: r["sha256"] for r in recorded.get("files", [])}
        current_map = {r["path"]: r["sha256"] for r in current["files"]}
        for path in sorted(set(recorded_map) | set(current_map)):
            if recorded_map.get(path) != current_map.get(path):
                problems.append(f"definition mismatch: {path}")
    if recorded.get("aggregate_digest") != current["aggregate_digest"]:
        problems.append("aggregate definition digest mismatch")
    expected_hash_text = "".join(
        f"{row['sha256']}  {row['path']}\n" for row in recorded.get("files", [])
    )
    if HASH_FILE.read_text(encoding="utf-8") != expected_hash_text:
        problems.append("DEFINITION_HASHES.sha256 does not match definition-snapshot.json")
    return not problems, problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.write:
        snapshot = write_snapshot()
        print(json.dumps({"aggregate_digest": snapshot["aggregate_digest"], "file_count": snapshot["file_count"]}, sort_keys=True))
        return 0
    ok, problems = verify()
    if ok:
        print("definition snapshot: PASS")
        return 0
    print("definition snapshot: FAIL")
    for problem in problems:
        print("ERROR:", problem)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
