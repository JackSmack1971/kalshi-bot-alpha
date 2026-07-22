"""Tests for kalshi_bot.rest.client.KalshiDemoRestClient (Phase 1 PR 4).

No network, filesystem, or real credential material anywhere in this
file. Uses a duck-typed fake signer (records every ``sign()`` call) and
``httpx.MockTransport``/a small scripted fake transport so retries,
backoff, and pagination are deterministic and never sleep in real wall
time.
"""

from __future__ import annotations

import io
import json
from collections.abc import Iterator

import httpx
import pytest

from kalshi_bot.auth.signer import SignedHeaders
from kalshi_bot.config.models import AppConfig, CredentialReferences
from kalshi_bot.observability import configure_logging, get_logger
from kalshi_bot.observability.logging import _reset_registered_sensitive_values_for_tests
from kalshi_bot.rest import client as rest_client_module
from kalshi_bot.rest.client import KalshiDemoRestClient
from kalshi_bot.rest.errors import (
    KalshiApiError,
    KalshiAuthError,
    PaginationError,
    ResponseDecodeError,
    ResponseValidationError,
    TransportExhaustedError,
)

FAKE_ACCESS_KEY = "FAKE-ACCESS-KEY-FOR-REST-CLIENT-TESTS"
FAKE_SIGNATURE = "FAKE-SIGNATURE-FOR-REST-CLIENT-TESTS"


@pytest.fixture(autouse=True)
def _reset_registry() -> Iterator[None]:
    _reset_registered_sensitive_values_for_tests()
    yield
    _reset_registered_sensitive_values_for_tests()


class _FakeSigner:
    """Duck-typed stand-in for RequestSigner; no real key material.

    Records every ``sign()`` call so tests can assert the exact
    ``(method, path, timestamp_ms)`` handed to the signer -- in
    particular, that ``path`` never carries a query string.
    """

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, int]] = []

    def sign(self, method: str, path: str, timestamp_ms: int) -> SignedHeaders:
        self.calls.append((method, path, timestamp_ms))
        return SignedHeaders(
            access_key=FAKE_ACCESS_KEY, signature=FAKE_SIGNATURE, timestamp_ms=timestamp_ms
        )


class _FakeClock:
    def __init__(self, start: int = 1_700_000_000_000) -> None:
        self._value = start

    def __call__(self) -> int:
        self._value += 1
        return self._value


class _RecordingSleeper:
    def __init__(self) -> None:
        self.calls: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


class _ScriptedTransport(httpx.BaseTransport):
    """Replays a fixed sequence of responses/exceptions, one per request.

    Used where ``httpx.MockTransport``'s single-handler-per-request
    model is not expressive enough (e.g. "raise a connect error on the
    first call, then succeed").
    """

    def __init__(self, script: list[Exception | httpx.Response]) -> None:
        self._script = list(script)
        self.requests: list[httpx.Request] = []

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        item = self._script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _make_config(
    *,
    rest_timeout_seconds: float = 5.0,
    rest_max_retries: int = 2,
    rest_retry_backoff_min_seconds: float = 0.01,
    rest_retry_backoff_max_seconds: float = 0.08,
) -> AppConfig:
    return AppConfig(
        rest_timeout_seconds=rest_timeout_seconds,
        rest_max_retries=rest_max_retries,
        rest_retry_backoff_min_seconds=rest_retry_backoff_min_seconds,
        rest_retry_backoff_max_seconds=rest_retry_backoff_max_seconds,
        ws_timeout_seconds=5.0,
        ws_reconnect_backoff_min_seconds=0.01,
        ws_reconnect_backoff_max_seconds=0.08,
        credentials=CredentialReferences(
            access_key_env="TEST_REST_CLIENT_ACCESS_KEY_ENV",
            private_key_path_env="TEST_REST_CLIENT_PRIVATE_KEY_PATH_ENV",
        ),
    )


def _build_client(
    transport: httpx.BaseTransport,
    *,
    config: AppConfig | None = None,
    signer: _FakeSigner | None = None,
    sleeper: _RecordingSleeper | None = None,
    clock: _FakeClock | None = None,
) -> tuple[KalshiDemoRestClient, _FakeSigner, _RecordingSleeper]:
    fake_signer = signer or _FakeSigner()
    fake_sleeper = sleeper or _RecordingSleeper()
    client = KalshiDemoRestClient(
        fake_signer,  # type: ignore[arg-type]
        config or _make_config(),
        clock_ms=clock or _FakeClock(),
        sleeper=fake_sleeper,
        transport=transport,
    )
    return client, fake_signer, fake_sleeper


_EXCHANGE_STATUS_BODY: dict[str, object] = {"exchange_active": True, "trading_active": True}
_EXCHANGE_SCHEDULE_BODY: dict[str, object] = {
    "schedule": {"standard_hours": [], "maintenance_windows": []}
}


def _markets_page(markets: list[dict[str, str]], cursor: str) -> dict[str, object]:
    return {"markets": markets, "cursor": cursor}


# -- Basic successful calls -------------------------------------------------


def test_get_exchange_status_success() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=_EXCHANGE_STATUS_BODY))
    client, _, _ = _build_client(transport)

    status = client.get_exchange_status()

    assert status.exchange_active is True
    assert status.trading_active is True


def test_get_exchange_schedule_success() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json=_EXCHANGE_SCHEDULE_BODY)
    )
    client, _, _ = _build_client(transport)

    schedule = client.get_exchange_schedule()

    assert schedule.standard_hours == []
    assert schedule.maintenance_windows == []


def test_list_markets_single_page_no_cursor() -> None:
    body = _markets_page([{"ticker": "T1"}, {"ticker": "T2"}], "")
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=body))
    client, _, _ = _build_client(transport)

    markets = client.list_markets()

    assert [m.ticker for m in markets] == ["T1", "T2"]
    assert isinstance(markets, tuple)


# -- Signing: exact path, no query string ------------------------------------


def test_signed_path_excludes_query_string_and_uses_get() -> None:
    body = _markets_page([{"ticker": "T1"}], "")
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=body))
    client, signer, _ = _build_client(transport)

    client.list_markets(limit=10, event_ticker="EVT")

    assert len(signer.calls) == 1
    method, path, _timestamp = signer.calls[0]
    assert method == "GET"
    assert path == "/trade-api/v2/markets"
    assert "?" not in path
    assert "limit" not in path


def test_query_params_are_sent_on_the_wire_not_in_signed_path() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json=_markets_page([], ""))

    transport = httpx.MockTransport(handler)
    client, signer, _ = _build_client(transport)

    client.list_markets(limit=10, event_ticker="KXBTC-25JAN01-EVT", status="open")

    assert len(captured) == 1
    request = captured[0]
    assert request.url.params["limit"] == "10"
    assert request.url.params["event_ticker"] == "KXBTC-25JAN01-EVT"
    assert request.url.params["status"] == "open"
    # Signed path never carries the query string.
    assert signer.calls[0][1] == "/trade-api/v2/markets"


def test_request_url_targets_exact_demo_host_and_path() -> None:
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json=_EXCHANGE_STATUS_BODY)

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    client.get_exchange_status()

    assert str(captured[0].url).startswith(
        "https://external-api.demo.kalshi.co/trade-api/v2/exchange/status"
    )


# -- Timeout propagation -----------------------------------------------------


def test_rest_timeout_seconds_propagated_to_httpx_client() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=_EXCHANGE_STATUS_BODY))
    config = _make_config(rest_timeout_seconds=17.5)
    client, _, _ = _build_client(transport, config=config)

    timeout = client._client.timeout  # noqa: SLF001 - internal attribute access is intentional here
    assert timeout.connect == 17.5
    assert timeout.read == 17.5


# -- Retry classification: transport-level -----------------------------------


def test_connect_error_then_success_recovers() -> None:
    scripted = _ScriptedTransport(
        [httpx.ConnectError("boom"), httpx.Response(200, json=_EXCHANGE_STATUS_BODY)]
    )
    client, _, sleeper = _build_client(scripted, config=_make_config(rest_max_retries=2))

    status = client.get_exchange_status()

    assert status.exchange_active is True
    assert len(scripted.requests) == 2
    assert len(sleeper.calls) == 1


def test_read_timeout_then_success_recovers() -> None:
    scripted = _ScriptedTransport(
        [
            httpx.ReadTimeout("timed out"),
            httpx.Response(200, json=_EXCHANGE_STATUS_BODY),
        ]
    )
    client, _, sleeper = _build_client(scripted, config=_make_config(rest_max_retries=2))

    status = client.get_exchange_status()

    assert status.exchange_active is True
    assert len(sleeper.calls) == 1


def test_transport_error_retries_exhausted_raises() -> None:
    scripted = _ScriptedTransport(
        [httpx.ConnectError("boom"), httpx.ConnectError("boom"), httpx.ConnectError("boom")]
    )
    client, _, sleeper = _build_client(scripted, config=_make_config(rest_max_retries=2))

    with pytest.raises(TransportExhaustedError):
        client.get_exchange_status()

    assert len(scripted.requests) == 3
    assert len(sleeper.calls) == 2


def test_zero_retries_configured_fails_immediately_without_sleeping() -> None:
    scripted = _ScriptedTransport([httpx.ConnectError("boom")])
    client, _, sleeper = _build_client(scripted, config=_make_config(rest_max_retries=0))

    with pytest.raises(TransportExhaustedError):
        client.get_exchange_status()

    assert len(scripted.requests) == 1
    assert sleeper.calls == []


# -- Retry classification: HTTP status ----------------------------------------


@pytest.mark.parametrize("status_code", [429, 500, 503, 504])
def test_retryable_status_then_success_recovers(status_code: int) -> None:
    scripted = _ScriptedTransport(
        [
            httpx.Response(status_code, json={"error": "transient"}),
            httpx.Response(200, json=_EXCHANGE_STATUS_BODY),
        ]
    )
    client, _, sleeper = _build_client(scripted, config=_make_config(rest_max_retries=2))

    status = client.get_exchange_status()

    assert status.exchange_active is True
    assert len(sleeper.calls) == 1


def test_retryable_status_exhausted_raises_transport_exhausted() -> None:
    scripted = _ScriptedTransport(
        [
            httpx.Response(503, json={"error": "unavailable"}),
            httpx.Response(503, json={"error": "unavailable"}),
        ]
    )
    client, _, sleeper = _build_client(scripted, config=_make_config(rest_max_retries=1))

    with pytest.raises(TransportExhaustedError):
        client.get_exchange_status()

    assert len(sleeper.calls) == 1


@pytest.mark.parametrize("status_code", [401, 403])
def test_auth_status_raises_immediately_and_is_never_retried(status_code: int) -> None:
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        return httpx.Response(status_code, json={"error": "auth"})

    transport = httpx.MockTransport(handler)
    client, _, sleeper = _build_client(transport, config=_make_config(rest_max_retries=3))

    with pytest.raises(KalshiAuthError) as excinfo:
        client.get_exchange_status()

    assert excinfo.value.status_code == status_code
    assert call_count == 1
    assert sleeper.calls == []


@pytest.mark.parametrize("status_code", [400, 404, 418, 422])
def test_other_client_error_status_raises_immediately_and_is_never_retried(
    status_code: int,
) -> None:
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        return httpx.Response(status_code, json={"error": "bad request"})

    transport = httpx.MockTransport(handler)
    client, _, sleeper = _build_client(transport, config=_make_config(rest_max_retries=3))

    with pytest.raises(KalshiApiError) as excinfo:
        client.get_exchange_status()

    assert excinfo.value.status_code == status_code
    assert call_count == 1
    assert sleeper.calls == []


# -- Backoff math: bounded exponential ----------------------------------------


def test_backoff_is_bounded_exponential_and_capped() -> None:
    responses: list[Exception | httpx.Response] = [
        httpx.Response(503, json={"error": "unavailable"}) for _ in range(5)
    ]
    responses.append(httpx.Response(200, json=_EXCHANGE_STATUS_BODY))
    scripted = _ScriptedTransport(responses)
    config = _make_config(
        rest_max_retries=5,
        rest_retry_backoff_min_seconds=0.01,
        rest_retry_backoff_max_seconds=0.08,
    )
    client, _, sleeper = _build_client(scripted, config=config)

    client.get_exchange_status()

    # attempt 1 -> 0.01, 2 -> 0.02, 3 -> 0.04, 4 -> 0.08 (capped), 5 -> 0.08 (capped)
    assert sleeper.calls == pytest.approx([0.01, 0.02, 0.04, 0.08, 0.08])


# -- JSON decode / schema validation failures ---------------------------------


def test_invalid_json_body_raises_response_decode_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not json at all {{{")

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(ResponseDecodeError):
        client.get_exchange_status()


def test_non_object_json_body_raises_response_decode_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=json.dumps([1, 2, 3]).encode("utf-8"))

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(ResponseDecodeError):
        client.get_exchange_status()


def test_missing_required_field_raises_response_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"exchange_active": True})  # missing trading_active

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(ResponseValidationError):
        client.get_exchange_status()


def test_wrong_typed_required_field_raises_response_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, json={"exchange_active": "true", "trading_active": True}
        )

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(ResponseValidationError):
        client.get_exchange_status()


def test_unknown_response_field_is_tolerated() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "exchange_active": True,
                "trading_active": True,
                "a_brand_new_field_kalshi_added": "surprise",
            },
        )

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    status = client.get_exchange_status()
    assert status.exchange_active is True


# -- Pagination ---------------------------------------------------------------


def test_list_markets_multi_page_preserves_order() -> None:
    pages = [
        _markets_page([{"ticker": "T1"}, {"ticker": "T2"}], "cursor-1"),
        _markets_page([{"ticker": "T3"}], ""),
    ]
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        body = pages[call_count]
        call_count += 1
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    markets = client.list_markets()

    assert [m.ticker for m in markets] == ["T1", "T2", "T3"]
    assert call_count == 2


def test_list_markets_second_page_request_carries_returned_cursor() -> None:
    pages = [
        _markets_page([{"ticker": "T1"}], "cursor-1"),
        _markets_page([{"ticker": "T2"}], ""),
    ]
    call_count = 0
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        captured.append(request)
        body = pages[call_count]
        call_count += 1
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    client.list_markets()

    assert "cursor" not in captured[0].url.params
    assert captured[1].url.params["cursor"] == "cursor-1"


def test_list_markets_repeated_cursor_raises_pagination_error_no_partial_result() -> None:
    pages = [
        _markets_page([{"ticker": "T1"}], "cursor-1"),
        _markets_page([{"ticker": "T2"}], "cursor-1"),  # repeats the same cursor
    ]
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        body = pages[call_count]
        call_count += 1
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(PaginationError):
        client.list_markets()

    # No caller-visible way to retrieve a partial list: the only
    # outcome of this call is the raised exception above.


def test_list_markets_duplicate_ticker_across_pages_raises_pagination_error() -> None:
    pages = [
        _markets_page([{"ticker": "T1"}], "cursor-1"),
        _markets_page([{"ticker": "T1"}], ""),  # duplicate ticker
    ]
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        body = pages[call_count]
        call_count += 1
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(PaginationError):
        client.list_markets()


def test_list_markets_duplicate_ticker_within_same_page_raises_pagination_error() -> None:
    body = _markets_page([{"ticker": "T1"}, {"ticker": "T1"}], "")
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=body))
    client, _, _ = _build_client(transport)

    with pytest.raises(PaginationError):
        client.list_markets()


def test_list_markets_exceeding_max_pages_raises_pagination_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(rest_client_module, "_MAX_MARKET_LIST_PAGES", 2)

    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        call_count += 1
        # Always returns a fresh, never-empty, never-repeated cursor so
        # pagination would otherwise continue forever.
        return httpx.Response(
            200, json=_markets_page([{"ticker": f"T{call_count}"}], f"cursor-{call_count}")
        )

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(PaginationError):
        client.list_markets()

    assert call_count == 2  # stopped exactly at the ceiling, no unbounded loop


def test_list_markets_malformed_cursor_raises_response_validation_error() -> None:
    """A non-string cursor in the decoded body is this client's
    definition of "malformed cursor" -- rejected at schema validation,
    before pagination reasoning ever inspects it."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"markets": [], "cursor": 12345})

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    with pytest.raises(ResponseValidationError):
        client.list_markets()


def test_list_markets_pagination_failure_raises_before_second_page_used(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Proves a page-2 pagination-invariant failure never lets any
    caller observe page 1's items: the only way to reach them is
    through this call's return value, and it never returns one."""
    pages = [
        _markets_page([{"ticker": "T1"}], "cursor-1"),
        _markets_page([{"ticker": "T1"}], ""),  # duplicate of page 1's ticker
    ]
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        body = pages[call_count]
        call_count += 1
        return httpx.Response(200, json=body)

    transport = httpx.MockTransport(handler)
    client, _, _ = _build_client(transport)

    result = None
    try:
        result = client.list_markets()
    except PaginationError:
        pass

    assert result is None


# -- Logging: no header/signature leakage, structured fields present ---------


def test_no_secret_leakage_in_logs_and_structured_fields_present() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    logger_name = "test.rest_client.no_leakage"
    # Re-bind the module logger for this call so we can capture its
    # output on our own stream without depending on import order.
    monkey_logger = get_logger(logger_name)
    original_logger = rest_client_module._logger
    rest_client_module._logger = monkey_logger
    try:
        transport = httpx.MockTransport(
            lambda request: httpx.Response(200, json=_EXCHANGE_STATUS_BODY)
        )
        client, _, _ = _build_client(transport)
        client.get_exchange_status()
    finally:
        rest_client_module._logger = original_logger

    rendered = stream.getvalue()
    assert FAKE_ACCESS_KEY not in rendered
    assert FAKE_SIGNATURE not in rendered

    lines = [json.loads(line) for line in rendered.splitlines() if line.strip()]
    success_lines = [line for line in lines if line.get("event") == "rest_request_succeeded"]
    assert success_lines, rendered
    assert success_lines[0]["operation"] == "get_exchange_status"
    assert success_lines[0]["status_code"] == 200
    assert "access_key" not in success_lines[0]
    assert "signature" not in success_lines[0]
    assert "headers" not in success_lines[0]


def test_retry_log_includes_backoff_and_status_but_no_secret() -> None:
    stream = io.StringIO()
    configure_logging(level="INFO", stream=stream)
    monkey_logger = get_logger("test.rest_client.retry_logging")
    original_logger = rest_client_module._logger
    rest_client_module._logger = monkey_logger
    try:
        scripted = _ScriptedTransport(
            [
                httpx.Response(503, json={"error": "unavailable"}),
                httpx.Response(200, json=_EXCHANGE_STATUS_BODY),
            ]
        )
        client, _, _ = _build_client(scripted, config=_make_config(rest_max_retries=2))
        client.get_exchange_status()
    finally:
        rest_client_module._logger = original_logger

    rendered = stream.getvalue()
    assert FAKE_ACCESS_KEY not in rendered
    assert FAKE_SIGNATURE not in rendered

    lines = [json.loads(line) for line in rendered.splitlines() if line.strip()]
    retry_lines = [line for line in lines if line.get("event") == "rest_request_retry"]
    assert retry_lines, rendered
    assert retry_lines[0]["status_code"] == 503
    assert "backoff_seconds" in retry_lines[0]


# -- close()/context manager --------------------------------------------------


def test_close_is_idempotent() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=_EXCHANGE_STATUS_BODY))
    client, _, _ = _build_client(transport)
    client.close()
    client.close()


def test_context_manager_closes_underlying_transport() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=_EXCHANGE_STATUS_BODY))
    fake_signer = _FakeSigner()
    with KalshiDemoRestClient(
        fake_signer,  # type: ignore[arg-type]
        _make_config(),
        clock_ms=_FakeClock(),
        sleeper=_RecordingSleeper(),
        transport=transport,
    ) as client:
        client.get_exchange_status()
    assert client._client.is_closed  # noqa: SLF001 - internal attribute access is intentional here
