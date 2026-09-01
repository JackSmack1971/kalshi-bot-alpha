---
name: swarm-standup
description: Use only when the user explicitly asks for a multi-agent/swarm standup or parallel handoff check. Produces a read-only current-state briefing plus an independent memory-sync drift check. Not for ordinary status questions where the single-agent swarm-status-briefing skill is sufficient.
---

# Multi-agent swarm standup

Run two read-only tasks concurrently and wait for both:

1. A general subagent follows `swarm-status-briefing` exactly and prioritizes unresolved `[BLOCKER]` and `[DECISION-NEEDED]`, then `[INVARIANT-RISK]`, then `[QUESTION]`/`[HANDOFF]`, followed by one line per domain's latest activity.
2. A general read-only subagent inspects `git status --short` and `git diff --stat`, compares touched `src/`, `schemas/`, and `config/` paths with the ownership table in `.codex/agents/phase-router.toml` and recent `.codex/memory/domains/*.md` entries, and reports any missing domain-memory coverage as a **memory-sync gap**, not a code defect.
3. Run `python .codex/scripts/memory_coverage.py <product-paths...>` for the mechanical coverage check. A `memory-sync-gap` result is incomplete evidence, never a clean result.

Do not edit memory while briefing. Return both reports and surface contradictions without resolving them silently.


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `briefing_result`, `memory_coverage_gap`, `contradiction_found`, `worker_failure`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
