# Workflows Directory

Each file is a self-contained Workflow-tool script (plain JavaScript,
`export const meta = {...}` header) that deterministically orchestrates the
domain-engineering subagents in `.claude/agents/`, the procedures in
`.claude/skills/`, and the stigmergic substrate in `.claude/memory/`. These
are opt-in: invoke with the `Workflow` tool (`name: "<workflow-name>"`) only
when the user has explicitly asked for multi-agent orchestration, per that
tool's own gating rules. `.claude/**` is unreviewed process tooling per
`docs/IMPLEMENTATION_STATUS.md`, not a Phase 0+ product artifact — these
workflows never edit `docs/IMPLEMENTATION_STATUS.md`, never fabricate human
approval, and never let AI output become authoritative.

| Workflow | Purpose | Args |
| --- | --- | --- |
| `implement-feature` | Route a change request to the owning domain engineer(s) in dependency order, implement, then independently verify architecture boundaries, safety invariants, and tests. | `{ request: string }` |
| `phase-readiness-gate` | Four independent auditors (phase-exit, safety-invariants, architecture-boundaries, swarm-status) run in parallel and get synthesized into one evidence-backed readiness report. Never marks a phase complete. | none |
| `swarm-standup` | Read-only: swarm-status-briefing plus a memory-sync drift check (uncommitted diff paths vs. domain-log coverage). | none |
| `control-plane-change` | Route a `.claude/**` change to rules-specialist / skills-specialist / workflow-specialist, author it, then independently verify with control-plane-verifier. | `{ request: string }` |
| `contract-evolution` | Draft a `schemas/` contract change, then independently check breaking-change versioning, downstream architecture impact, and authority-sensitive fields. | `{ request: string }` |
| `security-sweep` | Multi-lens adversarial sweep (injection, credential leakage, capability escalation, replay/idempotency, prompt injection) across sensitive surfaces; adversarially refutes each raw finding before treating it as confirmed; fixes are opt-in. | `{ autoFix?: boolean }` |

## Design choices worth knowing

- **Routing never dispatches from inside itself.** `implement-feature` and
  `control-plane-change` call `phase-integrator` / the target specialist only
  to *classify and plan*, never to further fan out via their own `Agent`
  tool — the workflow script stays the single source of orchestration
  control and progress visibility.
- **Verification is always a separate identity from authorship.**
  `architecture-boundary-verifier`, `control-plane-verifier`, and
  `security-adversarial-reviewer` never author or repair the change they are
  reviewing — a finding routes back to the owning domain agent, matching
  each agent's own system-prompt constraint.
- **`security-sweep` is adversarial by construction**: every raw finding
  must survive an independent refutation pass (default `refuted=true` on
  uncertainty) before it counts as confirmed, and confirmed findings are
  only auto-fixed when the caller explicitly opts in with `autoFix: true`.
- **Nothing here grants or infers human approval.** `phase-readiness-gate`
  and `contract-evolution` explicitly report `needs-human-approval` rather
  than a pass/fail binary when a decision in
  `.claude/rules/governance-and-approvals.md` is at stake.
