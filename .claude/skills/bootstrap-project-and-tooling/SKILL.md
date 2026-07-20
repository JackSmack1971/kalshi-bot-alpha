---
name: bootstrap-project-and-tooling
description: Produce the minimum project bootstrap and tooling readiness evidence for the approved MVP slice, including setup steps, build commands, and CI baseline expectations.
when_to_use: Use after architecture is approved and before backend/frontend implementation starts.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Bootstrap Project And Tooling

## Purpose

Produce the minimum project bootstrap and tooling readiness evidence for the approved MVP slice, including setup steps, build commands, and CI baseline expectations.

## Entry Conditions

- Use after architecture is approved and before backend/frontend implementation starts.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Inspect the active handoff, especially the owned paths, authoritative inputs, and validation command.
2. Make only the minimum tooling or setup changes needed inside the delegated paths.
3. Run the delegated validation command or the smallest equivalent setup verification command when changes occurred.
4. Record the minimum environment and setup needed to build and test the slice.
5. State the CI or command baseline required for reproducibility.
6. Surface environment constraints and setup risks.

## Permitted Tools

- `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `development_guide`
- `ci_baseline`
- `environment_constraints`
- `setup_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not turn this into platform-wide infrastructure redesign.
- Do not assume reproducibility without explicit setup steps.
- Do not hide missing tooling prerequisites.
