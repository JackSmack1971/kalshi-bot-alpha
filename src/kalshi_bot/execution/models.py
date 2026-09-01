"""Immutable execution-domain values."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from kalshi_bot.market_data import Side


class OrderState(StrEnum):
    INTENT_CREATED = "INTENT_CREATED"
    RISK_APPROVED = "RISK_APPROVED"
    SUBMISSION_PENDING = "SUBMISSION_PENDING"
    REJECTED = "REJECTED"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"
    RECONCILING = "RECONCILING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    OPEN = "OPEN"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCEL_PENDING = "CANCEL_PENDING"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True, slots=True)
class TradeIntent:
    intent_id: str | UUID
    strategy_id: str
    strategy_version: str
    market_ticker: str
    side: Side
    limit_price: Decimal
    desired_count: int
    feature_snapshot_id: str = "snapshot"
    market_archetype_id: str = "UNCLASSIFIED"
    action: str = "place"
    time_in_force: str = "good_till_canceled"
    post_only: bool = True
    expiry_timestamp: datetime | None = None
    reason_codes: tuple[str, ...] = ("SIMULATION",)
    signal_confidence: Decimal = Decimal("0")
    expected_fill_probability: Decimal = Decimal("0")
    expected_net_edge_usd: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if not self.market_ticker or self.desired_count <= 0:
            raise ValueError("intent market and positive desired_count are required")
        if isinstance(self.limit_price, float):
            raise TypeError("limit_price must not be a binary float")
        if not Decimal("0.01") <= self.limit_price <= Decimal("0.99"):
            raise ValueError("limit_price must be between 0.01 and 0.99")
        if self.expiry_timestamp is None:
            object.__setattr__(self, "expiry_timestamp", datetime.max.replace(tzinfo=timezone.utc))
