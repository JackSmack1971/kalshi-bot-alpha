#!/usr/bin/env python3
"""Validate the skill corpus or compare like-for-like evaluation summaries."""

from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / ".codex/evals/skill-routing.json"


def validate() -> int:
    cases = json.loads(CORPUS.read_text(encoding="utf-8"))
    if not cases:
        raise ValueError("empty evaluation corpus")
    keys = {"skill", "query", "should_trigger"}
    if any(
        set(c) != keys or not c["query"].strip() or not isinstance(c["should_trigger"], bool)
        for c in cases
    ):
        raise ValueError("each case must contain exactly skill, query, should_trigger")
    skills = {p.name for p in (ROOT / ".agents/skills").iterdir() if p.is_dir()}
    missing = sorted({c["skill"] for c in cases} - skills)
    if missing:
        raise ValueError(f"unknown skills: {missing}")
    per = {s: {True: 0, False: 0} for s in skills}
    for c in cases:
        per[c["skill"]][c["should_trigger"]] += 1
    if any(not v[True] or not v[False] for v in per.values() if v[True] or v[False]):
        raise ValueError("every covered skill needs positive and negative cases")
    print(
        json.dumps({"cases": len(cases), "skills_covered": len(per), "valid": True}, sort_keys=True)
    )
    return 0


def compare(left: Path, right: Path) -> int:
    a = json.loads(left.read_text(encoding="utf-8"))
    b = json.loads(right.read_text(encoding="utf-8"))
    if a.get("mode") != b.get("mode") or a.get("skill_name") != b.get("skill_name"):
        raise ValueError("paired records must use the same skill and mode")
    ar = {x["query"]: x for x in a.get("results", [])}
    br = {x["query"]: x for x in b.get("results", [])}
    if set(ar) != set(br):
        raise ValueError("paired records must contain identical queries")
    result = []
    for q in sorted(ar):
        result.append(
            {
                "query": q,
                "baseline_pass": ar[q].get("pass"),
                "with_skill_pass": br[q].get("pass"),
                "changed": ar[q].get("pass") != br[q].get("pass"),
            }
        )
    print(
        json.dumps(
            {
                "skill_name": a["skill_name"],
                "mode": a["mode"],
                "results": result,
                "unknown": sum(x["with_skill_pass"] is None for x in result),
            },
            sort_keys=True,
        )
    )
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--validate", action="store_true")
    p.add_argument("--compare", nargs=2, metavar=("BASELINE", "WITH_SKILL"))
    a = p.parse_args()
    try:
        if a.validate:
            return validate()
        if a.compare:
            return compare(Path(a.compare[0]), Path(a.compare[1]))
        p.error("choose --validate or --compare")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as e:
        print(f"skill eval error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
