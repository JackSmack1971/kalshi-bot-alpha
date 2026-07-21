---
name: swarm-status-briefing
description: Produce a read-only synthesis of the domain-engineering swarm's current state by combining docs/IMPLEMENTATION_STATUS.md, .claude/memory/INDEX.md, and every .claude/memory/domains/*.md log. Trigger on "what's the state of the swarm", "what's in flight", "any open blockers", "catch me up", session handoff, or before dispatching new work across more than one domain. Used directly by a human, by phase-integrator's own routing step, or by any agent picking up mid-stream work. Does not replace phase-integrator's dispatch decision and never edits any file — pure synthesis.
---

# Swarm status briefing

1. Read `docs/IMPLEMENTATION_STATUS.md` for the active phase, its
   exit-criteria table, known gaps, and the phase ledger.
2. Read `.claude/memory/INDEX.md` in full. Extract every entry that has
   no later entry resolving it, grouped by tag: `[BLOCKER]`,
   `[QUESTION]`, `[HANDOFF]`, `[DECISION-NEEDED]`, `[INVARIANT-RISK]`,
   `[FINDING]`.
3. Skim each `.claude/memory/domains/*.md` log for its most recent
   entries — `Status` field and anything that contradicts what
   `INDEX.md` implies is already resolved.
4. Cross-check: does a domain log mark a task `done` while `INDEX.md`
   still lists a `[BLOCKER]`/`[DECISION-NEEDED]` for that same domain
   unresolved? Flag the discrepancy — do not resolve it yourself.
5. Produce the report below.
6. This skill is strictly read-only: never append to, edit, or resolve
   an `INDEX.md` or domain-log entry while producing this briefing. A
   finding that warrants escalation is handed back to the caller to
   record via `memory-domain-sync`, not written here.

Final swarm status briefing:

```text
Swarm status briefing

Active phase
- Phase, and whether any in-flight work already exceeds its scope.

Open items by tag
- [BLOCKER] / [QUESTION] / [HANDOFF] / [DECISION-NEEDED] / [INVARIANT-RISK] / [FINDING]
  — domain, date, one-line description, action or decision that resolves it.

Per-domain last activity
- One line per domain log that has an entry, newest first.

Discrepancies
- Domain log vs INDEX.md mismatches found in step 4, if any.
```
