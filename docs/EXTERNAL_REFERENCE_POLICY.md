# External Reference Observation Policy

## Non-authoritative observation only (blueprint SS5.8.1)

The passive-spread strategy may observe external crypto markets for
toxicity detection, segmentation, and later research, but those feeds
never possess trading authority. No external reference feed may
directly or indirectly authorize, size, or trigger an order; it may
only inform features and research artifacts that a deterministic
strategy or risk component separately evaluates.

## Approved reference bundle contents

For supported underlyings, an approved reference bundle records:

- Liquid-exchange spot midpoint, preferably from a reviewed primary
  venue such as Binance where accessible.
- Reference timestamp and age.
- Short-horizon realized volatility.
- 24-hour volume and change.
- Cross-source spot deviation using a slower metadata/reference source
  such as CoinGecko.
- Kalshi threshold distance.
- Time remaining.
- Kalshi-implied probability movement relative to spot movement.

## Normalized state variable

For threshold markets, when inputs are valid:

```text
z = (K - S_t) / (sigma_t * sqrt(T))
```

This is a segmentation and toxicity feature, not a complete probability
model, and must never be presented or consumed as one.

## Source roles

- A liquid primary exchange (for example Binance, where accessible)
  supplies the low-latency microstructure reference.
- CoinGecko may support identity, metadata, broad historical context,
  and source-divergence checks, but must never be the primary
  low-latency microstructure reference.

## Freshness and missing-data handling

Reference data receives its own quality states and freshness limits.
Missing, stale, or divergent external data must be represented
explicitly and may cause the relevant analytical feature to become
unavailable; it must never silently substitute a fabricated value
(for example, a missing volatility estimate must never silently become
`0`, since `0` is itself a meaningful value this policy must not
confuse with "unavailable").

## Non-goals of this phase

No external-reference fetcher, no reference bundle schema, and no
normalized-state-variable calculation exist yet. Phase 0 makes no
network call of any kind, including to Binance or CoinGecko. This
policy fixes the authority boundary and the missing-data discipline
that the implementing phase (blueprint SS5.8.1) must satisfy; the
reference-bundle schema itself is deferred (see
`docs/DATA_MODEL.md` "Models deferred to later phases").
