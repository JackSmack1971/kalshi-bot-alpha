# Queue-State and Calibration Policy

## Queue position as a first-class research object (blueprint SS5.6)

Queue position is a first-class research object for every passive
order, not a derived afterthought. For each order, the model must
capture:

- Displayed size ahead at submission.
- Same-price displayed size and subsequent changes.
- Trades executed at the level.
- Estimated cancellations ahead.
- Time spent at each queue estimate.
- Estimated queue advancement.
- Queue percentile or bounded queue-position interval.
- Fill probability conditional on queue state, market archetype, and
  time to close.

## Queue-completion ratio

```text
QCR = estimated volume consumed ahead / displayed size ahead at entry
```

## Bounded-interval requirement

Because exchange data may not identify individual queue priority,
every queue-position estimate must include a lower bound, an upper
bound, its assumptions, and a versioned calibration method — never a
single point estimate presented as exact. The lower bound must never
exceed the upper bound (a property-based invariant for the phase that
implements queue estimation; not itself expressible as a JSON Schema
constraint, and therefore documented here as a binding invariant on
the implementation).

## Executable contract

`schemas/queue-calibration.schema.json` fixes:

- `calibration_method_version` as a required, independently versioned
  field from the record's own `schema_version`.
- `queue_position_lower_bound` and `queue_position_upper_bound` as two
  separate required fields (each bounded to `[0, 1]`), rather than one
  point estimate — the ordering invariant between them is an
  application-level property test obligation for the implementing
  phase, documented in this schema's description and here.
- `fill_probability_conditional`, `estimated_cancellations_ahead`,
  `displayed_size_ahead_at_submission`, and an optional
  `same_price_displayed_size_history` time series.

## Fill-model hierarchy (blueprint SS12 "Fill-model hierarchy")

Use progressively stronger evidence:

1. **Naive model** — fill at quoted price when a trade crosses it.
2. **Queue-aware approximation** — account for displayed size ahead.
3. **Paper/live comparison** — calibrate assumptions using demo fills.
4. **Conservative stress model** — add latency, missed fills, fees,
   and adverse selection.

Backtest output must distinguish signal quality, fill-model
assumptions, gross P&L, fees, slippage, net P&L, maximum drawdown,
market coverage, and data gaps. A backtest that reports only net P&L
without this decomposition does not satisfy this policy.

## Non-goals of this phase

No order-book builder, no queue-position estimator, and no fill model
exist yet. This policy and schema fix the target shape and evidentiary
bar; a later phase (blueprint SS5.6) implements the estimator.
