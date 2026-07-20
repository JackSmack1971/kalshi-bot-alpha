---
name: ideate-features
description: Convert an approved core problem into a bounded feature-candidate backlog that traces to user jobs and known risks. Use at the start of define before prioritization or UX flows.
when_to_use: Use only after discovery approval. Do not use to approve MVP scope, architecture, or release behavior.
allowed-tools: Read Grep Glob
---

# Ideate Features

## Purpose

Convert an approved core problem into a bounded feature-candidate backlog that traces to user jobs and known risks. Use at the start of define before prioritization or UX flows.

## Entry Conditions

- Use only after discovery approval. Do not use to approve MVP scope, architecture, or release behavior.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Convert the approved problem and user jobs into candidate capabilities.
2. Include risk-reduction or evidence-gathering features only when explicitly justified.
3. Keep the backlog bounded and distinct.
4. Call out the weakest candidate that should likely be excluded later.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `feature_candidate_backlog`
- `feature_candidates`
- `scope_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not add features that do not trace to the approved problem.
- Do not smuggle implementation details into feature ideation.
- Do not imply that every candidate belongs in the MVP.
