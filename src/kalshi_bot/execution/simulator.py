"""Conservative, replayable local matching and order-state machine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from kalshi_bot.execution.models import OrderState, TradeIntent
from kalshi_bot.persistence import Direction, FinancialEvent, FinancialEventType, LedgerStore
from kalshi_bot.risk import RiskDecision

_TRANSITIONS = {
    OrderState.INTENT_CREATED: {OrderState.RISK_APPROVED},
    OrderState.RISK_APPROVED: {OrderState.SUBMISSION_PENDING},
    OrderState.SUBMISSION_PENDING: {
        OrderState.ACKNOWLEDGED,
        OrderState.REJECTED,
        OrderState.OUTCOME_UNKNOWN,
    },
    OrderState.ACKNOWLEDGED: {OrderState.OPEN, OrderState.FILLED, OrderState.CANCELLED},
    OrderState.OPEN: {
        OrderState.PARTIALLY_FILLED,
        OrderState.FILLED,
        OrderState.CANCEL_PENDING,
        OrderState.EXPIRED,
    },
    OrderState.PARTIALLY_FILLED: {
        OrderState.PARTIALLY_FILLED,
        OrderState.FILLED,
        OrderState.CANCEL_PENDING,
        OrderState.EXPIRED,
    },
    OrderState.CANCEL_PENDING: {OrderState.CANCELLED},
    OrderState.OUTCOME_UNKNOWN: {OrderState.RECONCILING},
    OrderState.RECONCILING: {
        OrderState.ACKNOWLEDGED,
        OrderState.REJECTED,
        OrderState.CANCELLED,
        OrderState.FILLED,
    },
}


@dataclass(frozen=True, slots=True)
class SimulatedFill:
    fill_id: str
    order_id: str
    quantity: Decimal
    price: Decimal
    fee: Decimal


@dataclass(frozen=True, slots=True)
class SimulatedOrder:
    client_order_id: str
    intent: TradeIntent
    submitted_count: Decimal
    filled_count: Decimal
    remaining_count: Decimal
    state: OrderState


class LocalSimulator:
    """Execution accepts only an approved :class:`RiskDecision`."""

    def __init__(self, store: LedgerStore, *, fee_rate: Decimal = Decimal("0")) -> None:
        if isinstance(fee_rate, float) or fee_rate < 0:
            raise TypeError("fee_rate must be a non-negative Decimal")
        self.store = store
        self.fee_rate = fee_rate

    def submit(
        self,
        decision: RiskDecision,
        *,
        evidence: str = "simulated-submit",
        best_opposite_price: Decimal | None = None,
        auto_acknowledge: bool = True,
    ) -> SimulatedOrder:
        if not decision.approved:
            raise PermissionError("execution requires an approved risk decision")
        intent = decision.intent
        if not isinstance(intent, TradeIntent):
            raise TypeError("risk decision does not contain a TradeIntent")
        order_id = str(uuid4())
        self.store.record_strategy_intent(
            str(intent.intent_id),
            intent.strategy_id,
            intent.market_ticker,
            intent.market_archetype_id,
            {"strategy_version": intent.strategy_version},
        )
        self.store.record_feature_snapshot(
            intent.feature_snapshot_id, intent.market_ticker, intent.market_archetype_id, {}
        )
        self.store.record_risk_decision(
            decision.risk_decision_id,
            str(intent.intent_id),
            True,
            {"exposure": format(decision.exposure, "f")},
        )
        self.store.record_order(
            order_id,
            str(intent.intent_id),
            intent.feature_snapshot_id,
            decision.risk_decision_id,
            intent.market_ticker,
            intent.side,
            intent.desired_count,
            intent.limit_price,
            OrderState.INTENT_CREATED.value,
        )
        self.store.transition_order(
            order_id, None, OrderState.INTENT_CREATED.value, "intent-created"
        )
        self._transition(
            order_id, OrderState.INTENT_CREATED, OrderState.RISK_APPROVED, "risk-approved"
        )
        self._transition(
            order_id, OrderState.RISK_APPROVED, OrderState.SUBMISSION_PENDING, evidence
        )
        if (
            intent.post_only
            and best_opposite_price is not None
            and best_opposite_price <= intent.limit_price
        ):
            self._transition(
                order_id,
                OrderState.SUBMISSION_PENDING,
                OrderState.REJECTED,
                "post-only-would-cross",
            )
            return SimulatedOrder(
                order_id,
                intent,
                Decimal(intent.desired_count),
                Decimal("0"),
                Decimal(intent.desired_count),
                OrderState.REJECTED,
            )
        self.store.record_event(
            FinancialEvent(
                FinancialEventType.ORDER_RESERVED,
                f"reserve:{order_id}",
                market_ticker=intent.market_ticker,
                client_order_id=order_id,
                amount=decision.exposure,
            )
        )
        if not auto_acknowledge:
            return SimulatedOrder(
                order_id,
                intent,
                Decimal(intent.desired_count),
                Decimal("0"),
                Decimal(intent.desired_count),
                OrderState.SUBMISSION_PENDING,
            )
        self._transition(
            order_id, OrderState.SUBMISSION_PENDING, OrderState.ACKNOWLEDGED, "simulated-ack"
        )
        self._transition(order_id, OrderState.ACKNOWLEDGED, OrderState.OPEN, "simulated-open")
        return SimulatedOrder(
            order_id,
            intent,
            Decimal(intent.desired_count),
            Decimal("0"),
            Decimal(intent.desired_count),
            OrderState.OPEN,
        )

    def fill(
        self,
        order: SimulatedOrder,
        quantity: Decimal | int | str,
        *,
        price: Decimal | None = None,
        fill_id: str | None = None,
    ) -> SimulatedOrder:
        quantity = Decimal(quantity)
        price = price if price is not None else order.intent.limit_price
        if quantity <= 0 or quantity > order.remaining_count:
            raise ValueError("fill quantity exceeds remaining order quantity")
        fill_id = fill_id or str(uuid4())
        fee = quantity * price * self.fee_rate
        direction = Direction.BUY if order.intent.side.value == "YES" else Direction.BUY
        applied = self.store.apply_fill(
            fill_id,
            order.client_order_id,
            order.intent.market_ticker,
            order.intent.side,
            direction,
            quantity,
            price,
            fee,
        )
        if not applied:
            return order
        filled = order.filled_count + quantity
        remaining = order.submitted_count - filled
        state = OrderState.FILLED if remaining == 0 else OrderState.PARTIALLY_FILLED
        self._transition(order.client_order_id, order.state, state, f"fill:{fill_id}")
        return SimulatedOrder(
            order.client_order_id, order.intent, order.submitted_count, filled, remaining, state
        )

    def cancel(self, order: SimulatedOrder) -> SimulatedOrder:
        if order.state not in (OrderState.OPEN, OrderState.PARTIALLY_FILLED):
            return order
        self._transition(
            order.client_order_id, order.state, OrderState.CANCEL_PENDING, "simulated-cancel"
        )
        release = order.remaining_count * order.intent.limit_price
        if release:
            self.store.record_event(
                FinancialEvent(
                    FinancialEventType.ORDER_RELEASED,
                    f"release:{order.client_order_id}:{order.remaining_count}",
                    client_order_id=order.client_order_id,
                    amount=release,
                )
            )
        self._transition(
            order.client_order_id,
            OrderState.CANCEL_PENDING,
            OrderState.CANCELLED,
            "simulated-cancel-ack",
        )
        return SimulatedOrder(
            order.client_order_id,
            order.intent,
            order.submitted_count,
            order.filled_count,
            order.remaining_count,
            OrderState.CANCELLED,
        )

    def mark_outcome_unknown(self, order: SimulatedOrder) -> SimulatedOrder:
        self._transition(
            order.client_order_id, order.state, OrderState.OUTCOME_UNKNOWN, "simulated-ambiguous"
        )
        return SimulatedOrder(
            order.client_order_id,
            order.intent,
            order.submitted_count,
            order.filled_count,
            order.remaining_count,
            OrderState.OUTCOME_UNKNOWN,
        )

    def begin_reconciliation(self, order: SimulatedOrder) -> SimulatedOrder:
        self._transition(
            order.client_order_id, order.state, OrderState.RECONCILING, "simulated-reconciliation"
        )
        return SimulatedOrder(
            order.client_order_id,
            order.intent,
            order.submitted_count,
            order.filled_count,
            order.remaining_count,
            OrderState.RECONCILING,
        )

    def mark(self, order: SimulatedOrder, price: Decimal) -> None:
        """Persist an exact mark used by the replayed unrealized P&L projection."""
        self.store.record_event(
            FinancialEvent(
                FinancialEventType.POSITION_MARKED,
                f"mark:{order.client_order_id}:{price}",
                market_ticker=order.intent.market_ticker,
                client_order_id=order.client_order_id,
                side=order.intent.side,
                price=price,
            )
        )

    def _transition(
        self, order_id: str, previous: OrderState, state: OrderState, evidence: str
    ) -> None:
        if state not in _TRANSITIONS.get(previous, set()):
            raise ValueError(f"illegal order transition {previous} -> {state}")
        self.store.transition_order(
            order_id, previous.value, state.value, evidence, datetime.now(timezone.utc).isoformat()
        )
