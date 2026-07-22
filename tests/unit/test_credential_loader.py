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

from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config.models import CredentialReferences
from kalshi_bot.credentials.loader import (
    CredentialLoadError,
    LoadedDemoCredentials,
    _build_request_signer,
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


def _generate_rsa_pem(key_size: int = 2048) -> bytes:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa

    key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def test_build_request_signer_returns_only_a_request_signer(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Proves the final PR 3 boundary: the only conversion out of
    LoadedDemoCredentials produces a RequestSigner -- never the raw
    access-key ID, PEM bytes, a tuple, or any other raw-material
    container. There is no callback/factory parameter anywhere in this
    path, since a caller-supplied callback would be a wider surface
    than this fixed, one-shot construction."""
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(_generate_rsa_pem())
    monkeypatch.setenv(ACCESS_KEY_ENV, SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv(PRIVATE_KEY_PATH_ENV, str(key_file))
    credentials = load_credentials(REFS)

    result = _build_request_signer(credentials)

    assert isinstance(result, RequestSigner)
    assert not isinstance(result, tuple)


def test_generic_callback_seam_no_longer_exists() -> None:
    """The PR 2 generic callback (_reveal_for_signer_construction) and
    the PR 3-interim raw-tuple seam (_reveal_for_request_signer) must
    not exist anywhere in this module -- only _build_request_signer,
    which returns a RequestSigner, may remain."""
    import kalshi_bot.credentials.loader as loader_module

    assert not hasattr(loader_module, "_reveal_for_signer_construction")
    assert not hasattr(loader_module, "_reveal_for_request_signer")


def test_no_reveal_unwrap_or_consume_named_function_remains() -> None:
    """No function name containing reveal/unwrap/consume may exist in
    the credentials or auth packages -- the only sanctioned conversion
    is the RequestSigner-returning _build_request_signer /
    _RequestSignerBuilder.from_raw_material pair."""
    import kalshi_bot.auth.signer as signer_module
    import kalshi_bot.credentials.loader as loader_module

    forbidden_substrings = ("reveal", "unwrap", "consume")

    for module in (loader_module, signer_module):
        for name in dir(module):
            lowered = name.lower()
            assert not any(substr in lowered for substr in forbidden_substrings), (
                f"{module.__name__}.{name} contains a forbidden reveal/unwrap/"
                "consume name"
            )


def test_build_request_signer_is_not_imported_outside_credential_boundary() -> None:
    """Static check: _build_request_signer and _RequestSignerBuilder
    are convention- and review-enforced seams, not language-level
    boundaries -- so this test is the actual enforcement mechanism.
    Only kalshi_bot.credentials and kalshi_bot.auth may reference
    either name; REST, WebSocket, market-data, and every other module
    must depend on RequestSigner instead."""
    src_root = Path(__file__).resolve().parents[2] / "src" / "kalshi_bot"
    allowed_roots = {"credentials", "auth"}
    forbidden_names = ("_build_request_signer", "_RequestSignerBuilder")
    violations: list[str] = []

    for path in src_root.rglob("*.py"):
        relative = path.relative_to(src_root)
        top = relative.parts[0] if len(relative.parts) > 1 else None
        if top in allowed_roots:
            continue
        text = path.read_text(encoding="utf-8")
        if any(name in text for name in forbidden_names):
            violations.append(str(relative).replace("\\", "/"))

    assert violations == [], (
        "Only kalshi_bot.credentials/auth may reference "
        "_build_request_signer or _RequestSignerBuilder; found in: "
        + ", ".join(violations)
    )


def test_loaded_demo_credentials_raw_fields_not_reachable_via_public_surface(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Raw access-key and PEM values cannot be obtained through public
    attributes, iteration, tuple conversion, or serialization -- only
    through the fixed _build_request_signer construction path."""
    credentials = _load_valid_credentials(monkeypatch, tmp_path)

    assert not any(not name.startswith("_") for name in dir(credentials))
    with pytest.raises(TypeError):
        tuple(credentials)  # type: ignore[arg-type]
