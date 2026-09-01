# Architecture Overview

Deterministic, demo-only Kalshi crypto paper-trading bot with a
separate, OpenRouter-exclusive AI research/control plane. The full
system contract is `docs-dev/Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md`
(adopted by `docs/adr/0001-blueprint-v3-baseline.md`,
status: Accepted — see
`docs/IMPLEMENTATION_STATUS.md`). This page is an orientation map, not
a replacement.

## Authority model

```text
AI may observe, investigate, challenge, explain, and propose.
Deterministic code must calculate, authorize, execute, reconcile, and account.
Humans must approve strategy, risk, market eligibility, reconciliation,
active configuration, and promotion changes.
```

This split is binding for every future component. See
`docs/SAFETY_MODEL.md` for how it is enforced.

## Trading pipeline (deterministic, single process — target, not yet implemented)

```text
Kalshi Demo REST/WS
  -> market catalog + eligibility (allowlist)
  -> order-book builder (health states)
  -> feature engine (immutable snapshots)
  -> strategy engine (emits TradeIntent; never calls the exchange)
  -> risk gateway (synchronous, non-bypassable)
  -> execution engine (unique client_order_id, idempotent, post-only)
  -> order state machine (exchange-evidence driven)
  -> append-only portfolio ledger
  -> reconciliation service (suspends trading on mismatch)
```

None of these components exist yet (see "Current implementation
limitations" below). This diagram fixes the target sequencing and
module boundaries that the phase introducing each component must
satisfy.

## AI control plane (separate process, later phases)

```text
immutable sanitized evidence bundles
  -> agent supervisor + role agents (analyst / researcher / critic / reporter)
  -> OpenRouter gateway only (structured outputs, budgets, egress scanning)
  -> validated findings and proposals (distinct schemas + storage)
  -> human approval queue
```

No agent tool can reach execution, active configuration, ledger state,
or credentials. OpenRouter outage degrades analysis only. Phase 0
introduces no AI-agent runtime and no OpenRouter client.

## Demo-only boundary

Only these Kalshi endpoints are ever permitted, anywhere in this
codebase:

```text
REST:      https://external-api.demo.kalshi.co/trade-api/v2
WebSocket: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2
```

This is a structural, not configurable, boundary — see
`docs/SAFETY_MODEL.md` §1 and `docs/DEMO_ENDPOINT_POLICY.md` for the
enforcement mechanisms that exist today.

## Current Phase 3 implementation

The deterministic runtime includes read-only Kalshi connectivity, market
eligibility and order-book models, synchronous risk checks, passive-spread
strategy evaluation, simulated execution, persistence, reconciliation, and
the CLI mock acceptance path. Exchange mutation and the separate AI control
plane remain out of scope. The following contracts and modules define the
current implementation:

| Contract | Location |
| --- | --- |
| Safety model (endpoints, credentials, authority, approvals) | `docs/SAFETY_MODEL.md` |
| Domain models, order state machine, ledger, invariants | `docs/DATA_MODEL.md` |
| Risk-limit schema and correlated scenario risk | `docs/RISK_MODEL.md`, `config/risk/conservative.yaml` |
| Failure taxonomy | `docs/FAILURE_TAXONOMY.md` |
| Passive-spread strategy and quote-expectancy contract | `docs/STRATEGY_SPEC.md` |
| Microstructure contracts (archetypes, queue, markout, external reference) | `docs/MICROSTRUCTURE_CONTRACT.md` |
| Experiment registry and statistical policy | `docs/RESEARCH_PROTOCOL.md` |
| Paper-trading evaluation protocol | `docs/PAPER_TRADING_PROTOCOL.md` |
| Frozen machine-readable schemas | `schemas/*.schema.json` |
| Phase tracking | `docs/IMPLEMENTATION_STATUS.md` |

### Authoritative schema inventory

Every schema file uses kebab-case naming and is paired with a
companion `docs/*.md` policy document that governs its meaning; the
schema is the executable contract, the doc explains it:

| Schema | Companion document |
| --- | --- |
| `schemas/trade-intent.schema.json` | `docs/DATA_MODEL.md` §2 |
| `schemas/order-state.schema.json` | `docs/DATA_MODEL.md` §3, `docs/ORDER_STATE_MACHINE.md` |
| `schemas/risk-limits.schema.json` | `docs/RISK_MODEL.md` |
| `schemas/market-archetype.schema.json` | `docs/MICROSTRUCTURE_CONTRACT.md` §1 |
| `schemas/quote-expectancy.schema.json` | `docs/STRATEGY_SPEC.md` §3 |
| `schemas/queue-calibration.schema.json` | `docs/MICROSTRUCTURE_CONTRACT.md` §2 |
| `schemas/markout-toxicity.schema.json` | `docs/MICROSTRUCTURE_CONTRACT.md` §4 |
| `schemas/experiment-registration.schema.json` | `docs/RESEARCH_PROTOCOL.md` §1 |
| `schemas/statistical-sufficiency.schema.json` | `docs/RESEARCH_PROTOCOL.md` §2, §5 |

`trade-intent.schema.json` is the single authoritative shape that may
be produced by the deterministic strategy engine; no AI output path
may deserialize into it (see `docs/SAFETY_MODEL.md` §3).

## Module and authority boundaries

Per blueprint §3 "Deployment shape", the eventual trading runtime is a
single local process with internally separated modules:

```text
CLI / Supervisor
      |
      v
Application Runtime
  +-- Market Data
  +-- Strategy
  +-- Risk
  +-- Execution
  +-- Portfolio
  +-- Persistence
  +-- Observability
```

The AI control plane is a separate local process consuming immutable,
sanitized evidence bundles exported by the deterministic runtime; it
never shares a process, credential set, or authority with the trading
runtime (blueprint §2.3, §3 "AI deployment shape"). See
`docs/SAFETY_MODEL.md` §2–3 for the credential and authority
boundaries this implies.

## Repository layout

Matches blueprint §11:

```text
docs/            prose contracts and policy documents
schemas/         frozen machine-checkable JSON Schema contracts
src/kalshi_bot/  the deterministic demo-only runtime package (Phase 3)
tests/           unit, contract, integration, acceptance, property
config/          risk and other operator-reviewed configuration
migrations/      persistence migrations
```

`docs-dev/` contains the blueprint and retained Kalshi reference material.
Generated OpenAPI source/site indexes are intentionally excluded from the
repository because they are not consumed by the runtime or tests.
`scripts/verify_demo_only.py` enforces the endpoint policy from Phase
0 onward.

## Current implementation limitations

The current implementation is deterministic and demo-only. It does not
place live orders, use production endpoints, or provide an AI-agent runtime
or OpenRouter client. See `docs/IMPLEMENTATION_STATUS.md` for the
authoritative phase ledger and exit criteria.
