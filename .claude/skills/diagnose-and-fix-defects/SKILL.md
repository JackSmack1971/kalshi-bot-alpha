---
name: diagnose-and-fix-defects
description: Produce bounded defect-resolution evidence, including root cause, corrective action, regression coverage, and any remaining open defects.
when_to_use: Use when test or review findings require a defect-resolution loop. Do not use to silently waive defects.
allowed-tools: Read Grep Glob
---

# Diagnose And Fix Defects

## Purpose

Produce bounded defect-resolution evidence, including root cause, corrective action, regression coverage, and any remaining open defects.

## Entry Conditions

- Use when test or review findings require a defect-resolution loop. Do not use to silently waive defects.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Record the defect set and owning area.
2. Summarize root cause and corrective action.
3. Record regression coverage and remaining open defects.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `defect_resolution_log`
- `root_cause_summary`
- `regression_coverage`
- `open_defects`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not close a defect because one rerun passed.
- Do not omit root cause or regression coverage.
- Do not hide remaining open defects.
