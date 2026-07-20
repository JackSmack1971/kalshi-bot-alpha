---
name: conduct-usability-testing
description: Evaluate the interactive prototype (a design-stage mock, not the built MVP candidate) against target journeys and return evidence-backed usability findings with severity and recommended action. Use during design after prototype preparation and before design handoff. For usability evidence on the built/functional candidate, use conduct-uat-and-usability-validation instead.
when_to_use: Use only after a prototype manifest exists, during the design phase, before a built/functional candidate exists. Do not use to approve implementation or to conceal critical usability findings. Once functional evidence exists, use conduct-uat-and-usability-validation instead.
allowed-tools: Read Grep Glob
---

# Conduct Usability Testing

## Purpose

Evaluate the interactive prototype (a design-stage mock, not the built MVP candidate) against target journeys and return evidence-backed usability findings with severity and recommended action. Use during design after prototype preparation and before design handoff. For usability evidence on the built/functional candidate, use conduct-uat-and-usability-validation instead.

## Entry Conditions

- Use only after a prototype manifest exists. Do not use to approve implementation or to conceal critical usability findings.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Evaluate the prototype against the critical journeys and test goals.
2. Record the most important findings with severity and evidence.
3. Distinguish resolved assumptions from unresolved usability risks.
4. Recommend the next action clearly.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `usability_findings`
- `severity_summary`
- `recommended_action`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent participant evidence.
- Do not collapse findings into vague approval language.
- Do not suppress critical or recurring issues.
