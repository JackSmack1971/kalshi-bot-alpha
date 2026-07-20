# Market-Microstructure Contracts

Normative Phase 0 contract covering the market-archetype schema, the
queue-state and calibration contract, the markout and toxicity taxonomy,
and the external-reference observation policy. Sources: blueprint
§5.5.1, §5.6, §5.8.1, §15.1;
`.claude/rules/research-evaluation-integrity.md`,
`market-data-and-eligibility.md`.

## 1. Market-archetype schema

Every eligible market receives a versioned `market_archetype_id`
(`schemas/market-archetype.schema.json`). "Crypto market" alone is not
an analytically sufficient category. The classifier is deterministic and
versioned; classification dimensions:

- Underlying asset.
- Contract structure: `directional`, `threshold`, `range`, or another
  reviewed type.
- Strike/threshold distance bucket.
- Time-to-settlement bucket.
- Market age bucket.
- Time-of-day and day-of-week bucket.
- Spread regime.
- Visible-depth regime.
- External-reference volatility regime.
- Event-driven vs. routine market.

Every feature snapshot, strategy intent, order, fill, and evaluation
record preserves the archetype ID in effect at decision time. Reporting
must segment by archetype before presenting any aggregate.

## 2. Queue-state and calibration contract

Queue position is a first-class research object for every passive order
(`queue_state_snapshots`, `queue_calibrations`). Captured per order:

- Displayed size ahead at submission; same-price displayed size and its
  subsequent changes.
- Trades executed at the level; estimated cancellations ahead.
- Time spent at each queue estimate; estimated queue advancement.
- Queue percentile or bounded queue-position interval.
- Fill probability conditional on queue state, market archetype, and
  time to close.

Core diagnostic — queue-completion ratio:

```text
QCR = estimated volume consumed ahead / displayed size ahead at entry
```

Because exchange data may not identify individual queue priority, every
estimate carries **lower and upper bounds, explicit assumptions, and a
versioned calibration method**. Lower bounds never exceed upper bounds
(property-tested). Unavailable queue evidence is represented as
unavailable — never inferred to a favorable value.

## 3. Complementary-price consistency

YES/NO complementarity is tracked explicitly, never assumed: record the
complementarity residual, cross-side implied spread, best executable
synthetic probability, inconsistency duration, and the data-quality
state during it. Temporary inconsistencies are classified as
`DATA_ARTIFACT`, `THIN_BOOK_EFFECT`, `UNCONFIRMED_OPPORTUNITY`, or
`UNRESOLVED_ANOMALY`. Apparent cross-side arbitrage is never treated as
executable edge without deterministic validation against fees, latency,
and queue assumptions.

## 4. Markout and toxicity taxonomy

For each fill, compute signed realized spread at 5-, 30-, and 60-second
horizons:

```text
RealizedSpread_t = s × 2 × (P_fill − M_t)     s = +1 sell, −1 buy
```

Report median, 10th and 25th percentiles, expected shortfall,
positive-markout frequency, and segmentation by archetype and
time-to-close.

Fill classification (versioned rules; `toxicity_classifications`):

```text
BENIGN   TOXIC   STALE_QUOTE   LIFECYCLE   INVENTORY_REBALANCING   AMBIGUOUS
```

Every classification preserves its rules version and input evidence.

## 5. External-reference observation policy

External crypto feeds are **observational only** — segmentation and
toxicity inputs, never trading authority, and never a bypass of the
deterministic strategy and risk boundaries.

Approved reference bundle per supported underlying
(`external_reference_events`):

- Liquid-exchange spot midpoint from a reviewed primary venue.
- Reference timestamp and age.
- Short-horizon realized volatility; 24-hour volume and change.
- Cross-source spot deviation via a slower metadata source (e.g.
  CoinGecko — identity/metadata/divergence only, never the primary
  low-latency reference).
- Kalshi threshold distance and time remaining.
- Kalshi-implied probability movement relative to spot movement.

For threshold markets, when inputs are valid, compute the normalized
state variable `z = (K − S_t) / (σ_t √T)` — a segmentation and toxicity
feature, not a probability model.

Reference data has its own quality states and freshness limits. Missing,
stale, or divergent data is represented explicitly and may make the
dependent feature unavailable; it must never be silently substituted
with fabricated values, and a missing value never becomes a numeric
zero.

As of Phase 0, no external-reference fetcher, reference-bundle schema, or
normalized-state-variable calculation exists, and Phase 0 makes no
network call of any kind, including to Binance or CoinGecko; this
section fixes the authority boundary and missing-data discipline for the
implementing phase (blueprint §5.8.1).

## 6. Book-imbalance discipline

Book imbalance is a hypothesis requiring calibration, not an assumed
signal. Research must compare top-level, top-three-level,
distance-weighted, notional, and robust (largest-level-excluded)
variants, tested against midpoint movement, trade direction, fill
probability, and quote toxicity by regime.
