"""External Kalshi REST response models (Phase 1 PR 4).

Grounded in the local official Kalshi documentation:

- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-market-get-markets-dde969d3.md``
- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-exchange-get-exchange-status-c8224b5.md``
- ``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-api-reference-exchange-get-exchange-schedule-284531aa.md``

Every model here is an **external response** model: it describes data
Kalshi's demo API sends to this client, never a caller-supplied request
body (none of the three read-only operations in this PR take one) and
never an authoritative trading type. ``extra="ignore"`` is used
everywhere so that a field Kalshi adds upstream in the future cannot
break this client. Every field this client's *behavior* depends on is
required and strictly typed instead; a missing or wrong-typed required
field fails validation (fail closed) rather than silently defaulting.

Fields are intentionally typed to match the documented JSON shape
exactly (``strict=True``): a JSON string is never silently accepted for
a boolean field, an int is never silently accepted for a string field,
and so on. Kalshi's own examples always send these fields as their
documented JSON types, so this does not reject any conforming response.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "MarketSummary",
    "MarketListPage",
    "ExchangeIndexStatus",
    "ExchangeStatus",
    "DailyOpenClose",
    "StandardHoursBlock",
    "MaintenanceWindow",
    "ExchangeSchedule",
    # "_ExchangeScheduleEnvelope" is deliberately not exported; see its
    # docstring. It is imported directly by kalshi_bot.rest.client only.
]


class _KalshiResponseModel(BaseModel):
    """Base for every external Kalshi response model.

    - ``frozen=True``: a validated response is an immutable snapshot,
      matching this repository's general model-immutability convention
      (see ``kalshi_bot.config.models``).
    - ``extra="ignore"``: Kalshi may add fields upstream; that must
      never break this client.
    - ``strict=True``: reject cross-type coercion (e.g. a numeric
      string silently becoming a bool, or vice versa) instead of
      silently normalizing it.
    - ``populate_by_name=True``: harmless default for models that
      currently have no field aliases, kept for consistency should a
      future field need one (Kalshi field names are already valid
      Python identifiers throughout the fields modeled here).
    """

    model_config = ConfigDict(
        frozen=True, extra="ignore", strict=True, populate_by_name=True
    )


class MarketSummary(_KalshiResponseModel):
    """One market entry from the ``markets`` array of ``GET /markets``.

    Only ``ticker`` is required. The grounding doc's ``Response``
    section marks only the top-level ``markets`` (object[]) and
    ``cursor`` fields as ``required``; it does not mark any individual
    child attribute of a market object as required, so every other
    field here is optional. ``ticker`` is required anyway because this
    client's pagination invariants (duplicate-ticker detection across
    pages) depend on it being present and a string.

    ``status`` is deliberately **omitted** from this model. It is not a
    documented response field anywhere in the local Kalshi docs pack --
    the only occurrence of ``status`` near a market in the grounding
    doc is the *request-side* query filter enum
    (``unopened``/``open``/``paused``/``closed``/``settled``) on
    ``GET /markets``, not a field of the returned market object. A
    corpus-wide grep for ``"status"`` near "market" in
    ``docs-dev/kalshi-docs-pack/docs/`` confirms no response schema
    documents it. Inventing a default or an optional field for it here
    would fabricate response-schema behavior this client cannot verify
    against the grounding docs; per this PR's binding decisions, that
    is not done.

    Field list below preserves data useful for later paper-trading
    research (ticker, event association, title/subtitle, quoted
    prices, volume, open interest, and timestamps) without adding any
    trading-authority behavior: no computed eligibility flag, no
    order-placement helper, and no derived field of any kind.
    """

    ticker: str

    event_ticker: str | None = None
    title: str | None = None
    subtitle: str | None = None
    yes_sub_title: str | None = None
    no_sub_title: str | None = None

    created_time: str | None = None
    updated_time: str | None = None
    open_time: str | None = None
    close_time: str | None = None
    expiration_time: str | None = None
    expected_expiration_time: str | None = None

    yes_bid_dollars: str | None = None
    yes_ask_dollars: str | None = None
    no_bid_dollars: str | None = None
    no_ask_dollars: str | None = None
    last_price_dollars: str | None = None
    previous_price_dollars: str | None = None

    volume_fp: str | None = None
    volume_24h_fp: str | None = None
    open_interest_fp: str | None = None
    liquidity_dollars: str | None = None
    notional_value_dollars: str | None = None

    can_close_early: bool | None = None


class MarketListPage(_KalshiResponseModel):
    """One raw, unvalidated-against-pagination-invariants page of ``GET /markets``.

    Mirrors the documented envelope exactly: ``markets`` (required
    array, possibly empty) and ``cursor`` (required string, possibly
    empty on the last page). This model performs no pagination
    reasoning of its own (no cursor-repetition, page-count, or
    duplicate-ticker checks) -- that invariant enforcement lives in
    :meth:`kalshi_bot.rest.client.KalshiDemoRestClient.list_markets`,
    which validates each page against this model before applying those
    invariants across the whole paginated fetch. A non-string cursor in
    the decoded JSON body (Kalshi's "malformed cursor" case, as this
    client defines it) is rejected right here, at the
    ``strict=True`` type-validation layer, before any pagination logic
    ever runs.
    """

    markets: list[MarketSummary] = Field(default_factory=list)
    cursor: str


class ExchangeIndexStatus(_KalshiResponseModel):
    """One entry of ``exchange_index_statuses`` from ``GET /exchange/status``.

    All four fields are marked required here because they are always
    present together in the grounding doc's single documented example
    of this nested object; the array itself is optional at the parent
    level (see :class:`ExchangeStatus`).
    """

    exchange_index: int
    exchange_active: bool
    trading_active: bool
    intra_exchange_transfers_active: bool


class ExchangeStatus(_KalshiResponseModel):
    """``GET /exchange/status`` response body.

    ``exchange_active`` and ``trading_active`` are the only two fields
    the grounding doc marks ``required``. ``intra_exchange_transfers_active``,
    ``exchange_estimated_resume_time``, and ``exchange_index_statuses``
    are documented but not marked required, so they are optional here
    (``exchange_index_statuses`` is explicitly documented as "absent
    when the per-index breakdown is unavailable").

    This model exposes only the raw, documented booleans and fields --
    it does not synthesize an undocumented "healthy"/"degraded"
    business-state enum on top of them, per this PR's binding
    decisions.
    """

    exchange_active: bool
    trading_active: bool
    intra_exchange_transfers_active: bool | None = None
    exchange_estimated_resume_time: str | None = None
    exchange_index_statuses: list[ExchangeIndexStatus] | None = None


class DailyOpenClose(_KalshiResponseModel):
    """One ``{open_time, close_time}`` entry of a weekday's hours."""

    open_time: str
    close_time: str


class StandardHoursBlock(_KalshiResponseModel):
    """One entry of ``schedule.standard_hours`` from ``GET /exchange/schedule``.

    The grounding doc's single example always populates every weekday
    array (even if some entries only ever hold zero or one interval in
    practice), so all seven weekday fields are modeled as required
    lists here; an empty list is a valid value distinct from a missing
    field, and each entry's own fields (``start_time``/``end_time``)
    are likewise treated as required, matching the doc's example.
    """

    start_time: str
    end_time: str
    monday: list[DailyOpenClose]
    tuesday: list[DailyOpenClose]
    wednesday: list[DailyOpenClose]
    thursday: list[DailyOpenClose]
    friday: list[DailyOpenClose]
    saturday: list[DailyOpenClose]
    sunday: list[DailyOpenClose]


class MaintenanceWindow(_KalshiResponseModel):
    """One entry of ``schedule.maintenance_windows``."""

    start_datetime: str
    end_datetime: str


class ExchangeSchedule(_KalshiResponseModel):
    """The inner ``schedule`` object of ``GET /exchange/schedule``.

    The grounding doc's ``Response`` section marks only the top-level
    ``schedule`` object itself as ``required`` (the whole envelope);
    it does not separately mark ``standard_hours``/``maintenance_windows``
    as required child attributes. Both are treated as optional lists
    here (defaulting to empty) for the same reason. See
    :class:`~kalshi_bot.rest.client._ExchangeScheduleEnvelope` for the
    top-level ``{"schedule": {...}}`` envelope this type is nested
    inside; :meth:`kalshi_bot.rest.client.KalshiDemoRestClient.get_exchange_schedule`
    returns this inner type directly, not the envelope.
    """

    standard_hours: list[StandardHoursBlock] = Field(default_factory=list)
    maintenance_windows: list[MaintenanceWindow] = Field(default_factory=list)


class _ExchangeScheduleEnvelope(_KalshiResponseModel):
    """The literal top-level ``{"schedule": {...}}`` envelope Kalshi returns.

    Not exported (not in ``__all__``): callers of
    :meth:`kalshi_bot.rest.client.KalshiDemoRestClient.get_exchange_schedule`
    receive the unwrapped :class:`ExchangeSchedule` directly, never this
    envelope. Kept as a separate model (rather than folding ``schedule``
    into :class:`ExchangeSchedule` itself) purely so the required-ness
    of the envelope's ``schedule`` key -- the grounding doc's only
    ``required`` field for this endpoint -- is validated precisely.
    """

    schedule: ExchangeSchedule
