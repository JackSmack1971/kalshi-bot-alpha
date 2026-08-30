#!/usr/bin/env python3
"""Emit a deterministic, read-only summary of memory status and discrepancies."""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAGS = ("BLOCKER", "QUESTION", "HANDOFF", "DECISION-NEEDED", "INVARIANT-RISK", "FINDING")


def entries(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    chunks = re.split(r"(?m)^## ", text)[1:]
    out = []
    for chunk in chunks:
        lines = chunk.splitlines()
        title = lines[0] if lines else ""
        row = {"title": title}
        for key in ("Task", "Touched", "Verified", "Status", "Notes"):
            m = re.search(rf"(?m)^{key}: (.+)$", chunk)
            row[key.lower()] = m.group(1).strip() if m else ""
        out.append(row)
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    index = entries(ROOT / ".codex/memory/INDEX.md")
    domains = {
        x.stem: entries(x)[-1] if entries(x) else {}
        for x in (ROOT / ".codex/memory/domains").glob("*.md")
    }
    unresolved = {tag: sum(1 for e in index if f"[{tag}]" in e["title"]) for tag in TAGS}
    payload = {
        "unresolved_counts": unresolved,
        "domain_latest_status": {k: v.get("status", "") for k, v in sorted(domains.items())},
        "index_entries": len(index),
        "domain_entries": sum(
            len(entries(x)) for x in (ROOT / ".codex/memory/domains").glob("*.md")
        ),
    }
    if a.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print("Swarm status")
        print("Unresolved: " + ", ".join(f"{k}={v}" for k, v in unresolved.items()))
        for k, v in payload["domain_latest_status"].items():
            print(f"{k}: {v or 'no entries'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
