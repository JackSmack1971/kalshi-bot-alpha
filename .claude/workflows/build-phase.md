# Build Phase Contract

## Objective

Turn the approved product and design contracts into bounded implementation and
integration evidence before test or launch work proceeds.

## Inputs

- approved MVP PRD
- design handoff
- constraints

## Outputs

- architecture summary
- development guide
- backend implementation
- frontend implementation
- integration report
- code-review report
- implementation record

## States and Legal Transitions

- Enter from `build` after design evidence is ready.
- Advance node-by-node through nodes 18 to 23.
- Exit to `test` only when architecture, implementation, integration, and independent review evidence are ready.
- Return `blocked` or `recoverable` instead of advancing when build evidence is incomplete or interrupted.

## Input Contract

- approved PRD and design handoff are authoritative markdown inputs under `artifacts/`
- shared contracts must be explicit before backend and frontend work run in parallel
- review disposition must be returned explicitly rather than inferred

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist build artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- approved design and define artifacts under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- build artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- build handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough implementation and review evidence for test work to begin without rediscovering build intent

## Gate

The phase passes only when:

- architecture constraints are explicit
- backend and frontend work align with shared contracts
- integration evidence exists
- independent technical review does not report unresolved blockers

## Rework

- revisit architecture when feasibility issues invalidate MVP assumptions
- revisit integration when backend and frontend contracts drift
- stop before test when review blockers remain unresolved

## Failure Criteria

- block when architecture, integration, or review findings leave unresolved build blockers
- mark the active node `recoverable` when interruption leaves partial build outputs or dirty workflow files behind

## Budgets

- one authoritative writer per owned path
- backend and frontend may run in parallel only after shared contracts are explicit
- stop before test when independent review blocks readiness

## Resume and Rollback

- resume from the persisted eligible build node instead of restarting the phase
- rollback by superseding or reclassifying stale build artifacts rather than deleting history

## Observability

- record build gate results and decision records
- persist delegated handoffs, shared contracts, and changed authoritative artifact paths
- surface build blockers, required approvals, and active risks in the returned status

## Human Approval Points

- no standalone human approval boundary inside this phase; independent review and downstream test readiness govern exit

## Ownership

- solution architect owns node 18 and the implementation record
- DevOps owns node 19
- backend, frontend, and integration engineers own nodes 20, 21, and 22
- technical lead owns the independent review at node 23
