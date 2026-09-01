from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

from kalshi_bot.market_data import (
    BookQuality,
    EligibilityDecision,
    EligibilityReason,
    OrderBookLevel,
    OrderBookSnapshot,
    Side,
)
from kalshi_bot.persistence import LedgerStore
from kalshi_bot.strategies import FeatureSnapshot, PassiveSpreadConfig, PassiveSpreadStrategy


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def book() -> OrderBookSnapshot:
    return OrderBookSnapshot(
        "KXBTC-TEST",
        NOW,
        yes_bids=(OrderBookLevel.parse("0.40", "12"),),
        no_bids=(OrderBookLevel.parse("0.55", "20"),),
        quality=BookQuality.HEALTHY,
    )


def eligible() -> EligibilityDecision:
    return EligibilityDecision(
        "KXBTC-TEST", True, "BTC_THRESHOLD_SHORT", (EligibilityReason.ELIGIBLE,)
    )


def features(strategy: PassiveSpreadStrategy) -> FeatureSnapshot:
    return strategy.feature_snapshot(
        book(),
        now=NOW,
        eligibility=eligible(),
        time_to_close=timedelta(hours=1),
        current_inventory=Decimal("0"),
    )


def test_emits_one_post_only_bid_with_complete_evidence() -> None:
    strategy = PassiveSpreadStrategy()
    snapshot = features(strategy)
    result = strategy.quote(snapshot, eligibility=eligible(), now=NOW)
    assert result is not None
    intent, queue, expectancy = result
    assert (intent.side, intent.limit_price, intent.post_only, intent.desired_count) == (
        Side.YES,
        Decimal("0.40"),
        True,
        1,
    )
    assert queue.quality == "UNCERTAIN"
    assert queue.queue_position_lower_bound == Decimal("0")
    assert queue.queue_position_upper_bound == Decimal("12")
    assert expectancy.edge_model_version == "passive-v0.1-conservative"
    assert expectancy.expected_net_edge_usd == Decimal("0.0040")


def test_rejects_threshold_inventory_and_duplicate_quote() -> None:
    strategy = PassiveSpreadStrategy(PassiveSpreadConfig(max_inventory=Decimal("1")))
    snapshot = features(strategy)
    first = strategy.quote(snapshot, eligibility=eligible(), now=NOW)
    assert first is not None
    assert (
        strategy.quote(snapshot, eligibility=eligible(), now=NOW, existing_quotes=(first[0],))
        is None
    )
    over_limit = strategy.feature_snapshot(
        book(),
        now=NOW,
        eligibility=eligible(),
        time_to_close=timedelta(hours=1),
        current_inventory=Decimal("1"),
    )
    assert strategy.quote(over_limit, eligibility=eligible(), now=NOW) is None


def test_persists_inputs_and_evidence(tmp_path: Path) -> None:
    store = LedgerStore.connect(tmp_path / "strategy.sqlite3", migrate=True)
    strategy = PassiveSpreadStrategy()
    snapshot = features(strategy)
    result = strategy.quote(snapshot, eligibility=eligible(), now=NOW, store=store)
    assert result is not None
    intent, queue, expectancy = result
    assert store._connection.execute("SELECT COUNT(*) FROM feature_snapshots").fetchone()[0] == 1
    assert store._connection.execute("SELECT COUNT(*) FROM strategy_intents").fetchone()[0] == 1
    assert (
        store._connection.execute("SELECT COUNT(*) FROM queue_state_snapshots").fetchone()[0] == 1
    )
    row = store._connection.execute("SELECT payload_json FROM quote_expectancy_records").fetchone()
    assert row is not None and "passive-v0.1-conservative" in row[0]
    assert intent.feature_snapshot_id == snapshot.snapshot_id
    assert queue.snapshot_id == expectancy.queue_state_snapshot_id
    store.close()


def test_cancel_reasons_fail_closed() -> None:
    strategy = PassiveSpreadStrategy()
    snapshot = features(strategy)
    assert (
        strategy.cancel_reason(
            snapshot,
            now=NOW,
            quote_created_at=NOW,
            eligible=True,
            best_price_at_quote=Decimal("0.40"),
            risk_enabled=False,
        )
        == "RISK_OR_KILL_SWITCH"
    )
    assert (
        strategy.cancel_reason(
            snapshot,
            now=NOW + timedelta(seconds=31),
            quote_created_at=NOW,
            eligible=True,
            best_price_at_quote=Decimal("0.40"),
        )
        == "QUOTE_TOO_OLD"
    )
