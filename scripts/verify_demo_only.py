#!/usr/bin/env python3
"""Fail-closed static enforcement of the demo-only endpoint policy.

Scans enforced repository paths for Kalshi hostnames and fails when any
hostname outside the demo allowlist appears. See docs/SAFETY_MODEL.md §1.

Enforced from Phase 0 onward; intended to run in CI on every change.
Exit status: 0 when compliant, 1 when any violation is found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NamedTuple

ALLOWED_HOSTS: frozenset[str] = frozenset(
    {
        "external-api.demo.kalshi.co",
        "external-api-ws.demo.kalshi.co",
    }
)

# Any dotted hostname containing the label "kalshi", e.g. bare apex
# domains, demo hosts, and any production or elections API host.
KALSHI_HOSTNAME_RE = re.compile(
    r"\b(?:[a-z0-9-]+\.)*kalshi\.[a-z]{2,}(?:\.[a-z]{2,})?\b",
    re.IGNORECASE,
)

# Paths (relative to the repository root) where the policy is enforced.
# Reference material (docs-dev/) and prose documentation (docs/) may name
# forbidden hosts in order to forbid them; enforced paths may not.
ENFORCED_PATHS: tuple[str, ...] = (
    "src",
    "config",
    "schemas",
    "scripts",
    "tests",
    "migrations",
    "pyproject.toml",
    ".env.example",
)

SCANNED_SUFFIXES: frozenset[str] = frozenset(
    {".py", ".toml", ".yaml", ".yml", ".json", ".ini", ".cfg", ".txt", ".env", ".example"}
)


class Violation(NamedTuple):
    path: str
    line: int
    hostname: str


def find_violations_in_text(text: str, path: str = "<text>") -> list[Violation]:
    """Return every non-allowlisted Kalshi hostname found in ``text``."""
    violations: list[Violation] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in KALSHI_HOSTNAME_RE.finditer(line):
            hostname = match.group(0).lower()
            if hostname not in ALLOWED_HOSTS:
                violations.append(Violation(path=path, line=lineno, hostname=hostname))
    return violations


def iter_enforced_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for entry in ENFORCED_PATHS:
        target = repo_root / entry
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            files.extend(
                p
                for p in sorted(target.rglob("*"))
                if p.is_file() and (p.suffix in SCANNED_SUFFIXES or p.name.startswith(".env"))
            )
    return files


def scan_repository(repo_root: Path) -> list[Violation]:
    violations: list[Violation] = []
    for file_path in iter_enforced_files(repo_root):
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(file_path.relative_to(repo_root))
        violations.extend(find_violations_in_text(text, path=rel))
    return violations


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    violations = scan_repository(repo_root)
    if violations:
        print("DEMO-ONLY POLICY VIOLATION: non-demo Kalshi hostname(s) found:")
        for v in violations:
            print(f"  {v.path}:{v.line}: {v.hostname}")
        print("Only these hosts are permitted in enforced paths:")
        for host in sorted(ALLOWED_HOSTS):
            print(f"  {host}")
        return 1
    print(f"demo-only policy OK ({len(iter_enforced_files(repo_root))} files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
