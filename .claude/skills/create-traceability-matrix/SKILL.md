---
name: create-traceability-matrix
description: Build a bounded idea-to-MVP traceability matrix from problem evidence through requirements, design, implementation, tests, and analytics signals. Use when a workflow node needs explicit coverage proof instead of assuming downstream artifacts still align.
when_to_use: Use when enough upstream artifacts exist to map one delivery chain end to end, or when change impact, audit, testing, or release readiness depends on explicit traceability. Do not use to invent missing artifacts.
allowed-tools: Read Grep Glob
---

# Create Traceability Matrix

## Purpose

Build a bounded idea-to-MVP traceability matrix from problem evidence through requirements, design, implementation, tests, and analytics signals. Use when a workflow node needs explicit coverage proof instead of assuming downstream artifacts still align.

## Entry Conditions

- Use when enough upstream artifacts exist to map one delivery chain end to end, or when change impact, audit, testing, or release readiness depends on explicit traceability. Do not use to invent missing artifacts.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Start from the authoritative problem, JTBD, or requirement inputs in scope.
2. Map each item to downstream design surfaces, implementation outputs, tests, and analytics signals that actually exist.
3. Mark gaps, broken links, and one-to-many dependencies explicitly.
4. Return the portable traceability matrix and the smallest uncovered set that still blocks confidence.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `traceability_matrix`
- `coverage_gaps`
- `broken_links`
- `downstream_dependencies`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not fabricate downstream coverage for requirements that have no artifact support.
- Do not collapse missing links into a generic “to be confirmed” bucket.
- Do not treat file existence alone as traceability proof.
