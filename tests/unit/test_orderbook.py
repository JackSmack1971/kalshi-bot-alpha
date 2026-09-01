from datetime import datetime, timezone
from decimal import Decimal

import pytest

from kalshi_bot.market_data.orderbook import (
    BookQuality,
    FixedPointCount,
    FixedPointPrice,
    OrderBookSnapshot,
    Side,
)


STAMP = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_rest_snapshot_normalizes_duplicates_and_derives_complements() -> None:
    snapshot = OrderBookSnapshot.from_rest(
        "KXBTC-1",
        {
            "orderbook_fp": {
                "yes_dollars": [["0.6000", "2.00"], ["0.4000", "1.00"], ["0.600", "3.00"]],
                "no_dollars": [["0.2500", "4.00"]],
            }
        },
        snapshot_timestamp=STAMP,
    )
    assert [level.price.value for level in snapshot.yes_bids] == [
        Decimal("0.4000"),
        Decimal("0.600"),
    ]
    assert snapshot.yes_best_bid is not None
    assert snapshot.yes_best_bid.count.value == Decimal("5.00")
    assert snapshot.yes_best_ask is not None
    yes_ask = snapshot.yes_best_ask
    assert yes_ask is not None
    assert yes_ask.price.value == Decimal("0.75")
    spread = snapshot.spread()
    assert spread is not None
    assert spread.value == Decimal("0.15")
    midpoint = snapshot.midpoint()
    assert midpoint is not None
    assert midpoint.value == Decimal("0.675")


def test_fixed_point_types_reject_binary_float_and_negative_count() -> None:
    with pytest.raises(TypeError):
        FixedPointPrice.parse(0.5)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        FixedPointCount.parse("-0.01")


def test_snapshot_is_immutable_and_quality_is_explicit() -> None:
    snapshot = OrderBookSnapshot("T1", STAMP, quality=BookQuality.HEALTHY)
    assert snapshot.quality is BookQuality.HEALTHY
    with pytest.raises(AttributeError):
        snapshot.quality = BookQuality.STALE  # type: ignore[misc]


def test_side_metrics_use_the_binary_complement() -> None:
    snapshot = OrderBookSnapshot.from_rest(
        "T1",
        {"yes_dollars": [["0.40", "1"]], "no_dollars": [["0.30", "1"]]},
        snapshot_timestamp=STAMP,
    )
    assert snapshot.best_bid(Side.NO).price.value == Decimal("0.30")  # type: ignore[union-attr]
    assert snapshot.best_ask(Side.NO).price.value == Decimal("0.60")  # type: ignore[union-attr]
