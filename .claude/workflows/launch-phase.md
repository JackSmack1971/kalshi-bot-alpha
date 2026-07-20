# Launch Phase Contract

## Objective

Separate deployment, analytics readiness, and product release authorization for
the idea-to-MVP workflow.

## Inputs

- release evidence
- test evidence
- residual risks
- KPI and event requirements
- current constraints

## Outputs

- deployment record
- rollback evidence
- analytics plan
- event validation report
- release record and release notes

## States and Legal Transitions

- Enter from `launch` after test evidence is ready.
- Advance node-by-node through nodes 29 to 31.
- Exit to `feedback` only after release authorization is recorded.
- Return `blocked` or `recoverable` instead of advancing when launch evidence is incomplete or interrupted.

## Input Contract

- test evidence, residual risks, and analytics requirements are authoritative inputs
- deployment readiness and release authorization are separate values and must not be merged
- release approval must come from persisted workflow state rather than inference

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist launch artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- approved test and product artifacts under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- launch artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- launch handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough release evidence for feedback work to begin without inventing authorization

## Gate

The phase passes only when:

- deployment evidence is explicit
- rollback readiness is stated
- critical analytics events are validated or flagged
- release authorization is requested explicitly instead of invented

## Rework

- block when deployment evidence is incomplete
- block when critical analytics readiness is missing
- stop before user exposure when release authorization is missing

## Failure Criteria

- block when deployment, analytics, or release evidence is incomplete
- mark the active node `recoverable` when interruption leaves partial launch outputs or dirty workflow files behind

## Budgets

- one authoritative writer at a time per owned output
- deployment and analytics preparation may overlap, but release authorization remains serialized
- stop at the release-authorization boundary instead of continuing into feedback

## Resume and Rollback

- resume from the persisted eligible launch node instead of restarting the phase
- rollback by superseding or reclassifying stale launch artifacts rather than deleting history

## Observability

- record launch gate results and decision records
- persist delegated handoffs and changed authoritative artifact paths
- surface launch blockers, required approvals, and active risks in the returned status

## Human Approval Points

- require explicit release-boundary approval after node 31 before entering `feedback`
