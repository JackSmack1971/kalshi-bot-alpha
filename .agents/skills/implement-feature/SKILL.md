---
name: implement-feature
description: Use only when the user explicitly asks for a multi-agent/swarm implementation of a bounded feature, fix, or refactor inside the active phase. Routes work to one or more domain-engineering subagents in dependency order, then independently verifies architecture, safety when sensitive, and repository-native tests. Not for ordinary single-agent implementation; use safe-change-preflight/implement-safe-change instead.
---

# Multi-agent implement feature

This skill replaces the former Claude JavaScript workflow with native Codex subagent orchestration.

## Mandatory entry conditions

1. The user explicitly requested multi-agent/swarm orchestration.
2. Read `AGENTS.md`, `docs/IMPLEMENTATION_STATUS.md`, `.codex/memory/INDEX.md`, and `.codex/policies/architecture/dependency-boundaries.md`.
3. Do not implement beyond the active phase. If scope is outside it, return `out-of-scope` with evidence and stop.

## Route

Spawn `phase-router` to produce: `inScope`, `reason`, `sensitiveSurfaces`, and an ordered `tasks` list of `{domain, agentType, task}`. Allowed implementation roles are `transport-safety-engineer`, `market-data-engineer`, `strategy-engineer`, `risk-engineer`, `accounting-ledger-engineer`, `runtime-execution-engineer`, `research-integrity-engineer`, `openrouter-agent-engineer`, and `governance-approvals-engineer`.

Require upstream-to-downstream ordering when one domain's output feeds another. Do not begin implementation until routing is complete and in scope.

## Implement

For each routed task **sequentially in dependency order**, spawn the named domain role. Tell it to follow `safe-change-preflight`, `implement-safe-change`, and `memory-domain-sync` for its bounded task. Wait for that role to finish and inspect its result before starting a dependent task. If a role reports a blocker, failed required verification, or need for human approval, stop downstream writes and surface the blocker.

## Independent verification

If a routed worker fails or returns partial output, stop dependent tasks,
record the failed result, and hand the unresolved task back to the human. Never
treat a missing worker result as an empty successful task.

After implementation, spawn `architecture-boundary-verifier` against the uncommitted diff. If `sensitiveSurfaces` is nonempty, also spawn `security-finding-reviewer` to follow `audit-safety-invariants`. These read/review tasks may run concurrently because neither should repair the implementation being reviewed.

Any verifier result other than PASS blocks a ready verdict. Do not ask the verifier to repair its own finding.

## Test

Run `verify-change` against the final diff. Narrow decisive checks first, then repository-required broader checks. Record exact commands, exit results, skipped checks, and reasons.

## Completion

Return exactly one workflow status: `out-of-scope`, `needs-attention`, or `ready-for-human-review`. `ready-for-human-review` requires all independent verifiers and required checks to pass. It is not human approval and does not complete a phase.


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `phase_gate`, `domain_task_routed`, `subagent_result`, `verifier_result`, `workflow_result`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
