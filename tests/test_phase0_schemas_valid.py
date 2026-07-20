"""Validate every Phase 0 JSON Schema contract under schemas/.

For each schema this asserts:

1. The schema file itself is syntactically valid Draft 2020-12 JSON
   Schema (``Draft202012Validator.check_schema``).
2. A minimal conforming example object validates successfully.
3. A deliberately invalid example object fails validation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

SCHEMAS_DIR = Path(__file__).resolve().parents[1] / "schemas"


def _load_schema(name: str) -> dict[str, Any]:
    path = SCHEMAS_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def _all_schema_files() -> list[Path]:
    return sorted(SCHEMAS_DIR.glob("*.schema.json"))


def test_schemas_directory_has_expected_files() -> None:
    expected = {
        "risk_limits.schema.json",
        "order-state.schema.json",
        "market_archetype.schema.json",
        "quote_expectancy.schema.json",
        "queue-calibration.schema.json",
        "markout-toxicity.schema.json",
        "experiment_registry.schema.json",
        "statistical-sufficiency.schema.json",
    }
    found = {p.name for p in _all_schema_files()}
    assert expected == found


@pytest.mark.parametrize("path", _all_schema_files(), ids=lambda p: p.name)
def test_schema_file_is_valid_draft_2020_12(path: Path) -> None:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)


# ---------------------------------------------------------------------------
# Minimal conforming examples and deliberately invalid examples, one pair per
# schema, keyed by schema filename.
# ---------------------------------------------------------------------------

VALID_EXAMPLES: dict[str, dict[str, Any]] = {
    "risk_limits.schema.json": {
        "schema_version": "1.0.0",
        "paper_bankroll": 1000,
        "max_risk_per_order": 5,
        "max_exposure_per_market": 25,
        "max_aggregate_exposure": 100,
        "max_open_orders": 10,
        "max_daily_paper_loss": 25,
        "max_strategy_drawdown_pct": 5,
        "min_time_before_close_seconds": 1800,
        "max_market_data_age_seconds": 2,
        "max_outstanding_request_age_seconds": 10,
    },
    "order-state.schema.json": {
        "schema_version": "1.0.0",
        "order_id": "ord-1",
        "client_order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "state": "INTENT_CREATED",
        "previous_state": None,
        "transitioned_at": "2026-07-20T00:00:00Z",
        "evidence_reference": "intent-evidence-1",
    },
    "market_archetype.schema.json": {
        "schema_version": "1.0.0",
        "archetype_id": "btc-threshold-24h-tight-spread-v1",
        "classifier_version": "1.0.0",
        "underlying_asset": "BTC",
        "contract_structure": "threshold",
        "time_to_settlement_bucket": "12h-24h",
        "market_age_bucket": "0-1d",
        "time_of_day_bucket": "UTC-12",
        "day_of_week": "MON",
        "spread_regime": "tight",
        "depth_regime": "thin",
        "external_reference_volatility_regime": "low",
        "event_driven": False,
    },
    "quote_expectancy.schema.json": {
        "schema_version": "1.0.0",
        "edge_model_version": "1.0.0",
        "quote_id": "quote-1",
        "signal_confidence": 0.6,
        "expected_fill_probability": 0.4,
        "expected_gross_spread_capture": 0.02,
        "expected_fee_cost": 0.001,
        "expected_adverse_selection": 0.002,
        "expected_inventory_cost": 0.001,
        "expected_settlement_risk": 0.001,
        "expected_cancel_reprice_cost": 0.0005,
        "expected_net_edge": 0.0135,
        "calibration_sample_size": 500,
        "calibration_confidence": 0.8,
    },
    "queue-calibration.schema.json": {
        "schema_version": "1.0.0",
        "calibration_method_version": "1.0.0",
        "order_id": "ord-1",
        "displayed_size_ahead_at_submission": 120,
        "queue_position_lower_bound": 0.2,
        "queue_position_upper_bound": 0.5,
        "estimated_cancellations_ahead": 10,
        "fill_probability_conditional": 0.35,
    },
    "markout-toxicity.schema.json": {
        "schema_version": "1.0.0",
        "rules_version": "1.0.0",
        "fill_id": "fill-1",
        "realized_spread_by_horizon": [{"horizon_seconds": 1, "realized_spread": 0.01}],
        "classification": "BENIGN",
        "input_evidence_ids": ["evt-1"],
    },
    "experiment_registry.schema.json": {
        "schema_version": "1.0.0",
        "experiment_id": "exp-1",
        "registered_at": "2026-07-20T00:00:00Z",
        "hypothesis": "Passive spread capture has positive net edge in tight-spread regimes.",
        "falsification_criteria": "Net edge CI upper bound <= 0 on holdout.",
        "primary_metric": "expected_net_edge",
        "secondary_metrics": ["fill_rate"],
        "parameter_grid": {"quote_offset_ticks": [1, 2]},
        "included_market_archetypes": ["btc-threshold-24h-tight-spread-v1"],
        "excluded_market_archetypes": [],
        "training_window": {"start": "2026-01-01T00:00:00Z", "end": "2026-02-01T00:00:00Z"},
        "development_window": {"start": "2026-02-01T00:00:00Z", "end": "2026-03-01T00:00:00Z"},
        "holdout_window": {"start": "2026-03-01T00:00:00Z", "end": "2026-04-01T00:00:00Z"},
        "min_sample_size": 200,
        "diversity_requirements": "At least 20 distinct settlement events.",
        "multiple_comparison_correction": "benjamini_hochberg",
        "missing_data_treatment": "exclude_and_report",
        "is_exploratory": True,
        "versions": {
            "strategy_version": "1.0.0",
            "feature_version": "1.0.0",
            "expectancy_model_version": "1.0.0",
            "archetype_classifier_version": "1.0.0",
            "fill_model_version": "1.0.0",
        },
        "immutable_after": "2026-03-01T00:00:00Z",
    },
    "statistical-sufficiency.schema.json": {
        "schema_version": "1.0.0",
        "evaluation_id": "eval-1",
        "experiment_id": "exp-1",
        "decision_state": "INCONCLUSIVE",
        "sample_size": 50,
        "effective_sample_size": 12.5,
        "diversity_gate_passed": False,
        "clustering_unit": "market",
        "multiple_comparison_correction_applied": "benjamini_hochberg",
        "confidence_intervals": {"net_edge": {"low": -0.01, "high": 0.02}},
        "assigned_at": "2026-07-20T00:00:00Z",
        "assigned_by": "deterministic_evaluation_policy",
    },
}

INVALID_EXAMPLES: dict[str, dict[str, Any]] = {
    # Missing every required property.
    "risk_limits.schema.json": {"schema_version": "1.0.0"},
    # state is not one of the enum values.
    "order-state.schema.json": {
        "schema_version": "1.0.0",
        "order_id": "ord-1",
        "client_order_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "state": "NOT_A_REAL_STATE",
        "previous_state": None,
        "transitioned_at": "2026-07-20T00:00:00Z",
        "evidence_reference": "intent-evidence-1",
    },
    # contract_structure is not one of the enum values.
    "market_archetype.schema.json": {
        "schema_version": "1.0.0",
        "archetype_id": "a",
        "classifier_version": "1.0.0",
        "underlying_asset": "BTC",
        "contract_structure": "not_a_real_structure",
        "time_to_settlement_bucket": "12h-24h",
        "market_age_bucket": "0-1d",
        "time_of_day_bucket": "UTC-12",
        "day_of_week": "MON",
        "spread_regime": "tight",
        "depth_regime": "thin",
        "external_reference_volatility_regime": "low",
        "event_driven": False,
    },
    # signal_confidence out of [0, 1] range.
    "quote_expectancy.schema.json": {
        "schema_version": "1.0.0",
        "edge_model_version": "1.0.0",
        "quote_id": "quote-1",
        "signal_confidence": 1.5,
        "expected_fill_probability": 0.4,
        "expected_gross_spread_capture": 0.02,
        "expected_fee_cost": 0.001,
        "expected_adverse_selection": 0.002,
        "expected_inventory_cost": 0.001,
        "expected_settlement_risk": 0.001,
        "expected_cancel_reprice_cost": 0.0005,
        "expected_net_edge": 0.0135,
        "calibration_sample_size": 500,
        "calibration_confidence": 0.8,
    },
    # displayed_size_ahead_at_submission is negative.
    "queue-calibration.schema.json": {
        "schema_version": "1.0.0",
        "calibration_method_version": "1.0.0",
        "order_id": "ord-1",
        "displayed_size_ahead_at_submission": -5,
        "queue_position_lower_bound": 0.2,
        "queue_position_upper_bound": 0.5,
        "estimated_cancellations_ahead": 10,
        "fill_probability_conditional": 0.35,
    },
    # classification is not one of the enum values.
    "markout-toxicity.schema.json": {
        "schema_version": "1.0.0",
        "rules_version": "1.0.0",
        "fill_id": "fill-1",
        "realized_spread_by_horizon": [{"horizon_seconds": 1, "realized_spread": 0.01}],
        "classification": "NOT_A_REAL_CLASS",
        "input_evidence_ids": ["evt-1"],
    },
    # missing required "versions" object.
    "experiment_registry.schema.json": {
        "schema_version": "1.0.0",
        "experiment_id": "exp-1",
        "registered_at": "2026-07-20T00:00:00Z",
        "hypothesis": "x",
        "falsification_criteria": "x",
        "primary_metric": "expected_net_edge",
        "secondary_metrics": [],
        "parameter_grid": {},
        "included_market_archetypes": [],
        "excluded_market_archetypes": [],
        "training_window": {"start": "2026-01-01T00:00:00Z", "end": "2026-02-01T00:00:00Z"},
        "development_window": {"start": "2026-02-01T00:00:00Z", "end": "2026-03-01T00:00:00Z"},
        "holdout_window": {"start": "2026-03-01T00:00:00Z", "end": "2026-04-01T00:00:00Z"},
        "min_sample_size": 200,
        "diversity_requirements": "x",
        "multiple_comparison_correction": "x",
        "missing_data_treatment": "x",
        "is_exploratory": True,
        "immutable_after": "2026-03-01T00:00:00Z",
    },
    # decision_state is not one of the five allowed states.
    "statistical-sufficiency.schema.json": {
        "schema_version": "1.0.0",
        "evaluation_id": "eval-1",
        "experiment_id": "exp-1",
        "decision_state": "MAYBE",
        "sample_size": 50,
        "effective_sample_size": 12.5,
        "diversity_gate_passed": False,
        "clustering_unit": "market",
        "multiple_comparison_correction_applied": "benjamini_hochberg",
        "confidence_intervals": {},
        "assigned_at": "2026-07-20T00:00:00Z",
        "assigned_by": "deterministic_evaluation_policy",
    },
}


@pytest.mark.parametrize("name", sorted(VALID_EXAMPLES), ids=lambda n: n)
def test_minimal_conforming_example_validates(name: str) -> None:
    schema = _load_schema(name)
    Draft202012Validator(schema).validate(VALID_EXAMPLES[name])


@pytest.mark.parametrize("name", sorted(INVALID_EXAMPLES), ids=lambda n: n)
def test_deliberately_invalid_example_fails_validation(name: str) -> None:
    schema = _load_schema(name)
    validator = Draft202012Validator(schema)
    assert not validator.is_valid(INVALID_EXAMPLES[name])


def test_valid_and_invalid_examples_cover_every_schema() -> None:
    all_names = {p.name for p in _all_schema_files()}
    assert set(VALID_EXAMPLES) == all_names
    assert set(INVALID_EXAMPLES) == all_names
