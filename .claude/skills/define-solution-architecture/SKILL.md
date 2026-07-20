---
name: define-solution-architecture
description: Define the minimum architecture, interfaces, constraints, and feasibility findings required for the approved MVP slice. Use after scope is defined and before implementation or test records are prepared.
when_to_use: Use only for the approved MVP slice. Do not use to expand scope or design the full product roadmap.
allowed-tools: Read Grep Glob
---

# Define Solution Architecture

## Purpose

Define the minimum architecture, interfaces, constraints, and feasibility findings required for the approved MVP slice. Use after scope is defined and before implementation or test records are prepared.

## Entry Conditions

- Use only for the approved MVP slice. Do not use to expand scope or design the full product roadmap.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Describe the minimum system shape that satisfies the MVP.
2. Identify interfaces, data boundaries, and major technical constraints.
3. Record feasibility risks and architecture decisions.
4. Flag unresolved items that block implementation or test planning.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `architecture_summary`
- `architecture_decisions`
- `feasibility_risks`
- `open_technical_questions`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not optimize for a future platform the MVP does not need.
- Do not hide infeasibility behind optimistic prose.
- Do not change product scope to fit a preferred design.
