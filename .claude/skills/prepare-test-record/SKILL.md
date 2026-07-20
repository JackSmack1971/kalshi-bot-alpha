---
name: prepare-test-record
description: Produce the first vertical slice's test record, including verification strategy, acceptance coverage, residual gaps, and pass or fail readiness. Use after the implementation record exists and before a release recommendation.
when_to_use: Use for release-evidence preparation. Do not use to redefine the product scope or architecture.
allowed-tools: Read Grep Glob
---

# Prepare Test Record

## Purpose

Produce the first vertical slice's test record, including verification strategy, acceptance coverage, residual gaps, and pass or fail readiness. Use after the implementation record exists and before a release recommendation.

## Entry Conditions

- Use for release-evidence preparation. Do not use to redefine the product scope or architecture.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Map the slice requirements to the minimum verification evidence needed.
2. Record what is covered, what is missing, and what still requires execution.
3. Identify release-blocking gaps.
4. Return a readiness recommendation.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `test_record`
- `coverage_map`
- `release_blockers`
- `readiness_recommendation`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not claim tests exist if only plans exist.
- Do not mark a gap covered without evidence.
- Do not collapse functional, usability, and release checks into one vague statement.
