"""Contract tests: kalshi_bot.rest.models against the local grounding docs.

Grounded in:
- docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-market-get-markets-dde969d3.md
- docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-exchange-get-exchange-status-c8224b5.md
- docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-exchange-get-exchange-schedule-284531aa.md

These tests parse literal example payloads copied from those docs (not
live network responses) and prove the required/optional shape this
client's models commit to matches what the docs actually document as
``required``.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from kalshi_bot.rest.models import (
    ExchangeStatus,
    MarketListPage,
    MarketSummary,
    _ExchangeScheduleEnvelope,
)

# -- GET /markets: doc marks "markets" and "cursor" required; this client's
# -- binding pagination-termination decision treats an absent/null cursor
# -- as a valid terminal-page signal instead, per
# -- KalshiDemoRestClient.list_markets's documented tri-state contract.


def test_get_markets_envelope_cursor_defaults_to_none_when_absent() -> None:
    """Deliberate, documented departure from the raw doc's ``required``
    marking on ``cursor``: this client treats an absent (or explicit
    JSON ``null``) cursor as equivalent to an empty-string cursor --
    both mean "no further page" -- rather than a validation failure."""
    page = MarketListPage.model_validate({"markets": []})
    assert page.cursor is None


def test_get_markets_envelope_markets_required_and_rejects_when_absent() -> None:
    """The doc marks "markets" required and this client enforces that:
    a page body missing the ``markets`` key fails closed with a
    validation error rather than silently defaulting to an empty page,
    which would make a malformed/truncated response indistinguishable
    from a legitimately empty one."""
    with pytest.raises(ValidationError):
        MarketListPage.model_validate({"cursor": ""})


def test_market_object_documented_example_round_trips() -> None:
    """The literal example market object from the grounding doc's 200
    response, minus keys this client does not model (multivariate-event
    and pricing-structure fields out of scope for Phase 1 read-only
    discovery)."""
    example = {
        "ticker": "<string>",
        "event_ticker": "<string>",
        "yes_sub_title": "<string>",
        "no_sub_title": "<string>",
        "created_time": "2023-11-07T05:31:56Z",
        "updated_time": "2023-11-07T05:31:56Z",
        "open_time": "2023-11-07T05:31:56Z",
        "close_time": "2023-11-07T05:31:56Z",
        "yes_bid_dollars": "0.5600",
        "yes_ask_dollars": "0.5600",
        "no_bid_dollars": "0.5600",
        "no_ask_dollars": "0.5600",
        "last_price_dollars": "0.5600",
        "volume_fp": "10.00",
        "volume_24h_fp": "10.00",
        "can_close_early": True,
        "open_interest_fp": "10.00",
        "notional_value_dollars": "0.5600",
        "previous_price_dollars": "0.5600",
        "title": "<string>",
        "subtitle": "<string>",
        "expected_expiration_time": "2023-11-07T05:31:56Z",
        "expiration_time": "2023-11-07T05:31:56Z",
        "liquidity_dollars": "0.5600",
    }
    market = MarketSummary.model_validate(example)
    assert market.ticker == "<string>"
    assert market.can_close_early is True


def test_market_object_has_no_status_field_per_grounding_doc() -> None:
    """A corpus-wide grep for '"status"' near "market" in
    docs-dev/kalshi-docs-pack/docs/ finds only the GET /markets
    *request-side* filter parameter, never a response field on the
    market object itself (the example response body in the grounding
    doc never includes a "status" key). This client must not invent
    one."""
    assert "status" not in MarketSummary.model_fields


# -- GET /exchange/status: only exchange_active/trading_active required --


def test_exchange_status_required_fields_match_doc() -> None:
    required = {
        name
        for name, field in ExchangeStatus.model_fields.items()
        if field.is_required()
    }
    assert required == {"exchange_active", "trading_active"}


def test_exchange_status_documented_error_statuses_are_retryable() -> None:
    """The grounding doc lists 200/500/503/504 as this endpoint's
    possible response statuses. The 500/503/504 set is exactly what
    kalshi_bot.rest.client._RETRYABLE_STATUS_CODES treats as
    server-side-transient (plus 429, grounded separately in the
    rate-limits doc)."""
    from kalshi_bot.rest.client import _RETRYABLE_STATUS_CODES

    assert {500, 503, 504} <= _RETRYABLE_STATUS_CODES


# -- GET /exchange/schedule: only "schedule" itself is required ----------


def test_exchange_schedule_envelope_required_fields_match_doc() -> None:
    required = {
        name
        for name, field in _ExchangeScheduleEnvelope.model_fields.items()
        if field.is_required()
    }
    assert required == {"schedule"}
