# Implementation Status

Read this before planning or editing (per `CLAUDE.md`). Implement only
the active phase; do not build later-phase behavior early.

- **Active phase:** Phase 0 — Contracts and safety model
- **Phase 0 state:** Delivered — **awaiting human review and approval**
  (including ADR-0001 acceptance). Phase 1 must not begin until that
  approval is durably recorded here.
- **AI phases:** not started (AI Phase A is gated on stable deterministic
  simulation, risk, ledger, and replay evidence — Phases 3+).

## Phase 0 deliverables

| Deliverable (blueprint §12) | Artifact(s) |
| --- | --- |
| Architecture decision record | `docs/adr/ADR-0001-blueprint-v3-baseline.md` (status: Proposed) |
| Demo-only endpoint policy | `docs/SAFETY_MODEL.md` §1, `scripts/verify_demo_only.py`, `tests/unit/test_demo_only_policy.py` |
| Credential policy | `docs/SAFETY_MODEL.md` §2–3, `.env.example` |
| Domain model definitions | `docs/DATA_MODEL.md`, `schemas/trade-intent.schema.json` |
| Order-state machine | `docs/DATA_MODEL.md` §3 (full transition table) |
| Risk-limit schema | `schemas/risk-limits.schema.json`, `config/risk/conservative.yaml`, `docs/RISK_MODEL.md` |
| Failure taxonomy | `docs/FAILURE_TAXONOMY.md` |
| Paper-trading protocol | `docs/PAPER_TRADING_PROTOCOL.md` |
| Market-archetype schema | `schemas/market-archetype.schema.json`, `docs/MICROSTRUCTURE_CONTRACT.md` §1 |
| Quote-expectancy schema | `schemas/quote-expectancy.schema.json`, `docs/STRATEGY_SPEC.md` §3 |
| Queue-state and calibration contract | `docs/MICROSTRUCTURE_CONTRACT.md` §2 |
| Markout and toxicity taxonomy | `docs/MICROSTRUCTURE_CONTRACT.md` §4 |
| External-reference observation policy | `docs/MICROSTRUCTURE_CONTRACT.md` §5 |
| Correlated scenario-risk contract | `docs/RISK_MODEL.md` §3 |
| Immutable experiment-registry contract | `docs/RESEARCH_PROTOCOL.md` §1, `schemas/experiment-registration.schema.json` |
| Statistical sufficiency and multiple-testing policy | `docs/RESEARCH_PROTOCOL.md` §2–4 |

## Phase 0 exit criteria

| Exit criterion | Evidence |
| --- | --- |
| Production endpoints are explicitly forbidden | `docs/SAFETY_MODEL.md` §1; `scripts/verify_demo_only.py` scan passes; detection of non-demo hosts proven by `tests/unit/test_demo_only_policy.py` |
| All state transitions and invariants are documented | `docs/DATA_MODEL.md` §3 (order states), §4 (ledger), §6 (traceability); order-book quality states in `docs/MICROSTRUCTURE_CONTRACT.md`; failure states in `docs/FAILURE_TAXONOMY.md` |
| No trading code exists yet | `src/kalshi_bot/` contains only the package marker; asserted by `test_no_trading_code_exists_in_phase_0` |
| Signal confidence, fill probability, and expected net edge are separate fields | Distinct required fields in `schemas/trade-intent.schema.json` and `schemas/quote-expectancy.schema.json` |
| Passive-spread edge is defined by a versioned expectancy decomposition | `docs/STRATEGY_SPEC.md` §3; required `edge_model_version` in both schemas |
| Promotion requires sample and diversity gates in addition to elapsed time | `docs/PAPER_TRADING_PROTOCOL.md` §2, §4; `docs/RESEARCH_PROTOCOL.md` §3; `minimum_evidence` required in `schemas/experiment-registration.schema.json` |

## Known gaps and deferred work

- `README.md` was intentionally removed by the repository owner and has
  not been recreated.
- `docs/RUNBOOK.md` is a Phase 6 deliverable (not started).
- Correlation-group definitions (`scenario.correlation_groups_version`)
  and the frozen `edge_model_version` are deliberately null until their
  owning phases (pre-Phase-5).
- Alembic is not configured yet; `migrations/` is a placeholder until
  Phase 2–3 introduces persistence.
- CI workflow wiring for `scripts/verify_demo_only.py` and pytest is not
  yet set up (no `.github/workflows/` exists in this repository).

## Phase ledger

| Phase | Status |
| --- | --- |
| 0 — Contracts and safety model | Delivered; pending human review |
| 1 — Read-only connectivity | Not started |
| 2 — Order-book integrity | Not started |
| 3 — Portfolio and simulated execution | Not started |
| 4 — Demo order lifecycle | Not started |
| 5 — Passive spread strategy | Not started |
| 6 — Evaluation and hardening | Not started |
| AI A–D | Not started (gated) |
