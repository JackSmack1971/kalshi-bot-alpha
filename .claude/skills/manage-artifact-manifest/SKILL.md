---
name: manage-artifact-manifest
description: Maintain the idea-to-MVP artifact manifest when the workflow needs artifact IDs, owners, dependency links, status transitions, downstream consumers, approval state, or supersession recorded consistently. Use when a specialist output must be registered or audited without rewriting the whole workflow state.
when_to_use: Use after an artifact is created, reviewed, approved, superseded, rejected, or found stale. Do not use to invent artifact content or approve quality on its own.
allowed-tools: Read Grep Glob
---

# Manage Artifact Manifest

## Purpose

Maintain the idea-to-MVP artifact manifest when the workflow needs artifact IDs, owners, dependency links, status transitions, downstream consumers, approval state, or supersession recorded consistently. Use when a specialist output must be registered or audited without rewriting the whole workflow state.

## Entry Conditions

- Use after an artifact is created, reviewed, approved, superseded, rejected, or found stale. Do not use to invent artifact content or approve quality on its own.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Identify the authoritative artifact, owner, status, and direct upstream inputs.
2. Record downstream consumers, approval state, validation evidence, and superseded relationships.
3. Flag missing dependency links, unresolved placeholders, or illegal status transitions.
4. Return only the bounded manifest update needed for the workflow state.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `artifact_manifest_update`
- `dependency_links`
- `status_transitions`
- `manifest_findings`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not treat file existence as artifact completion.
- Do not invent upstream dependencies, reviewers, or approvals.
- Do not mark unrelated downstream artifacts stale by default.
