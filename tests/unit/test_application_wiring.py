"""Deterministic tests for the Phase 1 composition root."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from types import SimpleNamespace
from typing import Any

import pytest

from kalshi_bot.application import Phase1StartupError, run_phase1_supervisor
from kalshi_bot.config import load_config


CONFIG = {
    "log_level": "INFO",
    "rest_timeout_seconds": 1.0,
    "rest_max_retries": 0,
    "rest_retry_backoff_min_seconds": 0.1,
    "rest_retry_backoff_max_seconds": 0.1,
    "ws_timeout_seconds": 1.0,
    "ws_reconnect_backoff_min_seconds": 0.1,
    "ws_reconnect_backoff_max_seconds": 0.1,
    "credentials": {
        "access_key_env": "KALSHI_DEMO_ACCESS_KEY",
        "private_key_path_env": "KALSHI_DEMO_PRIVATE_KEY_PATH",
    },
}


class _FakeStream:
    def __aiter__(self) -> AsyncIterator[object]:
        return self

    async def __anext__(self) -> object:
        await asyncio.Future()
        raise AssertionError("unreachable")


class _FakeRest:
    instances: list[_FakeRest] = []

    def __init__(self, signer: object, config: object) -> None:
        self.signer = signer
        self.config = config
        self.closed = False
        self.__class__.instances.append(self)

    def get_exchange_status(self) -> SimpleNamespace:
        return SimpleNamespace(exchange_active=True, trading_active=True)

    def list_markets(self) -> tuple[SimpleNamespace, ...]:
        return (SimpleNamespace(ticker="TICKER-1"),)

    def close(self) -> None:
        self.closed = True


class _FakeWebSocket:
    instances: list[_FakeWebSocket] = []

    def __init__(self, signer: object, config: object) -> None:
        self.signer = signer
        self.config = config
        self.connected = False
        self.disconnected = False
        self.ticker_tickers: list[str] | None = None
        self.trade_tickers: list[str] | None = None
        self.__class__.instances.append(self)

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.disconnected = True

    def subscribe_ticker(self, tickers: list[str]) -> _FakeStream:
        self.ticker_tickers = tickers
        return _FakeStream()

    def subscribe_trades(self, tickers: list[str]) -> _FakeStream:
        self.trade_tickers = tickers
        return _FakeStream()


def _install_fakes(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    import kalshi_bot.application as application

    application_module: Any = application
    credentials = object()
    signer = object()
    monkeypatch.setattr(application, "load_credentials", lambda refs: credentials)
    monkeypatch.setattr(application_module.RequestSigner, "from_credentials", lambda value: signer)
    monkeypatch.setattr(application, "KalshiDemoRestClient", _FakeRest)
    monkeypatch.setattr(application, "KalshiDemoWebSocketClient", _FakeWebSocket)
    _FakeRest.instances.clear()
    _FakeWebSocket.instances.clear()
    return {"credentials": credentials, "signer": signer}


def test_supervisor_wires_read_only_stack_and_cleans_up(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = _install_fakes(monkeypatch)
    config = load_config(CONFIG)

    async def run() -> None:
        task = asyncio.create_task(run_phase1_supervisor(config))
        while not _FakeWebSocket.instances or not _FakeWebSocket.instances[0].connected:
            await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(run())

    rest = _FakeRest.instances[0]
    websocket = _FakeWebSocket.instances[0]
    assert rest.signer is expected["signer"]
    assert websocket.signer is expected["signer"]
    assert websocket.ticker_tickers == ["TICKER-1"]
    assert websocket.trade_tickers == ["TICKER-1"]
    assert websocket.disconnected
    assert rest.closed


def test_credential_failure_prevents_transport_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import kalshi_bot.application as application

    secret = "SYNTHETIC-SECRET-MARKER-APPLICATION-FAILURE"
    error = RuntimeError(f"credential load failed: {secret}")
    monkeypatch.setattr(application, "load_credentials", lambda refs: (_ for _ in ()).throw(error))
    monkeypatch.setattr(application, "KalshiDemoRestClient", _FakeRest)
    monkeypatch.setattr(application, "KalshiDemoWebSocketClient", _FakeWebSocket)
    _FakeRest.instances.clear()
    _FakeWebSocket.instances.clear()

    with pytest.raises(Phase1StartupError) as excinfo:
        asyncio.run(run_phase1_supervisor(load_config(CONFIG)))

    assert secret not in str(excinfo.value)
    assert secret not in repr(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)
    assert not _FakeRest.instances
    assert not _FakeWebSocket.instances


def test_exchange_failure_closes_rest_without_connecting_websocket(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import kalshi_bot.application as application

    application_module: Any = application
    monkeypatch.setattr(application, "load_credentials", lambda refs: object())
    monkeypatch.setattr(
        application_module.RequestSigner, "from_credentials", lambda value: object()
    )

    class FailingRest(_FakeRest):
        def get_exchange_status(self) -> SimpleNamespace:
            raise RuntimeError("status unavailable")

    monkeypatch.setattr(application, "KalshiDemoRestClient", FailingRest)
    monkeypatch.setattr(application, "KalshiDemoWebSocketClient", _FakeWebSocket)
    FailingRest.instances.clear()
    _FakeWebSocket.instances.clear()

    with pytest.raises(Phase1StartupError, match=r"phase1 startup failed \(RuntimeError\)"):
        asyncio.run(run_phase1_supervisor(load_config(CONFIG)))

    assert FailingRest.instances[0].closed
    assert not _FakeWebSocket.instances


def test_inactive_exchange_fails_closed_and_closes_rest(monkeypatch: pytest.MonkeyPatch) -> None:
    import kalshi_bot.application as application

    application_module: Any = application
    monkeypatch.setattr(application, "load_credentials", lambda refs: object())
    monkeypatch.setattr(
        application_module.RequestSigner, "from_credentials", lambda value: object()
    )

    class InactiveRest(_FakeRest):
        def get_exchange_status(self) -> SimpleNamespace:
            return SimpleNamespace(exchange_active=False, trading_active=False)

    monkeypatch.setattr(application, "KalshiDemoRestClient", InactiveRest)
    monkeypatch.setattr(application, "KalshiDemoWebSocketClient", _FakeWebSocket)
    InactiveRest.instances.clear()
    _FakeWebSocket.instances.clear()

    with pytest.raises(Phase1StartupError, match="inactive"):
        asyncio.run(run_phase1_supervisor(load_config(CONFIG)))

    assert InactiveRest.instances[0].closed
    assert not _FakeWebSocket.instances
