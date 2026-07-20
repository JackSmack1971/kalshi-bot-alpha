---
name: implement-frontend-experience
description: Produce bounded frontend implementation evidence for the approved MVP slice, including accessibility status, UI test status, and frontend risks.
when_to_use: Use after design handoff and API expectations are explicit. Do not use to invent UI scope.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Implement Frontend Experience

## Purpose

Produce bounded frontend implementation evidence for the approved MVP slice, including accessibility status, UI test status, and frontend risks.

## Entry Conditions

- Use after design handoff and API expectations are explicit. Do not use to invent UI scope.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Inspect the active handoff, especially the owned paths, authoritative inputs, and validation command.
2. Make only the minimum frontend code or configuration changes needed inside the delegated paths.
3. Run the delegated validation command or the smallest equivalent frontend verification command when code changed.
4. Record accessibility status and UI test status.
5. Surface frontend blockers and risks.

## Permitted Tools

- `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `frontend_implementation`
- `accessibility_status`
- `frontend_test_status`
- `frontend_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent additional flows or surfaces.
- Do not defer accessibility requirements silently.
- Do not mark the frontend done without explicit test status.
