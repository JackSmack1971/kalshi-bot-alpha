---
name: define-target-users-and-jtbd
description: Convert discovery evidence into bounded target-user segments and jobs-to-be-done that trace to validated problems and available alternatives. Use during discovery after problem validation and market research.
when_to_use: Use only in discovery. Do not use to redefine the core problem after approval or to scope MVP features.
allowed-tools: Read Grep Glob
---

# Define Target Users And JTBD

## Purpose

Convert discovery evidence into bounded target-user segments and jobs-to-be-done that trace to validated problems and available alternatives. Use during discovery after problem validation and market research.

## Entry Conditions

- Use only in discovery. Do not use to redefine the core problem after approval or to scope MVP features.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Identify the most affected user segments from the discovery evidence.
2. State each segment's primary job-to-be-done and pain context.
3. Connect the segment and job to evidence or mark it experimental.
4. Call out the main uncertainty that could change downstream scope.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `target_users_jtbd`
- `primary_segments`
- `jobs`
- `open_user_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent segments unsupported by the discovery evidence.
- Do not collapse distinct users into one vague persona.
- Do not hide uncertainty about the primary job.
