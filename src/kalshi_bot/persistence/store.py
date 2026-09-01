"""Append-only SQLite ledger and deterministic accounting projections."""

from __future__ import annotations

import json
import sqlite3
import uuid
from uuid import uuid4
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

from alembic import command
from alembic.config import Config

from kalshi_bot.market_data.orderbook import Side

_ZERO = Decimal("0")


class FinancialEventType(StrEnum):
    ORDER_RESERVED = "ORDER_RESERVED"
    ORDER_RELEASED = "ORDER_RELEASED"
    FILL_APPLIED = "FILL_APPLIED"
    FEE_APPLIED = "FEE_APPLIED"
    POSITION_MARKED = "POSITION_MARKED"


class Direction(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


def _decimal(value: Decimal | str | int, field: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{field} must not be a binary float")
    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a finite decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def _text(value: Decimal | str | int, field: str) -> str:
    return format(_decimal(value, field), "f")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class FinancialEvent:
    event_type: FinancialEventType
    idempotency_key: str
    market_ticker: str | None = None
    client_order_id: str | None = None
    side: Side | None = None
    direction: Direction = Direction.BUY
    quantity: Decimal = _ZERO
    price: Decimal = _ZERO
    amount: Decimal = _ZERO
    event_id: str = ""
    event_at: str = ""

    def __post_init__(self) -> None:
        if not self.idempotency_key:
            raise ValueError("idempotency_key is required")
        object.__setattr__(self, "quantity", _decimal(self.quantity, "quantity"))
        object.__setattr__(self, "price", _decimal(self.price, "price"))
        object.__setattr__(self, "amount", _decimal(self.amount, "amount"))
        if self.event_type in (FinancialEventType.FILL_APPLIED, FinancialEventType.POSITION_MARKED):
            if not self.market_ticker or self.side is None:
                raise ValueError("market and side are required for position events")
        if self.event_type is FinancialEventType.FILL_APPLIED:
            if self.quantity <= 0 or self.price < 0 or self.amount != self.quantity * self.price:
                raise ValueError("fill quantity, price, and amount are inconsistent")
        if (
            self.event_type
            in (
                FinancialEventType.ORDER_RESERVED,
                FinancialEventType.ORDER_RELEASED,
                FinancialEventType.FEE_APPLIED,
            )
            and self.amount <= 0
        ):
            raise ValueError("financial event amount must be positive")


@dataclass(frozen=True, slots=True)
class PositionSnapshot:
    market_ticker: str
    side: Side
    quantity: Decimal
    average_entry_price: Decimal
    realized_pnl: Decimal
    mark_price: Decimal | None
    unrealized_pnl: Decimal
    fees: Decimal


@dataclass(frozen=True, slots=True)
class AccountSnapshot:
    cash: Decimal
    reserved_cash: Decimal
    fees: Decimal
    open_order_exposure: Decimal
    positions: tuple[PositionSnapshot, ...]


class LedgerStore:
    """SQLite store whose balances are projections of the append-only ledger."""

    def __init__(self, connection: sqlite3.Connection):
        self._connection = connection
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")

    @classmethod
    def connect(cls, path: str | Path = ":memory:", *, migrate: bool = False) -> LedgerStore:
        if migrate and str(path) == ":memory:":
            raise ValueError("Alembic migration requires a file-backed SQLite database")
        if migrate:
            database = Path(path).resolve()
            config = Config(str(Path("alembic.ini").resolve()))
            config.set_main_option("sqlalchemy.url", f"sqlite:///{database.as_posix()}")
            command.upgrade(config, "head")
        return cls(sqlite3.connect(str(path)))

    def close(self) -> None:
        self._connection.close()

    def record_event(self, event: FinancialEvent) -> bool:
        """Append one event; return False for an already-recorded idempotency key."""
        try:
            self._connection.execute(
                """INSERT INTO ledger_entries
                (event_id, idempotency_key, event_type, market_ticker, client_order_id,
                 side, direction, quantity, price, amount, event_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    event.event_id or str(uuid.uuid4()),
                    event.idempotency_key,
                    event.event_type.value,
                    event.market_ticker,
                    event.client_order_id,
                    event.side.value if event.side else None,
                    event.direction.value,
                    _text(event.quantity, "quantity"),
                    _text(event.price, "price"),
                    _text(event.amount, "amount"),
                    event.event_at or _now(),
                ),
            )
            self.replay()
        except sqlite3.IntegrityError as exc:
            if "idempotency_key" in str(exc):
                existing = self._connection.execute(
                    "SELECT event_type, market_ticker, client_order_id, side, direction, "
                    "quantity, price, amount FROM ledger_entries WHERE idempotency_key = ?",
                    (event.idempotency_key,),
                ).fetchone()
                if existing is None:
                    raise
                same = (
                    existing["event_type"] == event.event_type.value
                    and existing["market_ticker"] == event.market_ticker
                    and existing["client_order_id"] == event.client_order_id
                    and existing["side"] == (event.side.value if event.side else None)
                    and existing["direction"] == event.direction.value
                    and existing["quantity"] == _text(event.quantity, "quantity")
                    and existing["price"] == _text(event.price, "price")
                    and existing["amount"] == _text(event.amount, "amount")
                )
                if same:
                    return False
                raise ValueError("idempotency key conflicts with a different event") from None
            raise
        except Exception:
            self._connection.rollback()
            raise
        self._connection.commit()
        self._refresh_positions()
        return True

    def replay(self) -> AccountSnapshot:
        """Reconstruct all balances and positions solely from ledger rows."""
        rows = self._connection.execute("SELECT * FROM ledger_entries ORDER BY rowid").fetchall()
        cash = _ZERO
        reserved = _ZERO
        fees = _ZERO
        positions: dict[tuple[str, Side], dict[str, Decimal | None]] = {}
        marks: dict[tuple[str, Side], Decimal] = {}
        for row in rows:
            event_type = FinancialEventType(row["event_type"])
            amount, quantity, price = (
                Decimal(row["amount"]),
                Decimal(row["quantity"]),
                Decimal(row["price"]),
            )
            if event_type is FinancialEventType.ORDER_RESERVED:
                reserved += amount
            elif event_type is FinancialEventType.ORDER_RELEASED:
                reserved -= amount
                if reserved < 0:
                    raise ValueError("released reservation exceeds reserved cash")
            elif event_type is FinancialEventType.FEE_APPLIED:
                cash -= amount
                fees += amount
                if row["market_ticker"] and row["side"]:
                    state = positions.setdefault(
                        (row["market_ticker"], Side(row["side"])), self._empty_position()
                    )
                    state["fees"] = self._required(state["fees"]) + amount
            elif event_type is FinancialEventType.FILL_APPLIED:
                side = Side(row["side"])
                key = (row["market_ticker"], side)
                state = positions.setdefault(key, self._empty_position())
                cash += amount if row["direction"] == Direction.SELL else -amount
                self._apply_fill(state, quantity, price, Direction(row["direction"]))
            elif event_type is FinancialEventType.POSITION_MARKED:
                marks[(row["market_ticker"], Side(row["side"]))] = price
        snapshots: list[PositionSnapshot] = []
        for key, state in positions.items():
            mark = marks.get(key)
            quantity = self._required(state["quantity"])
            average = self._required(state["average"])
            unrealized = _ZERO if mark is None else (mark - average) * quantity
            snapshots.append(
                PositionSnapshot(
                    key[0],
                    key[1],
                    quantity,
                    average,
                    self._required(state["realized"]),
                    mark,
                    unrealized,
                    self._required(state["fees"]),
                )
            )
        snapshots.sort(key=lambda item: (item.market_ticker, item.side.value))
        return AccountSnapshot(cash, reserved, fees, reserved, tuple(snapshots))

    def _refresh_positions(self) -> None:
        snapshot = self.replay()
        with self._connection:
            self._connection.execute("DELETE FROM positions")
            for position in snapshot.positions:
                self._connection.execute(
                    """INSERT INTO positions
                    (market_ticker, side, quantity, average_entry_price, realized_pnl,
                     mark_price, unrealized_pnl, fees) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        position.market_ticker,
                        position.side.value,
                        _text(position.quantity, "quantity"),
                        _text(position.average_entry_price, "average"),
                        _text(position.realized_pnl, "realized"),
                        None if position.mark_price is None else _text(position.mark_price, "mark"),
                        _text(position.unrealized_pnl, "unrealized"),
                        _text(position.fees, "fees"),
                    ),
                )

    @staticmethod
    def _empty_position() -> dict[str, Decimal | None]:
        return {"quantity": _ZERO, "average": _ZERO, "realized": _ZERO, "fees": _ZERO}

    @staticmethod
    def _required(value: Decimal | None) -> Decimal:
        if value is None:
            raise AssertionError("internal accounting state is incomplete")
        return value

    @classmethod
    def _apply_fill(
        cls,
        state: dict[str, Decimal | None],
        quantity: Decimal,
        price: Decimal,
        direction: Direction,
    ) -> None:
        current = cls._required(state["quantity"])
        average = cls._required(state["average"])
        if direction is Direction.BUY:
            total = current + quantity
            state["average"] = ((average * current) + (price * quantity)) / total
            state["quantity"] = total
        else:
            if quantity > current:
                raise ValueError("sell fill exceeds position")
            state["realized"] = cls._required(state["realized"]) + ((price - average) * quantity)
            state["quantity"] = current - quantity

    def record_strategy_intent(
        self,
        intent_id: str,
        strategy_id: str,
        market_ticker: str,
        market_archetype_id: str,
        payload: Mapping[str, Any],
        created_at: str | None = None,
    ) -> None:
        self._insert(
            "strategy_intents",
            (
                intent_id,
                strategy_id,
                market_ticker,
                market_archetype_id,
                json.dumps(dict(payload), sort_keys=True),
                created_at or _now(),
            ),
            "(intent_id, strategy_id, market_ticker, market_archetype_id, payload_json, created_at)",
        )

    def record_feature_snapshot(
        self,
        snapshot_id: str,
        market_ticker: str,
        market_archetype_id: str,
        payload: Mapping[str, Any],
        captured_at: str | None = None,
    ) -> None:
        self._insert(
            "feature_snapshots",
            (
                snapshot_id,
                market_ticker,
                market_archetype_id,
                json.dumps(dict(payload), sort_keys=True),
                captured_at or _now(),
            ),
            "(snapshot_id, market_ticker, market_archetype_id, payload_json, captured_at)",
        )

    def record_risk_decision(
        self,
        risk_decision_id: str,
        intent_id: str,
        approved: bool,
        payload: Mapping[str, Any],
        decided_at: str | None = None,
    ) -> None:
        self._insert(
            "risk_decisions",
            (
                risk_decision_id,
                intent_id,
                int(approved),
                json.dumps(dict(payload), sort_keys=True),
                decided_at or _now(),
            ),
            "(risk_decision_id, intent_id, approved, payload_json, decided_at)",
        )

    def record_reconciliation(
        self,
        reconciliation_id: str,
        status: str,
        evidence_reference: str,
        started_at: str | None = None,
        completed_at: str | None = None,
    ) -> None:
        self._insert(
            "reconciliation_runs",
            (reconciliation_id, status, evidence_reference, started_at or _now(), completed_at),
            "(reconciliation_id, status, evidence_reference, started_at, completed_at)",
        )

    def record_order(
        self,
        client_order_id: str,
        intent_id: str,
        feature_snapshot_id: str,
        risk_decision_id: str,
        market_ticker: str,
        side: Side,
        quantity: Decimal | str | int,
        price: Decimal | str | int,
        state: str,
        created_at: str | None = None,
    ) -> None:
        self._insert(
            "orders",
            (
                client_order_id,
                intent_id,
                feature_snapshot_id,
                risk_decision_id,
                market_ticker,
                side.value,
                _text(quantity, "quantity"),
                _text(price, "price"),
                state,
                created_at or _now(),
            ),
            "(client_order_id, intent_id, feature_snapshot_id, risk_decision_id, market_ticker, "
            "side, quantity, price, state, created_at)",
        )

    def get_order(self, client_order_id: str) -> sqlite3.Row | None:
        """Return the local order projection for idempotency checks."""
        return cast(
            sqlite3.Row | None,
            self._connection.execute(
                "SELECT * FROM orders WHERE client_order_id = ?", (client_order_id,)
            ).fetchone(),
        )

    def record_transition(
        self,
        transition_id: str,
        client_order_id: str,
        previous_state: str | None,
        state: str,
        evidence_reference: str,
        transitioned_at: str | None = None,
    ) -> None:
        self._insert(
            "order_state_transitions",
            (
                transition_id,
                client_order_id,
                previous_state,
                state,
                evidence_reference,
                transitioned_at or _now(),
            ),
            "(transition_id, client_order_id, previous_state, state, evidence_reference, transitioned_at)",
        )

    def record_fill(
        self,
        fill_id: str,
        client_order_id: str,
        exchange_fill_id: str,
        quantity: Decimal | str | int,
        price: Decimal | str | int,
        fee: Decimal | str | int,
        filled_at: str | None = None,
    ) -> None:
        self._insert(
            "fills",
            (
                fill_id,
                client_order_id,
                exchange_fill_id,
                _text(quantity, "quantity"),
                _text(price, "price"),
                _text(fee, "fee"),
                filled_at or _now(),
            ),
            "(fill_id, client_order_id, exchange_fill_id, quantity, price, fee, filled_at)",
        )

    def apply_fill(
        self,
        fill_id: str,
        client_order_id: str,
        market_ticker: str,
        side: Side,
        direction: Direction,
        quantity: Decimal | str | int,
        price: Decimal | str | int,
        fee: Decimal | str | int,
        filled_at: str | None = None,
    ) -> bool:
        """Atomically persist one fill, its cash movement, fee, and reserve release.

        ``fill_id`` is the idempotency key for the external evidence.  A repeated
        identical fill is a no-op; a conflicting replay is rejected.
        """
        quantity_d, price_d, fee_d = (
            _decimal(quantity, "quantity"), _decimal(price, "price"), _decimal(fee, "fee")
        )
        existing = self._connection.execute(
            "SELECT client_order_id, quantity, price, fee FROM fills WHERE exchange_fill_id = ?",
            (fill_id,),
        ).fetchone()
        expected = (_text(quantity_d, "quantity"), _text(price_d, "price"), _text(fee_d, "fee"))
        if existing is not None:
            actual = (existing["quantity"], existing["price"], existing["fee"])
            if (existing["client_order_id"], *actual) != (client_order_id, *expected):
                raise ValueError("fill evidence conflicts with an existing fill")
            return False
        amount = quantity_d * price_d
        timestamp = filled_at or _now()
        try:
            self._connection.execute(
                "INSERT INTO fills (fill_id, client_order_id, exchange_fill_id, quantity, price, fee, filled_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (fill_id, client_order_id, fill_id, _text(quantity_d, "quantity"),
                 _text(price_d, "price"), _text(fee_d, "fee"), timestamp),
            )
            event_rows = [
                (f"fill:{fill_id}", FinancialEventType.FILL_APPLIED, market_ticker, client_order_id,
                 side, direction, quantity_d, price_d, amount),
                (f"release:{fill_id}", FinancialEventType.ORDER_RELEASED, market_ticker, client_order_id,
                 side, direction, Decimal("0"), Decimal("0"), amount),
            ]
            if fee_d:
                event_rows.append(
                    (f"fee:{fill_id}", FinancialEventType.FEE_APPLIED, market_ticker, client_order_id,
                     side, direction, Decimal("0"), Decimal("0"), fee_d)
                )
            for key, kind, ticker, order_id, event_side, event_direction, qty, event_price, event_amount in event_rows:
                self._connection.execute(
                    """INSERT INTO ledger_entries
                    (event_id, idempotency_key, event_type, market_ticker, client_order_id,
                     side, direction, quantity, price, amount, event_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (str(uuid4()), key, kind.value, ticker, order_id,
                     event_side.value, event_direction.value, _text(qty, "quantity"),
                     _text(event_price, "price"), _text(event_amount, "amount"), timestamp),
                )
            self.replay()
        except Exception:
            self._connection.rollback()
            raise
        self._connection.commit()
        self._refresh_positions()
        return True

    def transition_order(
        self,
        client_order_id: str,
        previous_state: str | None,
        state: str,
        evidence_reference: str,
        transitioned_at: str | None = None,
    ) -> None:
        """Append a state transition and atomically advance the order projection."""
        row = self._connection.execute(
            "SELECT state FROM orders WHERE client_order_id = ?", (client_order_id,)
        ).fetchone()
        if row is None:
            raise ValueError("order does not exist")
        if previous_state is not None and row["state"] != previous_state:
            raise ValueError("order transition has stale previous state")
        self._connection.execute(
            """INSERT INTO order_state_transitions
             (transition_id, client_order_id, previous_state, state, evidence_reference, transitioned_at)
             VALUES (?, ?, ?, ?, ?, ?)""",
            (str(uuid4()), client_order_id, previous_state, state, evidence_reference,
             transitioned_at or _now()),
        )
        self._connection.execute(
            "UPDATE orders SET state = ? WHERE client_order_id = ?", (state, client_order_id)
        )
        self._connection.commit()

    def _insert(self, table: str, values: tuple[Any, ...], columns: str) -> None:
        placeholders = ",".join("?" for _ in values)
        self._connection.execute(f"INSERT INTO {table} {columns} VALUES ({placeholders})", values)
        self._connection.commit()
