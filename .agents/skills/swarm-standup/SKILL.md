---
name: swarm-standup
description: Use only when the user explicitly asks for a multi-agent/swarm standup or parallel handoff check. Produces a read-only current-state briefing plus an independent memory-sync drift check. Not for ordinary status questions where the single-agent swarm-status-briefing skill is sufficient.
---

# Multi-agent swarm standup

Run two read-only tasks concurrently and wait for both:

1. A general subagent follows `swarm-status-briefing` exactly and prioritizes unresolved `[BLOCKER]` and `[DECISION-NEEDED]`, then `[INVARIANT-RISK]`, then `[QUESTION]`/`[HANDOFF]`, followed by one line per domain's latest activity.
2. A general read-only subagent inspects `git status --short` and `git diff --stat`, compares touched `src/`, `schemas/`, and `config/` paths with the ownership table in `.codex/agents/phase-integrator.toml` and recent `.codex/memory/domains/*.md` entries, and reports any missing domain-memory coverage as a **memory-sync gap**, not a code defect.

Do not edit memory while briefing. Return both reports and surface contradictions without resolving them silently.
