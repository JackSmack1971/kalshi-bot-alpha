"""Property tests for kalshi_bot.auth.signer (Phase 1 PR 3).

RSA-PSS signatures are randomized (a fresh salt per signature), so no
property here ever asserts byte-for-byte equality between two
signatures of the same input -- only that verification succeeds or
fails as expected. A session-scoped synthetic RSA keypair is reused
across examples rather than generating a fresh 2048-bit key per
example, since key generation dominates test wall-clock time.
"""

from __future__ import annotations

import base64
from collections.abc import Iterator

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from kalshi_bot.auth.signer import RequestSigner, SigningError, _canonical_message
from kalshi_bot.credentials.loader import LoadedDemoCredentials
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests

_VALID_METHODS = st.sampled_from(["GET", "POST", "PUT", "DELETE", "PATCH"])
_VALID_PATH_SEGMENTS = st.lists(
    st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd"), max_codepoint=122), min_size=1, max_size=12),
    min_size=1,
    max_size=5,
)
_VALID_TIMESTAMPS = st.integers(min_value=1, max_value=2**53)


def _valid_path(segments: list[str]) -> str:
    return "/trade-api/v2/" + "/".join(segments)


@pytest.fixture(scope="module")
def _keypair() -> tuple[bytes, rsa.RSAPublicKey]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem, key.public_key()


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


def _verify(public_key: rsa.RSAPublicKey, message: bytes, signature_b64: str) -> None:
    signature_bytes = base64.b64decode(signature_b64, validate=True)
    public_key.verify(
        signature_bytes,
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
        hashes.SHA256(),
    )


@given(method=_VALID_METHODS, segments=_VALID_PATH_SEGMENTS, timestamp_ms=_VALID_TIMESTAMPS)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None, max_examples=50)
def test_round_trip_verification_holds_for_valid_inputs(
    _keypair: tuple[bytes, rsa.RSAPublicKey], method: str, segments: list[str], timestamp_ms: int
) -> None:
    pem, public_key = _keypair
    path = _valid_path(segments)
    signer = RequestSigner.from_credentials(LoadedDemoCredentials("SYNTHETIC-PROPERTY-KEY", pem))

    headers = signer.sign(method, path, timestamp_ms)
    message = _canonical_message(method, path, timestamp_ms)

    _verify(public_key, message, headers.signature)


@given(
    method=_VALID_METHODS,
    segments=_VALID_PATH_SEGMENTS,
    timestamp_ms=_VALID_TIMESTAMPS,
    other_timestamp_delta=st.integers(min_value=1, max_value=10_000),
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None, max_examples=50)
def test_single_field_mutation_fails_cross_verification(
    _keypair: tuple[bytes, rsa.RSAPublicKey],
    method: str,
    segments: list[str],
    timestamp_ms: int,
    other_timestamp_delta: int,
) -> None:
    pem, public_key = _keypair
    path = _valid_path(segments)
    signer = RequestSigner.from_credentials(LoadedDemoCredentials("SYNTHETIC-PROPERTY-KEY", pem))

    headers = signer.sign(method, path, timestamp_ms)

    mutated_timestamp = timestamp_ms + other_timestamp_delta
    mutated_message = _canonical_message(method, path, mutated_timestamp)

    with pytest.raises(InvalidSignature):
        _verify(public_key, mutated_message, headers.signature)


def test_two_signatures_of_identical_input_are_not_asserted_byte_equal(
    _keypair: tuple[bytes, rsa.RSAPublicKey],
) -> None:
    """Documents the deliberate absence of a byte-equality property:
    RSA-PSS salts are random, so signing the same input twice produces
    two different (both individually valid) signatures."""
    pem, public_key = _keypair
    signer = RequestSigner.from_credentials(LoadedDemoCredentials("SYNTHETIC-PROPERTY-KEY", pem))

    method, path, timestamp_ms = "GET", "/trade-api/v2/markets", 1_000_000
    first = signer.sign(method, path, timestamp_ms)
    second = signer.sign(method, path, timestamp_ms)

    message = _canonical_message(method, path, timestamp_ms)
    _verify(public_key, message, first.signature)
    _verify(public_key, message, second.signature)
    # No assertion that first.signature == second.signature -- they are
    # expected to differ given RSA-PSS's random salt.


@given(
    invalid_timestamp=st.one_of(
        st.integers(max_value=0),
        st.booleans(),
        st.text(),
        st.floats(allow_nan=False, allow_infinity=False),
    )
)
@settings(deadline=None, max_examples=50)
def test_invalid_timestamps_are_rejected(invalid_timestamp: object) -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", "/trade-api/v2/markets", invalid_timestamp)  # type: ignore[arg-type]


@given(
    invalid_method=st.one_of(
        st.just(""),
        st.text(
            alphabet=st.characters(whitelist_categories=("Ll",)),  # type: ignore[arg-type]
            min_size=1,
            max_size=8,
        ),
        st.just("Get"),
        st.just("GET "),
    )
)
@settings(deadline=None, max_examples=50)
def test_invalid_methods_are_rejected(invalid_method: str) -> None:
    with pytest.raises(SigningError):
        _canonical_message(invalid_method, "/trade-api/v2/markets", 1000)


@given(
    invalid_path=st.one_of(
        st.just(""),
        st.just("trade-api/v2/markets"),
        st.just("http://external-api.demo.kalshi.co/trade-api/v2/markets"),
        st.just("//external-api.demo.kalshi.co/trade-api/v2/markets"),
        st.just("/trade-api/v2/markets#fragment"),
    )
)
@settings(deadline=None, max_examples=50)
def test_invalid_paths_are_rejected(invalid_path: str) -> None:
    with pytest.raises(SigningError):
        _canonical_message("GET", invalid_path, 1000)
