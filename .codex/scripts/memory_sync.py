#!/usr/bin/env python3
"""Deterministically append a compliant memory entry; no prior entry is edited."""

from __future__ import annotations
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAINS = {
    "transport-safety",
    "market-data",
    "strategy",
    "risk",
    "accounting-ledger",
    "runtime-execution",
    "research-integrity",
    "openrouter-agents",
    "governance-approvals",
    "security",
    "architecture",
    "phase-integration",
}
STATUSES = {"done", "blocked", "needs-human-approval", "handoff", "refused-scope"}
SECRET_VALUE = re.compile(
    r"(?i)(bearer\s+\S+|-----begin|sk-[A-Za-z0-9]{16,}|api[_-]?key\s*[:=]\s*\S+)"
)


def _require_initialized_memory() -> None:
    required = [
        ROOT / ".codex/memory/PROTOCOL.md",
        ROOT / ".codex/memory/INDEX.md",
    ]
    missing = [p.relative_to(ROOT).as_posix() for p in required if not p.is_file()]
    if missing:
        raise ValueError(
            "runtime memory is not initialized; run "
            "`python .codex/scripts/initialize_runtime_state.py --initialize` first; "
            f"missing: {', '.join(missing)}"
        )


def append(
    domain: str,
    task: str,
    touched: str,
    verified: str,
    status: str,
    notes: str,
    index_tag: str | None,
) -> dict[str, str]:
    _require_initialized_memory()
    if domain not in DOMAINS or status not in STATUSES or not all((task, touched, verified, notes)):
        raise ValueError("invalid domain, status, or empty entry field")
    if index_tag and index_tag not in {
        "BLOCKER",
        "QUESTION",
        "HANDOFF",
        "DECISION-NEEDED",
        "INVARIANT-RISK",
        "FINDING",
    }:
        raise ValueError("invalid index tag")
    values = (task, touched, verified, notes)
    if any(SECRET_VALUE.search(v) for v in values):
        raise ValueError("sensitive content rejected")
    heading = f"## {date.today().isoformat()} — {domain} — {notes[:70]}"
    body = f"{heading}\nTask: {task}\nTouched: {touched}\nVerified: {verified}\nStatus: {status}\nNotes: {notes}\n"
    target = ROOT / ".codex/memory/domains" / f"{domain}.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8", newline="\n") as h:
        h.write("\n" + body)
    if index_tag:
        index_body = body.replace(f"— {domain} —", f"— {domain} — [{index_tag}]", 1)
        with (ROOT / ".codex/memory/INDEX.md").open("a", encoding="utf-8", newline="\n") as h:
            h.write("\n" + index_body)
    return {"domain": domain, "status": status, "index_appended": str(bool(index_tag)).lower()}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("domain", "task", "touched", "verified", "status", "notes"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--index-tag")
    a = p.parse_args()
    try:
        print(
            json.dumps(
                append(a.domain, a.task, a.touched, a.verified, a.status, a.notes, a.index_tag),
                sort_keys=True,
            )
        )
        return 0
    except (OSError, ValueError) as e:
        print(f"memory sync error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
