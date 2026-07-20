# Risk Model

Normative Phase 0 contract for the risk-limit schema and the correlated
scenario-risk contract. Sources: blueprint §5.9;
`.claude/rules/strategy-and-risk.md`. Machine-readable schema:
`schemas/risk-limits.schema.json`; conservative defaults:
`config/risk/conservative.yaml`.

## 1. Risk gateway contract

All trade intents pass through **one synchronous, centralized,
deterministic, versioned, non-bypassable** policy boundary. Every
decision (approve or reject, with the failing rule) is persisted in
`risk_decisions` and linked to the intent.

Checks, all of which must pass:

1. Demo environment confirmed.
2. Exchange and market active; market allowlisted.
3. Data fresh (≤ `max_market_data_age_seconds`); order book `HEALTHY`.
4. Intent not expired; price valid; count positive and within limits.
5. Per-order risk, per-market exposure, aggregate exposure, per-market
   loss, portfolio daily loss, and drawdown limits will not be exceeded.
6. Open-order count and order-rate budget available.
7. Strategy enabled; kill switch inactive.
8. Settlement-proximity restriction passes
   (≥ `min_minutes_before_close`).
9. No unresolved reconciliation incident exists.
10. Scenario checks (§3 below) pass.

Tests must prove the strategy cannot call execution directly or bypass
any rule. Changing any limit value requires durable human approval.

## 2. Risk-limit schema (v1)

| Field | Conservative default | Meaning |
| --- | --- | --- |
| `bankroll.paper_bankroll_usd` | 1000.00 | fixed paper bankroll |
| `order.max_risk_per_order_usd` | 5.00 | worst-case cost of a single order |
| `order.max_open_orders` | 10 | simultaneous resting orders |
| `market.max_exposure_per_market_usd` | 25.00 | per-market exposure cap |
| `market.min_minutes_before_close` | 30 | quoting cutoff before settlement |
| `market.max_market_data_age_seconds` | 2 | data-freshness gate |
| `portfolio.max_aggregate_exposure_usd` | 100.00 | total exposure cap |
| `portfolio.max_daily_paper_loss_usd` | 25.00 | daily stop |
| `portfolio.max_strategy_drawdown_pct` | 5.0 | strategy drawdown stop |
| `scenario.max_single_market_liability_usd` | 25.00 | worst-case outcome liability per market |
| `scenario.max_correlated_scenario_loss_usd` | 50.00 | worst reviewed scenario loss |
| `execution_budget.max_outstanding_request_age_seconds` | 10 | uncertain-request timeout |
| `execution_budget.order_rate_budget_per_minute` | 30 | mutating-request budget |

These are engineering defaults, not recommended financial limits. All
monetary values are fixed-point decimal strings.

## 3. Correlated scenario-risk contract

Nominal order cost is not a complete representation of binary-market
risk. The risk service additionally tracks, per decision:

- **Worst-case outcome liability** by contract (what is lost if the
  position settles against us).
- **Correlated exposure groups**: markets expressing the same underlying
  directional or settlement scenario (e.g. several BTC threshold markets
  over the same window) belong to one deterministic, reviewed, versioned
  correlation group (`scenario.correlation_groups_version`).
- **Scenario loss** over reviewed settlement states: for each plausible
  underlying settlement scenario *q*, `ScenarioLoss(q) = Σᵢ PnLᵢ(q)`
  across all open positions and resting orders.
- **Liquidity-adjusted exposure** (exposure scaled by exit feasibility).
- **Exposure-weighted time to close** and position-size scaling as
  settlement approaches.

Approval must reject an order that breaches single-market liability,
correlated scenario-loss, liquidity-adjusted, or settlement-proximity
limits **even when nominal exposure remains below the fixed-dollar
caps**. Scenario aggregation must be invariant to position ordering
(property-tested). Scenario snapshots are persisted in
`scenario_risk_snapshots`.

## 4. Kill switch

A deterministic runtime control that cancels managed open orders and
blocks new submissions. It is never operated by AI, and its state is
part of the risk-decision record and operator status view.
