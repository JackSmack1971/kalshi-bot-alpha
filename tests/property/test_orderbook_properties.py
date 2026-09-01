from datetime import datetime, timedelta, timezone
from decimal import Decimal

from hypothesis import given, strategies as st

from kalshi_bot.market_data.orderbook import (
    BookQuality,
    FixedPointPrice,
    OrderBookDelta,
    OrderBookReconstructor,
    OrderBookSnapshot,
    Side,
)

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _snapshot(sequence: int = 10, count: str = "5") -> OrderBookSnapshot:
    return OrderBookSnapshot(
        "T1",
        NOW,
        yes_bids=(
            OrderBookSnapshot.from_rest(
                "T1",
                {"yes_dollars": [["0.50", count]], "no_dollars": []},
                snapshot_timestamp=NOW,
                sequence=sequence,
            ).yes_bids[0],
        ),
        sequence=sequence,
        quality=BookQuality.HEALTHY,
    )


@given(st.decimals(min_value="0.01", max_value="100", allow_nan=False, allow_infinity=False))
def test_negative_result_never_becomes_a_level(count: Decimal) -> None:
    reconstructor = OrderBookReconstructor("T1")
    reconstructor.apply_snapshot(_snapshot(count=str(count)))
    result = reconstructor.apply_delta(
        OrderBookDelta(
            "T1",
            11,
            Side.YES,
            FixedPointPrice.parse("0.50"),
            -count - Decimal("0.01"),
            NOW + timedelta(milliseconds=1),
        )
    )
    assert result is None
    assert reconstructor.quality is BookQuality.GAP
    assert reconstructor.healthy(NOW + timedelta(seconds=1)) is None


def test_gap_and_reordered_sequences_are_unusable_until_snapshot() -> None:
    reconstructor = OrderBookReconstructor("T1")
    reconstructor.apply_snapshot(_snapshot(11))
    assert (
        reconstructor.apply_delta(
            OrderBookDelta("T1", 12, Side.YES, FixedPointPrice.parse("0.50"), "1", NOW)
        )
        is not None
    )
    assert (
        reconstructor.apply_delta(
            OrderBookDelta("T1", 14, Side.YES, FixedPointPrice.parse("0.50"), "1", NOW)
        )
        is None
    )
    assert reconstructor.healthy(NOW) is None
    assert (
        reconstructor.apply_delta(
            OrderBookDelta("T1", 13, Side.YES, FixedPointPrice.parse("0.50"), "1", NOW)
        )
        is None
    )
    reconstructor.apply_snapshot(_snapshot(20))
    assert reconstructor.quality is BookQuality.HEALTHY


def test_duplicate_sequence_is_idempotent() -> None:
    reconstructor = OrderBookReconstructor("T1")
    reconstructor.apply_snapshot(_snapshot())
    delta = OrderBookDelta("T1", 11, Side.YES, FixedPointPrice.parse("0.50"), "1", NOW)
    first = reconstructor.apply_delta(delta)
    second = reconstructor.apply_delta(delta)
    assert first == second
    assert first is not None and first.yes_best_bid is not None
    assert first.yes_best_bid.count.value == Decimal("6")


def test_stale_books_are_not_exposed_as_healthy() -> None:
    reconstructor = OrderBookReconstructor("T1", max_age_seconds=2)
    reconstructor.apply_snapshot(_snapshot())
    assert reconstructor.healthy(NOW + timedelta(seconds=2)) is not None
    assert reconstructor.healthy(NOW + timedelta(seconds=2, milliseconds=1)) is None


def test_reconnect_reset_requires_a_fresh_snapshot() -> None:
    reconstructor = OrderBookReconstructor("T1")
    old = reconstructor.apply_snapshot(_snapshot(30))
    reconstructor.reset()
    assert reconstructor.healthy(NOW) is None
    assert (
        reconstructor.apply_delta(
            OrderBookDelta("T1", 31, Side.YES, FixedPointPrice.parse("0.50"), "1", NOW)
        )
        is None
    )
    fresh = reconstructor.apply_snapshot(_snapshot(4))
    assert fresh.sequence == 4
    assert fresh.yes_best_bid is not None
    assert fresh.yes_best_bid.count.value == old.yes_best_bid.count.value  # type: ignore[union-attr]
