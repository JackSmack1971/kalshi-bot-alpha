# Change Impact Loop Contract

## Objective

Reassess downstream idea-to-MVP artifacts after an authoritative upstream change
without regenerating the entire workflow blindly.

## Inputs

- one or more changed artifact ids
- the canonical idea-to-MVP state directory

## Outputs

- updated artifact manifest statuses
- list of changed artifacts
- list of downstream artifacts marked `fully_stale` or `partially_stale`
- validation result after the update

## States and Legal Transitions

- Enter when one or more authoritative artifact ids have changed.
- Reclassify only affected downstream artifacts.
- Exit once the manifest validates cleanly or return `blocked` when impact analysis is not trustworthy.
- Return `recoverable` if interruption leaves partial state updates.

## Input Contract

- changed artifact ids are stable artifact ids, not filesystem paths
- the artifact dependency graph and artifact manifest are canonical inputs
- unknown changed artifact ids must block the loop instead of being ignored

## Output Contract

- return updated changed-artifact statuses plus validation evidence
- persist manifest status changes under the canonical idea-to-MVP state directory without regenerating unrelated artifacts

## Read Set

- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-dependency-graph.json`
- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`

## Write Set

- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- `.claude/control-plane/state/idea-to-mvp/workflow-state.json` when stale authoritative artifacts block downstream progress

## Success Criteria

- satisfy the gate below and preserve bounded downstream rework

## Status Rules

- changed authoritative artifacts become `review_required`
- directly dependent downstream artifacts become `fully_stale`
- transitive downstream artifacts become `partially_stale`
- terminal `superseded` or `rejected` artifacts remain unchanged

## Gate

The loop passes only when:

- the dependency graph is machine-readable and valid
- the updated artifact manifest validates cleanly
- only affected downstream artifacts are reclassified
- untouched artifacts are not regenerated automatically

## Rework

- fix the dependency graph when an artifact id is missing or duplicated
- rerun the loop after recording the upstream artifact change
- stop and escalate when required changed artifact ids are unknown

## Failure Criteria

- block when dependency-graph integrity or changed-artifact identity is not trustworthy
- mark the update `recoverable` when interruption leaves partial manifest reclassification behind

## Budgets

- one authoritative writer at a time
- no blind artifact regeneration inside the impact loop
- stop after manifest reclassification and validation

## Resume and Rollback

- resume from persisted stale-artifact state instead of reclassifying from memory
- rollback by restoring the last valid manifest status set from persisted state, not by deleting history

## Observability

- surface changed artifacts, stale artifacts, and validation results
- record manifest-status transitions in canonical workflow state
- preserve enough evidence to audit why each downstream artifact was reclassified

## Human Approval Points

- no standalone human approval boundary; escalate only when changed artifact identity or dependency integrity is unknown
