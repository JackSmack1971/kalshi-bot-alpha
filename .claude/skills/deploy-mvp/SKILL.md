---
name: deploy-mvp
description: Produce deployment evidence for the MVP candidate, including rollout posture, rollback readiness, operational ownership, and health-check expectations. Use during the launch phase before product release.
when_to_use: Use only after release-candidate evidence exists. Do not use to authorize user exposure on its own.
allowed-tools: Read Write Edit Bash Grep Glob
---

# Deploy MVP

## Purpose

Produce deployment evidence for the MVP candidate, including rollout posture, rollback readiness, operational ownership, and health-check expectations. Use during the launch phase before product release.

## Entry Conditions

- Use only after release-candidate evidence exists. Do not use to authorize user exposure on its own.
- Required upstream artifacts, approvals, and workflow context for this node are available.

## Required Inputs

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-inputs) — no skill-specific additions.

## Procedure

1. Inspect the active handoff, especially the owned paths, authoritative inputs, and validation command.
2. Make only the minimum tooling or deployment-readiness changes needed inside the delegated paths.
3. Run the delegated validation command or the smallest equivalent deployment-readiness verification command when changes occurred.
4. Record rollout posture, rollback evidence, and health-check expectations.
5. State who owns operations and what remains unproven.
6. Return a deployment recommendation with blockers if evidence is incomplete.

## Permitted Tools

- `Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`

## Required Evidence

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#required-evidence) — no skill-specific additions.

## Output Artifact Contract

Return:

- `deployment_record`
- `rollback_evidence`
- `operational_owner`
- `health_check_summary`
- `deployment_recommendation`

## Validation Checks

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#validation-checks) — no skill-specific additions.

## Failure Conditions

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#failure-conditions) — no skill-specific additions.

## Handoff Destination

See [Idea-to-MVP Common Skill Sections](../_shared/idea-to-mvp-common-sections.md#handoff-destination) — no skill-specific additions.

## Explicit Non-Goals

- Do not confuse deployment with release.
- Do not claim rollback is ready without explicit evidence or a bounded gap statement.
- Do not hide missing operational ownership.
