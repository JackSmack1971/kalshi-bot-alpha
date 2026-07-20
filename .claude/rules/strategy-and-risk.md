---
paths:
  - "src/strategies/**/*.py"
  - "src/risk/**/*.py"
  - "src/features/**/*.py"
  - "src/orders/**/*.py"
  - "tests/strategies/**/*.py"
  - "tests/risk/**/*.py"
  - "tests/features/**/*.py"
---

# Strategy and deterministic risk

Initial-release constraints: paper only, limit orders only, one active strategy, small fixed bankroll, no leverage, no margin, no RFQ or block trading, no automatic live parameter optimization, and no trading on stale, uncertain, incomplete, or unresolved state.

A visible spread is not edge. Every passive quote must preserve a versioned expectancy decomposition covering fill probability, gross spread, fees, adverse selection, inventory cost, settlement risk, cancellation or repricing cost, expected net edge, calibration coverage and confidence, queue-state evidence, market archetype, and evidence snapshot.

Keep signal confidence, fill probability, and expected profitability as distinct fields.

Risk approval must consider per-order and per-market limits, aggregate exposure, worst-case binary liability, correlated settlement scenarios, liquidity-adjusted exposure, time to close, drawdown and loss limits, open-order and request budgets, reconciliation state, and market/data health.

Risk policy must remain synchronous, centralized, deterministic, versioned, and non-bypassable. Tests must prove strategy cannot call execution directly or bypass risk.
