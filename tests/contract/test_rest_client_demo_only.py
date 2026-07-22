"""Demo-only transport-authority contract tests for KalshiDemoRestClient.

Proves, executably: the exact demo base URL, the absence of any
host/environment-selector constructor path, fail-closed refusal if
demo-host validation ever fails, the exact read-only operation
allowlist, and the absence of any mutation/generic-request surface.

No network, filesystem, or real credential material anywhere in this
file -- construction only, using a duck-typed fake signer (this file
never exercises real signing, only the client's own policy surface).
"""

from __future__ import annotations

import inspect

import httpx
import pytest

import kalshi_bot.rest.client as rest_client_module
from kalshi_bot.auth.signer import SignedHeaders
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.rest.client import KalshiDemoRestClient, _validate_operation_request
from kalshi_bot.rest.errors import DemoHostValidationError, OperationNotAllowedError


class _FakeSigner:
    """Duck-typed stand-in for RequestSigner; no real key material."""

    def sign(self, method: str, path: str, timestamp_ms: int) -> SignedHeaders:
        return SignedHeaders(
            access_key="FAKE-ACCESS-KEY-FOR-CONTRACT-TESTS",
            signature="FAKE-SIGNATURE-FOR-CONTRACT-TESTS",
            timestamp_ms=timestamp_ms,
        )


def _make_config() -> AppConfig:
    return AppConfig(
        rest_timeout_seconds=5.0,
        rest_max_retries=1,
        rest_retry_backoff_min_seconds=0.01,
        rest_retry_backoff_max_seconds=0.02,
        ws_timeout_seconds=5.0,
        ws_reconnect_backoff_min_seconds=0.01,
        ws_reconnect_backoff_max_seconds=0.02,
        credentials=CredentialReferences(
            access_key_env="TEST_DEMO_ONLY_ACCESS_KEY_ENV",
            private_key_path_env="TEST_DEMO_ONLY_PRIVATE_KEY_PATH_ENV",
        ),
    )


def _build_client() -> KalshiDemoRestClient:
    return KalshiDemoRestClient(
        _FakeSigner(),  # type: ignore[arg-type]
        _make_config(),
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})),
    )


# -- Exact base URL --------------------------------------------------------


def test_base_url_is_exact_demo_host() -> None:
    client = _build_client()
    assert client.base_url == "https://external-api.demo.kalshi.co/trade-api/v2"


# -- No host/environment-selector constructor path ------------------------


def test_constructor_signature_has_no_host_or_environment_parameter() -> None:
    signature = inspect.signature(KalshiDemoRestClient.__init__)
    param_names = set(signature.parameters) - {"self"}
    forbidden = {"host", "base_url", "environment", "production", "url", "endpoint"}
    assert param_names.isdisjoint(forbidden)
    assert param_names == {"signer", "config", "clock_ms", "sleeper", "transport"}


def test_client_refuses_construction_when_demo_host_validation_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(rest_client_module, "validate_host", lambda host: False)
    with pytest.raises(DemoHostValidationError):
        KalshiDemoRestClient(
            _FakeSigner(),  # type: ignore[arg-type]
            _make_config(),
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})),
        )


def test_client_construction_succeeds_when_demo_host_validates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def _recording_validate_host(host: str) -> bool:
        calls.append(host)
        return True

    monkeypatch.setattr(rest_client_module, "validate_host", _recording_validate_host)
    _build_client()
    assert calls == ["external-api.demo.kalshi.co"]


# -- Exact operation allowlist / no generic request escape hatch ----------


def test_public_surface_is_exactly_the_read_only_operations() -> None:
    public_names = {name for name in dir(KalshiDemoRestClient) if not name.startswith("_")}
    assert public_names == {
        "get_exchange_status",
        "get_exchange_schedule",
        "list_markets",
        "close",
        "base_url",
    }


def test_no_generic_request_method_exists() -> None:
    assert not hasattr(KalshiDemoRestClient, "request")


@pytest.mark.parametrize("verb", ["post", "put", "patch", "delete", "head", "options"])
def test_no_mutation_or_other_http_verb_methods_exist(verb: str) -> None:
    assert not hasattr(KalshiDemoRestClient, verb)


def test_no_order_or_portfolio_mutation_method_name_exists() -> None:
    public_names = {name.lower() for name in dir(KalshiDemoRestClient) if not name.startswith("_")}
    forbidden_substrings = ("order", "cancel", "amend", "portfolio", "create", "place")
    for name in public_names:
        for forbidden in forbidden_substrings:
            assert forbidden not in name, f"{name!r} suggests a mutation surface"


def test_operation_paths_are_get_only_and_read_only() -> None:
    assert rest_client_module._ALLOWED_METHOD == "GET"
    for path in rest_client_module._OPERATION_PATHS.values():
        assert path.startswith("/trade-api/v2")
        assert "order" not in path
        assert "portfolio" not in path


# -- Internal policy gate: independently testable rejection ---------------


def test_validate_operation_request_accepts_exact_allowlisted_paths() -> None:
    for path in rest_client_module._OPERATION_PATHS.values():
        _validate_operation_request("GET", path)  # must not raise


@pytest.mark.parametrize("method", ["POST", "PUT", "PATCH", "DELETE", "get", "Get"])
def test_validate_operation_request_rejects_non_get_method(method: str) -> None:
    with pytest.raises(OperationNotAllowedError):
        _validate_operation_request(method, "/trade-api/v2/markets")


@pytest.mark.parametrize(
    "path",
    [
        "https://external-api.demo.kalshi.co/trade-api/v2/markets",
        "//external-api.demo.kalshi.co/trade-api/v2/markets",
        "http://evil.example/trade-api/v2/markets",
    ],
)
def test_validate_operation_request_rejects_absolute_urls(path: str) -> None:
    with pytest.raises(OperationNotAllowedError):
        _validate_operation_request("GET", path)


@pytest.mark.parametrize(
    "path",
    [
        "/trade-api/v2/portfolio/orders",
        "/trade-api/v2/portfolio/orders/cancel",
        "/trade-api/v2/markets/KXBTC-25JAN01/orderbook",
        "/trade-api/v2/markets/",
        "/arbitrary/path",
        "",
    ],
)
def test_validate_operation_request_rejects_non_allowlisted_paths(path: str) -> None:
    with pytest.raises(OperationNotAllowedError):
        _validate_operation_request("GET", path)
