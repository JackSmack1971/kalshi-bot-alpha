"""Tests for kalshi_bot.observability.logging wiring (Phase 1 PR 2).

These are behavioral tests of rendered output only -- the module
exports just ``configure_logging``/``get_logger``, so internals (the
redaction processor) are never imported or asserted on directly here.
"""

from __future__ import annotations

import io
import json
import logging

from kalshi_bot.observability import configure_logging, get_logger


def _read_json_lines(stream: io.StringIO) -> list[dict[str, object]]:
    return [json.loads(line) for line in stream.getvalue().splitlines() if line.strip()]


def test_configure_logging_emits_json_lines() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    get_logger("test.logging").info("hello", detail="value")

    lines = _read_json_lines(stream)
    assert len(lines) == 1
    assert lines[0]["event"] == "hello"
    assert lines[0]["detail"] == "value"
    assert lines[0]["level"] == "info"


def test_configure_logging_filters_below_configured_level() -> None:
    stream = io.StringIO()
    configure_logging(level="WARNING", stream=stream)

    logger = get_logger("test.logging.level")
    logger.info("should not appear")
    logger.warning("should appear")

    lines = _read_json_lines(stream)
    assert len(lines) == 1
    assert lines[0]["event"] == "should appear"


def test_reconfiguring_logging_replaces_handlers_rather_than_accumulating() -> None:
    stream_one = io.StringIO()
    configure_logging(level="INFO", stream=stream_one)

    stream_two = io.StringIO()
    configure_logging(level="INFO", stream=stream_two)

    get_logger("test.logging.reconfigure").info("only once")

    assert _read_json_lines(stream_one) == []
    lines = _read_json_lines(stream_two)
    assert len(lines) == 1
    assert lines[0]["event"] == "only once"
    assert len(logging.getLogger().handlers) == 1


def test_get_logger_returns_usable_logger_without_configure_logging_export() -> None:
    import kalshi_bot.observability as observability_pkg

    assert set(observability_pkg.__all__) == {"configure_logging", "get_logger"}
