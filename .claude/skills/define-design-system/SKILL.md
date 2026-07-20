---
name: define-design-system
description: Define the design tokens, components, variants, and accessibility rules needed to implement the approved high-fidelity direction. Use during design after hi-fi screens and before prototyping.
when_to_use: Use only after high-fidelity design direction exists. Do not use to create engineering components or implementation code.
allowed-tools: Read Grep Glob
---

# Define Design System

## Purpose

Define the design tokens, components, variants, and accessibility rules needed to implement the approved high-fidelity direction. Use during design after hi-fi screens and before prototyping.

## Entry Conditions

- Use only after high-fidelity design direction exists. Do not use to create engineering components or implementation code.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Extract the minimum design tokens and components needed for the approved surfaces.
2. Define required variants, states, and accessibility rules.
3. Keep the system bounded to the MVP.
4. Record the strongest component inconsistency risk.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `design_system_spec`
- `component_inventory`
- `design_system_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not create a speculative full design system beyond MVP needs.
- Do not leave component states implicit.
- Do not defer accessibility rules to engineering.
