---
name: memory-domain-sync
description: Read and append compliant stigmergic memory for domain-agent tasks and handoffs. Use when a procedure requires .codex/memory coordination. Not for changing PROTOCOL.md or replacing domain invariant checks.
---

# Memory domain sync

The domain-engineering swarm has no direct messaging channel between
agents — each has its own context window. `.codex/memory/` is the only
coordination medium. This skill is the mechanical protocol every domain
agent follows to read and write it correctly; `.codex/memory/PROTOCOL.md`
is the source of truth this skill implements — read it in full once per
session if you have not already.

## Before starting work (read)

1. Read your own domain log, `.codex/memory/domains/<domain>.md`,
   starting from the most recent entries.
2. Read `.codex/memory/INDEX.md` in full. Note every entry tagged for
   your domain — `[BLOCKER]`, `[QUESTION]`, `[HANDOFF]`,
   `[DECISION-NEEDED]`, `[INVARIANT-RISK]`, `[FINDING]` — that has no
   later entry resolving it.
3. Read the domain log(s) of any upstream domain you consume, per
   `.codex/policies/architecture/dependency-boundaries.md` (e.g.
   `strategy` reads `market-data`; `risk` reads `strategy` and
   `accounting-ledger`).
4. If an unresolved `[BLOCKER]` or `[DECISION-NEEDED]` entry directly
   blocks the requested task, stop and report it — do not work around
   it or proceed as if it were resolved.

## After finishing work (write)

5. Append exactly one entry to your own domain log, in this shape (from
   `PROTOCOL.md`):

   ```markdown
   ## <ISO date> — <domain> — <short title>
   Task: <what was asked>
   Touched: <files changed, or "none — read-only">
   Verified: <exact commands run + results, or "none — planning only">
   Status: <done | blocked | needs-human-approval | handoff | refused-scope>
   Notes: <what the next reader needs to know>
   ```

   Write one for every task with an observable effect: a code change, a
   test added, a finding, or a refusal. A read-only investigation still
   gets an entry if it produced a conclusion another agent should see.
   Put the exact command and its result in `Verified`, never a narrative
   ("ran `uv run pytest -q tests/risk` — 4 passed", not "risk logic
   looks solid").
6. If the task affects another domain's assumptions, creates a blocker,
   raises a question only a human or another specialist can resolve, or
   exposes a `AGENTS.md` safety-invariant risk, append a second entry —
   same shape, plus the matching tag in its title — to
   `.codex/memory/INDEX.md` in the same pass. Do not defer this.
7. Never edit or delete a prior entry, in either file. To correct one,
   append a new entry that references the original by date and title
   and states the correction — the history of being wrong is itself
   signal.
8. Never silently resolve an open `INDEX.md` entry. Append a follow-up
   entry that references the original by date and title and states the
   resolution or the remaining gap.

## What this skill does not cover

- It does not decide *what* to check for your domain — that is your own
  agent prompt's non-negotiable invariants and active-phase gate.
- It does not authorize you to write outside `.codex/memory/**` and
  your own owned paths.
- Memory entries carry no authority under `AGENTS.md`'s governing-authority
  split. An entry is a working note, never a human approval, ledger
  event, reconciliation resolution, or active-configuration record.

For mechanical append and validation, use `python .codex/scripts/memory_sync.py`
with explicit fields. Use `python .codex/scripts/swarm_status.py --json` for
counts and latest statuses. These helpers do not replace reading the protocol,
upstream logs, or unresolved entries.


## Observable workflow and telemetry

Emit one started record and one terminal record with `.codex/scripts/skill_telemetry.py` for each invocation. Emit the consequential events below when that decision occurs; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `unresolved_item`, `domain_append_result`, `index_escalation`, `protocol_violation`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
