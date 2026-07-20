# Quote Expectancy Policy

## Binding contract (blueprint SS5.8 "Binding quote-expectancy contract")

A visible spread is not edge. For every proposed passive quote, the
strategy engine must persist a versioned decomposition approximating:

```text
EV = P(fill) x (gross spread - fees - adverse selection
                - inventory cost - settlement risk)
     - cancel/reprice cost
```

## The three-field separation requirement

**Signal confidence, fill confidence, and expected profitability are
separate quantities and must never share one ambiguous field.** This
is a hard structural requirement, not a style preference:

- `signal_confidence` — confidence in the underlying directional or
  microstructure signal.
- `fill_probability` — the probability this passive quote fills.
- `expected_net_edge_usd` — the fully decomposed expected value, net of
  fees, adverse selection, inventory cost, settlement risk, and
  cancel/reprice cost.

Collapsing any two of these into one field would hide whether a
strategy's apparent edge comes from genuine signal, from favorable
fill dynamics, or from an under-modeled cost term — exactly the
ambiguity this contract exists to prevent.

Initially, the expectancy model may be used for research and
observability rather than as a binding order threshold, but every
quote must still record its decomposition and model version.

## Quote lifecycle efficiency (blueprint SS5.8)

Alongside the expectancy decomposition, the strategy must record:

- Cancels per fill.
- Reprices per fill.
- Mutating API requests per unit of gross and net spread.
- Median quote lifetime.
- Percentage canceled before meaningful queue advancement.
- Opportunity loss caused by request throttling.

## Executable contract

`schemas/quote-expectancy.schema.json` fixes:

- `schema_version` and `edge_model_version` as independent version
  fields, so a schema-shape change is always distinguishable from a
  model-parameter change.
- `signal_confidence`, `fill_probability` (with
  `fill_probability_lower_bound`/`fill_probability_upper_bound`), and
  `expected_net_edge_usd` as three separate required fields (the first
  two bounded to `[0, 1]`, the third an unbounded signed fixed-point
  decimal string), satisfying blueprint Phase 0 exit criterion "Signal
  confidence, fill probability, and expected net edge are separate
  fields."
- The full cost decomposition (`gross_spread_usd`, `fee_cost_usd`,
  `adverse_selection_usd`, `inventory_cost_usd`, `settlement_risk_usd`,
  `cancel_reprice_cost_usd`) as required, fixed-point decimal string
  fields, satisfying blueprint Phase 0 exit criterion "Passive-spread
  edge is defined by a versioned expectancy decomposition."
- `intent_id`, `market_ticker`, `market_archetype_id`, and
  `queue_state_snapshot_id` as required identifiers, so every recorded
  decomposition traces to the trade intent, market, market archetype,
  and queue-state snapshot in effect at quote time (`docs/DATA_MODEL.md`
  §6 traceability invariants).
- An optional `quote_lifecycle` object for the efficiency metrics
  above.

## Non-goals of this phase

No strategy engine, no expectancy calculation, and no order-threshold
enforcement exist yet. This policy and schema fix the target shape; a
later phase (blueprint SS5.8) implements the calculation and, if
approved, promotes it from observability-only to a binding order
threshold.
