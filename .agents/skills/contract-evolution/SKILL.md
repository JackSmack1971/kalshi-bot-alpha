---
name: contract-evolution
description: Use only when the user explicitly asks for a multi-agent review of a frozen schema/contract change. Drafts a proposal, then independently checks breaking-change versioning, downstream dependents, and authority-sensitive fields before handing the result to a human. Never activates configuration or fabricates approval.
---

# Multi-agent contract evolution

## Propose

Follow `propose-contract-change` for the user's requested schema/contract change. Produce a reviewable proposal only. If higher-precedence authority blocks the change, stop and report the conflict.

## Check

After the proposal exists, run three independent checks concurrently and wait for all:

1. A general reviewer decides whether the proposal is breaking and, if so, whether it uses an already-established explicit versioning mechanism rather than in-place semantic mutation.
2. `architecture-boundary-verifier` checks all existing source, tests, downstream schemas, docs, examples, and fixtures that depend on the touched field(s), including whether dependents were updated coherently.
3. `security-finding-reviewer` checks authority-sensitive fields: risk limits, approval/promotion state, credential/transport config, and the AI/deterministic-authority boundary.

Each check reports `pass`, `fail`, or `needs-human-approval`, with concrete findings. A failed or indeterminate check blocks the proposal from being described as review-ready. No result is itself human approval.


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `proposal_result`, `review_verdict`, `reviewer_disagreement`, `workflow_result`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
