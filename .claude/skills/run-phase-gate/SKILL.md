---
name: run-phase-gate
description: Produce the machine-readable phase-gate result for an idea-to-MVP phase, including status, checks, blocking findings, accepted risks, required rework, human decisions, and supporting evidence. Use when a phase is ready to pass, fail, block, or conditionally pass based on explicit artifacts.
when_to_use: Use after the phase evidence exists and before the workflow advances. Do not use to bypass missing approvals or missing evidence.
allowed-tools: Read Grep Glob
---

# Run Phase Gate

## Purpose

Produce the machine-readable phase-gate result for an idea-to-MVP phase, including status, checks, blocking findings, accepted risks, required rework, human decisions, and supporting evidence. Use when a phase is ready to pass, fail, block, or conditionally pass based on explicit artifacts.

## Entry Conditions

- Use after the phase evidence exists and before the workflow advances. Do not use to bypass missing approvals or missing evidence.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Gather the authoritative evidence for the phase and its required checks.
2. Evaluate each check and classify the overall status as `pass`, `conditional_pass`, `fail`, or `blocked`.
3. Record blocking findings, accepted risks, required rework, human decisions, and evidence paths.
4. Return the gate result in a machine-readable structure.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `phase_gate_result`
- `blocking_findings`
- `accepted_risks`
- `required_rework`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not emit `pass` when blocking evidence is missing.
- Do not hide accepted risks or required rework inside narrative prose.
- Do not merge phase status with product-owner approval status when they are separate decisions.
