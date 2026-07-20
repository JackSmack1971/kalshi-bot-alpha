# Strategy Specification — Passive Spread Capture

Normative Phase 0 contract. Sources: blueprint §5.8, §15;
`.claude/rules/strategy-and-risk.md`. Implementation and activation are
Phase 5 and require durable human approval; this document freezes the
contract now.

## 1. Strategy boundary

The strategy engine consumes immutable feature snapshots and emits
`TradeIntent` objects (see `docs/DATA_MODEL.md` §2). It never calls the
Kalshi API, never bypasses the risk gateway, and may operate only when
the order book is `HEALTHY` and all deterministic preconditions
(reconciliation, eligibility, data health, stream health) are confirmed.

Initial release constraints: paper only, limit orders only, one active
strategy, post-only quoting, small fixed bankroll, no leverage/margin,
no RFQs or block trades, no automatic parameter optimization during a
scored run.

## 2. Behavior (passive spread capture v0.1)

- Quote only in liquid, narrow-spread, allowlisted markets.
- Place passive **post-only** bids at or behind the best bid; never
  cross the spread.
- Limit inventory in either outcome
  (`inventory.max_inventory_per_outcome_contracts`).
- Cancel quotes when features become stale.
- Reprice only after a minimum price movement or quote age.
- Stop quoting `stop_quoting_minutes_before_close` before market close.
- Do not quote when estimated net edge < estimated fees + safety buffer.

Rationale for this strategy first: it exercises order-book accuracy,
create/cancel/fill/reconciliation paths, and execution quality without
requiring an external crypto price oracle.

## 3. Binding quote-expectancy contract

**A visible spread is not edge.** Every proposed passive quote must
persist a versioned decomposition
(`schemas/quote-expectancy.schema.json`, stored in
`quote_expectancy_records`) approximating:

```text
EV = P(fill) × (gross spread − fees − adverse selection
                − inventory cost − settlement risk)
     − cancel/reprice cost
```

Binding rules:

1. `signal_confidence`, `expected_fill_probability`, and
   `expected_net_edge` are separate quantities in separate fields —
   never one ambiguous number.
2. Every quote records its `edge_model_version`,
   `calibration_sample_size`, `calibration_confidence`, queue-state
   snapshot reference, and market archetype ID.
3. Initially the expectancy model may serve research and observability
   rather than acting as a binding order threshold — but recording the
   decomposition is mandatory from the first quote and may not be
   disabled.
4. Fill-probability estimates must be queue-aware with explicit bounds
   and calibration method (see `docs/MICROSTRUCTURE_CONTRACT.md`).

## 4. Quote lifecycle efficiency

The strategy must record: cancels per fill; reprices per fill; mutating
API requests per unit of gross and net spread; median quote lifetime;
percentage of quotes canceled before meaningful queue advancement; and
opportunity loss caused by request throttling.

## 5. Edge-claim preconditions

No passive spread-capture edge may be claimed unless the system
separates and quantifies (blueprint §15): displayed spread; fill
probability conditional on bounded queue position; fees and
mutating-request costs; immediate and delayed adverse selection;
inventory and settlement risk; external-reference lag and stale-quote
exposure; market-archetype dependence; correlated scenario exposure;
fill-model uncertainty; and statistical uncertainty with
multiple-testing disclosure. Missing coverage on any component makes the
result `INCONCLUSIVE` (see `docs/RESEARCH_PROTOCOL.md`).

## 6. Future strategies

A second strategy comparing Kalshi-implied probabilities with an
external crypto reference model is a separate, human-approved later
phase. External reference feeds remain observational until then and
carry no trading authority.
