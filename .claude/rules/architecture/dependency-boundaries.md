---
paths:
  - "src/market_data/**/*.py"
  - "src/features/**/*.py"
  - "src/strategies/**/*.py"
  - "src/risk/**/*.py"
  - "src/execution/**/*.py"
  - "src/portfolio/**/*.py"
  - "src/persistence/**/*.py"
  - "src/reconciliation/**/*.py"
  - "src/agents/**/*.py"
  - "src/openrouter/**/*.py"
  - "src/agent_tools/**/*.py"
  - "tests/architecture/**/*.py"
  - "tests/contract/**/*.py"
---

# Dependency and authority boundaries

Preserve one-way ownership:

- `market_data` produces normalized, quality-scored market state.
- `features` consumes immutable market state and emits immutable feature snapshots.
- `strategies` consumes immutable features and emits non-authoritative trade intents.
- `risk` consumes intents and authoritative state and emits approved or rejected decisions.
- `execution` accepts only risk-approved order plans.
- `portfolio` and `persistence` record exchange-evidenced transitions.
- `reconciliation` compares local and exchange state and suspends trading on unresolved differences.
- `agents`, `openrouter`, and `agent_tools` consume sanitized immutable evidence only.

Forbidden reachability:

- Trading-runtime packages must not depend on agent packages.
- `strategies` must not import Kalshi clients or execution services.
- `risk` must not call exchange transports.
- Agent packages must not import execution transports, ledger mutation APIs, active-configuration writers, secret loaders, or unrestricted database sessions.
- Agent tools must not expose generic Kalshi API access, arbitrary SQL, arbitrary shell, or raw filesystem traversal.
- Shared domain models must not carry clients, callbacks, credentials, service handles, or mutation capabilities.

When a dependency would violate these boundaries, introduce a narrow immutable interface or sanitized evidence projection rather than bypassing the boundary. Add architecture tests for forbidden imports and capability reachability.
