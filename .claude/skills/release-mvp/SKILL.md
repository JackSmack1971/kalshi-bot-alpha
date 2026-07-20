---
name: release-mvp
description: Produce the product-release decision package from deployment and release evidence, including release notes, known limitations, required approval, and the final release recommendation. Use during the launch phase after deployment and analytics readiness are summarized.
when_to_use: Use only after deployment and analytics evidence are available. Do not use to bypass product-owner approval.
allowed-tools: Read Grep Glob
---

# Release MVP

## Purpose

Produce the product-release decision package from deployment and release evidence, including release notes, known limitations, required approval, and the final release recommendation. Use during the launch phase after deployment and analytics readiness are summarized.

## Entry Conditions

- Use only after deployment and analytics evidence are available. Do not use to bypass product-owner approval.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Summarize the release boundary and evidence available.
2. Write release notes and known limitations.
3. State the exact approval still required for exposure.
4. Return the release recommendation and follow-up actions.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `release_record`
- `release_notes`
- `required_approval`
- `release_recommendation`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not treat deployment success as release authorization.
- Do not hide known limitations or missing evidence.
- Do not invent product-owner approval.
