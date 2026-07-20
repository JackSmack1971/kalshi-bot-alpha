---
name: create-test-plan
description: Produce the minimum test plan and traceability evidence for the approved MVP slice, including requirement coverage and risk-driven checks.
when_to_use: Use after build artifacts exist and before functional execution starts.
allowed-tools: Read Grep Glob
---

# Create Test Plan

## Purpose

Produce the minimum test plan and traceability evidence for the approved MVP slice, including requirement coverage and risk-driven checks.

## Entry Conditions

- Use after build artifacts exist and before functional execution starts.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Map requirements and risks to concrete test coverage.
2. Record traceability and uncovered areas.
3. State what still needs execution before launch.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `test_plan`
- `traceability_matrix`
- `coverage_gaps`
- `test_execution_order`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not pretend planned tests were executed.
- Do not skip traceability for critical requirements.
- Do not hide uncovered risks.
