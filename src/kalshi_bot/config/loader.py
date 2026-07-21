"""Validate supplied non-secret configuration data (Phase 1 PR 2).

This module validates an already-parsed mapping into an
:class:`~kalshi_bot.config.models.AppConfig`; it does not parse any
file format itself. Phase 1 PR 2 does not add a YAML dependency --
callers are responsible for producing the mapping (from JSON, an
already-parsed YAML document, environment variables, or any other
narrow source) before calling :func:`load_config`.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from kalshi_bot.config.models import AppConfig

__all__ = ["ConfigError", "load_config"]


class ConfigError(Exception):
    """Raised when supplied configuration data fails validation.

    The message contains only sanitized validation metadata -- field
    location, the stable pydantic error-type code, and pydantic's
    fixed message template -- never the rejected input value, the
    supplied mapping, or the raw ``ValidationError`` text. The mapping
    passed to :func:`load_config` is arbitrary at this boundary and may
    contain a caller-supplied secret in an unexpected or malformed
    field; the underlying ``ValidationError`` is deliberately not
    chained (``raise ... from None``) so it can never reach a
    traceback or the exception-logging pipeline.
    """


def _sanitize_validation_error(exc: ValidationError) -> str:
    parts = []
    for error in exc.errors(include_url=False, include_context=False, include_input=False):
        loc = ".".join(str(segment) for segment in error["loc"]) or "<root>"
        parts.append(f"{loc}: {error['type']} ({error['msg']})")
    return "; ".join(parts)


def load_config(data: Mapping[str, Any]) -> AppConfig:
    """Validate ``data`` into an :class:`AppConfig`.

    Raises a typed :class:`ConfigError` on any malformed or
    unrecognized field, before any network-capable object is
    constructed. The error message never includes the rejected value,
    the supplied mapping, or any other part of ``data``.
    """
    try:
        return AppConfig.model_validate(dict(data))
    except ValidationError as exc:
        raise ConfigError(f"invalid configuration: {_sanitize_validation_error(exc)}") from None
