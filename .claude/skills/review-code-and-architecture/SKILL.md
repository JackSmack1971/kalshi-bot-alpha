---
name: review-code-and-architecture
description: Produce independent review evidence for the integrated MVP candidate, including blocker-level findings and accepted findings.
when_to_use: Use after integration and before test sign-off. Do not use to restate implementation notes.
allowed-tools: Read Grep Glob
---

# Review Code And Architecture

## Purpose

Produce independent review evidence for the integrated MVP candidate, including blocker-level findings and accepted findings.

## Entry Conditions

- Use after integration and before test sign-off. Do not use to restate implementation notes.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Review the integrated candidate against approved scope and architecture.
2. Separate blocking findings from accepted findings.
3. Leave a clear review disposition.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `code_review_report`
- `blocking_findings`
- `accepted_findings`
- `review_disposition`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not hide blocker-level findings.
- Do not promote speculative style nits to blockers.
- Do not grade your own work as sufficient evidence.
