---
name: record-decision
description: Produce a structured decision record when the idea-to-MVP workflow needs a bounded decision, context, options, evidence, rationale, consequences, risks, reversal conditions, owner, or affected-artifact list captured consistently. Use for approvals and architecture or product decisions that should be replayable later.
when_to_use: Use when a real decision has been made or is ready for human approval. Do not use to smuggle in a new decision that the workflow has not actually reached.
allowed-tools: Read Grep Glob
---

# Record Decision

## Purpose

Produce a structured decision record when the idea-to-MVP workflow needs a bounded decision, context, options, evidence, rationale, consequences, risks, reversal conditions, owner, or affected-artifact list captured consistently. Use for approvals and architecture or product decisions that should be replayable later.

## Entry Conditions

- Use when a real decision has been made or is ready for human approval. Do not use to smuggle in a new decision that the workflow has not actually reached.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Capture the decision context, options considered, and authoritative evidence.
2. Record the chosen option, rationale, consequences, risks, and reversal conditions.
3. Name the decision owner, date, and affected artifacts explicitly.
4. Return a portable decision record that can be persisted without extra interpretation.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `decision_record`
- `options_considered`
- `decision_risks`
- `affected_artifacts`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent evidence or approved status.
- Do not collapse rejected options into one-line placeholders.
- Do not omit consequences, risks, or reversal conditions.
