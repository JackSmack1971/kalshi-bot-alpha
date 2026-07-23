"""Read-only demo Kalshi WebSocket client (Phase 1 PR 5).

``KalshiDemoWebSocketClient`` exposes exactly two subscription
operations -- ``subscribe_ticker(tickers)`` and
``subscribe_trades(tickers)`` -- and nothing else. There is no generic
``subscribe(channels, tickers)`` escape hatch anywhere on this class,
no constructor argument that selects a host/environment, and no code
path that can ever request the ``orderbook_delta`` channel or any
channel other than ``ticker``/``trade``. See
``.claude/rules/kalshi-transport-safety.md`` for the invariants this
module must never weaken, and ``docs/PHASE1_PLAN.md`` PR 5 for this
module's exact forbidden scope (no order-book reconstruction, no
eligibility, no persistence, no strategy/risk/portfolio/ledger/
reconciliation/replay/external-reference/order-mutation/AI-control-plane
code).

**Demo-only authority.** The WebSocket URL is derived only from
``kalshi_bot.contracts.demo_endpoints.DEMO_WS_HOST`` and validated via
``validate_host`` at construction time, before any connector, socket,
or background task is created. There is no
``environment``/``host``/``url`` constructor parameter of any kind.

**Signing.** The connection handshake is signed via an injected
``kalshi_bot.auth.signer.RequestSigner`` against the canonical
``GET /trade-api/ws/v2`` method/path pair (not the REST API root),
per ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-getting-started-quick-start-websockets-a95bc67f.md``.
This client never reads ``os.environ`` or loads credentials itself.

**Proxy isolation.** Every real connect call passes ``proxy=None``
explicitly and unconditionally to ``websockets.connect()``, mirroring
``kalshi_bot.rest.client``'s ``trust_env=False`` rationale: the
``websockets`` library reads ``HTTPS_PROXY``/``getproxies()`` by
default (``proxy=True``), which could silently route this client's
signed handshake through infrastructure selected by the process
environment. This client never trusts that environment.

**Reconnect.** A dropped connection (after the initial successful
connect) is retried indefinitely with bounded exponential backoff and
jitter (:class:`ReconnectPolicy`), parameterized by
``AppConfig.ws_reconnect_backoff_min_seconds``/``ws_reconnect_backoff_max_seconds``
-- there is no maximum-attempt-count cutoff (the binding Phase 1 plan
specifies bounded backoff seconds, not a bounded attempt count).
Reconnect never happens after an explicit ``disconnect()``/context-
manager exit. Every connection attempt is tagged with a monotonically
increasing ``generation`` counter; a frame originating from a
superseded connection generation is dropped rather than delivered to a
caller, even if it is still technically in flight when the switch
happens.

**Logging.** Uses only ``kalshi_bot.observability.logging.get_logger``.
Every log call here uses structured, non-secret keyword fields
(channel, ticker count, reconnect attempt number, backoff seconds,
malformed-frame counters) -- never a headers dict, a
``SignedHeaders``/credential object, or raw frame content.
"""

from __future__ import annotations

import asyncio
import contextlib
import enum
import json
import random
import time
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from types import TracebackType
from typing import Protocol

import websockets
from websockets.exceptions import ConnectionClosedError

from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config.models import AppConfig
from kalshi_bot.contracts.demo_endpoints import DEMO_WS_HOST, validate_host
from kalshi_bot.observability.logging import get_logger
from kalshi_bot.ws.errors import (
    DemoHostValidationError,
    RequestValidationError,
    WebSocketClientStateError,
    WebSocketConnectionError,
    WebSocketDisconnected,
)
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

__all__ = ["KalshiDemoWebSocketClient", "ReconnectPolicy"]

_logger = get_logger(__name__)

_WS_HANDSHAKE_METHOD = "GET"
_WS_HANDSHAKE_PATH = "/trade-api/ws/v2"

#: Bound on how many recent disconnect events are retained for caller
#: inspection via ``disconnect_events`` -- a long-running client must
#: not grow this list without bound.
_MAX_TRACKED_DISCONNECT_EVENTS = 256


class _WebSocketConnection(Protocol):
    """Structural interface this client needs from a connected socket.

    Satisfied by ``websockets.asyncio.client.ClientConnection`` (the
    real production connection type) and by any test fake with a
    matching shape -- there is no ``isinstance`` check against this
    protocol anywhere, only static typing.
    """

    def __aiter__(self) -> AsyncIterator[str | bytes]: ...

    async def send(self, message: str) -> None: ...

    async def close(self, code: int = 1000, reason: str = "") -> None: ...


#: The injectable "connect function/factory" test hook's type: given the
#: fixed demo URL, the signed handshake headers, and the configured
#: open-connection timeout, return a connected socket. Production code
#: always uses ``KalshiDemoWebSocketClient._default_connector``; tests
#: may substitute a callable that ignores ``url`` and dials a local
#: ``websockets.serve`` test server instead.
_Connector = Callable[[str, Mapping[str, str], float], Awaitable[_WebSocketConnection]]


class _Channel(enum.Enum):
    """The closed set of channels this client can ever subscribe to.

    There is no third value, and no public API accepts an arbitrary
    channel string -- ``subscribe_ticker``/``subscribe_trades`` are the
    only two call sites that ever construct a subscribe command, and
    each hard-codes exactly one of these two values.
    """

    TICKER = "ticker"
    TRADE = "trade"


class _Stop:
    """Internal sentinel pushed onto a channel queue to end its generator.

    A dedicated type (rather than ``None`` or a string) so it can never
    be confused with a legitimate queued item, including under
    ``isinstance`` narrowing.
    """

    __slots__ = ()


_STOP = _Stop()


class ReconnectPolicy:
    """Bounded exponential backoff with jitter for the reconnect loop.

    Pure and independently unit-testable: :meth:`next_delay_seconds`
    takes the 1-based consecutive-failure ``attempt`` count and a
    caller-supplied ``jitter_fraction`` in ``[0.0, 1.0)`` (production
    code supplies ``random.random()``; tests inject a deterministic
    value) and returns a delay bounded to
    ``[min_backoff_seconds, min(max_backoff_seconds, min_backoff_seconds
    * 2**(attempt-1))]``. ``attempt`` always restarts at 1 after every
    successful reconnect -- there is no cumulative, ever-growing
    backoff across a long-running client's full lifetime.
    """

    __slots__ = ("min_backoff_seconds", "max_backoff_seconds")

    def __init__(self, min_backoff_seconds: float, max_backoff_seconds: float) -> None:
        if min_backoff_seconds <= 0:
            raise ValueError("min_backoff_seconds must be > 0")
        if max_backoff_seconds < min_backoff_seconds:
            raise ValueError("max_backoff_seconds must be >= min_backoff_seconds")
        self.min_backoff_seconds = min_backoff_seconds
        self.max_backoff_seconds = max_backoff_seconds

    def next_delay_seconds(self, attempt: int, jitter_fraction: float) -> float:
        """Return the bounded, jittered backoff delay for ``attempt``."""
        if attempt < 1:
            raise ValueError("attempt must be >= 1")
        if not (0.0 <= jitter_fraction < 1.0):
            raise ValueError("jitter_fraction must be in [0.0, 1.0)")
        base: float = min(
            self.max_backoff_seconds, self.min_backoff_seconds * (2 ** (attempt - 1))
        )
        return self.min_backoff_seconds + (base - self.min_backoff_seconds) * jitter_fraction


def _validate_tickers(tickers: list[str]) -> tuple[str, ...]:
    """Fail-closed validation gate for a ``subscribe_*`` ``tickers`` argument.

    Called before any connection state is touched or any command is
    sent. Requires a nonempty list of nonempty, non-whitespace-padded,
    non-duplicated strings. The grounding doc's example subscribe
    command also supports omitting ``market_tickers`` entirely to mean
    "all markets on this channel" -- this client deliberately narrows
    that: an empty ``tickers`` list is rejected rather than silently
    subscribing to every market, mirroring
    ``kalshi_bot.rest.client``'s own disclosed narrower-than-documented
    parameter choices (see that module's ``limit`` lower-bound
    docstring for the precedent).
    """
    if not isinstance(tickers, list):
        raise RequestValidationError("tickers must be a list of strings")
    if len(tickers) == 0:
        raise RequestValidationError("tickers must not be empty")

    seen: set[str] = set()
    validated: list[str] = []
    for value in tickers:
        if not isinstance(value, str) or value == "":
            raise RequestValidationError("each ticker must be a nonempty string")
        if value != value.strip():
            raise RequestValidationError(
                "each ticker must not have leading or trailing whitespace"
            )
        if value in seen:
            raise RequestValidationError(f"duplicate ticker {value!r} in subscription request")
        seen.add(value)
        validated.append(value)
    return tuple(validated)


def _default_jitter_source() -> float:
    """Production jitter source. Tests inject a deterministic callable instead."""
    return random.random()


async def _default_sleeper(seconds: float) -> None:
    """Production async sleeper. Tests inject a recording no-op instead."""
    await asyncio.sleep(seconds)


def _default_clock_ms() -> int:
    """Production millisecond clock, matching ``kalshi_bot.rest.client``'s
    same indirection point so tests never depend on wall-clock time."""
    return int(time.time() * 1000)


class KalshiDemoWebSocketClient:
    """Read-only demo Kalshi WebSocket client.

    Construction takes only ``signer`` and ``config`` (plus optional
    test-only injected ``clock_ms``/``connector``/``jitter_source``/
    ``sleeper``) -- no host, base URL, environment, or
    production-selector argument of any kind exists on this
    constructor. The WebSocket URL is derived internally from
    ``kalshi_bot.contracts.demo_endpoints.DEMO_WS_HOST`` and validated
    via ``validate_host`` before any connector, socket, or background
    task is created; construction raises
    :class:`~kalshi_bot.ws.errors.DemoHostValidationError` rather than
    proceeding if that check ever fails.

    Public surface is exactly ``connect``, ``disconnect``,
    ``subscribe_ticker``, ``subscribe_trades``, plus async
    context-manager support. There is no generic ``subscribe(channels,
    tickers)`` method and no method that can ever request a channel
    other than ``ticker``/``trade``.

    **Concurrency scope, stated explicitly:** this client supports at
    most one active ``subscribe_ticker`` iteration and one active
    ``subscribe_trades`` iteration at a time. Calling either method
    again while a previous call on the same channel is still being
    iterated replaces that channel's active ticker set and queue (the
    older iterator stops receiving further items) rather than fanning
    the same channel out to multiple independent consumers -- this
    fan-out capability is not required by ``docs/PHASE1_PLAN.md`` PR 5
    and is not implemented here.
    """

    def __init__(
        self,
        signer: RequestSigner,
        config: AppConfig,
        *,
        clock_ms: Callable[[], int] | None = None,
        connector: _Connector | None = None,
        jitter_source: Callable[[], float] | None = None,
        sleeper: Callable[[float], Awaitable[None]] | None = None,
    ) -> None:
        if not validate_host(DEMO_WS_HOST):
            # Unreachable in ordinary operation -- see
            # DemoHostValidationError's docstring for why this
            # unconditional check still runs before any I/O.
            raise DemoHostValidationError(
                "the fixed Kalshi demo WebSocket host failed validate_host(); "
                "refusing to construct a connector"
            )

        self._signer = signer
        self._config = config
        self._clock_ms = clock_ms if clock_ms is not None else _default_clock_ms
        self._connector: _Connector = connector if connector is not None else self._default_connector
        self._jitter_source = jitter_source if jitter_source is not None else _default_jitter_source
        self._sleeper = sleeper if sleeper is not None else _default_sleeper

        self._ws_url = f"wss://{DEMO_WS_HOST}{_WS_HANDSHAKE_PATH}"
        self._reconnect_policy = ReconnectPolicy(
            min_backoff_seconds=config.ws_reconnect_backoff_min_seconds,
            max_backoff_seconds=config.ws_reconnect_backoff_max_seconds,
        )

        self._connection: _WebSocketConnection | None = None
        self._connection_task: asyncio.Task[None] | None = None
        self._closing = False
        self._generation = 0
        self._command_id = 0

        self._active_channel_tickers: dict[_Channel, tuple[str, ...]] = {}
        self._channel_queues: dict[_Channel, "asyncio.Queue[TickerUpdate | TradeUpdate | _Stop]"] = {}

        self._malformed_frame_count = 0
        self._stale_frame_drop_count = 0
        self._disconnect_events: list[WebSocketDisconnected] = []

    # -- Properties ---------------------------------------------------------

    @property
    def ws_url(self) -> str:
        """The fixed demo WebSocket URL this client is permanently bound to."""
        return self._ws_url

    @property
    def malformed_frame_count(self) -> int:
        """Count of frames dropped for being undecodable or schema-invalid."""
        return self._malformed_frame_count

    @property
    def stale_frame_drop_count(self) -> int:
        """Count of typed events dropped because their connection
        generation was superseded before they could be delivered."""
        return self._stale_frame_drop_count

    @property
    def disconnect_events(self) -> tuple[WebSocketDisconnected, ...]:
        """Read-only history (bounded, oldest evicted first) of every
        non-caller-initiated disconnect this client has observed."""
        return tuple(self._disconnect_events)

    # -- Lifecycle ------------------------------------------------------

    async def connect(self) -> None:
        """Open the initial connection and start the reconnect supervisor.

        Raises :class:`~kalshi_bot.ws.errors.WebSocketConnectionError`
        immediately (no retry) if the very first dial fails -- a
        Phase-1-scoped startup fails fast rather than blocking
        forever, per ``.claude/rules/runtime-lifecycle.md``'s
        fail-closed posture. Every subsequent drop (after this initial
        success) is instead retried indefinitely with bounded backoff
        by the background supervisor task; see the module docstring.
        """
        if self._connection is not None or self._connection_task is not None:
            raise WebSocketClientStateError("connect() called while already connected")

        self._closing = False
        try:
            conn = await self._dial()
        except Exception as exc:
            _logger.warning("ws_initial_connect_failed", error_type=type(exc).__name__)
            raise WebSocketConnectionError(
                f"initial WebSocket connection failed ({type(exc).__name__})"
            ) from None

        self._generation += 1
        generation = self._generation
        self._connection = conn
        await self._resubscribe_all()
        self._connection_task = asyncio.ensure_future(self._supervise_connection(conn, generation))
        _logger.info("ws_connected", generation=generation)

    async def disconnect(self) -> None:
        """Clean shutdown. Idempotent; never triggers a further reconnect.

        Cancels the background supervisor task, closes the current
        connection if any, and releases every active
        ``subscribe_ticker``/``subscribe_trades`` iterator (they return
        rather than raising).
        """
        if self._closing:
            return
        self._closing = True

        task = self._connection_task
        self._connection_task = None
        if task is not None:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

        if self._connection is not None:
            await self._safe_close(self._connection)
            self._connection = None

        for queue in self._channel_queues.values():
            queue.put_nowait(_STOP)
        _logger.info("ws_disconnected_clean")

    async def __aenter__(self) -> KalshiDemoWebSocketClient:
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.disconnect()

    # -- Public subscriptions --------------------------------------------

    async def subscribe_ticker(self, tickers: list[str]) -> AsyncIterator[TickerUpdate]:
        """Subscribe to the ``ticker`` channel for ``tickers``.

        Yields normalized :class:`~kalshi_bot.ws.models.TickerUpdate`
        events indefinitely, transparently surviving reconnects, until
        the client is disconnected. There is no parameter or code path
        through which any channel other than ``ticker`` can ever be
        requested here.
        """
        async for item in self._subscribe_channel(_Channel.TICKER, tickers):
            if isinstance(item, TickerUpdate):
                yield item

    async def subscribe_trades(self, tickers: list[str]) -> AsyncIterator[TradeUpdate]:
        """Subscribe to the ``trade`` channel for ``tickers``.

        Yields normalized :class:`~kalshi_bot.ws.models.TradeUpdate`
        events indefinitely, transparently surviving reconnects, until
        the client is disconnected. There is no parameter or code path
        through which any channel other than ``trade`` can ever be
        requested here.
        """
        async for item in self._subscribe_channel(_Channel.TRADE, tickers):
            if isinstance(item, TradeUpdate):
                yield item

    async def _subscribe_channel(
        self, channel: _Channel, tickers: list[str]
    ) -> AsyncIterator[TickerUpdate | TradeUpdate]:
        validated = _validate_tickers(tickers)
        queue: "asyncio.Queue[TickerUpdate | TradeUpdate | _Stop]" = asyncio.Queue()
        self._channel_queues[channel] = queue
        self._active_channel_tickers[channel] = validated

        if self._connection is not None:
            await self._send_subscribe(channel, validated)

        try:
            while True:
                item = await queue.get()
                if isinstance(item, _Stop):
                    return
                yield item
        finally:
            if self._channel_queues.get(channel) is queue:
                del self._channel_queues[channel]

    # -- Internal connection management ----------------------------------

    async def _default_connector(
        self, url: str, headers: Mapping[str, str], timeout: float
    ) -> _WebSocketConnection:
        """Production connector: dial the fixed demo host with no proxy trust.

        ``proxy=None`` is passed explicitly and unconditionally --
        never derived from ``HTTPS_PROXY``/``getproxies()`` or any
        other process-environment proxy configuration. See the module
        docstring's "Proxy isolation" section.
        """
        connection = await websockets.connect(
            url,
            additional_headers=dict(headers),
            proxy=None,
            open_timeout=timeout,
        )
        return connection

    async def _dial(self) -> _WebSocketConnection:
        timestamp_ms = self._clock_ms()
        signed = self._signer.sign(_WS_HANDSHAKE_METHOD, _WS_HANDSHAKE_PATH, timestamp_ms)
        headers = {
            "KALSHI-ACCESS-KEY": signed.access_key,
            "KALSHI-ACCESS-SIGNATURE": signed.signature,
            "KALSHI-ACCESS-TIMESTAMP": str(signed.timestamp_ms),
        }
        return await self._connector(self._ws_url, headers, self._config.ws_timeout_seconds)

    async def _safe_close(self, conn: _WebSocketConnection) -> None:
        try:
            await conn.close()
        except Exception as exc:  # noqa: BLE001 - closing a possibly-broken socket must never raise
            _logger.info("ws_close_error_ignored", error_type=type(exc).__name__)

    async def _resubscribe_all(self) -> None:
        """Re-issue exactly the caller's currently tracked subscriptions.

        Never accumulates: each channel holds exactly one tracked
        ticker tuple (overwritten by the most recent
        ``subscribe_ticker``/``subscribe_trades`` call, never appended
        to), so a reconnect can never amplify into duplicate
        subscribe commands for the same channel/ticker set.
        """
        for channel, tickers in self._active_channel_tickers.items():
            if tickers:
                await self._send_subscribe(channel, tickers)

    async def _send_subscribe(self, channel: _Channel, tickers: tuple[str, ...]) -> None:
        conn = self._connection
        if conn is None:
            return
        self._command_id += 1
        command_id = self._command_id
        command = {
            "id": command_id,
            "cmd": "subscribe",
            "params": {"channels": [channel.value], "market_tickers": list(tickers)},
        }
        await conn.send(json.dumps(command))
        _logger.info(
            "ws_subscribe_sent",
            channel=channel.value,
            ticker_count=len(tickers),
            command_id=command_id,
        )

    async def _supervise_connection(self, conn: _WebSocketConnection, generation: int) -> None:
        """Background task: run the receive loop, reconnect on drop.

        Runs until ``disconnect()`` cancels this task (no further
        reconnect attempted) or the process managing this client exits.
        """
        current_conn = conn
        current_generation = generation
        try:
            while True:
                reason = await self._receive_loop(current_conn, current_generation)
                await self._safe_close(current_conn)
                self._connection = None

                if self._closing:
                    return
                if reason == "superseded":
                    # This connection was already superseded by a newer
                    # generation before this loop noticed the drop --
                    # unreachable via this class's own sequential
                    # reconnect design (only one connection is ever
                    # dialed at a time), kept only as defense in depth.
                    _logger.info("ws_supervisor_superseded", generation=current_generation)
                    return

                self._record_disconnect(reason=reason, generation=current_generation, attempt=1)

                next_conn = await self._reconnect_with_backoff(1)
                if next_conn is None:
                    return

                self._generation += 1
                current_generation = self._generation
                current_conn = next_conn
                self._connection = current_conn
                await self._resubscribe_all()
                _logger.info("ws_reconnected", generation=current_generation)
        except asyncio.CancelledError:
            await self._safe_close(current_conn)
            raise

    async def _reconnect_with_backoff(self, start_attempt: int) -> _WebSocketConnection | None:
        """Retry the dial indefinitely with bounded backoff.

        Returns ``None`` only if ``disconnect()`` requested shutdown
        while this loop was waiting or dialing -- the caller must treat
        that as "stop, do not reconnect."
        """
        attempt = start_attempt
        while True:
            if self._closing:
                return None
            backoff = self._reconnect_policy.next_delay_seconds(attempt, self._jitter_source())
            _logger.info("ws_reconnect_backoff_wait", attempt=attempt, backoff_seconds=backoff)
            await self._sleeper(backoff)
            if self._closing:
                return None
            try:
                return await self._dial()
            except Exception as exc:  # noqa: BLE001 - dial failures are classified generically and retried
                _logger.warning(
                    "ws_reconnect_dial_failed", attempt=attempt, error_type=type(exc).__name__
                )
                attempt += 1

    async def _receive_loop(self, conn: _WebSocketConnection, generation: int) -> str:
        """Read and dispatch frames until the connection ends.

        Returns ``"closed_ok"`` for a clean closure, ``"closed_error"``
        for a protocol/network failure, or ``"superseded"`` if this
        connection's generation was replaced mid-loop (see
        ``_supervise_connection``'s docstring for why that is
        unreachable in this class's current sequential design).
        """
        try:
            async for raw in conn:
                if generation != self._generation:
                    return "superseded"
                self._dispatch_frame(raw, generation)
            return "closed_ok"
        except ConnectionClosedError:
            return "closed_error"

    def _dispatch_frame(self, raw: str | bytes, generation: int) -> None:
        result = parse_frame(raw)

        if isinstance(result, MalformedFrame):
            self._malformed_frame_count += 1
            _logger.warning(
                "ws_malformed_frame",
                reason=result.reason,
                malformed_frame_count=self._malformed_frame_count,
            )
            return

        if isinstance(result, UnknownChannelFrame):
            _logger.info("ws_unknown_frame_type", frame_type=result.frame_type)
            return

        if isinstance(result, TickerUpdate):
            self._route_to_queue(_Channel.TICKER, result, generation)
            return

        if isinstance(result, TradeUpdate):
            self._route_to_queue(_Channel.TRADE, result, generation)
            return

        if isinstance(result, SubscribedFrame):
            _logger.info("ws_subscribed", channel=result.channel, sid=result.sid)
            return

        if isinstance(result, UnsubscribedFrame):
            _logger.info("ws_unsubscribed", sid=result.sid)
            return

        if isinstance(result, OkFrame):
            _logger.info("ws_ok_frame")
            return

        if isinstance(result, ErrorFrame):
            _logger.warning("ws_error_frame", code=result.code, message=result.message)
            return

    def _route_to_queue(
        self, channel: _Channel, item: TickerUpdate | TradeUpdate, generation: int
    ) -> None:
        if generation != self._generation:
            self._stale_frame_drop_count += 1
            _logger.info(
                "ws_stale_frame_dropped",
                channel=channel.value,
                frame_generation=generation,
                current_generation=self._generation,
            )
            return
        queue = self._channel_queues.get(channel)
        if queue is None:
            return
        queue.put_nowait(item)

    def _record_disconnect(self, *, reason: str, generation: int, attempt: int) -> None:
        event = WebSocketDisconnected(
            reason=reason,
            generation=generation,
            attempt=attempt,
            timestamp_ms=self._clock_ms(),
        )
        self._disconnect_events.append(event)
        if len(self._disconnect_events) > _MAX_TRACKED_DISCONNECT_EVENTS:
            self._disconnect_events.pop(0)
        _logger.warning("ws_disconnected", reason=reason, generation=generation, attempt=attempt)
