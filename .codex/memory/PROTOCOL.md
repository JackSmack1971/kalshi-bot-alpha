# Stigmergic Memory Protocol

Purpose: a file-based, asynchronous coordination substrate for the project's
domain-engineering agent swarm (`.codex/agents/*.toml` custom roles). Modeled on
stigmergy: agents do not message each other directly. Each agent leaves a
trace in the shared environment, and other agents read those traces before
acting. The environment — this directory — is the coordination medium.

This directory is Codex CLI orchestration tooling, not a Phase 0+ product
artifact. It carries no authority under AGENTS.md's governing-authority
split: nothing written here is a human approval, a ledger event, a
reconciliation resolution, active configuration, or evidence that a phase
exit criterion is satisfied. Treat every entry as a working note.

## Layout

- `INDEX.md` — shared signal board. Append-only. Cross-domain traces:
  blockers, questions, handoffs, decisions needed, invariant risk,
  notable findings.
- `domains/<domain>.md` — one append-only log per domain. Local traces:
  what a domain worker or read-only evidence producer did, touched,
  verified, and left open. Read-only reviewers/routers do not write these
  files directly; the parent/orchestrator records their returned evidence
  with source-role attribution.

Domains (one file per coordination domain, created on first write):
`transport-safety.md`, `market-data.md`, `strategy.md`, `risk.md`,
`accounting-ledger.md`, `runtime-execution.md`, `research-integrity.md`,
`openrouter-agents.md`, `governance-approvals.md`, `security.md`,
`architecture.md`, `phase-integration.md`.

## Rules

1. **Append-only.** Never edit or delete a prior entry. If a prior entry
   was wrong, append a correction entry that references it by date and
   title — the history of being wrong is itself signal.
2. **Read before you write.** Before starting a task, read (a) the most
   recent entries in your own domain log, (b) any unresolved `INDEX.md`
   entries tagged for your domain, and (c) the domain logs of any
   upstream domain you consume per
   `.codex/policies/architecture/dependency-boundaries.md`.
3. **Write after you finish, unless the active role is read-only.** A
   write-capable domain worker appends one entry to its domain log for every
   task with observable effect. A read-only reviewer/router/verifier returns
   evidence to the parent/orchestrator instead; the parent records that
   evidence through `memory-domain-sync` and attributes the source role.
   Planning-only or read-only investigation still gets an entry when it
   produced a conclusion another agent should see, but read-only roles never
   widen their authority merely to record it.
4. **Escalate cross-domain effects to `INDEX.md`.** If your change
   affects another domain's assumptions, creates a blocker, raises a
   question only a human or another specialist can resolve, or exposes
   invariant risk, append a tagged entry to `INDEX.md` in addition to
   your domain log.
5. **Evidence, not narrative.** Record the command you ran and its
   result, not a summary of your intentions. "Ran `uv run pytest -q
   tests/risk` — 4 passed" beats "risk logic looks solid."
6. **No secrets, no raw exchange payloads, no credential material.**
   Memory files are plain repository text; treat them exactly like log
   output under `.codex/policies/credential-privacy.md`.
7. **Never silently resolve an `INDEX.md` entry.** Append a follow-up
   entry that references the original and states the resolution or
   remaining gap. Do not delete stale entries — mark them.

## Entry format

Use this shape in both `INDEX.md` and domain logs:

```markdown
## <ISO date> — <domain> — <short title>
Task: <what was asked>
Touched: <files changed, or "none — read-only">
Verified: <exact commands run + results, or "none — planning only">
Status: <done | blocked | needs-human-approval | handoff | refused-scope>
Notes: <what the next reader needs to know>
```

`INDEX.md` entries additionally carry one tag in the title, immediately
after the domain:

- `[BLOCKER]` — cannot proceed without something from another domain or a
  human.
- `[QUESTION]` — needs an answer before work continues.
- `[HANDOFF]` — work product is ready for a specific downstream domain.
- `[DECISION-NEEDED]` — crosses a human-approval gate in
  `.codex/policies/governance-and-approvals.md`.
- `[INVARIANT-RISK]` — a safety invariant from `AGENTS.md` may be at
  risk; state which one.
- `[FINDING]` — an adversarial or architecture finding another domain
  should account for.

Example:

```markdown
## 2026-07-20 — risk — [HANDOFF] limit-check interface ready for strategy
Task: define RiskDecision shape consumed by strategies per
  schemas/risk-limits.schema.json
Touched: none — planning only, Phase 1 has no implementation yet
Verified: none — planning only
Status: handoff
Notes: strategy-engineer should not assume synchronous latency budget
  until Phase 3; do not implement either side before Phase 1 exit.
```
