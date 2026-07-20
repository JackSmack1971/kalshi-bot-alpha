---
paths:
  - "src/**/kalshi/**/*.py"
  - "src/**/transport/**/*.py"
  - "src/**/client/**/*.py"
  - "src/**/configuration/**/*.py"
  - "src/**/config/**/*.py"
  - "tests/**/*kalshi*.py"
  - "tests/**/*endpoint*.py"
  - "tests/**/*transport*.py"
---

# Kalshi transport safety

- Permit only `https://external-api.demo.kalshi.co/trade-api/v2` and `wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2`.
- Reject non-demo hostnames in configuration, environment-derived settings, persisted runtime state, constructed URLs, redirects, and generated variants.
- Do not implement `environment=production`, dormant production constants, or a generic `KalshiClient(environment)` abstraction.
- Prefer demo-specific transport types such as `KalshiDemoRestClient` and `KalshiDemoWebSocketClient`.
- Keep `DEMO MODE` explicit in operator-visible status.
- Static and property tests must prove production hostnames are rejected across configuration variants.
- Mutating calls require unique `client_order_id` values and idempotent recovery.
- An uncertain mutation outcome must become `OUTCOME_UNKNOWN`; suspend the affected market, query by `client_order_id`, reconcile exchange state, and resume only after a deterministic result.
- Never retry a mutating request blindly.
- Acceptance tests that place or cancel demo orders must be explicitly opt-in and must fail before transport creation if endpoint validation is not demo-only.
