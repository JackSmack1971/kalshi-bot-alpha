"""The only authority boundary between an intent and execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from kalshi_bot.market_data import BookQuality
from kalshi_bot.persistence import AccountSnapshot


@dataclass(frozen=True, slots=True)
class RiskLimits:
    max_risk_per_order: Decimal = Decimal("5.00")
    max_exposure_per_market: Decimal = Decimal("25.00")
    max_aggregate_exposure: Decimal = Decimal("100.00")
    max_open_orders: int = 10
    min_minutes_before_close: int = 30
    max_market_data_age_seconds: Decimal = Decimal("2")
    paper_bankroll: Decimal = Decimal("1000.00")


@dataclass(frozen=True, slots=True)
class MarketState:
    allowlisted: bool = True
    active: bool = True
    book_quality: BookQuality = BookQuality.HEALTHY
    book_age_seconds: Decimal = Decimal("0")
    minutes_to_close: Decimal = Decimal("60")


@dataclass(frozen=True, slots=True)
class RuntimeState:
    demo_mode: bool = True
    strategy_enabled: bool = True
    kill_switch: bool = False
    reconciliation_required: bool = False


@dataclass(frozen=True, slots=True)
class PortfolioState:
    account: AccountSnapshot
    open_order_count: int = 0
    daily_loss: Decimal = Decimal("0")
    drawdown: Decimal = Decimal("0")
    market_exposure: Decimal = Decimal("0")


@dataclass(frozen=True, slots=True)
class RiskDecision:
    risk_decision_id: str
    intent_id: str
    approved: bool
    reason_codes: tuple[str, ...]
    exposure: Decimal
    decided_at: datetime
    intent: object = field(repr=False)


class RiskGateway:
    """Evaluate every rule synchronously and return an immutable decision."""

    def evaluate(
        self,
        intent: object,
        market: MarketState,
        portfolio: PortfolioState,
        runtime: RuntimeState,
        limits: RiskLimits,
        *,
        now: datetime | None = None,
    ) -> RiskDecision:
        now = now or datetime.now(timezone.utc)
        reasons: list[str] = []
        price = getattr(intent, "limit_price", Decimal("0"))
        count = getattr(intent, "desired_count", 0)
        expiry = getattr(intent, "expiry_timestamp", now)
        exposure = price * Decimal(count)
        checks = (
            (runtime.demo_mode, "NOT_DEMO_MODE"),
            (runtime.strategy_enabled, "STRATEGY_DISABLED"),
            (not runtime.kill_switch, "KILL_SWITCH"),
            (not runtime.reconciliation_required, "RECONCILIATION_REQUIRED"),
            (market.allowlisted, "MARKET_NOT_ALLOWLISTED"),
            (market.active, "MARKET_INACTIVE"),
            (market.book_quality is BookQuality.HEALTHY, "BOOK_NOT_HEALTHY"),
            (market.book_age_seconds <= limits.max_market_data_age_seconds, "STALE_MARKET_DATA"),
            (market.minutes_to_close >= limits.min_minutes_before_close, "TOO_CLOSE_TO_CLOSE"),
            (isinstance(count, int) and count > 0, "INVALID_COUNT"),
            (Decimal("0.01") <= price <= Decimal("0.99"), "INVALID_PRICE"),
            (expiry > now, "INTENT_EXPIRED"),
            (exposure <= limits.max_risk_per_order, "ORDER_LIMIT"),
            (
                portfolio.market_exposure + exposure <= limits.max_exposure_per_market,
                "MARKET_LIMIT",
            ),
            (
                portfolio.account.open_order_exposure + exposure <= limits.max_aggregate_exposure,
                "PORTFOLIO_LIMIT",
            ),
            (portfolio.open_order_count < limits.max_open_orders, "OPEN_ORDER_LIMIT"),
            (portfolio.daily_loss <= limits.max_aggregate_exposure, "DAILY_LOSS_LIMIT"),
        )
        reasons.extend(code for passed, code in checks if not passed)
        return RiskDecision(
            str(uuid4()),
            getattr(intent, "intent_id", ""),
            not reasons,
            tuple(reasons),
            exposure,
            now,
            intent,
        )
