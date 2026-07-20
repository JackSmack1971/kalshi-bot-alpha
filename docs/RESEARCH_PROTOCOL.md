# Research Protocol — Experiment Registry and Statistical Policy

Normative Phase 0 contract for the immutable experiment-registry
contract and the statistical sufficiency and multiple-testing policy.
Sources: blueprint §9, §15.2;
`.claude/rules/research-evaluation-integrity.md`.

## 1. Immutable experiment-registry contract

Before any **confirmatory** strategy analysis begins, the experiment is
registered (`schemas/experiment-registration.schema.json`, stored in
`experiment_registry`) with:

- Hypothesis and falsification criteria.
- Primary metric; secondary metrics.
- Fixed parameter grid.
- Included and excluded market archetypes.
- Training, development, and holdout windows.
- Minimum sample and diversity requirements (§3).
- Multiple-comparison correction method.
- Planned missing-data treatment.
- Frozen versions: strategy, feature, expectancy model, archetype
  classifier, fill model, and (where AI participated) agent policy,
  prompt, schema, and tool-registry versions.

**Immutability:** once the scored data window begins, the registration
record is frozen. Any change to model, prompt, schema, tool, evidence,
parameters, or windows creates a *new* experiment version; the original
is never edited (supersession links, not mutation). Mutation attempts
after freeze are test-covered failures.

Exploratory analysis is permitted but must be labeled exploratory, and
**all tested variants are retained, not only winners**. Confirmatory
evidence requires a holdout period or market set that was not used to
formulate the hypothesis.

## 2. Statistical sufficiency policy

- Report confidence intervals for fill rate, positive-markout rate, net
  edge, P&L, tail loss, cancellation efficiency, and archetype-specific
  results.
- Resampling must **cluster by market or settlement event** when
  order-level observations are not independent.
- Effective sample size must account for autocorrelation and repeated
  observations from the same market.
- Calendar duration alone is never sufficient evidence of edge; the
  sample and diversity gates below always apply.

## 3. Sample and diversity gates (promotion prerequisites)

A confirmatory evaluation is valid only when all preregistered minimums
are met:

- Minimum eligible quote opportunities.
- Minimum submitted quotes and minimum fills.
- Minimum fills per included market archetype.
- Minimum distinct settlement events.
- Minimum adverse-selection observations.
- Minimum clean restarts and reconciliations.
- Maximum unresolved data gaps.
- Minimum effective sample size after clustering and autocorrelation
  adjustment.
- Multiple crypto market types and expirations represented.

## 4. Multiple-testing policy

Every confirmatory analysis declares its correction method (e.g.
Benjamini–Hochberg or Bonferroni over the preregistered variant count)
at registration time. The full record of all tested variants —
including abandoned and negative ones — is disclosed with any reported
result. Positive aggregate results driven by one archetype, one
settlement event, or an unrealistic fill model are not accepted.

## 5. Statistical decision states

Deterministic evaluation policy assigns **exactly one** state from
versioned statistical outputs:

```text
OPERATIONALLY_INVALID    evidence integrity or accounting insufficient
ECONOMICALLY_NEGATIVE    conservative net-edge estimate is negative
INCONCLUSIVE             coverage or effective sample size insufficient
PROMISING_EXPLORATORY    positive exploratory evidence, not confirmatory
CONFIRMATORY_PASS        preregistered holdout and uncertainty gates pass
```

Missing required coverage yields `INCONCLUSIVE`, never an inferred
favorable result. The platform must be capable of producing trustworthy
*negative* evidence when no edge is present. No AI agent may assign,
promote, override, or reinterpret these states; AI may only explain
them. Numerical AI claims must originate from deterministic analysis
tools, not model arithmetic.

## 6. Fill-model hierarchy

Progressively stronger evidence, each level recorded with its
assumptions: (1) naive — fill when a trade crosses the quote; (2)
queue-aware approximation using displayed size ahead; (3) paper/live
calibration against demo fills; (4) conservative stress model adding
latency, missed fills, fees, and adverse selection. Backtest output
distinguishes signal quality, fill-model assumptions, gross P&L, fees,
slippage, net P&L, maximum drawdown, market coverage, and data gaps.
