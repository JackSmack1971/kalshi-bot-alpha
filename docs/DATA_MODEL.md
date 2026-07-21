# Data Model

Normative Phase 0 contract for domain models, the order state machine,
the ledger, and traceability invariants. Sources: blueprint §5.6, §5.8,
§5.11–§5.14; `.claude/rules/accounting-and-domain-models.md`.

This document owns the order-state and ledger shapes directly (§3–§4)
and does not duplicate the sibling contracts it depends on. For the
full definitions, see:

- Quote-expectancy decomposition — `docs/STRATEGY_SPEC.md` §3,
  `schemas/quote-expectancy.schema.json`.
- Market archetype — `docs/MICROSTRUCTURE_CONTRACT.md` §1,
  `schemas/market-archetype.schema.json`.
- Experiment registry entry — `docs/RESEARCH_PROTOCOL.md` §1,
  `schemas/experiment-registration.schema.json`.
- Risk limits and correlated scenario risk — `docs/RISK_MODEL.md`,
  `schemas/risk-limits.schema.json`.
- AI evidence bundles — referenced by `docs/RESEARCH_PROTOCOL.md` and
  `docs/SAFETY_MODEL.md` §3, §6; no evidence-bundle schema is frozen
  yet, since it requires the reconciliation and ledger models this
  document defines and no evidence-producing runtime exists in Phase 0.

## 1. Value conventions

- **Prices and money are exact fixed-point decimals** (cents for Kalshi
  contract prices; decimal USD for cash). Binary floating point is
  forbidden for exchange prices and accounting values. In YAML/JSON,
  monetary values are strings (e.g. `"25.00"`) to prevent accidental
  float parsing.
- **Domain models are immutable** (frozen Pydantic v2 models) wherever
  practical; state changes create new records, not mutations.
- **Provenance is mandatory.** Every derived record preserves source and
  calculation timestamps, source event ranges, version IDs, quality
  states, and content hashes where applicable.
- **Timestamps** are UTC, millisecond precision.
- For binary contracts, complementary YES/NO prices are derived
  consistently, but the original exchange-side representation is
  retained for audit and reconciliation.

## 2. TradeIntent (authoritative; strategy → risk only)

Frozen field set (`schemas/trade-intent.schema.json`):

```text
intent_id                    strategy_id               strategy_version
market_ticker                action                    side
limit_price                  desired_count             time_in_force
reason_codes                 feature_snapshot_id       signal_confidence
expected_fill_probability    expected_queue_wait_seconds
expected_gross_spread_capture  expected_fee_cost
expected_adverse_selection   expected_inventory_cost
expected_settlement_risk     expected_cancel_probability
expected_net_edge_usd        edge_model_version
calibration_sample_size      calibration_confidence    expiry_timestamp
```

Binding rules:

- `signal_confidence`, `expected_fill_probability`, and
  `expected_net_edge_usd` are **three distinct fields** and must never
  share one ambiguous field.
- `TradeIntent.expected_net_edge_usd` and
  `QuoteExpectancyRecord.expected_net_edge_usd`
  (`schemas/quote-expectancy.schema.json`, referenced above) are frozen
  under the same field name by design, but are not the same value or
  the same record: `TradeIntent`'s is the strategy engine's forward
  estimate at decision time, owned by `trade-intent.schema.json`; the
  quote-expectancy record's is the versioned decomposition persisted
  per quote (`docs/STRATEGY_SPEC.md` §3), owned by
  `quote-expectancy.schema.json`. Neither schema aliases or derives
  from the other.
- Every intent references exactly one immutable `feature_snapshot_id`
  and a versioned `edge_model_version`.
- `TradeIntent` may be produced **only** by the deterministic strategy
  engine. No AI output path may deserialize into this type (distinct
  proposal schemas, namespaces, storage, and validation are mandatory).
- Intents expire; the risk gateway rejects expired intents.

## 3. Order state machine

States and legal transitions (blueprint §5.11). Transitions are driven
by exchange evidence, never assumptions.

| From | To | Trigger |
| --- | --- | --- |
| — | `INTENT_CREATED` | strategy emits `TradeIntent` |
| `INTENT_CREATED` | `RISK_APPROVED` | risk gateway approves (records decision) |
| `INTENT_CREATED` | *(terminal: risk-rejected)* | any risk rule fails; intent never becomes an order |
| `RISK_APPROVED` | `SUBMISSION_PENDING` | execution engine records command idempotently, then transmits |
| `SUBMISSION_PENDING` | `REJECTED` | exchange rejects (typed error) |
| `SUBMISSION_PENDING` | `OUTCOME_UNKNOWN` | timeout/ambiguous transport result after transmission |
| `SUBMISSION_PENDING` | `ACKNOWLEDGED` | exchange acknowledgement with exchange_order_id |
| `OUTCOME_UNKNOWN` | `RECONCILING` | reconciliation queries by `client_order_id`; market suspended meanwhile |
| `RECONCILING` | `ACKNOWLEDGED` / `REJECTED` / `CANCELLED` / `FILLED` | deterministic exchange evidence resolves the outcome |
| `ACKNOWLEDGED` | `OPEN` | resting on book |
| `ACKNOWLEDGED` | `FILLED` / `CANCELLED` / `EXPIRED` | immediate terminal evidence |
| `OPEN` | `PARTIALLY_FILLED` | fill event for less than full count |
| `OPEN` | `CANCEL_PENDING` | cancel command transmitted |
| `PARTIALLY_FILLED` | `FILLED` | remaining count reaches zero |
| `PARTIALLY_FILLED` | `CANCEL_PENDING` | cancel command transmitted |
| `CANCEL_PENDING` | `CANCELLED` | exchange confirms cancel (fills received meanwhile are applied first) |
| `OPEN` / `PARTIALLY_FILLED` | `EXPIRED` | exchange lifecycle evidence |

Terminal states: `REJECTED`, `FILLED`, `CANCELLED`, `EXPIRED`. Any other
observed transition is an incident (`IMPOSSIBLE_STATE`) and suspends
trading pending reconciliation.

Invariants: `filled_count ≤ submitted_count`; `remaining_count ≥ 0`;
every transition is persisted append-only in `order_state_transitions`
with its triggering evidence.

## 4. Ledger

Append-only financial events; derived balances must be reproducible by
replaying the ledger:

```text
ORDER_RESERVED   ORDER_RELEASED   FILL_APPLIED     FEE_APPLIED
POSITION_MARKED  MARKET_SETTLED   ADJUSTMENT_RECONCILED
```

- Applying the same event twice must not create duplicate value
  (idempotency keys on event identity).
- `ADJUSTMENT_RECONCILED` requires exchange evidence and durable human
  approval; there is no silent repair path.
- Tracked balances: cash, reserved cash, YES/NO positions, average entry
  price, realized/unrealized P&L, fees, open-order exposure, settlement
  outcomes, strategy attribution.

## 5. Persistence tables (target schema)

Blueprint §5.14: `markets`, `market_snapshots`, `orderbook_events`,
`trade_events`, `feature_snapshots`, `strategy_intents`,
`risk_decisions`, `orders`, `order_state_transitions`, `fills`,
`positions`, `ledger_entries`, `reconciliation_runs`,
`runtime_incidents`, `strategy_runs`, `daily_performance`,
`queue_state_snapshots`, `queue_calibrations`,
`quote_expectancy_records`, `external_reference_events`,
`market_archetypes`, `markout_measurements`, `toxicity_classifications`,
`scenario_risk_snapshots`, `experiment_registry`,
`statistical_evaluations` — introduced phase by phase via Alembic
migrations, never ahead of the phase that uses them.

## 6. Traceability invariants

- `client_order_id` is globally unique (UUID-based).
- Every submitted order traces to exactly one strategy intent, one
  feature snapshot, and one approved risk decision.
- Every fill traces to one exchange order.
- Every position/cash change traces to one or more ledger events.
- Every strategy decision records its strategy and feature versions.
- Every passive order traces to one quote-expectancy record and one
  queue-state snapshot; a fill can never reference a snapshot created
  after its order's submission.
- Every fill receives versioned markout and toxicity classifications
  when data coverage permits.
- Every market and decision preserves its `market_archetype_id`.
- Every external numerical claim used by an agent traces to a
  deterministic tool result.
- Every confirmatory experiment is preregistered before its scored data
  window begins and is immutable afterwards.

## Phase 0 scope

No ORM, database, or Alembic migration exists yet; `migrations/` is a
placeholder (see `docs/IMPLEMENTATION_STATUS.md`). This document fixes
the shapes and invariants that the phase introducing persistence must
implement without weakening. `trade-intent.schema.json` and the
sibling schemas listed above are the only frozen, machine-checkable
contracts as of Phase 0; the persistence table list in §5 is a target
schema, not an implemented one.
