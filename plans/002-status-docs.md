# Plan 002: Reconcile phase and architecture authority documents

> Follow this plan in order. Run every verification gate. Touch only in-scope files. Stop on any listed STOP condition instead of broadening scope.

## Status

- **Finding ID**: DOC-001
- **Type**: corrective
- **Priority**: P1
- **Leverage**: 20.0
- **Effort**: M
- **Implementation risk**: MED
- **Depends on**: plans/001-ci-enforcement.md
- **Planned at**: 5ac063051a066163c6a3bc0def998d861b3a319f
- **State**: DONE

## Outcome

The phase ledger and architecture map accurately describe the merged tree, current verification evidence, active/deferred scope, and human-approval gates.

## Evidence and current behavior

- `docs/IMPLEMENTATION_STATUS.md:36-39` — says runtime capabilities present in `src/` are not authorized.
- `docs/IMPLEMENTATION_STATUS.md:110-135` — reports empty tests, no runtime dependencies, and no Alembic persistence despite current files.
- `docs/IMPLEMENTATION_STATUS.md:168-219` — records old commit/scanner evidence and says CI/Alembic are absent.
- `docs/ARCHITECTURE.md:23-41` — says the pipeline is not implemented and no components exist, contradicting its Phase 3 section and source tree.

## Assumptions

- [ASSUMPTION] The merged Phase 3 implementation is the baseline.
- [ASSUMPTION] A human owner decides whether Phase 4 is active or delivered ahead of the ledger.
- [ASSUMPTION] `AGENTS.md` is the intended control-plane reference because `CLAUDE.md` is absent.

## Scope

**In scope**
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/ARCHITECTURE.md`

**Out of scope**
- Source, tests, schemas, migrations, configuration, and blueprint redesign.
- Implementing any deferred phase or changing runtime authority.

## Implementation constraints

- Preserve demo-only, deterministic-authority, credential-isolation, and AI-gating statements.
- Every current-state claim must have path, symbol, or command evidence.
- Do not present prose reconciliation as human approval or implementation.

## Steps

### Step 1: Build the current evidence inventory

Inventory packages, tests, migrations, CLI entrypoints, and verification commands at the planned SHA.

**Verify**: `git ls-tree -r --name-only HEAD src tests alembic .github; git rev-parse HEAD`
**Expected**: all present runtime and verification artifacts are identified.

### Step 2: Resolve phase and reference decisions

Obtain the owner decision on active phase, Phase 4 status, and the `CLAUDE.md`/`AGENTS.md` reference before editing prose.

**Verify**: `rg -n "Active phase|Phase 4|CLAUDE.md|AGENTS.md" docs README.md AGENTS.md`
**Expected**: one unambiguous decision is recorded for each open question.

### Step 3: Rewrite only stale authority claims

Update inventory, ledger, verification table, known gaps, and pipeline labels while retaining deferred boundaries.

**Verify**: `rg -n "None of these components|dependencies = \[\]|placeholder|CI workflow wiring|CLAUDE.md" docs/IMPLEMENTATION_STATUS.md docs/ARCHITECTURE.md`
**Expected**: no present capability is described as absent, and intentional deferrals remain explicit.

## Test plan

- Review changed links and evidence paths.
- Run pytest and the demo-only scanner.
- Run `git diff --check` and inspect the diff for authority overreach.

## Verification matrix

| Gate | Command | Expected | Required |
|---|---|---|---|
| Stale-claim scan | `rg -n "None of these components|dependencies = \[\]|placeholder|CI workflow wiring|CLAUDE.md" docs/IMPLEMENTATION_STATUS.md docs/ARCHITECTURE.md` | no obsolete claims | yes |
| Full tests | `uv run pytest -q` | all pass | yes |
| Demo safety | `uv run python scripts/verify_demo_only.py` | policy passes | yes |
| Links/evidence | manual path review | all references resolve | yes |
| Scope | `git diff --name-only` | two docs only | yes |

## Rollback or containment

Revert the documentation commit only; preserve independent code, CI, or governance changes.

## Done criteria

- [x] Status and architecture agree with the merged tree.
- [x] Current evidence names the current tree, verification commands, and remediation commit `94e51a9`.
- [x] Active/deferred boundaries and approval gates are explicit.
- [x] No prose update grants runtime authority.

## STOP conditions

- The owner has not decided the active phase or Phase 4 status.
- An evidence anchor no longer matches or an in-scope document has unrelated changes.
- Reconciliation requires a frozen-contract or source change.
- A verification command fails twice after one bounded correction.

## Review focus

Authority wording, phase gating, evidence freshness, links, and preservation of demo-only and human-approval invariants.

## Deferred work

Blueprint redesign, runtime changes, and deferred-phase implementation are excluded because this plan corrects documentation only.
