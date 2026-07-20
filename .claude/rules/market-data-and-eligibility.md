---
paths:
  - "src/market_data/**/*.py"
  - "src/markets/**/*.py"
  - "src/eligibility/**/*.py"
  - "src/strategies/**/*.py"
  - "src/config/**/*market*.py"
  - "tests/market_data/**/*.py"
  - "tests/markets/**/*.py"
  - "tests/eligibility/**/*.py"
---

# Market eligibility and data quality

Trade only markets admitted by a durable, reviewed, versioned policy.

- Do not rely on keyword matching alone.
- Preserve approved series, settlement terms, lifecycle state, and market-archetype version.
- Reject paused, closed, malformed, unsupported, stale, or insufficiently understood markets.
- Record eligibility decisions and policy versions.
- Strategy code must not mutate the allowlist.

Authoritative order-book states:

```text
INITIALIZING
HEALTHY
STALE
GAP_DETECTED
RESYNCING
UNAVAILABLE
```

Strategies may operate only on `HEALTHY` books. After disconnect, sequence gap, or inconsistency: mark affected books stale immediately, suspend new orders, resnapshot, rebuild, reconcile, and resume only after deterministic health restoration.

Missing external-reference data must become an explicit unavailable state, never a fabricated value or numeric zero. Preserve source timestamp, freshness, divergence, quality, provenance, and calculation timestamp.
