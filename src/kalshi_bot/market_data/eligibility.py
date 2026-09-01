"""Deterministic, fail-closed market eligibility and trading-state gate.

This module classifies no market dynamically and has no network or execution
side effects.  The approved series-to-archetype mapping is reviewed static
configuration; all runtime decisions are derived from the supplied snapshots.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from kalshi_bot.market_data.orderbook import BookQuality, OrderBookSnapshot

__all__ = [
    "EligibilityConfig",
    "EligibilityDecision",
    "EligibilityReason",
    "MarketCandidate",
    "MarketStatus",
    "UNCLASSIFIED_ARCHETYPE_ID",
    "evaluate_eligibility",
]

UNCLASSIFIED_ARCHETYPE_ID: Final = "UNCLASSIFIED_V0_1"


class MarketStatus(StrEnum):
    OPEN = "open"
    UNOPENED = "unopened"
    PAUSED = "paused"
    CLOSED = "closed"
    SETTLED = "settled"


class EligibilityReason(StrEnum):
    ELIGIBLE = "eligible"
    NOT_CRYPTO = "not_crypto"
    SERIES_NOT_APPROVED = "series_not_approved"
    MARKET_NOT_OPEN = "market_not_open"
    TOO_CLOSE_TO_CLOSE = "insufficient_time_before_close"
    BOOK_UNAVAILABLE = "book_unavailable"
    BOOK_NOT_HEALTHY = "book_not_healthy"
    BOOK_TICKER_MISMATCH = "book_ticker_mismatch"
    DATA_STALE = "data_stale"
    DATA_TIMESTAMP_INVALID = "data_timestamp_invalid"
    SPREAD_UNAVAILABLE = "spread_unavailable"
    SPREAD_NONPOSITIVE = "spread_nonpositive"


@dataclass(frozen=True, slots=True)
class EligibilityConfig:
    """Reviewed static eligibility controls; no automatic allowlisting."""

    approved_series: Mapping[str, str]
    min_remaining: timedelta = timedelta(minutes=30)
    max_data_age: timedelta = timedelta(seconds=2)
    crypto_category: str = "crypto"

    def __post_init__(self) -> None:
        if self.min_remaining < timedelta(0):
            raise ValueError("min_remaining must not be negative")
        if self.max_data_age <= timedelta(0):
            raise ValueError("max_data_age must be positive")
        if not self.crypto_category:
            raise ValueError("crypto_category must not be empty")
        mapping = dict(self.approved_series)
        if any(not series or not archetype for series, archetype in mapping.items()):
            raise ValueError("approved_series keys and archetypes must be non-empty")
        object.__setattr__(self, "approved_series", MappingProxyType(mapping))


@dataclass(frozen=True, slots=True)
class MarketCandidate:
    market_ticker: str
    series_ticker: str
    category: str
    status: MarketStatus
    close_time: datetime


@dataclass(frozen=True, slots=True)
class EligibilityDecision:
    market_ticker: str
    eligible: bool
    market_archetype_id: str
    reasons: tuple[EligibilityReason, ...]


def evaluate_eligibility(
    candidate: MarketCandidate,
    book: OrderBookSnapshot | None,
    *,
    now: datetime,
    config: EligibilityConfig,
) -> EligibilityDecision:
    """Evaluate every deterministic prerequisite and return an auditable decision."""
    if now.tzinfo is None or candidate.close_time.tzinfo is None:
        raise ValueError("now and close_time must be timezone-aware")
    archetype = config.approved_series.get(candidate.series_ticker, UNCLASSIFIED_ARCHETYPE_ID)
    reasons: list[EligibilityReason] = []

    if candidate.category != config.crypto_category:
        reasons.append(EligibilityReason.NOT_CRYPTO)
    if candidate.series_ticker not in config.approved_series:
        reasons.append(EligibilityReason.SERIES_NOT_APPROVED)
    if candidate.status is not MarketStatus.OPEN:
        reasons.append(EligibilityReason.MARKET_NOT_OPEN)
    if candidate.close_time - now < config.min_remaining:
        reasons.append(EligibilityReason.TOO_CLOSE_TO_CLOSE)

    if book is None:
        reasons.extend((EligibilityReason.BOOK_UNAVAILABLE, EligibilityReason.SPREAD_UNAVAILABLE))
    elif book.market_ticker != candidate.market_ticker:
        reasons.extend(
            (EligibilityReason.BOOK_TICKER_MISMATCH, EligibilityReason.SPREAD_UNAVAILABLE)
        )
    else:
        if book.quality is not BookQuality.HEALTHY:
            reasons.append(EligibilityReason.BOOK_NOT_HEALTHY)
        age = now - book.snapshot_timestamp
        if age < timedelta(0):
            reasons.append(EligibilityReason.DATA_TIMESTAMP_INVALID)
        elif age > config.max_data_age:
            reasons.append(EligibilityReason.DATA_STALE)
        try:
            spread = book.spread()
        except ValueError:
            spread = None
            reasons.append(EligibilityReason.SPREAD_NONPOSITIVE)
        if spread is None and EligibilityReason.SPREAD_NONPOSITIVE not in reasons:
            reasons.append(EligibilityReason.SPREAD_UNAVAILABLE)
        elif spread is not None and spread.value <= 0:
            reasons.append(EligibilityReason.SPREAD_NONPOSITIVE)

    if not reasons:
        reasons.append(EligibilityReason.ELIGIBLE)
    return EligibilityDecision(
        market_ticker=candidate.market_ticker,
        eligible=reasons == [EligibilityReason.ELIGIBLE],
        market_archetype_id=archetype,
        reasons=tuple(reasons),
    )
