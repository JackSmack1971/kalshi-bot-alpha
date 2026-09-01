# Repository improvement plans

These plans were produced by the repository-improvement audit at commit
`5ac063051a066163c6a3bc0def998d861b3a319f`.

| Plan | Finding | Scope |
| --- | --- | --- |
| [001](001-ci-enforcement.md) | TEST-001 | Add required, credential-free CI checks. |
| [002](002-status-docs.md) | DOC-001 | Reconcile phase and architecture authority documents. |
| [003](003-runtime-entrypoint.md) | ARCH-001 | Resolve the duplicate Phase 1/current runtime boundary. |

Ordering is intentional: establish merge-time verification first, then repair
the written authority model, then make the runtime ownership decision.

These are planning artifacts only. No implementation, remote setting change,
commit, push, or merge was performed by this audit.
