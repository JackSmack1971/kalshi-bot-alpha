from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace

from kalshi_bot.acceptance import run_demo_smoke_order
from kalshi_bot.market_data import (
    BookQuality,
    FixedPointPrice,
    OrderBookLevel,
    OrderBookSnapshot,
    Side,
)
from kalshi_bot.persistence import LedgerStore
from kalshi_bot.risk import RiskGateway, RiskLimits


def test_demo_smoke_order_is_exactly_one_post_only_order_and_cleans_up(tmp_path: Path) -> None:
    store = LedgerStore.connect(tmp_path / "acceptance.sqlite3", migrate=True)
    calls: list[str] = []
    try:

        def create_limit_order(**kwargs: object) -> SimpleNamespace:
            calls.append("create")
            assert kwargs["count"] == 1
            store.record_order(
                str(kwargs["client_order_id"]),
                str(kwargs["intent_id"]),
                str(kwargs["feature_snapshot_id"]),
                str(kwargs["risk_decision_id"]),
                "KXBTC-TEST",
                Side.YES,
                1,
                Decimal("0.40"),
                "ACKNOWLEDGED",
            )
            return SimpleNamespace(order_id="exchange-1", client_order_id=kwargs["client_order_id"])

        def cancel_order(*, order_id: str) -> SimpleNamespace:
            calls.append("cancel")
            assert order_id == "exchange-1"
            return SimpleNamespace(status="canceled")

        def get_order(*, order_id: str) -> SimpleNamespace:
            assert order_id == "exchange-1"
            return SimpleNamespace(status="canceled")

        client = SimpleNamespace(
            base_url="https://external-api.demo.kalshi.co/trade-api/v2",
            create_limit_order=create_limit_order,
            cancel_order=cancel_order,
            get_order=get_order,
            list_open_orders=lambda: (),
            get_fills=lambda: (),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        book = OrderBookSnapshot(
            "KXBTC-TEST",
            datetime.now(timezone.utc),
            yes_bids=(OrderBookLevel.parse("0.40", "1"),),
            no_bids=(OrderBookLevel.parse("0.50", "1"),),
            quality=BookQuality.HEALTHY,
        )
        result = run_demo_smoke_order(
            client=client,
            store=store,
            ticker="KXBTC-TEST",
            price=FixedPointPrice.parse("0.40").value,
            count=1,
            book=book,
            risk=RiskGateway(),
            limits=RiskLimits(),
        )
        assert calls == ["create", "cancel"]
        assert result.reconciliation.clean
        assert not store.replay().positions
    finally:
        store.close()
