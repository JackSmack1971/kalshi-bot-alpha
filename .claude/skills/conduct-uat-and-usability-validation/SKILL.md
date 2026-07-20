---
name: conduct-uat-and-usability-validation
description: Produce UAT and usability-validation evidence for the built/functional MVP candidate (not a design-stage prototype), including accepted outcomes, rejected outcomes, and usability risks. Use during the test phase after functional evidence exists. For usability evidence on a design-stage prototype, use conduct-usability-testing instead.
when_to_use: Use after functional evidence exists and candidate journeys can be exercised, during the test phase — not on a design-stage prototype. Use conduct-usability-testing for prototype-stage evaluation.
allowed-tools: Read Grep Glob
---

# Conduct UAT And Usability Validation

## Purpose

Produce UAT and usability-validation evidence for the built/functional MVP candidate (not a design-stage prototype), including accepted outcomes, rejected outcomes, and usability risks. Use during the test phase after functional evidence exists. For usability evidence on a design-stage prototype, use conduct-usability-testing instead.

## Entry Conditions

- Use after functional evidence exists and candidate journeys can be exercised.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Evaluate the candidate against critical user journeys.
2. Record accepted outcomes, rejected outcomes, and usability risks.
3. State the UAT disposition explicitly.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `uat_report`
- `uat_disposition`
- `accepted_outcomes`
- `usability_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent user acceptance.
- Do not suppress critical journey failures.
- Do not treat functional pass status as UAT acceptance automatically.
