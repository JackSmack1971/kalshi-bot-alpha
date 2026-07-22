"""Bounded/expiring transient-secret redaction registry (Phase 1 PR 3 fix).

Exercises ``_register_transient_sensitive_value`` and its interaction
with ``_redact_string`` directly against a deterministic, injected
monotonic clock -- no real sleeps. Persistent-registry behavior is
covered by ``tests/unit/test_log_redaction.py``; this file proves the
transient registry's TTL, capacity, and eviction semantics in
isolation, plus that it does not disturb the persistent registry.
"""

from __future__ import annotations

import io
import threading
from collections.abc import Iterator

import pytest

import kalshi_bot.observability.logging as logging_module
from kalshi_bot.observability import configure_logging, get_logger
from kalshi_bot.observability.logging import (
    _register_sensitive_value,
    _register_transient_sensitive_value,
    _reset_registered_sensitive_values_for_tests,
    _transient_registry_size_for_tests,
)


class _FakeClock:
    """Deterministic, manually-advanced monotonic clock for tests."""

    def __init__(self, start: float = 1_000_000.0) -> None:
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


@pytest.fixture
def fake_clock(monkeypatch: pytest.MonkeyPatch) -> _FakeClock:
    clock = _FakeClock()
    monkeypatch.setattr(logging_module, "_monotonic", clock)
    return clock


def _signature(suffix: str) -> str:
    return f"SYNTHETIC-TRANSIENT-SIGNATURE-{suffix}"


# -- Basic redaction --


def test_newly_registered_transient_value_is_redacted(fake_clock: _FakeClock) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    value = _signature("0001")
    _register_transient_sensitive_value(value)

    get_logger("test.transient.basic").info(f"signature is {value}")

    rendered = stream.getvalue()
    assert value not in rendered
    assert "[REDACTED]" in rendered


def test_repeated_registration_of_same_value_is_harmless(fake_clock: _FakeClock) -> None:
    value = _signature("0002")
    _register_transient_sensitive_value(value)
    _register_transient_sensitive_value(value)
    _register_transient_sensitive_value(value)

    assert _transient_registry_size_for_tests() == 1


def test_short_transient_value_is_ignored(fake_clock: _FakeClock) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    short_value = "abc123"
    _register_transient_sensitive_value(short_value)

    get_logger("test.transient.short").info(f"code is {short_value}")

    rendered = stream.getvalue()
    assert short_value in rendered


# -- TTL expiry --


def test_expired_transient_value_is_no_longer_redacted(fake_clock: _FakeClock) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    value = _signature("0003")
    _register_transient_sensitive_value(value)
    fake_clock.advance(logging_module._TRANSIENT_VALUE_TTL_SECONDS + 1.0)

    get_logger("test.transient.expired").info(f"signature is {value}")

    rendered = stream.getvalue()
    assert value in rendered


def test_expired_transient_value_is_pruned_from_registry(fake_clock: _FakeClock) -> None:
    value = _signature("0004")
    _register_transient_sensitive_value(value)
    assert _transient_registry_size_for_tests() == 1

    fake_clock.advance(logging_module._TRANSIENT_VALUE_TTL_SECONDS + 1.0)
    # Pruning happens opportunistically on the next registration or redaction.
    _register_transient_sensitive_value(_signature("0005"))

    assert _transient_registry_size_for_tests() == 1


def test_value_just_under_ttl_is_still_redacted(fake_clock: _FakeClock) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    value = _signature("0006")
    _register_transient_sensitive_value(value)
    fake_clock.advance(logging_module._TRANSIENT_VALUE_TTL_SECONDS - 1.0)

    get_logger("test.transient.not_expired").info(f"signature is {value}")

    rendered = stream.getvalue()
    assert value not in rendered


# -- Capacity and eviction --


def test_registry_never_exceeds_configured_maximum(fake_clock: _FakeClock) -> None:
    max_values = logging_module._MAX_TRANSIENT_VALUES
    for i in range(max_values + 50):
        _register_transient_sensitive_value(_signature(f"cap-{i:05d}"))

    assert _transient_registry_size_for_tests() == max_values


def test_entries_are_evicted_oldest_first_when_capacity_exceeded(fake_clock: _FakeClock) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    max_values = logging_module._MAX_TRANSIENT_VALUES
    first_value = _signature("evict-first")
    _register_transient_sensitive_value(first_value)

    for i in range(max_values):
        _register_transient_sensitive_value(_signature(f"evict-fill-{i:05d}"))

    assert _transient_registry_size_for_tests() == max_values

    get_logger("test.transient.evicted").info(f"signature is {first_value}")
    rendered = stream.getvalue()
    assert first_value in rendered  # evicted -- no longer redacted

    stream.truncate(0)
    stream.seek(0)
    last_value = _signature(f"evict-fill-{max_values - 1:05d}")
    get_logger("test.transient.retained").info(f"signature is {last_value}")
    rendered = stream.getvalue()
    assert last_value not in rendered  # still present -- still redacted


# -- Isolation from the persistent registry --


def test_persistent_registration_is_not_evicted_with_transient_signatures(
    fake_clock: _FakeClock,
) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    access_key = "SYNTHETIC-PERSISTENT-ACCESS-KEY-0007"
    _register_sensitive_value(access_key)

    max_values = logging_module._MAX_TRANSIENT_VALUES
    for i in range(max_values + 50):
        _register_transient_sensitive_value(_signature(f"isolation-{i:05d}"))

    get_logger("test.transient.isolation").info(f"access key is {access_key}")
    rendered = stream.getvalue()
    assert access_key not in rendered


def test_reset_hook_clears_both_registries(fake_clock: _FakeClock) -> None:
    _register_sensitive_value("SYNTHETIC-PERSISTENT-RESET-CHECK-0008")
    _register_transient_sensitive_value(_signature("reset-check"))

    _reset_registered_sensitive_values_for_tests()

    assert _transient_registry_size_for_tests() == 0


# -- Overlap / ordering / logging cost --


def test_overlapping_transient_and_persistent_values_remain_longest_first_safe(
    fake_clock: _FakeClock,
) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    shorter = "SYNTHETIC-OVERLAP-TRANSIENT-BASE-0009"
    longer = shorter + "-EXTENDED-SUFFIX"
    _register_sensitive_value(shorter)
    _register_transient_sensitive_value(longer)

    get_logger("test.transient.overlap").info(f"key in use: {longer}")

    rendered = stream.getvalue()
    assert longer not in rendered
    assert shorter not in rendered
    assert "-EXTENDED-SUFFIX" not in rendered


def test_logging_cost_does_not_iterate_expired_historical_entries(fake_clock: _FakeClock) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    for i in range(500):
        _register_transient_sensitive_value(_signature(f"history-{i:05d}"))
        fake_clock.advance(1.0)

    fake_clock.advance(logging_module._TRANSIENT_VALUE_TTL_SECONDS)

    current_value = _signature("current")
    _register_transient_sensitive_value(current_value)

    get_logger("test.transient.no_growth").info(f"signature is {current_value}")

    assert _transient_registry_size_for_tests() == 1


# -- Thread safety --


def test_concurrent_transient_registration_and_logging_does_not_raise_or_leak(
    fake_clock: _FakeClock,
) -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    values = [_signature(f"concurrent-{i:05d}") for i in range(20)]
    errors: list[BaseException] = []

    def register_and_log(value: str) -> None:
        try:
            _register_transient_sensitive_value(value)
            get_logger("test.transient.concurrent").info(f"using {value}")
        except BaseException as exc:  # noqa: BLE001 - captured for the assertion below
            errors.append(exc)

    threads = [threading.Thread(target=register_and_log, args=(value,)) for value in values]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)

    assert errors == []
    rendered = stream.getvalue()
    for value in values:
        assert value not in rendered


def test_no_public_accessor_exposes_transient_registry() -> None:
    public_names = [name for name in dir(logging_module) if not name.startswith("_")]
    forbidden_terms = ("transient", "registered", "registry", "sensitive_value")
    leaking = [
        name for name in public_names if any(term in name.lower() for term in forbidden_terms)
    ]

    assert leaking == []
