# Idea-to-MVP Workflow Contract

## Objective

Move a product idea from discovery through MVP release and post-launch learning
with explicit gates, traceable artifacts, and bounded rework.

## Trigger

- Direct invocation of `/idea-to-mvp`.
- A request to resume or assess the current idea-to-MVP workflow state.

## Modes

- `guided`: stop after each node and persist the next node cursor for review.
- `phase-autonomous`: run all eligible work in the current phase, then stop at the phase boundary.
- `guardrailed-autonomous`: continue across phases until a blocker, failed gate, or mandatory human approval stops advancement.
- `audit`: inspect persisted state, approvals, and traceability without producing new phase work.
- `re-entry`: infer and validate an existing repository baseline before resuming from the earliest materially incomplete node.

## Phases

1. `discover`
2. `define`
3. `design`
4. `build`
5. `test`
6. `launch`
7. `feedback`

## First Vertical Slice

The first replayable slice is:

1. brainstorm
2. validate problem
3. research market and competitors
4. define target users and JTBD
5. form value proposition
6. core-problem approval stop
7. ideate features
8. prioritize features
9. design user flows
10. design information architecture
11. produce low-fidelity wireframes
12. MVP scope
13. create high-fidelity interface
14. define design system
15. build interactive prototype
16. conduct usability testing
17. prepare design handoff
18. architecture
19. bootstrap project and tooling
20. implement backend capabilities
21. implement frontend experience
22. integrate product components
23. review code and architecture
24. create test plan
25. execute functional testing
26. conduct UAT and usability validation
27. diagnose and fix defects
28. validate performance and security
29. deployment evidence
30. analytics readiness
31. release record
32. post-launch review
33. next-iteration plan

## States and Legal Transitions

- Start in `discover` at the earliest eligible node.
- Advance only through legal phase order: `discover` -> `define` -> `design` -> `build` -> `test` -> `launch` -> `feedback`.
- Stop at any required approval, failed gate, blocked prerequisite, or interrupted recoverable node.
- Resume from persisted workflow state instead of replaying completed nodes blindly.

## Required State

- workflow state document
- artifact manifest
- artifact dependency graph
- risk register
- assumptions register
- handoff packets for delegated work
- gate results for phase exits
- decision records for approvals and architecture decisions

Canonical persisted state lives under:

- `.claude/control-plane/state/idea-to-mvp/workflow-state.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-manifest.json`
- `.claude/control-plane/state/idea-to-mvp/artifact-dependency-graph.json`
- `.claude/control-plane/state/idea-to-mvp/risk-register.json`
- `.claude/control-plane/state/idea-to-mvp/assumptions-register.json`
- `.claude/control-plane/state/idea-to-mvp/gate-results.jsonl`
- `.claude/control-plane/state/idea-to-mvp/decision-records.jsonl`
- `.claude/control-plane/state/idea-to-mvp/artifacts/`
- `.claude/control-plane/state/idea-to-mvp/handoffs/`

## Input Contract

- `mode` must be one of `guided`, `phase-autonomous`, `guardrailed-autonomous`, `audit`, or `re-entry`
- `currentPhase`, when supplied, is a phase hint and must still be reconciled against persisted state
- approvals arrive as explicit booleans and must never be invented
- artifact and state paths must resolve to the canonical idea-to-MVP state directory

## Output Contract

- every orchestrator return exposes the runtime output contract below
- every stateful run persists workflow state, artifact-manifest updates, handoffs, gate results, and decision records through the canonical state-management path

## Read Set

- canonical workflow state, artifact manifest, dependency graph, risk register, and assumptions register
- authoritative artifact markdown under `.claude/control-plane/state/idea-to-mvp/artifacts/`
- persisted handoffs, gate results, and decision records

## Write Set

- canonical workflow state and artifact manifest
- authoritative artifact markdown produced by the active node
- persisted handoffs, gate results, decision records, risk-register updates, and assumption updates

## Success Criteria

- move only through eligible nodes, stop at explicit approvals, and preserve traceability from problem evidence through release and feedback
- keep the artifact manifest and workflow state aligned with reality rather than with intent

## Approval Gates

- product direction after discovery
- MVP scope after define
- release boundary before launch
- any manifest change touching the control-plane trust boundary

The workflow must stop and return structured status when a required approval is
missing. It must not invent the approval or continue past the gate.

## Runtime Output Contract

Every orchestrator return must expose:

- `currentPhase`
- `completedNodes`
- `eligibleNodes`
- `blockedNodes`
- `requiredHumanDecisions`
- `activeRisks`
- `plan.artifactsToProduce`
- `plan.parallelism`
- `plan.proposedExecutionPlan`
- `plan.stopCondition`

## Independent Validation

- Persisted handoffs must name a reviewer that is different from the assigned specialist.
- A delegated specialist cannot be the only validator of its own authoritative output.

## Traceability

- Persisted artifact-manifest entries must record direct upstream artifact dependencies for every non-root artifact.
- Traceability must remain explicit enough to audit problem-to-test and release evidence chains.

## Rework Policy

- Reopen only affected downstream artifacts by default.
- Block advancement when an authoritative upstream artifact is stale.
- Record stale status instead of regenerating all artifacts blindly.
- Mark interrupted workflow nodes as `recoverable` at turn stop when watched state or workflow files remain dirty.

## Failure Criteria

- return `blocked` when missing evidence, stale authoritative artifacts, or failed gates make progress unsafe
- return `recoverable` when interruption leaves partial state or artifact updates that must be resumed explicitly

## Budgets

- one authoritative writer at a time
- no nested delegation or agent-team expansion unless explicitly enabled outside this workflow contract
- keep per-phase work bounded and stop at the next required approval in guided and phase-autonomous modes

## Resume and Rollback

- resume from persisted eligible nodes and canonical state instead of recomputing from memory
- rollback by superseding or reclassifying stale artifacts and by preserving append-only gate and decision evidence

## Observability

- return structured status with blockers, approvals, active risks, artifacts to produce, plan, and stop condition
- persist gate results, decision records, handoffs, and changed authoritative artifact paths for audit
- preserve enough evidence for audit mode and re-entry mode to validate the current repository state

## Human Approval Points

- discovery direction after `discover`
- MVP scope after `define`
- release boundary before `feedback`
- any control-plane trust-boundary change such as a required manifest edit
