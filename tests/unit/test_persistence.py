from decimal import Decimal
from collections.abc import Generator
from pathlib import Path

import pytest

from kalshi_bot.market_data import Side
from kalshi_bot.persistence import (
    Direction,
    FinancialEvent,
    FinancialEventType,
    LedgerStore,
)


def event(event_type: FinancialEventType, key: str, **changes: object) -> FinancialEvent:
    values: dict[str, object] = {
        "event_type": event_type,
        "idempotency_key": key,
        "market_ticker": "KXBTC-TEST",
        "side": Side.YES,
        "quantity": Decimal("0"),
        "price": Decimal("0"),
        "amount": Decimal("0"),
    }
    values.update(changes)
    return FinancialEvent(**values)  # type: ignore[arg-type]


@pytest.fixture
def store(tmp_path: Path) -> Generator[LedgerStore, None, None]:
    result = LedgerStore.connect(tmp_path / "ledger.sqlite3", migrate=True)
    yield result
    result.close()


def test_migration_creates_only_minimal_tables(store: LedgerStore) -> None:
    names = {
        row[0]
        for row in store._connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    }
    assert names == {
        "alembic_version",
        "strategy_intents",
        "feature_snapshots",
        "risk_decisions",
        "orders",
        "order_state_transitions",
        "fills",
        "ledger_entries",
        "positions",
        "reconciliation_runs",
        "queue_state_snapshots",
        "quote_expectancy_records",
    }


def test_replay_derives_exact_balances_positions_pnl_fees_and_reserve(store: LedgerStore) -> None:
    assert store.record_event(
        event(FinancialEventType.ORDER_RESERVED, "reserve-1", amount=Decimal("1.25"))
    )
    assert store.record_event(
        event(FinancialEventType.ORDER_RELEASED, "release-1", amount=Decimal("0.25"))
    )
    assert store.record_event(
        event(
            FinancialEventType.FILL_APPLIED,
            "fill-1",
            quantity=Decimal("2"),
            price=Decimal("0.40"),
            amount=Decimal("0.80"),
            direction=Direction.BUY,
        )
    )
    assert store.record_event(
        event(FinancialEventType.FEE_APPLIED, "fee-1", amount=Decimal("0.02"))
    )
    assert store.record_event(
        event(FinancialEventType.POSITION_MARKED, "mark-1", price=Decimal("0.50"))
    )
    assert store.record_event(
        event(
            FinancialEventType.FILL_APPLIED,
            "fill-2",
            quantity=Decimal("1"),
            price=Decimal("0.60"),
            amount=Decimal("0.60"),
            direction=Direction.SELL,
        )
    )
    snapshot = store.replay()
    position = snapshot.positions[0]
    assert snapshot.cash == Decimal("-0.22")
    assert snapshot.reserved_cash == Decimal("1.00")
    assert snapshot.open_order_exposure == Decimal("1.00")
    assert snapshot.fees == Decimal("0.02")
    assert position.quantity == Decimal("1")
    assert position.average_entry_price == Decimal("0.40")
    assert position.realized_pnl == Decimal("0.20")
    assert position.unrealized_pnl == Decimal("0.10")
    assert position.fees == Decimal("0.02")


def test_duplicate_event_is_idempotent_and_conflict_is_rejected(store: LedgerStore) -> None:
    first = event(FinancialEventType.ORDER_RESERVED, "same", amount=Decimal("1.00"))
    assert store.record_event(first) is True
    assert store.record_event(first) is False
    with pytest.raises(ValueError, match="idempotency key conflicts"):
        store.record_event(event(FinancialEventType.ORDER_RESERVED, "same", amount=Decimal("2.00")))
    assert store.replay().reserved_cash == Decimal("1.00")


def test_float_accounting_values_are_rejected(store: LedgerStore) -> None:
    with pytest.raises(TypeError, match="binary float"):
        event(FinancialEventType.ORDER_RESERVED, "float", amount=0.1)


def test_invalid_sell_and_over_release_do_not_commit(store: LedgerStore) -> None:
    with pytest.raises(ValueError, match="exceeds reserved"):
        store.record_event(event(FinancialEventType.ORDER_RELEASED, "release", amount=Decimal("1")))
    with pytest.raises(ValueError, match="exceeds position"):
        store.record_event(
            event(
                FinancialEventType.FILL_APPLIED,
                "sell",
                quantity=Decimal("1"),
                price=Decimal("0.5"),
                amount=Decimal("0.5"),
                direction=Direction.SELL,
            )
        )
    assert store._connection.execute("SELECT COUNT(*) FROM ledger_entries").fetchone()[0] == 0
