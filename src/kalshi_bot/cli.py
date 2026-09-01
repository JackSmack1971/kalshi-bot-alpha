"""Small operator entry point for the first demo-order acceptance flow."""

from __future__ import annotations

import argparse
import asyncio
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import uuid4

from kalshi_bot.acceptance import run_demo_smoke_order
from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config import load_config
from kalshi_bot.credentials import load_credentials
from kalshi_bot.persistence import LedgerStore
from kalshi_bot.market_data import Side
from kalshi_bot.reconciliation import ReconciliationService
from kalshi_bot.rest import KalshiDemoRestClient
from kalshi_bot.rest.models import Balance, Fill, Order, Position
from kalshi_bot.risk import RiskGateway, RiskLimits
from kalshi_bot.ws import KalshiDemoWebSocketClient


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kalshi-bot")
    command = parser.add_subparsers(dest="command", required=True)
    smoke = command.add_parser("demo-smoke-order")
    smoke.add_argument("--ticker", required=True)
    smoke.add_argument("--price", required=True, type=Decimal)
    smoke.add_argument("--count", required=True, type=int)
    smoke.add_argument("--db", default="kalshi_bot.sqlite3")
    smoke.add_argument(
        "--mock",
        action="store_true",
        help="run the complete lifecycle against an in-memory demo API (no credentials/network)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "demo-smoke-order":
        return 2
    return asyncio.run(_run_smoke(args.ticker, args.price, args.count, Path(args.db), args.mock))


async def _run_smoke(ticker: str, price: Decimal, count: int, db: Path, mock: bool = False) -> int:
    if mock:
        return _run_mock_smoke(ticker, price, count, db)
    config = load_config(
        {
            "rest_timeout_seconds": 10.0,
            "rest_max_retries": 0,
            "rest_retry_backoff_min_seconds": 0.1,
            "rest_retry_backoff_max_seconds": 0.1,
            "ws_timeout_seconds": 10.0,
            "ws_reconnect_backoff_min_seconds": 0.1,
            "ws_reconnect_backoff_max_seconds": 5.0,
            "credentials": {
                "access_key_env": "KALSHI_DEMO_ACCESS_KEY",
                "private_key_path_env": "KALSHI_DEMO_PRIVATE_KEY_PATH",
            },
        }
    )
    credentials = load_credentials(config.credentials)
    signer = RequestSigner.from_credentials(credentials)
    store = LedgerStore.connect(db, migrate=True)
    rest = KalshiDemoRestClient(signer, config)
    def reconcile_reconnect() -> None:
        result = reconciler.on_reconnect()
        if not result.clean:
            raise RuntimeError("reconnect reconciliation suspended trading")

    websocket = KalshiDemoWebSocketClient(signer, config, on_reconnect=reconcile_reconnect)
    reconciler = ReconciliationService(store, rest)
    try:
        startup = reconciler.on_startup()
        if not startup.clean:
            raise RuntimeError("startup reconciliation suspended trading")
        await websocket.connect()
        books = websocket.subscribe_orderbooks([ticker])
        book = await asyncio.wait_for(books.__anext__(), timeout=config.ws_timeout_seconds)
        result = run_demo_smoke_order(
            client=rest,
            store=store,
            ticker=ticker,
            price=price,
            count=count,
            book=book,
            risk=RiskGateway(),
            limits=RiskLimits(),
        )
        print(f"DEMO MODE acceptance clean: {result.client_order_id}")
        return 0
    finally:
        shutdown_error: Exception | None = None
        try:
            reconciler.before_shutdown()
        except Exception as exc:
            shutdown_error = exc
        try:
            await websocket.disconnect()
        finally:
            rest.close()
            store.close()
        if shutdown_error is not None:
            raise shutdown_error


class _MockDemoClient:
    """Deterministic local stand-in for the explicitly opt-in acceptance path."""

    base_url = "https://external-api.demo.kalshi.co/trade-api/v2"

    def __init__(self, store: LedgerStore) -> None:
        self.store = store
        self.order = Order(
            order_id="mock-exchange-order-1",
            client_order_id=None,
            ticker=None,
            status="cancelled",
        )

    def create_limit_order(self, **kwargs: Any) -> Order:
        client_order_id = str(kwargs["client_order_id"])
        self.store.record_order(
            client_order_id,
            str(kwargs["intent_id"]),
            str(kwargs["feature_snapshot_id"]),
            str(kwargs["risk_decision_id"]),
            str(kwargs["ticker"]),
            Side.YES,
            int(kwargs["count"]),
            Decimal(str(kwargs["price"])),
            "ACKNOWLEDGED",
        )
        self.store.record_transition(
            str(uuid4()), client_order_id, None, "ACKNOWLEDGED", "mock-acknowledgement"
        )
        self.order = Order(
            order_id="mock-exchange-order-1",
            client_order_id=client_order_id,
            ticker=str(kwargs["ticker"]),
            side="bid",
            status="resting",
            initial_count_fp=str(kwargs["count"]),
            yes_price_dollars=str(kwargs["price"]),
        )
        return self.order

    def cancel_order(self, *, order_id: str) -> Order:
        if order_id != self.order.order_id:
            raise ValueError("unknown mock order")
        self.order = self.order.model_copy(update={"status": "cancelled"})
        return self.order

    def get_order(self, *, order_id: str) -> Order:
        if order_id != self.order.order_id:
            raise ValueError("unknown mock order")
        return self.order

    def list_open_orders(self) -> tuple[Order, ...]:
        return () if self.order.status == "cancelled" else (self.order,)

    def get_fills(self) -> tuple[Fill, ...]:
        return ()

    def get_positions(self) -> tuple[Position, ...]:
        return ()

    def get_balance(self) -> Balance:
        return Balance(balance_dollars="0")


def _run_mock_smoke(ticker: str, price: Decimal, count: int, db: Path) -> int:
    from datetime import datetime, timezone
    from kalshi_bot.market_data import BookQuality, OrderBookLevel, OrderBookSnapshot

    store = LedgerStore.connect(db, migrate=True)
    client = _MockDemoClient(store)
    reconciler = ReconciliationService(store, client)
    book = OrderBookSnapshot(
        ticker,
        datetime.now(timezone.utc),
        yes_bids=(OrderBookLevel.parse("0.40", "1"),),
        no_bids=(OrderBookLevel.parse("0.50", "1"),),
        quality=BookQuality.HEALTHY,
    )
    try:
        if not reconciler.on_startup().clean:
            raise RuntimeError("startup reconciliation suspended trading")
        result = run_demo_smoke_order(
            client=client,
            store=store,
            ticker=ticker,
            price=price,
            count=count,
            book=book,
            risk=RiskGateway(),
            limits=RiskLimits(),
        )
        print(f"DEMO MODE mock acceptance clean: {result.client_order_id}")
        return 0
    finally:
        shutdown_error: Exception | None = None
        try:
            if not reconciler.before_shutdown().clean:
                shutdown_error = RuntimeError("shutdown reconciliation suspended trading")
        except Exception as exc:
            shutdown_error = exc
        store.close()
        if shutdown_error is not None:
            raise shutdown_error


if __name__ == "__main__":
    raise SystemExit(main())
