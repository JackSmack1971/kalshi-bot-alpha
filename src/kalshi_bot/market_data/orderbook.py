"""Exact, immutable order-book representations.

The exchange supplies bids only.  Asks are derived from the opposite binary
side using ``1.00 - price``; all arithmetic remains in :class:`Decimal`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

__all__ = [
    "BookQuality",
    "OrderBookDelta",
    "OrderBookReconstructor",
    "FixedPointCount",
    "FixedPointPrice",
    "OrderBookLevel",
    "OrderBookSnapshot",
    "Side",
]

_ONE = Decimal("1.00")


def _decimal(value: str | Decimal | int, field: str) -> Decimal:
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError(f"{field} must not be a binary float")
    if not isinstance(value, (str, Decimal, int)):
        raise TypeError(f"{field} must be a string, Decimal, or int")
    try:
        result = Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} is not a valid fixed-point decimal") from exc
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


@dataclass(frozen=True, slots=True)
class FixedPointPrice:
    value: Decimal

    def __post_init__(self) -> None:
        value = _decimal(self.value, "price")
        if not Decimal("0") <= value <= _ONE:
            raise ValueError("price must be between 0 and 1 inclusive")
        object.__setattr__(self, "value", value)

    @classmethod
    def parse(cls, value: str | Decimal | int) -> FixedPointPrice:
        return cls(_decimal(value, "price"))

    @property
    def dollars(self) -> Decimal:
        return self.value

    def complement(self) -> FixedPointPrice:
        return FixedPointPrice(_ONE - self.value)

    def __str__(self) -> str:
        return format(self.value, "f")


@dataclass(frozen=True, slots=True)
class FixedPointCount:
    value: Decimal

    def __post_init__(self) -> None:
        value = _decimal(self.value, "count")
        if value < 0:
            raise ValueError("count must not be negative")
        object.__setattr__(self, "value", value)

    @classmethod
    def parse(cls, value: str | Decimal | int) -> FixedPointCount:
        return cls(_decimal(value, "count"))

    def __str__(self) -> str:
        return format(self.value, "f")


class Side(str, Enum):
    YES = "YES"
    NO = "NO"


class BookQuality(str, Enum):
    INITIALIZING = "INITIALIZING"
    HEALTHY = "HEALTHY"
    STALE = "STALE"
    GAP = "GAP"
    GAP_DETECTED = "GAP"  # compatibility spelling for the governing contract
    RESYNCING = "RESYNCING"


@dataclass(frozen=True, slots=True)
class OrderBookLevel:
    price: FixedPointPrice
    count: FixedPointCount

    @classmethod
    def parse(cls, price: str | Decimal | int, count: str | Decimal | int) -> OrderBookLevel:
        return cls(FixedPointPrice.parse(price), FixedPointCount.parse(count))


def _normalize(levels: Iterable[OrderBookLevel]) -> tuple[OrderBookLevel, ...]:
    merged: dict[Decimal, Decimal] = {}
    for level in levels:
        merged[level.price.value] = merged.get(level.price.value, Decimal("0")) + level.count.value
    return tuple(
        OrderBookLevel(FixedPointPrice(price), FixedPointCount(count))
        for price, count in sorted(merged.items())
    )


@dataclass(frozen=True, slots=True)
class OrderBookSnapshot:
    market_ticker: str
    snapshot_timestamp: datetime
    yes_bids: tuple[OrderBookLevel, ...] = ()
    no_bids: tuple[OrderBookLevel, ...] = ()
    sequence: int | None = None
    version: int | str | None = None
    quality: BookQuality = BookQuality.INITIALIZING

    def __post_init__(self) -> None:
        if not self.market_ticker or self.market_ticker != self.market_ticker.strip():
            raise ValueError("market_ticker must be non-empty and trimmed")
        if (
            not isinstance(self.snapshot_timestamp, datetime)
            or self.snapshot_timestamp.tzinfo is None
        ):
            raise ValueError("snapshot_timestamp must be timezone-aware")
        if self.sequence is not None and (
            isinstance(self.sequence, bool)
            or not isinstance(self.sequence, int)
            or self.sequence < 0
        ):
            raise ValueError("sequence must be a non-negative integer")
        if not isinstance(self.quality, BookQuality):
            raise ValueError("quality must be a BookQuality")
        object.__setattr__(self, "yes_bids", _normalize(self.yes_bids))
        object.__setattr__(self, "no_bids", _normalize(self.no_bids))

    @classmethod
    def from_rest(
        cls,
        market_ticker: str,
        payload: Mapping[str, Any],
        *,
        snapshot_timestamp: datetime,
        sequence: int | None = None,
        version: int | str | None = None,
        quality: BookQuality = BookQuality.HEALTHY,
    ) -> OrderBookSnapshot:
        if not isinstance(payload, Mapping):
            raise ValueError("REST order-book payload must be an object")
        book = payload.get("orderbook_fp", payload)
        if not isinstance(book, Mapping):
            raise ValueError("orderbook_fp must be an object")
        yes_key = "yes_dollars" if "yes_dollars" in book else "yes_dollars_fp"
        no_key = "no_dollars" if "no_dollars" in book else "no_dollars_fp"
        if yes_key not in book or no_key not in book:
            raise ValueError("orderbook_fp must contain yes_dollars and no_dollars")
        return cls(
            market_ticker=market_ticker,
            snapshot_timestamp=snapshot_timestamp,
            yes_bids=_parse_wire_levels(book.get(yes_key)),
            no_bids=_parse_wire_levels(book.get(no_key)),
            sequence=sequence,
            version=version,
            quality=quality,
        )

    @property
    def yes_best_bid(self) -> OrderBookLevel | None:
        return self.yes_bids[-1] if self.yes_bids else None

    @property
    def no_best_bid(self) -> OrderBookLevel | None:
        return self.no_bids[-1] if self.no_bids else None

    @property
    def yes_best_ask(self) -> OrderBookLevel | None:
        return _complement_level(self.no_best_bid)

    @property
    def no_best_ask(self) -> OrderBookLevel | None:
        return _complement_level(self.yes_best_bid)

    def best_bid(self, side: Side) -> OrderBookLevel | None:
        return self.yes_best_bid if side is Side.YES else self.no_best_bid

    def best_ask(self, side: Side) -> OrderBookLevel | None:
        return self.yes_best_ask if side is Side.YES else self.no_best_ask

    def spread(self, side: Side = Side.YES) -> FixedPointPrice | None:
        bid, ask = self.best_bid(side), self.best_ask(side)
        return (
            None
            if bid is None or ask is None
            else FixedPointPrice(ask.price.value - bid.price.value)
        )

    def midpoint(self, side: Side = Side.YES) -> FixedPointPrice | None:
        bid, ask = self.best_bid(side), self.best_ask(side)
        return (
            None
            if bid is None or ask is None
            else FixedPointPrice((bid.price.value + ask.price.value) / 2)
        )


@dataclass(frozen=True, slots=True)
class OrderBookDelta:
    """One Kalshi ``orderbook_delta`` event.

    ``delta`` is an additive change to the aggregated level.  It is never
    treated as an absolute size and a negative result is never clamped.
    """

    market_ticker: str
    sequence: int
    side: Side
    price: FixedPointPrice
    delta: str | Decimal | int
    timestamp: datetime

    def __post_init__(self) -> None:
        if not self.market_ticker or self.market_ticker != self.market_ticker.strip():
            raise ValueError("market_ticker must be non-empty and trimmed")
        if (
            isinstance(self.sequence, bool)
            or not isinstance(self.sequence, int)
            or self.sequence < 0
        ):
            raise ValueError("sequence must be a non-negative integer")
        if not isinstance(self.side, Side):
            raise ValueError("side must be YES or NO")
        if not isinstance(self.timestamp, datetime) or self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")
        value = _decimal(self.delta, "delta")
        object.__setattr__(self, "delta", value)


class OrderBookReconstructor:
    """Fail-closed, single-market order-book delta state machine.

    ``apply_delta`` is transactional: validation and sequence checks happen
    before the candidate book is published.  A gap, reordered event, or
    impossible negative level discards the usable book and requires a new
    snapshot.  Exact duplicate sequence numbers are ignored.
    """

    __slots__ = (
        "market_ticker",
        "max_age_seconds",
        "_book",
        "_last_sequence",
        "_last_update",
        "_invalid_quality",
    )

    def __init__(self, market_ticker: str, *, max_age_seconds: float = 2.0) -> None:
        if not market_ticker or market_ticker != market_ticker.strip():
            raise ValueError("market_ticker must be non-empty and trimmed")
        if max_age_seconds <= 0:
            raise ValueError("max_age_seconds must be > 0")
        self.market_ticker = market_ticker
        self.max_age_seconds = max_age_seconds
        self._book: OrderBookSnapshot | None = None
        self._last_sequence: int | None = None
        self._last_update: datetime | None = None
        self._invalid_quality = BookQuality.INITIALIZING

    @property
    def quality(self) -> BookQuality:
        return self._invalid_quality if self._book is None else self._book.quality

    @property
    def last_sequence(self) -> int | None:
        return self._last_sequence

    def reset(self) -> None:
        """Discard all pre-disconnect or pre-resynchronization state."""
        self._book = None
        self._last_sequence = None
        self._last_update = None
        self._invalid_quality = BookQuality.INITIALIZING

    def apply_snapshot(self, snapshot: OrderBookSnapshot) -> OrderBookSnapshot:
        if snapshot.market_ticker != self.market_ticker:
            raise ValueError("snapshot market does not match reconstructor")
        if snapshot.sequence is None:
            raise ValueError("streaming snapshot requires a sequence")
        self._book = OrderBookSnapshot(
            market_ticker=snapshot.market_ticker,
            snapshot_timestamp=snapshot.snapshot_timestamp,
            yes_bids=snapshot.yes_bids,
            no_bids=snapshot.no_bids,
            sequence=snapshot.sequence,
            version=snapshot.version,
            quality=BookQuality.HEALTHY,
        )
        self._last_sequence = snapshot.sequence
        self._last_update = snapshot.snapshot_timestamp
        self._invalid_quality = BookQuality.HEALTHY
        return self._book

    def apply_delta(self, delta: OrderBookDelta) -> OrderBookSnapshot | None:
        if delta.market_ticker != self.market_ticker:
            raise ValueError("delta market does not match reconstructor")
        expected = None if self._last_sequence is None else self._last_sequence + 1
        if expected is None or delta.sequence != expected:
            if self._last_sequence is not None and delta.sequence == self._last_sequence:
                return self._book  # idempotent duplicate
            self._invalidate(BookQuality.GAP)
            return None
        if self._book is None or self._book.quality is not BookQuality.HEALTHY:
            self._invalidate(BookQuality.GAP)
            return None

        levels = list(self._book.yes_bids if delta.side is Side.YES else self._book.no_bids)
        by_price = {level.price.value: level.count.value for level in levels}
        next_count = by_price.get(delta.price.value, Decimal("0")) + _decimal(delta.delta, "delta")
        if next_count < 0:
            self._invalidate(BookQuality.GAP)
            return None
        if next_count == 0:
            by_price.pop(delta.price.value, None)
        else:
            by_price[delta.price.value] = next_count
        updated = tuple(
            OrderBookLevel(FixedPointPrice(price), FixedPointCount(count))
            for price, count in sorted(by_price.items())
        )
        self._book = OrderBookSnapshot(
            market_ticker=self.market_ticker,
            snapshot_timestamp=delta.timestamp,
            yes_bids=updated if delta.side is Side.YES else self._book.yes_bids,
            no_bids=updated if delta.side is Side.NO else self._book.no_bids,
            sequence=delta.sequence,
            version=self._book.version,
            quality=BookQuality.HEALTHY,
        )
        self._last_sequence = delta.sequence
        self._last_update = delta.timestamp
        return self._book

    def current(self, now: datetime) -> OrderBookSnapshot:
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if self._book is None:
            return OrderBookSnapshot(
                self.market_ticker, now, sequence=self._last_sequence, quality=self.quality
            )
        age = (now - self._last_update).total_seconds() if self._last_update else float("inf")
        if age > self.max_age_seconds and self._book.quality is BookQuality.HEALTHY:
            return OrderBookSnapshot(
                self.market_ticker,
                self._book.snapshot_timestamp,
                self._book.yes_bids,
                self._book.no_bids,
                self._book.sequence,
                self._book.version,
                BookQuality.STALE,
            )
        return self._book

    def healthy(self, now: datetime) -> OrderBookSnapshot | None:
        book = self.current(now)
        return book if book.quality is BookQuality.HEALTHY else None

    def _invalidate(self, quality: BookQuality) -> None:
        if self._book is not None:
            self._book = OrderBookSnapshot(
                self._book.market_ticker,
                self._book.snapshot_timestamp,
                self._book.yes_bids,
                self._book.no_bids,
                self._book.sequence,
                self._book.version,
                quality,
            )
        else:
            self._last_sequence = None
            self._invalid_quality = quality
        self._last_update = None


def _complement_level(level: OrderBookLevel | None) -> OrderBookLevel | None:
    return None if level is None else OrderBookLevel(level.price.complement(), level.count)


def _parse_wire_levels(raw: Any) -> tuple[OrderBookLevel, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
        raise ValueError("order-book levels must be an array")
    parsed: list[OrderBookLevel] = []
    for level in raw:
        if (
            not isinstance(level, Sequence)
            or isinstance(level, (str, bytes, bytearray))
            or len(level) != 2
        ):
            raise ValueError("each order-book level must be a two-item array")
        parsed.append(OrderBookLevel.parse(level[0], level[1]))
    return tuple(parsed)
