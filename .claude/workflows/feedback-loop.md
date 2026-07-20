# Feedback Loop Contract

## Objective

Turn post-launch telemetry and user feedback into an evidence-backed next-step
decision for the idea-to-MVP workflow.

## Inputs

- telemetry summary
- user feedback
- known defects
- strategy context

## Outputs

- post-launch review
- signal synthesis
- next-iteration plan
- one decision outcome: continue, change, expand, or stop

## States and Legal Transitions

- Enter from `feedback` after release authorization is recorded.
- Advance node-by-node through nodes 32 and 33.
- Exit in a learning-ready state once the next-step decision is captured.
- Return `blocked` or `recoverable` instead of closing the loop when evidence is incomplete or interrupted.

## Input Contract

- telemetry, feedback, and defect summaries are authoritative inputs for learning work
- decision options are bounded to continue, change, expand, or stop
- post-launch evidence quality must be explicit rather than assumed

## Output Contract

- return structured workflow status with `currentPhase`, `status`, `completedNodes`, `eligibleNodes`, `blockedNodes`, `artifacts`, `requiredHumanDecisions`, and `activeRisks`
- persist feedback artifacts, handoffs, gate results, and decision records under the canonical idea-to-MVP state directory

## Read Set

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- launch artifacts and feedback inputs under `.claude/control-plane/state/idea-to-mvp/artifacts/`

## Write Set

- feedback artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- feedback handoffs under `.claude/control-plane/state/idea-to-mvp/handoffs/`
- canonical workflow state, artifact manifest, gate results, and decision records

## Success Criteria

- satisfy the gate below and persist enough learning evidence for a defensible next-step decision

## Gate

The phase passes only when:

- signals are normalized instead of listed raw
- the MVP hypothesis is explicitly reassessed
- the next-step decision is documented
- data-quality risks remain visible

## Rework

- block when telemetry cannot support the hypothesis review
- repeat synthesis when feedback is contradictory or too raw to act on
- stop before roadmap expansion when the evidence does not support it

## Failure Criteria

- block when telemetry or normalized feedback cannot support the hypothesis review
- mark the active node `recoverable` when interruption leaves partial feedback outputs or dirty workflow files behind

## Budgets

- one authoritative writer at a time
- keep synthesis and next-step planning sequential at the phase level
- stop after the next-step decision instead of auto-starting another iteration

## Resume and Rollback

- resume from the persisted eligible feedback node instead of restarting the phase
- rollback by superseding or reclassifying stale feedback artifacts rather than deleting history

## Observability

- record feedback gate results and decision records
- persist delegated handoffs and changed authoritative artifact paths
- surface data-quality blockers, required approvals, and active risks in the returned status

## Human Approval Points

- require explicit approval for the next-iteration decision before starting a new iteration
