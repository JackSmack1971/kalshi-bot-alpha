from datetime import datetime, timedelta, timezone

import pytest

from kalshi_bot.market_data import (
    BookQuality,
    EligibilityConfig,
    EligibilityReason,
    MarketCandidate,
    MarketStatus,
    OrderBookSnapshot,
    evaluate_eligibility,
)

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def candidate(**changes: object) -> MarketCandidate:
    values: dict[str, object] = {
        "market_ticker": "KXBTC-TEST",
        "series_ticker": "KXBTC",
        "category": "crypto",
        "status": MarketStatus.OPEN,
        "close_time": NOW + timedelta(hours=1),
    }
    values.update(changes)
    return MarketCandidate(**values)  # type: ignore[arg-type]


def healthy_book(
    *, quality: BookQuality = BookQuality.HEALTHY, stamp: datetime = NOW
) -> OrderBookSnapshot:
    return OrderBookSnapshot.from_rest(
        "KXBTC-TEST",
        {"yes_dollars": [["0.40", "1"]], "no_dollars": [["0.50", "1"]]},
        snapshot_timestamp=stamp,
        quality=quality,
    )


def test_all_prerequisites_produce_eligible_decision_with_archetype() -> None:
    book = healthy_book()
    decision = evaluate_eligibility(
        candidate(), book, now=NOW, config=EligibilityConfig({"KXBTC": "BTC_THRESHOLD_SHORT"})
    )
    assert decision.eligible is True
    assert decision.market_archetype_id == "BTC_THRESHOLD_SHORT"
    assert decision.reasons == (EligibilityReason.ELIGIBLE,)


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        ({"category": "sports"}, EligibilityReason.NOT_CRYPTO),
        ({"series_ticker": "KXETH"}, EligibilityReason.SERIES_NOT_APPROVED),
        ({"status": MarketStatus.PAUSED}, EligibilityReason.MARKET_NOT_OPEN),
        ({"close_time": NOW + timedelta(minutes=29)}, EligibilityReason.TOO_CLOSE_TO_CLOSE),
    ],
)
def test_market_prerequisites_fail_closed(
    change: dict[str, object], reason: EligibilityReason
) -> None:
    book = OrderBookSnapshot.from_rest(
        "KXBTC-TEST",
        {"yes_dollars": [["0.40", "1"]], "no_dollars": [["0.50", "1"]]},
        snapshot_timestamp=NOW,
    )
    decision = evaluate_eligibility(
        candidate(**change),
        book,
        now=NOW,
        config=EligibilityConfig({"KXBTC": "BTC_THRESHOLD_SHORT"}),
    )
    assert decision.eligible is False
    assert reason in decision.reasons
    assert decision.market_archetype_id


@pytest.mark.parametrize(
    "book",
    [None, healthy_book(quality=BookQuality.GAP), healthy_book(stamp=NOW - timedelta(seconds=3))],
)
def test_book_health_and_freshness_are_required(book: OrderBookSnapshot | None) -> None:
    decision = evaluate_eligibility(
        candidate(), book, now=NOW, config=EligibilityConfig({"KXBTC": "BTC_THRESHOLD_SHORT"})
    )
    assert decision.eligible is False
    assert decision.market_archetype_id == "BTC_THRESHOLD_SHORT"


def test_unknown_series_gets_unclassified_archetype() -> None:
    decision = evaluate_eligibility(
        candidate(series_ticker="KXETH"),
        None,
        now=NOW,
        config=EligibilityConfig({"KXBTC": "BTC_THRESHOLD_SHORT"}),
    )
    assert decision.market_archetype_id == "UNCLASSIFIED_V0_1"


@pytest.mark.parametrize(
    "book",
    [
        OrderBookSnapshot.from_rest(
            "KXBTC-TEST",
            {"yes_dollars": [["0.40", "1"]], "no_dollars": [["0.60", "1"]]},
            snapshot_timestamp=NOW,
        ),
        OrderBookSnapshot.from_rest(
            "KXBTC-TEST", {"yes_dollars": [["0.40", "1"]], "no_dollars": []}, snapshot_timestamp=NOW
        ),
    ],
)
def test_nonzero_spread_is_required(book: OrderBookSnapshot) -> None:
    decision = evaluate_eligibility(
        candidate(), book, now=NOW, config=EligibilityConfig({"KXBTC": "BTC_THRESHOLD_SHORT"})
    )
    assert decision.eligible is False
    assert any(
        reason in decision.reasons
        for reason in (EligibilityReason.SPREAD_NONPOSITIVE, EligibilityReason.SPREAD_UNAVAILABLE)
    )


def test_crossed_book_is_rejected_without_raising() -> None:
    book = OrderBookSnapshot.from_rest(
        "KXBTC-TEST",
        {"yes_dollars": [["0.70", "1"]], "no_dollars": [["0.40", "1"]]},
        snapshot_timestamp=NOW,
    )
    decision = evaluate_eligibility(
        candidate(), book, now=NOW, config=EligibilityConfig({"KXBTC": "BTC_THRESHOLD_SHORT"})
    )
    assert decision.eligible is False
    assert EligibilityReason.SPREAD_NONPOSITIVE in decision.reasons
