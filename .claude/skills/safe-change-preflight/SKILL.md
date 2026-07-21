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
10. Produce the report below.

If authoritative sources conflict, preserve the safer current behavior and surface the conflict rather than silently resolving it.

Final preflight plan:

```text
Preflight — <task>

Current state
- Active phase, relevant exit criteria, deferred work, known gaps.
- Owning module(s), existing conventions/types reused instead of duplicated.

Implementation boundary
- What is in scope; what later-phase behavior stays unimplemented.

Affected invariants
- Safety, authority-boundary, persistence, schema, and interface contracts touched.

Verification strategy
- Checks this change will require (tests, lint, static analysis, migrations).

Conflicts
- Any authoritative-source conflict found and the safer behavior preserved, or "none found."
```
