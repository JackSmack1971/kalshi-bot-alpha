---
name: prepare-minimal-implementation-record
description: Produce a thin implementation record for the approved MVP slice, including the smallest deliverable set, owners, dependencies, and integration notes. Use after architecture is defined for the first vertical slice.
when_to_use: Use for thin-slice planning only. Do not convert it into a full backlog or speculative roadmap.
allowed-tools: Read Grep Glob
---

# Prepare Minimal Implementation Record

## Purpose

Produce a thin implementation record for the approved MVP slice, including the smallest deliverable set, owners, dependencies, and integration notes. Use after architecture is defined for the first vertical slice.

## Entry Conditions

- Use for thin-slice planning only. Do not convert it into a full backlog or speculative roadmap.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. List the smallest implementation deliverables required for the slice.
2. Note ownership and dependency order.
3. Record integration points and failure boundaries.
4. Flag anything that still blocks implementation readiness.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `implementation_record`
- `deliverable_order`
- `integration_notes`
- `implementation_blockers`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not expand the slice into a full implementation backlog.
- Do not invent code-level details without an architectural basis.
- Do not omit integration dependencies.
