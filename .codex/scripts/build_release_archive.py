#!/usr/bin/env python3
"""Build a deterministic definition-only control-plane release archive.

The archive is built from the verified definition snapshot plus the generated
snapshot files themselves. Mutable memory, Skill event streams, runtime state,
caches, bytecode, and Git metadata are never selected for packaging.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / ".codex" / "control-plane"
SNAPSHOT = CONTROL / "definition-snapshot.json"
HASHES = CONTROL / "DEFINITION_HASHES.sha256"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def _load_snapshot_builder():
    path = ROOT / ".codex" / "scripts" / "build_definition_snapshot.py"
    spec = importlib.util.spec_from_file_location("definition_snapshot", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def release_members() -> tuple[dict, list[Path]]:
    builder = _load_snapshot_builder()
    ok, problems = builder.verify()
    if not ok:
        raise ValueError("definition snapshot invalid: " + "; ".join(problems))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    paths = [ROOT / row["path"] for row in snapshot["files"]]
    paths.extend([HASHES, SNAPSHOT])
    seen: set[str] = set()
    ordered: list[Path] = []
    for path in sorted(paths, key=lambda p: p.relative_to(ROOT).as_posix()):
        rel = path.relative_to(ROOT).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        if path.is_symlink():
            raise ValueError(f"release member must not be a symlink: {rel}")
        if not path.is_file():
            raise ValueError(f"release member missing: {rel}")
        ordered.append(path)
    return snapshot, ordered


def build(output: Path) -> dict:
    snapshot, members = release_members()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in members:
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(rel, date_time=FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            mode = 0o755 if rel.startswith(".codex/scripts/") and rel.endswith(".py") else 0o644
            info.external_attr = (mode & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    archive_sha = hashlib.sha256(output.read_bytes()).hexdigest()
    manifest = json.loads((CONTROL / "manifest.json").read_text(encoding="utf-8"))
    return {
        "archive": str(output),
        "archive_sha256": f"sha256:{archive_sha}",
        "version": manifest["version"],
        "definition_digest": snapshot["aggregate_digest"],
        "member_count": len(members),
        "mutable_runtime_state_packaged": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(args.output)
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
