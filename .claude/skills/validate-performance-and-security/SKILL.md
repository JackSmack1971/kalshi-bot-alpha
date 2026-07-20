---
name: validate-performance-and-security
description: Produce bounded performance and security validation evidence for the MVP candidate, including threshold disposition and residual risks.
when_to_use: Use after functional and UAT evidence exist and before launch preparation begins.
allowed-tools: Read Grep Glob
---

# Validate Performance And Security

## Purpose

Produce bounded performance and security validation evidence for the MVP candidate, including threshold disposition and residual risks.

## Entry Conditions

- Use after functional and UAT evidence exist and before launch preparation begins.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Summarize the candidate and the thresholds being checked.
2. Record performance evidence, security evidence, and residual risks.
3. State the combined disposition explicitly.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `performance_report`
- `security_report`
- `residual_risks`
- `validation_disposition`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not invent benchmark or security evidence.
- Do not hide residual findings behind a passing summary.
- Do not waive threshold failures without explicit authority.
