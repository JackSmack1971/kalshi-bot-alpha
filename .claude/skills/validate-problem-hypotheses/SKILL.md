---
name: validate-problem-hypotheses
description: Test candidate problems for affected users, severity, frequency, evidence strength, and falsifiers. Use during discovery after opportunities exist and before selecting a core problem.
when_to_use: Use in discovery validation only. Do not use to approve final scope or architecture.
allowed-tools: Read Grep Glob
---

# Validate Problem Hypotheses

## Purpose

Test candidate problems for affected users, severity, frequency, evidence strength, and falsifiers. Use during discovery after opportunities exist and before selecting a core problem.

## Entry Conditions

- Use in discovery validation only. Do not use to approve final scope or architecture.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Evaluate each candidate problem for user, frequency, severity, and alternatives.
2. Separate verified facts, inferences, assumptions, and unknowns.
3. State a falsifier for each problem hypothesis.
4. Mark whether the problem is evidence-backed or experiment-backed.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `problem_validation`
- `evidence_gaps`
- `falsifiers`
- `recommended_candidates`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not treat assumptions as evidence.
- Do not hide missing evidence.
- Do not select the final problem in this skill.
