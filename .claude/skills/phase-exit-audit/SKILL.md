---
name: phase-exit-audit
description: Use to check whether the currently active phase in docs/IMPLEMENTATION_STATUS.md actually satisfies its own deliverables and exit criteria, with objective evidence, before anyone claims the phase is complete. Trigger on requests like "is phase N done", "can we close out this phase", "check exit criteria", "is this ready for phase review", or before a phase transition is recorded. Reports readiness only; never edits docs/IMPLEMENTATION_STATUS.md and never records a phase transition, since that is a human-reviewed action. NOT for auditing cross-cutting safety invariants on a diff (use audit-safety-invariants) and NOT for evolving a frozen schema contract (use propose-contract-change).
---

# Phase exit audit

1. Read `docs/IMPLEMENTATION_STATUS.md`; identify the active phase, its deliverables table, and its exit-criteria table exactly as written. Note the current phase-ledger status and any listed known gaps or deferred work.
2. For each deliverable, locate its named artifact(s) and inspect them directly — open the doc section, open the schema file, run the referenced test or script. Do not infer satisfaction from a file's mere existence, a filename match, or a stub/placeholder body.
3. For each exit criterion, require objective, reviewable evidence: a test that actually runs and passes, a schema that actually validates a representative sample payload, a doc section that actually contains the described content (not a heading placeholder). Explicitly reject a stub, TODO, mock-only path, skipped test, or bare interface declaration as satisfying a criterion.
4. Classify every deliverable and every exit criterion using exactly this vocabulary, taken from CLAUDE.md's completion bar: `implemented`, `tested`, `mocked`, `simulated`, `partially implemented`, `unverified`, or `deferred`. Use the most accurate single term; if more than one applies, state the combination (e.g. "implemented, unverified" for code that exists but was not exercised by a passing test in this audit).
5. Explicitly check for and reject any claim of phase completion that rests on later-phase work being partially or fully done instead of the active phase's own criteria. Opportunistic later-phase progress does not advance the active phase's exit criteria.
6. Cross-check the "Known gaps and deferred work" section and the phase ledger against what was actually found; note any discrepancy (e.g. a gap listed as deferred that is in fact now satisfied, or a deliverable claimed "Delivered" that this audit could not verify).
7. Produce the report below.

Do not edit `docs/IMPLEMENTATION_STATUS.md` or any other project documentation. Do not mark, update, or imply a change to the phase ledger. Do not assert, imply, or record that human review or approval has occurred — recording a phase transition is a human action this skill cannot perform and must not simulate. Do not run destructive or mutating commands; this is a read-and-verify procedure only.

Final phase exit audit report:

```text
Phase exit audit — Phase <N> (<phase name>)

Deliverables
| Deliverable | Artifact(s) | Evidence | Status |
| --- | --- | --- | --- |
| <from docs/IMPLEMENTATION_STATUS.md> | <artifact path(s)> | <what was inspected/run and the result> | implemented / tested / mocked / simulated / partially implemented / unverified / deferred |

Exit criteria
| Exit criterion | Evidence | Status |
| --- | --- | --- |
| <from docs/IMPLEMENTATION_STATUS.md> | <what was inspected/run and the result> | implemented / tested / mocked / simulated / partially implemented / unverified / deferred |

Later-phase leakage check
- Any later-phase work found substituting for an active-phase criterion: yes/no; detail if yes.

Known-gaps cross-check
- Discrepancies between this audit and the "Known gaps and deferred work" section or phase ledger, if any.

Overall readiness
- Ready for human review | Not ready — blocking gaps listed above.
- This report does not change docs/IMPLEMENTATION_STATUS.md. Recording a phase transition requires a human to review this evidence and update the phase ledger themselves.
```
