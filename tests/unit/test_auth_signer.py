"""Tests for kalshi_bot.auth.signer (Phase 1 PR 3).

No network, filesystem, or environment access is used anywhere in this
file; all keypairs are synthetic and generated in-test.
"""

from __future__ import annotations

import base64
import io
import logging
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm

from kalshi_bot.auth.signer import RequestSigner, SignedHeaders, SigningError, _canonical_message
from kalshi_bot.config.models import CredentialReferences
from kalshi_bot.credentials.loader import LoadedDemoCredentials, load_credentials
from kalshi_bot.observability import configure_logging, get_logger
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests

SYNTHETIC_ACCESS_KEY = "SYNTHETIC-SIGNER-ACCESS-KEY-0001"


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


def _generate_rsa_pem(key_size: int = 2048, *, encrypt: bool = False) -> bytes:
    key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    encryption = (
        serialization.BestAvailableEncryption(b"synthetic-test-password")
        if encrypt
        else serialization.NoEncryption()
    )
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )


def _generate_rsa_keypair(key_size: int = 2048) -> tuple[bytes, rsa.RSAPublicKey]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem, key.public_key()


def _credentials(pem: bytes, access_key_id: str = SYNTHETIC_ACCESS_KEY) -> LoadedDemoCredentials:
    return LoadedDemoCredentials(access_key_id, pem)


def _verify(public_key: rsa.RSAPublicKey, message: bytes, signature_b64: str) -> None:
    signature_bytes = base64.b64decode(signature_b64, validate=True)
    public_key.verify(
        signature_bytes,
        message,
        padding.PSS(
            mgf=padding.MGF1(crypto_hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH,
        ),
        crypto_hashes.SHA256(),
    )


# -- Canonical message construction --


def test_canonical_message_exact_bytes() -> None:
    message = _canonical_message("GET", "/trade-api/v2/portfolio/balance", 1703123456789)

    assert message == b"1703123456789GET/trade-api/v2/portfolio/balance"


def test_canonical_message_excludes_query_parameters() -> None:
    with_query = _canonical_message("GET", "/trade-api/v2/portfolio/orders?limit=5", 1000)
    without_query = _canonical_message("GET", "/trade-api/v2/portfolio/orders", 1000)

    assert with_query == without_query


def test_canonical_message_preserves_path_case_and_percent_encoding() -> None:
    message = _canonical_message("GET", "/trade-api/v2/Markets/KXBTC%2D25JAN01", 1000)

    assert message == b"1000GET/trade-api/v2/Markets/KXBTC%2D25JAN01"


def test_canonical_message_preserves_method_case_exactly() -> None:
    # Not silently uppercased -- a lowercase method is rejected, not corrected.
    with pytest.raises(SigningError):
        _canonical_message("get", "/trade-api/v2/markets", 1000)


@pytest.mark.parametrize(
    "path",
    [
        "http://external-api.demo.kalshi.co/trade-api/v2/markets",
        "https://external-api.demo.kalshi.co/trade-api/v2/markets",
        "//external-api.demo.kalshi.co/trade-api/v2/markets",
    ],
)
def test_canonical_message_rejects_absolute_urls(path: str) -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", path, 1000)


def test_canonical_message_rejects_fragment() -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", "/trade-api/v2/markets#section", 1000)


def test_canonical_message_rejects_missing_leading_slash() -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", "trade-api/v2/markets", 1000)


def test_canonical_message_rejects_empty_method() -> None:
    with pytest.raises(SigningError):
        _canonical_message("", "/trade-api/v2/markets", 1000)


def test_canonical_message_rejects_empty_path() -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", "", 1000)


def test_canonical_message_rejects_lowercase_method() -> None:
    with pytest.raises(SigningError):
        _canonical_message("get", "/trade-api/v2/markets", 1000)


def test_canonical_message_rejects_boolean_timestamp() -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", "/trade-api/v2/markets", True)


@pytest.mark.parametrize("timestamp_ms", [0, -1, -1703123456789])
def test_canonical_message_rejects_zero_and_negative_timestamp(timestamp_ms: int) -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", "/trade-api/v2/markets", timestamp_ms)


# -- RequestSigner construction and key validation --


def test_from_credentials_round_trip_verification() -> None:
    pem, public_key = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))

    headers = signer.sign("GET", "/trade-api/v2/portfolio/balance", 1703123456789)

    assert isinstance(headers, SignedHeaders)
    assert headers.access_key == SYNTHETIC_ACCESS_KEY
    assert headers.timestamp_ms == 1703123456789

    message = _canonical_message("GET", "/trade-api/v2/portfolio/balance", 1703123456789)
    _verify(public_key, message, headers.signature)


@pytest.mark.parametrize(
    ("mutate_method", "mutate_path", "mutate_timestamp"),
    [
        (True, False, False),
        (False, True, False),
        (False, False, True),
    ],
)
def test_mutated_method_path_or_timestamp_fails_verification(
    mutate_method: bool, mutate_path: bool, mutate_timestamp: bool
) -> None:
    pem, public_key = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))

    method, path, timestamp_ms = "GET", "/trade-api/v2/portfolio/balance", 1703123456789
    headers = signer.sign(method, path, timestamp_ms)

    if mutate_method:
        method = "POST"
    if mutate_path:
        path = "/trade-api/v2/portfolio/orders"
    if mutate_timestamp:
        timestamp_ms = timestamp_ms + 1

    mutated_message = _canonical_message(method, path, timestamp_ms)

    with pytest.raises(InvalidSignature):
        _verify(public_key, mutated_message, headers.signature)


def test_mutated_key_fails_verification() -> None:
    pem, _ = _generate_rsa_keypair()
    other_pem, other_public_key = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))

    method, path, timestamp_ms = "GET", "/trade-api/v2/portfolio/balance", 1703123456789
    headers = signer.sign(method, path, timestamp_ms)
    message = _canonical_message(method, path, timestamp_ms)

    with pytest.raises(InvalidSignature):
        _verify(other_public_key, message, headers.signature)


def test_mutated_signature_fails_verification() -> None:
    pem, public_key = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))

    method, path, timestamp_ms = "GET", "/trade-api/v2/portfolio/balance", 1703123456789
    headers = signer.sign(method, path, timestamp_ms)
    message = _canonical_message(method, path, timestamp_ms)

    corrupted_bytes = bytearray(base64.b64decode(headers.signature, validate=True))
    corrupted_bytes[0] ^= 0xFF
    corrupted_b64 = base64.b64encode(bytes(corrupted_bytes)).decode("ascii")

    with pytest.raises(InvalidSignature):
        _verify(public_key, message, corrupted_b64)


def test_malformed_pem_raises_sanitized_signing_error() -> None:
    with pytest.raises(SigningError) as excinfo:
        RequestSigner.from_credentials(_credentials(b"not a pem file at all"))

    assert "not a pem file at all" not in str(excinfo.value)


def test_empty_pem_raises_sanitized_signing_error() -> None:
    with pytest.raises(SigningError):
        RequestSigner.from_credentials(_credentials(b""))


def test_encrypted_pem_raises_sanitized_signing_error() -> None:
    encrypted_pem = _generate_rsa_pem(encrypt=True)

    with pytest.raises(SigningError) as excinfo:
        RequestSigner.from_credentials(_credentials(encrypted_pem))

    assert "synthetic-test-password" not in str(excinfo.value)


def test_non_rsa_key_raises_sanitized_signing_error() -> None:
    ec_key = ec.generate_private_key(ec.SECP256R1())
    ec_pem = ec_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with pytest.raises(SigningError):
        RequestSigner.from_credentials(_credentials(ec_pem))


def test_wrong_rsa_key_size_raises_sanitized_signing_error() -> None:
    small_pem = _generate_rsa_pem(key_size=1024)

    with pytest.raises(SigningError):
        RequestSigner.from_credentials(_credentials(small_pem))


def test_signing_error_never_includes_pem_or_access_key() -> None:
    pem = b"garbage-pem-data-that-should-never-appear-in-any-error"

    with pytest.raises(SigningError) as excinfo:
        RequestSigner.from_credentials(_credentials(pem, access_key_id="SYNTHETIC-KEY-XYZ"))

    assert "garbage-pem-data-that-should-never-appear-in-any-error" not in str(excinfo.value)
    assert "SYNTHETIC-KEY-XYZ" not in str(excinfo.value)


# -- Opacity / redaction --


def test_request_signer_has_fixed_redacted_repr_and_str() -> None:
    pem, _ = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))

    assert repr(signer) == "RequestSigner(<redacted>)"
    assert str(signer) == "RequestSigner(<redacted>)"


def test_credentials_repr_stays_redacted_after_signer_construction() -> None:
    pem, _ = _generate_rsa_keypair()
    credentials = _credentials(pem)
    RequestSigner.from_credentials(credentials)

    assert repr(credentials) == "LoadedDemoCredentials(<redacted>)"


def test_signature_is_registered_and_redacted_in_actual_signer_output() -> None:
    pem, _ = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))

    headers = signer.sign("GET", "/trade-api/v2/portfolio/balance", 1703123456789)

    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    get_logger("test.auth.signature_redaction").info(f"signature is {headers.signature}")

    rendered = stream.getvalue()
    assert headers.signature not in rendered
    assert "[REDACTED]" in rendered


def test_access_key_is_redacted_in_actual_signer_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Exercises the real load_credentials -> RequestSigner pipeline: the
    access-key ID is registered at credential-loading time (unchanged
    from PR 2), not re-registered by the signer -- this test proves
    that registration still reaches actual signer output end to end."""
    pem, _ = _generate_rsa_keypair()
    key_file = tmp_path / "key.pem"
    key_file.write_bytes(pem)
    monkeypatch.setenv("TEST_AUTH_SIGNER_ACCESS_KEY", SYNTHETIC_ACCESS_KEY)
    monkeypatch.setenv("TEST_AUTH_SIGNER_PRIVATE_KEY_PATH", str(key_file))

    refs = CredentialReferences(
        access_key_env="TEST_AUTH_SIGNER_ACCESS_KEY",
        private_key_path_env="TEST_AUTH_SIGNER_PRIVATE_KEY_PATH",
    )
    credentials = load_credentials(refs)
    signer = RequestSigner.from_credentials(credentials)

    headers = signer.sign("GET", "/trade-api/v2/portfolio/balance", 1703123456789)

    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    get_logger("test.auth.access_key_redaction").info(f"access key is {headers.access_key}")

    rendered = stream.getvalue()
    assert headers.access_key not in rendered


def _signed_headers() -> SignedHeaders:
    pem, _ = _generate_rsa_keypair()
    signer = RequestSigner.from_credentials(_credentials(pem))
    return signer.sign("GET", "/trade-api/v2/portfolio/balance", 1703123456789)


def test_signed_headers_repr_and_str_are_redacted() -> None:
    headers = _signed_headers()

    assert repr(headers) == "SignedHeaders(<redacted>)"
    assert str(headers) == "SignedHeaders(<redacted>)"
    assert headers.access_key not in repr(headers)
    assert headers.signature not in repr(headers)
    assert headers.access_key not in str(headers)
    assert headers.signature not in str(headers)


def test_signed_headers_fields_remain_accessible() -> None:
    headers = _signed_headers()

    assert headers.access_key == SYNTHETIC_ACCESS_KEY
    assert isinstance(headers.signature, str) and headers.signature
    assert headers.timestamp_ms == 1703123456789


def test_signed_headers_equality_and_immutability() -> None:
    headers = _signed_headers()
    same_values = SignedHeaders(
        access_key=headers.access_key,
        signature=headers.signature,
        timestamp_ms=headers.timestamp_ms,
    )

    assert headers == same_values
    with pytest.raises(AttributeError):
        headers.access_key = "MUTATED"  # type: ignore[misc]


def test_signed_headers_logged_via_structlog_does_not_leak() -> None:
    headers = _signed_headers()

    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    get_logger("test.auth.signed_headers_structlog").info("signed", headers=headers)

    rendered = stream.getvalue()
    assert headers.access_key not in rendered
    assert headers.signature not in rendered
    assert "SignedHeaders(<redacted>)" in rendered


def test_signed_headers_logged_via_stdlib_logging_does_not_leak() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    headers = _signed_headers()

    logging.getLogger("test.auth.signed_headers_stdlib").info("signed headers: %s", headers)

    rendered = stream.getvalue()
    assert headers.access_key not in rendered
    assert headers.signature not in rendered
    assert "SignedHeaders(<redacted>)" in rendered


def test_signed_headers_nested_in_dict_and_list_does_not_leak() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    headers = _signed_headers()

    get_logger("test.auth.signed_headers_nested").info(
        "signed", nested={"headers": headers}, listed=[headers]
    )

    rendered = stream.getvalue()
    assert headers.access_key not in rendered
    assert headers.signature not in rendered
    assert rendered.count("SignedHeaders(<redacted>)") == 2


def test_unsupported_algorithm_raises_sanitized_signing_error() -> None:
    pem, _ = _generate_rsa_keypair()

    with patch(
        "kalshi_bot.auth.signer.serialization.load_pem_private_key",
        side_effect=UnsupportedAlgorithm("unsupported by this OpenSSL build"),
    ):
        with pytest.raises(SigningError) as excinfo:
            RequestSigner.from_credentials(_credentials(pem, access_key_id="SYNTHETIC-KEY-UAE"))

    message = str(excinfo.value)
    assert "unsupported by this OpenSSL build" not in message
    assert "SYNTHETIC-KEY-UAE" not in message
    assert pem.decode("ascii", errors="ignore") not in message


def test_unsupported_algorithm_not_leaked_in_repr_or_logs() -> None:
    pem, _ = _generate_rsa_keypair()

    with patch(
        "kalshi_bot.auth.signer.serialization.load_pem_private_key",
        side_effect=UnsupportedAlgorithm("unsupported by this OpenSSL build"),
    ):
        with pytest.raises(SigningError) as excinfo:
            RequestSigner.from_credentials(_credentials(pem, access_key_id="SYNTHETIC-KEY-UAE"))

    assert "unsupported by this OpenSSL build" not in repr(excinfo.value)

    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    try:
        raise excinfo.value
    except SigningError:
        get_logger("test.auth.unsupported_algorithm").exception("signing failed")

    rendered = stream.getvalue()
    assert "unsupported by this OpenSSL build" not in rendered
