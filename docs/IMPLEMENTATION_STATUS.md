# Implementation Status

Read this before planning or editing. Implement only the active phase; do
not build later-phase behavior early.

- **Planning baseline:** the repository contains the accepted Phase 0
  contracts and safety model, Phase 1 read-only connectivity, and the Phase
  3 deterministic paper-trading kernel.
- **Active phase:** Phase 3 — Portfolio and simulated execution.
- **AI phases:** not started. AI Phase A remains gated on stable
  deterministic simulation, risk, ledger, and replay evidence.

## Authority and approval state

Phase 0 and ADR-0001 are accepted by the human repository owner. Phase 1 was
explicitly activated for the read-only connectivity and soak workflow in
`docs/PHASE1_PLAN.md`. These approvals do not authorize live trading,
exchange mutation, production endpoints, or AI control-plane behavior.

The constitutional authority split remains binding:

```text
AI may observe, investigate, challenge, explain, and propose.
Deterministic code must calculate, authorize, execute, reconcile, and account.
Humans must approve strategy, risk, market eligibility, reconciliation,
active configuration, and promotion changes.
```

## Current tree

- `src/kalshi_bot/rest/` and `src/kalshi_bot/ws/` provide demo-only
  read-only transports.
- `src/kalshi_bot/auth/`, `credentials/`, `config/`, and `observability/`
  isolate signing, credential loading, configuration, and redaction.
- `src/kalshi_bot/market_data/` provides eligibility and order-book models.
- `src/kalshi_bot/strategies/`, `risk/`, and `execution/` provide
  deterministic strategy evaluation, synchronous risk checks, and simulated
  execution.
- `src/kalshi_bot/persistence/` and `reconciliation/` provide the append-only
  store and startup/reconnect/shutdown reconciliation boundaries.
- `src/kalshi_bot/cli.py` is the installed `kalshi-bot demo-smoke-order`
  operator entry point, with an explicitly opt-in local mock mode.
- `scripts/soak_phase1.py` is the separately supported, explicitly
  acknowledged Phase 1 demo-soak and evidence workflow.
- `alembic/` and `alembic/versions/` provide the persistence migration
  environment.
- `.github/workflows/ci.yml` runs the credential-free required checks;
  `.github/workflows/codeql.yml` remains a separate security workflow.

The former `src/kalshi_bot/application.py` Phase 1 supervisor was retired
because it had no production caller and would have created a second runtime
composition boundary. Its focused tests were retired with it. The supported
composition decision is recorded in `docs/PHASE1_PLAN.md`.

## Phase ledger

| Phase | Status |
| --- | --- |
| 0 — Contracts and safety model | Accepted and complete |
| 1 — Read-only connectivity | Implemented; explicit soak workflow retained |
| 2 — Order-book integrity | Not started as a separately promoted phase |
| 3 — Portfolio and simulated execution | Active; deterministic kernel implemented and verified locally |
| 4 — Demo order lifecycle | Deferred; exchange mutation is not implemented |
| 5 — Passive spread strategy | Deferred beyond the current deterministic evaluation kernel |
| 6 — Evaluation and hardening | Not started |
| AI A–D | Not started and gated |

## Safety boundaries

Only the Kalshi demo REST and WebSocket endpoints are permitted. No
production hostname or production switch exists. The current CLI mock path
does not use credentials or network access; the live demo path is not a CI
or pytest path and requires explicit operator configuration.

Trading code never requires `OPENROUTER_API_KEY`. No AI process, AI output,
or proposal path has execution, ledger-mutation, reconciliation-resolution,
allowlist, or active-configuration authority. Human approval is not inferred
or granted by code.

## Verification evidence

The repository-native verification contract is documented in
`.github/CONTRIBUTING.md` and enforced by `.github/workflows/ci.yml`:

| Check | Command | Scope |
| --- | --- | --- |
| Tests | `uv run pytest -q` | Full `tests/` tree |
| Lint | `uv run ruff check .` | Repository |
| Types | `uv run mypy .` | Repository |
| Demo safety | `uv run python scripts/verify_demo_only.py` | Enforced source/config/schema/test paths |
| Diff hygiene | `git diff --check` | Proposed diff |

Verification for remediation commit `94e51a9` completed locally: `uv run
pytest -q` passed, `uv run ruff check .` passed, `uv run mypy .` passed for
76 source files, `uv run python scripts/verify_demo_only.py` passed for 88
files, and `git diff --check` passed. CI repeats these checks on pull
requests and pushes to `main`; branch-protection required-check settings
remain a remote governance concern outside this change.

## Known gaps and deferred work

- Exchange order mutation, live order lifecycle, and production trading are
  not implemented and must remain absent.
- AI/OpenRouter control-plane runtime is not implemented.
- Full Phase 1 live-soak evidence is operator-generated and is not produced
  by CI.
- `docs/RUNBOOK.md` remains a later-phase deliverable.
- Correlation-group definitions and frozen edge-model versions remain owned
  by their later phases.
- `.claude/**`, if present, is process tooling and is outside product-phase
  approval unless separately reviewed.

## Human-review gates

- ADR-0001 acceptance: closed; see `docs/adr/0001-blueprint-v3-baseline.md`.
- Phase 0 sign-off: closed.
- Phase 1 activation: closed for the bounded scope in
  `docs/PHASE1_PLAN.md`; individual changes still require review.
- Phase 3 remains active and does not authorize exchange mutation or AI
  behavior.
