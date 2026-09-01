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
    protocol = ROOT / ".codex/memory/PROTOCOL.md"
    index_path = ROOT / ".codex/memory/INDEX.md"
    domains_path = ROOT / ".codex/memory/domains"
    initialized = protocol.is_file() and index_path.is_file() and domains_path.is_dir()
    if not initialized:
        payload = {
            "runtime_state": "MISSING",
            "instruction": "run `python .codex/scripts/initialize_runtime_state.py --initialize`",
            "unresolved_counts": {tag: 0 for tag in TAGS},
            "domain_latest_status": {},
            "index_entries": 0,
            "domain_entries": 0,
        }
        if a.json:
            print(json.dumps(payload, sort_keys=True))
        else:
            print("Swarm status: runtime memory missing")
            print(payload["instruction"])
        return 1
    index = entries(index_path)
    domains = {
        x.stem: entries(x)[-1] if entries(x) else {}
        for x in domains_path.glob("*.md")
    }
    unresolved = {tag: sum(1 for e in index if f"[{tag}]" in e["title"]) for tag in TAGS}
    payload = {
        "unresolved_counts": unresolved,
        "runtime_state": "READY",
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
