"""Structured logging with global secret redaction (Phase 1 PR 2).

The public API is exactly ``configure_logging`` and ``get_logger``.
Sensitive-value registration (``_register_sensitive_value`` in
``observability.logging``) is an internal hook for
``kalshi_bot.credentials.loader`` and is deliberately not re-exported
here.
"""

from kalshi_bot.observability.logging import configure_logging, get_logger

__all__ = ["configure_logging", "get_logger"]
