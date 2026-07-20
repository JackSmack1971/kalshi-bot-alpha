# Architecture Overview

Deterministic, demo-only Kalshi crypto paper-trading bot with a
separate, OpenRouter-exclusive AI research/control plane. The full
system contract is `docs-dev/Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md`
(adopted by `docs/adr/ADR-0001-blueprint-v3-baseline.md`); this page is
an orientation map, not a replacement.

## Authority model

```text
AI may observe, investigate, challenge, explain, and propose.
Deterministic code must calculate, authorize, execute, reconcile, and account.
Humans must approve strategy, risk, market eligibility, reconciliation,
active configuration, and promotion changes.
```

## Trading pipeline (deterministic, single process)

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

## AI control plane (separate process, later phases)

```text
immutable sanitized evidence bundles
  -> agent supervisor + role agents (analyst / researcher / critic / reporter)
  -> OpenRouter gateway only (structured outputs, budgets, egress scanning)
  -> validated findings and proposals (distinct schemas + storage)
  -> human approval queue
```

No agent tool can reach execution, active configuration, ledger state,
or credentials. OpenRouter outage degrades analysis only.

## Contract documents (Phase 0)

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

## Repository layout

Matches blueprint §11. `src/kalshi_bot/` is an empty package until
Phase 1. `scripts/verify_demo_only.py` enforces the endpoint policy from
Phase 0 onward.
