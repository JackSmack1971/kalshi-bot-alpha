# Discover Phase Contract

## Objective

Establish the core problem worth solving before downstream product definition or
implementation begins.

## Inputs

- founder intent or user request
- constraints
- existing product or repository context
- any prior discovery artifacts

## Outputs

- opportunity catalog
- problem validation
- market and competitor report
- target users and JTBD
- value proposition
- core problem decision

## States and Legal Transitions

- Enter from `discover` when node 1 is the next eligible node.
- Advance node-by-node through nodes 1 to 6.
- Exit to `define` only after discovery artifacts exist and product-direction approval is recorded.
- Return `blocked` or `recoverable` instead of advancing when discovery evidence is incomplete or the run is interrupted.

## Input Contract

- founder intent and constraints are freeform strings or bullet lists
- prior discovery artifacts, when present, are authoritative markdown artifacts under `artifacts/`
- approvals arrive from persisted workflow state and must never be inferred

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist discovery artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- prior discovery artifacts under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- discovery artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- discovery handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough evidence to resume from the next phase without rerunning discovery blindly

## Gate

The phase passes only when:

- one core problem is selected
- at least one target segment is defined
- evidence gaps are explicit
- alternatives are documented
- the product owner accepts the discovery direction

## Rework

- repeat market research when evidence is weak
- repeat target-user work when the affected user is unclear
- stop before define when discovery artifacts conflict

## Failure Criteria

- block when evidence gaps, conflicting artifacts, or missing approval prevent a trustworthy core-problem decision
- mark the active node `recoverable` when interruption leaves partial discovery outputs or dirty workflow files behind

## Budgets

- one authoritative writer at a time
- keep discovery sequential at the phase level even if research fans out internally
- stop at the discovery approval gate instead of continuing into define

## Resume and Rollback

- resume from the persisted eligible discovery node instead of restarting the phase
- rollback by superseding or reclassifying stale discovery artifacts rather than deleting history

## Observability

- record discovery gate results and decision records
- persist delegated handoffs and changed authoritative artifact paths
- surface discovery blockers, required approvals, and active risks in the returned status

## Human Approval Points

- require explicit product-direction approval after node 6 before entering `define`

## Ownership

- product strategist owns nodes 1, 2, 4, 5, and 6
- market researcher owns node 3
- discovery must not collapse market research into a vague strategist summary
