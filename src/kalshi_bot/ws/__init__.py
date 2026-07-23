"""Read-only demo Kalshi WebSocket client (Phase 1 PR 5).

Public API: :class:`~kalshi_bot.ws.client.KalshiDemoWebSocketClient`,
:class:`~kalshi_bot.ws.client.ReconnectPolicy`, and the two typed
subscription event models this client ever yields
(:class:`~kalshi_bot.ws.models.TickerUpdate`,
:class:`~kalshi_bot.ws.models.TradeUpdate`). There is no
``orderbook_delta`` subscription, order-book reconstruction, or generic
``subscribe(channels, tickers)`` surface anywhere in this package.

**Deviation from ``docs/PHASE1_PLAN.md``'s literal PR 5 paths.** The
plan text names ``src/kalshi_bot/kalshi/websocket_client.py`` and
``src/kalshi_bot/market_data/normalizer.py``. This package intentionally
does not use those paths. The already-merged PR 4 (the REST client)
itself departed from its own plan's stated
``src/kalshi_bot/kalshi/`` + ``src/kalshi_bot/market_data/`` split and
instead landed as a single cohesive ``src/kalshi_bot/rest/`` package
(``rest/client.py``, ``rest/models.py``, ``rest/errors.py``,
``rest/__init__.py``). This package (``src/kalshi_bot/ws/``) follows
that established, already-merged convention for the WebSocket
transport: ``ws/client.py``, ``ws/models.py``, ``ws/errors.py``,
``ws/normalizer.py``, ``ws/__init__.py`` -- the same shape as
``kalshi_bot.rest``, so the two Phase 1 transports are structurally
consistent with each other rather than with the plan's original,
superseded two-package split. Test paths remain exactly as specified in
``docs/PHASE1_PLAN.md`` (``tests/unit/test_websocket_client.py``,
``tests/unit/test_subscriptions.py``,
``tests/contract/test_ws_message_schema.py``,
``tests/integration/test_websocket_reconnect.py``); only the
implementation package location changed.
"""

from kalshi_bot.ws.client import KalshiDemoWebSocketClient, ReconnectPolicy
from kalshi_bot.ws.errors import (
    DemoHostValidationError,
    KalshiWsError,
    RequestValidationError,
    WebSocketClientStateError,
    WebSocketConnectionError,
    WebSocketDisconnected,
)
from kalshi_bot.ws.models import TickerUpdate, TradeUpdate

__all__ = [
    "KalshiDemoWebSocketClient",
    "ReconnectPolicy",
    "DemoHostValidationError",
    "KalshiWsError",
    "RequestValidationError",
    "WebSocketClientStateError",
    "WebSocketConnectionError",
    "WebSocketDisconnected",
    "TickerUpdate",
    "TradeUpdate",
]
