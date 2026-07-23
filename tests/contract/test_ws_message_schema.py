"""Contract tests: Kalshi WebSocket message schemas match the
documented shapes exactly (Phase 1 PR 5).

Grounded in the local official Kalshi documentation:

- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-market-ticker-e3bb8f9b.md``
- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-public-trades-6774a251.md``
- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-websocket-connection-e95d7b48.md``

Explicitly proves that ``orderbook_delta`` (and every other channel this
client never subscribes to) is treated as an unknown channel, never
confused with a known type -- see
``.claude/rules/kalshi-transport-safety.md`` and ``docs/PHASE1_PLAN.md``
PR 5's forbidden-scope list.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from kalshi_bot.ws.models import TickerUpdate, TradeUpdate
from kalshi_bot.ws.normalizer import (
    ErrorFrame,
    MalformedFrame,
    OkFrame,
    SubscribedFrame,
    UnknownChannelFrame,
    UnsubscribedFrame,
    parse_frame,
)

# -- Exact documented example payloads ----------------------------------------

_DOCUMENTED_TICKER_FRAME: dict[str, Any] = {
    "type": "ticker",
    "sid": 11,
    "msg": {
        "market_ticker": "FED-23DEC-T3.00",
        "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
        "price_dollars": "0.480",
        "yes_bid_dollars": "0.450",
        "yes_ask_dollars": "0.530",
        "volume_fp": "33896.00",
        "open_interest_fp": "20422.00",
        "dollar_volume": 16948,
        "dollar_open_interest": 10211,
        "yes_bid_size_fp": "300.00",
        "yes_ask_size_fp": "150.00",
        "last_trade_size_fp": "25.00",
        "ts": 1669149841,
        "ts_ms": 1669149841000,
        "time": "2022-11-22T20:44:01Z",
    },
}

_DOCUMENTED_TRADE_FRAME: dict[str, Any] = {
    "type": "trade",
    "sid": 11,
    "msg": {
        "trade_id": "d91bc706-ee49-470d-82d8-11418bda6fed",
        "market_ticker": "HIGHNY-22DEC23-B53.5",
        "yes_price_dollars": "0.360",
        "no_price_dollars": "0.640",
        "count_fp": "136.00",
        "taker_side": "no",
        "ts": 1669149841,
        "ts_ms": 1669149841000,
    },
}


def test_documented_ticker_frame_parses_to_ticker_update() -> None:
    result = parse_frame(json.dumps(_DOCUMENTED_TICKER_FRAME))
    assert isinstance(result, TickerUpdate)
    assert result.market_ticker == "FED-23DEC-T3.00"
    assert result.price_dollars == "0.480"
    assert result.yes_bid_dollars == "0.450"
    assert result.yes_ask_dollars == "0.530"
    assert result.dollar_volume == 16948
    assert result.ts_ms == 1669149841000


def test_documented_trade_frame_parses_to_trade_update() -> None:
    result = parse_frame(json.dumps(_DOCUMENTED_TRADE_FRAME))
    assert isinstance(result, TradeUpdate)
    assert result.trade_id == "d91bc706-ee49-470d-82d8-11418bda6fed"
    assert result.market_ticker == "HIGHNY-22DEC23-B53.5"
    assert result.taker_side == "no"


def test_ticker_frame_bytes_input_is_accepted() -> None:
    result = parse_frame(json.dumps(_DOCUMENTED_TICKER_FRAME).encode("utf-8"))
    assert isinstance(result, TickerUpdate)


def test_ticker_update_pydantic_model_matches_documented_fields_directly() -> None:
    update = TickerUpdate.model_validate(_DOCUMENTED_TICKER_FRAME["msg"])
    assert update.market_ticker == "FED-23DEC-T3.00"


def test_trade_update_pydantic_model_matches_documented_fields_directly() -> None:
    update = TradeUpdate.model_validate(_DOCUMENTED_TRADE_FRAME["msg"])
    assert update.trade_id == "d91bc706-ee49-470d-82d8-11418bda6fed"


# -- Control-frame shapes -------------------------------------------------------


def test_subscribed_response_parses() -> None:
    frame = {"id": 1, "type": "subscribed", "msg": {"channel": "ticker", "sid": 1}}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, SubscribedFrame)
    assert result.channel == "ticker"
    assert result.sid == 1


def test_unsubscribed_response_parses() -> None:
    frame = {"id": 102, "sid": 2, "seq": 7, "type": "unsubscribed"}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, UnsubscribedFrame)
    assert result.sid == 2


def test_ok_response_parses() -> None:
    frame = {
        "id": 123,
        "sid": 456,
        "seq": 222,
        "type": "ok",
        "msg": {"market_tickers": ["MARKET-1", "MARKET-2", "MARKET-3"]},
    }
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, OkFrame)


def test_ok_response_with_list_msg_parses() -> None:
    """The documented ``list_subscriptions`` response's ``msg`` is an
    array, not an object -- both documented ``ok`` shapes must parse."""
    frame = {
        "id": 3,
        "type": "ok",
        "msg": [
            {"channel": "orderbook_delta", "sid": 1},
            {"channel": "ticker", "sid": 2},
            {"channel": "fill", "sid": 3},
        ],
    }
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, OkFrame)


def test_error_response_parses() -> None:
    frame = {"id": 123, "type": "error", "msg": {"code": 6, "msg": "Already subscribed"}}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, ErrorFrame)
    assert result.code == 6
    assert result.message == "Already subscribed"


def test_error_frame_missing_code_is_malformed() -> None:
    frame = {"id": 1, "type": "error", "msg": {"msg": "boom"}}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, MalformedFrame)


# -- Unknown channel, explicitly including orderbook_delta --------------------


@pytest.mark.parametrize(
    "frame_type",
    [
        "orderbook_delta",
        "orderbook_snapshot",
        "fill",
        "market_positions",
        "communications",
        "order_group_updates",
        "market_lifecycle_v2",
        "multivariate_market_lifecycle",
        "multivariate",
        "cfbenchmarks_value",
        "pyth_value",
        "totally_made_up_type",
    ],
)
def test_every_non_ticker_trade_channel_is_treated_as_unknown(frame_type: str) -> None:
    frame = {"type": frame_type, "sid": 1, "msg": {}}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, UnknownChannelFrame)
    assert result.frame_type == frame_type


def test_orderbook_delta_is_never_confused_with_a_known_type() -> None:
    frame = {
        "type": "orderbook_delta",
        "sid": 1,
        "msg": {"market_ticker": "KXBTC-25JAN01", "client_order_id": "abc"},
    }
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, UnknownChannelFrame)
    assert not isinstance(result, TickerUpdate)
    assert not isinstance(result, TradeUpdate)


# -- Malformed frames ------------------------------------------------------------


def test_invalid_json_is_malformed() -> None:
    result = parse_frame("not json at all {{{")
    assert isinstance(result, MalformedFrame)


def test_non_object_json_is_malformed() -> None:
    result = parse_frame(json.dumps([1, 2, 3]))
    assert isinstance(result, MalformedFrame)


def test_missing_type_field_is_malformed() -> None:
    result = parse_frame(json.dumps({"sid": 1, "msg": {}}))
    assert isinstance(result, MalformedFrame)


def test_non_string_type_field_is_malformed() -> None:
    result = parse_frame(json.dumps({"type": 5, "sid": 1, "msg": {}}))
    assert isinstance(result, MalformedFrame)


def test_empty_string_type_field_is_malformed() -> None:
    result = parse_frame(json.dumps({"type": "", "sid": 1, "msg": {}}))
    assert isinstance(result, MalformedFrame)


def test_ticker_frame_missing_required_market_ticker_is_malformed() -> None:
    frame = {"type": "ticker", "sid": 1, "msg": {"price_dollars": "0.5"}}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, MalformedFrame)


def test_trade_frame_missing_required_fields_is_malformed() -> None:
    frame = {"type": "trade", "sid": 1, "msg": {"market_ticker": "KXBTC-25JAN01"}}
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, MalformedFrame)


def test_ticker_frame_wrong_typed_field_is_malformed() -> None:
    frame = {
        "type": "ticker",
        "sid": 1,
        "msg": {"market_ticker": "KXBTC-25JAN01", "dollar_volume": "not-an-int"},
    }
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, MalformedFrame)


def test_invalid_utf8_bytes_is_malformed() -> None:
    result = parse_frame(b"\xff\xfe\xfd")
    assert isinstance(result, MalformedFrame)


def test_unknown_response_field_is_tolerated_on_ticker() -> None:
    frame = dict(_DOCUMENTED_TICKER_FRAME)
    frame["msg"] = dict(frame["msg"])
    frame["msg"]["a_brand_new_field_kalshi_added"] = "surprise"
    result = parse_frame(json.dumps(frame))
    assert isinstance(result, TickerUpdate)
