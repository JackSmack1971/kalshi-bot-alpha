---
name: prepare-design-handoff
description: Convert the approved design artifacts into an engineering-ready design handoff with states, behavior, accessibility, data, and tracking requirements. Use at the end of design before technical architecture and implementation.
when_to_use: Use only after usability findings are available. Do not use to invent engineering behavior or to bypass unresolved critical usability issues.
allowed-tools: Read Grep Glob
---

# Prepare Design Handoff

## Purpose

Convert the approved design artifacts into an engineering-ready design handoff with states, behavior, accessibility, data, and tracking requirements. Use at the end of design before technical architecture and implementation.

## Entry Conditions

- Use only after usability findings are available. Do not use to invent engineering behavior or to bypass unresolved critical usability issues.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Merge the approved design artifacts and usability outcomes into one handoff.
2. Specify states, behavior, accessibility, data, and tracking requirements.
3. Keep every handoff section traceable to design and product artifacts.
4. Record known limitations explicitly.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `design_handoff`
- `handoff_coverage`
- `known_limitations`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not leave key behavior to “developer decides”.
- Do not omit loading, empty, error, or disabled states when required.
- Do not hide known limitations or unresolved UX decisions.
