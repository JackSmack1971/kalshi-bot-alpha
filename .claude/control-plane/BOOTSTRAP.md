# Bootstrap Procedure

## Phase 0 — Trust substrate

Review and validate together:

- `manifest.yaml`
- `TRUST_MODEL.md`
- schemas under `schemas/`
- scripts under `scripts/`
- `control-plane-verifier.md`

Do not enable self-extension before Phase 0 passes.

## Phase 1 — Read-only inventory

### Skills inventory prompt

> Invoke `skills-specialist` in read-only analysis mode. Inventory every project
> skill, map description overlap, identify unresolved references, measure description
> and body tokens, and propose the smallest evaluation-backed consolidation plan. Do
> not edit files.

### Rules inventory prompt

> Invoke `rules-specialist` in read-only analysis mode. Inventory all applicable
> `AGENTS.md` and `.claude/rules` instructions, including nested and imported
> sources.
> Produce an activation map, contradiction report, duplicate report, and startup
> context estimate. Do not edit files.

### Workflow inventory prompt

> Invoke `workflow-specialist` in read-only analysis mode. Inventory all agents,
> hooks, settings, teams, forked skills, and workflow state. Identify unsupported
> references, permission risks, recursion paths, missing termination conditions,
> malformed-payload behavior, and observability gaps. Do not edit files.

## Phase 2 — Migration planning

> Using the three inventories, produce one ordered migration plan. Assign exactly one
> owner to each artifact, define transaction boundaries, list deterministic validators,
> define behavioral regression cases, and identify every required human approval
> point. Do not apply the migration.

## Phase 3 — Normalize one domain at a time

Recommended sequence:

1. Rules and instruction hierarchy.
2. Skill descriptions and behavioral cases.
3. Workflows, hooks, and orchestration.
4. Agent definitions and permissions.

Verify and close each transaction before opening the next.

## Phase 4 — Routing evaluation

Run the cases in `evals/routing-cases.yaml` in fresh sessions. Record:

- correct specialist selection;
- inappropriate delegation;
- expected abstention;
- false-positive skill invocation;
- cross-domain collision rate.

## Phase 5 — Controlled self-extension

A specialist may propose a new control-plane artifact only after:

- the trust substrate validates;
- routing cases pass;
- ownership remains non-overlapping;
- a separate verifier approves the transaction;
- rollback evidence exists.
