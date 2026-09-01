#!/usr/bin/env python3
"""Initialize missing mutable control-plane runtime state from immutable seeds.

The seed is release definition; `.codex/memory/**` is mutable runtime data and is
not part of release identity. Initialization creates missing files only and never
overwrites existing memory. Running this script does not grant runtime authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / ".codex" / "control-plane" / "runtime-seed" / "memory"
TARGET = ROOT / ".codex" / "memory"


def seed_files() -> list[Path]:
    if not SEED.is_dir():
        raise RuntimeError(f"runtime-state seed missing: {SEED}")
    files = sorted((p for p in SEED.rglob("*") if p.is_file()), key=lambda p: p.relative_to(SEED).as_posix())
    if not files:
        raise RuntimeError("runtime-state seed is empty")
    return files


def check() -> dict:
    expected = [p.relative_to(SEED).as_posix() for p in seed_files()]
    missing = [rel for rel in expected if not (TARGET / rel).is_file()]
    return {
        "status": "READY" if not missing else "MISSING",
        "runtime_root": ".codex/memory",
        "expected_files": expected,
        "missing_files": missing,
        "statement": "Runtime memory is mutable coordination data and carries no authorization.",
    }


def initialize() -> dict:
    created: list[str] = []
    existing: list[str] = []
    for source in seed_files():
        rel = source.relative_to(SEED)
        target = TARGET / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            with target.open("xb") as handle:
                handle.write(source.read_bytes())
            created.append(rel.as_posix())
        except FileExistsError:
            if not target.is_file():
                raise RuntimeError(f"runtime-state target exists but is not a file: {target}")
            existing.append(rel.as_posix())
    result = check()
    result.update({"created": created, "preserved_existing": existing})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--initialize", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = initialize() if args.initialize else check()
    except (OSError, RuntimeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
