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

    Configuration data is non-secret by construction (see
    :class:`~kalshi_bot.config.models.AppConfig`), so it is safe for
    this error's message to include the underlying validation detail.
    """


def load_config(data: Mapping[str, Any]) -> AppConfig:
    """Validate ``data`` into an :class:`AppConfig`.

    Raises a typed :class:`ConfigError` on any malformed or
    unrecognized field, before any network-capable object is
    constructed.
    """
    try:
        return AppConfig.model_validate(dict(data))
    except ValidationError as exc:
        raise ConfigError(f"invalid configuration: {exc}") from exc
