# Define Phase Contract

## Objective

Turn the approved core problem into a bounded MVP product contract before
design, build, or test work proceeds.

## Inputs

- approved core problem decision
- target users and JTBD
- constraints
- prior discovery artifacts

## Outputs

- feature candidate backlog
- feature prioritization
- user flows
- information architecture
- wireframe specification
- MVP PRD

## States and Legal Transitions

- Enter from `define` after discovery approval is recorded.
- Advance node-by-node through nodes 7 to 12.
- Exit to `design` only after MVP-scope approval is recorded.
- Return `blocked` or `recoverable` instead of advancing when define artifacts are incomplete or interrupted.

## Input Contract

- approved discovery artifacts are authoritative markdown inputs under `artifacts/`
- constraints are carried forward as strings or bullets and may limit scope but must not replace approval
- approvals come from persisted workflow state only

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist define artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- approved discovery artifacts under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- define artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- define handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough scope and UX-structure evidence to resume design without redoing define work blindly

## Gate

The phase passes only when:

- every MVP feature traces to the core problem
- acceptance criteria are observable
- failure, loading, empty, and recovery states are visible
- scope exclusions are explicit
- the product owner accepts the MVP boundary

## Rework

- revisit feature prioritization when dependencies exceed MVP bounds
- revisit UX structure when flows omit failure or recovery states
- stop before design when scope or acceptance criteria are still ambiguous

## Failure Criteria

- block when scope, acceptance criteria, or approval status cannot support design work
- mark the active node `recoverable` when interruption leaves partial define outputs or dirty workflow files behind

## Budgets

- one authoritative writer at a time
- keep define sequential at the phase level so downstream UX structure does not outrun scope
- stop at the MVP-scope approval gate instead of continuing into design

## Resume and Rollback

- resume from the persisted eligible define node instead of restarting the phase
- rollback by superseding or reclassifying stale define artifacts rather than deleting history

## Observability

- record define gate results and decision records
- persist delegated handoffs and changed authoritative artifact paths
- surface define blockers, required approvals, and active risks in the returned status

## Human Approval Points

- require explicit MVP-scope approval after node 12 before entering `design`

## Ownership

- product manager owns nodes 7, 8, and 12
- UX designer owns nodes 9, 10, and 11
- definition must stop for explicit MVP-scope approval
