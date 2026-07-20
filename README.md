# Claude Code Control Plane

This repository is a bounded, evidence-gated control plane for Claude Code configuration
artifacts, plus an idea-to-MVP operating system built on top of it: executable workflows,
a specialist subagent roster, and lifecycle skills that carry a product idea from discovery
through MVP release and post-launch learning.

## Included

### Control-plane governance (bootstrap)

- Authoring specialists (`skills-specialist`, `rules-specialist`, `workflow-specialist`)
  plus one independent read-only verifier
- Control-plane ownership manifest (`.claude/control-plane/manifest.yaml`)
- JSON Schemas for change plans, candidate packages, verification results, run events,
  and workflow/artifact state
- Routing, skill, rule, and workflow evaluation fixtures under `.claude/control-plane/evals/`
- Cross-platform Python validation, inventory, candidate-emission, and historical-replay
  scripts under `.claude/control-plane/scripts/`
- Append-only run-ledger layout with deterministic replay evidence
- Recursive self-improvement workflow trigger (`UserPromptSubmit` hook)
- Bootstrap and operating documentation
- Minimal `AGENTS.md` integration

### Idea-to-MVP operating system

- Executable workflow phases (`discover`, `define`, `design`, `build`, `test`, `launch`,
  `feedback`) under `.claude/workflows/`, each with a paired `.md` contract and `.js` runner
- A specialist subagent roster covering product, UX/UI, architecture, backend/frontend/
  integration engineering, QA, security, data analysis, DevOps, technical review, and
  workflow-state management (`.claude/agents/`)
- Lifecycle skills covering every phase artifact — discovery, scope/requirements,
  architecture, implementation, testing, release, and the post-launch feedback loop
  (`.claude/skills/`)
- Persisted workflow state, artifact manifest, decision records, risk register, and
  interruption/recovery tracking under `.claude/control-plane/state/idea-to-mvp/`
- `PreToolUse`/`PostToolUse`/`Stop` hooks that guard tool use and validate state against
  the idea-to-MVP contract (`.claude/hooks/`)

### Tooling

- A portable, cross-repo PowerShell status line with theme/density options and a mock
  test harness (`.claude/statusline-command.ps1`, `.claude/statusline.json`,
  `.claude/statusline-tests.ps1`)

## Safety model

The scaffold assumes:

1. One primary writer per transaction.
2. An explicit write set before mutation.
3. Deterministic validation before semantic review.
4. Independent verification after authoring.
5. Rollback on failed verification.
6. No same-run self-authorization.
7. No application-source ownership by control-plane agents.

This is a self-proposing control plane, not a self-authorizing one.

## Installation

Copy the contents of this scaffold into the repository root.

Expected paths:

```text
AGENTS.md
.claude/
  AGENTS.md
  agents/
  control-plane/
  rules/
  skills/
  workflows/
  hooks/
```

Review `.claude/control-plane/manifest.yaml` before enabling any write workflow. Tailor allowed and forbidden roots to the repository.

## Requirements

The validation scripts use Python 3.10+.

Required package:

```bash
python -m pip install pyyaml
```

Recommended package for full schema meta-validation:

```bash
python -m pip install jsonschema
```

Without `PyYAML`, `validate.py` cannot parse the manifest or eval fixtures and fails closed.
Without `jsonschema`, validation still runs but skips JSON Schema meta-validation and emits a warning.

The `UserPromptSubmit` self-improvement hook in `.claude/settings.json` is configured in exec form (`command` plus `args`) so project roots with spaces remain portable across Windows and POSIX shells.

## First commands

```bash
python .claude/control-plane/scripts/inventory.py
python .claude/control-plane/scripts/validate.py
python .claude/control-plane/scripts/estimate_context.py
```

`inventory.py` rewrites `.claude/control-plane/inventory.json` using repo-relative
paths and canonical text hashing so a clean Windows or Unix checkout produces the
same inventory for the same tracked content.

`validate.py` fails closed on stale `PACKAGE_MANIFEST.json` entries or a stale
committed inventory snapshot.

The scaffold also ships an active `UserPromptSubmit` hook in `.claude/settings.json`
that runs `.claude/control-plane/scripts/self_improvement_evidence.py --hook`
and injects latest-run or first-run evidence when a prompt matches the
self-improvement workflow trigger terms.

`estimate_context.py` is read-only by default and prints the full JSON report to stdout. To persist a generated report, pass `--output .claude/control-plane/context-estimate.json`; that file is ignored by git and excluded from managed inventory baselines.

Then run the three analysis-only bootstrap prompts in:

```text
.claude/control-plane/BOOTSTRAP.md
```

## Transaction lifecycle

```text
RECEIVED
  -> CLASSIFIED
  -> BASELINED
  -> PLANNED
  -> PLAN_VALIDATED
  -> APPLYING
  -> VERIFYING
  -> COMMITTED

Any mutable state
  -> FAILED
  -> ROLLED_BACK

Any nonterminal state
  -> CANCELLED
```

Each transaction should create:

```text
.claude/control-plane/runs/<run-id>/
  request.json
  baseline.json
  plan.json
  events.jsonl
  proposed.patch
  verification.json
  result.json
```

The `runs/` directory is gitignored by default. Preserve it elsewhere when audit retention is required.

## Idea-to-MVP workflow

Invoke `/idea-to-mvp` to start or resume the operating system described in
`.claude/workflows/idea-to-mvp.md`. It runs in one of five modes (`guided`,
`phase-autonomous`, `guardrailed-autonomous`, `audit`, `re-entry`) across seven phases
(`discover`, `define`, `design`, `build`, `test`, `launch`, `feedback`), stopping at
explicit human-approval gates for product direction, MVP scope, and release readiness.
Persisted state, artifact manifest, decision records, and the risk register live under
`.claude/control-plane/state/idea-to-mvp/`; see the `README.md` there for the layout.

## Status line

The Claude Code status line is wired to `.claude/statusline-command.ps1` via
`.claude/settings.json`. Configure it with `.claude/statusline.json` or the
`STATUSLINE_*` environment variables documented at the top of the script. Run
`.claude/statusline-tests.ps1` to exercise the mock test harness after changes.

## Recommended next step

Run the read-only inventory phase before permitting any specialist to edit the existing control plane.

See [CHANGELOG.md](CHANGELOG.md) for release history.
