---
name: memory-domain-sync
description: Use at the start and end of any domain-engineering agent's task (transport-safety, market-data, strategy, risk, accounting-ledger, runtime-execution, research-integrity, openrouter-agents, governance-approvals, security, architecture, phase-integration) to read the stigmergic memory substrate before acting and append a compliant entry after finishing. Trigger whenever an agent's own procedure says "read/append to .claude/memory" or when coordinating with another domain agent through memory instead of a direct message. NOT for authoring or amending the protocol itself (that is `.claude/memory/PROTOCOL.md`, a rules-specialist/human concern) and NOT a substitute for the domain-specific invariant checks each agent's own system prompt requires.
---

# Memory domain sync

The domain-engineering swarm has no direct messaging channel between
agents — each has its own context window. `.claude/memory/` is the only
coordination medium. This skill is the mechanical protocol every domain
agent follows to read and write it correctly; `.claude/memory/PROTOCOL.md`
is the source of truth this skill implements — read it in full once per
session if you have not already.

## Before starting work (read)

1. Read your own domain log, `.claude/memory/domains/<domain>.md`,
   starting from the most recent entries.
2. Read `.claude/memory/INDEX.md` in full. Note every entry tagged for
   your domain — `[BLOCKER]`, `[QUESTION]`, `[HANDOFF]`,
   `[DECISION-NEEDED]`, `[INVARIANT-RISK]`, `[FINDING]` — that has no
   later entry resolving it.
3. Read the domain log(s) of any upstream domain you consume, per
   `.claude/rules/architecture/dependency-boundaries.md` (e.g.
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
   exposes a `CLAUDE.md` safety-invariant risk, append a second entry —
   same shape, plus the matching tag in its title — to
   `.claude/memory/INDEX.md` in the same pass. Do not defer this.
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
- It does not authorize you to write outside `.claude/memory/**` and
  your own owned paths.
- Memory entries carry no authority under `CLAUDE.md`'s governing-authority
  split. An entry is a working note, never a human approval, ledger
  event, reconciliation resolution, or active-configuration record.
