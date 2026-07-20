---
name: select-core-problem
description: Choose one primary problem from discovery outputs with explicit rationale and rejected alternatives. Use at the discovery gate when the workflow needs a single approved direction or a request for approval.
when_to_use: Use only after opportunity and validation artifacts exist. Do not use to define MVP scope or architecture.
allowed-tools: Read Grep Glob
---

# Select Core Problem

## Purpose

Choose one primary problem from discovery outputs with explicit rationale and rejected alternatives. Use at the discovery gate when the workflow needs a single approved direction or a request for approval.

## Entry Conditions

- Use only after opportunity and validation artifacts exist. Do not use to define MVP scope or architecture.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Compare the validated candidates against constraints and evidence strength.
2. Select one primary problem statement.
3. Record the rejected alternatives and the reason each lost.
4. Surface the exact human approval needed to continue.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `core_problem_decision`
- `rejected_alternatives`
- `required_approval`
- `gate_recommendation`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not pick multiple primary problems.
- Do not hide why alternatives were rejected.
- Do not imply human approval where none exists.
