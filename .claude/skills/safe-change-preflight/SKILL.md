---
name: safe-change-preflight
description: Use before any nontrivial repository modification to inspect current state, identify owning modules and invariants, protect unrelated work, and produce a bounded implementation plan. Trigger on requests to implement, fix, refactor, migrate, integrate, or change code. NOT for read-only explanation or simple text edits.
---

# Safe change preflight

Perform this workflow before editing:

1. Inspect `git status`, branch/worktree state, and the relevant repository tree.
2. Read `docs/IMPLEMENTATION_STATUS.md`; identify the active phase, completed/incomplete exit criteria, deferred work, and known gaps.
3. Read the relevant blueprint sections, accepted architecture decisions, frozen schemas, and contracts.
4. Read `pyproject.toml`, applicable configuration, migrations, tests, and recent related implementation.
5. Search for existing domain types, services, invariants, safety checks, and conventions before creating new ones.
6. Identify the owning module and test locations.
7. Enumerate affected safety invariants, authority boundaries, persistence contracts, schemas, migrations, public interfaces, observability, failure modes, and tests.
8. Confirm unrelated worktree changes will not be overwritten.
9. Define the narrowest coherent implementation boundary and later-phase behavior that must remain unimplemented.
10. State a bounded plan naming affected invariants and the verification strategy.

If authoritative sources conflict, preserve the safer current behavior and surface the conflict rather than silently resolving it.
