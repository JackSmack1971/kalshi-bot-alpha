#!/usr/bin/env python3
"""Report whether product paths have a matching append-only domain-memory trace."""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_HINTS = {
    "transport": "transport-safety",
    "rest": "transport-safety",
    "ws": "transport-safety",
    "market": "market-data",
    "strategy": "strategy",
    "risk": "risk",
    "ledger": "accounting-ledger",
    "recon": "accounting-ledger",
    "agent": "openrouter-agents",
    "openrouter": "openrouter-agents",
    "approval": "governance-approvals",
    "runtime": "runtime-execution",
    "experiment": "research-integrity",
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("paths", nargs="+")
    a = p.parse_args()
    logs = {
        x.stem: x.read_text(encoding="utf-8") for x in (ROOT / ".codex/memory/domains").glob("*.md")
    }
    gaps = []
    covered = []
    for raw in a.paths:
        path = raw.replace("\\", "/")
        if not path.startswith(("src/", "schemas/", "config/")):
            continue
        key = next((v for k, v in DOMAIN_HINTS.items() if k in path.lower()), None)
        if key and re.search(rf"(?m)^Touched: .*{re.escape(path)}", logs.get(key, "")):
            covered.append(path)
        else:
            gaps.append(path)
    print(
        json.dumps(
            {"covered": covered, "gaps": gaps, "status": "pass" if not gaps else "memory-sync-gap"},
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
