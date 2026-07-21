# Phase 1 Implementation Plan — Read-only connectivity

- **Status:** Activated
- **Activation date:** 2026-07-20
- **Decider:** Human repository owner
- **Governs:** blueprint §12 Phase 1 ("Read-only connectivity") and its
  exit criteria (runs 4 hours without unhandled failure, reconnects
  successfully, no order endpoint implemented — all specified in §12).
  Blueprint §14 ("Definition of Done") applies separately as the
  broader completion bar and does not itself define these Phase 1
  exit criteria.

This document is the binding scope for Phase 1. It supersedes any
informal plan discussed before this record. Each PR below still
requires its own review before merge — activation of Phase 1 as a
phase is not pre-approval of any individual PR's diff. No PR in this
stack may implement order placement/amendment/cancellation, order-book
delta subscription or reconstruction, market-eligibility decisions,
persistence, strategy, risk, portfolio, ledger, reconciliation,
replay, external-reference ingestion, or AI-control-plane behavior —
those remain out of scope for every Phase 1 PR regardless of
convenience or overlap.

`scripts/verify_demo_only.py` requires no change for this plan:
`ENFORCED_PATHS` already covers the entire `src/` tree recursively, so
every new module under `src/kalshi_bot/{observability,config,
credentials,auth,kalshi,market_data}/` is scanned without any
allowlist edit. No PR below may edit that script's `ENFORCED_PATHS`,
`SCANNED_SUFFIXES`, or `NEGATIVE_FIXTURE_MARKER` without first
demonstrating, in that PR's description, a concrete file that is in
scope for the demo-only guarantee but not covered by the current
allowlist.

All standard verification across every PR runs with no live
credentials and no live network access: mocked REST (`respx`), a
local controlled WebSocket test server, synthetic keypairs, and
sanitized fixtures. The one exception is the real four-hour demo soak
in PR 6, which is explicitly opt-in and never part of the standard
`pytest` gate.

---

## PR 1 — Phase 1 activation record and binding implementation plan

- **Paths:** `docs/IMPLEMENTATION_STATUS.md` (active-phase section,
  human-review gates, phase ledger), `docs/PHASE1_PLAN.md` (this file).
- **Responsibility:** record the human decision activating Phase 1 and
  commit this document as the binding scope subsequent PRs are checked
  against.
- **Forbidden:** no `src/` changes; no implementation of any kind.
- **Dependencies:** none (first PR).
- **Verification:** `git diff --check`; full existing verification
  suite re-run to confirm the documentation change didn't disturb
  anything (`uv run pytest -q`, `uv run ruff check .`, `uv run mypy .`,
  `uv run python scripts/verify_demo_only.py`).
- **Completion:** `docs/IMPLEMENTATION_STATUS.md` shows Phase 1
  activated, dated, and attributed to the human decider; this plan is
  named as the binding scope for PRs 2–6.

## PR 2 — Structured logging, global redaction, configuration, and credential loading

- **Paths:** `src/kalshi_bot/observability/__init__.py`,
  `src/kalshi_bot/observability/logging.py`;
  `src/kalshi_bot/config/__init__.py`,
  `src/kalshi_bot/config/models.py`,
  `src/kalshi_bot/config/loader.py`;
  `src/kalshi_bot/credentials/__init__.py`,
  `src/kalshi_bot/credentials/loader.py`;
  `tests/unit/test_logging.py`, `tests/unit/test_log_redaction.py`,
  `tests/unit/test_config_loader.py`,
  `tests/unit/test_credential_loader.py`.
- **Responsibility — separation of concerns is exact and enforced by
  code shape, not just convention:**
  - `config/models.py` + `config/loader.py` validate only **non-secret**
    settings (log level, timeouts, retry/backoff bounds) plus
    `CredentialReferences` — a value object holding only
    environment-variable **names** and a key-file **path**, never a
    secret value.
  - `credentials/loader.py` is the sole reader of `os.environ` and the
    private-key file anywhere in the repository. It consumes a
    `CredentialReferences` and produces `LoadedDemoCredentials` — a
    narrow, opaque type. `LoadedDemoCredentials` is constructed **only**
    inside this loader; no other module builds one directly.
  - `LoadedDemoCredentials` itself does not hand out raw private-key
    material to callers. Raw key material is encapsulated behind a
    signing-capability object (`RequestSigner`, built in PR 3) that the
    loader hands the material to once, internally. REST/WS clients in
    PR 4/5 depend on the signer interface, never on
    `LoadedDemoCredentials` or raw key bytes directly.
  - `observability/logging.py` is production-quality `structlog`-based
    structured JSON logging with a global redaction processor **from
    this PR onward** — the permanent interface, not a temporary stub.
    It unconditionally redacts access-key IDs, signatures, auth
    headers, private-key material, and raw request/response bodies.
    No PR in this stack introduces `print` or unredacted stdlib
    logging at any point, including before this PR lands.
- **Dependencies added:** `structlog`; `pydantic>=2` for
  `config/models.py`'s non-secret settings only (the Pydantic
  restriction from the binding decisions applies to the signer's
  internal value object in PR 3, not to configuration).
- **Interfaces:**
  - `configure_logging(level: str) -> None`; `get_logger(name: str) ->
    BoundLogger`; exported `redact_processor` so tests can assert it is
    wired into every logger instance, not just the root.
  - `CredentialReferences(access_key_env: str, private_key_path_env:
    str)`.
  - `LoadedDemoCredentials` — opaque; no `__repr__`/`__str__` that
    exposes key material; consumed only by PR 3's signer construction.
  - `AppConfig` (Pydantic model: log level, REST/WS timeout/retry
    bounds, `CredentialReferences`) — never a literal secret field.
- **Failure states:** missing/unreadable private-key file or env var →
  typed `CredentialLoadError`, fails closed, no fallback to an
  unauthenticated mode; malformed config → typed `ConfigError` at
  startup, before any network component is constructed.
- **Tests:**
  - Redaction: adversarial suite using synthetic secret markers (never
    realistic-looking material) proving they never appear in emitted
    JSON across normal logging, raised exceptions, retries, and nested
    structures.
  - Config: valid/invalid settings; rejection of any host-selection
    field that isn't the fixed demo host.
  - Credential loader: missing file, unreadable permissions, present
    env var, absent env var — all fail closed with typed errors, no
    secret value in any raised exception's message or `repr`.
- **Verification:** `uv run pytest tests/unit/test_logging.py
  tests/unit/test_log_redaction.py tests/unit/test_config_loader.py
  tests/unit/test_credential_loader.py`, `uv run mypy .`,
  `uv run ruff check .`, `uv run python scripts/verify_demo_only.py`.
  No live credentials or network — synthetic key files in a temp dir.
- **Dependencies:** PR 1.

## PR 3 — Authentication signer

- **Paths:** `src/kalshi_bot/auth/__init__.py`,
  `src/kalshi_bot/auth/signer.py`; `tests/unit/test_auth_signer.py`,
  `tests/property/test_auth_signer_properties.py`.
- **Responsibility:** pure request-signing per Kalshi's documented
  RSA-PSS scheme. `RequestSigner` is constructed once from
  `LoadedDemoCredentials` inside the credential-loading path (or
  immediately after, at application wiring in PR 6) and is the only
  object downstream code holds — it encapsulates the raw private key
  and never re-exposes it. The signer itself never touches `os.environ`
  or the key file.
- **Forbidden:** no network I/O; no credential loading; no logging of
  key material.
- **Dependencies added:** `cryptography` (RSA-PSS) — the only new
  dependency this PR adds.
- **Interfaces:** a lightweight `@dataclass(frozen=True, slots=True)`
  (not Pydantic) `SignedHeaders(access_key: str, signature: str,
  timestamp_ms: int)`; `RequestSigner.sign(method: str, path: str,
  timestamp_ms: int) -> SignedHeaders`; `RequestSigner.from_credentials
  (credentials: LoadedDemoCredentials) -> RequestSigner`.
- **Failure states:** invalid/unusable key material → typed
  `SigningError`; never produces a partially-populated or unsigned
  `SignedHeaders`.
- **Tests — corrected RSA-PSS plan (signatures are randomized; no
  byte-for-byte reproducibility assertion):**
  - Canonical message construction: given fixed `method`/`path`/
    `timestamp_ms`, the exact byte string handed to the signature
    primitive matches the documented canonical form — this part is
    deterministic and byte-checkable.
  - Round-trip verification: sign with a synthetic test keypair,
    verify the signature against the corresponding public key.
  - Negative verification: mutating method, path, timestamp, key, or
    signature independently causes verification to fail — one test per
    mutated field.
- **Verification:** `uv run pytest tests/unit/test_auth_signer.py
  tests/property/test_auth_signer_properties.py`, `uv run mypy .`,
  `uv run ruff check .`. Synthetic keypair generated in-test; no live
  credentials.
- **Dependencies:** PR 2.

## PR 4 — Read-only demo REST client, exchange status, and market discovery

- **Paths:** `src/kalshi_bot/kalshi/__init__.py`,
  `src/kalshi_bot/kalshi/demo_endpoints.py` (existing, reused),
  `src/kalshi_bot/kalshi/rest_client.py`,
  `src/kalshi_bot/kalshi/models.py`, `src/kalshi_bot/kalshi/errors.py`,
  `src/kalshi_bot/market_data/__init__.py`,
  `src/kalshi_bot/market_data/catalog.py`,
  `src/kalshi_bot/market_data/exchange_status.py`;
  `tests/unit/test_rest_client.py`,
  `tests/contract/test_rest_client_demo_only.py`,
  `tests/contract/test_market_summary_schema.py`,
  `tests/unit/test_catalog.py`, `tests/unit/test_exchange_status.py`,
  `tests/integration/test_rest_client_mocked.py`.
- **Responsibility:** `KalshiDemoRestClient` validates the demo host
  at construction (refuses before any socket opens) and receives a
  `RequestSigner`, never raw credentials and never reads the
  environment itself. Exposes only `GET /markets`, `GET
  /exchange/status`, `GET /exchange/schedule`. `market_data/catalog.py`
  wraps market listing/pagination into typed `MarketSummary` objects —
  discovery only, no eligibility logic (later phase, per
  `market-data-and-eligibility.md`). `market_data/exchange_status.py`
  wraps status/schedule into typed `ExchangeStatus`/`ExchangeSchedule`.
- **Forbidden:** no `POST`/`DELETE`, no generic
  `request(method, path)` escape hatch, no `environment` parameter or
  dormant production constant, no eligibility/allowlist decision
  logic, no persistence.
- **Dependencies added:** `httpx`; `respx` (dev-only).
- **Interfaces:** `KalshiDemoRestClient(signer: RequestSigner, config:
  AppConfig)`; `get_markets(...) -> list[MarketSummary]`;
  `get_exchange_status() -> ExchangeStatus`; `get_exchange_schedule()
  -> ExchangeSchedule`.
- **Failure states:** non-demo host at construction → raises before
  any socket opens; HTTP/auth error → typed `KalshiApiError`/
  `KalshiAuthError` with status/body captured through PR 2's redacted
  logger, never raw; pagination failure mid-fetch → raises, never
  returns a silently-truncated list.
- **Verification:** `uv run pytest tests/unit/test_rest_client.py
  tests/unit/test_catalog.py tests/unit/test_exchange_status.py
  tests/contract/ tests/integration/test_rest_client_mocked.py`,
  `uv run python scripts/verify_demo_only.py`, `uv run mypy .`,
  `uv run ruff check .`. `respx` against the demo host only — no live
  network, no live credentials, synthetic keypair from PR 3's fixtures.
- **Dependencies:** PR 2, PR 3.

## PR 5 — Demo WebSocket client, reconnect lifecycle, ticker and trade subscriptions

- **Paths:** `src/kalshi_bot/kalshi/websocket_client.py`,
  `src/kalshi_bot/market_data/normalizer.py` (WS frame → typed event;
  not an order-book builder); `tests/unit/test_websocket_client.py`,
  `tests/unit/test_subscriptions.py`,
  `tests/contract/test_ws_message_schema.py`,
  `tests/integration/test_websocket_reconnect.py`.
- **Responsibility:** `KalshiDemoWebSocketClient` validates the demo
  WS host at construction, signs the WS handshake via the `RequestSigner`
  from PR 3, exposes connect/disconnect/bounded-jittered-backoff
  reconnect, and subscription to `ticker`/`trade` channels only.
  Normalizes frames into typed `TickerUpdate`/`TradeUpdate` events
  delivered to a caller-supplied async consumer.
- **Forbidden:** no `orderbook_delta` subscription or order-book
  reconstruction of any kind; no eligibility decisions; no persistence
  beyond in-process/log; no strategy, risk, portfolio, ledger,
  reconciliation, replay, external-reference, order-mutation, or
  AI-control-plane code anywhere in this PR.
- **Dependencies added:** `websockets`.
- **Interfaces:** `KalshiDemoWebSocketClient(signer: RequestSigner,
  config: AppConfig)` as an async context manager;
  `subscribe_ticker(tickers: list[str]) -> AsyncIterator[TickerUpdate]`;
  `subscribe_trades(tickers: list[str]) -> AsyncIterator[TradeUpdate]`;
  `ReconnectPolicy` (bounded exponential backoff with jitter).
- **Failure states:** non-demo WS host → refuse before dial; dropped
  connection → typed `WebSocketDisconnected` event logged and
  reconnect triggered, never a silent message drop; malformed frame →
  logged and dropped with a typed counter, does not crash the
  subscription loop; unknown channel → ignored and logged, never
  silently accepted as a known type.
- **Reconnect evidence, clarified:**
  - Standard-gate integration tests must prove reconnect behavior using
    a **local controlled WebSocket test server** (`tests/integration/
    test_websocket_reconnect.py`) — this is the primary and only
    evidence required for the standard verification gate.
  - The live demo soak in PR 6 may close its own client-side socket
    exactly once, through a safe, explicit transport hook designed for
    that purpose (e.g. an injectable "simulate local disconnect"
    callable that closes the client's own connection object). It must
    never send malformed, abusive, or otherwise disruptive traffic to
    Kalshi's demo servers, and must never attempt to force a
    server-side disconnect.
  - The evidence report (PR 6) explicitly labels which reconnect
    events came from the local mock server (standard-gate proof) versus
    the one client-side-triggered reconnect observed during the live
    demo run (soak proof). These are never merged into a single
    undifferentiated count.
- **Verification:** `uv run pytest tests/unit/test_websocket_client.py
  tests/unit/test_subscriptions.py tests/contract/test_ws_message_schema.py
  tests/integration/test_websocket_reconnect.py`,
  `uv run python scripts/verify_demo_only.py`, `uv run mypy .`,
  `uv run ruff check .`. No live credentials or network.
- **Dependencies:** PR 3, PR 4.

## PR 6 — Phase 1 supervisor, opt-in four-hour soak tooling, evidence report, and phase-exit audit

- **Paths:** `src/kalshi_bot/application.py` (minimal Phase 1
  supervisor: wires config → credential loader → signer → REST/WS
  clients → subscriptions, using PR 2's logger throughout — a
  Phase-1-scoped subset of `runtime-lifecycle.md`'s startup sequence:
  config, demo-policy, logging, credentials, exchange-status,
  discovery-without-eligibility-filter, WS-connect, subscribe,
  stream-health; nothing beyond that, since reconciliation/eligibility/
  risk don't exist yet); `scripts/soak_phase1.py` (operator-run,
  opt-in, not imported by any test); `docs/PHASE1_SOAK_TEMPLATE.md`
  (report schema/template, versioned); `artifacts/phase1/soak/<run-id>/`
  (immutable, timestamped evidence directories — created by the soak
  script, not hand-authored); `tests/unit/test_soak_report_schema.py`,
  `tests/unit/test_application_wiring.py`; plus a re-run of PR 2's
  redaction suite extended to every real call site introduced by PRs
  3–5, including their exception and retry paths.
- **Responsibility:**
  - `application.py`: minimal composition root proving PRs 2–5 wire
    together correctly; still entirely read-only.
  - `scripts/soak_phase1.py`: runs the wired application against the
    live demo endpoints for 4 hours, triggers exactly one client-side
    disconnect via the safe transport hook from PR 5, and writes a new
    immutable evidence directory rather than overwriting any prior run.
  - **Soak evidence layout (immutable, timestamped, one run = one
    directory):**
    ```
    artifacts/phase1/soak/<run-id>/
      report.json        # schema-versioned, see fields below
      report.md           # human-readable rendering of report.json
    ```
    `<run-id>` is a deterministic identifier derived from the run's UTC
    start timestamp (e.g. `2026-07-20T140000Z`), not a counter that
    could collide or be reused. The soak script refuses to write into
    an existing `<run-id>` directory — each real run gets its own,
    nothing is ever overwritten. `report.json` records at minimum:
    - commit SHA
    - configuration hash
    - lockfile/dependency hash (`uv.lock` hash)
    - UTC start and end timestamps
    - duration
    - REST and WebSocket event counts (by type)
    - reconnect events and latency, **partitioned into**
      `local_mock_reconnects` (from the PR 5 standard-gate integration
      test evidence, referenced by test run, not re-executed live) and
      `live_soak_reconnects` (the single client-side-triggered
      disconnect/reconnect observed during this run)
    - unhandled failure count (must be zero for the run to count as
      exit-criterion evidence)
    - redaction/secret-scan result (pass/fail, referencing the PR 2/PR
      6 adversarial suite run against this run's logs)
    - report schema version
  - Redaction completion: extends PR 2's adversarial redaction suite to
    cover every transport/auth call site introduced by PRs 3–5,
    including exception and retry paths, proving synthetic secrets
    never appear in emitted records anywhere in the finished Phase 1
    surface.
  - A phase-exit-audit pass (reusing the existing
    `.claude/skills/phase-exit-audit` skill, not new code) run against
    the actual soak evidence directory before anyone claims Phase 1's
    exit criteria are met.
- **Forbidden:** no order placement of any kind during the soak or
  anywhere in this PR; no malformed/abusive/disruptive traffic to
  Kalshi under any circumstance; the soak script must not run as part
  of the standard `pytest` gate or any CI-equivalent invocation; no
  overwriting a prior `artifacts/phase1/soak/<run-id>/` directory.
- **Interfaces:** `run_phase1_supervisor(config, credentials) -> None`;
  CLI entry `uv run python scripts/soak_phase1.py --duration-hours 4`.
- **Failure states:** any unhandled exception during the soak → nonzero
  exit, the evidence directory is still written with the failure
  recorded (never discarded).
- **Tests:** `test_application_wiring.py` (mocked end-to-end, no live
  network); `test_soak_report_schema.py` (report-writer produces the
  documented shape and the immutable-directory-per-run behavior given
  synthetic run data, including a test that a second write to the same
  `<run-id>` is refused); the extended redaction suite (mocked/
  synthetic, no live network).
- **Verification (standard gate — no live credentials or network):**
  `uv run pytest tests/unit/test_application_wiring.py
  tests/unit/test_soak_report_schema.py` plus the full redaction suite,
  `uv run mypy .`, `uv run ruff check .`,
  `uv run python scripts/verify_demo_only.py`. **Separately, opt-in
  only:** the actual 4-hour `scripts/soak_phase1.py` run against live
  demo credentials, explicitly triggered by a human, producing a new
  `artifacts/phase1/soak/<run-id>/` directory.
- **Completion:** standard suite green with zero live dependencies; a
  real 4-hour soak evidence directory exists showing zero unhandled
  failures and at least one successful reconnect, with local-mock and
  live-soak reconnect evidence clearly distinguished — this is the
  literal Phase 1 exit criterion from blueprint §12, and must also
  satisfy the broader completion bar in §14, so PR 6 is not "done" for
  exit-criteria purposes until that real run has happened and been
  reviewed.
- **Dependencies:** PR 2, PR 3, PR 4, PR 5.

---

No PR beyond PR 1 is implemented by this document. PR 2 begins only
after PR 1 is reviewed and merged.
