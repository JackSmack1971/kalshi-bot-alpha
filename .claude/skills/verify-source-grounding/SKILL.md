---
name: verify-source-grounding
description: Verify that research-facing idea-to-MVP artifacts distinguish fact, inference, estimate, and assumption, and that volatile claims stay tied to explicit dated sources. Use when discovery, market, feedback, or decision artifacts rely on external evidence that must hold up at a gate.
when_to_use: Use after a research or evidence-heavy draft exists and before a gate, approval, or downstream decision treats it as authoritative. Do not use as a substitute for doing the research itself.
allowed-tools: Read Grep Glob
---

# Verify Source Grounding

## Purpose

Verify that research-facing idea-to-MVP artifacts distinguish fact, inference, estimate, and assumption, and that volatile claims stay tied to explicit dated sources. Use when discovery, market, feedback, or decision artifacts rely on external evidence that must hold up at a gate.

## Entry Conditions

- Use after a research or evidence-heavy draft exists and before a gate, approval, or downstream decision treats it as authoritative. Do not use as a substitute for doing the research itself.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Identify the claims in scope and the evidence each claim relies on.
2. Separate verified facts from inferences, estimates, assumptions, and recommendations.
3. Flag missing source dates, retrieval dates, weak citations, or unsupported market truth.
4. Return a bounded grounding review with concrete fixes instead of broad prose.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `grounding_assessment`
- `verified_claims`
- `unsupported_claims`
- `required_citation_fixes`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not treat competitor marketing copy as independent validation.
- Do not convert assumptions into facts because they appear in multiple drafts.
- Do not hide unsupported or undated claims behind summary language.
