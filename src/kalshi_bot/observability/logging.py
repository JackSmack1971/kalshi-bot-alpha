"""Canonical structured logging with global secret redaction (Phase 1 PR 2).

This is the permanent logging interface for the repository, not a
temporary stub: every logger, structlog-bound or stdlib/third-party,
is wired through the same processor chain so that access-key IDs,
signatures, authorization headers, and private-key material can never
reach emitted output, per ``docs/PHASE1_PLAN.md`` PR 2 and
``.claude/rules/credential-privacy.md``.

Redaction combines three narrow, precise mechanisms rather than a
broad content scan:

1. Recursive **exact-key** redaction over dict/list-shaped event data
   -- a fixed set of known-sensitive field names (``access_key``,
   ``signature``, ``authorization``, ``private_key``, ``api_key``,
   ``secret``, ``password``, ``token``, ``bearer_token``, and their
   documented variants), matched by normalized exact name so that
   legitimate fields such as ``input_token_count`` or ``secretary_id``
   are never caught by accident.
2. A narrow **PEM-block marker scan** (``-----BEGIN ...-----`` /
   ``-----END ...-----``) over string values and rendered exception
   text, so private-key material embedded in a message or traceback is
   still caught.
3. **Exact registered sensitive values** -- runtime secret values
   (currently: the loaded access-key ID; future PRs may register a
   computed request signature) registered once via
   :func:`register_sensitive_value` and then redacted wherever that
   exact substring appears in emitted text, including free-form
   messages and exception text, across both structlog and
   stdlib/third-party logging paths.

There is intentionally no generic base64/hex value-shape regex: that
would also redact legitimate hashes, IDs, and evidence values that are
not secrets.
"""

from __future__ import annotations

import logging
import re
import threading
from collections.abc import Mapping, MutableMapping
from typing import IO, Any

import structlog

__all__ = ["configure_logging", "get_logger", "register_sensitive_value"]

# Exact, normalized (lowercase, hyphens -> underscores) field names
# redacted regardless of nesting depth. Deliberately not substring or
# generic-suffix matching: "token_budget", "input_token_count", and
# "secretary_id" must never be redacted, so only names identical to an
# entry below (after normalization) match.
_SENSITIVE_EXACT_KEYS: frozenset[str] = frozenset(
    {
        "access_key",
        "access_key_id",
        "api_key",
        "authorization",
        "authorization_header",
        "signature",
        "private_key",
        "private_key_pem",
        "password",
        "secret",
        "token",
        "bearer",
        "bearer_token",
    }
)

_PEM_BLOCK_PATTERN = re.compile(
    r"-----BEGIN [A-Z0-9 ]+-----.*?-----END [A-Z0-9 ]+-----",
    re.DOTALL,
)

_REDACTED = "[REDACTED]"
_REDACTED_PEM = "[REDACTED-PEM]"

# Minimum length for a registered sensitive value before it is used for
# substring redaction. Short values would over-match unrelated text;
# real access-key IDs and signatures are always well above this length.
_MIN_REGISTERED_VALUE_LENGTH = 8

_registry_lock = threading.Lock()
_registered_sensitive_values: set[str] = set()


def register_sensitive_value(value: str) -> None:
    """Register an exact runtime secret value for redaction.

    Call this once, immediately after loading or computing a real
    secret value -- for example the access-key ID returned by
    :func:`kalshi_bot.credentials.loader.load_credentials`, or (in a
    later Phase 1 PR) a computed request signature -- and never log
    the value yourself in the interim. Once registered, the exact
    value is redacted wherever it appears in emitted output: plain
    messages, exception text, and nested structures, across both
    structlog and stdlib/third-party logging paths.

    Registered values cannot be read back through this module; there
    is no accessor. Values shorter than
    ``_MIN_REGISTERED_VALUE_LENGTH`` characters are ignored (too short
    to safely value-redact without over-matching unrelated text), as
    are empty or whitespace-only values.
    """
    if not value or not value.strip() or len(value) < _MIN_REGISTERED_VALUE_LENGTH:
        return
    with _registry_lock:
        _registered_sensitive_values.add(value)


def _reset_registered_sensitive_values_for_tests() -> None:
    """Test-only: clear registered values so tests do not leak across cases.

    Not part of the public API (not in ``__all__``); import it
    directly from this module only from test fixtures.
    """
    with _registry_lock:
        _registered_sensitive_values.clear()


def _is_sensitive_key(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_")
    return normalized in _SENSITIVE_EXACT_KEYS


def _redact_string(value: str) -> str:
    if _PEM_BLOCK_PATTERN.search(value):
        value = _PEM_BLOCK_PATTERN.sub(_REDACTED_PEM, value)
    with _registry_lock:
        registered = tuple(_registered_sensitive_values)
    for secret_value in registered:
        if secret_value in value:
            value = value.replace(secret_value, _REDACTED)
    return value


def _redact_value(value: Any) -> Any:
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, Mapping):
        return _redact_mapping(value)
    if isinstance(value, (list, tuple)):
        return type(value)(_redact_value(item) for item in value)
    return value


def _redact_mapping(mapping: Mapping[Any, Any]) -> dict[Any, Any]:
    redacted: dict[Any, Any] = {}
    for key, value in mapping.items():
        if isinstance(key, str) and _is_sensitive_key(key):
            redacted[key] = _REDACTED
        else:
            redacted[key] = _redact_value(value)
    return redacted


def _redact_processor(
    logger: Any, method_name: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    return _redact_mapping(event_dict)


def _build_shared_processors() -> list[Any]:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.ExtraAdder(),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        _redact_processor,
    ]


def configure_logging(level: str = "INFO", *, stream: IO[str] | None = None) -> None:
    """Configure the one canonical, redacted, JSON-structured logging pipeline.

    Wires ``structlog``-bound loggers and stdlib/third-party
    ``logging.Logger`` records through the identical processor chain
    (including ``_redact_processor``), so no logging path in the
    process can bypass redaction.

    ``stream`` is exposed only so tests can capture rendered output
    without touching internals; production callers should omit it.
    """
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    shared_processors = _build_shared_processors()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(stream) if stream is not None else logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(resolved_level)


def get_logger(name: str) -> Any:
    """Return a logger built from the canonical configured pipeline.

    Callers must never construct a logger any other way (no
    ``logging.getLogger`` call sites, no ``print``) so nothing bypasses
    ``configure_logging``'s redaction wiring.
    """
    return structlog.get_logger(name)
