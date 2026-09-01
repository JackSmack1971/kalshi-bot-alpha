#!/usr/bin/env python3
"""Validate the 65-case control-plane corpus and grade observed Codex trials.

This script does not claim to execute Codex itself. It turns the corpus into an
executable grading contract for externally captured baseline/candidate runs.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / ".codex" / "control-plane" / "evals"
FILES = {
    "routing": EVALS / "routing_cases.jsonl",
    "task": EVALS / "task_cases.jsonl",
    "failure": EVALS / "failure_cases.jsonl",
}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{lineno}: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{lineno}: record must be object")
        rows.append(value)
    return rows


def corpus() -> dict[str, list[dict[str, Any]]]:
    return {kind: _read_jsonl(path) for kind, path in FILES.items()}


def validate_corpus() -> dict[str, Any]:
    data = corpus()
    errors = []
    seen = set()
    for kind, rows in data.items():
        for row in rows:
            cid = row.get("id")
            if not isinstance(cid, str) or not cid:
                errors.append(f"{kind}: missing id")
                continue
            if cid in seen:
                errors.append(f"duplicate case id: {cid}")
            seen.add(cid)
    for row in data["routing"]:
        if row.get("kind") not in {"positive", "negative", "neighbor"} or not row.get("prompt"):
            errors.append(f"invalid routing case: {row.get('id')}")
            continue
        if row.get("kind") == "positive" and not row.get("expected_skill"):
            errors.append(f"positive routing case missing expected_skill: {row.get('id')}")
        if row.get("expected_skill") is not None and not isinstance(row.get("expected_skill"), str):
            errors.append(f"routing expected_skill must be string or null: {row.get('id')}")
    for row in data["task"]:
        if not row.get("skill") or not row.get("goal") or not isinstance(row.get("success"), list) or not row["success"]:
            errors.append(f"invalid task case: {row.get('id')}")
    for row in data["failure"]:
        if not row.get("condition") or not row.get("expected"):
            errors.append(f"invalid failure case: {row.get('id')}")
    counts = {kind: len(rows) for kind, rows in data.items()}
    return {"valid": not errors, "errors": errors, "counts": counts, "total": sum(counts.values())}


def grade(path: Path) -> dict[str, Any]:
    data = corpus()
    expected = {row["id"]: (kind, row) for kind, rows in data.items() for row in rows}
    observed = _read_jsonl(path)
    by_id: dict[str, dict[str, Any]] = {}
    errors = []
    for row in observed:
        cid = row.get("case_id")
        if cid not in expected:
            errors.append(f"unknown case_id: {cid}")
            continue
        if cid in by_id:
            errors.append(f"duplicate observed case_id: {cid}")
        by_id[cid] = row

    routing_total = routing_pass = 0
    assertion_total = assertion_pass = 0
    missing = []
    details = []
    for cid, (kind, case) in expected.items():
        obs = by_id.get(cid)
        if obs is None:
            missing.append(cid)
            continue
        if kind == "routing":
            routing_total += 1
            selected = obs.get("selected_skill")
            passed = selected == case.get("expected_skill")
            routing_pass += int(passed)
            details.append({"case_id": cid, "kind": kind, "pass": passed})
            continue

        assertions = obs.get("assertions")
        if not isinstance(assertions, dict):
            details.append({"case_id": cid, "kind": kind, "pass": False, "reason": "missing assertions object"})
            if kind == "task":
                assertion_total += len(case["success"])
            else:
                assertion_total += 1
            continue
        criteria = case["success"] if kind == "task" else [case["expected"]]
        passed_all = True
        for criterion in criteria:
            assertion_total += 1
            passed = assertions.get(criterion) is True
            assertion_pass += int(passed)
            passed_all &= passed
        details.append({"case_id": cid, "kind": kind, "pass": passed_all})

    complete = not missing and not errors
    passed = (
        complete
        and routing_pass == routing_total
        and assertion_pass == assertion_total
    )
    return {
        "complete": complete,
        "passed": passed,
        "errors": errors,
        "missing_cases": sorted(missing),
        "routing": {
            "passed": routing_pass,
            "total": routing_total,
            "accuracy": (routing_pass / routing_total) if routing_total else None,
        },
        "workflow_assertions": {
            "passed": assertion_pass,
            "total": assertion_total,
            "pass_rate": (assertion_pass / assertion_total) if assertion_total else None,
        },
        "details": details,
        "note": (
            "complete means every corpus case had a structurally usable observation; "
            "passed additionally requires every routing expectation and workflow assertion to pass. "
            "A passed grade is empirical only when observations came from actual Codex trials "
            "against the intended target repository/runtime."
        )
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--validate-corpus", action="store_true")
    group.add_argument("--grade", type=Path)
    args = parser.parse_args()
    try:
        result = validate_corpus() if args.validate_corpus else grade(args.grade)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.validate_corpus:
        return 0 if result["valid"] else 1
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
