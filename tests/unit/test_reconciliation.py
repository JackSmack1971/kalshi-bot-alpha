from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from kalshi_bot.persistence import LedgerStore
from kalshi_bot.reconciliation import ReconciliationService, ReconciliationStatus


def _store(path: Path) -> LedgerStore:
    return LedgerStore.connect(path, migrate=True)


def test_reconciliation_compares_all_surfaces_and_records_clean_run(tmp_path: Path) -> None:
    store = _store(tmp_path / "clean.sqlite3")
    try:
        client = SimpleNamespace(
            list_open_orders=lambda: (),
            get_fills=lambda: (),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        result = ReconciliationService(store, client).reconcile(trigger="startup")
        assert result.status is ReconciliationStatus.CLEAN
        assert result.mismatches == ()
        assert (
            store._connection.execute("SELECT status FROM reconciliation_runs").fetchone()[0]
            == "CLEAN"
        )
    finally:
        store.close()


def test_reconciliation_latches_suspension_without_repairing_local_state(tmp_path: Path) -> None:
    store = _store(tmp_path / "mismatch.sqlite3")
    try:
        client = SimpleNamespace(
            list_open_orders=lambda: (SimpleNamespace(client_order_id="remote-1"),),
            get_fills=lambda: (),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        service = ReconciliationService(store, client)
        result = service.reconcile(trigger="reconnect")
        assert result.status is ReconciliationStatus.TRADING_SUSPENDED_RECONCILIATION_REQUIRED
        assert service.suspended
        assert store.get_order("remote-1") is None
        assert "open_orders_missing_local:remote-1" in result.mismatches
        restarted = ReconciliationService(store, client)
        clean_exchange = SimpleNamespace(
            list_open_orders=lambda: (),
            get_fills=lambda: (),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        clean_result = ReconciliationService(store, clean_exchange).reconcile(trigger="startup")
        assert restarted.suspended
        assert clean_result.status is ReconciliationStatus.TRADING_SUSPENDED_RECONCILIATION_REQUIRED
    finally:
        store.close()


def test_reconciliation_suspends_on_unavailable_truth_surface(tmp_path: Path) -> None:
    store = _store(tmp_path / "unavailable.sqlite3")
    try:
        def unavailable() -> tuple[object, ...]:
            raise RuntimeError("synthetic transport detail")

        client = SimpleNamespace(
            list_open_orders=unavailable,
            get_fills=lambda: (),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        result = ReconciliationService(store, client).reconcile(trigger="startup")
        assert result.status is ReconciliationStatus.TRADING_SUSPENDED_RECONCILIATION_REQUIRED
        assert result.mismatches == ("reconciliation_unavailable:RuntimeError",)
        assert store.reconciliation_required()
    finally:
        store.close()


def test_reconciliation_rejects_duplicate_or_unidentified_fill_evidence(tmp_path: Path) -> None:
    store = _store(tmp_path / "fills.sqlite3")
    try:
        fill = SimpleNamespace(
            fill_id="fill-1",
            trade_id=None,
            count_fp="1",
            yes_price_dollars="0.40",
            no_price_dollars=None,
            fee_cost="0",
            client_order_id="order-1",
        )
        client = SimpleNamespace(
            list_open_orders=lambda: (),
            get_fills=lambda: (fill, fill, SimpleNamespace(fill_id=None, trade_id=None)),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        result = ReconciliationService(store, client).reconcile(trigger="reconnect")
        assert result.status is ReconciliationStatus.TRADING_SUSPENDED_RECONCILIATION_REQUIRED
        assert "duplicate_exchange_fill:fill-1" in result.mismatches
        assert "fill_missing_exchange_id" in result.mismatches
    finally:
        store.close()


@pytest.mark.parametrize(
    "trigger", ["startup", "reconnect", "uncertain-submission", "before-shutdown"]
)
def test_lifecycle_triggers_are_explicit(trigger: str, tmp_path: Path) -> None:
    store = _store(tmp_path / f"{trigger}.sqlite3")
    try:
        client = SimpleNamespace(
            list_open_orders=lambda: (),
            get_fills=lambda: (),
            get_positions=lambda: (),
            get_balance=lambda: SimpleNamespace(balance_dollars="0"),
        )
        result = ReconciliationService(store, client).reconcile(trigger=trigger)
        assert result.trigger == trigger
    finally:
        store.close()
