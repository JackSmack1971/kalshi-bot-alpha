"""Read-only demo Kalshi REST client (Phase 1 PR 4).

``KalshiDemoRestClient`` exposes exactly three read-only operations --
``GET /exchange/status``, ``GET /exchange/schedule``, ``GET /markets``
(with pagination) -- and nothing else. There is no generic
``request(method, path)`` escape hatch anywhere on this class, no
constructor argument that selects a host/environment, and no code path
that can reach a mutating (``POST``/``PUT``/``PATCH``/``DELETE``) verb
or an order/portfolio-mutation route. See
``.claude/rules/kalshi-transport-safety.md`` for the invariants this
module must never weaken.

**Demo-only authority.** The base URL is derived only from
``kalshi_bot.contracts.demo_endpoints.DEMO_REST_HOST`` and validated via
``validate_host`` at construction time, before any ``httpx.Client`` (and
therefore before any socket) is created. There is no
``environment``/``host``/``base_url`` constructor parameter of any kind.

**Signing.** Every request is signed via an injected
``kalshi_bot.auth.signer.RequestSigner``. This client never reads
``os.environ`` or loads credentials itself. The exact canonical API
path (starting at ``/trade-api/v2/...``, no query string) and the exact
uppercase HTTP method are passed to ``signer.sign()``; query parameters
are attached separately via ``httpx``'s ``params=`` kwarg and are never
appended to the signed path string.

**Retry policy** (grounded in the local docs pack; see
``_RETRYABLE_STATUS_CODES`` below for the exact status-code reasoning):
retries connect failures, timeouts, and a narrow set of transient HTTP
statuses, using bounded exponential backoff between
``AppConfig.rest_retry_backoff_min_seconds`` and
``AppConfig.rest_retry_backoff_max_seconds``. Never retries 401/403,
never retries other 4xx client errors, never retries a JSON-decode or
schema-validation failure, and never implements ``Retry-After`` header
handling (deliberate: see the docstring on ``_RETRYABLE_STATUS_CODES``).

**Logging.** Uses only ``kalshi_bot.observability.logging.get_logger``.
Every log call here uses structured, non-secret keyword fields
(operation name, attempt number, status code, retry/backoff decision,
page number, item count) -- never a header dict, a
``SignedHeaders``/credential object, a full URL with its query string,
or a raw response body.
"""

from __future__ import annotations

import enum
import time
from collections.abc import Callable, Mapping
from types import TracebackType
from typing import Any, cast
from decimal import Decimal
from urllib.parse import quote
from uuid import UUID, uuid4

import httpx
from pydantic import ValidationError as PydanticValidationError

from kalshi_bot.auth.signer import RequestSigner
from kalshi_bot.config.models import AppConfig
from kalshi_bot.contracts.demo_endpoints import DEMO_REST_HOST, validate_host
from kalshi_bot.observability.logging import get_logger
from kalshi_bot.rest.errors import (
    DemoHostValidationError,
    KalshiApiError,
    KalshiAuthError,
    OperationNotAllowedError,
    PaginationError,
    RequestValidationError,
    ResponseDecodeError,
    ResponseValidationError,
    TransportExhaustedError,
    TransportFailureError,
    AmbiguousOutcomeError,
    DuplicateSubmissionError,
    PreTransmissionFailure,
)
from kalshi_bot.rest.models import (
    ExchangeSchedule,
    ExchangeStatus,
    MarketListPage,
    MarketSummary,
    _ExchangeScheduleEnvelope,
    Balance,
    Fill,
    FillList,
    Order,
    OrderList,
    Position,
    PositionList,
)

__all__ = ["KalshiDemoRestClient"]

_logger = get_logger(__name__)

_TRADE_API_ROOT = "/trade-api/v2"

#: The only HTTP method this client ever issues. There is no code path
#: -- public or private -- that can substitute a different verb.
_ALLOWED_METHOD = "GET"

class _StoredSide(enum.StrEnum):
    YES = "YES"
    NO = "NO"

#: Hard ceiling on pages fetched by a single ``list_markets`` call, so a
#: misbehaving or malicious server that never returns an empty cursor
#: cannot make this client loop forever. 1000 pages at up to 1000
#: markets/page (the documented per-page maximum) comfortably exceeds
#: any real Kalshi crypto-market catalog while still being a bound, not
#: "effectively unbounded."
_MAX_MARKET_LIST_PAGES = 1000

#: Retryable HTTP statuses, each individually grounded in the local
#: docs pack -- nothing here is guessed:
#:
#: - ``429``: ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-getting-started-rate-limits-ba01b109.md``
#:   states plainly "Apply exponential backoff on 429" and that 429
#:   responses "do not currently include ``Retry-After`` or
#:   ``X-RateLimit-*`` headers" and carry "no penalty or cooldown" --
#:   i.e. the bucket keeps refilling and a subsequent request can
#:   simply succeed once it does. This is explicit grounding to retry
#:   429 using this client's own bounded backoff, and explicit
#:   grounding *not* to implement ``Retry-After`` handling (Kalshi does
#:   not send one on this response).
#: - ``500``, ``503``, ``504``: ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-exchange-get-exchange-status-c8224b5.md``
#:   explicitly documents these three as possible response statuses for
#:   a demo REST GET endpoint. All three read-only operations in this
#:   client share this retry policy since they are all idempotent GET
#:   requests with no side effects to duplicate.
#: - ``502`` is deliberately **not** included: it does not appear
#:   anywhere in the local docs pack for any endpoint this client
#:   calls, and this client does not guess at undocumented transient
#:   statuses.
_RETRYABLE_STATUS_CODES: frozenset[int] = frozenset({429, 500, 503, 504})

#: HTTP statuses that mean "authentication/permission failure," never
#: retried, and raised as the distinct KalshiAuthError type rather than
#: the generic KalshiApiError.
_AUTH_STATUS_CODES: frozenset[int] = frozenset({401, 403})

#: Transport-level exceptions this client retries: connection failures
#: and any timeout (connect/read/write/pool -- httpx.TimeoutException is
#: the shared base for all of them). Deliberately excludes other
#: httpx.TransportError subclasses (e.g. ProtocolError, ProxyError),
#: which more often indicate a client-side bug or environment
#: misconfiguration than a transient network condition. Nothing in the
#: local docs pack justifies retrying them, so ``_execute`` wraps every
#: other ``httpx.TransportError`` subclass in a single non-retried
#: ``TransportFailureError`` instead (see the second ``except`` clause
#: there) rather than letting a raw, unsanitized third-party exception
#: propagate out of this client.
_RETRYABLE_TRANSPORT_EXCEPTIONS: tuple[type[Exception], ...] = (
    httpx.ConnectError,
    httpx.TimeoutException,
)


class _Operation(enum.Enum):
    """The closed set of read-only operations this client can perform.

    Every allowed (method, path) pair is modeled through this enum
    rather than ever being string-built from caller input -- see
    ``_OPERATION_PATHS`` below.
    """

    GET_EXCHANGE_STATUS = "get_exchange_status"
    GET_EXCHANGE_SCHEDULE = "get_exchange_schedule"
    LIST_MARKETS = "list_markets"


#: The exact, fixed canonical API path (starting at ``/trade-api/v2``,
#: no query string) for each allowed operation. This is the single
#: source of truth both for the path handed to
#: ``RequestSigner.sign()`` and for the path suffix appended to the
#: fixed demo host to build the outgoing request URL.
_OPERATION_PATHS: dict[_Operation, str] = {
    _Operation.GET_EXCHANGE_STATUS: f"{_TRADE_API_ROOT}/exchange/status",
    _Operation.GET_EXCHANGE_SCHEDULE: f"{_TRADE_API_ROOT}/exchange/schedule",
    _Operation.LIST_MARKETS: f"{_TRADE_API_ROOT}/markets",
}

_ALLOWED_OPERATION_PATHS: frozenset[str] = frozenset(_OPERATION_PATHS.values())


def _validate_operation_request(method: str, path: str) -> None:
    """Fail-closed policy gate: only the exact allowlisted GET paths pass.

    Called before every transport execution. Every current call site in
    this module can only ever produce one of the three allowlisted
    ``(method, path)`` pairs from ``_OPERATION_PATHS``, so this check is
    defense in depth rather than the only thing standing between a
    caller and a mutating or arbitrary request -- but it is still an
    explicit, independently unit-testable rejection, not merely "we
    never call it," per this PR's binding decisions.
    """
    if method != _ALLOWED_METHOD:
        raise OperationNotAllowedError(
            f"HTTP method {method!r} is not permitted; only {_ALLOWED_METHOD} is allowed"
        )
    if "://" in path or path.startswith("//"):
        raise OperationNotAllowedError("absolute request URLs are not permitted")
    if path not in _ALLOWED_OPERATION_PATHS:
        raise OperationNotAllowedError(
            f"path {path!r} is not one of the allowlisted read-only operations"
        )


#: ``GET /markets``'s documented ``status`` filter enum, per
#: ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-market-get-markets-dde969d3.md``.
#: Matched case-sensitively -- the doc never states this filter is
#: case-insensitive, so a differently-cased caller value is rejected
#: rather than silently normalized.
_VALID_MARKET_STATUS_VALUES: frozenset[str] = frozenset(
    {"unopened", "open", "paused", "closed", "settled"}
)

#: ``GET /markets``'s documented ``limit`` bound is "Required range:
#: ``0 <= x <= 1000``" (default 100). This client deliberately narrows
#: the *lower* bound to 1: a caller-requested ``limit=0`` is a
#: degenerate, zero-result page request that is not a meaningful
#: pagination call for this client, even though the raw doc text
#: technically allows it. This is a disclosed, deliberate
#: stricter-than-documented choice, not an oversight -- see this PR's
#: final report for the explicit callout.
_MIN_LIST_MARKETS_LIMIT = 1
_MAX_LIST_MARKETS_LIMIT = 1000


def _validate_ticker_like_component(value: str, *, field_name: str) -> None:
    """Shared nonempty/no-surrounding-whitespace check for a single
    ticker-shaped string value (``event_ticker``, ``series_ticker``, or
    one comma-separated component of ``tickers``).

    The grounding doc documents no format or maximum-length constraint
    for any of these three parameters beyond "a string" / "comma-
    separated list of market tickers" -- none is invented here.
    """
    if value == "":
        raise RequestValidationError(f"{field_name} must not be an empty string")
    if value != value.strip():
        raise RequestValidationError(
            f"{field_name} must not have leading or trailing whitespace"
        )


def _validate_list_markets_params(
    *,
    limit: int | None,
    event_ticker: str | None,
    series_ticker: str | None,
    status: str | None,
    tickers: str | None,
) -> None:
    """Fail-closed validation gate for every ``list_markets`` query parameter.

    Called at the very start of ``list_markets``, before any clock
    access, signing, signature registration, sleeper use, or transport
    execution -- an invalid parameter never reaches the network. Every
    bound/enum here is grounded in
    ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-market-get-markets-dde969d3.md``
    (see each check's own comment for the specific grounding, including
    the one deliberate, disclosed deviation from the raw documented
    ``limit`` range). No documented mutual-exclusivity or combination
    constraint exists in that doc between any pair of the five
    parameters this client currently exposes (``limit``,
    ``event_ticker``, ``series_ticker``, ``status``, ``tickers``), so
    none is enforced here -- they are passed through independently.
    """
    if limit is not None:
        # isinstance(x, bool) is also isinstance(x, int) in Python;
        # reject bool explicitly so True/False can never silently pass
        # as 1/0.
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise RequestValidationError("limit must be an int, not bool or another type")
        if not (_MIN_LIST_MARKETS_LIMIT <= limit <= _MAX_LIST_MARKETS_LIMIT):
            raise RequestValidationError(
                f"limit must be between {_MIN_LIST_MARKETS_LIMIT} and "
                f"{_MAX_LIST_MARKETS_LIMIT} inclusive"
            )

    if event_ticker is not None:
        if not isinstance(event_ticker, str):
            raise RequestValidationError("event_ticker must be a string")
        _validate_ticker_like_component(event_ticker, field_name="event_ticker")

    if series_ticker is not None:
        if not isinstance(series_ticker, str):
            raise RequestValidationError("series_ticker must be a string")
        _validate_ticker_like_component(series_ticker, field_name="series_ticker")

    if status is not None:
        if not isinstance(status, str) or status not in _VALID_MARKET_STATUS_VALUES:
            raise RequestValidationError(
                f"status must be exactly one of {sorted(_VALID_MARKET_STATUS_VALUES)} "
                "(case-sensitive)"
            )

    if tickers is not None:
        if not isinstance(tickers, str):
            raise RequestValidationError("tickers must be a string")
        if tickers == "":
            raise RequestValidationError("tickers must not be an empty string")
        # A leading/trailing/doubled comma produces an empty component
        # once split, so the per-component nonempty check below also
        # rejects malformed separators (",AAA", "AAA,", "AAA,,BBB")
        # without a separate check.
        for component in tickers.split(","):
            _validate_ticker_like_component(component, field_name="tickers component")


def _sanitize_pydantic_error(exc: PydanticValidationError) -> str:
    """Summarize a pydantic ``ValidationError`` without leaking field values.

    Mirrors ``kalshi_bot.config.loader._sanitize_validation_error``:
    field location, the stable pydantic error-type code, and pydantic's
    fixed message template only -- never the rejected input value,
    which comes from the network and is not controlled by this client.
    """
    parts = []
    for error in exc.errors(include_url=False, include_context=False, include_input=False):
        loc = ".".join(str(segment) for segment in error["loc"]) or "<root>"
        parts.append(f"{loc}: {error['type']} ({error['msg']})")
    return "; ".join(parts)


def _default_clock_ms() -> int:
    """Production millisecond clock. Injected the same way ``_monotonic``
    is indirected in ``kalshi_bot.observability.logging``, so tests never
    depend on wall-clock time."""
    return int(time.time() * 1000)


def _default_sleeper(seconds: float) -> None:
    """Production sleeper. Tests inject a no-op/recording callable instead."""
    time.sleep(seconds)


class KalshiDemoRestClient:
    """Read-only demo Kalshi REST client.

    Construction takes only ``signer`` and ``config`` (plus optional
    test-only injected ``clock_ms``/``sleeper``/``transport``) -- no
    host, base URL, environment, or production-selector argument of any
    kind exists on this constructor. The base URL is derived internally
    from ``kalshi_bot.contracts.demo_endpoints.DEMO_REST_HOST`` and
    validated via ``validate_host`` before any ``httpx.Client`` is
    created; construction raises :class:`~kalshi_bot.rest.errors.DemoHostValidationError`
    rather than proceeding if that check ever fails.

    Public surface is exactly ``get_exchange_status``,
    ``get_exchange_schedule``, ``list_markets``, and ``close`` (plus
    context-manager support). There is no generic ``request(method,
    path)`` method and no method that issues a mutating HTTP verb.
    """

    def __init__(
        self,
        signer: RequestSigner,
        config: AppConfig,
        *,
        clock_ms: Callable[[], int] | None = None,
        sleeper: Callable[[float], None] | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not validate_host(DEMO_REST_HOST):
            # Unreachable in ordinary operation -- see
            # DemoHostValidationError's docstring for why this
            # unconditional check still runs before any I/O.
            raise DemoHostValidationError(
                "the fixed Kalshi demo REST host failed validate_host(); "
                "refusing to construct a transport"
            )

        self._signer = signer
        self._config = config
        self._clock_ms = clock_ms if clock_ms is not None else _default_clock_ms
        self._sleeper = sleeper if sleeper is not None else _default_sleeper
        self._base_url = f"https://{DEMO_REST_HOST}{_TRADE_API_ROOT}"

        # follow_redirects is left at httpx's default of False: this
        # client never wants a redirect response to silently move a
        # request to a different host or path than the one it signed
        # and validated.
        #
        # trust_env=False: httpx.Client defaults to trust_env=True,
        # which reads HTTP_PROXY/HTTPS_PROXY/ALL_PROXY, NO_PROXY, and
        # CA-bundle environment variables and can silently route this
        # client's requests -- including its signed Kalshi auth headers
        # -- through infrastructure selected by the process environment
        # rather than directly to the fixed demo host. That contradicts
        # the demo-only transport boundary even though the URL string
        # itself is still the allowlisted host, so environment trust is
        # disabled unconditionally; this client never reads proxy or CA
        # configuration from the environment.
        self._client = httpx.Client(
            timeout=config.rest_timeout_seconds,
            transport=transport,
            trust_env=False,
        )

    @property
    def base_url(self) -> str:
        """The fixed demo REST base URL this client is permanently bound to."""
        return self._base_url

    def close(self) -> None:
        """Close the underlying transport. Idempotent."""
        self._client.close()

    def __enter__(self) -> KalshiDemoRestClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    # -- Public read-only operations -----------------------------------

    def get_exchange_status(self) -> ExchangeStatus:
        """``GET /exchange/status`` -> :class:`~kalshi_bot.rest.models.ExchangeStatus`."""
        body = self._execute(_Operation.GET_EXCHANGE_STATUS)
        try:
            return ExchangeStatus.model_validate(body)
        except PydanticValidationError as exc:
            raise ResponseValidationError(
                f"get_exchange_status: response failed schema validation: "
                f"{_sanitize_pydantic_error(exc)}"
            ) from None

    def get_exchange_schedule(self) -> ExchangeSchedule:
        """``GET /exchange/schedule`` -> :class:`~kalshi_bot.rest.models.ExchangeSchedule`.

        Returns the unwrapped ``schedule`` object, not the top-level
        ``{"schedule": {...}}`` envelope Kalshi returns.
        """
        body = self._execute(_Operation.GET_EXCHANGE_SCHEDULE)
        try:
            envelope = _ExchangeScheduleEnvelope.model_validate(body)
        except PydanticValidationError as exc:
            raise ResponseValidationError(
                f"get_exchange_schedule: response failed schema validation: "
                f"{_sanitize_pydantic_error(exc)}"
            ) from None
        return envelope.schedule

    def list_markets(
        self,
        *,
        limit: int | None = None,
        event_ticker: str | None = None,
        series_ticker: str | None = None,
        status: str | None = None,
        tickers: str | None = None,
    ) -> tuple[MarketSummary, ...]:
        """``GET /markets``, fully paginated -> an ordered tuple of :class:`~kalshi_bot.rest.models.MarketSummary`.

        Every parameter is validated by ``_validate_list_markets_params``
        before anything else in this method runs -- before building any
        query dict, before the pagination loop, and therefore before any
        clock access, signing, signature registration, sleeper use, or
        transport execution. An invalid parameter raises
        :class:`~kalshi_bot.rest.errors.RequestValidationError` and
        never reaches the network. See that function's docstring for
        the exact per-parameter rules and their doc grounding.

        Pagination invariants (all fail closed -- never a silently
        truncated/partial result):

        - The opaque ``cursor`` is only ever compared for equality and
          passed back verbatim; its contents are never parsed or
          interpreted.
        - ``cursor`` is tri-state: a nonempty string means "there is a
          next page"; ``""`` (empty string) and ``None`` (JSON ``null``
          or the key absent entirely) both mean "this was the last
          page." Pagination stops as soon as either terminal form is
          seen. Only ever-seen nonempty string cursors are added to the
          repeated-cursor-detection set below -- ``None`` is never
          added to (or checked against) that set, since every terminal
          page's cursor is expected to differ in kind (or be entirely
          absent) from a real pagination cursor.
        - A nonempty ``cursor`` value equal to one already seen on an
          earlier page raises
          :class:`~kalshi_bot.rest.errors.PaginationError` (the server
          is not making forward progress).
        - Fetching more than ``_MAX_MARKET_LIST_PAGES`` pages raises
          :class:`~kalshi_bot.rest.errors.PaginationError` rather than
          looping unboundedly.
        - A market ``ticker`` seen on more than one page raises
          :class:`~kalshi_bot.rest.errors.PaginationError`.
        - A cursor value that is neither a string nor ``null``/absent in
          a decoded response body is rejected by
          :class:`~kalshi_bot.rest.models.MarketListPage`'s
          ``strict=True`` validation before any of the above pagination
          logic runs, surfacing as
          :class:`~kalshi_bot.rest.errors.ResponseValidationError`.

        Item order is deterministic: page order, then in-page order.
        ``limit``/``event_ticker``/``series_ticker``/``status``/``tickers``
        map directly to the documented ``GET /markets`` query
        parameters and are sent via ``httpx``'s ``params=`` kwarg, never
        appended to the signed path.
        """
        _validate_list_markets_params(
            limit=limit,
            event_ticker=event_ticker,
            series_ticker=series_ticker,
            status=status,
            tickers=tickers,
        )

        base_params: dict[str, Any] = {}
        if limit is not None:
            base_params["limit"] = limit
        if event_ticker is not None:
            base_params["event_ticker"] = event_ticker
        if series_ticker is not None:
            base_params["series_ticker"] = series_ticker
        if status is not None:
            base_params["status"] = status
        if tickers is not None:
            base_params["tickers"] = tickers

        collected: list[MarketSummary] = []
        seen_tickers: set[str] = set()
        seen_cursors: set[str] = set()
        cursor: str | None = None
        page_number = 0

        while True:
            page_number += 1
            if page_number > _MAX_MARKET_LIST_PAGES:
                raise PaginationError(
                    f"list_markets: exceeded maximum page count "
                    f"({_MAX_MARKET_LIST_PAGES})"
                )

            page_params = dict(base_params)
            if cursor:
                page_params["cursor"] = cursor

            body = self._execute(_Operation.LIST_MARKETS, params=page_params)
            try:
                page = MarketListPage.model_validate(body)
            except PydanticValidationError as exc:
                raise ResponseValidationError(
                    f"list_markets: page {page_number} failed schema validation: "
                    f"{_sanitize_pydantic_error(exc)}"
                ) from None

            for market in page.markets:
                if market.ticker in seen_tickers:
                    raise PaginationError(
                        f"list_markets: duplicate market ticker seen across pages "
                        f"(page {page_number})"
                    )
                seen_tickers.add(market.ticker)
                collected.append(market)

            _logger.info(
                "rest_list_markets_page",
                page=page_number,
                item_count=len(page.markets),
                has_next_cursor=bool(page.cursor),
            )

            next_cursor = page.cursor
            if next_cursor is None or next_cursor == "":
                break

            if next_cursor in seen_cursors:
                raise PaginationError(
                    f"list_markets: repeated pagination cursor detected "
                    f"(page {page_number})"
                )
            seen_cursors.add(next_cursor)
            cursor = next_cursor

        _logger.info(
            "rest_list_markets_completed",
            pages=page_number,
            item_count=len(collected),
        )
        return tuple(collected)

    # -- Narrow order/portfolio lifecycle --------------------------------

    def create_limit_order(
        self,
        *,
        ticker: str,
        client_order_id: str | UUID,
        side: str,
        count: int,
        price: Decimal | str | int,
        store: Any,
        intent_id: str | None = None,
        feature_snapshot_id: str | None = None,
        risk_decision_id: str | None = None,
        time_in_force: str = "good_till_canceled",
    ) -> Order:
        """Create exactly one demo, limit, post-only order.

        A local order and its ``SUBMISSION_PENDING`` transition are committed
        before the POST.  Once transmission begins this method never retries;
        uncertain outcomes are persisted as ``OUTCOME_UNKNOWN`` then
        ``RECONCILING`` and raised for the reconciliation owner.
        """
        order_key = str(client_order_id)
        self._validate_order_request(ticker, order_key, side, count, price, time_in_force)
        if store is None or not (intent_id and feature_snapshot_id and risk_decision_id):
            raise PreTransmissionFailure(
                "create_limit_order requires a local store and approved-order provenance"
            )
        existing = store.get_order(order_key)
        if existing is not None:
            raise DuplicateSubmissionError("client_order_id already has a local submission")
        price_d = Decimal(str(price))
        try:
            store.record_order(
                order_key, intent_id, feature_snapshot_id, risk_decision_id,
                ticker, self._side(side), count, price_d, "SUBMISSION_PENDING",
            )
            store.record_transition(
                str(uuid4()), order_key, None, "SUBMISSION_PENDING", "local-before-transmission"
            )
        except Exception as exc:
            raise PreTransmissionFailure("local submission could not be persisted") from exc

        payload = {
            "ticker": ticker, "client_order_id": order_key, "side": side.lower(),
            "count": str(count), "price": format(price_d, "f"),
            "time_in_force": time_in_force,
            "self_trade_prevention_type": "taker_at_cross", "post_only": True,
        }
        try:
            body = self._execute_lifecycle("POST", f"{_TRADE_API_ROOT}/portfolio/orders", json_body=payload)
            result = Order.model_validate(body.get("order", body))
            if result.order_id is None or result.client_order_id != order_key:
                raise ValueError("acknowledgement did not identify the submitted order")
        except (KalshiApiError, KalshiAuthError):
            store.transition_order(order_key, "SUBMISSION_PENDING", "REJECTED", "exchange-definitive-response")
            raise
        except PreTransmissionFailure:
            raise
        except Exception as exc:
            self._mark_unknown(store, order_key)
            raise AmbiguousOutcomeError("create_limit_order acknowledgement is uncertain") from exc
        try:
            store.transition_order(order_key, "SUBMISSION_PENDING", "ACKNOWLEDGED", "exchange-acknowledgement")
        except Exception as exc:
            self._mark_unknown(store, order_key)
            raise AmbiguousOutcomeError("local acknowledgement persistence is uncertain") from exc
        return result

    def cancel_order(self, *, order_id: str) -> Order:
        self._validate_path_id(order_id)
        body = self._execute_lifecycle("DELETE", f"{_TRADE_API_ROOT}/portfolio/orders/{quote(order_id, safe='')}")
        return Order.model_validate(body.get("order", body))

    def get_order(self, *, order_id: str) -> Order:
        self._validate_path_id(order_id)
        body = self._execute_lifecycle("GET", f"{_TRADE_API_ROOT}/portfolio/orders/{quote(order_id, safe='')}")
        return Order.model_validate(body.get("order", body))

    def list_open_orders(self) -> tuple[Order, ...]:
        body = self._execute_lifecycle("GET", f"{_TRADE_API_ROOT}/portfolio/orders", params={"status": "resting"})
        return tuple(OrderList.model_validate(body).orders)

    def get_fills(self) -> tuple[Fill, ...]:
        return tuple(FillList.model_validate(self._execute_lifecycle("GET", f"{_TRADE_API_ROOT}/portfolio/fills")).fills)

    def get_positions(self) -> tuple[Position, ...]:
        return tuple(PositionList.model_validate(self._execute_lifecycle("GET", f"{_TRADE_API_ROOT}/portfolio/positions")).market_positions)

    def get_balance(self) -> Balance:
        return Balance.model_validate(self._execute_lifecycle("GET", f"{_TRADE_API_ROOT}/portfolio/balance"))

    @staticmethod
    def _side(value: str) -> _StoredSide:
        if not isinstance(value, str):
            raise PreTransmissionFailure("side must be bid or ask") from None
        if value.lower() == "bid":
            return _StoredSide.YES
        if value.lower() == "ask":
            return _StoredSide.NO
        raise PreTransmissionFailure("side must be bid or ask") from None

    @staticmethod
    def _validate_path_id(value: str) -> None:
        if not isinstance(value, str) or not value or quote(value, safe="") != value:
            raise PreTransmissionFailure("order_id must be a nonempty path-safe string")

    @classmethod
    def _validate_order_request(cls, ticker: str, order_id: str, side: str, count: int, price: Any, tif: str) -> None:
        if not isinstance(ticker, str) or not ticker or ticker != ticker.strip():
            raise PreTransmissionFailure("ticker is invalid")
        cls._validate_path_id(order_id)
        cls._side(side)
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise PreTransmissionFailure("count must be a positive integer")
        try:
            value = Decimal(price)
        except Exception:
            raise PreTransmissionFailure("price must be a finite Decimal") from None
        if not value.is_finite() or not Decimal("0.01") <= value <= Decimal("0.99"):
            raise PreTransmissionFailure("price must be between 0.01 and 0.99")
        if tif != "good_till_canceled":
            raise PreTransmissionFailure("only good_till_canceled limit orders are supported")

    @staticmethod
    def _mark_unknown(store: Any, order_id: str) -> None:
        store.transition_order(order_id, "SUBMISSION_PENDING", "OUTCOME_UNKNOWN", "post-transmission-uncertain")
        store.transition_order(order_id, "OUTCOME_UNKNOWN", "RECONCILING", "reconciliation-required")

    def _execute_lifecycle(self, method: str, path: str, *, params: Mapping[str, Any] | None = None, json_body: Mapping[str, Any] | None = None) -> dict[str, Any]:
        if not self._is_allowlisted_lifecycle_path(method, path):
            raise PreTransmissionFailure("lifecycle operation is not allowlisted")
        try:
            timestamp_ms = self._clock_ms()
            signed = self._signer.sign(method, path, timestamp_ms)
        except Exception as exc:
            raise PreTransmissionFailure("request could not be prepared before transmission") from exc
        headers = {"KALSHI-ACCESS-KEY": signed.access_key, "KALSHI-ACCESS-SIGNATURE": signed.signature, "KALSHI-ACCESS-TIMESTAMP": str(signed.timestamp_ms)}
        try:
            response = self._client.request(method, f"https://{DEMO_REST_HOST}{path}", params=params, json=json_body, headers=headers)
        except Exception as exc:
            raise AmbiguousOutcomeError("lifecycle request transmission outcome is uncertain") from exc
        if response.status_code in _AUTH_STATUS_CODES:
            raise KalshiAuthError(method.lower(), response.status_code)
        if response.status_code in _RETRYABLE_STATUS_CODES:
            raise AmbiguousOutcomeError("lifecycle response may not reflect the mutation outcome")
        if not (200 <= response.status_code < 300):
            raise KalshiApiError(method.lower(), response.status_code)
        try:
            decoded = response.json()
        except ValueError:
            raise ResponseDecodeError("lifecycle response is not valid JSON") from None
        if not isinstance(decoded, dict):
            raise ResponseDecodeError("lifecycle response is not a JSON object")
        return cast(dict[str, Any], decoded)

    @staticmethod
    def _is_allowlisted_lifecycle_path(method: str, path: str) -> bool:
        fixed = {
            ("POST", f"{_TRADE_API_ROOT}/portfolio/orders"),
            ("GET", f"{_TRADE_API_ROOT}/portfolio/orders"),
            ("GET", f"{_TRADE_API_ROOT}/portfolio/fills"),
            ("GET", f"{_TRADE_API_ROOT}/portfolio/positions"),
            ("GET", f"{_TRADE_API_ROOT}/portfolio/balance"),
        }
        if (method, path) in fixed:
            return True
        return method in {"GET", "DELETE"} and path.startswith(
            f"{_TRADE_API_ROOT}/portfolio/orders/"
        ) and "/" not in path.rsplit("/", 1)[-1]

    # -- Internal request execution --------------------------------------

    def _compute_backoff_seconds(self, attempt: int) -> float:
        """Bounded exponential backoff: ``min_s * 2**(attempt-1)``, capped at ``max_s``."""
        min_s: float = self._config.rest_retry_backoff_min_seconds
        max_s: float = self._config.rest_retry_backoff_max_seconds
        return float(min(max_s, min_s * (2 ** (attempt - 1))))

    def _execute(
        self, operation: _Operation, *, params: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        """Sign, send, retry, and return the decoded JSON body for ``operation``.

        Never returns a partial or best-effort result: any failure
        raises one of the typed errors in ``kalshi_bot.rest.errors``
        instead.
        """
        path = _OPERATION_PATHS[operation]
        _validate_operation_request(_ALLOWED_METHOD, path)
        url = f"https://{DEMO_REST_HOST}{path}"

        max_attempts = self._config.rest_max_retries + 1

        for attempt in range(1, max_attempts + 1):
            timestamp_ms = self._clock_ms()
            signed = self._signer.sign(_ALLOWED_METHOD, path, timestamp_ms)
            request_headers = {
                "KALSHI-ACCESS-KEY": signed.access_key,
                "KALSHI-ACCESS-SIGNATURE": signed.signature,
                "KALSHI-ACCESS-TIMESTAMP": str(signed.timestamp_ms),
            }

            try:
                response = self._client.get(url, params=params, headers=request_headers)
            except _RETRYABLE_TRANSPORT_EXCEPTIONS as exc:
                if attempt < max_attempts:
                    backoff = self._compute_backoff_seconds(attempt)
                    _logger.info(
                        "rest_request_retry",
                        operation=operation.value,
                        attempt=attempt,
                        max_attempts=max_attempts,
                        reason="transport_error",
                        error_type=type(exc).__name__,
                        backoff_seconds=backoff,
                    )
                    self._sleeper(backoff)
                    continue
                _logger.warning(
                    "rest_request_retry_exhausted",
                    operation=operation.value,
                    attempt=attempt,
                    reason="transport_error",
                    error_type=type(exc).__name__,
                )
                raise TransportExhaustedError(
                    f"{operation.value}: transport retries exhausted after "
                    f"{attempt} attempt(s)"
                ) from None
            except httpx.TransportError as exc:
                # Any httpx.TransportError subclass not already matched
                # by _RETRYABLE_TRANSPORT_EXCEPTIONS above (e.g.
                # httpx.ProtocolError, httpx.ProxyError) is treated as
                # non-transient: zero retries, zero sleeps, raised
                # immediately. The message carries only the operation
                # name and the exception's class name -- never
                # str(exc)/repr(exc), which can embed a proxy URL,
                # connection string, or other unsanitized detail.
                _logger.warning(
                    "rest_request_transport_failure",
                    operation=operation.value,
                    attempt=attempt,
                    error_type=type(exc).__name__,
                )
                raise TransportFailureError(
                    f"{operation.value}: non-retryable transport failure "
                    f"({type(exc).__name__})"
                ) from None

            status_code = response.status_code

            if status_code in _RETRYABLE_STATUS_CODES:
                if attempt < max_attempts:
                    backoff = self._compute_backoff_seconds(attempt)
                    _logger.info(
                        "rest_request_retry",
                        operation=operation.value,
                        attempt=attempt,
                        max_attempts=max_attempts,
                        reason="retryable_status",
                        status_code=status_code,
                        backoff_seconds=backoff,
                    )
                    self._sleeper(backoff)
                    continue
                _logger.warning(
                    "rest_request_retry_exhausted",
                    operation=operation.value,
                    attempt=attempt,
                    reason="retryable_status",
                    status_code=status_code,
                )
                raise TransportExhaustedError(
                    f"{operation.value}: retries exhausted after {attempt} attempt(s) "
                    f"(last status {status_code})"
                )

            if status_code in _AUTH_STATUS_CODES:
                _logger.warning(
                    "rest_request_auth_failed",
                    operation=operation.value,
                    attempt=attempt,
                    status_code=status_code,
                )
                raise KalshiAuthError(operation.value, status_code)

            if not (200 <= status_code < 300):
                _logger.warning(
                    "rest_request_failed",
                    operation=operation.value,
                    attempt=attempt,
                    status_code=status_code,
                )
                raise KalshiApiError(operation.value, status_code)

            _logger.info(
                "rest_request_succeeded",
                operation=operation.value,
                attempt=attempt,
                status_code=status_code,
            )
            try:
                decoded: Any = response.json()
            except ValueError:
                raise ResponseDecodeError(
                    f"{operation.value}: response body is not valid JSON"
                ) from None
            if not isinstance(decoded, dict):
                raise ResponseDecodeError(
                    f"{operation.value}: response body is not a JSON object"
                )
            return cast("dict[str, Any]", decoded)

        # Unreachable: the loop above always returns or raises before
        # exhausting its range (max_attempts >= 1, and the final
        # iteration always either returns or raises).
        raise TransportExhaustedError(f"{operation.value}: retries exhausted")
