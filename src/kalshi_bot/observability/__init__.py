"""Structured logging with global secret redaction (Phase 1 PR 2)."""

from kalshi_bot.observability.logging import configure_logging, get_logger

__all__ = ["configure_logging", "get_logger"]
