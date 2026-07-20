# Correlated Scenario-Risk Policy

## Beyond nominal exposure (blueprint SS5.9 "Probability- and scenario-aware risk")

Nominal order cost is not a complete representation of binary-market
risk. The risk gateway must additionally track:

- Worst-case outcome liability by contract.
- Correlated exposure groups across markets expressing the same
  underlying directional or settlement scenario.
- Scenario loss over reviewed settlement states.
- Liquidity-adjusted exposure.
- Exposure-weighted time to close.
- Position-size scaling as settlement approaches.

## Scenario loss

For plausible underlying settlement scenarios `q`:

```text
Scenario_Loss(q) = sum_i PnL_i(q)
```

Risk approval must reject orders that breach single-market liability,
correlated scenario-loss, liquidity-adjusted, or settlement-proximity
limits **even when nominal exposure remains below the fixed-dollar
cap**. A nominal-cap-only risk gateway is explicitly insufficient
under this policy: it can approve an order that is individually small
but that, combined with existing correlated positions, produces an
unacceptable loss under a single plausible settlement scenario.

Correlation groups and scenarios must be deterministic, reviewed, and
versioned — never inferred ad hoc at approval time.

## Executable contract

`schemas/risk-limits.schema.json` fixes a `scenario` object with:

- `correlation_groups_version` — a version pointer to the deterministic,
  reviewed, externally-maintained correlation-group definitions; `null`
  only while no strategy is active, and must be frozen before Phase 5
  activation.
- `max_correlated_scenario_loss_usd` — worst reviewed scenario loss
  limit.
- `max_single_market_liability_usd` — worst-case outcome liability per
  market.

Correlation groups themselves (member `market_tickers` and their
scenario-loss limits) are not embedded in the risk-limit configuration
schema: they are a separately reviewed and versioned artifact
referenced by `correlation_groups_version`, consistent with
"Correlation groups and scenarios must be deterministic, reviewed, and
versioned — never inferred ad hoc at approval time." This is shape
only: no numeric limit values are presented as production-ready
defaults (see `docs/adr/0001-phase-0-contracts-and-safety-model.md`).

## Non-goals of this phase

No risk gateway, no scenario-loss calculator, and no correlation-group
definitions exist yet. This policy and the `risk-limits.schema.json`
shape fix the target contract; a later phase (blueprint §5.9)
implements the deterministic, versioned scenario-risk engine and its
reviewed correlation groups.
