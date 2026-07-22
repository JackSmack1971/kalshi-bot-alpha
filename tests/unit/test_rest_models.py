"""Tests for kalshi_bot.rest.models (Phase 1 PR 4).

No network, filesystem, or credential material anywhere in this file.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

from kalshi_bot.rest.models import (
    DailyOpenClose,
    ExchangeIndexStatus,
    ExchangeStatus,
    MaintenanceWindow,
    MarketListPage,
    MarketSummary,
    StandardHoursBlock,
    _ExchangeScheduleEnvelope,
)

# -- MarketSummary -----------------------------------------------------


def test_market_summary_requires_only_ticker() -> None:
    market = MarketSummary.model_validate({"ticker": "KXBTC-25JAN01"})
    assert market.ticker == "KXBTC-25JAN01"
    assert market.event_ticker is None
    assert market.title is None


def test_market_summary_missing_ticker_raises() -> None:
    with pytest.raises(ValidationError):
        MarketSummary.model_validate({"event_ticker": "KXBTC-25JAN01"})


def test_market_summary_rejects_wrong_typed_ticker() -> None:
    with pytest.raises(ValidationError):
        MarketSummary.model_validate({"ticker": 12345})


def test_market_summary_rejects_wrong_typed_can_close_early() -> None:
    # strict=True: a string is never silently coerced into a bool field.
    with pytest.raises(ValidationError):
        MarketSummary.model_validate({"ticker": "KXBTC-25JAN01", "can_close_early": "true"})


def test_market_summary_accepts_documented_example_fields() -> None:
    payload = {
        "ticker": "KXBTC-25JAN01",
        "event_ticker": "KXBTC-25JAN01-EVT",
        "yes_sub_title": "Yes",
        "no_sub_title": "No",
        "created_time": "2023-11-07T05:31:56Z",
        "updated_time": "2023-11-07T05:31:56Z",
        "open_time": "2023-11-07T05:31:56Z",
        "close_time": "2023-11-07T05:31:56Z",
        "yes_bid_dollars": "0.5600",
        "yes_ask_dollars": "0.5700",
        "no_bid_dollars": "0.4300",
        "no_ask_dollars": "0.4400",
        "last_price_dollars": "0.5600",
        "volume_fp": "10.00",
        "volume_24h_fp": "10.00",
        "can_close_early": True,
        "open_interest_fp": "10.00",
        "notional_value_dollars": "0.5600",
        "previous_price_dollars": "0.5500",
        "title": "Will BTC close above $100k?",
        "subtitle": "By Jan 1",
        "expiration_time": "2023-11-07T05:31:56Z",
        "expected_expiration_time": "2023-11-07T05:31:56Z",
        "liquidity_dollars": "1000.00",
    }
    market = MarketSummary.model_validate(payload)
    assert market.ticker == "KXBTC-25JAN01"
    assert market.title == "Will BTC close above $100k?"
    assert market.can_close_early is True
    assert market.yes_bid_dollars == "0.5600"


def test_market_summary_tolerates_unknown_upstream_fields() -> None:
    market = MarketSummary.model_validate(
        {"ticker": "KXBTC-25JAN01", "a_future_kalshi_field_not_yet_modeled": "surprise"}
    )
    assert market.ticker == "KXBTC-25JAN01"
    assert not hasattr(market, "a_future_kalshi_field_not_yet_modeled")


def test_market_summary_has_no_status_field() -> None:
    """``status`` is not a documented GET /markets response field (only a
    request-side filter enum of the same name exists); it must never be
    invented here. See kalshi_bot.rest.models.MarketSummary's docstring."""
    assert "status" not in MarketSummary.model_fields


def test_market_summary_is_frozen() -> None:
    market = MarketSummary.model_validate({"ticker": "KXBTC-25JAN01"})
    with pytest.raises(ValidationError):
        market.ticker = "OTHER"


# -- MarketListPage ------------------------------------------------------


def test_market_list_page_requires_cursor() -> None:
    with pytest.raises(ValidationError):
        MarketListPage.model_validate({"markets": []})


def test_market_list_page_allows_empty_cursor_and_empty_markets() -> None:
    page = MarketListPage.model_validate({"markets": [], "cursor": ""})
    assert page.markets == []
    assert page.cursor == ""


def test_market_list_page_rejects_non_string_cursor() -> None:
    """This is this client's definition of a "malformed cursor": a
    non-string value in the decoded JSON body. strict=True rejects it
    at the type-validation layer, before any pagination logic runs."""
    with pytest.raises(ValidationError):
        MarketListPage.model_validate({"markets": [], "cursor": 12345})


def test_market_list_page_parses_nested_markets() -> None:
    page = MarketListPage.model_validate(
        {
            "markets": [{"ticker": "T1"}, {"ticker": "T2"}],
            "cursor": "abc",
        }
    )
    assert [m.ticker for m in page.markets] == ["T1", "T2"]


# -- ExchangeStatus / ExchangeIndexStatus --------------------------------


def test_exchange_status_requires_exchange_active_and_trading_active() -> None:
    with pytest.raises(ValidationError):
        ExchangeStatus.model_validate({"trading_active": True})
    with pytest.raises(ValidationError):
        ExchangeStatus.model_validate({"exchange_active": True})


def test_exchange_status_optional_fields_default_to_none() -> None:
    status = ExchangeStatus.model_validate({"exchange_active": True, "trading_active": False})
    assert status.exchange_active is True
    assert status.trading_active is False
    assert status.intra_exchange_transfers_active is None
    assert status.exchange_estimated_resume_time is None
    assert status.exchange_index_statuses is None


def test_exchange_status_rejects_string_for_boolean_field() -> None:
    with pytest.raises(ValidationError):
        ExchangeStatus.model_validate({"exchange_active": "true", "trading_active": True})


def test_exchange_status_does_not_synthesize_business_state() -> None:
    """No computed "healthy"/"degraded" field exists on this model."""
    fields = set(ExchangeStatus.model_fields)
    assert "healthy" not in fields
    assert "degraded" not in fields
    assert "status" not in fields


def test_exchange_status_parses_documented_example() -> None:
    payload = {
        "exchange_active": True,
        "trading_active": True,
        "intra_exchange_transfers_active": True,
        "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",
        "exchange_index_statuses": [
            {
                "exchange_index": 0,
                "exchange_active": True,
                "trading_active": True,
                "intra_exchange_transfers_active": True,
            }
        ],
    }
    status = ExchangeStatus.model_validate(payload)
    assert status.exchange_active is True
    assert status.exchange_index_statuses is not None
    assert status.exchange_index_statuses[0].exchange_index == 0


def test_exchange_index_status_requires_all_four_fields() -> None:
    with pytest.raises(ValidationError):
        ExchangeIndexStatus.model_validate({"exchange_index": 0, "exchange_active": True})


# -- ExchangeSchedule / envelope ------------------------------------------


def test_exchange_schedule_envelope_requires_schedule_key() -> None:
    with pytest.raises(ValidationError):
        _ExchangeScheduleEnvelope.model_validate({})


def test_exchange_schedule_defaults_to_empty_lists() -> None:
    envelope = _ExchangeScheduleEnvelope.model_validate({"schedule": {}})
    assert envelope.schedule.standard_hours == []
    assert envelope.schedule.maintenance_windows == []


def test_exchange_schedule_parses_documented_example() -> None:
    payload = {
        "schedule": {
            "standard_hours": [
                {
                    "start_time": "2023-11-07T05:31:56Z",
                    "end_time": "2023-11-07T05:31:56Z",
                    "monday": [{"open_time": "09:00", "close_time": "17:00"}],
                    "tuesday": [{"open_time": "09:00", "close_time": "17:00"}],
                    "wednesday": [{"open_time": "09:00", "close_time": "17:00"}],
                    "thursday": [{"open_time": "09:00", "close_time": "17:00"}],
                    "friday": [{"open_time": "09:00", "close_time": "17:00"}],
                    "saturday": [],
                    "sunday": [],
                }
            ],
            "maintenance_windows": [
                {
                    "start_datetime": "2023-11-07T05:31:56Z",
                    "end_datetime": "2023-11-07T06:31:56Z",
                }
            ],
        }
    }
    envelope = _ExchangeScheduleEnvelope.model_validate(payload)
    schedule = envelope.schedule
    assert len(schedule.standard_hours) == 1
    assert schedule.standard_hours[0].monday == [DailyOpenClose(open_time="09:00", close_time="17:00")]
    assert schedule.standard_hours[0].saturday == []
    assert len(schedule.maintenance_windows) == 1
    assert schedule.maintenance_windows[0].start_datetime == "2023-11-07T05:31:56Z"


def test_standard_hours_block_missing_weekday_raises() -> None:
    with pytest.raises(ValidationError):
        StandardHoursBlock.model_validate(
            {
                "start_time": "2023-11-07T05:31:56Z",
                "end_time": "2023-11-07T05:31:56Z",
                "monday": [],
                "tuesday": [],
                "wednesday": [],
                "thursday": [],
                "friday": [],
                "saturday": [],
                # sunday missing
            }
        )


def test_maintenance_window_requires_both_fields() -> None:
    with pytest.raises(ValidationError):
        MaintenanceWindow.model_validate({"start_datetime": "2023-11-07T05:31:56Z"})


# -- extra="ignore" tolerance, shared across all response models --------


@pytest.mark.parametrize(
    ("model_cls", "payload"),
    [
        (ExchangeStatus, {"exchange_active": True, "trading_active": True}),
        (MarketSummary, {"ticker": "T1"}),
        (MarketListPage, {"markets": [], "cursor": ""}),
    ],
)
def test_models_ignore_unknown_upstream_fields(
    model_cls: type[BaseModel], payload: dict[str, object]
) -> None:
    extended = dict(payload, some_future_field="unexpected-value")
    instance = model_cls.model_validate(extended)
    assert not hasattr(instance, "some_future_field")
