---
name: implement-backend-capabilities
description: Produce bounded backend implementation evidence for the approved MVP slice, including contract status, server-side test status, and backend risks.
when_to_use: Use after architecture and setup are ready. Do not use to broaden API scope.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Implement Backend Capabilities

## Purpose

Produce bounded backend implementation evidence for the approved MVP slice, including contract status, server-side test status, and backend risks.

## Entry Conditions

- Use after architecture and setup are ready. Do not use to broaden API scope.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Inspect the active handoff, especially the owned paths, authoritative inputs, and validation command.
2. Make only the minimum backend code or configuration changes needed inside the delegated paths.
3. Run the delegated validation command or the smallest equivalent backend verification command when code changed.
4. Record contract status and server-side test status.
5. Surface backend blockers and risks.

## Permitted Tools

- `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `backend_implementation`
- `contract_status`
- `backend_test_status`
- `backend_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent new backend features.
- Do not claim contract completion without explicit status.
- Do not hide backend test gaps.
