# Market Archetype Policy

## Rationale (blueprint SS5.5.1)

"Crypto market" alone is not an analytically sufficient category.
Every eligible market must receive a versioned `market_archetype_id`
so that strategy performance, risk exposure, and research findings can
be segmented rather than pooled into an uninformative aggregate.

## Required classification dimensions

At minimum, an archetype classifies a market by:

- Underlying asset.
- Contract structure — directional, threshold, range, or another
  reviewed type.
- Strike or threshold distance (omitted only when not applicable to
  the contract structure).
- Time-to-settlement bucket.
- Market age.
- Time-of-day and day-of-week bucket.
- Spread regime.
- Visible-depth regime.
- External-reference volatility regime.
- Whether the market is event-driven versus routine.

## Determinism and versioning

The classifier must be deterministic and versioned. Every feature
snapshot, strategy intent, order, fill, and evaluation record must
preserve the `market_archetype_id` and `classifier_version` used at decision
time. Reporting must segment results by archetype before presenting
aggregate performance — an aggregate-only report is not acceptable
evidence of strategy performance under this policy.

## Executable contract

`schemas/market-archetype.schema.json` fixes:

- `market_archetype_id` — a deterministic identifier stable for
  identical classifier inputs and `classifier_version`.
- `classifier_version` — a required, independent version field from
  `market_archetype_id` itself, so a classifier change is always
  distinguishable from an archetype change for the same market.
- `contract_structure` — a closed enum
  (`directional`, `threshold`, `range`, `other_reviewed`) rather than a
  free-text field, so "other" categories require an explicit reviewed
  addition to the enum rather than silent proliferation of ad hoc
  strings.
- `day_of_week_bucket` — a closed enum (`MON`…`SUN`) rather than a
  free-text bucket, for the same determinism reason.
- Every other required classification dimension listed above.

## Non-goals of this phase

No classifier implementation exists yet. This policy and schema fix
the target shape; a later phase (blueprint SS5.5.1, alongside the
market catalog of SS5.5) implements the deterministic classification
logic against this contract.
