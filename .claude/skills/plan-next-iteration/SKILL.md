---
name: plan-next-iteration
description: Turn post-launch review evidence into the next iteration decision and plan. Use after telemetry and feedback have been synthesized.
when_to_use: Use only after post-launch evidence exists. Do not use to restate launch findings without making a decision.
allowed-tools: Read Grep Glob
---

# Plan Next Iteration

## Purpose

Turn post-launch review evidence into the next iteration decision and plan. Use after telemetry and feedback have been synthesized.

## Entry Conditions

- Use only after post-launch evidence exists. Do not use to restate launch findings without making a decision.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Summarize the evidence that matters for the next iteration decision.
2. Choose and justify one decision outcome: continue, change, expand, or stop.
3. List the smallest concrete next steps and open approvals.
4. Return the next-iteration plan and prioritized follow-ups.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `next_iteration_plan`
- `decision`
- `prioritized_follow_ups`
- `required_approval`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not choose continue, change, expand, or stop without citing evidence.
- Do not smuggle large scope expansion into a vague follow-up list.
- Do not leave the decision outcome implicit.
