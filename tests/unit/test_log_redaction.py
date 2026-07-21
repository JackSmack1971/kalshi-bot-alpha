"""Adversarial redaction suite (Phase 1 PR 2).

Proves that structural secret redaction holds across every logging
path this repository can produce, using exact registered synthetic
secret values rather than realistic-looking material. Only key-based
and PEM-marker redaction is exercised -- there is no generic
base64/hex value-shape redaction, so this suite does not attempt to
prove redaction of arbitrary hash-shaped strings (those are legitimate
evidence values, not secrets).
"""

from __future__ import annotations

import io
import json
import logging
from collections.abc import Iterator

import pytest

from kalshi_bot.observability import configure_logging, get_logger, register_sensitive_value
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests

# Exact registered synthetic secret values. Never realistic-looking.
SYNTHETIC_ACCESS_KEY = "SYNTHETIC-ACCESS-KEY-0001"
SYNTHETIC_SIGNATURE = "SYNTHETIC-SIGNATURE-0002"
SYNTHETIC_AUTH_HEADER = "Bearer SYNTHETIC-TOKEN-0003"
SYNTHETIC_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "SYNTHETIC-KEY-MATERIAL-0004\n"
    "-----END PRIVATE KEY-----"
)


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


def _read_json_lines(stream: io.StringIO) -> list[dict[str, object]]:
    return [json.loads(line) for line in stream.getvalue().splitlines() if line.strip()]


def test_bound_structlog_log_redacts_sensitive_keys() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    get_logger("test.redaction.structlog").info(
        "request signed",
        access_key=SYNTHETIC_ACCESS_KEY,
        signature=SYNTHETIC_SIGNATURE,
        authorization=SYNTHETIC_AUTH_HEADER,
        market_ticker="KXBTC-25JAN01",
    )

    rendered = stream.getvalue()
    assert SYNTHETIC_ACCESS_KEY not in rendered
    assert SYNTHETIC_SIGNATURE not in rendered
    assert SYNTHETIC_AUTH_HEADER not in rendered

    line = _read_json_lines(stream)[0]
    assert line["access_key"] == "[REDACTED]"
    assert line["signature"] == "[REDACTED]"
    assert line["authorization"] == "[REDACTED]"
    assert line["market_ticker"] == "KXBTC-25JAN01"


def test_stdlib_log_with_structured_extra_redacts_sensitive_keys() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    stdlib_logger = logging.getLogger("test.redaction.stdlib")
    stdlib_logger.info("stdlib event", extra={"authorization": SYNTHETIC_AUTH_HEADER})

    rendered = stream.getvalue()
    assert SYNTHETIC_AUTH_HEADER not in rendered

    line = _read_json_lines(stream)[0]
    assert line["authorization"] == "[REDACTED]"


def test_simulated_third_party_log_redacts_sensitive_keys() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    # A "third-party" logger is just another stdlib logger under a
    # foreign name -- this repository never controls its call sites,
    # so redaction must hold regardless of logger name.
    third_party_logger = logging.getLogger("some_vendor_sdk.transport")
    third_party_logger.warning(
        "signed request failed", extra={"signature": SYNTHETIC_SIGNATURE}
    )

    rendered = stream.getvalue()
    assert SYNTHETIC_SIGNATURE not in rendered

    line = _read_json_lines(stream)[0]
    assert line["signature"] == "[REDACTED]"


def test_exception_message_pem_marker_is_redacted_structlog() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    try:
        raise ValueError(f"signing failed with key material: {SYNTHETIC_PEM}")
    except ValueError:
        get_logger("test.redaction.exception").exception("signing failed")

    rendered = stream.getvalue()
    assert SYNTHETIC_PEM not in rendered
    assert "SYNTHETIC-KEY-MATERIAL-0004" not in rendered
    assert "[REDACTED-PEM]" in rendered


def test_exception_message_pem_marker_is_redacted_stdlib() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    stdlib_logger = logging.getLogger("test.redaction.stdlib_exception")
    try:
        raise ValueError(f"signing failed with key material: {SYNTHETIC_PEM}")
    except ValueError:
        stdlib_logger.exception("signing failed")

    rendered = stream.getvalue()
    assert SYNTHETIC_PEM not in rendered
    assert "SYNTHETIC-KEY-MATERIAL-0004" not in rendered
    assert "[REDACTED-PEM]" in rendered


def test_nested_dict_and_list_structures_are_redacted() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    get_logger("test.redaction.nested").info(
        "nested event",
        request={
            "headers": {"authorization": SYNTHETIC_AUTH_HEADER},
            "items": [
                {"access_key": SYNTHETIC_ACCESS_KEY},
                "unrelated-item",
                {"nested_again": {"signature": SYNTHETIC_SIGNATURE}},
            ],
        },
    )

    rendered = stream.getvalue()
    assert SYNTHETIC_AUTH_HEADER not in rendered
    assert SYNTHETIC_ACCESS_KEY not in rendered
    assert SYNTHETIC_SIGNATURE not in rendered

    line = _read_json_lines(stream)[0]
    request: dict[str, object] = line["request"]  # type: ignore[assignment]
    headers: dict[str, object] = request["headers"]  # type: ignore[assignment]
    items: list[object] = request["items"]  # type: ignore[assignment]
    assert headers["authorization"] == "[REDACTED]"
    assert items[0]["access_key"] == "[REDACTED]"  # type: ignore[index]
    assert items[1] == "unrelated-item"
    assert items[2]["nested_again"]["signature"] == "[REDACTED]"  # type: ignore[index]


def test_legitimate_hash_and_id_values_are_not_redacted() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    legitimate_hash = "a" * 64  # sha256-hex-shaped, not a secret
    legitimate_order_id = "order-6b1f7e2c-demo"

    get_logger("test.redaction.legitimate").info(
        "market event",
        content_hash=legitimate_hash,
        order_id=legitimate_order_id,
    )

    line = _read_json_lines(stream)[0]
    assert line["content_hash"] == legitimate_hash
    assert line["order_id"] == legitimate_order_id


# -- Precise key matching: exact-name/normalized match, not substring --


def test_exact_sensitive_key_names_are_redacted() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    fields = {
        "access_key": "s1",
        "access_key_id": "s2",
        "api_key": "s3",
        "authorization": "s4",
        "authorization_header": "s5",
        "signature": "s6",
        "private_key": "s7",
        "private_key_pem": "s8",
        "password": "s9",
        "secret": "s10",
        "token": "s11",
        "bearer_token": "s12",
    }
    get_logger("test.redaction.precise").info("event", **fields)

    line = _read_json_lines(stream)[0]
    for field_name in fields:
        assert line[field_name] == "[REDACTED]", field_name


def test_benign_lookalike_keys_are_not_redacted() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    get_logger("test.redaction.benign").info(
        "event",
        input_token_count=42,
        output_token_count=7,
        token_budget=1000,
        secretary_id="employee-42",
        bearer_status="active",
    )

    line = _read_json_lines(stream)[0]
    assert line["input_token_count"] == 42
    assert line["output_token_count"] == 7
    assert line["token_budget"] == 1000
    assert line["secretary_id"] == "employee-42"
    assert line["bearer_status"] == "active"


# -- Exact registered sensitive values --


def test_registered_value_is_redacted_in_free_form_structlog_message() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    registered_secret = "SYNTHETIC-REGISTERED-ACCESS-KEY-0005"
    register_sensitive_value(registered_secret)

    get_logger("test.redaction.registered").info(
        f"authenticated request using key {registered_secret} succeeded"
    )

    rendered = stream.getvalue()
    assert registered_secret not in rendered
    assert "[REDACTED]" in rendered


def test_registered_value_is_redacted_in_exception_text() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    registered_secret = "SYNTHETIC-REGISTERED-SIGNATURE-0006"
    register_sensitive_value(registered_secret)

    try:
        raise ValueError(f"request failed for key {registered_secret}")
    except ValueError:
        get_logger("test.redaction.registered_exception").exception("request failed")

    rendered = stream.getvalue()
    assert registered_secret not in rendered


def test_registered_value_is_redacted_in_stdlib_log() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    registered_secret = "SYNTHETIC-REGISTERED-VALUE-0007"
    register_sensitive_value(registered_secret)

    logging.getLogger("test.redaction.registered_stdlib").info(
        "value is %s", registered_secret
    )

    rendered = stream.getvalue()
    assert registered_secret not in rendered


def test_registered_value_is_redacted_in_nested_structure() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    registered_secret = "SYNTHETIC-REGISTERED-NESTED-0008"
    register_sensitive_value(registered_secret)

    get_logger("test.redaction.registered_nested").info(
        "event", details={"note": f"used {registered_secret} for this call"}
    )

    rendered = stream.getvalue()
    assert registered_secret not in rendered


def test_short_registered_value_is_ignored() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    short_value = "abc123"  # below the minimum registration length
    register_sensitive_value(short_value)

    get_logger("test.redaction.short").info(f"code is {short_value}")

    rendered = stream.getvalue()
    assert short_value in rendered  # too short to safely value-redact


def test_registry_reset_stops_further_redaction() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    registered_secret = "SYNTHETIC-REGISTERED-RESET-CHECK-0009"
    register_sensitive_value(registered_secret)
    _reset_registered_sensitive_values_for_tests()

    get_logger("test.redaction.reset").info(f"value is {registered_secret}")

    rendered = stream.getvalue()
    assert registered_secret in rendered
