"""Real REST-client acceptance lifecycle against a deterministic HTTP mock."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import cast

import httpx

from kalshi_bot.acceptance import run_demo_smoke_order
from kalshi_bot.auth.signer import RequestSigner, SignedHeaders
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.market_data import BookQuality, OrderBookLevel, OrderBookSnapshot
from kalshi_bot.persistence import LedgerStore
from kalshi_bot.reconciliation import ReconciliationService
from kalshi_bot.rest.client import KalshiDemoRestClient
from kalshi_bot.risk import RiskGateway, RiskLimits


class _Signer:
    def sign(self, method: str, path: str, timestamp_ms: int) -> SignedHeaders:
        return SignedHeaders("SYNTHETIC-ACCESS-KEY", "SYNTHETIC-SIGNATURE", timestamp_ms)


def _config() -> AppConfig:
    return AppConfig(
        rest_timeout_seconds=1.0,
        rest_max_retries=0,
        rest_retry_backoff_min_seconds=0.01,
        rest_retry_backoff_max_seconds=0.01,
        ws_timeout_seconds=1.0,
        ws_reconnect_backoff_min_seconds=0.01,
        ws_reconnect_backoff_max_seconds=0.01,
        credentials=CredentialReferences(
            access_key_env="SYNTHETIC_ACCESS_KEY_ENV",
            private_key_path_env="SYNTHETIC_PRIVATE_KEY_ENV",
        ),
    )


def test_real_rest_client_completes_mocked_demo_acceptance_lifecycle(tmp_path: Path) -> None:
    state = {"open": False, "client_order_id": ""}
    requests: list[tuple[str, str]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        requests.append((request.method, path))
        if request.method == "POST" and path.endswith("/portfolio/events/orders"):
            payload = json.loads(request.content)
            state["client_order_id"] = payload["client_order_id"]
            state["open"] = True
            return httpx.Response(
                200,
                json={
                    "order": {
                        "order_id": "exchange-order-1",
                        "client_order_id": state["client_order_id"],
                        "ticker": "KXBTC-TEST",
                        "side": "yes",
                        "status": "resting",
                        "initial_count_fp": "1",
                        "yes_price_dollars": "0.40",
                    }
                },
            )
        if request.method == "DELETE" and path.endswith("/exchange-order-1"):
            state["open"] = False
            return httpx.Response(
                200,
                json={"order": {"order_id": "exchange-order-1", "status": "canceled"}},
            )
        if request.method == "GET" and path.endswith("/exchange-order-1"):
            return httpx.Response(
                200,
                json={"order": {"order_id": "exchange-order-1", "status": "canceled"}},
            )
        if request.method == "GET" and path.endswith("/portfolio/orders"):
            order = {
                "order_id": "exchange-order-1",
                "client_order_id": state["client_order_id"],
                "ticker": "KXBTC-TEST",
                "side": "yes",
                "status": "resting",
                "initial_count_fp": "1",
                "yes_price_dollars": "0.40",
            }
            return httpx.Response(200, json={"orders": [order] if state["open"] else []})
        if request.method == "GET" and path.endswith("/portfolio/fills"):
            return httpx.Response(200, json={"fills": []})
        if request.method == "GET" and path.endswith("/portfolio/positions"):
            return httpx.Response(200, json={"market_positions": []})
        if request.method == "GET" and path.endswith("/portfolio/balance"):
            return httpx.Response(200, json={"balance_dollars": "0"})
        raise AssertionError(f"unexpected mocked request: {request.method} {path}")

    store = LedgerStore.connect(tmp_path / "acceptance.sqlite3", migrate=True)
    client = KalshiDemoRestClient(
        cast(RequestSigner, _Signer()), _config(), transport=httpx.MockTransport(handler)
    )
    book = OrderBookSnapshot(
        "KXBTC-TEST",
        datetime.now(timezone.utc),
        yes_bids=(OrderBookLevel.parse("0.40", "1"),),
        no_bids=(OrderBookLevel.parse("0.50", "1"),),
        quality=BookQuality.HEALTHY,
    )
    try:
        assert ReconciliationService(store, client).on_startup().clean
        result = run_demo_smoke_order(
            client=client,
            store=store,
            ticker="KXBTC-TEST",
            price=Decimal("0.40"),
            count=1,
            book=book,
            risk=RiskGateway(),
            limits=RiskLimits(),
        )
        assert result.reconciliation.clean
        assert requests.count(("POST", "/trade-api/v2/portfolio/events/orders")) == 1
        assert requests.count(("DELETE", "/trade-api/v2/portfolio/orders/exchange-order-1")) == 1
        assert not state["open"]
        assert not store.local_open_orders()
        assert not store.replay().positions
    finally:
        client.close()
        store.close()
