"""Tests for KalshiDemoWebSocketClient.subscribe_ticker/subscribe_trades
(Phase 1 PR 5): parameter validation, exact subscribe-command shape,
resubscription-after-reconnect discipline (no duplicate-subscription
amplification), and clean-shutdown behavior for active iterators.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import AsyncIterator, Iterator, Mapping
from typing import Any

import pytest

from kalshi_bot.auth.signer import SignedHeaders
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests
from kalshi_bot.ws.client import KalshiDemoWebSocketClient
from kalshi_bot.ws.errors import RequestValidationError

FAKE_ACCESS_KEY = "FAKE-ACCESS-KEY-FOR-SUBSCRIPTION-TESTS"
FAKE_SIGNATURE = "FAKE-SIGNATURE-FOR-SUBSCRIPTION-TESTS"


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


class _FakeSigner:
    def sign(self, method: str, path: str, timestamp_ms: int) -> SignedHeaders:
        return SignedHeaders(
            access_key=FAKE_ACCESS_KEY, signature=FAKE_SIGNATURE, timestamp_ms=timestamp_ms
        )


class _FakeClock:
    def __init__(self, start: int = 1_700_000_000_000) -> None:
        self._value = start

    def __call__(self) -> int:
        self._value += 1
        return self._value


async def _no_sleep(seconds: float) -> None:
    await asyncio.sleep(0)


def _make_config(**overrides: Any) -> AppConfig:
    defaults: dict[str, Any] = {
        "rest_timeout_seconds": 5.0,
        "rest_max_retries": 2,
        "rest_retry_backoff_min_seconds": 0.01,
        "rest_retry_backoff_max_seconds": 0.08,
        "ws_timeout_seconds": 5.0,
        "ws_reconnect_backoff_min_seconds": 0.001,
        "ws_reconnect_backoff_max_seconds": 0.01,
        "credentials": CredentialReferences(
            access_key_env="TEST_WS_SUBSCRIPTIONS_ACCESS_KEY_ENV",
            private_key_path_env="TEST_WS_SUBSCRIPTIONS_PRIVATE_KEY_PATH_ENV",
        ),
    }
    defaults.update(overrides)
    return AppConfig(**defaults)


class _CloseOk:
    __slots__ = ()


_CLOSE_OK = _CloseOk()


class _FakeConnection:
    def __init__(self) -> None:
        self._incoming: asyncio.Queue[object] = asyncio.Queue()
        self.sent: list[dict[str, Any]] = []

    def push(self, raw: str) -> None:
        self._incoming.put_nowait(raw)

    def push_close_ok(self) -> None:
        self._incoming.put_nowait(_CLOSE_OK)

    async def send(self, message: str) -> None:
        self.sent.append(json.loads(message))

    async def close(self, code: int = 1000, reason: str = "") -> None:
        pass

    async def __aiter__(self) -> AsyncIterator[str]:
        while True:
            item = await self._incoming.get()
            if item is _CLOSE_OK:
                return
            assert isinstance(item, str)
            yield item


class _ScriptedConnector:
    def __init__(self, items: list[_FakeConnection | Exception]) -> None:
        self._items = list(items)
        self.calls: list[tuple[str, dict[str, str], float]] = []

    async def __call__(self, url: str, headers: Mapping[str, str], timeout: float) -> Any:
        self.calls.append((url, dict(headers), timeout))
        item = self._items.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


async def _cancel_and_await(task: "asyncio.Task[Any]") -> None:
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


def _ticker_frame(market_ticker: str) -> str:
    return json.dumps({"type": "ticker", "sid": 1, "msg": {"market_ticker": market_ticker}})


def _make_client(signer: Any, config: AppConfig, **kwargs: Any) -> KalshiDemoWebSocketClient:
    """Constructs the client with a duck-typed fake signer -- see
    ``tests/unit/test_websocket_client.py``'s identical helper for the
    full rationale (isolates the resulting mypy ``arg-type`` mismatch
    to one place, matching ``tests/unit/test_rest_client.py``'s
    equivalent convention)."""
    return KalshiDemoWebSocketClient(signer, config, **kwargs)


# -- Validation: raised lazily, on first iteration, before any I/O -----------


@pytest.mark.parametrize(
    "bad_tickers",
    [
        [],
        [""],
        [" KXBTC-25JAN01 "],
        ["KXBTC-25JAN01", "KXBTC-25JAN01"],
    ],
)
def test_subscribe_ticker_rejects_invalid_tickers_lists(bad_tickers: list[str]) -> None:
    async def run() -> None:
        connector = _ScriptedConnector([_FakeConnection()])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            with pytest.raises(RequestValidationError):
                async for _ in client.subscribe_ticker(bad_tickers):
                    pass
        finally:
            await client.disconnect()

    asyncio.run(run())


@pytest.mark.parametrize(
    "bad_tickers",
    [[], [""], ["KXBTC-25JAN01", "KXBTC-25JAN01"]],
)
def test_subscribe_trades_rejects_invalid_tickers_lists(bad_tickers: list[str]) -> None:
    async def run() -> None:
        connector = _ScriptedConnector([_FakeConnection()])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            with pytest.raises(RequestValidationError):
                async for _ in client.subscribe_trades(bad_tickers):
                    pass
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_subscribe_generator_construction_does_not_validate_until_iterated() -> None:
    async def run() -> None:
        connector = _ScriptedConnector([_FakeConnection()])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker([])  # invalid, but constructing must not raise yet
            with pytest.raises(RequestValidationError):
                await gen.__anext__()
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- Exact documented subscribe-command shape ---------------------------------


def test_subscribe_ticker_sends_exact_documented_command_shape() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01", "KXETH-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)
            await asyncio.sleep(0)

            assert len(conn.sent) == 1
            command = conn.sent[0]
            assert command["cmd"] == "subscribe"
            assert command["params"]["channels"] == ["ticker"]
            assert command["params"]["market_tickers"] == ["KXBTC-25JAN01", "KXETH-25JAN01"]
            assert isinstance(command["id"], int)

            await _cancel_and_await(task)
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_subscribe_trades_sends_exact_documented_command_shape() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            gen = client.subscribe_trades(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)
            await asyncio.sleep(0)

            assert len(conn.sent) == 1
            command = conn.sent[0]
            assert command["cmd"] == "subscribe"
            assert command["params"]["channels"] == ["trade"]
            assert command["params"]["market_tickers"] == ["KXBTC-25JAN01"]

            await _cancel_and_await(task)
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_no_command_ever_requests_orderbook_delta_or_any_other_channel() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            ticker_gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            trade_gen = client.subscribe_trades(["KXBTC-25JAN01"])
            ticker_task: "asyncio.Task[Any]" = asyncio.ensure_future(ticker_gen.__anext__())
            trade_task: "asyncio.Task[Any]" = asyncio.ensure_future(trade_gen.__anext__())
            await asyncio.sleep(0)
            await asyncio.sleep(0)

            all_channels = {
                channel for command in conn.sent for channel in command["params"]["channels"]
            }
            assert all_channels == {"ticker", "trade"}

            await _cancel_and_await(ticker_task)
            await _cancel_and_await(trade_task)
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- End-to-end normalized delivery --------------------------------------------


def test_subscribe_ticker_yields_normalized_ticker_updates() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)

            conn.push(_ticker_frame("KXBTC-25JAN01"))
            update = await asyncio.wait_for(task, timeout=1.0)

            assert update.market_ticker == "KXBTC-25JAN01"
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- No duplicate-subscription amplification across reconnects ---------------


def test_resubscribe_after_reconnect_sends_exactly_one_command_with_current_tickers() -> None:
    async def run() -> None:
        conn1 = _FakeConnection()
        conn2 = _FakeConnection()
        connector = _ScriptedConnector([conn1, conn2])
        client = _make_client(
            _FakeSigner(),
            _make_config(
                ws_reconnect_backoff_min_seconds=0.001, ws_reconnect_backoff_max_seconds=0.01
            ),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_no_sleep,
            jitter_source=lambda: 0.0,
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01", "KXETH-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)

            assert len(conn1.sent) == 1
            first_command = conn1.sent[0]
            assert first_command["params"]["market_tickers"] == [
                "KXBTC-25JAN01",
                "KXETH-25JAN01",
            ]

            conn1.push_close_ok()

            for _ in range(100):
                await asyncio.sleep(0)
                if conn2.sent:
                    break

            assert len(conn2.sent) == 1  # exactly one resubscribe command -- no accumulation
            second_command = conn2.sent[0]
            assert second_command["params"]["channels"] == ["ticker"]
            assert second_command["params"]["market_tickers"] == [
                "KXBTC-25JAN01",
                "KXETH-25JAN01",
            ]

            await _cancel_and_await(task)
        finally:
            await client.disconnect()

    asyncio.run(run())


def test_repeated_reconnects_never_accumulate_duplicate_subscribe_commands() -> None:
    async def run() -> None:
        conn1 = _FakeConnection()
        conn2 = _FakeConnection()
        conn3 = _FakeConnection()
        connector = _ScriptedConnector([conn1, conn2, conn3])
        client = _make_client(
            _FakeSigner(),
            _make_config(
                ws_reconnect_backoff_min_seconds=0.001, ws_reconnect_backoff_max_seconds=0.01
            ),
            connector=connector,
            clock_ms=_FakeClock(),
            sleeper=_no_sleep,
            jitter_source=lambda: 0.0,
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0)

            conn1.push_close_ok()
            for _ in range(100):
                await asyncio.sleep(0)
                if conn2.sent:
                    break
            conn2.push_close_ok()
            for _ in range(100):
                await asyncio.sleep(0)
                if conn3.sent:
                    break

            assert len(conn1.sent) == 1
            assert len(conn2.sent) == 1
            assert len(conn3.sent) == 1
            for conn in (conn1, conn2, conn3):
                assert conn.sent[0]["params"]["market_tickers"] == ["KXBTC-25JAN01"]

            await _cancel_and_await(task)
        finally:
            await client.disconnect()

    asyncio.run(run())


# -- Clean shutdown releases active iterators ---------------------------------


def test_disconnect_ends_active_subscribe_iterators_cleanly() -> None:
    async def run() -> None:
        conn = _FakeConnection()
        connector = _ScriptedConnector([conn])
        client = _make_client(
            _FakeSigner(), _make_config(), connector=connector, clock_ms=_FakeClock(), sleeper=_no_sleep
        )
        await client.connect()

        received: list[Any] = []

        async def consume() -> None:
            async for update in client.subscribe_ticker(["KXBTC-25JAN01"]):
                received.append(update)

        consumer_task: "asyncio.Task[Any]" = asyncio.ensure_future(consume())
        await asyncio.sleep(0)

        await client.disconnect()
        await asyncio.wait_for(consumer_task, timeout=1.0)  # must return cleanly, not raise

        assert received == []

    asyncio.run(run())
