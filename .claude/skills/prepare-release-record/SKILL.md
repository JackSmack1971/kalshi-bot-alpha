---
name: prepare-release-record
description: Produce a release record for the thin MVP slice, summarizing scope delivered, evidence gathered, residual risks, rollback posture, and the final release recommendation. Use at the end of the first vertical slice.
when_to_use: Use only after test evidence is summarized. Do not use to approve release without explicit evidence.
allowed-tools: Read Grep Glob
---

# Prepare Release Record

## Purpose

Produce a release record for the thin MVP slice, summarizing scope delivered, evidence gathered, residual risks, rollback posture, and the final release recommendation. Use at the end of the first vertical slice.

## Entry Conditions

- Use only after test evidence is summarized. Do not use to approve release without explicit evidence.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Summarize the approved slice and delivered artifacts.
2. Record verification evidence, blockers, and residual risks.
3. State rollback posture and any missing operational evidence.
4. Return a release recommendation with required follow-up actions.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `release_record`
- `residual_risks`
- `rollback_posture`
- `release_recommendation`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not state that the slice is releasable without explicit evidence.
- Do not hide residual risks.
- Do not confuse planned work with delivered work.
