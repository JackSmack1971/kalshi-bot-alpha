#!/usr/bin/env python3
"""Compile deterministic path-scoped behavioral policy selections.

This resolver selects repository behavioral policy. It does not grant runtime
permissions. The JSON mode emits an identifiable ResolvedPolicySet suitable
for inclusion in an execution snapshot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
POLICY_ROOT = ROOT / ".codex" / "policies"
COMPILER = "policy-resolver/v2"


def _strip_dot_slash(value: str) -> str:
    value = value.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def parse_paths(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    parts = text.split("---", 2)
    if len(parts) < 3:
        return []
    out: list[str] = []
    in_paths = False
    for line in parts[1].splitlines():
        if re.match(r"^paths:\s*$", line):
            in_paths = True
            continue
        if in_paths:
            m = re.match(r'^\s+-\s+["\']?(.+?)["\']?\s*$', line)
            if m:
                out.append(m.group(1))
                continue
            if line and not line[0].isspace():
                break
    return out


def glob_regex(pattern: str) -> re.Pattern[str]:
    p = _strip_dot_slash(pattern)
    if not p:
        raise ValueError("empty policy path pattern")
    if PurePosixPath(p).is_absolute() or ".." in PurePosixPath(p).parts:
        raise ValueError(f"policy pattern escapes repository scope: {pattern!r}")
    out = ["^"]
    i = 0
    while i < len(p):
        if p.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
        elif p.startswith("**", i):
            out.append(".*")
            i += 2
        elif p[i] == "*":
            out.append("[^/]*")
            i += 1
        elif p[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(p[i]))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def normalize(path: str) -> str:
    raw = path.replace("\\", "/")
    p = Path(raw)
    if p.is_absolute():
        try:
            rel = p.resolve(strict=False).relative_to(ROOT.resolve())
        except ValueError as exc:
            raise ValueError(f"path is outside repository root: {path}") from exc
        normalized = rel.as_posix()
    else:
        stripped = _strip_dot_slash(raw)
        pure = PurePosixPath(stripped)
        if pure.is_absolute() or ".." in pure.parts:
            raise ValueError(f"path escapes repository root: {path}")
        normalized = pure.as_posix()
    if normalized in {"", "."}:
        raise ValueError("target path must identify a repository-relative path")
    return normalized


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for f in sorted(POLICY_ROOT.rglob("*.md")):
        content = f.read_bytes()
        text = content.decode("utf-8")
        pats = parse_paths(text)
        rows.append(
            {
                "path": f.relative_to(ROOT).as_posix(),
                "uri": f"repo://{f.relative_to(ROOT).as_posix()}",
                "content_digest": f"sha256:{_sha256(content)}",
                "patterns": pats,
                "compiled": [(p, glob_regex(p)) for p in pats],
            }
        )
    return rows


def resolve(paths: list[str]) -> list[dict[str, Any]]:
    """Compatibility view used by existing callers/tests."""
    inv = inventory()
    result: list[dict[str, Any]] = []
    for raw in paths:
        path = normalize(raw)
        matches: list[dict[str, Any]] = []
        for row in inv:
            matched = [pat for pat, rx in row["compiled"] if rx.fullmatch(path)]
            if matched:
                matches.append(
                    {
                        "policy": row["path"],
                        "patterns": matched,
                        "content_digest": row["content_digest"],
                    }
                )
        result.append({"path": path, "matches": matches})
    return result


def compile_policy_set(paths: list[str]) -> dict[str, Any]:
    # A write set is semantically a set, not an ordered list. Canonicalize it
    # before compilation so callers that discover the same targets in a
    # different order receive the same policy snapshot identity.
    canonical_targets = sorted({normalize(path) for path in paths})
    resolved = resolve(canonical_targets)
    selected: dict[str, dict[str, Any]] = {}
    for target in resolved:
        for match in target["matches"]:
            entry = selected.setdefault(
                match["policy"],
                {
                    "uri": f"repo://{match['policy']}",
                    "content_digest": match["content_digest"],
                    "matched_patterns": set(),
                    "matched_targets": set(),
                },
            )
            entry["matched_patterns"].update(match["patterns"])
            entry["matched_targets"].add(target["path"])

    policies = []
    for policy in sorted(selected):
        entry = selected[policy]
        policies.append(
            {
                "uri": entry["uri"],
                "content_digest": entry["content_digest"],
                "matched_patterns": sorted(entry["matched_patterns"]),
                "matched_targets": sorted(entry["matched_targets"]),
            }
        )

    core = {
        "compiler": COMPILER,
        "target_paths": [row["path"] for row in resolved],
        "policies": policies,
    }
    digest = _sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode())
    return {**core, "digest": f"sha256:{digest}"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true", help="emit ResolvedPolicySet JSON")
    args = ap.parse_args()
    try:
        if args.json:
            print(json.dumps(compile_policy_set(args.paths), indent=2, sort_keys=True))
            return 0
        rows = resolve(args.paths)
    except ValueError as exc:
        ap.error(str(exc))

    for row in rows:
        print(row["path"])
        if not row["matches"]:
            print("  (no path-specific policy)")
        for match in row["matches"]:
            print("  " + match["policy"])
            print("    digest " + match["content_digest"])
            for pat in match["patterns"]:
                print("    <- " + pat)
    print("ResolvedPolicySet: " + compile_policy_set(args.paths)["digest"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
