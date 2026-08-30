"""Phase 1 read-only application composition root.

This module wires the already-reviewed Phase 1 foundations and transports
without adding a strategy, eligibility, persistence, or order capability.
Startup is fail-closed: a failure before the WebSocket is healthy prevents
the supervisor from entering its streaming wait state.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator

from kalshi_bot.auth import RequestSigner
from kalshi_bot.config import AppConfig
from kalshi_bot.credentials import load_credentials
from kalshi_bot.observability import configure_logging, get_logger
from kalshi_bot.rest import KalshiDemoRestClient
from kalshi_bot.ws import KalshiDemoWebSocketClient

__all__ = ["Phase1StartupError", "run_phase1_supervisor"]

_logger = get_logger(__name__)


class Phase1StartupError(RuntimeError):
    """Raised when the read-only Phase 1 runtime cannot start safely."""


async def _consume_stream(events: AsyncIterator[object], channel: str) -> None:
    """Keep one approved stream subscription active until it ends."""
    async for _event in events:
        _logger.debug("phase1_stream_event", channel=channel)


async def run_phase1_supervisor(config: AppConfig) -> None:
    """Start and supervise Phase 1's read-only market-data runtime.

    The caller supplies already-validated, non-secret :class:`AppConfig`.
    Credentials are loaded only through the credential loader, and only the
    resulting signer is passed to the demo-specific transports. The function
    remains active while both approved subscriptions are running and cleans
    up both transports on cancellation or startup failure.
    """
    rest: KalshiDemoRestClient | None = None
    websocket: KalshiDemoWebSocketClient | None = None
    stream_tasks: tuple[asyncio.Task[None], ...] = ()

    try:
        configure_logging(level=config.log_level)

        credentials = load_credentials(config.credentials)
        signer = RequestSigner.from_credentials(credentials)
        rest = KalshiDemoRestClient(signer, config)
        status = rest.get_exchange_status()
        if not status.exchange_active or not status.trading_active:
            raise Phase1StartupError("demo exchange or trading is inactive")

        markets = rest.list_markets()
        tickers = [market.ticker for market in markets]
        if not tickers:
            raise Phase1StartupError("market discovery returned no markets")

        websocket = KalshiDemoWebSocketClient(signer, config)
        await websocket.connect()
        stream_tasks = (
            asyncio.create_task(_consume_stream(websocket.subscribe_ticker(tickers), "ticker")),
            asyncio.create_task(_consume_stream(websocket.subscribe_trades(tickers), "trade")),
        )
        _logger.info("phase1_started", mode="DEMO MODE", market_count=len(tickers))

        done, _pending = await asyncio.wait(stream_tasks, return_when=asyncio.FIRST_EXCEPTION)
        for task in done:
            exception = task.exception()
            if exception is not None:
                raise Phase1StartupError(
                    "approved market-data stream stopped unexpectedly"
                ) from None
        raise Phase1StartupError("approved market-data stream stopped unexpectedly")
    except Phase1StartupError:
        raise
    except Exception as exc:
        # Boundary exceptions from injected transports or dependencies may
        # include request details. Preserve only their stable type name.
        raise Phase1StartupError(f"phase1 startup failed ({type(exc).__name__})") from None
    finally:
        for task in stream_tasks:
            if not task.done():
                task.cancel()
        if stream_tasks:
            await asyncio.gather(*stream_tasks, return_exceptions=True)
        if websocket is not None:
            await websocket.disconnect()
        if rest is not None:
            rest.close()
