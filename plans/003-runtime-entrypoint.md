# Plan 003: Resolve the duplicate runtime entrypoint boundary

> Follow this plan in order. Run every verification gate. Touch only in-scope files. Stop on any listed STOP condition instead of broadening scope.

## Status

- **Finding ID**: ARCH-001
- **Type**: corrective
- **Priority**: P2
- **Leverage**: 10.0
- **Effort**: M
- **Implementation risk**: MED
- **Depends on**: plans/002-status-docs.md
- **Planned at**: 5ac063051a066163c6a3bc0def998d861b3a319f
- **State**: DONE

## Outcome

The repository has one explicitly supported runtime composition boundary, with no split ownership of startup, credential, lifecycle, or fail-closed behavior.

## Evidence and current behavior

- `src/kalshi_bot/application.py:1-7` — describes a Phase 1 root lacking capabilities now present in the active tree.
- `src/kalshi_bot/application.py:21-43` — publicly exports `run_phase1_supervisor`.
- `src/kalshi_bot/cli.py:41-218` — installed CLI does not call it.
- `tests/unit/test_application_wiring.py:1-20` — supervisor is maintained by tests; search finds no production caller outside its definition.

## Assumptions

- [ASSUMPTION] The current CLI/Phase 3 composition is the default operator path.
- [ASSUMPTION] `scripts/soak_phase1.py` may still be supported; confirm before removal.
- [ASSUMPTION] Deleting a public function is unsafe without an owner decision.

## Scope

**In scope**
- `src/kalshi_bot/application.py`
- `src/kalshi_bot/cli.py`
- `scripts/soak_phase1.py`
- `tests/unit/test_application_wiring.py`
- Documentation references identified by the entrypoint trace.

**Out of scope**
- Runtime rewrite, new transport, live endpoint, production switch, or AI work.
- Frozen schemas and unrelated lifecycle behavior.

## Implementation constraints

- Retain credential/process isolation and fail-closed startup behavior.
- Preserve a supported soak workflow if the owner confirms it is required.
- Add no new dependency or alternate composition framework.
- Do not remove a public interface without documenting compatibility impact.

## Steps

### Step 1: Trace supported and test-only callers

Inspect CLI, soak script, package exports, operator docs, and tests to classify every caller.

**Verify**: `rg -n "run_phase1_supervisor|soak_phase1|kalshi-bot|__main__|main\(" src scripts tests docs README.md`
**Expected**: every supported, operator, and test-only caller is classified.

### Step 2: Decide ownership before changing code

Confirm whether Phase 1 streaming remains a supported library/soak interface; choose integrate versus deprecate/retire.

**Verify**: `rg -n "Phase 1|Phase 3|soak" docs README.md scripts/soak_phase1.py`
**Expected**: the owner decision and compatibility requirement are explicit.

### Step 3: Apply the smallest boundary change and test it

Integrate or deprecate the orphaned path, update focused tests and docs, and preserve startup cleanup and credential boundaries.

**Verify**: `uv run pytest tests/unit/test_application_wiring.py tests/unit/test_acceptance.py -q`
**Expected**: focused lifecycle and acceptance tests pass with one supported ownership path.

## Test plan

- Add or update tests for startup, cleanup, and fail-closed behavior.
- Test compatibility or explicit deprecation for any removed public interface.
- Run the full suite, static checks, and demo-only scanner.

## Verification matrix

| Gate | Command | Expected | Required |
|---|---|---|---|
| Entrypoint trace | `rg -n "run_phase1_supervisor|soak_phase1|kalshi-bot" src scripts tests docs README.md` | ownership explicit | yes |
| Focused tests | `uv run pytest tests/unit/test_application_wiring.py tests/unit/test_acceptance.py -q` | all pass | yes |
| Full tests | `uv run pytest -q` | all pass | yes |
| Static checks | `uv run ruff check .; uv run mypy .` | exit 0 | yes |
| Demo safety | `uv run python scripts/verify_demo_only.py` | policy passes | yes |
| Scope | `git diff --name-only` | only approved paths | yes |

## Rollback or containment

Revert the boundary change and tests together. If deprecation was published, restore the documented supported path before reverting callers.

## Done criteria

- [x] A maintainer can identify the one supported runtime composition immediately.
- [x] The retained CLI and soak paths retain their existing lifecycle coverage.
- [x] The retired API has an explicit compatibility record in `docs/PHASE1_PLAN.md`.
- [x] No live endpoint or production-capable switch is introduced.

## STOP conditions

- External callers or the supported soak workflow cannot be identified.
- Integration requires a frozen-contract change or second runtime framework.
- Credential isolation or fail-closed cleanup cannot be preserved.
- A verification command fails twice after one bounded correction.

## Review focus

Public API compatibility, lifecycle ownership, credential/process isolation, fail-closed behavior, and active-phase scope.

## Deferred work

Phase 3/4 runtime redesign and AI control-plane work remain deferred because this plan resolves ownership rather than adding behavior.
