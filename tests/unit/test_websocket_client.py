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

    asyncio.run(run())
