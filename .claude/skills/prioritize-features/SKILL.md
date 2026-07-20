---
name: prioritize-features
description: Prioritize the candidate feature backlog into a bounded MVP order with explicit dependencies, scoring logic, and exclusions. Use during define after feature ideation and before UX design artifacts.
when_to_use: Use only in define after candidate features exist. Do not use to finalize the PRD or to waive scope tradeoffs.
allowed-tools: Read Grep Glob
---

# Prioritize Features

## Purpose

Prioritize the candidate feature backlog into a bounded MVP order with explicit dependencies, scoring logic, and exclusions. Use during define after feature ideation and before UX design artifacts.

## Entry Conditions

- Use only in define after candidate features exist. Do not use to finalize the PRD or to waive scope tradeoffs.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Apply one explicit prioritization logic to the feature candidates.
2. Separate must-have MVP work from deferred items.
3. State the key dependencies and the strongest exclusion rationale.
4. Record one scope tradeoff that should remain visible in the PRD.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `feature_prioritization`
- `priority_order`
- `excluded_items`
- `dependency_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not hide the prioritization method.
- Do not keep exclusions implicit.
- Do not rank features without showing dependency or evidence tradeoffs.
