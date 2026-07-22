"""Mocked end-to-end integration test for KalshiDemoRestClient (Phase 1 PR 4).

Exercises the real ``kalshi_bot.auth.signer.RequestSigner`` (built from
an in-test-generated synthetic RSA keypair, per the pattern in
``tests/unit/test_auth_signer.py``) against ``httpx.MockTransport``, so
this proves genuine end-to-end request signing, retry recovery, full
pagination, and redaction -- with no live network and no live
credentials anywhere in this file.
"""

from __future__ import annotations

import base64
import io
import json
from collections.abc import Iterator

import httpx
import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.credentials.loader import LoadedDemoCredentials
from kalshi_bot.observability import configure_logging, get_logger
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests
from kalshi_bot.rest.client import KalshiDemoRestClient

SYNTHETIC_ACCESS_KEY = "SYNTHETIC-INTEGRATION-ACCESS-KEY-0001"


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


def _generate_signer() -> tuple[RequestSigner, rsa.RSAPublicKey]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    credentials = LoadedDemoCredentials(SYNTHETIC_ACCESS_KEY, pem)
    signer = RequestSigner.from_credentials(credentials)
    return signer, key.public_key()


def _make_config(rest_max_retries: int = 2) -> AppConfig:
    return AppConfig(
        rest_timeout_seconds=5.0,
        rest_max_retries=rest_max_retries,
        rest_retry_backoff_min_seconds=0.001,
        rest_retry_backoff_max_seconds=0.01,
        ws_timeout_seconds=5.0,
        ws_reconnect_backoff_min_seconds=0.001,
        ws_reconnect_backoff_max_seconds=0.01,
        credentials=CredentialReferences(
            access_key_env="TEST_REST_INTEGRATION_ACCESS_KEY_ENV",
            private_key_path_env="TEST_REST_INTEGRATION_PRIVATE_KEY_PATH_ENV",
        ),
    )


def _verify_request_signature(
    request: httpx.Request, public_key: rsa.RSAPublicKey, access_key: str
) -> None:
    assert request.headers["KALSHI-ACCESS-KEY"] == access_key
    timestamp_ms = int(request.headers["KALSHI-ACCESS-TIMESTAMP"])
    signature_b64 = request.headers["KALSHI-ACCESS-SIGNATURE"]
    signature_bytes = base64.b64decode(signature_b64, validate=True)
    message = f"{timestamp_ms}{request.method}{request.url.path}".encode("utf-8")
    public_key.verify(
        signature_bytes,
        message,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH),
        hashes.SHA256(),
    )


def test_real_signer_produces_a_verifiable_signature_on_every_request() -> None:
    signer, public_key = _generate_signer()
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"exchange_active": True, "trading_active": True})

    client = KalshiDemoRestClient(
        signer, _make_config(), transport=httpx.MockTransport(handler)
    )

    status = client.get_exchange_status()

    assert status.exchange_active is True
    assert len(captured) == 1
    _verify_request_signature(captured[0], public_key, SYNTHETIC_ACCESS_KEY)
    assert captured[0].url.path == "/trade-api/v2/exchange/status"


def test_real_signer_end_to_end_paginated_market_discovery() -> None:
    signer, public_key = _generate_signer()
    pages = [
        {"markets": [{"ticker": "KXBTC-A"}, {"ticker": "KXBTC-B"}], "cursor": "page-2-cursor"},
        {"markets": [{"ticker": "KXBTC-C"}], "cursor": ""},
    ]
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        body = pages[len(captured) - 1]
        return httpx.Response(200, json=body)

    client = KalshiDemoRestClient(
        signer, _make_config(), transport=httpx.MockTransport(handler)
    )

    markets = client.list_markets(limit=2)

    assert [m.ticker for m in markets] == ["KXBTC-A", "KXBTC-B", "KXBTC-C"]
    assert len(captured) == 2
    for request in captured:
        _verify_request_signature(request, public_key, SYNTHETIC_ACCESS_KEY)
    assert captured[0].url.params["limit"] == "2"
    assert "cursor" not in captured[0].url.params
    assert captured[1].url.params["cursor"] == "page-2-cursor"


def test_real_signer_end_to_end_retry_then_recover() -> None:
    signer, public_key = _generate_signer()
    responses = [
        httpx.Response(503, json={"error": "unavailable"}),
        httpx.Response(200, json={"schedule": {"standard_hours": [], "maintenance_windows": []}}),
    ]
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return responses[len(captured) - 1]

    client = KalshiDemoRestClient(
        signer, _make_config(rest_max_retries=2), transport=httpx.MockTransport(handler)
    )

    schedule = client.get_exchange_schedule()

    assert schedule.standard_hours == []
    assert len(captured) == 2
    for request in captured:
        _verify_request_signature(request, public_key, SYNTHETIC_ACCESS_KEY)


def test_real_signature_and_access_key_never_leak_into_logs() -> None:
    signer, _public_key = _generate_signer()
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)

    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200, json={"exchange_active": True, "trading_active": True}
        )
    )
    client = KalshiDemoRestClient(signer, _make_config(), transport=transport)

    # Import after configure_logging so this module's own logger picks
    # up the just-configured stream (structlog's stdlib routing reads
    # the root logger's current handlers at call time, but re-binding
    # here keeps this test self-contained and independent of import
    # order across the test session).
    import kalshi_bot.rest.client as rest_client_module

    original_logger = rest_client_module._logger
    rest_client_module._logger = get_logger("test.integration.rest_client_redaction")
    try:
        status = client.get_exchange_status()
    finally:
        rest_client_module._logger = original_logger

    assert status.exchange_active is True

    rendered = stream.getvalue()
    assert SYNTHETIC_ACCESS_KEY not in rendered
    # The real signature is per-request and unpredictable; assert no
    # header/credential-shaped keys leaked into any structured line
    # instead of pinning an exact value.
    lines = [json.loads(line) for line in rendered.splitlines() if line.strip()]
    for line in lines:
        assert "access_key" not in line
        assert "signature" not in line
        assert "authorization" not in line
        assert "headers" not in line
