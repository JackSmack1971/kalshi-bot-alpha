"""Tests for kalshi_bot.credentials.loader (Phase 1 PR 2).

Portable across platforms: permission failures are mocked rather than
relying on POSIX file modes, so these tests behave identically on
Windows and POSIX.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from kalshi_bot.config.models import CredentialReferences
from kalshi_bot.credentials.loader import (
    CredentialLoadError,
    LoadedDemoCredentials,
    load_credentials,
)

SYNTHETIC_ACCESS_KEY = "SYNTHETIC-ACCESS-KEY-not-a-real-secret"
SYNTHETIC_PEM = (
    "-----BEGIN PRIVATE KEY-----\n"
    "SYNTHETIC-KEY-MATERIAL-not-a-real-secret\n"
    "-----END PRIVATE KEY-----\n"
).encode()

ACCESS_KEY_ENV = "TEST_KALSHI_ACCESS_KEY"
PRIVATE_KEY_PATH_ENV = "TEST_KALSHI_PRIVATE_KEY_PATH"

REFS = CredentialReferences(
    access_key_env=ACCESS_KEY_ENV,
    private_key_path_env=PRIVATE_KEY_PATH_ENV,
)


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ACCESS_KEY_ENV, raising=False)
    monkeypatch.delenv(PRIVATE_KEY_PATH_ENV, raising=False)


def test_missing_access_key_env_var_raises(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(SYNTHETIC_PEM)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(key_file))

    with pytest.raises(CredentialLoadError) as excinfo:
        load_credentials(REFS)

    assert ACCESS_KEY_ENV in str(excinfo.value)
    assert SYNTHETIC_PEM.decode() not in str(excinfo.value)


def test_missing_private_key_path_env_var_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)

    with pytest.raises(CredentialLoadError) as excinfo:
        load_credentials(REFS)

    assert PRIVATE_KEY_PATH_ENV in str(excinfo.value)
    assert SYNTHETIC_ACCESS_KEY not in str(excinfo.value)


def test_missing_key_file_raises(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(tmp_path / "does-not-exist.pem"))

    with pytest.raises(CredentialLoadError) as excinfo:
        load_credentials(REFS)

    assert "does not exist" in str(excinfo.value)
    assert SYNTHETIC_ACCESS_KEY not in str(excinfo.value)


def test_directory_path_raises(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(tmp_path))

    with pytest.raises(CredentialLoadError) as excinfo:
        load_credentials(REFS)

    assert "directory" in str(excinfo.value)


def test_read_failure_is_mocked_not_relying_on_posix_permissions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(SYNTHETIC_PEM)
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(key_file))

    with patch.object(Path, "read_bytes", side_effect=PermissionError("mocked permission denial")):
        with pytest.raises(CredentialLoadError) as excinfo:
            load_credentials(REFS)

    assert "could not be read" in str(excinfo.value)
    assert "mocked permission denial" not in str(excinfo.value)


def test_empty_key_file_raises(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(b"")
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(key_file))

    with pytest.raises(CredentialLoadError) as excinfo:
        load_credentials(REFS)

    assert "empty" in str(excinfo.value)


def test_valid_credentials_load_and_are_opaque(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(SYNTHETIC_PEM)
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(key_file))

    credentials = load_credentials(REFS)

    assert isinstance(credentials, LoadedDemoCredentials)
    assert repr(credentials) == "LoadedDemoCredentials(<redacted>)"
    assert str(credentials) == "LoadedDemoCredentials(<redacted>)"
    assert SYNTHETIC_ACCESS_KEY not in repr(credentials)
    assert SYNTHETIC_PEM.decode() not in repr(credentials)


def test_loaded_demo_credentials_has_no_public_raw_key_accessor() -> None:
    public_attrs = {name for name in dir(LoadedDemoCredentials) if not name.startswith("_")}

    assert public_attrs == set()
