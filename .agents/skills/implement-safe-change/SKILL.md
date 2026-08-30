---
name: implement-safe-change
description: Use to execute a bounded code change after preflight while preserving demo-only, deterministic authority, accounting, privacy, and phase constraints. Trigger on implementation, bug fix, refactor, integration, or migration tasks. NOT for planning-only work; run safe-change-preflight first.
---

# Implement a safe change

## Repository-specific decision boundary

This skill owns the mutation loop after preflight: failure-mode tests, the
smallest implementation inside the resolved write set, immediate targeted
checks, and final scope/invariant review. It does not rediscover phase or
policy scope, choose domain ownership, or replace independent verification;
those remain preflight and verify-change responsibilities. If preflight did
not produce a resolved write set, stop with `blocked`.

1. Establish current behavior from code and tests.
2. Reconfirm the narrow implementation boundary and affected invariants.
3. Add or update failure-mode tests before or with implementation.
4. Make the smallest coherent change that fully satisfies the requirement.
5. Preserve established public interfaces unless a reviewed contract change requires updates to all callers, schemas, tests, and documentation.
6. Run targeted tests immediately after the relevant change.
7. Run directly affected safety, authority-boundary, contract, migration, and integration suites.
8. Inspect the final diff for scope drift, accidental authority expansion, production reachability, secret leakage, weakened failure behavior, unrelated formatting, and speculative abstraction.
9. Update schemas, migrations, documentation, and implementation status only when required and authorized.
10. Never describe the work as complete until verification evidence supports it.

Keep the diff to the narrow boundary from step 2: touch only the files a reviewed acceptance criterion or invariant requires, in their existing style. Stubs, mocks, and skips are never completion evidence — only a passing run is.

Final implementation report:

```text
Summary
- What changed and why.

Safety and architecture
- Invariants preserved.
- Authority boundaries affected.
- Approved contract changes, if any.

Files changed
- Exact paths and purpose.

Verification
- Commands run and pass/fail results.
- Tests not run and why.

Remaining risks
- Limitations, unresolved evidence, or deferred work.

Phase status
- Exit criteria advanced, satisfied, or still incomplete.
```

Distinguish implemented, tested, mocked, simulated, partially implemented, unverified, and deferred behavior — AGENTS.md's completion-bar vocabulary.


## Observable workflow and telemetry

Emit one started record and one terminal record with `.codex/scripts/skill_telemetry.py` for each invocation. Emit the consequential events below when that decision occurs; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `implementation_boundary`, `failure_test_coverage`, `targeted_verification`, `scope_drift`, `workflow_result`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
