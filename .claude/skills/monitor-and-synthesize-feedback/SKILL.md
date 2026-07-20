---
name: monitor-and-synthesize-feedback
description: Synthesize telemetry and user feedback into a normalized post-launch review tied to the MVP hypothesis. Use after release when signals need to be interpreted instead of listed raw.
when_to_use: Use only after launch evidence exists. Do not use to make roadmap commitments without explicit signal interpretation.
allowed-tools: Read Grep Glob
---

# Monitor And Synthesize Feedback

## Purpose

Synthesize telemetry and user feedback into a normalized post-launch review tied to the MVP hypothesis. Use after release when signals need to be interpreted instead of listed raw.

## Entry Conditions

- Use only after launch evidence exists. Do not use to make roadmap commitments without explicit signal interpretation.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Normalize telemetry, defects, and user feedback into comparable signals.
2. Tie observed signals back to the MVP hypothesis and key risks.
3. Record what is working, what is failing, and what remains uncertain.
4. Return a post-launch review with evidence-backed signal synthesis.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `post_launch_review`
- `signal_summary`
- `hypothesis_assessment`
- `data_quality_risks`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not confuse anecdote with validated pattern.
- Do not collapse telemetry, defects, and qualitative feedback into one vague summary.
- Do not hide data-quality uncertainty.
