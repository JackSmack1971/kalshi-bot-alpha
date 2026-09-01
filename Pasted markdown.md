I’d do this as **10 PRs**, with two milestones:

* **PR 1–8:** shortest safe path to the **first tiny Kalshi demo order**
* **PR 9–10:** turn that order lifecycle into the **actual autonomous paper-trading MVP**

The key is to implement the frozen invariants without implementing the entire research platform. The contracts require exact accounting, centralized non-bypassable risk, append-only order transitions, provenance, and fail-closed behavior; those cannot be cut.

## Ruthless 10-PR plan

| PR | Deliverable                                      |    First demo trade? |     MVP? |
| -- | ------------------------------------------------ | -------------------: | -------: |
| 1  | Order-book snapshot + exact prices               |             Required | Required |
| 2  | WS deltas + resync/freshness                     |             Required | Required |
| 3  | Minimal market eligibility + book health         |             Required | Required |
| 4  | SQLite ledger + positions + P&L                  |             Required | Required |
| 5  | Deterministic risk gateway + kill switch         |             Required | Required |
| 6  | Local simulator + order state machine            |             Required | Required |
| 7  | Demo order REST API + idempotency                |             Required | Required |
| 8  | Reconciliation + tiny-order acceptance harness   | **FIRST DEMO ORDER** | Required |
| 9  | Minimal features + passive strategy + expectancy |                   No | Required |
| 10 | Runtime integration + autonomous MVP acceptance  |                   No |  **MVP** |

### PR 1 — Exact order book foundation

**Goal:** establish one trustworthy representation of a Kalshi book.

Build:

* fixed-point price/count models
* REST order-book snapshot endpoint
* immutable `OrderBookSnapshot`
* YES/NO representation/conversion rules
* best bid/ask, spread, midpoint
* explicit quality state: `INITIALIZING / HEALTHY / STALE / GAP / RESYNCING`
* snapshot timestamp and sequence/version metadata

Tests:

* malformed levels rejected
* duplicate levels handled deterministically
* negative size impossible
* prices stay exact; no `float`
* YES/NO complementarity math
* snapshot ordering invariant

The data model explicitly forbids binary floating point for exchange prices/accounting.

**Defer:** queue probability, archetypes, external crypto feeds, imbalance signals, persistence of every historical book.

---

### PR 2 — WebSocket order-book deltas + resynchronization

This is the first genuinely critical Phase 2 PR.

Add:

* `orderbook_delta` subscription
* deterministic delta application
* sequence/gap detection
* stale-data timer
* reconnect → discard local book → fetch new snapshot
* gap → immediately make book unusable
* resync before consumers resume
* consumer API exposing only healthy books

Required property tests:

* size never negative
* reordered/broken sequences never silently apply
* a gap cannot produce `HEALTHY`
* reconnect cannot retain stale pre-disconnect state
* duplicate event handling doesn't corrupt the book

Phase 2's formal exit criteria require reconnect/resnapshot survival and downstream suspension on gaps.

**Do not** optimize the book implementation yet.

---

### PR 3 — Minimal eligibility and trading-state gate

Do not build a fancy market-selection system.

Implement the smallest deterministic gate:

```text
crypto?
approved series?
market open?
enough time before close?
book HEALTHY?
data fresh?
spread nonzero?
```

Use a **static reviewed allowlist/config** initially.

Also assign a minimal `market_archetype_id`, because your frozen contracts eventually require one to follow decisions through the system.

For v0.1, archetypes can be intentionally coarse:

```text
BTC_THRESHOLD_SHORT
BTC_THRESHOLD_MEDIUM
ETH_THRESHOLD_SHORT
OTHER_APPROVED_CRYPTO
```

No ML/classification cleverness.

**Defer:**

* volatility regime classification
* event-driven detection
* external-reference regimes
* dynamic market scoring
* automatic allowlisting

Human-reviewed eligibility is preferable for MVP.

---

## Phase 3 begins here

### PR 4 — SQLite ledger, positions and P&L

Do this **before exchange order mutation**.

Implement the financial truth layer:

```text
ledger_entries
orders
order_state_transitions
fills
positions
risk_decisions
strategy_intents
feature_snapshots
reconciliation_runs
```

You do not need all 25 planned tables.

Use SQLite + Alembic now.

Implement these ledger events:

```text
ORDER_RESERVED
ORDER_RELEASED
FILL_APPLIED
FEE_APPLIED
POSITION_MARKED
```

Leave settlement/reconciliation adjustment sophistication until needed.

Hard requirements:

* append-only ledger
* idempotency key per financial event
* replay ledger → identical balances
* exact Decimal/fixed-point accounting
* positions derived from ledger
* realized/unrealized P&L
* fees
* reserved/open-order exposure

The normative model says balances must be reproducible from ledger replay and applying an event twice must never duplicate value.

This PR is larger than it looks. Don't combine it with execution.

---

### PR 5 — Central deterministic risk gateway

Implement **one** function boundary:

```python
RiskDecision evaluate(
    intent,
    market_state,
    portfolio,
    runtime_state,
    risk_limits,
)
```

Execution must accept **only approved decisions**, not arbitrary intents.

Must-have rules:

* demo mode
* approved market
* active exchange/market
* healthy/fresh book
* non-expired intent
* valid price/count
* $5 max per-order risk
* per-market exposure
* aggregate exposure
* daily loss
* drawdown
* open-order limit
* order-rate budget
* time-to-close cutoff
* kill switch
* unresolved-reconciliation blockade

Those are frozen requirements, not optional design ideas.

### Ruthless treatment of scenario risk

Don't build a general scenario engine yet.

For the initial one-market MVP:

* worst-case liability = deterministic
* correlation group = reviewed static identifier
* aggregate same-underlying exposure conservatively
* treat everything in the group as moving adversely together

This is conservative and satisfies the authority boundary while avoiding a huge scenario-modeling project.

Later you can make it sophisticated.

---

### PR 6 — Local simulated execution + order state machine

Before calling Kalshi's mutation API, prove the entire internal pipeline.

Implement:

```text
TradeIntent
→ RiskDecision
→ simulated submission
→ ACKNOWLEDGED
→ OPEN
→ PARTIALLY_FILLED/FILLED/CANCELLED
→ ledger
→ position
→ P&L
```

Use the exact state-machine semantics already frozen in the repo, including `OUTCOME_UNKNOWN` and `RECONCILING`.

The simulator only needs:

* limit order
* post-only behavior
* partial fill
* full fill
* cancel
* fees
* deterministic replay

It does **not** need realistic queue simulation yet.

A deliberately conservative fill model is fine.

### Gate

Do not start PR 7 until randomized/property tests demonstrate:

```text
filled <= submitted
remaining >= 0
cash reconstructs exactly
position reconstructs exactly
risk-approved exposure never exceeds limits
duplicate fill event != duplicate money
```

At this point you have a **local paper-trading kernel**.

---

## Phase 4: the dangerous boundary

### PR 7 — Narrow demo order mutation API

Expand the existing REST client, but resist creating a generic execution client.

Expose only something like:

```python
create_limit_order(...)
cancel_order(...)
get_order(...)
list_open_orders(...)
get_fills(...)
get_positions(...)
get_balance(...)
```

For MVP:

* demo hostname permanently hard-coded
* limit only
* post-only only
* no amend initially
* globally unique `client_order_id`
* no arbitrary method/path interface
* retry policy differentiates pre-transmission vs ambiguous post-transmission failures
* never blindly retry an ambiguous create

The local order must be written as `SUBMISSION_PENDING` **before transmission**.

If acknowledgement is uncertain:

```text
SUBMISSION_PENDING
→ OUTCOME_UNKNOWN
→ RECONCILING
```

Never:

```text
timeout → shrug → submit another order
```

This is the PR that deserves the nastiest adversarial review.

---

### PR 8 — Reconciliation + first tiny demo order

This is your **FIRST PAPER TRADE milestone**.

Build reconciliation for:

```text
local open orders ↔ exchange open orders
local fills       ↔ exchange fills
local positions   ↔ exchange positions
local balance     ↔ exchange balance
```

Run it:

* startup
* reconnect
* uncertain submission
* before shutdown

On discrepancy:

```text
TRADING_SUSPENDED_RECONCILIATION_REQUIRED
```

No auto-fixing.

Then add a deliberately boring operator-run acceptance command:

```bash
kalshi-bot demo-smoke-order --ticker ... --price ... --count 1
```

or equivalent.

It should:

1. verify demo mode
2. get healthy book
3. construct a test/acceptance intent
4. pass the real risk gateway
5. submit **one tiny post-only demo order**
6. confirm acknowledgement
7. cancel it
8. verify cancellation
9. reconcile
10. prove no residual exposure/order

Then separately exercise a controlled demo fill when practical.

### Milestone

After PR 8 you can truthfully say:

> **The execution and accounting stack has completed a safe end-to-end Kalshi demo order lifecycle.**

But I would **not call that the MVP yet**, because it's operator-driven.

---

## Phase 5

### PR 9 — Minimal feature snapshot + passive spread v0.1

Do not build an alpha lab.

Features required for v0.1:

```text
best bid
best ask
spread
midpoint
top-level size
book age
time to close
current inventory
```

That's enough.

Strategy:

```text
IF market eligible
AND book healthy
AND spread >= threshold
AND inventory below limit
AND no existing equivalent quote
THEN emit one passive post-only TradeIntent
```

Cancel when:

* book stale
* market no longer eligible
* quote too old
* best price moved enough
* time-to-close cutoff reached
* risk/kill switch trips

The contract already calls for exactly this basic behavior: passive post-only bids, inventory caps, stale cancellation, quote aging and no quoting near settlement.

### Expectancy without boiling the ocean

You **cannot completely defer quote expectancy**, because the contract says every passive quote must record it from the first quote.

But make v0.1 deliberately primitive:

```text
edge_model_version = passive-v0.1-conservative

P(fill) = conservative bounded estimate
gross spread = exact
fees = exact/current configured model
adverse selection = fixed conservative haircut
inventory cost = fixed deterministic function
settlement risk = fixed deterministic function
cancel/reprice cost = configured conservative amount
```

Persist the full decomposition.

Don't claim it predicts edge well.

### Queue state

Same treatment.

Because every passive quote needs queue-state evidence, record:

* displayed same-price size
* bounded estimated size ahead
* lower/upper queue bound
* assumption/version

If actual queue position is unknowable:

```text
lower = 0
upper = displayed_size
quality = UNCERTAIN
```

That matches the contract's explicit requirement that uncertainty remain uncertainty rather than being fabricated into a favorable estimate.

---

### PR 10 — Autonomous runtime + MVP acceptance

Now wire the vertical loop:

```text
startup
↓
reconciliation
↓
market discovery
↓
eligibility
↓
order-book snapshot
↓
WS + health
↓
feature snapshot
↓
passive strategy
↓
TradeIntent
↓
risk
↓
execution
↓
order-state machine
↓
fills
↓
ledger / positions / P&L
↓
continuous reconciliation
```

Add graceful shutdown:

```text
kill strategy
→ block new intents
→ cancel managed orders
→ process late fills
→ reconcile
→ flush persistence
→ stop
```

The initial runtime should support **exactly one active strategy** and ideally **one market at a time** initially.

MVP acceptance test:

> Start from a clean database, automatically select one explicitly approved Kalshi crypto demo market, build a healthy book, generate a passive quote, pass deterministic risk, place/manage the order, process a cancellation or fill, update exact accounting, reconcile with Kalshi, shut down, restart, and reconcile to the identical state without duplicate orders or ledger value.

When that passes, **that's MVP v0.1**.

---

# What I'd deliberately postpone

This is where you save most of the schedule.

**Do not put these on the critical path to MVP:**

* OpenRouter / AI agents
* external Binance/CoinGecko reference feeds
* sophisticated market archetype classification
* empirical queue calibration
* sophisticated fill-probability model
* 5/30/60-second markout engine
* toxicity classification
* book-imbalance research
* historical replay UI/CLI
* generalized strategy plugin architecture
* multiple simultaneous strategies
* multiple sophisticated correlation scenarios
* dynamic market allowlisting
* automatic strategy promotion
* dashboard/web frontend
* production support of any kind
* PostgreSQL
* distributed services
* RFQs
* amend-order optimization
* elaborate observability stack
* automated parameter optimization
* 30-day evaluation tooling

These remain important **evaluation/hardening** work, but shouldn't stop the first autonomous demo loop.

## One important distinction

There are really three milestones:

```text
PR 6
LOCAL PAPER KERNEL
Simulation + risk + exact accounting work end-to-end.

PR 8
FIRST KALSHI DEMO TRADE
Tiny real demo order can be submitted/cancelled/reconciled.

PR 10
MVP
Bot autonomously generates and safely manages its own passive demo quote.
```

That distinction will keep “first trade” from turning into “we need to finish every research feature first.”

## Suggested PR boundaries

I would keep the sequence exactly like this:

1. `feat: add exact order-book snapshots and price models`
2. `feat: reconstruct demo books from websocket deltas`
3. `feat: add deterministic market eligibility and data-health gates`
4. `feat: add sqlite ledger, positions, and exact pnl accounting`
5. `feat: add centralized deterministic risk gateway`
6. `feat: add simulated execution and persistent order state machine`
7. `feat: add narrow Kalshi demo order lifecycle API`
8. `feat: add reconciliation and demo-order acceptance flow`
9. `feat: add passive-spread v0.1 strategy and quote expectancy`
10. `feat: wire autonomous demo paper-trading MVP`

I'd also make **PRs 4–8 merge-blocking on adversarial review**. That's where a subtle bug changes from “bad market-data output” to “incorrect orders/accounting.”

The central design rule throughout should be: **make the models simple; don't weaken the invariants.** The repo already has strong contracts. The fastest route is to implement conservative v0.1 versions behind those contracts rather than expanding the contracts or implementing research-grade sophistication prematurely.
