"""External Kalshi WebSocket response models (Phase 1 PR 5).

Grounded in the local official Kalshi documentation:

- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-market-ticker-e3bb8f9b.md``
- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-public-trades-6774a251.md``
- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-websocket-connection-e95d7b48.md``

Two kinds of model live here, mirroring ``kalshi_bot.rest.models``'s
split between exported and internal-only types:

- **Public, exported** data models: :class:`TickerUpdate` and
  :class:`TradeUpdate` -- the only two typed events this client's
  public API (``subscribe_ticker``/``subscribe_trades``) ever yields.
- **Internal, non-exported** wire-envelope models (the leading
  underscore, not in ``__all__``): every message this client can
  receive over the socket -- ``ticker``, ``trade``, ``subscribed``,
  ``unsubscribed``, ``ok``, ``error`` -- is validated against a
  ``{"id"?, "type", "sid"?, "msg"?}``-shaped envelope in
  ``kalshi_bot.ws.normalizer`` before its inner payload is trusted.
  These envelope models are private to this package: only
  ``kalshi_bot.ws.normalizer`` constructs them.

Deliberately **absent**: any ``orderbook_delta`` model of any kind.
This client never subscribes to, parses, or represents order-book
data -- see ``.claude/rules/kalshi-transport-safety.md`` and
``docs/PHASE1_PLAN.md`` PR 5's forbidden-scope list.

Every model here is an **external response** model: it describes data
Kalshi's demo WebSocket sends to this client, never a caller-supplied
command body. ``extra="ignore"`` is used everywhere so a field Kalshi
adds upstream in the future cannot break this client. Fields this
client's *behavior* depends on (market/trade identifiers) are required;
every other documented field is optional and typed to match the
documented JSON shape exactly (``strict=True``), mirroring
``kalshi_bot.rest.models``'s conventions.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

__all__ = ["TickerUpdate", "TradeUpdate"]


class _KalshiWsResponseModel(BaseModel):
    """Base for every Kalshi WebSocket response model in this module.

    See ``kalshi_bot.rest.models._KalshiResponseModel`` for the
    rationale behind each ``ConfigDict`` option; identical here.
    """

    model_config = ConfigDict(
        frozen=True, extra="ignore", strict=True, populate_by_name=True
    )


class TickerUpdate(_KalshiWsResponseModel):
    """The ``msg`` payload of a ``type: "ticker"`` WebSocket message.

    Only ``market_ticker`` is required: it is the sole field this
    client's own logic depends on (routing/identification). Every other
    field in the grounding doc's single documented example is modeled
    as optional, matching :class:`~kalshi_bot.rest.models.MarketSummary`'s
    same "only what behavior depends on is required" convention -- no
    field is invented beyond what the grounding doc's example shows.
    """

    market_ticker: str

    market_id: str | None = None
    price_dollars: str | None = None
    yes_bid_dollars: str | None = None
    yes_ask_dollars: str | None = None
    volume_fp: str | None = None
    open_interest_fp: str | None = None
    dollar_volume: int | None = None
    dollar_open_interest: int | None = None
    yes_bid_size_fp: str | None = None
    yes_ask_size_fp: str | None = None
    last_trade_size_fp: str | None = None
    ts: int | None = None
    ts_ms: int | None = None
    time: str | None = None


class TradeUpdate(_KalshiWsResponseModel):
    """The ``msg`` payload of a ``type: "trade"`` WebSocket message.

    ``trade_id`` and ``market_ticker`` are required: both are the
    identifiers this client's own logic depends on. Every other field
    in the grounding doc's single documented example is optional, for
    the same reason given on :class:`TickerUpdate`.
    """

    trade_id: str
    market_ticker: str

    yes_price_dollars: str | None = None
    no_price_dollars: str | None = None
    count_fp: str | None = None
    taker_side: str | None = None
    ts: int | None = None
    ts_ms: int | None = None


# -- Internal wire envelopes (not exported; used only by normalizer.py) -----


class _TickerFrame(_KalshiWsResponseModel):
    """The full ``{"type": "ticker", "sid": ..., "msg": {...}}`` envelope."""

    type: Literal["ticker"]
    sid: int
    msg: TickerUpdate


class _TradeFrame(_KalshiWsResponseModel):
    """The full ``{"type": "trade", "sid": ..., "msg": {...}}`` envelope."""

    type: Literal["trade"]
    sid: int
    msg: TradeUpdate


class _SubscribedMsg(_KalshiWsResponseModel):
    """The inner ``msg`` object of a ``subscribed`` response."""

    channel: str
    sid: int


class _SubscribedFrame(_KalshiWsResponseModel):
    """The full ``subscribed`` response envelope.

    Grounded in
    ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-websockets-websocket-connection-e95d7b48.md``'s
    documented ``{"id": 1, "type": "subscribed", "msg": {"channel": ...,
    "sid": ...}}`` shape.
    """

    id: int
    type: Literal["subscribed"]
    msg: _SubscribedMsg


class _UnsubscribedFrame(_KalshiWsResponseModel):
    """The full ``unsubscribed`` response envelope.

    Grounded in the same doc's ``{"id": 102, "sid": 2, "seq": 7,
    "type": "unsubscribed"}`` shape -- this response documented has no
    ``msg`` object.
    """

    id: int | None = None
    sid: int | None = None
    seq: int | None = None
    type: Literal["unsubscribed"]


class _OkFrame(_KalshiWsResponseModel):
    """The full ``ok`` response envelope.

    Grounded in the same doc's two documented ``ok`` shapes (a
    subscription-update confirmation with an object ``msg``, and a
    ``list_subscriptions`` response with an array ``msg``). This client
    never issues either command, so ``msg`` is modeled loosely
    (``Any``) and is never interpreted further -- only the envelope's
    presence is logged.
    """

    id: int | None = None
    sid: int | None = None
    seq: int | None = None
    type: Literal["ok"]
    msg: Any = None


class _ErrorMsg(_KalshiWsResponseModel):
    """The inner ``msg`` object of an ``error`` response."""

    code: int
    msg: str


class _ErrorFrame(_KalshiWsResponseModel):
    """The full ``error`` response envelope.

    Grounded in the same doc's ``{"id": 123, "type": "error", "msg":
    {"code": 6, "msg": "Already subscribed"}}`` shape.
    """

    id: int | None = None
    type: Literal["error"]
    msg: _ErrorMsg
