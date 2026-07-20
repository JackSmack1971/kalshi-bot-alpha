---
name: assess-change-impact
description: Assess downstream impact when an upstream idea-to-MVP artifact changes and the workflow needs bounded stale-status classification, required rework, or review-required outputs. Use when target users, scope, design, implementation, test, or release evidence changed and only the affected downstream work should reopen.
when_to_use: Use only after an upstream artifact has changed or been challenged. Do not use to regenerate the whole operating system by default.
allowed-tools: Read Grep Glob
---

# Assess Change Impact

## Purpose

Assess downstream impact when an upstream idea-to-MVP artifact changes and the workflow needs bounded stale-status classification, required rework, or review-required outputs. Use when target users, scope, design, implementation, test, or release evidence changed and only the affected downstream work should reopen.

## Entry Conditions

- Use only after an upstream artifact has changed or been challenged. Do not use to regenerate the whole operating system by default.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Identify the changed authoritative artifact and its direct downstream consumers.
2. Classify each affected artifact as `review_required`, `partially_stale`, or `fully_stale`.
3. State what must be regenerated, what can stand with review, and what human decisions are reopened.
4. Return only the bounded rework set and the reasoning chain.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `impact_assessment`
- `stale_artifacts`
- `required_rework`
- `reopened_decisions`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not mark every downstream artifact stale without tracing the dependency path.
- Do not hide contradictions between the changed artifact and existing outputs.
- Do not approve unchanged artifacts automatically when evidence is weak.
