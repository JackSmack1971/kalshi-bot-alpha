"""Tests for kalshi_bot.ws.client.KalshiDemoWebSocketClient (Phase 1 PR 5).

No network, filesystem, or real credential material anywhere in this
file. Uses a duck-typed fake signer and small scripted fake connections/
connectors so signing, reconnect/backoff, malformed-frame handling, and
stale-generation dropping are all deterministic and never sleep in real
wall time.
"""

from __future__ import annotations

import asyncio
import inspect
import io
import json
from collections.abc import AsyncIterator, Iterator, Mapping
from typing import Any

import pytest

import kalshi_bot.ws.client as ws_client_module
from kalshi_bot.auth.signer import SignedHeaders
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.observability import configure_logging, get_logger
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests
from kalshi_bot.ws.client import KalshiDemoWebSocketClient, ReconnectPolicy, _Channel
from kalshi_bot.ws.errors import (
    DemoHostValidationError,
    WebSocketClientStateError,
    WebSocketConnectionError,
)
from kalshi_bot.ws.models import TickerUpdate

FAKE_ACCESS_KEY = "FAKE-ACCESS-KEY-FOR-WS-CLIENT-TESTS"
FAKE_SIGNATURE = "FAKE-SIGNATURE-FOR-WS-CLIENT-TESTS"


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


class _FakeSigner:
    """Duck-typed stand-in for RequestSigner; no real key material."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, int]] = []

    def sign(self, method: str, path: str, timestamp_ms: int) -> SignedHeaders:
        self.calls.append((method, path, timestamp_ms))
        return SignedHeaders(
            access_key=FAKE_ACCESS_KEY, signature=FAKE_SIGNATURE, timestamp_ms=timestamp_ms
        )


class _FakeClock:
    def __init__(self, start: int = 1_700_000_000_000) -> None:
        self._value = start

    def __call__(self) -> int:
        self._value += 1
        return self._value


class _RecordingSleeper:
    """Records requested backoff durations; always yields once so the
    supervisor task cooperates with the event loop instead of spinning."""

    def __init__(self) -> None:
        self.calls: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)
        await asyncio.sleep(0)


def _make_config(
    *,
    ws_timeout_seconds: float = 5.0,
    ws_reconnect_backoff_min_seconds: float = 0.01,
    ws_reconnect_backoff_max_seconds: float = 0.08,
) -> AppConfig:
    return AppConfig(
        rest_timeout_seconds=5.0,
        rest_max_retries=2,
        rest_retry_backoff_min_seconds=0.01,
        rest_retry_backoff_max_seconds=0.08,
        ws_timeout_seconds=ws_timeout_seconds,
        ws_reconnect_backoff_min_seconds=ws_reconnect_backoff_min_seconds,
        ws_reconnect_backoff_max_seconds=ws_reconnect_backoff_max_seconds,
        credentials=CredentialReferences(
            access_key_env="TEST_WS_CLIENT_ACCESS_KEY_ENV",
            private_key_path_env="TEST_WS_CLIENT_PRIVATE_KEY_PATH_ENV",
        ),
    )


class _CloseOk:
    __slots__ = ()


class _CloseError:
    __slots__ = ()


_CLOSE_OK = _CloseOk()
_CLOSE_ERROR = _CloseError()


class _FakeConnection:
    """In-memory stand-in for a connected socket; no real I/O."""

    def __init__(self) -> None:
        self._incoming: asyncio.Queue[object] = asyncio.Queue()
        self.sent: list[str] = []
        self.close_calls = 0

    def push(self, raw: str) -> None:
        self._incoming.put_nowait(raw)

    def push_close_ok(self) -> None:
        self._incoming.put_nowait(_CLOSE_OK)

    def push_close_error(self) -> None:
        self._incoming.put_nowait(_CLOSE_ERROR)

    async def send(self, message: str) -> None:
        self.sent.append(message)

    async def close(self, code: int = 1000, reason: str = "") -> None:
        self.close_calls += 1

    async def __aiter__(self) -> AsyncIterator[str]:
        from websockets.exceptions import ConnectionClosedError

        while True:
            item = await self._incoming.get()
            if item is _CLOSE_OK:
                return
            if item is _CLOSE_ERROR:
                raise ConnectionClosedError(None, None)
            assert isinstance(item, str)
            yield item


class _ScriptedConnector:
    """Replays a fixed sequence of connections/exceptions, one per dial."""

    def __init__(self, items: list[_FakeConnection | Exception]) -> None:
        self._items = list(items)
        self.calls: list[tuple[str, dict[str, str], float]] = []

    async def __call__(self, url: str, headers: Mapping[str, str], timeout: float) -> Any:
        self.calls.append((url, dict(headers), timeout))
        item = self._items.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class _RaisingSendConnection(_FakeConnection):
    """A connection that dials successfully but whose ``send()`` always
    fails -- simulates the server closing the socket between a
    successful reconnect and the resubscribe command's send completing."""

    async def send(self, message: str) -> None:
        raise ConnectionResetError("simulated: server closed the socket during resubscribe send")


def _make_client(signer: Any, config: AppConfig, **kwargs: Any) -> KalshiDemoWebSocketClient:
    """Constructs the client with a duck-typed fake signer.

    ``_FakeSigner`` intentionally does not subclass
    ``kalshi_bot.auth.signer.RequestSigner`` (that class forbids direct
    construction outside its own module -- see its docstring), so this
    single, narrow ``type: ignore`` isolates the resulting mypy
    ``arg-type`` mismatch to one place instead of scattering it across
    every test in this file, matching
    ``tests/unit/test_rest_client.py``'s equivalent
    ``# type: ignore[arg-type]`` convention for its own duck-typed fake
    signer.
    """
    return KalshiDemoWebSocketClient(signer, config, **kwargs)


# -- Demo-host validation, before any I/O ------------------------------------


def test_demo_host_validation_runs_before_any_connector(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ws_client_module, "validate_host", lambda host: False)

    with pytest.raises(DemoHostValidationError):
        _make_client(_FakeSigner(), _make_config())


# -- Handshake signing and fixed URL ------------------------------------------


def test_connect_signs_ws_handshake_and_uses_fixed_url() -> None:
    async def run() -> None:
        signer = _FakeSigner()
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            signer,
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        try:
            await client.connect()

            assert len(signer.calls) == 1
            method, path, _timestamp_ms = signer.calls[0]
            assert method == "GET"
            assert path == "/trade-api/ws/v2"

            url, headers, timeout = connector.calls[0]
            assert url == "wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2"
            assert client.ws_url == url
            assert set(headers.keys()) == {
                "KALSHI-ACCESS-KEY",
                "KALSHI-ACCESS-SIGNATURE",
                "KALSHI-ACCESS-TIMESTAMP",
            }
            assert headers["KALSHI-ACCESS-KEY"] == FAKE_ACCESS_KEY
            assert headers["KALSHI-ACCESS-SIGNATURE"] == FAKE_SIGNATURE
            assert timeout == 5.0
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_default_connector_never_trusts_environment_proxy(monkeypatch: pytest.MonkeyPatch) -> None:
    """The ``websockets`` library reads HTTPS_PROXY/getproxies() by
    default (``proxy=True``); this client must pass ``proxy=None``
    explicitly and unconditionally on every real connect call."""
    monkeypatch.setenv("HTTPS_PROXY", "http://evil-proxy.invalid:8080")
    monkeypatch.setenv("HTTP_PROXY", "http://evil-proxy.invalid:8080")

    captured_kwargs: dict[str, Any] = {}

    class _FakeWebsocketsModule:
        @staticmethod
        async def connect(url: str, **kwargs: Any) -> _FakeConnection:
            captured_kwargs.update(kwargs)
            captured_kwargs["url"] = url
            return _FakeConnection()

    monkeypatch.setattr(ws_client_module, "websockets", _FakeWebsocketsModule())

    async def run() -> None:
        client = _make_client(
            _FakeSigner(), _make_config(), clock_ms=_FakeClock(), sleeper=_RecordingSleeper()
        )
        try:
            await client.connect()
        finally:
            await client.disconnect()

    asyncio.run(run())

    assert captured_kwargs["proxy"] is None
    assert captured_kwargs["url"] == "wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2"


# -- Lifecycle state machine --------------------------------------------------


def test_initial_connect_failure_raises_immediately_without_retry() -> None:
    async def run() -> None:
        connector = _ScriptedConnector([OSError("boom")])
        client = _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        with pytest.raises(WebSocketConnectionError):
            await client.connect()
        assert len(connector.calls) == 1

    asyncio.run(run())


def test_connect_twice_raises_state_error() -> None:
    async def run() -> None:
        connector = _ScriptedConnector([_FakeConnection(), _FakeConnection()])
        client = _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        try:
            await client.connect()
            with pytest.raises(WebSocketClientStateError):
                await client.connect()
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_disconnect_without_connect_is_a_noop() -> None:
    async def run() -> None:
        client = _make_client(_FakeSigner(), _make_config())
        await client.disconnect()
        await client.disconnect()

    asyncio.run(run())


def test_disconnect_is_idempotent_after_connect() -> None:
    async def run() -> None:
        connector = _ScriptedConnector([_FakeConnection()])
        client = _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        await client.connect()
        await client.disconnect()
        await client.disconnect()

    asyncio.run(run())


def test_context_manager_connects_and_disconnects() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        async with _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        ) as client:
            assert client.ws_url == "wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2"
        assert conn.close_calls == 1

    asyncio.run(run())


# -- Malformed frame handling --------------------------------------------------


def test_malformed_frame_increments_counter_and_does_not_crash() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        try:
            await client.connect()
            generation = client._generation  # noqa: SLF001 - internal attribute access is intentional here
            client._dispatch_frame("not json at all {{{", generation)  # noqa: SLF001
            client._dispatch_frame(json.dumps({"no_type": True}), generation)  # noqa: SLF001
            assert client.malformed_frame_count == 2
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_unknown_channel_frame_including_orderbook_delta_is_ignored_not_malformed() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        try:
            await client.connect()
            generation = client._generation  # noqa: SLF001
            client._dispatch_frame(  # noqa: SLF001
                json.dumps({"type": "orderbook_delta", "sid": 1, "msg": {}}), generation
            )
            client._dispatch_frame(  # noqa: SLF001
                json.dumps({"type": "market_lifecycle_v2", "sid": 1, "msg": {}}), generation
            )
            assert client.malformed_frame_count == 0
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- Stale-generation frame dropping -------------------------------------------


def test_stale_generation_frame_is_dropped_not_delivered() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(),
            _make_config(),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
        )
        try:
            await client.connect()
            current_generation = client._generation  # noqa: SLF001
            stale_generation = current_generation - 1

            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)
            await asyncio.sleep(0)

            frame = json.dumps(
                {"type": "ticker", "sid": 1, "msg": {"market_ticker": "KXBTC-25JAN01"}}
            )
            client._dispatch_frame(frame, stale_generation)  # noqa: SLF001
            assert client.stale_frame_drop_count == 1
            assert not task.done()

            client._dispatch_frame(frame, current_generation)  # noqa: SLF001
            update = await asyncio.wait_for(task, timeout=1.0)
            assert update.market_ticker == "KXBTC-25JAN01"
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- ReconnectPolicy: pure, independently testable ----------------------------


def test_reconnect_policy_rejects_invalid_bounds() -> None:
    with pytest.raises(ValueError):
        ReconnectPolicy(min_backoff_seconds=0.0, max_backoff_seconds=1.0)
    with pytest.raises(ValueError):
        ReconnectPolicy(min_backoff_seconds=2.0, max_backoff_seconds=1.0)


def test_reconnect_policy_rejects_invalid_attempt_or_jitter() -> None:
    policy = ReconnectPolicy(min_backoff_seconds=1.0, max_backoff_seconds=10.0)
    with pytest.raises(ValueError):
        policy.next_delay_seconds(0, 0.5)
    with pytest.raises(ValueError):
        policy.next_delay_seconds(1, 1.0)
    with pytest.raises(ValueError):
        policy.next_delay_seconds(1, -0.1)


def test_reconnect_policy_bounded_exponential_growth_with_jitter() -> None:
    policy = ReconnectPolicy(min_backoff_seconds=1.0, max_backoff_seconds=8.0)

    # attempt=1: exponential base equals min, so jitter has no effect yet.
    assert policy.next_delay_seconds(1, 0.0) == pytest.approx(1.0)
    assert policy.next_delay_seconds(1, 0.999) == pytest.approx(1.0)

    # attempt=2: base=2.0.
    assert policy.next_delay_seconds(2, 0.0) == pytest.approx(1.0)
    assert policy.next_delay_seconds(2, 1.0 - 1e-9) == pytest.approx(2.0, rel=1e-6)

    # attempt=10: base capped at max=8.0.
    assert policy.next_delay_seconds(10, 0.0) == pytest.approx(1.0)
    assert policy.next_delay_seconds(10, 1.0 - 1e-9) == pytest.approx(8.0, rel=1e-6)


# -- Reconnect loop behavior ----------------------------------------------------


def test_reconnect_after_clean_drop_uses_bounded_backoff() -> None:
    async def run() -> None:
        conn1 = _FakeConnection()
        conn2 = _FakeConnection()
        connector = _ScriptedConnector([conn1, conn2])
        sleeper = _RecordingSleeper()

        client = _make_client(
            _FakeSigner(),
            _make_config(ws_reconnect_backoff_min_seconds=0.05, ws_reconnect_backoff_max_seconds=0.4),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=sleeper,
            jitter_source=lambda: 0.0,
        )
        try:
            await client.connect()
            conn1.push_close_ok()

            for _ in range(50):
                await asyncio.sleep(0)
                if len(connector.calls) >= 2:
                    break

            assert len(client.disconnect_events) == 1
            assert client.disconnect_events[0].reason == "closed_ok"
            assert client.disconnect_events[0].attempt == 1
            assert sleeper.calls == [0.05]
            assert len(connector.calls) == 2
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_reconnect_after_protocol_error_records_closed_error_reason() -> None:
    async def run() -> None:
        conn1 = _FakeConnection()
        conn2 = _FakeConnection()
        connector = _ScriptedConnector([conn1, conn2])
        sleeper = _RecordingSleeper()

        client = _make_client(
            _FakeSigner(),
            _make_config(ws_reconnect_backoff_min_seconds=0.05, ws_reconnect_backoff_max_seconds=0.4),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=sleeper,
            jitter_source=lambda: 0.0,
        )
        try:
            await client.connect()
            conn1.push_close_error()

            for _ in range(50):
                await asyncio.sleep(0)
                if len(connector.calls) >= 2:
                    break

            assert len(client.disconnect_events) == 1
            assert client.disconnect_events[0].reason == "closed_error"
            assert len(connector.calls) == 2
        finally:
            await client.disconnect()

    asyncio.run(run())


class _BlockingSleeper:
    """Never returns on its own -- only task cancellation (as triggered
    by ``disconnect()``) can interrupt it. Used to prove that
    ``disconnect()`` genuinely cancels a pending backoff wait rather
    than merely running faster than a real one would."""

    def __init__(self) -> None:
        self.calls: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)
        await asyncio.Event().wait()


def test_disconnect_during_backoff_prevents_further_connect_calls() -> None:
    async def run() -> None:
        conn1 = _FakeConnection()
        # Only one item: if a reconnect dial ever happened after
        # disconnect(), popping a second item would raise IndexError.
        connector = _ScriptedConnector([conn1])
        sleeper = _BlockingSleeper()

        client = _make_client(
            _FakeSigner(),
            _make_config(
                ws_reconnect_backoff_min_seconds=1000.0, ws_reconnect_backoff_max_seconds=1000.0
            ),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=sleeper,
            jitter_source=lambda: 0.0,
        )
        await client.connect()
        conn1.push_close_error()

        # Let the supervisor observe the drop and enter its (never-
        # returning, until cancelled) backoff wait.
        for _ in range(20):
            await asyncio.sleep(0)
        assert sleeper.calls == [1000.0]  # confirms it is genuinely waiting, not done

        await client.disconnect()

        assert len(connector.calls) == 1  # only the initial dial ever happened

        for _ in range(20):
            await asyncio.sleep(0)
        assert len(connector.calls) == 1

    asyncio.run(run())


# -- Channel exclusivity: only ticker/trade are ever reachable ---------------


def test_only_ticker_and_trade_channels_are_ever_reachable() -> None:
    assert {c.value for c in _Channel} == {"ticker", "trade"}

    ticker_params = list(inspect.signature(KalshiDemoWebSocketClient.subscribe_ticker).parameters)
    trade_params = list(inspect.signature(KalshiDemoWebSocketClient.subscribe_trades).parameters)
    assert ticker_params == ["self", "tickers"]
    assert trade_params == ["self", "tickers"]

    public_methods = [name for name in dir(KalshiDemoWebSocketClient) if not name.startswith("_")]
    assert "subscribe" not in public_methods


# -- Redaction: no secret leakage across connect/reconnect/failure paths -----


def test_no_secret_leakage_during_connect_reconnect_and_failure_paths() -> None:
    async def run() -> None:
        stream = io.StringIO()
        configure_logging(level="INFO", stream=stream)
        monkey_logger = get_logger("test.ws_client.no_leakage")
        original_logger = ws_client_module._logger
        ws_client_module._logger = monkey_logger
        try:
            conn1 = _FakeConnection()
            conn2 = _FakeConnection()
            connector = _ScriptedConnector([conn1, OSError("boom"), conn2])
            signer = _FakeSigner()
            client = _make_client(
                signer,
                _make_config(
                    ws_reconnect_backoff_min_seconds=0.001, ws_reconnect_backoff_max_seconds=0.01
                ),
                connector=connector,
                clock_ms=_FakeClock(),
                sleeper=_RecordingSleeper(),
                jitter_source=lambda: 0.0,
            )
            await client.connect()
            conn1.push_close_error()

            for _ in range(50):
                await asyncio.sleep(0)
                if len(connector.calls) >= 3:
                    break

            await client.disconnect()
        finally:
            ws_client_module._logger = original_logger

        rendered = stream.getvalue()
        assert FAKE_ACCESS_KEY not in rendered
        assert FAKE_SIGNATURE not in rendered

        lines = [json.loads(line) for line in rendered.splitlines() if line.strip()]
        assert lines, rendered
        for line in lines:
            assert "headers" not in line
            if "signature" in line:
                assert line["signature"] == "[REDACTED]"
            if "access_key" in line:
                assert line["access_key"] == "[REDACTED]"


# -- Regression: resubscribe-send failure after reconnect must not kill the
# -- supervisor task (review finding P1) --------------------------------------


def test_resubscribe_failure_after_reconnect_does_not_kill_supervisor() -> None:
    """If the server closes the socket between a successful reconnect and
    the resubscribe command's send completing, the client must treat
    that exactly like another dropped connection -- close it, record
    it, and keep retrying -- rather than letting the background
    supervisor task die uncaught (which would leave the client
    permanently dark with no further reconnect ever attempted)."""

    async def run() -> None:
        conn1 = _FakeConnection()
        conn2 = _RaisingSendConnection()
        conn3 = _FakeConnection()
        connector = _ScriptedConnector([conn1, conn2, conn3])
        sleeper = _RecordingSleeper()

        client = _make_client(
            _FakeSigner(),
            _make_config(ws_reconnect_backoff_min_seconds=0.001, ws_reconnect_backoff_max_seconds=0.01),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=sleeper,
            jitter_source=lambda: 0.0,
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)
            assert len(conn1.sent) == 1

            conn1.push_close_ok()  # drop 1 -> dial conn2 -> resubscribe send raises

            for _ in range(200):
                await asyncio.sleep(0)
                if len(connector.calls) >= 3:
                    break

            # All three connections were dialed: the initial one, the
            # one whose resubscribe send failed, and a third that
            # recovered -- the supervisor task never died.
            assert len(connector.calls) == 3
            assert len(conn3.sent) == 1  # successfully resubscribed on the third connection
            resubscribe_command = json.loads(conn3.sent[0])
            assert resubscribe_command["params"]["market_tickers"] == ["KXBTC-25JAN01"]

            # Two distinct disconnect events: the original clean drop,
            # and the resubscribe failure -- both caller-observable.
            assert len(client.disconnect_events) == 2
            assert client.disconnect_events[0].reason == "closed_ok"
            assert client.disconnect_events[1].reason == "resubscribe_failed"

            # The client is still alive and can still deliver data.
            conn3.push(json.dumps({"type": "ticker", "sid": 1, "msg": {"market_ticker": "KXBTC-25JAN01"}}))
            update = await asyncio.wait_for(task, timeout=1.0)
            assert update.market_ticker == "KXBTC-25JAN01"
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- Regression: bounded per-channel queue, drop-oldest on overflow
# -- (review finding P2) -------------------------------------------------------


def test_channel_queue_is_bounded_and_drops_oldest_on_overflow() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_RecordingSleeper()
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)  # register the queue; task then suspends on queue.get()

            generation = client._generation  # noqa: SLF001
            max_size = ws_client_module._MAX_CHANNEL_QUEUE_SIZE  # noqa: SLF001
            overflow_count = max_size + 50

            # All frames share the same (subscribed) market_ticker so
            # none are dropped by the unmatched-ticker filter; ts_ms
            # distinguishes them for ordering verification instead.
            for i in range(overflow_count):
                frame = json.dumps(
                    {
                        "type": "ticker",
                        "sid": 1,
                        "msg": {"market_ticker": "KXBTC-25JAN01", "ts_ms": i},
                    }
                )
                client._dispatch_frame(frame, generation)  # noqa: SLF001 - proves this never raises

            expected_drops = overflow_count - max_size
            assert client.queue_full_drop_count == expected_drops

            # Drop-oldest means the first item the pending consumer
            # receives is the oldest *retained* one, not the very first
            # pushed (which was evicted).
            update = await asyncio.wait_for(task, timeout=1.0)
            assert update.ts_ms == expected_drops
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_disconnect_with_full_channel_queue_still_delivers_stop_sentinel() -> None:
    """A completely full channel queue must never prevent disconnect()
    from delivering the stop sentinel (a direct consequence of bounding
    the queue for finding P2 above: put_nowait on a full queue would
    otherwise raise asyncio.QueueFull).

    Deliberately does not use a live subscribe_ticker consumer here:
    once any item is queued, an awaiting consumer becomes eligible to
    run on the very next scheduler tick, racing with disconnect()'s own
    internal awaits over whether it drains an item before or after
    disconnect() evicts one -- either outcome would still be correct,
    but that raciness would make this test nondeterministic. Registering
    the queue directly (whitebox, mirroring this file's existing
    ``client._generation``/``client._dispatch_frame`` access pattern)
    with no consumer ever attached removes that race entirely.
    """

    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_RecordingSleeper()
        )
        await client.connect()

        max_size = ws_client_module._MAX_CHANNEL_QUEUE_SIZE  # noqa: SLF001
        queue: "asyncio.Queue[Any]" = asyncio.Queue(maxsize=max_size)
        client._channel_queues[_Channel.TICKER] = queue  # noqa: SLF001
        client._active_channel_tickers[_Channel.TICKER] = ("KXBTC-25JAN01",)  # noqa: SLF001
        for i in range(max_size):
            queue.put_nowait(TickerUpdate(market_ticker="KXBTC-25JAN01", ts_ms=i))
        assert queue.full()

        await client.disconnect()  # must not raise despite the full queue

        remaining: list[Any] = []
        while not queue.empty():
            remaining.append(queue.get_nowait())

        assert len(remaining) == max_size  # size unchanged: one evicted, one (STOP) added
        assert remaining[-1] is ws_client_module._STOP  # noqa: SLF001
        assert remaining[0].ts_ms == 1  # oldest item (ts_ms=0) was evicted to make room

    asyncio.run(run())


# -- Regression: server error message text must never be logged verbatim
# -- (review finding P2) -------------------------------------------------------


def test_error_frame_message_text_never_logged() -> None:
    async def run() -> None:
        stream = io.StringIO()
        configure_logging(level="INFO", stream=stream)
        monkey_logger = get_logger("test.ws_client.error_frame_redaction")
        original_logger = ws_client_module._logger
        ws_client_module._logger = monkey_logger
        adversarial_text = "ADVERSARIAL-UPSTREAM-ERROR-TEXT-SHOULD-NEVER-BE-LOGGED"
        try:
            conn = _FakeConnection()
            connector = _ScriptedConnector([conn])
            client = _make_client(
                _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_RecordingSleeper()
            )
            await client.connect()
            generation = client._generation  # noqa: SLF001
            frame = json.dumps({"id": 1, "type": "error", "msg": {"code": 6, "msg": adversarial_text}})
            client._dispatch_frame(frame, generation)  # noqa: SLF001
            await client.disconnect()
        finally:
            ws_client_module._logger = original_logger

        rendered = stream.getvalue()
        assert adversarial_text not in rendered

        lines = [json.loads(line) for line in rendered.splitlines() if line.strip()]
        error_lines = [line for line in lines if line.get("event") == "ws_error_frame"]
        assert error_lines, rendered
        assert error_lines[0]["code"] == 6
        assert "message" not in error_lines[0]

    asyncio.run(run())


# -- Regression: unexpected exceptions during frame processing must never
# -- crash the receive loop or leave disconnect() re-raising
# -- (review finding: adversarial-frame resilience) ---------------------------


def test_deeply_nested_frame_does_not_crash_receive_loop_or_disconnect() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_RecordingSleeper()
        )
        await client.connect()

        # Pathologically deep JSON nesting makes CPython's json decoder
        # raise RecursionError (a RuntimeError subclass), fed through
        # the real receive path (not a direct _dispatch_frame call) to
        # prove the whole chain -- json decode -> normalizer -> dispatch
        # -- survives.
        malicious_frame = "[" * 200_000
        conn.push(malicious_frame)

        for _ in range(50):
            await asyncio.sleep(0)
            if client.malformed_frame_count >= 1:
                break
        assert client.malformed_frame_count == 1

        # The connection must still be alive/usable afterward.
        gen = client.subscribe_ticker(["KXBTC-25JAN01"])
        task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
        await asyncio.sleep(0)
        conn.push(json.dumps({"type": "ticker", "sid": 1, "msg": {"market_ticker": "KXBTC-25JAN01"}}))
        update = await asyncio.wait_for(task, timeout=1.0)
        assert update.market_ticker == "KXBTC-25JAN01"

        await client.disconnect()  # must succeed cleanly, never re-raise

    asyncio.run(run())


def test_unexpected_dispatch_exception_is_treated_as_a_dropped_connection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Defense in depth, independent of the normalizer's own
    RecursionError fix: any unforeseen exception escaping frame
    processing must be treated as a dropped connection and retried,
    never let the supervisor task die uncaught."""

    async def run() -> None:
        conn1 = _FakeConnection()
        conn2 = _FakeConnection()
        connector = _ScriptedConnector([conn1, conn2])
        client = _make_client(
            _FakeSigner(),
            _make_config(ws_reconnect_backoff_min_seconds=0.001, ws_reconnect_backoff_max_seconds=0.01),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_RecordingSleeper(),
            jitter_source=lambda: 0.0,
        )
        try:
            await client.connect()

            original_dispatch = client._dispatch_frame  # noqa: SLF001
            call_count = 0

            def flaky_dispatch(raw: str | bytes, generation: int) -> None:
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise RuntimeError("simulated unexpected dispatch failure")
                original_dispatch(raw, generation)

            monkeypatch.setattr(client, "_dispatch_frame", flaky_dispatch)

            conn1.push("anything")  # triggers the forced failure on first dispatch

            for _ in range(100):
                await asyncio.sleep(0)
                if len(connector.calls) >= 2:
                    break

            assert len(connector.calls) == 2  # supervisor recovered and reconnected
            assert len(client.disconnect_events) == 1
            assert client.disconnect_events[0].reason == "unexpected_error"
        finally:
            await client.disconnect()  # must succeed cleanly, never re-raise

    asyncio.run(run())

    asyncio.run(run())
