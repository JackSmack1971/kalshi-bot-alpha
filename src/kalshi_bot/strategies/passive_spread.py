"""Small, deterministic passive-spread strategy for paper trading."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable
from uuid import uuid4

from kalshi_bot.execution import TradeIntent
from kalshi_bot.market_data import EligibilityDecision, OrderBookSnapshot, Side

if TYPE_CHECKING:
    from kalshi_bot.persistence import LedgerStore

EDGE_MODEL_VERSION = "passive-v0.1-conservative"
QUEUE_METHOD_VERSION = "queue-uncertain-v0.1"
_ZERO = Decimal("0")


def _text(value: Decimal) -> str:
    return format(value, "f")


@dataclass(frozen=True, slots=True)
class PassiveSpreadConfig:
    min_spread: Decimal = Decimal("0.03")
    max_inventory: Decimal = Decimal("25")
    quote_count: int = 1
    max_quote_age: timedelta = timedelta(seconds=30)
    min_price_move: Decimal = Decimal("0.01")
    stop_quoting_before_close: timedelta = timedelta(minutes=30)
    fee_per_contract: Decimal = Decimal("0.00")
    adverse_selection_per_contract: Decimal = Decimal("0.01")
    inventory_cost_per_contract: Decimal = Decimal("0.00")
    settlement_risk_per_contract: Decimal = Decimal("0.00")
    cancel_reprice_cost: Decimal = Decimal("0.00")
    fill_probability: Decimal = Decimal("0.10")
    signal_confidence: Decimal = Decimal("0")
    calibration_sample_size: int = 0
    calibration_confidence: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        if self.min_spread <= 0 or self.max_inventory < 0 or self.quote_count <= 0:
            raise ValueError("passive-spread limits must be positive")
        if self.max_quote_age <= timedelta(0) or self.min_price_move <= 0:
            raise ValueError("quote lifecycle limits must be positive")
        if self.stop_quoting_before_close < timedelta(0):
            raise ValueError("stop_quoting_before_close must not be negative")
        for name in ("fill_probability", "signal_confidence", "calibration_confidence"):
            value = getattr(self, name)
            if not Decimal("0") <= value <= Decimal("1"):
                raise ValueError(f"{name} must be between 0 and 1")
        if self.calibration_sample_size < 0:
            raise ValueError("calibration_sample_size must not be negative")


@dataclass(frozen=True, slots=True)
class FeatureSnapshot:
    snapshot_id: str
    market_ticker: str
    market_archetype_id: str
    captured_at: datetime
    best_bid: Decimal
    best_ask: Decimal
    spread: Decimal
    midpoint: Decimal
    top_level_size: Decimal
    book_age_seconds: Decimal
    time_to_close_seconds: Decimal
    current_inventory: Decimal

    @classmethod
    def from_book(
        cls,
        book: OrderBookSnapshot,
        *,
        now: datetime,
        time_to_close: timedelta,
        market_archetype_id: str,
        current_inventory: Decimal,
        side: Side = Side.YES,
    ) -> FeatureSnapshot:
        bid, ask = book.best_bid(side), book.best_ask(side)
        if bid is None or ask is None:
            raise ValueError("a feature snapshot requires both best bid and ask")
        if now.tzinfo is None or book.snapshot_timestamp.tzinfo is None:
            raise ValueError("snapshot timestamps must be timezone-aware")
        spread = ask.price.value - bid.price.value
        return cls(
            str(uuid4()),
            book.market_ticker,
            market_archetype_id,
            now,
            bid.price.value,
            ask.price.value,
            spread,
            (bid.price.value + ask.price.value) / 2,
            bid.count.value,
            Decimal(str(max(0, (now - book.snapshot_timestamp).total_seconds()))),
            Decimal(str(max(0, time_to_close.total_seconds()))),
            current_inventory,
        )

    def payload(self) -> dict[str, object]:
        return {
            name: _text(value) if isinstance(value, Decimal) else value
            for name, value in {
                "snapshot_id": self.snapshot_id,
                "market_ticker": self.market_ticker,
                "market_archetype_id": self.market_archetype_id,
                "captured_at": self.captured_at.isoformat(),
                "best_bid": self.best_bid,
                "best_ask": self.best_ask,
                "spread": self.spread,
                "midpoint": self.midpoint,
                "top_level_size": self.top_level_size,
                "book_age_seconds": self.book_age_seconds,
                "time_to_close_seconds": self.time_to_close_seconds,
                "current_inventory": self.current_inventory,
            }.items()
        }


@dataclass(frozen=True, slots=True)
class QueueStateEvidence:
    snapshot_id: str
    market_ticker: str
    displayed_size_ahead: Decimal
    queue_position_lower_bound: Decimal
    queue_position_upper_bound: Decimal
    quality: str = "UNCERTAIN"
    method_version: str = QUEUE_METHOD_VERSION
    assumptions: tuple[str, ...] = ("individual exchange queue priority is unavailable",)

    def __post_init__(self) -> None:
        if self.displayed_size_ahead < 0 or self.queue_position_lower_bound < 0:
            raise ValueError("queue sizes and lower bound must not be negative")
        if self.queue_position_upper_bound < self.queue_position_lower_bound:
            raise ValueError("queue lower bound must not exceed upper bound")
        if self.quality != "UNCERTAIN":
            raise ValueError("v0.1 queue evidence must remain UNCERTAIN")

    def payload(self) -> dict[str, object]:
        return {
            "queue_state_snapshot_id": self.snapshot_id,
            "market_ticker": self.market_ticker,
            "displayed_size_ahead": _text(self.displayed_size_ahead),
            "queue_position_lower_bound": _text(self.queue_position_lower_bound),
            "queue_position_upper_bound": _text(self.queue_position_upper_bound),
            "quality": self.quality,
            "method_version": self.method_version,
            "assumptions": list(self.assumptions),
        }


@dataclass(frozen=True, slots=True)
class QuoteExpectancy:
    quote_expectancy_id: str
    intent_id: str
    queue_state_snapshot_id: str
    market_ticker: str
    market_archetype_id: str
    edge_model_version: str
    signal_confidence: Decimal
    fill_probability: Decimal
    gross_spread_usd: Decimal
    fee_cost_usd: Decimal
    adverse_selection_usd: Decimal
    inventory_cost_usd: Decimal
    settlement_risk_usd: Decimal
    cancel_reprice_cost_usd: Decimal
    expected_net_edge_usd: Decimal
    calibration_sample_size: int
    calibration_confidence: Decimal
    created_at: datetime

    def payload(self) -> dict[str, object]:
        result = {
            "schema_version": "1.0.0",
            "quote_expectancy_id": self.quote_expectancy_id,
            "intent_id": self.intent_id,
            "market_ticker": self.market_ticker,
            "market_archetype_id": self.market_archetype_id,
            "queue_state_snapshot_id": self.queue_state_snapshot_id,
            "edge_model_version": self.edge_model_version,
            "signal_confidence": float(self.signal_confidence),
            "fill_probability": float(self.fill_probability),
            "fill_probability_lower_bound": 0.0,
            "fill_probability_upper_bound": float(self.fill_probability),
            "gross_spread_usd": self.gross_spread_usd,
            "fee_cost_usd": self.fee_cost_usd,
            "adverse_selection_usd": self.adverse_selection_usd,
            "inventory_cost_usd": self.inventory_cost_usd,
            "settlement_risk_usd": self.settlement_risk_usd,
            "cancel_reprice_cost_usd": self.cancel_reprice_cost_usd,
            "expected_net_edge_usd": self.expected_net_edge_usd,
            "calibration_method_version": QUEUE_METHOD_VERSION,
            "calibration_sample_size": self.calibration_sample_size,
            "calibration_confidence": float(self.calibration_confidence),
            "assumptions": ["conservative bounded fill estimate", "no empirical calibration"],
            "created_at": self.created_at.isoformat(),
        }
        return {
            key: _text(value) if isinstance(value, Decimal) else value
            for key, value in result.items()
        }


class PassiveSpreadStrategy:
    strategy_id = "passive_spread"
    strategy_version = "0.1.0"

    def __init__(self, config: PassiveSpreadConfig = PassiveSpreadConfig()) -> None:
        self.config = config

    def feature_snapshot(
        self,
        book: OrderBookSnapshot,
        *,
        now: datetime,
        eligibility: EligibilityDecision,
        time_to_close: timedelta,
        current_inventory: Decimal,
        side: Side = Side.YES,
    ) -> FeatureSnapshot:
        return FeatureSnapshot.from_book(
            book,
            now=now,
            time_to_close=time_to_close,
            market_archetype_id=eligibility.market_archetype_id,
            current_inventory=current_inventory,
            side=side,
        )

    def quote(
        self,
        features: FeatureSnapshot,
        *,
        eligibility: EligibilityDecision,
        now: datetime,
        existing_quotes: Iterable[TradeIntent] = (),
        store: LedgerStore | None = None,
    ) -> tuple[TradeIntent, QueueStateEvidence, QuoteExpectancy] | None:
        if now.tzinfo is None or not eligibility.eligible:
            return None
        if features.book_age_seconds > Decimal("2") or features.spread < self.config.min_spread:
            return None
        if (
            features.current_inventory + Decimal(self.config.quote_count)
            > self.config.max_inventory
        ):
            return None
        if features.time_to_close_seconds <= Decimal(
            str(self.config.stop_quoting_before_close.total_seconds())
        ):
            return None
        if any(
            q.market_ticker == features.market_ticker
            and q.side is Side.YES
            and q.post_only
            and q.action == "place"
            for q in existing_quotes
        ):
            return None
        intent_id = str(uuid4())
        queue = QueueStateEvidence(
            str(uuid4()),
            features.market_ticker,
            features.top_level_size,
            _ZERO,
            features.top_level_size,
        )
        gross = features.spread * Decimal(self.config.quote_count)
        fees = self.config.fee_per_contract * self.config.quote_count
        adverse = self.config.adverse_selection_per_contract * self.config.quote_count
        inventory = self.config.inventory_cost_per_contract * self.config.quote_count
        settlement = self.config.settlement_risk_per_contract * self.config.quote_count
        net = (
            self.config.fill_probability * (gross - fees - adverse - inventory - settlement)
            - self.config.cancel_reprice_cost
        )
        expectancy = QuoteExpectancy(
            str(uuid4()),
            intent_id,
            queue.snapshot_id,
            features.market_ticker,
            features.market_archetype_id,
            EDGE_MODEL_VERSION,
            self.config.signal_confidence,
            self.config.fill_probability,
            gross,
            fees,
            adverse,
            inventory,
            settlement,
            self.config.cancel_reprice_cost,
            net,
            self.config.calibration_sample_size,
            self.config.calibration_confidence,
            now,
        )
        intent = TradeIntent(
            intent_id=intent_id,
            strategy_id=self.strategy_id,
            strategy_version=self.strategy_version,
            market_ticker=features.market_ticker,
            side=Side.YES,
            limit_price=features.best_bid,
            desired_count=self.config.quote_count,
            feature_snapshot_id=features.snapshot_id,
            market_archetype_id=features.market_archetype_id,
            post_only=True,
            expiry_timestamp=now + self.config.max_quote_age,
            reason_codes=("PASSIVE_SPREAD", "POST_ONLY"),
            signal_confidence=self.config.signal_confidence,
            expected_fill_probability=self.config.fill_probability,
            expected_net_edge_usd=net,
        )
        if store is not None:
            expiry = intent.expiry_timestamp
            if expiry is None:
                raise AssertionError("passive quote expiry must be set")
            store.record_feature_snapshot(
                features.snapshot_id,
                features.market_ticker,
                features.market_archetype_id,
                features.payload(),
                features.captured_at.isoformat(),
            )
            store.record_strategy_intent(
                intent_id,
                self.strategy_id,
                features.market_ticker,
                features.market_archetype_id,
                {
                    "trade_intent": {
                        "intent_id": intent.intent_id,
                        "strategy_version": intent.strategy_version,
                        "side": intent.side.value,
                        "limit_price": _text(intent.limit_price),
                        "desired_count": intent.desired_count,
                        "post_only": intent.post_only,
                        "expiry_timestamp": expiry.isoformat(),
                        "reason_codes": list(intent.reason_codes),
                    }
                },
            )
            store.record_queue_state_snapshot(
                queue.snapshot_id,
                intent_id,
                features.market_ticker,
                queue.payload(),
                now.isoformat(),
            )
            store.record_quote_expectancy(
                expectancy.quote_expectancy_id,
                intent_id,
                queue.snapshot_id,
                features.market_ticker,
                expectancy.payload(),
                now.isoformat(),
            )
        return intent, queue, expectancy

    def cancel_reason(
        self,
        features: FeatureSnapshot,
        *,
        now: datetime,
        quote_created_at: datetime,
        eligible: bool,
        best_price_at_quote: Decimal,
        risk_enabled: bool = True,
    ) -> str | None:
        if not risk_enabled:
            return "RISK_OR_KILL_SWITCH"
        if not eligible:
            return "MARKET_NOT_ELIGIBLE"
        if features.book_age_seconds > Decimal("2"):
            return "STALE_DATA"
        if now - quote_created_at >= self.config.max_quote_age:
            return "QUOTE_TOO_OLD"
        if abs(features.best_bid - best_price_at_quote) >= self.config.min_price_move:
            return "BEST_PRICE_MOVED"
        if features.time_to_close_seconds <= Decimal(
            str(self.config.stop_quoting_before_close.total_seconds())
        ):
            return "TIME_TO_CLOSE"
        return None
