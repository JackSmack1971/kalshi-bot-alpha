---
paths:
  - "src/domain/**/*.py"
  - "src/orders/**/*.py"
  - "src/portfolio/**/*.py"
  - "src/ledger/**/*.py"
  - "src/accounting/**/*.py"
  - "src/persistence/**/*.py"
  - "src/reconciliation/**/*.py"
  - "tests/domain/**/*.py"
  - "tests/ledger/**/*.py"
  - "tests/accounting/**/*.py"
  - "tests/portfolio/**/*.py"
---

# Domain, ledger, and accounting rules

- Use exact fixed-point or decimal price types; never binary floating point for exchange prices.
- Prefer immutable Pydantic domain models where practical.
- Preserve source and calculation timestamps, event ranges, version IDs, hashes, quality states, and provenance.
- Every submitted order must trace to one strategy intent, one feature snapshot, one risk decision, and one unique `client_order_id`.
- Every fill must trace to an exchange order.
- Every position and cash change must trace to append-only ledger events.
- Derived balances and P&L must be reproducible from ledger events.
- Drive state transitions from exchange evidence, never assumptions.
- Never silently repair reconciliation discrepancies.
- Adjustments require explicit evidence and durable human approval.
- Preserve idempotency for create, cancel, fill ingestion, reconciliation, and ledger recording.
- Add tests for fixed-point behavior, transition legality, provenance continuity, replay reproducibility, duplicate evidence, and reconciliation suspension.
