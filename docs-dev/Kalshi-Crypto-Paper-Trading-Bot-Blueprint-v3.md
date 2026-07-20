# Kalshi Crypto Paper-Trading Bot Blueprint — Version 3

> **Version 3 scope:** Preserves the deterministic, demo-only architecture and OpenRouter-exclusive AI control plane, while adding a binding market-microstructure research contract covering queue position, expectancy decomposition, adverse selection, external-reference observation, scenario-aware risk, market archetypes, and statistical sufficiency. AI agents may observe, investigate, challenge, explain, and propose. Deterministic code must calculate, authorize, execute, reconcile, and account. Humans must approve strategy, risk, market-eligibility, and promotion changes.

## 1. Product Definition

### Objective

Build a reliable, auditable bot that:

1.  Discovers eligible Kalshi crypto prediction markets.
2.  Consumes real-time market and order-book data.
3.  Evaluates one or more deterministic strategies.
4.  Places and manages orders exclusively in Kalshi’s demo environment.
5.  Tracks simulated positions, fills, fees, exposure, and performance.
6.  Prevents any accidental production trading.
7.  Produces sufficient evidence to evaluate whether a strategy is
    suitable for later human-reviewed development.

### Initial operating boundary

The first release is:

- Crypto markets only.
- Kalshi demo environment only.
- One strategy active at a time.
- Limit orders only.
- Small fixed paper bankroll.
- No leverage or margin features.
- No RFQs, block trades, multivariate market creation, or FCM endpoints.
- No production trading mode.
- No automatic transition from paper to live trading.
- No AI-generated discretionary trade decisions in the execution path.
- OpenRouter is the exclusive external provider for all LLM inference.
- AI-agent operation is optional and must not be required for safe trading, cancellation, reconciliation, accounting, or shutdown.
- AI agents run outside the deterministic order-decision and execution path.
- External crypto reference feeds are observational inputs only; they cannot bypass the deterministic strategy and risk boundaries.
- Every passive quote must be attributable to a versioned expectancy model, queue-state estimate, market archetype, and evidence snapshot.
- Calendar duration alone is never sufficient evidence of strategy edge; minimum sample and diversity gates also apply.

### Non-goals

The MVP will not:

- Guarantee profitability.
- Predict cryptocurrency spot prices directly.
- Trade on external exchanges.
- Hold production Kalshi credentials.
- Automatically optimize strategy parameters during a live paper
  session.
- Place orders when market state, local state, or data freshness is
  uncertain.
- Treat backtest performance as evidence of live profitability.
- Allow an AI model to emit an executable trade intent, approve risk, submit or cancel orders, alter ledger state, resolve reconciliation discrepancies, or activate configuration.
- Give the AI-agent process access to Kalshi credentials, raw authentication material, or unrestricted shell/SQL tools.
- Automatically promote an AI proposal into an active strategy or risk policy.
- Treat displayed spread as synonymous with collectible edge.
- Infer queue priority, fill probability, or adverse-selection cost without recording the assumptions and calibration evidence.
- Use external exchange data as direct trading authority in the passive-spread MVP.
- Collapse operational quality, execution quality, strategy economics, and risk concentration into one composite score during research.

# 2. Safety Architecture

## 2.1 Demo-only enforcement

The application must contain a compile-time or startup policy that
permits only:

- REST: `https://external-api.demo.kalshi.co/trade-api/v2`
- WebSocket: `wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2`

The official WebSocket documentation identifies the demo WebSocket
endpoint separately from production.

### Required fail-closed controls

The bot must refuse to start when:

- A configured host is not on the demo allowlist.
- A production hostname appears anywhere in runtime configuration.
- Credentials are absent, malformed, or sourced from an unsafe location.
- Environment mode is unset or ambiguous.
- System time drift exceeds the configured authentication tolerance.
- A strategy attempts to bypass the central execution gateway.
- Persistent state indicates an unresolved prior shutdown or
  reconciliation failure.

### Production isolation

Do not implement a generic `environment=production` switch in the MVP.

Use a demo-specific transport implementation such as:

    KalshiDemoRestClient
    KalshiDemoWebSocketClient

Do not use:

    KalshiClient(environment)

This makes accidental production enablement require an explicit
architectural change rather than a configuration typo.

## 2.2 Credential handling

Use:

- Environment variables or an operating-system secret store.
- A demo-only API key.
- A local private key file outside the repository.
- File permissions restricted to the current user.
- Redaction of access key identifiers and signatures from logs.

Never:

- Commit keys.
- Paste keys into prompts.
- Store keys in strategy configuration.
- Return signatures in error telemetry.
- Expose credentials through a dashboard or frontend process.

Kalshi authenticated requests require an access-key ID, RSA-PSS request
signature, and millisecond timestamp.

## 2.3 AI authority and isolation boundary

The AI subsystem is a separate research and operations control plane. It is not part of the trading authority chain.

Binding separation:

```text
AI may observe, investigate, challenge, explain, and propose.

Deterministic code must calculate, authorize, execute, reconcile, and account.

Humans must approve strategy, risk, market-eligibility, and promotion changes.
```

AI agents must never:

- Produce objects accepted by the runtime as executable `TradeIntent` instances.
- Approve or bypass a risk decision.
- Call order-create, order-cancel, reconciliation-resolution, ledger-write, or strategy-activation functions.
- Modify active configuration during a strategy run.
- Add markets to the active allowlist.
- Mark incidents or reconciliation discrepancies resolved.
- Access Kalshi API credentials, private keys, signatures, or raw authentication headers.
- Execute arbitrary shell commands or arbitrary SQL.

The safest initial deployment uses process-level credential separation:

```text
paper-trader process:
  KALSHI_DEMO_ACCESS_KEY
  KALSHI_DEMO_PRIVATE_KEY_PATH
  no OPENROUTER_API_KEY required

agent-control-plane process:
  OPENROUTER_API_KEY
  no Kalshi credentials
  read-only sanitized evidence access
```

If process separation is temporarily unavailable, equivalent operating-system and application-level controls must prove that the agent runtime cannot read Kalshi secrets or invoke execution capabilities.

### Fail-closed AI controls

The agent subsystem must refuse a request when:

- The requested tool is not explicitly registered for that agent role.
- Evidence scope is missing or exceeds the job authorization.
- Prompt egress scanning detects credentials, signatures, private-key material, raw environment dumps, or prohibited personal data.
- The selected model lacks required structured-output or tool-calling capabilities.
- An authoritative workflow would silently fall back to an unapproved model.
- A response fails schema validation or cites unknown evidence identifiers.
- Cost, token, request, or tool-call budgets are exceeded.
- The workflow attempts to change active trading state.

OpenRouter failure must degrade only AI analysis. It must never prevent safe cancellation, reconciliation, risk enforcement, persistence, or shutdown.

# 3. Recommended Technology Stack

## Runtime

- Python 3.12+
- `asyncio`
- `httpx` for REST
- `websockets` for streaming
- Pydantic v2 for validated domain models
- SQLAlchemy 2.x or SQLModel
- SQLite for the MVP
- Alembic for schema migrations
- Typer for the command-line interface
- Structlog or standard JSON logging
- An application-owned asynchronous OpenRouter client using `httpx`
- JSON Schema-constrained agent outputs validated with Pydantic
- A typed, least-privilege agent tool gateway
- Pytest, pytest-asyncio, Hypothesis, and respx
- Ruff, mypy, and Bandit

## Why Python

Python is appropriate because the bot needs:

- Fast iteration.
- Strong async networking support.
- Straightforward quantitative analysis.
- Mature testing libraries.
- Easy use from Claude Code.
- A clean path from an MVP to later research and backtesting.

## Deployment shape

The first version should be a single local process with internally
separated modules, not microservices.

    CLI / Supervisor
          |
          v
    Application Runtime
      ├── Market Data
      ├── Strategy
      ├── Risk
      ├── Execution
      ├── Portfolio
      ├── Persistence
      └── Observability

A single process avoids distributed-state complexity while preserving
boundaries that can later become separate services.

## AI deployment shape

The trading runtime remains a single deterministic local process. The agent control plane should begin as a separate local process that consumes immutable, sanitized evidence bundles.

```text
Deterministic Trading Runtime
        |
        +--> immutable evidence exporter
                    |
                    v
             Agent Evidence Store
                    |
                    v
              AI Supervisor
        +-----------+-----------+----------------+
        |           |           |                |
 Operations   Strategy     Risk Critic     Evaluation
 Analyst      Researcher                   Reporter
        |           |           |                |
        +-----------+-----------+----------------+
                    |
                    v
          OpenRouter Gateway Only
```

This arrangement prevents model availability, latency, hallucination, or tool failure from entering the execution-critical path.

# 4. Logical Architecture

                      +----------------------+
                      | Kalshi Demo REST API |
                      +----------+-----------+
                                 |
                snapshots, markets, account state
                                 |
                                 v
    +-------------+      +-------+---------+      +------------------+
    | Scheduler / |----->| Market Catalog  |----->| Market Selector  |
    | Supervisor  |      +-----------------+      +--------+---------+
    +------+------+                                      |
           |                                             v
           |                                 +-----------+----------+
           |                                 | Active Market Set    |
           |                                 +-----------+----------+
           |                                             |
           v                                             v
    +------+----------------+                 +----------+-----------+
    | Kalshi Demo WebSocket |---------------> | Order-Book Builder  |
    +-----------------------+                 +----------+-----------+
                                                       |
                                                       v
                                             +---------+----------+
                                             | Feature Engine     |
                                             +---------+----------+
                                                       |
                                                       v
                                             +---------+----------+
                                             | Strategy Engine    |
                                             +---------+----------+
                                                       |
                                                Trade Intent
                                                       |
                                                       v
                                             +---------+----------+
                                             | Risk Gateway       |
                                             +---------+----------+
                                                       |
                                               Approved Order Plan
                                                       |
                                                       v
                                             +---------+----------+
                                             | Execution Engine   |
                                             +---------+----------+
                                                       |
                                    create/cancel/reconcile orders
                                                       |
                                                       v
                                             +---------+----------+
                                             | Order State Machine|
                                             +---------+----------+
                                                       |
                                  fills, positions, cash, realized P&L
                                                       |
                                                       v
                                             +---------+----------+
                                             | Portfolio Ledger   |
                                             +--------------------+

## 4.1 AI control-plane architecture

```text
Human Operator
      |
      v
Agent Supervisor
      |
      +--> Operations and Incident Analyst
      +--> Strategy Researcher
      +--> Risk and Adversarial Reviewer
      +--> Evaluation and Reporting Agent
      +--> Test Designer (later phase)
      |
      v
Evidence and Tool Gateway
      |
      +--> read sanitized database views
      +--> inspect immutable evidence bundles
      +--> run deterministic replay and statistics
      +--> create proposal/report artifacts
      |
      X--> no Kalshi transport tools
      X--> no order or cancellation tools
      X--> no active configuration writes
      X--> no credential access
```

The original trading data flow remains authoritative:

```text
immutable features
  -> deterministic strategy
  -> trade intent
  -> deterministic risk gateway
  -> deterministic execution
```

No AI response can be deserialized into the authoritative strategy intent type. Agent proposal schemas must use distinct types, namespaces, storage locations, and validation paths.

# 5. Core Components

## 5.1 Configuration and policy layer

Responsibilities:

- Load application settings.
- Validate demo endpoints.
- Load risk limits.
- Select strategy.
- Define eligible crypto series or ticker patterns.
- Establish database and logging paths.
- Enforce immutable runtime mode.

Example configuration domains:

    environment
    credentials
    market_selection
    market_data
    strategy
    risk
    execution
    persistence
    observability
external_reference
market_archetypes
expectancy_model
experiment_registry

Sensitive values must be references to environment variables, never
literal values in configuration files.

## 5.2 Authentication signer

Responsibilities:

- Generate millisecond timestamps.
- Construct the canonical message to sign.
- Produce RSA-PSS signatures.
- Add the three Kalshi authentication headers.
- Redact sensitive material from exceptions.
- Reject timestamps outside policy.

The WebSocket signing payload follows:

    timestamp + "GET" + "/trade-api/ws/v2"

Expose a narrow interface:

    sign(method, path_without_query) -> AuthHeaders

The signer must not know about strategies, positions, or business logic.

## 5.3 REST gateway

Responsibilities:

- Market and series discovery.
- Exchange-status checks.
- Initial order-book snapshots.
- Order creation.
- Order cancellation.
- Open-order reconciliation.
- Fill and position reconciliation.
- Rate-limit handling.
- Typed error conversion.

Every mutating call must:

1.  Carry a unique `client_order_id`.
2.  Be idempotently recorded before transmission.
3.  Record request intent without secrets.
4.  Persist the response.
5.  Trigger reconciliation after uncertain outcomes.

The documented order endpoint accepts a ticker, client order ID, side,
contract count, price, time in force, self-trade prevention, post-only
status, and related controls.

The response includes the exchange order ID, client order ID, filled
count, remaining count, and timestamp.

## 5.4 WebSocket gateway

Responsibilities:

- Establish the authenticated demo connection.
- Subscribe to selected channels.
- Track subscription IDs.
- Decode typed messages.
- Reconnect with bounded exponential backoff.
- Detect stale streams and sequence gaps.
- Request fresh snapshots after reconnecting.
- Send normalized events to the internal event bus.

Kalshi’s WebSocket stream can provide order-book changes, trades,
market-status updates, and fill notifications.

Initial channel set:

- `ticker`
- `trade`
- `orderbook_delta`
- `fill`
- `market_positions`
- `market_lifecycle_v2`

Subscriptions can be restricted to selected market tickers.

The connection manager must implement reconnect behavior with
exponential backoff, as recommended in the official lifecycle guidance.

## 5.5 Market catalog

Responsibilities:

- Retrieve open crypto-related series, events, and markets.
- Normalize market metadata.
- Filter out closed, settled, paused, malformed, or unsupported markets.
- Record settlement rules and close times.
- Maintain a durable market registry.
- Detect ticker or metadata changes.

Suggested eligibility rules:

    market status is active
    crypto category or approved series
    close time exceeds minimum remaining duration
    order book exists
    spread does not exceed configured maximum
    minimum visible depth is present
    market is not paused
    settlement terms are understood

Do not identify crypto markets solely through keyword matching. Prefer
an explicit allowlist of approved series, with a reviewed fallback
classifier.

## 5.5.1 Market archetype classifier

Every eligible market must receive a versioned `market_archetype_id`. “Crypto market” alone is not an analytically sufficient category.

At minimum, classify by:

- Underlying asset.
- Contract structure, including directional, threshold, range, or other reviewed type.
- Strike or threshold distance.
- Time-to-settlement bucket.
- Market age.
- Time-of-day and day-of-week bucket.
- Spread regime.
- Visible-depth regime.
- External-reference volatility regime.
- Event-driven versus routine market.

The classifier must be deterministic and versioned. Every feature snapshot, strategy intent, order, fill, and evaluation record must preserve the archetype ID used at decision time. Reporting must segment results by archetype before presenting aggregate performance.

## 5.6 Order-book builder

Bootstrap each selected market using a REST snapshot, then apply
WebSocket deltas.

The REST order-book endpoint returns fixed-point YES and NO price levels
and allows configurable depth from the full book through 100 levels.

Maintain:

    market_ticker
    snapshot_timestamp
    last_update_timestamp
    sequence/version metadata
    yes bids
    no bids
    derived asks
    best bid
    best ask
    spread
    midpoint
    depth by level
    data quality state

### Data-quality states

    INITIALIZING
    HEALTHY
    STALE
    GAP_DETECTED
    RESYNCING
    UNAVAILABLE

Strategies may operate only when the order book is `HEALTHY`.

### Complementary-price consistency

Track YES/NO complementarity explicitly rather than assuming perfect equivalence. Record:

- Complementarity residual.
- Cross-side implied spread.
- Best executable synthetic probability.
- Duration of any inconsistency.
- Data-quality state during the inconsistency.
- Whether the apparent opportunity survives fees, latency, and queue assumptions.

Temporary inconsistencies must be classified as data artifact, thin-book effect, unconfirmed opportunity, or unresolved anomaly. An apparent cross-side arbitrage must not be treated as executable edge without deterministic validation.

### Queue-state model

Queue position is a first-class research object for every passive order. Capture:

- Displayed size ahead at submission.
- Same-price displayed size and subsequent changes.
- Trades executed at the level.
- Estimated cancellations ahead.
- Time spent at each queue estimate.
- Estimated queue advancement.
- Queue percentile or bounded queue-position interval.
- Fill probability conditional on queue state, market archetype, and time to close.

A core diagnostic is the queue-completion ratio:

$$
QCR = \frac{\text{estimated volume consumed ahead}}{\text{displayed size ahead at entry}}
$$

Because exchange data may not identify individual queue priority, estimates must include lower and upper bounds, assumptions, and a versioned calibration method.

### Binary-market normalization

Internally represent prices as exact fixed-point decimal values, not
floating-point numbers.

For binary contracts, derive complementary prices consistently, but
retain the original exchange-side representation for audit and
reconciliation.

## 5.7 Feature engine

Produce strategy-neutral features:

- Best bid and ask.
- Midpoint.
- Spread.
- Weighted midpoint.
- Book imbalance.
- Visible depth.
- Recent trade direction.
- Short-window price movement.
- Volatility estimate.
- Time to close.
- Market activity rate.
- Data age.
- Current inventory.
- Estimated fees.
- Estimated slippage.
- Queue size ahead and bounded queue-position estimate.
- Estimated fill probability and expected queue wait.
- Complementarity residual and synthetic cross-side spread.
- External reference midpoint, age, source divergence, and short-horizon realized volatility.
- Threshold distance normalized by volatility and time, where applicable.
- Market archetype ID.
- Quote-cancellation and replacement intensity.


Book imbalance must be treated as a hypothesis requiring calibration, not an assumed directional signal. The research system must compare top-level, top-three-level, distance-weighted, notional, and robust variants that exclude the largest displayed level. Predictive claims must be tested against midpoint movement, trade direction, fill probability, and quote toxicity by regime.

Every feature record must include:

    market
    calculation timestamp
    source event range
    feature version
    data-quality status

## 5.8 Strategy engine

The strategy engine consumes immutable snapshots and emits trade
intents.

It does not call the Kalshi API.

Trade intent schema:

    intent_id
    strategy_id
    strategy_version
    market_ticker
    action
    side
    limit_price
    desired_count
    time_in_force
    reason_codes
    feature_snapshot_id
    signal_confidence
    expected_fill_probability
    expected_queue_wait_seconds
    expected_gross_spread_capture
    expected_fee_cost
    expected_adverse_selection
    expected_inventory_cost
    expected_settlement_risk
    expected_cancel_probability
    expected_net_edge
    edge_model_version
    calibration_sample_size
    calibration_confidence
    expiry_timestamp

### Recommended first strategy: passive spread capture

For the initial engineering MVP, use a simple market-making research
strategy rather than directional crypto prediction.

Example behavior:

- Quote only in liquid, narrow-spread markets.
- Place passive post-only bids at or behind the best bid.
- Avoid crossing the spread.
- Limit inventory in either outcome.
- Cancel quotes when features become stale.
- Reprice only after a minimum price movement or quote age.
- Stop quoting close to market close.
- Do not trade when estimated edge is less than estimated fees plus a
  safety buffer.

### Binding quote-expectancy contract

A visible spread is not edge. For each proposed passive quote, the strategy must persist a versioned decomposition approximating:

$$
EV = P(\text{fill}) \times (\text{gross spread} - \text{fees} - \text{adverse selection} - \text{inventory cost} - \text{settlement risk}) - \text{cancel/reprice cost}
$$

Signal confidence, fill confidence, and expected profitability are separate quantities and must never share one ambiguous field. Initially, the expectancy model may be used for research and observability rather than as a binding order threshold, but every quote must still record its decomposition and model version.

The strategy must also record quote lifecycle efficiency:

- Cancels per fill.
- Reprices per fill.
- Mutating API requests per unit of gross and net spread.
- Median quote lifetime.
- Percentage canceled before meaningful queue advancement.
- Opportunity loss caused by request throttling.

Why this strategy first:

- It tests order-book accuracy.
- It exercises create, cancel, fill, and reconciliation paths.
- It does not require an external cryptocurrency price oracle.
- It exposes execution quality and inventory risk clearly.

A later second strategy may compare Kalshi-implied probabilities with an
external crypto reference model, but that should be a separate approved
phase.

## 5.8.1 External crypto reference observer

The passive-spread MVP may observe external crypto markets for toxicity detection, segmentation, and later research, but those feeds do not possess trading authority.

For supported underlyings, record an approved reference bundle containing:

- Liquid-exchange spot midpoint, preferably from a reviewed primary venue such as Binance where accessible.
- Reference timestamp and age.
- Short-horizon realized volatility.
- 24-hour volume and change.
- Cross-source spot deviation using a slower metadata/reference source such as CoinGecko.
- Kalshi threshold distance.
- Time remaining.
- Kalshi-implied probability movement relative to spot movement.

For threshold markets, calculate a normalized state variable when inputs are valid:

$$
z = \frac{K-S_t}{\sigma_t\sqrt{T}}
$$

This value is a segmentation and toxicity feature, not a complete probability model.

CoinGecko may support identity, metadata, broad historical context, and source-divergence checks, but it must not be the primary low-latency microstructure reference.

Reference data receives its own quality states and freshness limits. Missing, stale, or divergent external data must be represented explicitly and may cause the relevant analytical feature to become unavailable; it must never silently substitute fabricated values.

## 5.9 Risk gateway

All trade intents must pass through one synchronous policy boundary.

Checks:

- Demo environment confirmed.
- Exchange and market active.
- Market is allowlisted.
- Data is fresh.
- Order book is healthy.
- Intent has not expired.
- Price is valid.
- Count is positive and within limits.
- Position limit will not be exceeded.
- Per-market loss limit will not be exceeded.
- Portfolio loss limit will not be exceeded.
- Open-order count is within limits.
- Order-rate budget is available.
- Strategy is enabled.
- Kill switch is inactive.
- Settlement proximity restriction passes.
- No unresolved reconciliation incident exists.

### Initial risk limits

Use conservative configurable defaults such as:

    Paper bankroll:                 $1,000
    Maximum risk per order:         $5
    Maximum exposure per market:    $25
    Maximum aggregate exposure:     $100
    Maximum open orders:            10
    Maximum daily paper loss:       $25
    Maximum strategy drawdown:      5%
    Minimum time before close:      30 minutes
    Maximum acceptable spread:      strategy-specific
    Maximum market-data age:        2 seconds
    Maximum outstanding request age: 10 seconds

These are engineering defaults, not recommended financial limits.

### Probability- and scenario-aware risk

Nominal order cost is not a complete representation of binary-market risk. The risk service must additionally track:

- Worst-case outcome liability by contract.
- Correlated exposure groups across markets expressing the same underlying directional or settlement scenario.
- Scenario loss over reviewed settlement states.
- Liquidity-adjusted exposure.
- Exposure-weighted time to close.
- Position-size scaling as settlement approaches.

For plausible underlying settlement scenarios $q$, calculate:

$$
\text{Scenario Loss}(q) = \sum_i \text{PnL}_i(q)
$$

Risk approval must reject orders that breach single-market liability, correlated scenario-loss, liquidity-adjusted, or settlement-proximity limits even when nominal exposure remains below the fixed-dollar cap. Correlation groups and scenarios must be deterministic, reviewed, and versioned.

## 5.10 Execution engine

Responsibilities:

- Convert approved order plans into Kalshi requests.
- Generate UUID-based client order IDs.
- Apply post-only and time-in-force policy.
- Submit orders.
- Cancel stale or invalid orders.
- Maintain order lifecycle.
- Reconcile uncertain responses.
- Prevent duplicate orders.
- Throttle requests.

For the first release:

- Use limit orders.
- Default to `post_only=true`.
- Use `good_till_canceled` only when an explicit cancellation supervisor
  is active.
- Use self-trade prevention.
- Do not use batch order endpoints until single-order semantics are
  proven.
- Use `cancel_order_on_pause` where supported and appropriate.
- Do not use `reduce_only` unless its behavior is specifically required
  and tested.

The order API documents response classes including success, invalid
request, authentication failure, conflict, rate limiting, and server
error.

### Uncertain-result rule

A timeout after request transmission does not mean the order failed.

On uncertainty:

1.  Mark the local command `OUTCOME_UNKNOWN`.
2.  Stop strategy actions for that market.
3.  Query orders using the client order ID.
4.  Reconcile exchange state.
5.  Resume only after a deterministic result.

## 5.11 Order state machine

    INTENT_CREATED
        |
    RISK_APPROVED
        |
    SUBMISSION_PENDING
        |
        +--> REJECTED
        |
        +--> OUTCOME_UNKNOWN --> RECONCILING
        |
    ACKNOWLEDGED
        |
        +--> OPEN
        |      |
        |      +--> PARTIALLY_FILLED
        |      |       |
        |      |       +--> FILLED
        |      |       +--> CANCEL_PENDING
        |      |
        |      +--> CANCEL_PENDING
        |
        +--> FILLED
        +--> CANCELLED
        +--> EXPIRED

State changes must be driven by exchange evidence, not assumptions.

## 5.12 Portfolio and accounting ledger

Track:

- Cash balance.
- Reserved cash.
- YES positions.
- NO positions.
- Average entry price.
- Realized P&L.
- Unrealized P&L.
- Fees.
- Open-order exposure.
- Market settlement.
- Strategy attribution.

Use an append-only internal ledger for financial events:

    ORDER_RESERVED
    ORDER_RELEASED
    FILL_APPLIED
    FEE_APPLIED
    POSITION_MARKED
    MARKET_SETTLED
    ADJUSTMENT_RECONCILED

Derived balances must be reproducible from ledger events.

## 5.13 Reconciliation service

Run reconciliation:

- At startup.
- After reconnect.
- After uncertain REST responses.
- At a periodic interval.
- Before shutdown.
- After detecting an impossible state.

Compare:

    local open orders vs exchange open orders
    local fills vs exchange fills
    local positions vs exchange positions
    local available balance vs exchange balance

Any mismatch places the bot into:

    TRADING_SUSPENDED_RECONCILIATION_REQUIRED

Do not silently “fix” ledger state. Record an explicit reconciliation
adjustment with supporting exchange evidence.

## 5.14 Persistence

Suggested tables:

    markets
    market_snapshots
    orderbook_events
    trade_events
    feature_snapshots
    strategy_intents
    risk_decisions
    orders
    order_state_transitions
    fills
    positions
    ledger_entries
    reconciliation_runs
    runtime_incidents
    strategy_runs
    daily_performance
queue_state_snapshots
queue_calibrations
quote_expectancy_records
external_reference_events
market_archetypes
markout_measurements
toxicity_classifications
scenario_risk_snapshots
experiment_registry
statistical_evaluations

Important invariants:

- `client_order_id` is globally unique.
- Every submitted order traces to one approved risk decision.
- Every fill traces to one exchange order.
- Every position change traces to one or more ledger events.
- Every strategy decision identifies its strategy and feature versions.
- Every passive order traces to one quote-expectancy record and queue-state snapshot.
- Every fill has versioned markout and toxicity classifications when data coverage permits.
- Every market and decision preserves a market archetype ID.
- Every external numerical claim used by an agent traces to a deterministic tool result.
- Every confirmatory experiment is preregistered before its scored data window begins.

## 5.15 Agent model gateway

OpenRouter is the only LLM inference provider. The application must own a single narrow interface, implemented only by an OpenRouter adapter.

```python
class AgentModelGateway(Protocol):
    async def complete(
        self,
        *,
        agent_id: str,
        messages: list[AgentMessage],
        output_schema: type[BaseModel],
        tools: list[ToolDefinition],
        policy: ModelPolicy,
        trace: AgentTraceContext,
    ) -> AgentResponse:
        ...


class OpenRouterAgentGateway(AgentModelGateway):
    ...
```

Do not add direct Anthropic, OpenAI, Google, xAI, or other model-provider clients. The gateway centralizes:

- Authentication through `OPENROUTER_API_KEY`.
- Network and privacy policy.
- Model and provider routing.
- Retries and timeout handling.
- Structured outputs.
- Tool-call validation.
- Token and cost budgets.
- Response provenance and telemetry.
- Redaction and prompt egress scanning.

## 5.16 Agent registry and model governance

Each role uses an explicit, reviewed policy. Agents cannot select arbitrary models.

```yaml
agents:
  operations_analyst:
    model: <approved-openrouter-model-id>
    temperature: 0.1
    max_completion_tokens: 5000
    required_capabilities: [structured_outputs, tool_calling]
    fallback_policy: recorded_non_binding

  strategy_researcher:
    model: <approved-openrouter-model-id>
    temperature: 0.2
    max_completion_tokens: 7000
    required_capabilities: [structured_outputs, tool_calling]
    fallback_policy: fail_closed

  risk_critic:
    model: <approved-independent-openrouter-model-id>
    temperature: 0.1
    max_completion_tokens: 5000
    required_capabilities: [structured_outputs]
    fallback_policy: fail_closed
```

For every scored or authoritative workflow, freeze and record:

- Agent policy version.
- Agent prompt version.
- Exact OpenRouter model ID.
- Actual provider and model used when returned by the API.
- Provider-routing and fallback policy.
- Structured-output schema version.
- Tool-registry version.
- Evidence manifest and hash.
- Sampling and reasoning parameters.

Convenience summaries may permit recorded fallback. Strategy evaluation, risk review, and go/no-go workflows must use pinned models and fail closed rather than silently substitute another model. Any permitted fallback makes the output non-binding until reviewed or rerun under the frozen policy.

## 5.17 Structured output validator

All agent outputs must conform to versioned JSON Schemas and corresponding Pydantic models. Free-form prose must not drive downstream automation.

Validation sequence:

1. Validate the response against its JSON Schema.
2. Reject unknown or prohibited fields.
3. Confirm every cited evidence ID exists and was available to the agent.
4. Confirm confidence and numeric values are within bounds.
5. Detect prohibited action recommendations.
6. Persist request/response hashes, model metadata, and the validated object.
7. Mark the result non-binding unless its workflow and review requirements are satisfied.

Structured output guarantees shape, not truth. Evidence and policy validation remain mandatory.

## 5.18 Evidence and context builder

The context builder assembles the minimum evidence needed for a job. It must not expose unrestricted database access or entire log archives by default.

Evidence types include:

- Strategy-run manifests.
- Sanitized log events.
- Metrics windows.
- Order-state transitions.
- Reconciliation records.
- Ledger references and derived summaries.
- Feature snapshots.
- Replay results.
- Configuration hashes and approved non-secret configuration.
- Market settlement text and reviewed research sources.

Every evidence item receives an immutable identifier, content hash, source, creation time, sensitivity classification, and authorization scope.

## 5.19 Agent tool gateway

Initial read-only tools:

- `get_strategy_run_summary`
- `get_incident_timeline`
- `get_order_lifecycle`
- `get_reconciliation_evidence`
- `get_market_data_quality`
- `get_feature_snapshot`
- `get_risk_decision`
- `get_position_history`
- `get_performance_slice`
- `compare_strategy_versions`
- `run_frozen_replay`
- `run_statistical_test`
- `retrieve_market_rules`
- `retrieve_approved_research`

Controlled artifact-write tools:

- `create_analysis_report`
- `create_experiment_proposal`
- `create_test_plan`
- `create_incident_remediation_draft`
- `create_configuration_patch_draft`

Controlled writes go only to an isolated proposal path such as:

```text
artifacts/agent-proposals/<proposal_id>/
```

The gateway must not expose order creation, cancellation, risk approval, ledger mutation, reconciliation resolution, strategy activation, active configuration replacement, credential reading, arbitrary shell, arbitrary SQL, or generic Kalshi API access.

## 5.20 Agent roles

### Supervisor

- Classifies analysis jobs.
- Selects an approved workflow and minimum agent set.
- Establishes evidence, tool, token, cost, and time budgets.
- Validates role separation and required reviews.
- Reconciles disagreements without inventing missing evidence.
- Escalates uncertainty to the operator.

### Operations and incident analyst

- Reconstructs operational timelines.
- Diagnoses disconnects, stale data, sequence gaps, unknown order outcomes, slow cancellation, and reconciliation failures.
- Reports primary and alternative hypotheses, confidence, missing evidence, proposed remediation, and required tests.
- Cannot resolve incidents.

The incident workflow must distinguish `SYSTEM_ANOMALY`, `DATA_PIPELINE_ANOMALY`, `MARKET_MICROSTRUCTURE_ANOMALY`, `EXECUTION_ANOMALY`, `ACCOUNTING_ANOMALY`, and `STRATEGY_BEHAVIOR_ANOMALY`.

### Strategy researcher

- Generates falsifiable hypotheses.
- Analyzes replay results, fill quality, adverse selection, market segmentation, and feature candidates.
- Produces preregistered experiment specifications, not trade instructions.
- Cannot modify parameters during a scored run or activate a strategy.

### Market-microstructure analyst

Responsible for queue analysis, spread decomposition, markout distributions, order-flow toxicity, market-archetype segmentation, external-reference lag, and quote-lifecycle efficiency. Its outputs are limited to statistical findings, anomaly classifications, and experiment proposals. Numerical claims must originate from deterministic analysis tools rather than model arithmetic.

### Risk and adversarial reviewer

- Challenges sample size, fill models, leakage, post-hoc optimization, concentration, fee assumptions, latency, tail exposure, and authority-boundary violations.
- Must be logically independent of the strategy researcher and should use a separately pinned model policy where practical.

### Evaluation and reporting agent

- Produces daily, weekly, and final reports from verified metrics.
- Separates operational correctness, data quality, execution quality, risk behavior, statistical evidence, unresolved uncertainty, and profitability.
- Cannot recommend promotion based only on P&L.

### Later optional roles

- Market-rules reviewer.
- Test designer.
- Data-quality investigator.
- Cost and model-governance analyst.

## 5.21 Agent memory and provenance

Use three distinct classes of durable information:

1. **Immutable evidence** — original logs, events, metrics, ledgers, configurations, and replay outputs.
2. **Validated findings** — schema-valid claims with evidence references, model/prompt/tool versions, confidence, review state, and supersession links.
3. **Proposals** — unapproved hypotheses, changes, experiments, risks, tests, acceptance criteria, and approval state.

Ordinary chat text is never trusted memory. A model statement becomes durable only through validation, provenance attachment, and the appropriate review workflow.

## 5.22 Privacy and prompt egress policy

For every OpenRouter request:

- Require Zero Data Retention routing where supported by the approved model/provider policy.
- Keep OpenRouter prompt/response logging and data-use opt-ins disabled unless separately reviewed.
- Minimize evidence to the authorized task scope.
- Redact credentials, signatures, authentication headers, raw secrets, unnecessary personal data, and sensitive local paths.
- Scan serialized outbound content for PEM headers, Kalshi key identifiers, signatures, environment dumps, and known secret patterns.
- Fail closed when prohibited content is detected.

Privacy policy must be tested against the actual OpenRouter request payload, not only the prompt template.

## 5.23 Agent persistence

Suggested tables:

- `agent_runs`
- `agent_messages`
- `agent_tool_calls`
- `agent_evidence_links`
- `agent_findings`
- `agent_proposals`
- `agent_reviews`
- `agent_model_usage`
- `agent_policy_violations`
- `agent_approvals`

Prefer storing prompt-template version, context manifest, evidence IDs, hashes, validated outputs, routing metadata, tokens, and cost rather than unnecessarily retaining full sensitive prompts.

## 5.24 Human approval boundary

Human approval is required before:

- Changing strategy logic or parameters.
- Changing risk limits.
- Adding a market or series to an allowlist.
- Activating a proposed configuration.
- Accepting a reconciliation adjustment.
- Promoting a strategy version.
- Treating an AI-generated conclusion as binding in a go/no-go review.

Approval must create a durable record containing approver, time, proposal hash, evidence scope, decision, and resulting code/configuration version. Approval does not directly mutate active runtime state; normal reviewed engineering and deployment paths remain required.

# 6. Runtime Data Flow

## Startup

1.  Load configuration.
2.  Validate demo-only endpoint policy.
3.  Initialize structured logging.
4.  Open database and run safe schema checks.
5.  Load credentials from the secret source.
6.  Verify clock health.
7.  Query exchange status.
8.  Reconcile account, positions, fills, and open orders.
9.  Discover eligible crypto markets.
10. Fetch initial market and order-book snapshots.
11. Connect to demo WebSocket.
12. Subscribe to selected channels.
13. Confirm stream health.
14. Enable the strategy.
15. Begin the evaluation loop.

## Decision cycle

    Market event
      -> normalized event
      -> updated healthy order book
      -> feature snapshot
      -> strategy evaluation
      -> trade intent
      -> risk decision
      -> order plan
      -> execution
      -> order/fill event
      -> ledger update
      -> metrics

## Agent-assisted daily review

The initial AI workflow runs outside the trading loop:

```text
frozen strategy-run evidence
  -> evidence manifest and redaction
  -> operations analysis
  -> performance evaluation
  -> independent risk critique
  -> supervisor consistency check
  -> human-readable report with evidence links
```

The daily report includes operational status, unexplained anomalies, performance decomposition, risk observations, missing evidence, and recommended offline investigations. It cannot change the active strategy or runtime.

## Mandatory daily quantitative scorecard

The daily review must publish five independent dimensions without collapsing them into one composite score.

### Data integrity

- Healthy-book uptime.
- Sequence-gap and snapshot-rebuild counts.
- Median and p95 event age.
- Complementarity residual.
- External-reference freshness and divergence.

### Execution quality

- Acknowledgement and cancellation latency.
- Unknown-outcome and duplicate-command rates.
- Queue position at entry and advancement.
- Fill rate and cancels per fill.

### Adverse selection

- Five-, 30-, and 60-second markouts.
- Markout expected shortfall.
- Toxic-fill percentage.
- Stale-quote-fill percentage.

### Strategy economics

- Gross spread captured.
- Fees.
- Inventory markout.
- Settlement P&L.
- Net P&L.
- Return on maximum capital at risk.
- Profit per submitted order, fill, and mutating API request.

### Risk concentration

- Maximum single-market liability.
- Maximum correlated scenario loss.
- Time near risk limits.
- Exposure-weighted time to close.
- Liquidity-adjusted position size.
- Drawdown.

## Incident investigation workflow

```text
incident created
  -> deterministic evidence bundle
  -> operations analyst
  -> alternative-cause/risk critic
  -> test designer
  -> remediation proposal
  -> human review
  -> normal engineering workflow
```

The agent cannot set an incident to `RESOLVED`.

## Strategy research workflow

```text
research question
  -> strategy researcher drafts falsifiable hypothesis
  -> test designer preregisters experiment
  -> human approves experiment
  -> deterministic replay runs
  -> evaluation agent interprets results
  -> risk critic challenges conclusions
  -> human may approve a new frozen strategy version
```

This workflow prohibits repeated AI-driven parameter modification until a favorable backtest appears.

## Shutdown

1.  Disable new strategy intents.
2.  Cancel managed open orders.
3.  Wait for acknowledgements within a bounded timeout.
4.  Reconcile open orders and positions.
5.  Flush ledger and metrics.
6.  Persist final strategy-run state.
7.  Close WebSocket and REST clients.
8.  Exit nonzero when clean reconciliation was not achieved.

# 7. Failure Handling

## WebSocket disconnect

- Mark all streamed books stale immediately.
- Suspend new orders.
- Keep or cancel existing orders according to configured disconnect
  policy.
- Reconnect with exponential backoff.
- Retrieve fresh snapshots.
- Rebuild books.
- Reconcile account state.
- Resume only when all selected markets are healthy.

## Subscription overflow

Kalshi documents a subscription-buffer-overflow error and recommends
reducing the subscribed data set or improving read throughput.

Bot response:

- Suspend strategy.
- Record incident.
- Reduce active market count.
- Reconnect and resnapshot.
- Alert the operator.
- Do not discard events and continue with a potentially corrupt book.

## Rate limiting

- Centralize all request budgeting.
- Honor server retry guidance when supplied.
- Apply jittered backoff.
- Prioritize cancellations and reconciliation over discovery.
- Never retry mutating calls blindly.
- Reduce market scanning frequency before sacrificing order safety.

## Database failure

- Stop new order submission.
- Attempt to cancel managed open orders.
- Keep in-memory incident evidence only long enough to perform safe
  shutdown.
- Exit with a critical incident status.

## Authentication failure

- Do not repeatedly retry invalid credentials.
- Suspend all operations.
- Redact credential material.
- Require operator intervention.

## Market pause or close

- Cancel applicable orders.
- Stop strategy evaluation for that market.
- Preserve positions for settlement tracking.
- Record the lifecycle transition.

## OpenRouter or agent failure

- Mark the analysis workflow failed or degraded.
- Do not block deterministic trading safety functions.
- Do not retry indefinitely.
- Respect request, token, cost, and wall-clock budgets.
- Record requested and actual model/provider metadata when available.
- Invalidate authoritative output after an unapproved fallback or schema failure.
- Preserve the evidence bundle for deterministic rerun.
- Require human review when an analysis was incomplete.

## Agent policy or privacy violation

- Stop the affected workflow immediately.
- Record a policy incident without storing detected secret material.
- Revoke the result's binding status.
- Do not broaden tools or evidence to complete the request.
- Require operator review before re-execution.

# 8. Observability

## Structured logs

Each event should include:

    timestamp
    level
    run_id
    component
    market_ticker
    strategy_id
    intent_id
    client_order_id
    exchange_order_id
    event_type
    outcome
    latency_ms
    error_code

Never log:

- Private keys.
- Request signatures.
- Full authentication headers.
- Raw secret environment variables.

## Metrics

### Connectivity

- REST request latency.
- REST errors by class.
- WebSocket reconnect count.
- Last message age.
- Subscription errors.
- Snapshot resync count.

### Market data

- Active market count.
- Stale-book count.
- Sequence gaps.
- Events processed per second.
- Order-book rebuild duration.

### Execution

- Orders submitted.
- Orders rejected.
- Orders canceled.
- Unknown outcomes.
- Fill ratio.
- Time to acknowledgement.
- Time to cancel.
- Maker versus taker fills.

### Risk

- Rejected intents by rule.
- Current gross exposure.
- Exposure by market.
- Daily P&L.
- Drawdown.
- Kill-switch state.

### Strategy

- Signals emitted.
- Quotes placed.
- Estimated edge at submission.
- Realized edge after fill.
- Adverse selection after 5, 30, and 60 seconds.
- Inventory duration.
- P&L by market and strategy version.

### AI control plane

- Agent requests by role and workflow.
- OpenRouter latency and error class.
- Requested versus actual model/provider.
- Input/output tokens and estimated cost.
- Structured-output validation failures.
- Tool-call denials and failures.
- Evidence-reference validation failures.
- Unsupported-claim and prohibited-action detections.
- Model/provider fallback count.
- Agent disagreement rate.
- Human acceptance, rejection, and revision rate.
- Prompt-egress scanner blocks.
- Budget-limit blocks.
- Analysis freshness and evidence age.

Agent logs must not contain full secrets, raw authentication material, or unnecessarily retained prompts.

## Operator status view

The MVP may use a terminal dashboard showing:

    DEMO MODE
    exchange status
    stream status
    selected markets
    open orders
    positions
    exposure
    daily P&L
    risk status
    latest incident

The phrase `DEMO MODE` should be permanently visible.

# 9. Backtesting and Replay

## Historical research mode

Create a separate replay command that:

1.  Loads historical trades and candlesticks.
2.  Reconstructs only the market information actually available at each
    timestamp.
3.  Applies the same feature and strategy interfaces used in paper mode.
4.  Uses an explicit fill model.
5.  Records assumptions and coverage limitations.
6.  Produces deterministic results from a fixed dataset and
    configuration.

The docs pack includes dedicated historical endpoints for markets,
candlesticks, trades, orders, and fills.

## Experiment registry and statistical discipline

Before confirmatory strategy analysis, register:

- Hypothesis and falsification criteria.
- Primary metric.
- Secondary metrics.
- Fixed parameter grid.
- Included and excluded market archetypes.
- Training, development, and holdout windows.
- Minimum sample and diversity requirements.
- Multiple-comparison correction.
- Planned missing-data treatment.
- Strategy, feature, expectancy, archetype, fill-model, and agent-policy versions.

Exploratory analysis must be labeled exploratory. All tested variants must be retained, not only winners. Confirmatory evidence requires a holdout period or market set that was not used to formulate the hypothesis.

Report confidence intervals for fill rate, positive-markout rate, net edge, P&L, tail loss, cancellation efficiency, and archetype-specific results. Resampling must cluster by market or settlement event when order-level observations are not independent. Effective sample size must account for autocorrelation and repeated observations from the same market.

## Fill-model hierarchy

Use progressively stronger evidence:

1.  **Naive model:** fill at quoted price when a trade crosses it.
2.  **Queue-aware approximation:** account for displayed size ahead.
3.  **Paper/live comparison:** calibrate assumptions using demo fills.
4.  **Conservative stress model:** add latency, missed fills, fees, and
    adverse selection.

Backtest output must distinguish:

    signal quality
    fill-model assumptions
    gross P&L
    fees
    slippage
    net P&L
    maximum drawdown
    market coverage
    data gaps

# 10. Testing Strategy

## Unit tests

- Request-signing canonicalization.
- Fixed-point price parsing.
- YES/NO price conversions.
- Order-book snapshot application.
- Delta application.
- Feature calculations.
- Strategy decisions.
- Every risk rule.
- Order-state transitions.
- P&L and fee calculations.
- Settlement accounting.
- Queue-state bounds and advancement calculations.
- Complementarity residuals and synthetic cross-side prices.
- Markout and toxicity classification.
- External-reference freshness, divergence, and normalized threshold distance.
- Scenario-loss and correlation-group calculations.
- Quote-expectancy decomposition.
- Clustered confidence intervals and effective-sample-size calculations.
- Configuration endpoint validation.

## Property-based tests

Examples:

- Book size never becomes negative.
- Applying the same event twice cannot create duplicate ledger value.
- Order filled count never exceeds submitted count.
- Remaining count never becomes negative.
- Risk-approved exposure never exceeds configured limits.
- Ledger-derived cash equals expected cash after arbitrary valid fill
  sequences.
- Production URLs are rejected for all generated configuration variants.
- Queue lower bounds never exceed upper bounds.
- A fill cannot reference a queue or expectancy snapshot created after submission.
- Scenario-risk aggregation is invariant to position ordering.
- Missing reference data never becomes a numeric zero without an explicit unavailable state.
- Confirmatory experiment records are immutable after the scored window begins.

## Contract tests

Record sanitized example payloads from the demo API and verify:

- REST response models.
- WebSocket event models.
- Optional fields.
- Unknown-field tolerance.
- Decimal precision.
- Error responses.

## Integration tests

Against mocked services:

- Startup reconciliation.
- Snapshot followed by deltas.
- Disconnect and reconnect.
- Order submission and fill.
- Partial fill then cancellation.
- Request timeout with eventual order discovery.
- Rate limiting.
- Market pause.
- Stale stream.
- Database failure.
- External reference disconnect, staleness, and source divergence.
- Queue-estimation uncertainty under partial book evidence.
- Toxic fill after a rapid reference move.
- Correlated scenario-limit rejection despite nominal exposure headroom.
- Experiment-registry mutation attempt after freeze.

## Demo-environment acceptance tests

- Connect with demo credentials.
- Discover approved crypto markets.
- Subscribe to market data.
- Maintain an order book for at least one hour.
- Place one tiny post-only order.
- Confirm acknowledgement.
- Cancel it.
- Reconcile no residual order.
- Obtain a controlled partial or full paper fill.
- Reconcile the fill and position.
- Stop and restart without state divergence.

## AI control-plane tests

### Unit and schema tests

- OpenRouter request construction and redaction.
- Model-policy and capability validation.
- Structured-output validation for every agent result.
- Evidence-ID and scope validation.
- Budget enforcement.
- Proposal-versus-active-configuration path separation.
- Prompt egress detection for key, signature, PEM, and environment patterns.

### Property-based safety tests

- No generated model output can deserialize as an executable `TradeIntent`.
- No registered agent tool can reach the execution engine.
- No agent operation can mutate append-only ledger state.
- Unknown evidence IDs always invalidate findings.
- Agent context never includes fields classified above its authorization.
- Replaying the same evidence cannot duplicate an approved action.
- Generated model or provider fallbacks cannot silently become binding.

### Integration and adversarial tests

- OpenRouter outage while managed orders require cancellation.
- Schema-invalid and partially streamed responses.
- Tool-call arguments that exceed evidence scope.
- Prompt injection embedded in market names, settlement text, logs, or retrieved research.
- Attempted private-key and credential exfiltration.
- Attempted active-configuration overwrite.
- Agent process inspection proving absence of Kalshi credentials.
- Seeded incidents with known root causes and plausible distractors.
- Conflicting researcher and critic conclusions.
- Human approval record requirements.

### Acceptance criteria

- The paper trader completes safe cancellation, reconciliation, and shutdown with OpenRouter unavailable.
- Agent reports cite only valid evidence available in the job manifest.
- Seeded policy attacks cannot obtain additional tools or data.
- Authoritative workflows fail closed on model substitution, schema failure, or missing evidence.
- Agent conclusions remain explicitly non-binding until required review and approval are complete.

# 11. Repository Layout

    kalshi-bot-alpha/
    ├── pyproject.toml
    ├── README.md
    ├── .env.example
    ├── config/
    │   ├── demo.example.yaml
    │   ├── strategies/
    │   │   └── passive_spread.yaml
    │   └── risk/
    │       └── conservative.yaml
    ├── src/
    │   └── kalshi_bot/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── application.py
    │       ├── config/
    │       │   ├── models.py
    │       │   └── loader.py
    │       ├── auth/
    │       │   └── signer.py
    │       ├── kalshi/
    │       │   ├── demo_endpoints.py
    │       │   ├── rest_client.py
    │       │   ├── websocket_client.py
    │       │   ├── models.py
    │       │   └── errors.py
    │       ├── market_data/
    │       │   ├── catalog.py
    │       │   ├── orderbook.py
    │       │   ├── normalizer.py
    │       │   └── freshness.py
    │       ├── features/
    │       │   ├── engine.py
    │       │   └── models.py
    │       ├── strategies/
    │       │   ├── base.py
    │       │   └── passive_spread.py
    │       ├── risk/
    │       │   ├── gateway.py
    │       │   ├── limits.py
    │       │   └── kill_switch.py
    │       ├── execution/
    │       │   ├── engine.py
    │       │   ├── order_manager.py
    │       │   └── state_machine.py
    │       ├── portfolio/
    │       │   ├── ledger.py
    │       │   ├── positions.py
    │       │   └── pnl.py
    │       ├── reconciliation/
    │       │   └── service.py
    │       ├── persistence/
    │       │   ├── database.py
    │       │   ├── models.py
    │       │   └── repositories.py
    │       ├── replay/
    │       │   ├── engine.py
    │       │   └── fill_models.py
    │       └── observability/
    │           ├── logging.py
    │           ├── metrics.py
    │           └── incidents.py
    ├── migrations/
    ├── tests/
    │   ├── unit/
    │   ├── property/
    │   ├── contract/
    │   ├── integration/
    │   └── acceptance/
    ├── scripts/
    │   ├── verify_demo_only.py
    │   ├── reconcile.py
    │   └── export_run_report.py
    ├── docs/
    │   ├── ARCHITECTURE.md
    │   ├── SAFETY_MODEL.md
    │   ├── STRATEGY_SPEC.md
    │   ├── DATA_MODEL.md
    │   ├── RUNBOOK.md
    │   └── PAPER_TRADING_PROTOCOL.md
    └── docs-dev/
        └── kalshi-docs-pack/

## 11.1 Version 2 agent-control-plane additions

```text
src/kalshi_bot/
├── agents/
│   ├── runtime.py
│   ├── supervisor.py
│   ├── registry.py
│   ├── context_builder.py
│   ├── tool_gateway.py
│   ├── output_validator.py
│   ├── approval.py
│   ├── memory.py
│   ├── evidence.py
│   ├── policies.py
│   └── roles/
│       ├── operations_analyst.py
│       ├── strategy_researcher.py
│       ├── risk_critic.py
│       ├── evaluation_reporter.py
│       └── test_designer.py
├── openrouter/
│   ├── client.py
│   ├── models.py
│   ├── routing.py
│   ├── capabilities.py
│   ├── privacy.py
│   ├── budgets.py
│   ├── errors.py
│   └── telemetry.py
└── agent_tools/
    ├── database_views.py
    ├── replay_tools.py
    ├── metrics_tools.py
    ├── report_tools.py
    ├── research_tools.py
    └── test_tools.py

config/
├── agents/
│   ├── registry.example.yaml
│   ├── model-policy.example.yaml
│   └── privacy-policy.example.yaml

schemas/
├── agent-job.schema.json
├── incident-analysis.schema.json
├── experiment-proposal.schema.json
├── risk-review.schema.json
└── evaluation-report.schema.json

artifacts/
├── evidence-bundles/
├── agent-proposals/
└── agent-reports/

tests/
├── agents/
├── openrouter/
├── privacy/
└── adversarial/

docs/
├── AI_AUTHORITY_MODEL.md
├── OPENROUTER_POLICY.md
├── AGENT_TOOL_POLICY.md
├── AGENT_EVIDENCE_MODEL.md
└── AI_EVALUATION_PROTOCOL.md
```

The agent process should receive read-only access to evidence exports or narrowly defined database views. It must not import the Kalshi execution package or receive the trading process environment.

## 11.2 Version 3 microstructure additions

```text
src/kalshi_bot/
├── market_data/
│   ├── archetypes.py
│   ├── complementarity.py
│   └── queue_state.py
├── external_reference/
│   ├── gateway.py
│   ├── models.py
│   ├── freshness.py
│   └── divergence.py
├── features/
│   ├── imbalance.py
│   ├── volatility.py
│   └── threshold_distance.py
├── strategies/
│   └── expectancy.py
├── risk/
│   ├── correlation_groups.py
│   └── scenario_loss.py
├── analytics/
│   ├── markouts.py
│   ├── toxicity.py
│   ├── queue_calibration.py
│   ├── confidence_intervals.py
│   └── scorecard.py
├── experiments/
│   ├── registry.py
│   ├── preregistration.py
│   └── multiple_testing.py
└── agents/roles/
    └── market_microstructure_analyst.py
```

# 12. Delivery Phases

## Phase 0 — Contracts and safety model

Deliver:

- Architecture decision record.
- Demo-only endpoint policy.
- Credential policy.
- Domain model definitions.
- Order-state machine.
- Risk-limit schema.
- Failure taxonomy.
- Paper-trading protocol.
- Market-archetype schema.
- Quote-expectancy schema.
- Queue-state and calibration contract.
- Markout and toxicity taxonomy.
- External-reference observation policy.
- Correlated scenario-risk contract.
- Immutable experiment-registry contract.
- Statistical sufficiency and multiple-testing policy.

Exit criteria:

- Production endpoints are explicitly forbidden.
- All state transitions and invariants are documented.
- No trading code exists yet.
- Signal confidence, fill probability, and expected net edge are separate fields.
- Passive-spread edge is defined by a versioned expectancy decomposition.
- Promotion requires sample and diversity gates in addition to elapsed time.

## Phase 1 — Read-only connectivity

Deliver:

- Authentication signer.
- Demo REST client.
- Market discovery.
- Exchange-status checks.
- WebSocket connection.
- Ticker and trade subscriptions.
- Structured logging.

Exit criteria:

- Runs for four hours without unhandled failure.
- Reconnects successfully.
- No order endpoint is implemented.

## Phase 2 — Order-book integrity

Deliver:

- REST snapshot loader.
- WebSocket delta handling.
- Freshness and resynchronization.
- Fixed-point price models.
- Order-book test corpus.
- Complementarity checks.
- Queue-state capture and bounded position estimates.
- Market-archetype classifier.
- External-reference observer with independent quality states.

Exit criteria:

- Books survive reconnect and resnapshot tests.
- Gap detection suspends downstream consumers.
- Property tests pass.

## Phase 3 — Portfolio and simulated execution

Before sending demo orders, create a local simulator:

- Local order matching.
- Position accounting.
- Fee model.
- Ledger.
- P&L reports.
- Strategy interface.
- Risk gateway.

Exit criteria:

- Deterministic replay.
- Accounting invariants pass.
- Risk limits cannot be bypassed.

## Phase 4 — Demo order lifecycle

Deliver:

- Create-order integration.
- Cancel-order integration.
- Open-order reconciliation.
- Fill processing.
- Position reconciliation.
- Uncertain-outcome recovery.

Exit criteria:

- A tiny demo order can be placed, canceled, and reconciled.
- Restart does not duplicate an order.
- Timeout tests prove idempotent recovery.

## Phase 5 — Passive spread strategy

Deliver:

- Feature engine.
- Passive quoting strategy.
- Inventory controls.
- Quote aging and repricing.
- Strategy metrics.
- Versioned quote-expectancy model.
- Queue-aware fill-probability estimates.
- Markout and toxicity classifications.
- Cancellation/replacement efficiency metrics.
- Scenario-aware inventory controls.

Exit criteria:

- Strategy runs for seven consecutive paper days.
- No risk-limit breach.
- No unreconciled state.
- Complete daily reports.

## Phase 6 — Evaluation and hardening

Deliver:

- Historical replay.
- Demo-versus-replay comparison.
- Chaos tests.
- Operational runbook.
- Performance report.
- Go/no-go review package.
- Archetype-segmented results.
- Clustered confidence intervals and effective sample size.
- Holdout evaluation and multiple-testing disclosure.
- External-reference lag and toxicity analysis.
- Correlated settlement-scenario stress report.

Exit criteria:

- At least 30 calendar days of paper evidence.
- All incidents classified.
- Strategy results reported after fees and conservative assumptions.
- Human review determines whether further development is justified.

## AI Phase A — Offline reporting

Begin after deterministic portfolio simulation, risk, ledger, and replay evidence are stable.

Deliver:

- OpenRouter gateway.
- Model registry and capability checks.
- Privacy and prompt-egress policy.
- Immutable evidence exporter.
- Structured evaluation reporter.
- Agent telemetry and budgets.

Exit criteria:

- Reports cite valid evidence.
- Sensitive-data tests pass.
- OpenRouter failure has no effect on trading safety.
- All conclusions are explicitly non-binding.
- No agent tool can reach execution or active configuration.

## AI Phase B — Incident analysis

Begin after demo order lifecycle and reconciliation are stable.

Deliver:

- Operations analyst.
- Incident timeline tools.
- Independent critic.
- Test-plan generation.
- Human review workflow.

Exit criteria:

- Every finding traces to evidence.
- Seeded incidents are classified with measured accuracy.
- Unsupported claims and missing evidence are surfaced.
- Agents cannot resolve or modify incidents.

## AI Phase C — Strategy research

Begin after deterministic historical replay and conservative fill models are complete.

Deliver:

- Strategy researcher.
- Market-microstructure analyst.
- Deterministic queue, markout, toxicity, and statistical-analysis tools.
- Statistical-analysis tools.
- Preregistered experiment schema.
- Frozen prompt/model/tool policy.
- Independent risk critique.

Exit criteria:

- No AI output enters the trade-intent interface.
- No automatic parameter optimization occurs during scored runs.
- Every proposal includes falsification criteria and required tests.
- Replay execution remains deterministic.
- Model, prompt, schema, tool, or evidence changes create a new experiment version.

## AI Phase D — Governed operations assistant

Begin only after Phases A–C satisfy their evaluation criteria.

Deliver:

- Scheduled daily and weekly reviews.
- Human approval queue.
- Bounded configuration patch drafts.
- Model, cost, and quality monitoring.
- Multi-model disagreement workflows where justified.

Exit criteria:

- Approval records are durable and auditable.
- Proposals cannot directly modify active runtime state.
- Agent quality is evaluated against a labeled incident and report corpus.
- Continued agent operation demonstrates measurable value after cost and review burden.

# 13. Paper-Trading Evaluation Protocol

Each strategy version must be frozen before evaluation.

Record:

    strategy version
    configuration hash
    code commit
    market-selection rules
    risk limits
    starting bankroll
    evaluation start and end
    planned exclusions
    known data limitations
    agent policy version
    agent prompt version
    OpenRouter model ID and actual provider/model metadata
    provider-routing and fallback policy
    structured-output schema version
    tool-registry version
    evidence-manifest hash

Minimum evaluation requires both time and evidence volume:

- At least 30 calendar days.
- A preregistered minimum number of eligible quote opportunities.
- Minimum submitted quotes and fills.
- Minimum fills per included market archetype.
- Minimum distinct settlement events.
- Minimum adverse-selection observations.
- Minimum clean restarts and reconciliations.
- Maximum unresolved data gaps.
- Minimum effective sample size after clustering and autocorrelation adjustment.
- Multiple crypto market types and expirations.
- No parameter changes during the scored period.
- Separate development and evaluation periods.
- Daily reconciliation.
- Weekly incident review.

Primary metrics:

- Net paper P&L after fees.
- Maximum drawdown.
- Return on maximum capital at risk.
- Fill rate.
- Adverse selection.
- Exposure concentration.
- Order rejection rate.
- Reconciliation incidents.
- Strategy uptime.
- Performance by market type.
- Performance by market archetype and time-to-close bucket.
- Fill probability calibration.
- Queue completion and queue-conditioned fill rates.
- Markout distribution, tail expected shortfall, and toxicity rate.
- Gross spread, fees, inventory markout, settlement P&L, and net edge decomposition.
- Profit per submitted order, fill, and API mutation.
- Maximum correlated scenario loss.
- Confidence intervals and effective sample size.
- Full multiple-testing and variant-disclosure record.

Promotion should require operational correctness before profitability:

1.  No production access.
2.  No unresolved accounting differences.
3.  No risk-limit bypass.
4.  Stable market-data processing.
5.  Deterministic restart recovery.
6.  Only then evaluate strategy performance.
7.  Strategy performance satisfies preregistered sample, diversity, uncertainty, holdout, and multiple-testing requirements.
8.  Positive aggregate results are not accepted when driven by one archetype, one settlement event, or an unrealistic fill model.

## 13.1 AI evaluation protocol

AI-agent quality must be evaluated separately from strategy profitability.

Use a frozen corpus containing:

- Known operational incidents.
- Clean runs with no incident.
- Ambiguous cases with intentionally missing evidence.
- Prompt-injection and data-exfiltration attempts.
- Conflicting but plausible hypotheses.
- Strategy reports with known statistical weaknesses.

Measure:

- Evidence citation validity.
- Root-cause classification accuracy.
- Unsupported-claim rate.
- Missing-evidence detection.
- Policy-violation rate.
- Structured-output success rate.
- Human acceptance and correction rate.
- Inter-model and rerun consistency.
- Latency, tokens, and cost.
- Net analyst time saved after review burden.

An agent workflow is promotable only when it provides repeatable operational value without receiving greater authority. Higher model quality does not justify broader trading permissions.

# 14. Definition of Done

The paper-trading bot is complete when:

- It can operate only against Kalshi’s demo environment.
- Production endpoints are rejected by tests and runtime policy.
- Secrets never enter source control or logs.
- Crypto markets are selected through an explicit reviewed policy.
- REST snapshots and WebSocket deltas produce reliable order books.
- Stale, missing, or inconsistent data suspends trading.
- Strategies emit intents rather than calling the exchange.
- Every intent passes through a centralized risk gateway.
- Every order uses a unique client order ID.
- Create, cancel, partial fill, fill, rejection, timeout, and restart
  paths are tested.
- Local orders, fills, positions, and balances reconcile with Kalshi
  demo state.
- The ledger can reproduce balances and P&L.
- A kill switch cancels managed orders and prevents new submissions.
- Daily performance and incident reports are generated.
- At least 30 days of version-frozen paper results are available.
- Passive quotes preserve versioned signal, fill-probability, queue, and expected-net-edge evidence.
- Queue estimates, markouts, toxicity classifications, and quote-lifecycle efficiency are measured.
- External crypto reference data is observational, quality-scored, and never an execution bypass.
- Results are segmented by deterministic market archetype.
- Risk includes correlated settlement scenarios, outcome liability, liquidity adjustment, and time to close.
- Confirmatory experiments are preregistered and immutable during scored windows.
- Sample-size, diversity, confidence-interval, holdout, and multiple-testing gates are satisfied or the result is explicitly inconclusive.
- Numerical AI claims trace to deterministic tool outputs with evidence provenance.
- No component claims live-trading readiness.
- OpenRouter is the only configured LLM inference gateway.
- The agent control plane has no Kalshi credentials or execution tools.
- Model output cannot deserialize into an executable trade intent.
- Agent reports and proposals cite immutable evidence identifiers.
- Structured-output, privacy, prompt-injection, and tool-boundary tests pass.
- OpenRouter outage cannot impair cancellation, reconciliation, accounting, risk controls, or shutdown.
- Authoritative AI workflows fail closed on unapproved model fallback, schema failure, missing evidence, or budget violation.
- Strategy, risk, market-eligibility, reconciliation, and promotion changes require durable human approval and normal reviewed implementation paths.
- Agent quality is measured on a frozen evaluation corpus and demonstrates value after cost and review burden.
- Any future live-trading capability requires a separate architecture,
  security review, implementation project, and explicit human approval.


# 15. Market-Microstructure Research Contract

The system is not permitted to claim passive spread-capture edge unless it can separate and quantify:

1. Displayed spread.
2. Fill probability conditional on bounded queue position.
3. Fees and mutating-request costs.
4. Immediate and delayed adverse selection.
5. Inventory and settlement risk.
6. External-reference lag and stale-quote exposure.
7. Market-archetype dependence.
8. Correlated scenario exposure.
9. Fill-model uncertainty.
10. Statistical uncertainty and multiple testing.

A strategy result is `INCONCLUSIVE` when any required component lacks sufficient coverage. Profitability claims must be net of fees and conservative queue, latency, missed-fill, and toxicity assumptions. The platform must be capable of producing trustworthy negative evidence when no edge is present.

## 15.1 Markout and toxicity contract

For each fill, calculate signed realized spread at multiple horizons:

$$
\text{Realized Spread}_t = s \times 2(P_{fill} - M_t)
$$

where $s=+1$ for a sell and $s=-1$ for a buy. Report median, 10th and 25th percentiles, expected shortfall, positive-markout frequency, and segmentation by archetype and time to close.

Classify fills as `BENIGN`, `TOXIC`, `STALE_QUOTE`, `LIFECYCLE`, `INVENTORY_REBALANCING`, or `AMBIGUOUS`. Every classification must preserve its rules version and input evidence.

## 15.2 Statistical decision states

Every strategy evaluation concludes with exactly one state:

- `OPERATIONALLY_INVALID` — evidence integrity or accounting is insufficient.
- `ECONOMICALLY_NEGATIVE` — conservative net-edge estimate is negative.
- `INCONCLUSIVE` — coverage or effective sample size is insufficient.
- `PROMISING_EXPLORATORY` — exploratory evidence is positive but not confirmatory.
- `CONFIRMATORY_PASS` — preregistered holdout and uncertainty gates pass.

No AI agent may promote or reinterpret these states. They are assigned by deterministic evaluation policy from versioned statistical outputs.

# 16. OpenRouter Reference Baseline

Implementation must verify current official documentation at build time because model capabilities, routing behavior, and privacy controls may change. The OpenRouter control-plane design is grounded in these official resources:

- API overview: <https://openrouter.ai/docs/api/reference/overview>
- Tool calling: <https://openrouter.ai/docs/guides/features/tool-calling>
- Structured outputs: <https://openrouter.ai/docs/guides/features/structured-outputs>
- Provider routing: <https://openrouter.ai/docs/guides/routing/provider-selection>
- Model fallbacks: <https://openrouter.ai/docs/guides/routing/model-fallbacks>
- Zero Data Retention: <https://openrouter.ai/docs/guides/features/zdr>
- Provider logging policy: <https://openrouter.ai/docs/guides/privacy/provider-logging>
- OpenRouter data collection: <https://openrouter.ai/docs/guides/privacy/data-collection>

Do not infer that every model supports every feature. Resolve required capabilities from current OpenRouter metadata and fail closed when the selected model/provider combination does not satisfy the workflow policy.
