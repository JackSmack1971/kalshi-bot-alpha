# ADR-0001 — Adopt Blueprint v3 as the architecture baseline

- **Status:** Accepted
- **Date:** 2026-07-20
- **Deciders:** repository owner

## Acceptance record

- **Acceptance date:** 2026-07-20
- **Decider:** Human repository owner
- **Basis:** explicit human review and approval of ADR-0001 with the
  amendments recorded in this document.

Acceptance requires all of the following:

1. a durable human approval record in this ADR (this section);
2. corresponding updates to `docs/IMPLEMENTATION_STATUS.md`;
3. Phase 0 marked accepted in the active-phase status and phase ledger
   in `docs/IMPLEMENTATION_STATUS.md`.

## Context

The repository contains a governance layer (`CLAUDE.md`,
`.claude/rules/`, `.claude/skills/`) and
`docs-dev/Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md`, but no
accepted architecture decision anchoring implementation. Phase 0
requires an architecture decision record before any trading code exists.

## Decision

1. **Blueprint v3 is the authoritative system contract.** Product scope
   (§1), safety architecture (§2), components (§5), runtime flow (§6),
   failure handling (§7), testing (§10), repository layout (§11),
   delivery phases (§12), evaluation protocol (§13), definition of done
   (§14), microstructure contract (§15), and OpenRouter baseline (§16)
   govern implementation, subordinate only to explicit user instruction
   and the safety invariants in `CLAUDE.md`. This ADR also incorporates
   `docs/SAFETY_MODEL.md` and the governance invariants in `CLAUDE.md`
   as co-equal binding sources for the deterministic authority split
   and demo-only controls.
2. **Demo-only, forever, for this project.** Only the two demo endpoints
   in `docs/SAFETY_MODEL.md` are reachable. No production switch,
   dormant production endpoint, or generic environment-parameterized
   client will ever be added within this project.
3. **Deterministic authority split.** AI observes/proposes; deterministic
   code calculates/authorizes/executes/reconciles/accounts; humans
   approve strategy, risk, eligibility, reconciliation, configuration,
   and promotion changes.
4. **Technology stack** (blueprint §3): Python 3.12+, `asyncio`, `httpx`,
   `websockets`, Pydantic v2, SQLAlchemy 2.x, SQLite (MVP), Alembic,
   Typer, structured JSON logging, pytest + pytest-asyncio + Hypothesis
   + respx, Ruff + mypy + Bandit. OpenRouter is the exclusive LLM
   gateway, via an application-owned `httpx` adapter; no vendor SDKs.
5. **Deployment shape:** one deterministic local trading process with
   internal module boundaries; the AI control plane is a separate local
   process consuming immutable sanitized evidence bundles.
6. **Delivery order:** Phases 0–6 strictly sequenced per §12, AI Phases
   A–D gated behind their deterministic prerequisites, tracked in
   `docs/IMPLEMENTATION_STATUS.md`. No later-phase behavior is built
   early.

## Consequences

- Accidental production trading requires deliberate architectural
  change, which is reviewable and forbidden — not a config typo.
- Every future subsystem change must cite the blueprint section it
  implements; deviations require a new ADR.
- The frozen Phase 0 schemas (`schemas/*.schema.json`) are immutable
  contracts. Any change after acceptance requires a new schema version
  and a new ADR, or an approved `propose-contract-change` workflow that
  produces an ADR. Silent edits are forbidden and must be rejected by
  the Phase exit audit.

## Alternatives considered

- *Config-switched environments (demo/prod):* rejected; violates the
  fail-closed invariant and blueprint §2.1.
- *Direct vendor LLM SDKs:* rejected; blueprint §16 and CLAUDE.md make
  OpenRouter the single gateway.
- *Starting with connectivity code and documenting later:* rejected;
  Phase 0 exit criteria explicitly require contracts before trading
  code.
