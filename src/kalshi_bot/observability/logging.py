"""Canonical structured logging with global secret redaction (Phase 1 PR 2).

This is the permanent logging interface for the repository, not a
temporary stub: every logger, structlog-bound or stdlib/third-party,
is wired through the same processor chain so that access-key IDs,
signatures, authorization headers, and private-key material can never
reach emitted output, per ``docs/PHASE1_PLAN.md`` PR 2 and
``.claude/rules/credential-privacy.md``.

Redaction is deliberately narrow and structural rather than a broad
content scan:

- Recursive key-based redaction over dict/list-shaped event data --
  any key that looks like a credential (``access_key``, ``signature``,
  ``authorization``, ``private_key``, ``api_key``, ``secret``,
  ``password``, ``token``, ``bearer``, case-insensitive) has its value
  replaced, at any nesting depth.
- A narrow PEM-block marker scan (``-----BEGIN ...-----`` /
  ``-----END ...-----``) over string values and rendered exception
  text, so private-key material embedded in a message or traceback is
  still caught.

There is intentionally no generic base64/hex value-shape regex: that
would also redact legitimate hashes, IDs, and evidence values that are
not secrets.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Mapping, MutableMapping
from typing import IO, Any

import structlog

__all__ = ["configure_logging", "get_logger"]

_SENSITIVE_KEY_PATTERN = re.compile(
    r"(access[_-]?key|signature|authoriz|auth[_-]?header|private[_-]?key|"
    r"api[_-]?key|secret|password|token|bearer)",
    re.IGNORECASE,
)

_PEM_BLOCK_PATTERN = re.compile(
    r"-----BEGIN [A-Z0-9 ]+-----.*?-----END [A-Z0-9 ]+-----",
    re.DOTALL,
)

_REDACTED = "[REDACTED]"
_REDACTED_PEM = "[REDACTED-PEM]"


def _redact_string(value: str) -> str:
    if _PEM_BLOCK_PATTERN.search(value):
        return _PEM_BLOCK_PATTERN.sub(_REDACTED_PEM, value)
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
        if isinstance(key, str) and _SENSITIVE_KEY_PATTERN.search(key):
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
