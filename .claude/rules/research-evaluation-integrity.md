---
paths:
  - "src/research/**/*.py"
  - "src/evaluation/**/*.py"
  - "src/analytics/**/*.py"
  - "src/experiments/**/*.py"
  - "src/microstructure/**/*.py"
  - "notebooks/**/*.ipynb"
  - "research/**/*.md"
  - "tests/evaluation/**/*.py"
  - "tests/research/**/*.py"
---

# Research and evaluation integrity

- Never treat displayed spread as collectible edge.
- Represent unavailable queue priority with bounded, calibrated estimates; record assumptions, bounds, and calibration version.
- External crypto references are observational only and cannot bypass strategy or risk gates.
- Make reference freshness, divergence, and unavailability explicit.
- Segment results by deterministic, versioned market archetype.
- Keep operational quality, data integrity, execution quality, adverse selection, economics, and risk concentration as separate dimensions.
- Preserve required markout horizons, classification rules, toxicity versions, and evidence.
- Confirmatory experiments require preregistration, frozen versions, holdout evidence, sample and diversity gates, and multiple-testing disclosure.
- Label exploratory findings as exploratory and retain every tested variant, not only winners.
- Account for clustering, autocorrelation, effective sample size, and repeated observations.
- Missing required coverage yields `INCONCLUSIVE`, never an inferred favorable result.
- Numerical AI claims must originate from deterministic analysis tools, not model arithmetic.

Deterministic policy assigns exactly one state:

```text
OPERATIONALLY_INVALID
ECONOMICALLY_NEGATIVE
INCONCLUSIVE
PROMISING_EXPLORATORY
CONFIRMATORY_PASS
```

AI may explain these states but must not assign, promote, override, or reinterpret them.
