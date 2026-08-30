"""Typed error/event hierarchy for the Kalshi demo WebSocket client (Phase 1 PR 5).

Mirrors ``kalshi_bot.rest.errors``'s discipline: every message here is
deliberately narrow (operation name, reason keyword, attempt/generation
counters) -- never a raw connect-headers dict, an access-key ID, a
signature, or a verbatim third-party exception's ``str()``/``repr()``.

:class:`WebSocketDisconnected` is intentionally **not** an ``Exception``
subclass even though it lives in this "errors" module alongside the
exception hierarchy: per ``docs/PHASE1_PLAN.md`` PR 5, a dropped
connection must be "logged and reconnect triggered, never a silent
message drop" -- it is a caller-observable *event*, not a fault that
propagates up and stops the subscription's async iterator (the client
recovers from it automatically). It is kept in this module rather than
``models.py`` because it is an internal client-lifecycle signal, not an
external Kalshi wire-format response model.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "KalshiWsError",
    "DemoHostValidationError",
    "RequestValidationError",
    "WebSocketClientStateError",
    "WebSocketConnectionError",
    "WebSocketDisconnected",
]


class KalshiWsError(Exception):
    """Base for every error raised by :mod:`kalshi_bot.ws`.

    Catching this catches every exception-shaped failure mode the demo
    WebSocket client can produce. Never carries credential-bearing
    text -- see the module docstring for the exact policy.
    """


class DemoHostValidationError(KalshiWsError):
    """Raised if the fixed demo WebSocket host ever fails ``validate_host``.

    Should be unreachable in ordinary operation: the host passed to
    ``validate_host`` is the same ``DEMO_WS_HOST`` constant that
    function checks against. The check still runs, unconditionally, at
    :class:`~kalshi_bot.ws.client.KalshiDemoWebSocketClient` construction
    time -- before any socket, connector, or background task is created
    -- per ``.claude/rules/kalshi-transport-safety.md``'s requirement
    that demo-host validation happen before any I/O.
    """


class RequestValidationError(KalshiWsError):
    """Raised when a caller-supplied ``tickers`` list fails validation.

    Covers an empty list, a non-string entry, an entry with surrounding
    whitespace, and a duplicate ticker within the same call. Raised
    before any connection state is touched or any command is sent --
    an invalid parameter never reaches the network.
    """


class WebSocketClientStateError(KalshiWsError):
    """Raised for an invalid lifecycle transition.

    Currently covers only calling ``connect()`` while already
    connected. ``disconnect()`` is intentionally idempotent (never
    raises this) so shutdown code never needs to guard every call with
    a state check.
    """


class WebSocketConnectionError(KalshiWsError):
    """Raised when the *initial* ``connect()`` dial fails.

    Distinct from a post-connect drop (which triggers the internal
    bounded-backoff reconnect loop automatically rather than raising):
    a failure on the very first dial is surfaced immediately so startup
    code fails fast rather than blocking forever, consistent with
    ``.claude/rules/runtime-lifecycle.md``'s fail-closed startup
    posture. The message carries only the underlying exception's class
    name (``type(exc).__name__``) -- never ``str(exc)``/``repr(exc)``.
    """


@dataclass(frozen=True, slots=True)
class WebSocketDisconnected:
    """A caller-observable record of one dropped-connection event.

    Emitted (logged, and appended to
    :attr:`~kalshi_bot.ws.client.KalshiDemoWebSocketClient.disconnect_events`)
    every time the managed connection drops for a reason other than the
    caller's own ``disconnect()``/context-manager exit -- never for a
    clean, caller-initiated shutdown, which must never trigger a
    reconnect at all.

    ``reason`` is one of ``"closed_ok"`` (the server or network closed
    the connection cleanly) or ``"closed_error"`` (a protocol error or
    network failure); ``generation`` is the monotonically increasing
    connection-attempt counter of the connection that dropped;
    ``attempt`` is always ``1`` (the reconnect attempt counter always
    restarts at 1 after every drop -- see
    :class:`~kalshi_bot.ws.client.ReconnectPolicy`).
    """

    reason: str
    generation: int
    attempt: int
    timestamp_ms: int
