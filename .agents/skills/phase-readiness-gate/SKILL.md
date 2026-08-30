---
name: phase-readiness-gate
description: Use only when the user explicitly asks for a multi-agent phase-readiness gate, asks whether the active phase is actually done using independent auditors, or requests a swarm phase-exit review. Runs independent phase, safety, architecture, and memory-status audits and synthesizes evidence. Never edits docs/IMPLEMENTATION_STATUS.md and never approves a phase.
---

# Multi-agent phase readiness gate

## Audit

Launch these four independent audit tasks concurrently, then wait for all four:

1. A general subagent follows `phase-exit-audit` and classifies every deliverable/exit criterion using the exact `AGENTS.md` completion vocabulary: implemented, tested, mocked, simulated, partially implemented, unverified, deferred. It must not edit `docs/IMPLEMENTATION_STATUS.md`.
2. `security-adversarial-reviewer` follows `audit-safety-invariants` against the full repository state and records exact output of `python scripts/verify_demo_only.py` if that script exists. Missing required script is a gap, not a pass.
3. `architecture-boundary-verifier` verifies dependency and capability reachability against the full current `src/` tree.
4. A read-only general subagent follows `swarm-status-briefing` and reports unresolved `[BLOCKER]`, `[DECISION-NEEDED]`, `[INVARIANT-RISK]`, plus domain logs whose latest status is blocked or needs human approval.

## Synthesize

After all four return, synthesize without reconciling away disagreements. Order the report as: blocking gaps, invariant risks, disagreements/inconclusive evidence, then overall evidence picture.

Never state that the phase is approved. The strongest permissible conclusion is `evidence-ready-for-human-phase-decision`; otherwise report `not-ready` or `indeterminate`.
