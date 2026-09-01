from datetime import datetime, timezone
from decimal import Decimal
from tempfile import TemporaryDirectory
from hypothesis import given, settings, strategies as st

from kalshi_bot.execution import LocalSimulator, TradeIntent
from kalshi_bot.market_data import Side
from kalshi_bot.persistence import AccountSnapshot, LedgerStore
from kalshi_bot.risk import MarketState, PortfolioState, RiskGateway, RiskLimits, RuntimeState


@given(
    st.integers(min_value=1, max_value=100),
    st.lists(st.integers(min_value=1, max_value=20), min_size=1, max_size=8),
)
@settings(deadline=None, max_examples=50)
def test_randomized_fill_reconstructs_exactly(submitted: int, requests: list[int]) -> None:
    with TemporaryDirectory() as directory:
        store = LedgerStore.connect(f"{directory}/execution.sqlite3", migrate=True)
        intent = TradeIntent(
            intent_id=f"intent-{submitted}-{requests}",
            strategy_id="s",
            strategy_version="1",
            market_ticker="M",
            side=Side.YES,
            limit_price=Decimal("0.25"),
            desired_count=submitted,
            expiry_timestamp=datetime(2030, 1, 1, tzinfo=timezone.utc),
        )
        account = AccountSnapshot(Decimal("0"), Decimal("0"), Decimal("0"), Decimal("0"), ())
        decision = RiskGateway().evaluate(
            intent,
            MarketState(),
            PortfolioState(account),
            RuntimeState(),
            RiskLimits(max_risk_per_order=Decimal("100")),
            now=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        simulator = LocalSimulator(store)
        order = simulator.submit(decision)
        total = 0
        for index, requested in enumerate(requests):
            quantity = min(requested, submitted - total)
            if quantity == 0:
                break
            order = simulator.fill(order, quantity, fill_id=f"fill-{submitted}-{index}")
            total += quantity
        assert order.filled_count <= order.submitted_count
        assert order.remaining_count >= 0
        assert store.replay().positions[0].quantity == order.filled_count
        assert store.replay().cash == -(Decimal("0.25") * order.filled_count)
        store.close()


@given(st.integers(min_value=1, max_value=20), st.integers(min_value=0, max_value=25))
@settings(deadline=None, max_examples=50)
def test_approved_exposure_never_exceeds_limits(count: int, existing: int) -> None:
    intent = TradeIntent(
        intent_id=f"risk-{count}-{existing}",
        strategy_id="s",
        strategy_version="1",
        market_ticker="M",
        side=Side.YES,
        limit_price=Decimal("0.25"),
        desired_count=count,
        expiry_timestamp=datetime(2030, 1, 1, tzinfo=timezone.utc),
    )
    account = AccountSnapshot(Decimal("0"), Decimal("0"), Decimal("0"), Decimal(existing), ())
    limits = RiskLimits(max_risk_per_order=Decimal("5"), max_exposure_per_market=Decimal("25"))
    decision = RiskGateway().evaluate(
        intent,
        MarketState(),
        PortfolioState(account, market_exposure=Decimal(existing)),
        RuntimeState(),
        limits,
        now=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    if decision.approved:
        assert existing + decision.exposure <= limits.max_exposure_per_market
        assert decision.exposure <= limits.max_risk_per_order
