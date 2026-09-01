"""Fail-closed reconciliation for the narrow demo lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from uuid import uuid4
from typing import Protocol

from kalshi_bot.persistence import LedgerStore
from kalshi_bot.rest.models import Balance, Fill, Order, Position


class _ExchangeReader(Protocol):
    def list_open_orders(self) -> tuple[Order, ...]: ...
    def get_fills(self) -> tuple[Fill, ...]: ...
    def get_positions(self) -> tuple[Position, ...]: ...
    def get_balance(self) -> Balance: ...


class ReconciliationStatus(StrEnum):
    CLEAN = "CLEAN"
    TRADING_SUSPENDED_RECONCILIATION_REQUIRED = "TRADING_SUSPENDED_RECONCILIATION_REQUIRED"


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    reconciliation_id: str
    trigger: str
    status: ReconciliationStatus
    mismatches: tuple[str, ...]

    @property
    def clean(self) -> bool:
        return self.status is ReconciliationStatus.CLEAN


def _decimal(value: str | int | Decimal | None) -> Decimal:
    return Decimal("0") if value is None else Decimal(str(value))


def _exchange_side(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.upper()
    return {"BID": "YES", "ASK": "NO", "YES": "YES", "NO": "NO"}.get(normalized)


class ReconciliationService:
    """Compare all four exchange/local truth surfaces without repairing either."""

    def __init__(self, store: LedgerStore, client: _ExchangeReader) -> None:
        self.store = store
        self.client = client
        self.suspended = store.reconciliation_required()

    def reconcile(self, *, trigger: str) -> ReconciliationResult:
        try:
            exchange_orders = tuple(self.client.list_open_orders())
            exchange_fills = tuple(self.client.get_fills())
            exchange_positions = tuple(self.client.get_positions())
            exchange_balance = self.client.get_balance()
            mismatches = tuple(
                self._compare_orders(exchange_orders)
                + self._compare_fills(exchange_fills)
                + self._compare_positions(exchange_positions)
                + self._compare_balance(exchange_balance)
            )
        except Exception as exc:
            # A partial or unavailable truth surface is not clean. Persist only
            # the stable exception type; never expose response/request details.
            mismatches = (f"reconciliation_unavailable:{type(exc).__name__}",)
        status = ReconciliationStatus.CLEAN
        self.suspended = self.suspended or bool(mismatches)
        if self.suspended:
            status = ReconciliationStatus.TRADING_SUSPENDED_RECONCILIATION_REQUIRED
        reconciliation_id = str(uuid4())
        self.store.record_reconciliation(
            reconciliation_id, status.value, f"trigger={trigger};mismatches={len(mismatches)}"
        )
        return ReconciliationResult(reconciliation_id, trigger, status, mismatches)

    def on_startup(self) -> ReconciliationResult:
        return self.reconcile(trigger="startup")

    def on_reconnect(self) -> ReconciliationResult:
        return self.reconcile(trigger="reconnect")

    def on_uncertain_submission(self) -> ReconciliationResult:
        return self.reconcile(trigger="uncertain-submission")

    def before_shutdown(self) -> ReconciliationResult:
        return self.reconcile(trigger="before-shutdown")

    def _compare_orders(self, exchange: tuple[Order, ...]) -> list[str]:
        local_rows = {row["client_order_id"]: row for row in self.store.local_open_orders()}
        local = set(local_rows)
        result = ["open_order_missing_exchange_id" for order in exchange if order.client_order_id is None]
        remote_rows = {order.client_order_id: order for order in exchange if order.client_order_id}
        remote = set(remote_rows)
        result.extend(f"open_orders_missing_local:{value}" for value in sorted(remote - local))
        result.extend(
            f"open_orders_missing_exchange:{value}" for value in sorted(local - remote)
        )
        for order_id in sorted(local & remote):
            row = local_rows[order_id]
            order = remote_rows[order_id]
            remote_price = order.yes_price_dollars or order.no_price_dollars
            remote_count = order.initial_count_fp or order.count
            remote_side = _exchange_side(order.side)
            if remote_price is None or remote_count is None or order.side is None:
                result.append(f"open_order_incomplete_exchange_evidence:{order_id}")
            elif (
                row["ticker"] != order.ticker
                or row["side"] != remote_side
                or _decimal(row["quantity"]) != _decimal(remote_count)
                or _decimal(row["price"]) != _decimal(remote_price)
            ):
                result.append(f"open_order_value_mismatch:{order_id}")
        return result

    def _compare_fills(self, exchange: tuple[Fill, ...]) -> list[str]:
        local = {
            row["exchange_fill_id"]: (
                row["client_order_id"],
                _decimal(row["quantity"]),
                _decimal(row["price"]),
                _decimal(row["fee"]),
            )
            for row in self.store.local_fills()
        }
        remote: dict[str, tuple[str | None, Decimal, Decimal, Decimal]] = {}
        result: list[str] = []
        for fill in exchange:
            fill_id = fill.fill_id or fill.trade_id
            if not fill_id:
                result.append("fill_missing_exchange_id")
                continue
            price = fill.yes_price_dollars or fill.no_price_dollars
            if price is None or fill.count_fp is None or fill.fee_cost is None:
                result.append(f"incomplete_exchange_fill:{fill_id}")
                continue
            if fill_id in remote:
                result.append(f"duplicate_exchange_fill:{fill_id}")
                continue
            remote[fill_id] = (
                getattr(fill, "client_order_id", None),
                _decimal(fill.count_fp),
                _decimal(price),
                _decimal(fill.fee_cost),
            )
        result.extend(f"fills_missing_local:{value}" for value in sorted(remote.keys() - local.keys()))
        result.extend(
            f"fills_missing_exchange:{value}" for value in sorted(local.keys() - remote.keys())
        )
        result.extend(
            f"fill_value_mismatch:{value}"
            for value in sorted(local.keys() & remote.keys())
            if local[value] != remote[value]
        )
        return result

    def _compare_positions(self, exchange: tuple[Position, ...]) -> list[str]:
        local: dict[str, Decimal] = {}
        for position in self.store.replay().positions:
            sign = Decimal("1") if position.side.value == "YES" else Decimal("-1")
            local[position.market_ticker] = (
                local.get(position.market_ticker, Decimal("0")) + sign * position.quantity
            )
        result = ["position_missing_exchange_ticker" for position in exchange if position.ticker is None]
        remote = {
            position.ticker: _decimal(position.position_fp)
            for position in exchange
            if position.ticker is not None
        }
        keys = local.keys() | remote.keys()
        result.extend(
            f"position_mismatch:{key}"
            for key in sorted(keys)
            if local.get(key, Decimal("0")) != remote.get(key, Decimal("0"))
        )
        return result

    def _compare_balance(self, exchange: object) -> list[str]:
        dollars = getattr(exchange, "balance_dollars", None)
        if dollars is None and getattr(exchange, "balance", None) is None:
            return ["balance_missing_exchange_value"]
        remote = (
            _decimal(dollars)
            if dollars is not None
            else _decimal(getattr(exchange, "balance", None)) / 100
        )
        local = self.store.replay().cash
        return [] if local == remote else [f"balance_mismatch:local={local};exchange={remote}"]
