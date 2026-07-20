---
name: validate-artifact-contract
description: Validate an idea-to-MVP artifact contract for structure, required fields, traceability, unresolved placeholders, and internal consistency. Use when a workflow artifact exists and needs contract-level review before it can count as evidence.
when_to_use: Use after a specialist draft exists and before a gate relies on it. Do not use as a substitute for independent human approval.
allowed-tools: Read Grep Glob
---

# Validate Artifact Contract

## Purpose

Validate an idea-to-MVP artifact contract for structure, required fields, traceability, unresolved placeholders, and internal consistency. Use when a workflow artifact exists and needs contract-level review before it can count as evidence.

## Entry Conditions

- Use after a specialist draft exists and before a gate relies on it. Do not use as a substitute for independent human approval.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Check required fields, structure, and expected sections.
2. Verify direct traceability to authoritative upstream inputs and decisions.
3. Flag unresolved placeholders, contradictions, and missing evidence.
4. Return a pass, conditional, or fail-style contract assessment with concrete findings.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `contract_assessment`
- `traceability_findings`
- `consistency_findings`
- `required_fixes`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not accept placeholder text, missing required sections, or broken traceability.
- Do not confuse a well-formatted artifact with a sufficient one.
- Do not approve artifacts whose inputs contradict their conclusions.
