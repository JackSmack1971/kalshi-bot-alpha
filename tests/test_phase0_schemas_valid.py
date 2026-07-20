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
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return data


def _all_schema_files() -> list[Path]:
    return sorted(SCHEMAS_DIR.glob("*.schema.json"))


def test_schemas_directory_has_expected_files() -> None:
    expected = {
        "risk-limits.schema.json",
        "order-state.schema.json",
        "market-archetype.schema.json",
        "quote-expectancy.schema.json",
        "queue-calibration.schema.json",
        "markout-toxicity.schema.json",
        "experiment-registration.schema.json",
        "statistical-sufficiency.schema.json",
        "trade-intent.schema.json",
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
    "risk-limits.schema.json": {
        "risk_limits_version": 1,
        "bankroll": {"paper_bankroll_usd": "1000.00"},
        "order": {"max_risk_per_order_usd": "5.00", "max_open_orders": 10},
        "market": {
            "max_exposure_per_market_usd": "25.00",
            "min_minutes_before_close": 30,
            "max_market_data_age_seconds": 2,
        },
        "portfolio": {
            "max_aggregate_exposure_usd": "100.00",
            "max_daily_paper_loss_usd": "25.00",
            "max_strategy_drawdown_pct": "5.0",
        },
        "scenario": {
            "correlation_groups_version": None,
            "max_correlated_scenario_loss_usd": "50.00",
            "max_single_market_liability_usd": "25.00",
        },
        "execution_budget": {
            "max_outstanding_request_age_seconds": 10,
            "order_rate_budget_per_minute": 30,
        },
        "kill_switch": {"enabled": True},
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
    "market-archetype.schema.json": {
        "schema_version": "1.0.0",
        "market_archetype_id": "btc-threshold-24h-tight-spread-v1",
        "classifier_version": "1.0.0",
        "underlying_asset": "BTC",
        "contract_structure": "threshold",
        "threshold_distance_bucket": "near",
        "time_to_settlement_bucket": "12h-24h",
        "market_age_bucket": "0-1d",
        "time_of_day_bucket": "UTC-12",
        "day_of_week_bucket": "MON",
        "spread_regime": "tight",
        "visible_depth_regime": "thin",
        "external_reference_volatility_regime": "low",
        "event_driven": False,
        "classified_at": "2026-07-20T00:00:00Z",
    },
    "quote-expectancy.schema.json": {
        "schema_version": "1.0.0",
        "quote_expectancy_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "intent_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "market_ticker": "KXBTC-24JUL20-T50000",
        "market_archetype_id": "btc-threshold-24h-tight-spread-v1",
        "queue_state_snapshot_id": "qss-1",
        "edge_model_version": "1.0.0",
        "signal_confidence": 0.6,
        "fill_probability": 0.4,
        "fill_probability_lower_bound": 0.3,
        "fill_probability_upper_bound": 0.5,
        "gross_spread_usd": "0.02",
        "fee_cost_usd": "0.001",
        "adverse_selection_usd": "0.002",
        "inventory_cost_usd": "0.001",
        "settlement_risk_usd": "0.001",
        "cancel_reprice_cost_usd": "0.0005",
        "expected_net_edge_usd": "0.0135",
        "calibration_method_version": "1.0.0",
        "calibration_sample_size": 500,
        "calibration_confidence": 0.8,
        "assumptions": ["Queue estimate is conservative."],
        "created_at": "2026-07-20T00:00:00Z",
        "quote_lifecycle": {
            "cancels_per_fill": 1.5,
            "reprices_per_fill": 0.5,
            "mutating_requests_per_unit_net_spread": 3.0,
            "median_quote_lifetime_seconds": 12.0,
            "pct_canceled_before_queue_advancement": 40.0,
            "opportunity_loss_from_throttling": 0.0,
        },
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
    "experiment-registration.schema.json": {
        "schema_version": "1.0.0",
        "experiment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
        "experiment_version": 1,
        "analysis_class": "exploratory",
        "hypothesis": "Passive spread capture has positive net edge in tight-spread regimes.",
        "falsification_criteria": ["Net edge CI upper bound <= 0 on holdout."],
        "primary_metric": "expected_net_edge",
        "secondary_metrics": ["fill_rate"],
        "parameter_grid": {"quote_offset_ticks": [1, 2]},
        "included_market_archetypes": ["btc-threshold-24h-tight-spread-v1"],
        "excluded_market_archetypes": [],
        "windows": {
            "training": {"start": "2026-01-01T00:00:00Z", "end": "2026-02-01T00:00:00Z"},
            "development": {"start": "2026-02-01T00:00:00Z", "end": "2026-03-01T00:00:00Z"},
            "holdout": {"start": "2026-03-01T00:00:00Z", "end": "2026-04-01T00:00:00Z"},
        },
        "minimum_evidence": {
            "min_calendar_days": 30,
            "min_eligible_quote_opportunities": 100,
            "min_submitted_quotes": 50,
            "min_fills": 20,
            "min_fills_per_included_archetype": 20,
            "min_distinct_settlement_events": 5,
            "min_adverse_selection_observations": 5,
            "min_clean_restarts": 1,
            "max_unresolved_data_gaps": 0,
            "min_effective_sample_size": 15,
        },
        "multiple_comparison_correction": {
            "method": "benjamini_hochberg",
            "declared_variant_count": 2,
        },
        "missing_data_treatment": "exclude_and_report",
        "frozen_versions": {
            "strategy_version": "1.0.0",
            "feature_version": "1.0.0",
            "expectancy_model_version": "1.0.0",
            "archetype_classifier_version": "1.0.0",
            "fill_model_version": "1.0.0",
        },
        "registered_at": "2026-07-20T00:00:00Z",
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
    "trade-intent.schema.json": {
        "schema_version": "1.0.0",
        "intent_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "strategy_id": "passive-spread-capture-v0",
        "strategy_version": "0.1.0",
        "market_ticker": "KXBTC-24JUL20-T50000",
        "market_archetype_id": "btc-threshold-24h-tight-spread-v1",
        "action": "place",
        "side": "yes",
        "limit_price_cents": 50,
        "desired_count": 1,
        "time_in_force": "good_till_canceled",
        "reason_codes": ["passive_spread_capture"],
        "feature_snapshot_id": "fs-1",
        "signal_confidence": 0.6,
        "expected_fill_probability": 0.4,
        "expected_queue_wait_seconds": 5,
        "expected_gross_spread_capture_usd": "0.02",
        "expected_fee_cost_usd": "0.001",
        "expected_adverse_selection_usd": "0.002",
        "expected_inventory_cost_usd": "0.001",
        "expected_settlement_risk_usd": "0.001",
        "expected_cancel_probability": 0.1,
        "expected_net_edge_usd": "0.0135",
        "edge_model_version": "1.0.0",
        "calibration_sample_size": 500,
        "calibration_confidence": 0.8,
        "created_at": "2026-07-20T00:00:00Z",
        "expiry_timestamp": "2026-07-20T00:05:00Z",
    },
}

INVALID_EXAMPLES: dict[str, dict[str, Any]] = {
    # Missing every required property.
    "risk-limits.schema.json": {"risk_limits_version": 1},
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
    "market-archetype.schema.json": {
        "schema_version": "1.0.0",
        "market_archetype_id": "a",
        "classifier_version": "1.0.0",
        "underlying_asset": "BTC",
        "contract_structure": "not_a_real_structure",
        "threshold_distance_bucket": "near",
        "time_to_settlement_bucket": "12h-24h",
        "market_age_bucket": "0-1d",
        "time_of_day_bucket": "UTC-12",
        "day_of_week_bucket": "MON",
        "spread_regime": "tight",
        "visible_depth_regime": "thin",
        "external_reference_volatility_regime": "low",
        "event_driven": False,
        "classified_at": "2026-07-20T00:00:00Z",
    },
    # signal_confidence out of [0, 1] range.
    "quote-expectancy.schema.json": {
        "schema_version": "1.0.0",
        "quote_expectancy_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "intent_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "market_ticker": "KXBTC-24JUL20-T50000",
        "market_archetype_id": "btc-threshold-24h-tight-spread-v1",
        "queue_state_snapshot_id": "qss-1",
        "edge_model_version": "1.0.0",
        "signal_confidence": 1.5,
        "fill_probability": 0.4,
        "fill_probability_lower_bound": 0.3,
        "fill_probability_upper_bound": 0.5,
        "gross_spread_usd": "0.02",
        "fee_cost_usd": "0.001",
        "adverse_selection_usd": "0.002",
        "inventory_cost_usd": "0.001",
        "settlement_risk_usd": "0.001",
        "cancel_reprice_cost_usd": "0.0005",
        "expected_net_edge_usd": "0.0135",
        "calibration_method_version": "1.0.0",
        "calibration_sample_size": 500,
        "calibration_confidence": 0.8,
        "assumptions": ["Queue estimate is conservative."],
        "created_at": "2026-07-20T00:00:00Z",
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
    # missing required "frozen_versions" object.
    "experiment-registration.schema.json": {
        "schema_version": "1.0.0",
        "experiment_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
        "experiment_version": 1,
        "analysis_class": "exploratory",
        "hypothesis": "x",
        "falsification_criteria": ["x"],
        "primary_metric": "expected_net_edge",
        "secondary_metrics": [],
        "parameter_grid": {},
        "included_market_archetypes": ["btc-threshold-24h-tight-spread-v1"],
        "excluded_market_archetypes": [],
        "windows": {
            "training": {"start": "2026-01-01T00:00:00Z", "end": "2026-02-01T00:00:00Z"},
            "development": {"start": "2026-02-01T00:00:00Z", "end": "2026-03-01T00:00:00Z"},
            "holdout": {"start": "2026-03-01T00:00:00Z", "end": "2026-04-01T00:00:00Z"},
        },
        "minimum_evidence": {
            "min_calendar_days": 30,
            "min_eligible_quote_opportunities": 100,
            "min_submitted_quotes": 50,
            "min_fills": 20,
            "min_fills_per_included_archetype": 20,
            "min_distinct_settlement_events": 5,
            "min_adverse_selection_observations": 5,
            "min_clean_restarts": 1,
            "max_unresolved_data_gaps": 0,
            "min_effective_sample_size": 15,
        },
        "multiple_comparison_correction": {
            "method": "benjamini_hochberg",
            "declared_variant_count": 2,
        },
        "missing_data_treatment": "x",
        "registered_at": "2026-07-20T00:00:00Z",
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
    # action is not one of the enum values.
    "trade-intent.schema.json": {
        "schema_version": "1.0.0",
        "intent_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "strategy_id": "passive-spread-capture-v0",
        "strategy_version": "0.1.0",
        "market_ticker": "KXBTC-24JUL20-T50000",
        "market_archetype_id": "btc-threshold-24h-tight-spread-v1",
        "action": "not_a_real_action",
        "side": "yes",
        "limit_price_cents": 50,
        "desired_count": 1,
        "time_in_force": "good_till_canceled",
        "reason_codes": ["passive_spread_capture"],
        "feature_snapshot_id": "fs-1",
        "signal_confidence": 0.6,
        "expected_fill_probability": 0.4,
        "expected_queue_wait_seconds": 5,
        "expected_gross_spread_capture_usd": "0.02",
        "expected_fee_cost_usd": "0.001",
        "expected_adverse_selection_usd": "0.002",
        "expected_inventory_cost_usd": "0.001",
        "expected_settlement_risk_usd": "0.001",
        "expected_cancel_probability": 0.1,
        "expected_net_edge_usd": "0.0135",
        "edge_model_version": "1.0.0",
        "calibration_sample_size": 500,
        "calibration_confidence": 0.8,
        "created_at": "2026-07-20T00:00:00Z",
        "expiry_timestamp": "2026-07-20T00:05:00Z",
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
