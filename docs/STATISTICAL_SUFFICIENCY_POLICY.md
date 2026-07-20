# Statistical Sufficiency and Multiple-Testing Policy

## Five decision states (blueprint SS15.2)

Every strategy evaluation concludes with exactly one of:

- `OPERATIONALLY_INVALID` — evidence integrity or accounting is
  insufficient.
- `ECONOMICALLY_NEGATIVE` — conservative net-edge estimate is
  negative.
- `INCONCLUSIVE` — coverage or effective sample size is insufficient.
- `PROMISING_EXPLORATORY` — exploratory evidence is positive but not
  confirmatory.
- `CONFIRMATORY_PASS` — preregistered holdout and uncertainty gates
  pass.

**No AI agent may promote or reinterpret these states.** They are
assigned exclusively by deterministic evaluation policy from versioned
statistical outputs. This is a hard authority boundary, not a
convention: an AI-authored summary that says a result "looks
confirmatory" does not change the assigned `decision_state`, and no
code path may accept an AI-proposed state value as authoritative.

## Sample sufficiency and clustering

Report confidence intervals for fill rate, positive-markout rate, net
edge, P&L, tail loss, cancellation efficiency, and archetype-specific
results. Resampling must cluster by market or settlement event when
order-level observations are not independent. Effective sample size
must account for autocorrelation and repeated observations from the
same market — a raw order count is not, by itself, an acceptable
sufficiency measure under this policy.

A strategy result is `INCONCLUSIVE` when any required component lacks
sufficient coverage. Profitability claims must be net of fees and
conservative queue, latency, missed-fill, and toxicity assumptions.
The platform must be capable of producing trustworthy negative
evidence when no edge is present — a design that can only produce
positive-looking results is not compliant with this policy.

## Executable contract

`schemas/statistical-sufficiency.schema.json` fixes:

- `decision_state` as the closed five-value enum above.
- `assigned_by` fixed via `const` to
  `"deterministic_evaluation_policy"`, structurally excluding any other
  value (including any AI-agent identifier) from ever populating this
  field.
- `sample_size` and `effective_sample_size` as two separate required
  fields, so raw count and autocorrelation-adjusted count are never
  conflated.
- `diversity_gate_passed` and `clustering_unit` as required fields,
  satisfying blueprint Phase 0 exit criterion "Promotion requires
  sample-size and diversity gates in addition to elapsed time."
- `confidence_intervals` as a nested object of `{low, high}` interval
  pairs for the named metrics.

## Non-goals of this phase

No evaluation-policy implementation, no confidence-interval
calculation, and no promotion workflow exist yet. This policy and
schema fix the target shape and the authority boundary that a later
phase (blueprint SS13 "Evaluation protocol") must implement.
