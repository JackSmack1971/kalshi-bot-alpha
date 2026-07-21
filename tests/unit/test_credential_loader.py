"""Tests for kalshi_bot.credentials.loader (Phase 1 PR 2).

Portable across platforms: permission failures are mocked rather than
relying on POSIX file modes, so these tests behave identically on
Windows and POSIX.
"""

from __future__ import annotations

import pickle
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest

from kalshi_bot.config.models import CredentialReferences
from kalshi_bot.credentials.loader import (
    CredentialLoadError,
    LoadedDemoCredentials,
    _reveal_for_signer_construction,
    load_credentials,
)
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests

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


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


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


def _load_valid_credentials(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> LoadedDemoCredentials:
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(SYNTHETIC_PEM)
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(key_file))
    return load_credentials(REFS)


def test_loaded_demo_credentials_has_no_dict_and_cannot_be_vars_inspected(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    credentials = _load_valid_credentials(monkeypatch, tmp_path)

    with pytest.raises(TypeError):
        vars(credentials)


def test_loaded_demo_credentials_is_not_iterable(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    credentials = _load_valid_credentials(monkeypatch, tmp_path)

    with pytest.raises(TypeError):
        iter(credentials)  # type: ignore[call-overload]


def test_loaded_demo_credentials_cannot_be_pickled(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    credentials = _load_valid_credentials(monkeypatch, tmp_path)

    with pytest.raises(TypeError):
        pickle.dumps(credentials)


def test_loaded_demo_credentials_is_not_json_serializable(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import json

    credentials = _load_valid_credentials(monkeypatch, tmp_path)

    with pytest.raises(TypeError):
        json.dumps(credentials)


def test_access_key_id_is_registered_for_redaction(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    import io

    from kalshi_bot.observability import configure_logging, get_logger

    _load_valid_credentials(monkeypatch, tmp_path)

    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    get_logger("test.credentials.registered").info(f"using key {SYNTHETIC_ACCESS_KEY}")

    rendered = stream.getvalue()
    assert SYNTHETIC_ACCESS_KEY not in rendered


def test_reveal_for_signer_construction_hands_raw_material_only_to_factory(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Proves the PR 3 seam works as intended: a factory receives the
    raw access-key ID and PEM bytes and must transform them into a
    result object (in PR 3, a RequestSigner) -- this is the sole
    sanctioned path to the material, reserved for
    kalshi_bot.auth.signer."""
    credentials = _load_valid_credentials(monkeypatch, tmp_path)

    captured: dict[str, object] = {}

    def factory(access_key_id: str, private_key_pem: bytes) -> str:
        captured["access_key_id"] = access_key_id
        captured["private_key_pem"] = private_key_pem
        return "signer-placeholder"

    result = _reveal_for_signer_construction(credentials, factory)

    assert result == "signer-placeholder"
    assert captured["access_key_id"] == SYNTHETIC_ACCESS_KEY
    assert captured["private_key_pem"] == SYNTHETIC_PEM


def test_reveal_for_signer_construction_is_not_imported_outside_credential_boundary() -> None:
    """Static check: _reveal_for_signer_construction is a convention- and
    review-enforced seam, not a language-level boundary (see its
    docstring) -- so this test is the actual enforcement mechanism.
    Only kalshi_bot.credentials (and, once PR 3 adds it,
    kalshi_bot.auth.signer) may reference the name; REST, WebSocket, and
    every other module must depend on the eventual RequestSigner
    instead."""
    src_root = Path(__file__).resolve().parents[2] / "src" / "kalshi_bot"
    allowed_roots = {"credentials", "auth"}
    violations: list[str] = []

    for path in src_root.rglob("*.py"):
        relative = path.relative_to(src_root)
        top = relative.parts[0] if len(relative.parts) > 1 else None
        if top in allowed_roots:
            continue
        if "_reveal_for_signer_construction" in path.read_text(encoding="utf-8"):
            violations.append(str(relative).replace("\\", "/"))

    assert violations == [], (
        "Only kalshi_bot.credentials/auth may reference "
        "_reveal_for_signer_construction; found in: " + ", ".join(violations)
    )
