"""Small operator entry point for the first demo-order acceptance flow."""

from __future__ import annotations

import argparse
import asyncio
from decimal import Decimal
from pathlib import Path

from kalshi_bot.acceptance import run_demo_smoke_order
from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config import load_config
from kalshi_bot.credentials import load_credentials
from kalshi_bot.persistence import LedgerStore
from kalshi_bot.reconciliation import ReconciliationService
from kalshi_bot.rest import KalshiDemoRestClient
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command != "demo-smoke-order":
        return 2
    return asyncio.run(_run_smoke(args.ticker, args.price, args.count, Path(args.db)))


async def _run_smoke(ticker: str, price: Decimal, count: int, db: Path) -> int:
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


if __name__ == "__main__":
    raise SystemExit(main())
