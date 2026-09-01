"""Operator-run, one-order demo acceptance lifecycle."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Protocol
from uuid import UUID, uuid4

from kalshi_bot.execution import TradeIntent
from kalshi_bot.market_data import BookQuality, OrderBookSnapshot, Side
from kalshi_bot.contracts.demo_endpoints import DEMO_REST_HOST
from kalshi_bot.persistence import LedgerStore
from kalshi_bot.reconciliation import ReconciliationResult, ReconciliationService
from kalshi_bot.risk import MarketState, PortfolioState, RiskGateway, RiskLimits, RuntimeState
from kalshi_bot.rest.models import Balance, Fill, Order, Position
from kalshi_bot.rest.errors import AmbiguousOutcomeError


class _OrderClient(Protocol):
    @property
    def base_url(self) -> str: ...

    def create_limit_order(
        self,
        *,
        ticker: str,
        client_order_id: str | UUID,
        side: str,
        count: int,
        price: Decimal | str | int,
        store: Any,
        intent_id: str | None = None,
        feature_snapshot_id: str | None = None,
        risk_decision_id: str | None = None,
        time_in_force: str = "good_till_canceled",
    ) -> Order: ...
    def cancel_order(self, *, order_id: str) -> Order: ...
    def get_order(self, *, order_id: str) -> Order: ...
    def list_open_orders(self) -> tuple[Order, ...]: ...
    def get_fills(self) -> tuple[Fill, ...]: ...
    def get_positions(self) -> tuple[Position, ...]: ...
    def get_balance(self) -> Balance: ...


@dataclass(frozen=True, slots=True)
class DemoSmokeResult:
    client_order_id: str
    reconciliation: ReconciliationResult


def run_demo_smoke_order(
    *,
    client: _OrderClient,
    store: LedgerStore,
    ticker: str,
    price: Decimal | str,
    count: int,
    book: OrderBookSnapshot,
    risk: RiskGateway,
    limits: RiskLimits,
) -> DemoSmokeResult:
    if client.base_url != f"https://{DEMO_REST_HOST}/trade-api/v2":
        raise RuntimeError("acceptance requires the fixed Kalshi demo REST client")
    if count != 1:
        raise ValueError("demo acceptance requires exactly one contract")
    if book.market_ticker != ticker or book.quality is not BookQuality.HEALTHY:
        raise RuntimeError("acceptance requires a healthy order book for the requested ticker")
    accepted_price = Decimal(str(price))
    best_ask = book.best_ask(Side.YES)
    if best_ask is not None and accepted_price >= best_ask.price.value:
        raise RuntimeError("post-only acceptance price would cross the healthy book")
    intent = TradeIntent(
        intent_id=str(uuid4()),
        strategy_id="demo-acceptance",
        strategy_version="acceptance-v1",
        market_ticker=ticker,
        side=Side.YES,
        limit_price=Decimal(str(price)),
        desired_count=count,
        feature_snapshot_id=str(uuid4()),
        reason_codes=("OPERATOR_ACCEPTANCE",),
    )
    now = datetime.now(timezone.utc)
    decision = risk.evaluate(
        intent,
        MarketState(book_quality=book.quality, book_age_seconds=Decimal("0")),
        PortfolioState(store.replay()),
        RuntimeState(demo_mode=True),
        limits,
        now=now,
    )
    if not decision.approved:
        raise PermissionError(f"acceptance risk rejected: {','.join(decision.reason_codes)}")
    store.record_strategy_intent(
        str(intent.intent_id),
        intent.strategy_id,
        ticker,
        intent.market_archetype_id,
        {"acceptance": True},
    )
    store.record_feature_snapshot(
        intent.feature_snapshot_id, ticker, intent.market_archetype_id, {"acceptance": True}
    )
    store.record_risk_decision(
        decision.risk_decision_id, str(intent.intent_id), True, {"acceptance": True}
    )
    order_id = str(uuid4())
    try:
        acknowledged = client.create_limit_order(
            ticker=ticker,
            client_order_id=order_id,
            side="bid",
            count=count,
            price=price,
            store=store,
            intent_id=str(intent.intent_id),
            feature_snapshot_id=intent.feature_snapshot_id,
            risk_decision_id=decision.risk_decision_id,
        )
    except AmbiguousOutcomeError:
        ReconciliationService(store, client).on_uncertain_submission()
        raise
    if acknowledged.client_order_id != order_id or acknowledged.order_id is None:
        raise RuntimeError("demo order acknowledgement did not identify the submitted order")
    store.transition_order(order_id, "ACKNOWLEDGED", "OPEN", "acceptance-acknowledged")
    try:
        cancelled = client.cancel_order(order_id=acknowledged.order_id)
    except AmbiguousOutcomeError:
        ReconciliationService(store, client).reconcile(trigger="uncertain-cancellation")
        raise
    if cancelled.status not in {"cancelled", "canceled", "executed", "filled"}:
        raise RuntimeError("demo order cancellation was not confirmed")
    verified = client.get_order(order_id=acknowledged.order_id)
    if verified.status not in {"cancelled", "canceled", "executed", "filled"}:
        raise RuntimeError("demo order cancellation was not independently verified")
    store.transition_order(order_id, "OPEN", "CANCELLED", "acceptance-cancelled")
    final = ReconciliationService(store, client).reconcile(trigger="acceptance-final")
    if not final.clean:
        raise RuntimeError("acceptance ended suspended: reconciliation required")
    if client.list_open_orders() or store.replay().positions:
        raise RuntimeError("acceptance left residual order or exposure")
    return DemoSmokeResult(order_id, final)
