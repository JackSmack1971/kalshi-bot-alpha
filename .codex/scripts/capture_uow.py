#!/usr/bin/env python3
"""Capture a Git-grounded UnitOfWork baseline without mutating the repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
COMPILER = "uow-capture/v2"


def _git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.rstrip("\n")


def _normalize_path(value: str) -> str:
    value = value.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or str(pure) in {"", "."}:
        raise ValueError(f"invalid repository-relative intended path: {value!r}")
    return pure.as_posix()


def _status_paths() -> list[dict[str, str]]:
    raw = _git("status", "--porcelain=v1", "-z")
    if not raw:
        return []
    chunks = raw.split("\0")
    rows = []
    i = 0
    while i < len(chunks):
        entry = chunks[i]
        if not entry:
            i += 1
            continue
        status = entry[:2]
        path = entry[3:]
        row = {"status": status, "path": path.replace("\\", "/")}
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            # With porcelain v1 -z, the first path is the destination and the
            # second NUL field is the original/source path. Preserve both so
            # the baseline identifies the complete Git-visible rename/copy.
            if i + 1 < len(chunks) and chunks[i + 1]:
                row["orig_path"] = chunks[i + 1].replace("\\", "/")
                i += 1
        rows.append(row)
        i += 1
    return sorted(rows, key=lambda x: (x["path"], x.get("orig_path", ""), x["status"]))


def _core(intended_paths: list[str]) -> dict:
    top = Path(_git("rev-parse", "--show-toplevel")).resolve()
    if top != ROOT.resolve():
        raise RuntimeError(f"expected repository root {ROOT}, git resolved {top}")
    baseline = _git("rev-parse", "HEAD")
    branch = _git("branch", "--show-current") or None
    dirty = _status_paths()
    intended = sorted({_normalize_path(p) for p in intended_paths})
    return {
        "compiler": COMPILER,
        "repository": "repo://.",
        "baseline_head": baseline,
        "branch": branch,
        "initial_dirty_state": dirty,
        "intended_delta": intended,
        "statement": "This UnitOfWork records intended change scope and baseline identity; it does not grant authorization.",
    }


def capture(intended_paths: list[str]) -> dict:
    core = _core(intended_paths)
    digest = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {**core, "uow_id": f"sha256:{digest}"}


def verify(record: dict) -> tuple[bool, list[str]]:
    problems: list[str] = []
    if record.get("compiler") != COMPILER:
        problems.append("UoW compiler mismatch")
    if record.get("repository") != "repo://.":
        problems.append("UoW repository identity mismatch")
    if "authorized_delta" in record:
        problems.append("legacy authorized_delta field is forbidden; UoW intent is not an authorization grant")
    intended = record.get("intended_delta")
    if not isinstance(intended, list) or any(not isinstance(p, str) for p in intended):
        problems.append("UoW intended_delta must be a list of repository-relative paths")
    core = {k: v for k, v in record.items() if k != "uow_id"}
    expected = "sha256:" + hashlib.sha256(
        json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if record.get("uow_id") != expected:
        problems.append("UoW digest mismatch")
    return not problems, problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--intended-path", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = capture(args.intended_path)
    except (RuntimeError, ValueError) as exc:
        print(f"uow capture error: {exc}")
        return 2
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
