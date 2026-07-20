---
paths:
  - "src/runtime/**/*.py"
  - "src/execution/**/*.py"
  - "src/reconciliation/**/*.py"
  - "src/portfolio/**/*.py"
  - "src/persistence/**/*.py"
  - "src/market_data/**/*.py"
  - "tests/runtime/**/*.py"
  - "tests/execution/**/*.py"
  - "tests/reconciliation/**/*.py"
  - "tests/integration/**/*.py"
---

# Runtime lifecycle and fail-closed behavior

Preserve startup order:

1. Load configuration.
2. Validate demo-only policy.
3. Initialize structured logging.
4. Open the database and run safe schema checks.
5. Load credentials from an approved source.
6. Verify clock health.
7. Query exchange status.
8. Reconcile account, positions, fills, and open orders.
9. Discover eligible markets.
10. Fetch initial snapshots.
11. Connect to the demo WebSocket.
12. Subscribe to approved channels.
13. Confirm stream health.
14. Enable strategy evaluation.
15. Enter the evaluation loop.

Never enable strategy evaluation before reconciliation, market eligibility, data quality, and stream health are confirmed.

Shutdown order:

1. Disable new intents.
2. Cancel managed open orders.
3. Wait for bounded acknowledgements.
4. Reconcile orders and positions.
5. Flush ledger, persistence, and metrics.
6. Persist final run state.
7. Close transports.
8. Exit nonzero if clean reconciliation was not achieved.

Refuse startup or suspend operation when applicable for non-demo endpoints, ambiguous mode, invalid credentials for authenticated connectivity, excessive clock drift, unresolved prior shutdown or reconciliation, ineligible markets, unhealthy books, bypassed gateways, uncertain order outcomes, unsafe persistence failure, or active kill switch.

Scope AI failures to the affected AI workflow. AI failure must never disable deterministic cancellation, reconciliation, accounting, persistence, risk enforcement, or shutdown.
