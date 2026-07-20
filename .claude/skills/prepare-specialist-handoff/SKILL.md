---
name: prepare-specialist-handoff
description: Package a bounded specialist handoff for the idea-to-MVP workflow with objective, authoritative inputs, relevant decisions, constraints, required output, acceptance checks, explicit exclusions, unresolved questions, allowed paths, and tool permissions. Use when the orchestrator needs to delegate work without leaking full-session context.
when_to_use: Use before specialist execution when the workflow needs a precise delegation packet. Do not use after the specialist work is already complete.
allowed-tools: Read Grep Glob
---

# Prepare Specialist Handoff

## Purpose

Package a bounded specialist handoff for the idea-to-MVP workflow with objective, authoritative inputs, relevant decisions, constraints, required output, acceptance checks, explicit exclusions, unresolved questions, allowed paths, and tool permissions. Use when the orchestrator needs to delegate work without leaking full-session context.

## Entry Conditions

- Use before specialist execution when the workflow needs a precise delegation packet. Do not use after the specialist work is already complete.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. State the objective, required output, and authoritative inputs.
2. Include relevant decisions, constraints, acceptance checks, and allowed paths.
3. List explicit exclusions, tool permissions, and unresolved questions.
4. Return a handoff packet that a specialist can execute without inheriting the full conversation.

## Permitted Tools

- `Read`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `specialist_handoff`
- `authoritative_inputs`
- `acceptance_checks`
- `unresolved_questions`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not send non-authoritative inputs as if they were approved facts.
- Do not omit explicit exclusions or allowed-path boundaries.
- Do not hide unresolved questions that could change the output.
