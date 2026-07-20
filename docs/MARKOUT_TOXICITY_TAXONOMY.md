# Markout and Toxicity Taxonomy

## Realized spread (blueprint SS15.1)

For each fill, calculate signed realized spread at multiple horizons:

```text
Realized_Spread_t = s * 2 * (P_fill - M_t)
```

where `s = +1` for a sell and `s = -1` for a buy, and `M_t` is the
reference midpoint at horizon `t`. Report median, 10th and 25th
percentiles, expected shortfall, positive-markout frequency, and
segmentation by market archetype and time to close.

## Classification states

Every fill must be classified as exactly one of:

- `BENIGN`
- `TOXIC`
- `STALE_QUOTE`
- `LIFECYCLE`
- `INVENTORY_REBALANCING`
- `AMBIGUOUS`

Every classification must preserve its `rules_version` and the
`input_evidence_ids` that produced it. A classification without a
citable evidence set is not acceptable output under this policy —
`AMBIGUOUS` exists precisely so that insufficient evidence has an
honest label instead of being forced into `BENIGN` or `TOXIC`.

## Executable contract

`schemas/markout-toxicity.schema.json` fixes:

- `realized_spread_by_horizon` — an array of `{horizon_seconds,
  realized_spread}` pairs, required and non-empty, so a classification
  can never be produced from a single ad hoc horizon.
- `classification` — the closed six-value enum above.
- `input_evidence_ids` — required, non-empty, so every classification
  cites its evidence.
- `rules_version` — an independent version field from the record's own
  `schema_version`, so a change to classification rules is always
  distinguishable from a schema-shape change.

## Non-goals of this phase

No fill-classification logic exists yet. This taxonomy and schema fix
the target shape and the evidentiary bar; a later phase (blueprint
SS15.1) implements the classifier against demo fills.
