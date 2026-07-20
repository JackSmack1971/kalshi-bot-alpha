# Failure Taxonomy

Normative Phase 0 contract. Sources: blueprint §5.10, §5.13, §7;
`.claude/rules/runtime-lifecycle.md`. Every runtime incident is
classified, persisted in `runtime_incidents`, and handled fail-closed:
explicit failure over silent degradation, always.

## 1. Incident classes

Deterministic classification used by runtime and (later) the AI
incident workflow:

```text
SYSTEM_ANOMALY                  process, clock, resource, or dependency failure
DATA_PIPELINE_ANOMALY           stale streams, sequence gaps, malformed events
MARKET_MICROSTRUCTURE_ANOMALY   book inconsistency, complementarity violations
EXECUTION_ANOMALY               unknown outcomes, duplicate commands, slow cancels
ACCOUNTING_ANOMALY              ledger/reconciliation mismatch, impossible state
STRATEGY_BEHAVIOR_ANOMALY       intents violating declared strategy contract
```

AI may analyze incidents; it can never mark one `RESOLVED`.

## 2. Category mapping and Phase 0 status

Each failure mode in §3 maps onto one or more of the following
cross-cutting categories. All categories are **contract-only in Phase
0**: no runtime, transport, strategy, risk gateway, execution engine,
reconciliation service, or agent workflow exists yet to raise any of
these incidents (see `docs/IMPLEMENTATION_STATUS.md`). The only
executable check today is the static demo-endpoint scan
(`scripts/verify_demo_only.py`), which is a safety-policy-violation
check, not an incident-taxonomy runtime.

| Category | Failure modes in §3 |
| --- | --- |
| Validation | Malformed/impossible order-state transitions (`IMPOSSIBLE_STATE`); schema/structured-output validation failures under "OpenRouter or agent failure" |
| Configuration | Authentication failure (malformed/unsafe credentials); demo-endpoint / environment-mode misconfiguration (`docs/SAFETY_MODEL.md` §1) |
| Data freshness | WebSocket disconnect (stale books); subscription overflow |
| Transport | Rate limiting; WebSocket disconnect and reconnect handling |
| Execution uncertainty | Uncertain mutation outcome (`OUTCOME_UNKNOWN`); duplicate or slow cancels |
| Reconciliation | Reconciliation mismatch (`TRADING_SUSPENDED_RECONCILIATION_REQUIRED`) |
| Accounting | Ledger mismatch requiring `ADJUSTMENT_RECONCILED`; database failure during ledger flush |
| Research integrity | OpenRouter/agent failure (budget, schema, fallback invalidation); preregistration and multiple-testing violations (`docs/RESEARCH_PROTOCOL.md` §4) |
| Safety-policy violation | Agent policy or privacy violation; demo-endpoint or credential-boundary violation (`docs/SAFETY_MODEL.md`) |

This mapping is descriptive, not a second incident-class enumeration:
the six `SYSTEM_ANOMALY`…`STRATEGY_BEHAVIOR_ANOMALY` classes in §1
remain the authoritative machine-facing taxonomy: `runtime_incidents`
records one of those six values, never a category name from this
table.

## 3. Failure modes and required responses

### WebSocket disconnect
Mark all streamed books stale immediately → suspend new orders → apply
configured disconnect policy to resting orders → reconnect with bounded
exponential backoff → fetch fresh snapshots → rebuild books → reconcile
account state → resume only when every selected market is `HEALTHY`.

### Subscription overflow
Suspend strategy → record incident → reduce active market count →
reconnect and resnapshot → alert operator. Never discard events and
continue with a potentially corrupt book.

### Rate limiting
All request budgeting is centralized. Honor server retry guidance;
apply jittered backoff; prioritize cancellations and reconciliation over
discovery; reduce scanning frequency before sacrificing order safety.
**Never retry a mutating call blindly.**

### Uncertain mutation outcome
A timeout after transmission does not mean failure. Mark the command
`OUTCOME_UNKNOWN` → stop strategy actions for that market → query orders
by `client_order_id` → reconcile exchange state → resume only after a
deterministic result.

### Reconciliation mismatch
Any mismatch between local and exchange open orders, fills, positions,
or balance puts the runtime into
`TRADING_SUSPENDED_RECONCILIATION_REQUIRED`. Ledger state is never
silently "fixed"; an explicit `ADJUSTMENT_RECONCILED` entry with
exchange evidence and durable human approval is required.

### Database failure
Stop new submissions → attempt to cancel managed open orders → retain
in-memory incident evidence only long enough for safe shutdown → exit
with critical incident status.

### Authentication failure
Do not retry invalid credentials repeatedly → suspend all operations →
redact credential material from all output → require operator
intervention.

### Market pause or close
Cancel applicable orders → stop strategy evaluation for that market →
preserve positions for settlement tracking → record the lifecycle
transition. Use `cancel_order_on_pause` where supported.

### OpenRouter or agent failure
Mark the analysis workflow failed/degraded. Never block deterministic
trading safety functions. Respect request/token/cost/wall-clock budgets;
record requested vs. actual model metadata; invalidate authoritative
output after unapproved fallback or schema failure; preserve the
evidence bundle for deterministic rerun; require human review of
incomplete analyses.

### Agent policy or privacy violation
Stop the workflow immediately → record a policy incident **without
storing the detected secret material** → revoke the result's binding
status → never broaden tools or evidence to complete the request →
require operator review before re-execution.

## 4. Shutdown contract

1. Disable new strategy intents.
2. Cancel managed open orders.
3. Await acknowledgements within a bounded timeout.
4. Reconcile open orders and positions.
5. Flush ledger and metrics; persist final strategy-run state.
6. Close WebSocket and REST clients.
7. **Exit nonzero when clean reconciliation was not achieved**, leaving
   persistent state that blocks the next startup until resolved.

See `docs/PAPER_TRADING_PROTOCOL.md` for how this sequence fits into
the full startup/decision-cycle/shutdown lifecycle.

## Governing principle across every failure mode

Deterministic trading safety functions (cancellation, reconciliation,
risk enforcement, persistence, shutdown) must never be blocked by an
AI or OpenRouter failure. Conversely, no failure-handling path may
silently continue with degraded, stale, or assumed-correct state; every
response in §3 either halts the affected function explicitly or
records an incident — never both nothing and neither.
