---
name: maintain-risk-register
description: Maintain the idea-to-MVP risk register when the workflow needs risk IDs, categories, likelihood, impact, exposure, early indicators, mitigations, contingencies, or status updates captured consistently. Use when new product, delivery, quality, release, or operational risks appear or existing ones materially change.
when_to_use: Use when risks need to be added, updated, escalated, mitigated, accepted, or closed. Do not use to replace a phase-gate decision or hide blocker severity.
allowed-tools: Read Grep Glob
---

# Maintain Risk Register

## Purpose

Maintain the idea-to-MVP risk register when the workflow needs risk IDs, categories, likelihood, impact, exposure, early indicators, mitigations, contingencies, or status updates captured consistently. Use when new product, delivery, quality, release, or operational risks appear or existing ones materially change.

## Entry Conditions

- Use when risks need to be added, updated, escalated, mitigated, accepted, or closed. Do not use to replace a phase-gate decision or hide blocker severity.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Identify the concrete risk, category, trigger, and affected artifacts or phases.
2. Record likelihood, impact, exposure, early indicators, mitigation, contingency, and owner.
3. Update status and note what evidence changed the risk posture.
4. Return only the bounded register delta and any escalation-worthy items.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `risk_register_update`
- `risk_exposure_summary`
- `mitigation_actions`
- `escalation_items`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not reduce every risk to generic narrative prose.
- Do not hide ownerless or unmitigated high-exposure risks.
- Do not close a risk without evidence that the status changed.
