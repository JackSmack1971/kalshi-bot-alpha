# Idea-to-MVP Common Skill Sections

This file holds the boilerplate body sections shared word-for-word across the
idea-to-MVP lifecycle skills under `.claude/skills/**`. Each lifecycle
`SKILL.md` keeps its own `## Header` line and points here instead of
repeating the identical bullet text, to reduce per-skill loaded context.
Skill-specific sections (`Purpose`, `Entry Conditions`, `Procedure`,
`Permitted Tools`, `Output Artifact Contract`, `Explicit Non-Goals`) are not
covered here and remain in each skill's own file.

## Required Inputs

- Active workflow state, node context, or specialist handoff for this task.
- Authoritative upstream artifacts referenced by the workflow or handoff.
- Explicit constraints, assumptions, and approvals that bound this node.

## Required Evidence

- The inputs and upstream artifacts actually consulted for this node.
- Any validation command, check output, or status cited in the result.
- Outstanding risks, gaps, or assumptions that affect downstream work.

## Validation Checks

- The result stays inside the declared phase and bounded node scope.
- Required artifact fields are present and internally consistent.
- Claims about evidence, approvals, tests, deployment, or market truth map to explicit inputs.

## Failure Conditions

- Required inputs, upstream artifacts, or approvals are missing or contradictory.
- Completing the task would require expanding scope beyond the approved MVP boundary.
- Available evidence is insufficient to support a required conclusion or recommendation.

## Handoff Destination

- Return the artifact and status to the invoking workflow node or the downstream specialist named in the active handoff.
