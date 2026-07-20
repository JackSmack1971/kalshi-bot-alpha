---
name: define-mvp-scope-and-requirements
description: Convert an approved core problem into a bounded MVP contract with scope, exclusions, acceptance criteria, dependencies, and metrics. Use during the define phase before architecture or implementation records.
when_to_use: Use only after discovery approval. Do not use to approve architecture or release readiness.
allowed-tools: Read Grep Glob
---

# Define MVP Scope And Requirements

## Purpose

Convert an approved core problem into a bounded MVP contract with scope, exclusions, acceptance criteria, dependencies, and metrics. Use during the define phase before architecture or implementation records.

## Entry Conditions

- Use only after discovery approval. Do not use to approve architecture or release readiness.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Define the MVP hypothesis and product outcome.
2. List in-scope capabilities and explicit non-goals.
3. Write observable acceptance criteria and success metrics.
4. Record dependencies, risks, and open decisions.
5. State the exact approval needed before build-oriented work proceeds.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `mvp_prd`
- `scope_boundaries`
- `acceptance_criteria`
- `dependencies_and_risks`
- `required_approval`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not add features that do not trace to the core problem.
- Do not leave exclusions implicit.
- Do not hide open decisions inside vague requirements.
