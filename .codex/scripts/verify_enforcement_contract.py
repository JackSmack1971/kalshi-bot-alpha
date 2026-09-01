#!/usr/bin/env python3
"""Verify supplied external authority evidence against the repository contract.

The contract is declarative. Passing this check means the supplied evidence
satisfies the declared requirements; it does not create or expand authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / ".codex" / "control-plane" / "enforcement-contract.json"


def evaluate(state: dict[str, Any], contract: dict[str, Any] | None = None) -> dict[str, Any]:
    contract = contract or json.loads(CONTRACT.read_text(encoding="utf-8"))
    satisfied = []
    missing = []
    violations = []
    optional_missing = []

    for key, rule in contract.get("required", {}).items():
        if key not in state:
            missing.append({"field": key, "reason": rule.get("reason")})
            continue
        value = state[key]
        if "equals" in rule and value != rule["equals"]:
            violations.append({"field": key, "observed": value, "rule": {"equals": rule["equals"]}, "reason": rule.get("reason")})
            continue
        if "not_in" in rule and value in rule["not_in"]:
            violations.append({"field": key, "observed": value, "rule": {"not_in": rule["not_in"]}, "reason": rule.get("reason")})
            continue
        satisfied.append(key)

    for key, rule in contract.get("optional_evidence", {}).items():
        if rule.get("present") and key not in state:
            optional_missing.append({"field": key, "reason": rule.get("reason")})

    status = "PASS" if not missing and not violations else ("FAIL" if violations else "UNVERIFIED")
    return {
        "status": status,
        "satisfied": sorted(satisfied),
        "missing_required_evidence": missing,
        "violations": violations,
        "missing_optional_evidence": optional_missing,
        "statement": "Verification observes supplied authority state; it does not grant authority."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="JSON object describing externally resolved authority state")
    args = parser.parse_args()
    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise ValueError("authority state must be a JSON object")
        result = evaluate(state)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"enforcement contract error: {exc}")
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
