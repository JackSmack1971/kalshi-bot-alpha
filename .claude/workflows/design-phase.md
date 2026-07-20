# Design Phase Contract

## Objective

Turn the approved MVP definition into implementation-ready experience evidence
before architecture or engineering decisions proceed.

## Inputs

- approved MVP PRD
- user flows
- information architecture
- wireframe specification
- constraints

## Outputs

- high-fidelity design spec
- design-system spec
- prototype manifest
- usability findings
- design handoff

## States and Legal Transitions

- Enter from `design` after MVP-scope approval is recorded.
- Advance node-by-node through nodes 13 to 17.
- Exit to `build` only when design handoff and usability evidence are ready.
- Return `blocked` or `recoverable` instead of advancing when design evidence is incomplete or interrupted.

## Input Contract

- approved define artifacts are authoritative markdown inputs under `artifacts/`
- constraints remain bounded carry-forward instructions and must not change approved scope
- usability disposition must be explicit rather than inferred

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist design artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- approved define artifacts under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- design artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- design handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough design evidence for build to proceed without redefining the experience contract

## Gate

The phase passes only when:

- approved MVP requirements have mapped interaction surfaces
- visual, responsive, and accessibility expectations are explicit
- critical usability failures are either resolved or called out as blockers
- the engineering handoff preserves scope boundaries

## Rework

- revisit high-fidelity or system work when usability exposes critical failures
- revisit prototype scenarios when key flows are missing
- stop before build when the design handoff is not implementation-ready

## Failure Criteria

- block when usability or handoff evidence says design is not implementation-ready
- mark the active node `recoverable` when interruption leaves partial design outputs or dirty workflow files behind

## Budgets

- one authoritative writer at a time
- allow bounded overlap only after high-fidelity direction is stable
- stop before build when design evidence is blocked

## Resume and Rollback

- resume from the persisted eligible design node instead of restarting the phase
- rollback by superseding or reclassifying stale design artifacts rather than deleting history

## Observability

- record design gate results and decision records
- persist delegated handoffs and changed authoritative artifact paths
- surface design blockers, required approvals, and active risks in the returned status

## Human Approval Points

- no standalone human approval boundary inside this phase; usability blockers and build readiness govern exit

## Ownership

- UI designer owns nodes 13, 14, 15, and 17
- UX researcher owns node 16
- design must not skip usability evidence
