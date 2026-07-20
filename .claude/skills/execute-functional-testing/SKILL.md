---
name: execute-functional-testing
description: Produce bounded functional test evidence for the MVP candidate, including acceptance status, failures, and residual risks.
when_to_use: Use after the test plan exists and a candidate build is available.
allowed-tools: Read Grep Glob
---

# Execute Functional Testing

## Purpose

Produce bounded functional test evidence for the MVP candidate, including acceptance status, failures, and residual risks.

## Entry Conditions

- Use after the test plan exists and a candidate build is available.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Summarize functional coverage against the test plan.
2. Record failures, pass status, and residual risks.
3. State whether the acceptance threshold was met.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `functional_test_report`
- `acceptance_status`
- `failed_paths`
- `functional_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not claim a passing threshold without explicit evidence.
- Do not collapse failed and untested paths together.
- Do not hide release-blocking failures.
