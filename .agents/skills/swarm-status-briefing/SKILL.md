---
name: swarm-status-briefing
description: Produce a read-only swarm-state synthesis from implementation status, memory index, and domain logs. Use for blockers, in-flight work, handoffs, or multi-domain routing. Never edits files or replaces phase-integrator dispatch.
---

# Swarm status briefing

Run `python .codex/scripts/swarm_status.py --json` first for deterministic
unresolved counts and latest domain statuses, then inspect source entries needed
to explain them. If it fails, report partial evidence explicitly.

1. Read `docs/IMPLEMENTATION_STATUS.md` for the active phase, its
   exit-criteria table, known gaps, and the phase ledger.
2. Read `.codex/memory/INDEX.md` in full. Extract every entry that has
   no later entry resolving it, grouped by tag: `[BLOCKER]`,
   `[QUESTION]`, `[HANDOFF]`, `[DECISION-NEEDED]`, `[INVARIANT-RISK]`,
   `[FINDING]`.
3. Skim each `.codex/memory/domains/*.md` log for its most recent
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


## Observable workflow and telemetry

Emit one started record and one terminal record with `.codex/scripts/skill_telemetry.py` for each invocation. Emit the consequential events below when that decision occurs; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `unresolved_counts`, `domain_latest_status`, `index_domain_discrepancy`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
