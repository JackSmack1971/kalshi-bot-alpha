---
name: configure-product-analytics
description: Produce the MVP analytics plan and event-validation view from KPI and event requirements. Use after launch inputs are known and before release authorization.
when_to_use: Use only when KPI and event requirements exist. Do not use to fabricate telemetry that has not been validated.
allowed-tools: Read Grep Glob
---

# Configure Product Analytics

## Purpose

Produce the MVP analytics plan and event-validation view from KPI and event requirements. Use after launch inputs are known and before release authorization.

## Entry Conditions

- Use only when KPI and event requirements exist. Do not use to fabricate telemetry that has not been validated.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Map KPI and event requirements to a bounded analytics plan.
2. Identify the critical events that must be validated end to end.
3. Record data-quality risks and missing instrumentation evidence.
4. Return analytics readiness and the event-validation report.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `analytics_plan`
- `event_validation_report`
- `metrics_readiness`
- `analytics_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not claim event wiring is verified without evidence.
- Do not omit critical event gaps just to keep the release path moving.
- Do not turn ambiguous KPIs into precise numbers without support.
