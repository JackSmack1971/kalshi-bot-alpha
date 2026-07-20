# Safety Model

Normative Phase 0 contract. Sources: blueprint §2, §5.24; `CLAUDE.md`;
`.claude/rules/kalshi-transport-safety.md`, `credential-privacy.md`,
`governance-and-approvals.md`. Where this document and the blueprint
disagree, the safer behavior wins and the conflict must be surfaced.

## 1. Demo-only endpoint policy

The only permitted Kalshi endpoints, in any code, configuration,
environment-derived setting, persisted state, constructed URL, redirect,
or generated variant:

```text
REST:      https://external-api.demo.kalshi.co/trade-api/v2
WebSocket: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2
```

Every other Kalshi hostname — including the bare `kalshi.co` /
`kalshi.com` domains and any production or elections API host — is
forbidden. This is enforced three ways:

1. **Statically:** `scripts/verify_demo_only.py` scans enforced paths
   (`src/`, `config/`, `schemas/`, `scripts/`, `tests/`, `migrations/`,
   `pyproject.toml`, `.env.example`) and fails on any Kalshi hostname
   outside the allowlist. `tests/unit/test_demo_only_policy.py` runs the
   scan in CI and proves the detector catches non-demo hosts.
2. **At startup (Phase 1+):** configuration validation must refuse to
   start when any configured host is off the allowlist, environment mode
   is unset or ambiguous, credentials are absent/malformed/unsafe, clock
   drift exceeds tolerance, or persistent state records an unresolved
   shutdown or reconciliation failure.
3. **Structurally (Phase 1+):** transports are demo-specific types
   (`KalshiDemoRestClient`, `KalshiDemoWebSocketClient`) whose endpoints
   are fixed at the type level. A generic `KalshiClient(environment)`,
   an `environment=production` switch, or a dormant production constant
   is an architecture violation, not a configuration option.

Operator-visible status must permanently display `DEMO MODE`.

Production enablement is out of scope for this entire project. It would
require a separate project, architecture, security review, and explicit
human approval.

## 2. Credential policy

Kalshi demo credentials (access-key ID + local RSA private-key file):

- Come only from environment-variable references, an OS secret store, or
  a private-key file **outside the repository** with owner-only
  permissions.
- Never appear in source control, prompts, logs, fixtures, snapshots,
  dashboards, telemetry, exception messages, frontend processes, or AI
  evidence bundles.
- Access-key IDs, signatures, and full authentication headers are
  redacted from all logs and errors. Tests use synthetic markers, never
  realistic secret material.

Authenticated Kalshi requests use an access-key ID, RSA-PSS signature,
and millisecond timestamp; timestamps outside drift policy are rejected.

## 3. Process isolation

```text
paper-trader process:
  KALSHI_DEMO_ACCESS_KEY, KALSHI_DEMO_PRIVATE_KEY_PATH
  never requires OPENROUTER_API_KEY

agent-control-plane process:
  OPENROUTER_API_KEY
  no Kalshi credentials, auth material, or execution capabilities
  read-only sanitized evidence access only
```

If process separation is ever temporarily unavailable, equivalent OS and
application controls must *prove* the agent runtime cannot read Kalshi
secrets or invoke execution. OpenRouter failure may degrade analysis
only; it must never impair cancellation, reconciliation, risk
enforcement, accounting, persistence, or shutdown.

## 4. Deterministic authority boundary

```text
AI may observe, investigate, challenge, explain, and propose.
Deterministic code must calculate, authorize, execute, reconcile, and account.
Humans must approve strategy, risk, market eligibility, reconciliation,
active configuration, and promotion changes.
```

AI agents must never: call Kalshi trading transports; create or cancel
orders; approve or bypass risk; resolve reconciliation; mutate ledger or
authoritative state; activate configuration; modify allowlists; mark
incidents resolved; or emit data accepted as an authoritative trading
type. Model output uses distinct proposal schemas, namespaces, storage,
and validation paths and can never deserialize into `TradeIntent`, an
approved order plan, a risk approval, a reconciliation resolution, a
ledger event, or active configuration.

Risk authorization is synchronous, centralized, deterministic,
versioned, and non-bypassable. Strategy evaluation must not begin before
reconciliation, market eligibility, data health, and stream health are
deterministically confirmed.

OpenRouter is the only external LLM inference provider; no direct vendor
SDKs or clients.

## 5. Human approval boundary

Durable human approval is required before: changing strategy logic or
parameters; changing risk limits; adding a market/series to an
allowlist; activating proposed configuration; accepting a reconciliation
adjustment; promoting a strategy version; treating an AI conclusion as
binding; expanding agent tool or evidence access; or weakening privacy,
fallback, or model policy.

An approval record contains: approver, timestamp, proposal hash,
evidence scope, decision, and resulting code/configuration version.
Approval never directly mutates active runtime state; normal reviewed
engineering and deployment paths remain required. Approval is never
simulated, inferred, fabricated, self-granted, or backfilled.
