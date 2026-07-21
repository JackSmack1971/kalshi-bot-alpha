"""Tests for kalshi_bot.config (Phase 1 PR 2)."""

from __future__ import annotations

import pytest

from kalshi_bot.config import AppConfig, ConfigError, CredentialReferences, load_config

VALID_DATA = {
    "log_level": "info",
    "rest_timeout_seconds": 5.0,
    "rest_max_retries": 3,
    "rest_retry_backoff_min_seconds": 0.5,
    "rest_retry_backoff_max_seconds": 8.0,
    "ws_timeout_seconds": 10.0,
    "ws_reconnect_backoff_min_seconds": 1.0,
    "ws_reconnect_backoff_max_seconds": 30.0,
    "credentials": {
        "access_key_env": "KALSHI_DEMO_ACCESS_KEY",
        "private_key_path_env": "KALSHI_DEMO_PRIVATE_KEY_PATH",
    },
}


def test_valid_data_loads_and_normalizes_log_level() -> None:
    config = load_config(VALID_DATA)

    assert isinstance(config, AppConfig)
    assert config.log_level == "INFO"
    assert config.rest_max_retries == 3
    assert isinstance(config.credentials, CredentialReferences)
    assert config.credentials.access_key_env == "KALSHI_DEMO_ACCESS_KEY"


def test_config_is_frozen() -> None:
    config = load_config(VALID_DATA)

    with pytest.raises(Exception):  # noqa: B017 - pydantic frozen-model error
        config.log_level = "DEBUG"


@pytest.mark.parametrize(
    "missing_field",
    [
        "rest_timeout_seconds",
        "rest_max_retries",
        "rest_retry_backoff_min_seconds",
        "rest_retry_backoff_max_seconds",
        "ws_timeout_seconds",
        "ws_reconnect_backoff_min_seconds",
        "ws_reconnect_backoff_max_seconds",
        "credentials",
    ],
)
def test_missing_required_field_raises_config_error(missing_field: str) -> None:
    data = {key: value for key, value in VALID_DATA.items() if key != missing_field}

    with pytest.raises(ConfigError):
        load_config(data)


def test_invalid_log_level_raises_config_error() -> None:
    data = {**VALID_DATA, "log_level": "NOT_A_LEVEL"}

    with pytest.raises(ConfigError):
        load_config(data)


@pytest.mark.parametrize(
    "field",
    [
        "rest_timeout_seconds",
        "rest_retry_backoff_min_seconds",
        "rest_retry_backoff_max_seconds",
        "ws_timeout_seconds",
        "ws_reconnect_backoff_min_seconds",
        "ws_reconnect_backoff_max_seconds",
    ],
)
def test_non_positive_bound_raises_config_error(field: str) -> None:
    data = {**VALID_DATA, field: 0.0}

    with pytest.raises(ConfigError):
        load_config(data)


def test_negative_retry_count_raises_config_error() -> None:
    data = {**VALID_DATA, "rest_max_retries": -1}

    with pytest.raises(ConfigError):
        load_config(data)


def test_backoff_max_below_min_raises_config_error() -> None:
    data = {
        **VALID_DATA,
        "rest_retry_backoff_min_seconds": 10.0,
        "rest_retry_backoff_max_seconds": 1.0,
    }

    with pytest.raises(ConfigError):
        load_config(data)


def test_ws_backoff_max_below_min_raises_config_error() -> None:
    data = {
        **VALID_DATA,
        "ws_reconnect_backoff_min_seconds": 10.0,
        "ws_reconnect_backoff_max_seconds": 1.0,
    }

    with pytest.raises(ConfigError):
        load_config(data)


def test_unknown_field_is_rejected() -> None:
    data = {**VALID_DATA, "environment": "production"}

    with pytest.raises(ConfigError):
        load_config(data)


def test_host_like_field_is_rejected() -> None:
    data = {**VALID_DATA, "host": "external-api.kalshi.co"}  # demo-scan: allow-negative-fixture

    with pytest.raises(ConfigError):
        load_config(data)


def test_credential_references_reject_invalid_env_var_name() -> None:
    with pytest.raises(Exception):  # noqa: B017 - pydantic validation error
        CredentialReferences(
            access_key_env="not-a-valid-name!",
            private_key_path_env="KALSHI_DEMO_PRIVATE_KEY_PATH",
        )


def test_credential_references_have_no_secret_field() -> None:
    refs = CredentialReferences(
        access_key_env="KALSHI_DEMO_ACCESS_KEY",
        private_key_path_env="KALSHI_DEMO_PRIVATE_KEY_PATH",
    )

    assert set(type(refs).model_fields) == {"access_key_env", "private_key_path_env"}
