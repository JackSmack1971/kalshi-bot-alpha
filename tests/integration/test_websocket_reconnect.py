"""Integration tests: KalshiDemoWebSocketClient against a local,
controlled WebSocket test server (Phase 1 PR 5).

No live network and no live Kalshi credentials anywhere in this file --
only a synthetic RSA keypair (matching
``tests/integration/test_rest_client_mocked.py``'s pattern) signing
real handshake headers, and a localhost-only ``websockets.serve``
server. This is the standard-gate reconnect evidence per
``docs/PHASE1_PLAN.md`` PR 5; it is distinct from (and does not
replace) the opt-in, PR-6-scoped live demo soak.

Three properties are proven here, each in its own test:

1. ``test_client_reconnects_after_local_server_closes_the_connection``:
   the client reconnects after the local server drops the connection.
2. ``test_disconnect_never_triggers_a_reconnect``: an explicit
   ``disconnect()`` is a clean shutdown -- no further connect() call
   happens afterward, even past a full backoff interval.
3. ``test_stale_generation_frames_are_never_delivered_to_a_caller``:
   a frame tagged with a superseded connection generation is dropped
   rather than delivered, using the real running client's own
   generation counters and dispatch path (see that test's docstring
   for the precise scope of what this proves).
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import Awaitable, Callable, Iterator, Mapping
from typing import Any

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from websockets.asyncio.client import connect as ws_connect
from websockets.asyncio.server import ServerConnection, serve
from websockets.exceptions import ConnectionClosed

from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.credentials.loader import LoadedDemoCredentials
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests
from kalshi_bot.ws.client import KalshiDemoWebSocketClient
from kalshi_bot.ws.models import TickerUpdate

SYNTHETIC_ACCESS_KEY = "SYNTHETIC-WS-INTEGRATION-ACCESS-KEY-0001"

OnSubscribe = Callable[[ServerConnection, int, dict[str, Any]], Awaitable[None]]


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


def _generate_signer() -> RequestSigner:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    credentials = LoadedDemoCredentials(SYNTHETIC_ACCESS_KEY, pem)
    return RequestSigner.from_credentials(credentials)


def _make_config(
    *,
    ws_reconnect_backoff_min_seconds: float = 0.02,
    ws_reconnect_backoff_max_seconds: float = 0.1,
) -> AppConfig:
    return AppConfig(
        rest_timeout_seconds=5.0,
        rest_max_retries=2,
        rest_retry_backoff_min_seconds=0.01,
        rest_retry_backoff_max_seconds=0.08,
        ws_timeout_seconds=5.0,
        ws_reconnect_backoff_min_seconds=ws_reconnect_backoff_min_seconds,
        ws_reconnect_backoff_max_seconds=ws_reconnect_backoff_max_seconds,
        credentials=CredentialReferences(
            access_key_env="TEST_WS_INTEGRATION_ACCESS_KEY_ENV",
            private_key_path_env="TEST_WS_INTEGRATION_PRIVATE_KEY_PATH_ENV",
        ),
    )


def _local_connector(
    local_url: str,
) -> Callable[[str, Mapping[str, str], float], Awaitable[Any]]:
    async def connector(url: str, headers: Mapping[str, str], timeout: float) -> Any:
        # Deliberately ignores `url` (the real, fixed demo host) and
        # dials the local controlled test server instead -- this is
        # exactly the injectable "connect function/factory" test hook
        # described in kalshi_bot.ws.client.KalshiDemoWebSocketClient's
        # constructor docstring.
        return await ws_connect(
            local_url, additional_headers=dict(headers), proxy=None, open_timeout=timeout
        )

    return connector


def _sample_msg_for_channel(channel: str, market_ticker: str) -> dict[str, Any]:
    if channel == "ticker":
        return {"market_ticker": market_ticker}
    return {"trade_id": "trade-1", "market_ticker": market_ticker}


class _RecordingServer:
    """Tracks every accepted connection; per-test behavior is injected
    via ``on_subscribe``, called once per received ``subscribe`` command."""

    def __init__(self) -> None:
        self.connections: list[ServerConnection] = []
        self.on_subscribe: OnSubscribe | None = None

    async def handler(self, ws: ServerConnection) -> None:
        self.connections.append(ws)
        index = len(self.connections)
        try:
            async for message in ws:
                data = json.loads(message)
                if data.get("cmd") == "subscribe" and self.on_subscribe is not None:
                    await self.on_subscribe(ws, index, data)
        except ConnectionClosed:
            return


# -- (a) Reconnect after the local server drops the connection ---------------


async def _run_reconnect_after_server_drop() -> None:
    server = _RecordingServer()

    async def on_subscribe(ws: ServerConnection, index: int, data: dict[str, Any]) -> None:
        channel = data["params"]["channels"][0]
        await ws.send(
            json.dumps({"id": data["id"], "type": "subscribed", "msg": {"channel": channel, "sid": index}})
        )
        if index == 1:
            # Simulate a server-initiated drop right after acking the
            # first subscription -- no data is ever sent on connection 1.
            await ws.close(code=1000, reason="simulated drop")
        else:
            market_ticker = data["params"]["market_tickers"][0]
            await ws.send(
                json.dumps(
                    {
                        "type": channel,
                        "sid": index,
                        "msg": _sample_msg_for_channel(channel, market_ticker),
                    }
                )
            )

    server.on_subscribe = on_subscribe

    async with serve(server.handler, "127.0.0.1", 0) as ws_server:
        port = ws_server.sockets[0].getsockname()[1]
        local_url = f"ws://127.0.0.1:{port}/trade-api/ws/v2"

        signer = _generate_signer()
        client = KalshiDemoWebSocketClient(
            signer, _make_config(), connector=_local_connector(local_url)
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            update = await asyncio.wait_for(gen.__anext__(), timeout=5.0)

            assert isinstance(update, TickerUpdate)
            assert update.market_ticker == "KXBTC-25JAN01"
            # Exactly two connections were accepted: the first (dropped
            # after acking the subscribe) and the second (which is where
            # the delivered ticker update actually came from).
            assert len(server.connections) == 2
            # A single non-caller-initiated disconnect was recorded and
            # is caller-observable via disconnect_events.
            assert len(client.disconnect_events) == 1
            assert client.disconnect_events[0].reason in ("closed_ok", "closed_error")
            assert client.disconnect_events[0].attempt == 1
        finally:
            await client.disconnect()


def test_client_reconnects_after_local_server_closes_the_connection() -> None:
    asyncio.run(_run_reconnect_after_server_drop())


# -- (b) Clean shutdown never triggers a reconnect ----------------------------


async def _run_no_reconnect_after_explicit_disconnect() -> None:
    server = _RecordingServer()

    async def on_subscribe(ws: ServerConnection, index: int, data: dict[str, Any]) -> None:
        channel = data["params"]["channels"][0]
        await ws.send(
            json.dumps({"id": data["id"], "type": "subscribed", "msg": {"channel": channel, "sid": index}})
        )
        # Deliberately never closes or drops -- any shutdown observed in
        # this test must be entirely client-initiated.

    server.on_subscribe = on_subscribe

    async with serve(server.handler, "127.0.0.1", 0) as ws_server:
        port = ws_server.sockets[0].getsockname()[1]
        local_url = f"ws://127.0.0.1:{port}/trade-api/ws/v2"

        signer = _generate_signer()
        config = _make_config(
            ws_reconnect_backoff_min_seconds=0.02, ws_reconnect_backoff_max_seconds=0.05
        )
        client = KalshiDemoWebSocketClient(signer, config, connector=_local_connector(local_url))

        await client.connect()
        gen = client.subscribe_ticker(["KXBTC-25JAN01"])
        task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
        await asyncio.sleep(0.1)  # let the subscribe command land on the server

        await client.disconnect()
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

        # Wait comfortably past a full backoff interval; a reconnect
        # would show up as a second accepted server connection.
        await asyncio.sleep(config.ws_reconnect_backoff_max_seconds * 5)

        assert len(server.connections) == 1
        assert client.disconnect_events == ()


def test_disconnect_never_triggers_a_reconnect() -> None:
    asyncio.run(_run_no_reconnect_after_explicit_disconnect())


# -- (c) Stale-generation frames are never delivered --------------------------


async def _run_stale_generation_frames_are_dropped() -> None:
    server = _RecordingServer()

    async def on_subscribe(ws: ServerConnection, index: int, data: dict[str, Any]) -> None:
        channel = data["params"]["channels"][0]
        await ws.send(
            json.dumps({"id": data["id"], "type": "subscribed", "msg": {"channel": channel, "sid": index}})
        )

    server.on_subscribe = on_subscribe

    async with serve(server.handler, "127.0.0.1", 0) as ws_server:
        port = ws_server.sockets[0].getsockname()[1]
        local_url = f"ws://127.0.0.1:{port}/trade-api/ws/v2"

        signer = _generate_signer()
        client = KalshiDemoWebSocketClient(
            signer, _make_config(), connector=_local_connector(local_url)
        )
        try:
            await client.connect()
            gen = client.subscribe_ticker(["KXBTC-25JAN01"])
            task: "asyncio.Task[Any]" = asyncio.ensure_future(gen.__anext__())
            await asyncio.sleep(0.1)  # let the subscribe command land on the server

            current_generation = client._generation  # noqa: SLF001 - whitebox proof, see module docstring
            stale_generation = current_generation - 1
            stale_frame = json.dumps(
                {"type": "ticker", "sid": 999, "msg": {"market_ticker": "KXBTC-25JAN01"}}
            )

            # This exercises the real, running client's own dispatch
            # path (its real connection, generation counters, and
            # queue routing) with a frame explicitly tagged as
            # originating from a superseded connection generation --
            # the same code path a genuinely stale in-flight frame from
            # an old connection would travel through. It is not a
            # reproduction of a live network race: this client's
            # sequential reconnect design (see ReconnectPolicy's and
            # KalshiDemoWebSocketClient._supervise_connection's
            # docstrings) never dials two connections concurrently, so
            # there is no way to provoke a genuine stale-frame race
            # over a real socket without an artificial, flaky delay.
            # This is therefore a targeted, deterministic proof of the
            # drop invariant itself, complementary to (not a
            # replacement for) test (a) above's genuine end-to-end
            # reconnect proof.
            client._dispatch_frame(stale_frame, stale_generation)  # noqa: SLF001

            assert client.stale_frame_drop_count == 1
            assert not task.done()

            # Prove the same frame, tagged with the CURRENT generation,
            # is genuinely delivered -- isolating that the drop above
            # was specifically about the generation mismatch, not some
            # other rejection.
            client._dispatch_frame(stale_frame, current_generation)  # noqa: SLF001
            update = await asyncio.wait_for(task, timeout=5.0)
            assert isinstance(update, TickerUpdate)
        finally:
            await client.disconnect()


def test_stale_generation_frames_are_never_delivered_to_a_caller() -> None:
    asyncio.run(_run_stale_generation_frames_are_dropped())
