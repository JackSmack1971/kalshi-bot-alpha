# Test Phase Contract

## Objective

Turn the approved implementation into release-readiness evidence before launch
or deployment authorization proceeds.

## Inputs

- approved MVP PRD
- implementation record
- user flows
- constraints

## Outputs

- test plan
- functional-test report
- UAT report
- defect-resolution log
- performance report
- security report
- test record

## States and Legal Transitions

- Enter from `test` after build evidence is ready.
- Advance node-by-node through nodes 24 to 28.
- Exit to `launch` only when release-readiness evidence exists and blockers are explicit.
- Return `blocked` or `recoverable` instead of advancing when test evidence is incomplete or interrupted.

## Input Contract

- approved implementation evidence and user-flow expectations are authoritative markdown inputs under `artifacts/`
- residual risks stay visible across the phase and cannot be silently cleared
- release recommendation must be returned explicitly rather than inferred

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist test artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- approved build, define, and UX artifacts under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- test artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- test handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough release-readiness evidence for launch planning without hiding quality gaps

## Gate

The phase passes only when:

- functional coverage exists for the MVP slice
- UAT and usability findings are explicit
- unresolved defects do not invalidate release claims
- performance and security blockers are visible
- the test record can support a bounded release recommendation

## Rework

- revisit implementation when unresolved defects block task success
- revisit flows when UAT exposes critical usability failures
- stop before launch when release evidence is incomplete

## Failure Criteria

- block when unresolved defects, performance gaps, security gaps, or missing release evidence prevent bounded launch planning
- mark the active node `recoverable` when interruption leaves partial test outputs or dirty workflow files behind

## Budgets

- one authoritative writer at a time per owned output
- allow bounded parallelism for performance and security only after core test evidence exists
- stop before launch when the release recommendation is blocked

## Resume and Rollback

- resume from the persisted eligible test node instead of restarting the phase
- rollback by superseding or reclassifying stale test artifacts rather than deleting history

## Observability

- record test gate results and decision records
- persist delegated handoffs and changed authoritative artifact paths
- surface test blockers, required approvals, and active risks in the returned status

## Human Approval Points

- no standalone human approval boundary inside this phase; launch authorization happens later once test evidence is complete

## Ownership

- QA owns nodes 24, 25, 28, and the performance evidence
- UX researcher owns node 26
- integration engineer owns node 27
- security engineer owns security validation at node 28
