---
name: integrate-product-components
description: Produce bounded integration evidence for backend and frontend candidates, including critical-path status and integration risks.
when_to_use: Use after backend and frontend candidates exist. Do not use to re-architect unrelated parts of the system.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Integrate Product Components

## Purpose

Produce bounded integration evidence for backend and frontend candidates, including critical-path status and integration risks.

## Entry Conditions

- Use after backend and frontend candidates exist. Do not use to re-architect unrelated parts of the system.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Inspect the active handoff, especially the owned paths, shared contracts, and validation command.
2. Make only the minimum integration or defect-resolution changes needed inside the delegated paths.
3. Run the delegated validation command or the smallest equivalent integration verification command when code changed.
4. Record critical-path status and interface alignment.
5. Surface integration risks and blockers.

## Permitted Tools

- `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `integration_report`
- `critical_path_status`
- `integration_risks`
- `open_integration_issues`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not rewrite ownership boundaries casually.
- Do not call critical paths passing without explicit status.
- Do not hide interface mismatches.
