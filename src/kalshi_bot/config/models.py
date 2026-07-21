"""Non-secret Phase 1 configuration models (Phase 1 PR 2).

Every field here is either a non-secret runtime bound (timeouts,
retry/backoff bounds, log level) or a reference to where a secret
lives (``CredentialReferences``) -- never a literal secret value.
There is no host, environment, or endpoint-selector field of any kind:
the demo host is a hard-coded constant in
``kalshi_bot.contracts.demo_endpoints``, never configuration, per
``.claude/rules/kalshi-transport-safety.md``.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

__all__ = ["AppConfig", "CredentialReferences"]

_ENV_VAR_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

_VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


class CredentialReferences(BaseModel):
    """Pointers to where Kalshi demo credentials live -- never a value.

    ``access_key_env`` and ``private_key_path_env`` are validated only
    for environment-variable identifier syntax. That validation cannot
    make misuse structurally impossible: both fields are plain strings
    by necessity (they name environment variables to be read later by
    ``kalshi_bot.credentials.loader``), so nothing here stops a caller
    from passing a secret-shaped string into them. Callers must not do
    so; this type simply never has a field designated to hold a secret
    value itself.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    access_key_env: str
    private_key_path_env: str

    @field_validator("access_key_env", "private_key_path_env")
    @classmethod
    def _validate_env_var_name(cls, value: str) -> str:
        if not _ENV_VAR_NAME_PATTERN.match(value):
            raise ValueError(
                "must be a valid environment variable identifier "
                "(letters, digits, underscore, not starting with a digit)"
            )
        return value


class AppConfig(BaseModel):
    """Non-secret Phase 1 runtime configuration.

    Covers the REST and WebSocket timeout/retry/backoff bounds
    committed in ``docs/PHASE1_PLAN.md`` PR 2/4/5, plus
    ``credentials`` (references only). ``extra="forbid"`` rejects any
    unrecognized field outright -- including an injected
    host/environment-selector key -- rather than silently ignoring it.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    log_level: str = "INFO"

    rest_timeout_seconds: float = Field(gt=0)
    rest_max_retries: int = Field(ge=0)
    rest_retry_backoff_min_seconds: float = Field(gt=0)
    rest_retry_backoff_max_seconds: float = Field(gt=0)

    ws_timeout_seconds: float = Field(gt=0)
    ws_reconnect_backoff_min_seconds: float = Field(gt=0)
    ws_reconnect_backoff_max_seconds: float = Field(gt=0)

    credentials: CredentialReferences

    @field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: str) -> str:
        upper = value.upper()
        if upper not in _VALID_LOG_LEVELS:
            raise ValueError(f"log_level must be one of {sorted(_VALID_LOG_LEVELS)}")
        return upper

    @model_validator(mode="after")
    def _validate_backoff_bounds(self) -> "AppConfig":
        if self.rest_retry_backoff_max_seconds < self.rest_retry_backoff_min_seconds:
            raise ValueError(
                "rest_retry_backoff_max_seconds must be >= rest_retry_backoff_min_seconds"
            )
        if self.ws_reconnect_backoff_max_seconds < self.ws_reconnect_backoff_min_seconds:
            raise ValueError(
                "ws_reconnect_backoff_max_seconds must be >= ws_reconnect_backoff_min_seconds"
            )
        return self
