from datetime import datetime, timezone
from decimal import Decimal
from collections.abc import Generator
from pathlib import Path

import pytest

from kalshi_bot.execution import LocalSimulator, OrderState, TradeIntent
from kalshi_bot.market_data import BookQuality, Side
from kalshi_bot.persistence import AccountSnapshot, Direction, LedgerStore
from kalshi_bot.risk import (
    MarketState,
    PortfolioState,
    RiskDecision,
    RiskGateway,
    RiskLimits,
    RuntimeState,
)


def make_intent(count: int = 10) -> TradeIntent:
    return TradeIntent(
        intent_id="intent-1",
        strategy_id="passive",
        strategy_version="1",
        market_ticker="KXBTC-TEST",
        side=Side.YES,
        limit_price=Decimal("0.40"),
        desired_count=count,
        expiry_timestamp=datetime(2030, 1, 1, tzinfo=timezone.utc),
    )


@pytest.fixture
def store(tmp_path: Path) -> Generator[LedgerStore, None, None]:
    result = LedgerStore.connect(tmp_path / "execution.sqlite3", migrate=True)
    yield result
    result.close()


def approved(intent: TradeIntent) -> RiskDecision:
    account = AccountSnapshot(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), ())
    return RiskGateway().evaluate(
        intent,
        MarketState(),
        PortfolioState(account),
        RuntimeState(),
        RiskLimits(),
        now=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def test_pipeline_partial_fill_cancel_and_exact_accounting(store: LedgerStore) -> None:
    intent = make_intent()
    decision = approved(intent)
    simulator = LocalSimulator(store, fee_rate=Decimal("0.01"))
    order = simulator.submit(decision)
    assert order.state is OrderState.OPEN
    order = simulator.fill(order, 3, fill_id="fill-1")
    assert (order.filled_count, order.remaining_count, order.state) == (
        Decimal("3"),
        Decimal("7"),
        OrderState.PARTIALLY_FILLED,
    )
    order = simulator.cancel(order)
    assert order.state is OrderState.CANCELLED
    account = store.replay()
    assert account.reserved_cash == Decimal("0")
    assert account.cash == Decimal("-1.212")
    assert account.positions[0].quantity == Decimal("3")
    simulator.mark(order, Decimal("0.50"))
    assert store.replay().positions[0].unrealized_pnl == Decimal("0.30")
    assert (
        store._connection.execute(
            "SELECT state FROM orders WHERE client_order_id = ?", (order.client_order_id,)
        ).fetchone()[0]
        == "CANCELLED"
    )
    assert (
        store._connection.execute(
            "SELECT COUNT(*) FROM order_state_transitions WHERE client_order_id = ?",
            (order.client_order_id,),
        ).fetchone()[0]
        == 8
    )


def test_post_only_cross_is_rejected_without_residual_reservation(store: LedgerStore) -> None:
    simulator = LocalSimulator(store)
    order = simulator.submit(approved(make_intent(1)), best_opposite_price=Decimal("0.39"))
    assert order.state is OrderState.REJECTED
    assert store.replay().reserved_cash == Decimal("0")


def test_unknown_outcome_has_explicit_reconciliation_path(store: LedgerStore) -> None:
    simulator = LocalSimulator(store)
    order = simulator.submit(approved(make_intent(1)), auto_acknowledge=False)
    order = simulator.mark_outcome_unknown(order)
    assert simulator.begin_reconciliation(order).state is OrderState.RECONCILING


def test_duplicate_fill_evidence_does_not_duplicate_money(store: LedgerStore) -> None:
    intent = make_intent(2)
    simulator = LocalSimulator(store)
    order = simulator.submit(approved(intent))
    once = simulator.fill(order, 1, fill_id="same-fill")
    twice = simulator.fill(order, 1, fill_id="same-fill")
    assert twice == order
    assert store.replay().cash == Decimal("-0.40")
    assert once.filled_count == Decimal("1")
    with pytest.raises(ValueError, match="conflicts"):
        store.apply_fill(
            "same-fill",
            order.client_order_id,
            intent.market_ticker,
            Side.YES,
            Direction.BUY,
            2,
            Decimal("0.40"),
            Decimal("0"),
        )


def test_risk_rejects_unhealthy_and_over_limit_intent() -> None:
    intent = make_intent(20)
    account = AccountSnapshot(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), ())
    decision = RiskGateway().evaluate(
        intent,
        MarketState(book_quality=BookQuality.STALE),
        PortfolioState(account),
        RuntimeState(),
        RiskLimits(max_risk_per_order=Decimal("5")),
        now=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert not decision.approved
    assert {"BOOK_NOT_HEALTHY", "ORDER_LIMIT"} <= set(decision.reason_codes)
