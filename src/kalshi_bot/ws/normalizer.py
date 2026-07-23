"""Pure WebSocket frame parsing (Phase 1 PR 5).

Deliberately **not** an order-book builder: this module has no
``orderbook_delta`` handling of any kind, and no state at all -- every
function here is a pure, side-effect-free transform from one raw
decoded (or undecodable) WebSocket frame to exactly one typed result.
It performs no I/O, holds no connection state, and does not know about
subscriptions, reconnects, or channels beyond the frame directly in
front of it.

:func:`parse_frame` is the single entry point. It never raises for a
malformed or unrecognized frame -- it always returns a typed result
instead (see :data:`FrameParseResult`), so callers (only
``kalshi_bot.ws.client``) can log-and-drop malformed input and
unrecognized channels without any ``try``/``except`` around parsing.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from pydantic import ValidationError

from kalshi_bot.ws.models import (
    TickerUpdate,
    TradeUpdate,
    _ErrorFrame,
    _OkFrame,
    _SubscribedFrame,
    _TickerFrame,
    _TradeFrame,
    _UnsubscribedFrame,
)

__all__ = [
    "FrameParseResult",
    "MalformedFrame",
    "UnknownChannelFrame",
    "SubscribedFrame",
    "UnsubscribedFrame",
    "OkFrame",
    "ErrorFrame",
    "parse_frame",
]


@dataclass(frozen=True, slots=True)
class MalformedFrame:
    """A frame that could not be decoded or failed schema validation.

    Covers: invalid UTF-8 bytes, invalid JSON, a JSON value that is not
    an object, a missing/non-string ``type`` field, and a recognized
    ``type`` whose ``msg``/envelope shape fails Kalshi's documented
    schema. ``reason`` is a short, fixed, non-secret classification
    string -- never the raw frame content (which comes from the network
    and could be arbitrarily large or, in a compromised-transport
    scenario, adversarial).
    """

    reason: str


@dataclass(frozen=True, slots=True)
class UnknownChannelFrame:
    """A well-formed frame whose ``type`` is not one this client recognizes.

    Covers every ``type`` value other than
    ``ticker``/``trade``/``subscribed``/``unsubscribed``/``ok``/``error``
    -- explicitly including ``orderbook_delta`` and any other private or
    public channel this client never subscribes to. Never treated as a
    known type and never forwarded to a caller as a
    :class:`~kalshi_bot.ws.models.TickerUpdate` or
    :class:`~kalshi_bot.ws.models.TradeUpdate`.
    """

    frame_type: str


@dataclass(frozen=True, slots=True)
class SubscribedFrame:
    """A parsed ``subscribed`` response (internal correlation/logging only)."""

    channel: str
    sid: int


@dataclass(frozen=True, slots=True)
class UnsubscribedFrame:
    """A parsed ``unsubscribed`` response (internal logging only)."""

    sid: int | None


@dataclass(frozen=True, slots=True)
class OkFrame:
    """A parsed ``ok`` response (internal logging only; ``msg`` is not
    interpreted -- see :class:`~kalshi_bot.ws.models._OkFrame`)."""


@dataclass(frozen=True, slots=True)
class ErrorFrame:
    """A parsed ``error`` response (internal logging only)."""

    code: int
    message: str


FrameParseResult = (
    TickerUpdate
    | TradeUpdate
    | SubscribedFrame
    | UnsubscribedFrame
    | OkFrame
    | ErrorFrame
    | UnknownChannelFrame
    | MalformedFrame
)


def parse_frame(raw: str | bytes) -> FrameParseResult:
    """Parse one raw WebSocket frame into a typed :data:`FrameParseResult`.

    Never raises. A frame this function cannot decode or validate
    against Kalshi's documented shape always yields
    :class:`MalformedFrame`, never a partially-populated model and
    never a propagated exception.
    """
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return MalformedFrame("frame is not valid UTF-8")
    else:
        text = raw

    try:
        decoded = json.loads(text)
    except (ValueError, TypeError):
        return MalformedFrame("frame is not valid JSON")

    if not isinstance(decoded, dict):
        return MalformedFrame("frame is not a JSON object")

    frame_type = decoded.get("type")
    if not isinstance(frame_type, str) or not frame_type:
        return MalformedFrame("frame is missing a nonempty string 'type' field")

    if frame_type == "ticker":
        try:
            envelope = _TickerFrame.model_validate(decoded)
        except ValidationError:
            return MalformedFrame("ticker frame failed schema validation")
        return envelope.msg

    if frame_type == "trade":
        try:
            trade_envelope = _TradeFrame.model_validate(decoded)
        except ValidationError:
            return MalformedFrame("trade frame failed schema validation")
        return trade_envelope.msg

    if frame_type == "subscribed":
        try:
            subscribed_envelope = _SubscribedFrame.model_validate(decoded)
        except ValidationError:
            return MalformedFrame("subscribed frame failed schema validation")
        return SubscribedFrame(
            channel=subscribed_envelope.msg.channel, sid=subscribed_envelope.msg.sid
        )

    if frame_type == "unsubscribed":
        try:
            unsubscribed_envelope = _UnsubscribedFrame.model_validate(decoded)
        except ValidationError:
            return MalformedFrame("unsubscribed frame failed schema validation")
        return UnsubscribedFrame(sid=unsubscribed_envelope.sid)

    if frame_type == "ok":
        try:
            _OkFrame.model_validate(decoded)
        except ValidationError:
            return MalformedFrame("ok frame failed schema validation")
        return OkFrame()

    if frame_type == "error":
        try:
            error_envelope = _ErrorFrame.model_validate(decoded)
        except ValidationError:
            return MalformedFrame("error frame failed schema validation")
        return ErrorFrame(code=error_envelope.msg.code, message=error_envelope.msg.msg)

    # Every other type value -- including "orderbook_delta" -- is
    # unrecognized by this client and is never treated as known.
    return UnknownChannelFrame(frame_type)
