---
name: implement-safe-change
description: Use to execute a bounded code change after preflight while preserving demo-only, deterministic authority, accounting, privacy, and phase constraints. Trigger on implementation, bug fix, refactor, integration, or migration tasks. NOT for planning-only work; run safe-change-preflight first.
---

# Implement a safe change

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

Do not refactor unrelated code, rename broad APIs, reformat unrelated files, weaken safety tests, implement later phases opportunistically, or use stubs/mocks/skips as completion evidence.

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

Distinguish implemented, tested, mocked, simulated, partial, unverified, and deferred behavior.
