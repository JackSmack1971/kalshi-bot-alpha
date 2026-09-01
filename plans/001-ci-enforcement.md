# Plan 001: Add required repository checks to CI

> Follow this plan in order. Run every verification gate. Touch only in-scope files. Stop on any listed STOP condition instead of broadening scope.

## Status

- **Finding ID**: TEST-001
- **Type**: corrective
- **Priority**: P1
- **Leverage**: 50.0
- **Effort**: S
- **Implementation risk**: LOW
- **Depends on**: none
- **Planned at**: 5ac063051a066163c6a3bc0def998d861b3a319f
- **State**: TODO

## Outcome

Every relevant PR and `main` push runs credential-free tests, static analysis, and the demo-only safety scanner with stable job names that can be required by branch protection.

## Evidence and current behavior

- `.github/workflows/codeql.yml:1-51` — the only workflow runs CodeQL; it does not run project checks.
- `.github/CONTRIBUTING.md:10-18` — requires pytest, Ruff, mypy, `verify_demo_only.py`, and `git diff --check`.
- `pyproject.toml:38-49` — native test, lint, and strict type-check configuration exists.
- `scripts/verify_demo_only.py:32-44` — fail-closed endpoint scanner scope.

## Assumptions

- [ASSUMPTION] Use Python 3.12 and the existing `uv.lock` contract.
- [ASSUMPTION] Keep CodeQL as a separate security-analysis job.
- [ASSUMPTION] CI receives no Kalshi or OpenRouter credentials.

## Scope

**In scope**
- `.github/workflows/` (one workflow file, create or update)
- Workflow validation and required-check configuration path.

**Out of scope**
- Application code, tests, dependency declarations, and lockfiles.
- Credentialed/live acceptance tests.
- Remote branch-protection changes unless separately authorized.

## Implementation constraints

- Use least-privilege permissions and pinned third-party action references.
- Run the exact contributor commands without service credentials.
- Do not narrow scanner coverage or upload sensitive artifacts.
- Do not add dependencies or a second toolchain convention.

## Steps

### Step 1: Confirm the locked runner setup

Inspect Python/uv and lockfile conventions and choose stable job names.

**Verify**: `rg -n "requires-python|uv.lock|uv run" pyproject.toml uv.lock .github .github/CONTRIBUTING.md`
**Expected**: Python 3.12, the existing lockfile, and documented commands are the setup contract.

### Step 2: Add the credential-free verification workflow

Add one PR and `main`-push job running pytest, Ruff, mypy, the demo-only scanner, and `git diff --check`; keep CodeQL separate.

**Verify**: `Get-Content .github/workflows/ci.yml`
**Expected**: all five commands are visible, failures fail the job, permissions are minimal, and actions are pinned.

### Step 3: Validate locally and review the workflow diff

Run all repository-native checks and inspect the diff. Configure required checks only through the approved governance path.

**Verify**: `uv run pytest -q; uv run ruff check .; uv run mypy .; uv run python scripts/verify_demo_only.py; git diff --check`
**Expected**: every command exits 0 and only the workflow path changes.

## Test plan

- Run the five documented commands from the repository root.
- Validate workflow YAML with an available parser or GitHub workflow validation.
- Observe one successful PR run and one controlled failing-check exercise; remove any exercise before merge.
- Confirm no CI step reads credentials or invokes live/demo acceptance.

## Verification matrix

| Gate | Command | Expected | Required |
|---|---|---|---|
| Full tests | `uv run pytest -q` | all pass | yes |
| Lint | `uv run ruff check .` | exit 0 | yes |
| Typecheck | `uv run mypy .` | exit 0 | yes |
| Demo safety | `uv run python scripts/verify_demo_only.py` | policy passes | yes |
| Diff hygiene | `git diff --check` | clean | yes |
| Scope | `git diff --name-only` | workflow only | yes |

## Rollback or containment

Revert the workflow commit and restore any separately changed required-check setting through the same governance path. Do not disable checks ad hoc.

## Done criteria

- [ ] The workflow runs on every relevant PR and `main` push.
- [ ] All five documented commands execute without credentials.
- [ ] The stable job is required by branch protection if approved.
- [ ] A reviewer confirms no scanner scope was narrowed.

## STOP conditions

- The locked runner setup requires credentials or mutable dependency resolution.
- A verification command needs live/demo credentials or fails twice after one bounded correction.
- The workflow needs an out-of-scope dependency, source path, or remote change without authorization.
- Action pinning, permissions, or secret isolation cannot be verified.

## Review focus

Trigger coverage, action pinning, secret isolation, scanner coverage, stable required-check naming, and failure propagation.

## Deferred work

Release automation, coverage thresholds, and credentialed acceptance testing remain deferred.
