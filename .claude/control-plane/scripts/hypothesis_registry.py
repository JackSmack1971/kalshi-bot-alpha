from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "hypothesis_id",
    "friction_key",
    "target_artifacts",
    "success_criteria",
    "evidence_refs",
    "recurrence_count",
    "impact_score",
    "priority_score",
    "evaluation",
)
EVALUATORS = {"control-plane-validation-errors"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
EVIDENCE_REF_PATTERN = re.compile(r"^\.claude/control-plane/runs/\S+$")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_int(record: dict[str, Any], key: str) -> int:
    value = record.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{record.get('hypothesis_id', '<unknown>')}: {key} must be an integer")
    return value


def normalize_record(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("Each hypothesis record must be an object")

    record = dict(raw)
    hypothesis_id = record.get("hypothesis_id")
    if not isinstance(hypothesis_id, str) or not ID_PATTERN.fullmatch(hypothesis_id):
        raise ValueError("Each hypothesis record must include a valid hypothesis_id")

    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError(f"{hypothesis_id}: missing required field(s): {', '.join(missing)}")

    recurrence_count = _require_int(record, "recurrence_count")
    impact_score = _require_int(record, "impact_score")
    priority_score = _require_int(record, "priority_score")

    if recurrence_count < 1:
        raise ValueError(f"{hypothesis_id}: recurrence_count must be >= 1")
    if impact_score < 0:
        raise ValueError(f"{hypothesis_id}: impact_score must be >= 0")

    derived_priority = recurrence_count * 1000 + impact_score
    if priority_score != derived_priority:
        raise ValueError(
            f"{hypothesis_id}: priority_score must equal recurrence_count * 1000 + impact_score"
        )

    target_artifacts = record["target_artifacts"]
    evidence_refs = record["evidence_refs"]
    if (
        not isinstance(target_artifacts, list)
        or not target_artifacts
        or any(not isinstance(value, str) or not value for value in target_artifacts)
    ):
        raise ValueError(f"{hypothesis_id}: target_artifacts must be a non-empty string list")
    if (
        not isinstance(evidence_refs, list)
        or not evidence_refs
        or any(
            not isinstance(value, str) or not EVIDENCE_REF_PATTERN.fullmatch(value)
            for value in evidence_refs
        )
    ):
        raise ValueError(f"{hypothesis_id}: evidence_refs must be a non-empty run-path string list")
    for key in ("friction_key", "success_criteria"):
        if not isinstance(record[key], str) or not record[key]:
            raise ValueError(f"{hypothesis_id}: {key} must be a non-empty string")

    evaluation = record["evaluation"]
    if not isinstance(evaluation, dict) or set(evaluation) != {
        "evaluator",
        "minimum_effect",
        "minimum_evidence_count",
    }:
        raise ValueError(f"{hypothesis_id}: evaluation must contain only the required policy fields")
    evaluator = evaluation["evaluator"]
    if evaluator not in EVALUATORS:
        raise ValueError(f"{hypothesis_id}: evaluator is not allowlisted")
    for key in ("minimum_effect", "minimum_evidence_count"):
        value = evaluation[key]
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise ValueError(f"{hypothesis_id}: {key} must be an integer >= 1")

    return {
        "hypothesis_id": hypothesis_id,
        "friction_key": record["friction_key"],
        "target_artifacts": target_artifacts,
        "success_criteria": record["success_criteria"],
        "evidence_refs": evidence_refs,
        "recurrence_count": recurrence_count,
        "impact_score": impact_score,
        "priority_score": priority_score,
        "evaluation": {
            "evaluator": evaluator,
            "minimum_effect": evaluation["minimum_effect"],
            "minimum_evidence_count": evaluation["minimum_evidence_count"],
        },
    }


def _sort_key(record: dict[str, Any]) -> tuple[int, int, int, str]:
    return (
        -record["recurrence_count"],
        -record["impact_score"],
        -record["priority_score"],
        record["hypothesis_id"],
    )


def load_hypotheses(path: Path) -> list[dict[str, Any]]:
    raw = _load_json(path)
    if isinstance(raw, dict):
        records = raw.get("hypotheses")
    else:
        records = raw
    if not isinstance(records, list):
        raise ValueError("Input must be a JSON list or an object with a hypotheses list")
    return [normalize_record(record) for record in records]


def sort_hypotheses(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(records, key=_sort_key)


def _self_check() -> None:
    records = [
        {
            "hypothesis_id": "h-2",
            "friction_key": "b",
            "target_artifacts": ["x"],
            "success_criteria": "s",
            "evidence_refs": [".claude/control-plane/runs/run-1/result.json"],
            "recurrence_count": 1,
            "impact_score": 5,
            "priority_score": 1005,
            "evaluation": {
                "evaluator": "control-plane-validation-errors",
                "minimum_effect": 1,
                "minimum_evidence_count": 1,
            },
        },
        {
            "hypothesis_id": "h-1",
            "friction_key": "a",
            "target_artifacts": ["x"],
            "success_criteria": "s",
            "evidence_refs": [".claude/control-plane/runs/run-1/result.json"],
            "recurrence_count": 2,
            "impact_score": 1,
            "priority_score": 2001,
            "evaluation": {
                "evaluator": "control-plane-validation-errors",
                "minimum_effect": 2,
                "minimum_evidence_count": 3,
            },
        },
        {
            "hypothesis_id": "h-3",
            "friction_key": "c",
            "target_artifacts": ["x"],
            "success_criteria": "s",
            "evidence_refs": [".claude/control-plane/runs/run-1/result.json"],
            "recurrence_count": 1,
            "impact_score": 5,
            "priority_score": 1005,
            "evaluation": {
                "evaluator": "control-plane-validation-errors",
                "minimum_effect": 1,
                "minimum_evidence_count": 1,
            },
        },
    ]
    ordered = sort_hypotheses(records)
    assert [item["hypothesis_id"] for item in ordered] == ["h-1", "h-2", "h-3"]
    assert normalize_record(records[0])["evaluation"] == records[0]["evaluation"]
    assert normalize_record(records[0])["hypothesis_id"] == "h-2"

    def must_fail(record: dict[str, Any]) -> None:
        try:
            normalize_record(record)
        except ValueError:
            return
        raise AssertionError("Malformed hypothesis input must fail closed")

    alias_only = dict(records[0])
    alias_only["id"] = alias_only.pop("hypothesis_id")
    must_fail(alias_only)
    missing_priority = dict(records[0])
    missing_priority.pop("priority_score")
    must_fail(missing_priority)
    missing_evaluation = dict(records[0])
    missing_evaluation.pop("evaluation")
    must_fail(missing_evaluation)
    for invalid in (
        {"evaluator": "shell", "minimum_effect": 1, "minimum_evidence_count": 1},
        {"evaluator": "control-plane-validation-errors", "minimum_effect": True, "minimum_evidence_count": 1},
        {"evaluator": "control-plane-validation-errors", "minimum_effect": 0, "minimum_evidence_count": 1},
        {"evaluator": "control-plane-validation-errors", "minimum_effect": 1, "minimum_evidence_count": 0},
        {"evaluator": "control-plane-validation-errors", "minimum_effect": 1, "minimum_evidence_count": 1, "extra": 1},
    ):
        malformed = dict(records[0])
        malformed["evaluation"] = invalid
        must_fail(malformed)
    for key, invalid in (
        ("friction_key", {}),
        ("friction_key", ""),
        ("success_criteria", {}),
        ("success_criteria", ""),
        ("target_artifacts", ["x", {}]),
        ("target_artifacts", [""]),
        ("evidence_refs", [".claude/control-plane/runs/run-1/result.json", {}]),
        ("evidence_refs", ["elsewhere/result.json"]),
    ):
        malformed = dict(records[0])
        malformed[key] = invalid
        must_fail(malformed)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sort hypothesis records deterministically.")
    parser.add_argument("--input", type=Path, help="Path to a JSON file containing hypothesis records.")
    parser.add_argument("--self-check", action="store_true", help="Run the built-in smoke check.")
    args = parser.parse_args(argv)

    if args.self_check:
        _self_check()
        print("PASS: hypothesis_registry self-check")
        return 0

    if args.input is None:
        parser.error("--input is required unless --self-check is used")

    records = load_hypotheses(args.input)
    json.dump(sort_hypotheses(records), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# Backward-compatible alias for older imports.
_normalize_record = normalize_record
