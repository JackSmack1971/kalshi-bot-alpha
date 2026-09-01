---
name: phase-readiness-gate
description: Use only when the user explicitly asks for a multi-agent phase-readiness gate, asks whether the active phase is actually done using independent auditors, or requests a swarm phase-exit review. Runs independent phase, safety, architecture, and memory-status audits and synthesizes evidence. Never edits docs/IMPLEMENTATION_STATUS.md and never approves a phase.
---

# Multi-agent phase readiness gate

## Audit

Launch these four independent audit tasks concurrently, then wait for all four:

1. A general subagent follows `phase-exit-audit` and classifies every deliverable/exit criterion using the exact `AGENTS.md` completion vocabulary: implemented, tested, mocked, simulated, partially implemented, unverified, deferred. It must not edit `docs/IMPLEMENTATION_STATUS.md`.
2. `security-finding-reviewer` follows `audit-safety-invariants` against the full repository state and records exact output of `python scripts/verify_demo_only.py` if that script exists. Missing required script is a gap, not a pass.
3. `architecture-boundary-verifier` verifies dependency and capability reachability against the full current `src/` tree.
4. A read-only general subagent follows `swarm-status-briefing` and reports unresolved `[BLOCKER]`, `[DECISION-NEEDED]`, `[INVARIANT-RISK]`, plus domain logs whose latest status is blocked or needs human approval.

## Synthesize

After all four return, synthesize without reconciling away disagreements. Order the report as: blocking gaps, invariant risks, disagreements/inconclusive evidence, then overall evidence picture.

If any auditor fails, times out, or returns indeterminate, preserve that lane as
unknown and report `not-ready`; never synthesize a pass from remaining lanes.

Never state that the phase is approved. The strongest permissible conclusion is `evidence-ready-for-human-phase-decision`; otherwise report `not-ready` or `indeterminate`.


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `lane_verdict`, `lane_failure`, `cross_lane_disagreement`, `synthesis_result`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
