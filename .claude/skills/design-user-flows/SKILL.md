---
name: design-user-flows
description: Produce bounded user flows for prioritized MVP capabilities, including happy paths and important failure or recovery paths. Use during define before information architecture and wireframes.
when_to_use: Use only after feature prioritization. Do not use to create visual design systems or final UI polish.
allowed-tools: Read Grep Glob
---

# Design User Flows

## Purpose

Produce bounded user flows for prioritized MVP capabilities, including happy paths and important failure or recovery paths. Use during define before information architecture and wireframes.

## Entry Conditions

- Use only after feature prioritization. Do not use to create visual design systems or final UI polish.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Map each in-scope capability to a primary user flow.
2. Add alternate, error, and recovery states where they matter.
3. Keep flows traceable to the prioritized scope.
4. Record open UX decisions instead of hiding them.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `user_flows`
- `flow_coverage`
- `open_ux_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not omit failure or recovery behavior when it affects task success.
- Do not invent new features to simplify the flow.
- Do not collapse multiple user stories into one vague journey.
