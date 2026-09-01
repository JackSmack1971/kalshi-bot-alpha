---
name: propose-contract-change
description: Propose reviewable changes to frozen JSON Schemas or governing contracts, including field additions, renames, types, and versions. Never activates config, marks phases complete, or fabricates approval. Not for approved-schema implementation, wording-only edits, or sensitive diff audits.
---

# Propose a contract change

1. Identify the exact schema(s) targeted and read them fully, together with the governing doc section(s) that describe the same contract (per `docs/DATA_MODEL.md`, `docs/RISK_MODEL.md`, `docs/MICROSTRUCTURE_CONTRACT.md`, `docs/STRATEGY_SPEC.md`, `docs/RESEARCH_PROTOCOL.md` as applicable).
2. Enumerate every downstream consumer before touching anything: other schemas that reference or duplicate the same fields, doc sections describing the same contract, example configs (e.g. `config/risk/*.yaml`), tests that validate the schema or construct sample payloads, and any implementation code that already constructs or consumes the contract.
3. Classify the requested change:
   - **Additive/backward-compatible**: a new optional field, a widened enum, a new example, a clarification that does not change accepted-payload semantics.
   - **Breaking**: a removed or renamed required field, a retyped field, a tightened validation rule, or any redefinition of an existing field's meaning.
4. For a breaking change to a frozen contract, require an explicit versioning mechanism already established in this repository (for example an `edge_model_version`-style field) rather than silently mutating the schema in place. If no such versioning mechanism exists for the field in question, stop and record that gap in the report instead of inventing an ad hoc one.
5. Apply AGENTS.md source precedence explicitly before drafting: check whether the requested change conflicts with a higher-precedence source — the demo-only, credential, authority, accounting, or fail-closed invariants; an accepted architecture decision; or an already-frozen schema guarantee. If a conflict exists, stop before editing. Do not silently reconcile it. Record the conflict, the affected invariant or ADR, and note that this repository has no dedicated ADR-drafting skill yet under `.agents/skills/`; recommend that a human author or update an ADR rather than fabricating one or proceeding around the conflict.
6. If no conflict blocks the change, draft it across every dependent artifact identified in step 2 together in one coherent change set: the schema file, the governing doc section(s), example configs, and test fixtures/cases. Do not update the schema alone and leave docs, examples, or tests inconsistent with it.
7. Add or update tests that exercise both a still-valid old-shape payload (for additive changes) and a new-shape payload, and, for breaking changes, a test proving the old payload now fails validation or requires the new version field.
8. Do not activate any configuration, do not mark any phase or exit criterion in `docs/IMPLEMENTATION_STATUS.md` complete, and do not record or imply human approval. This procedure always ends in "awaiting human approval," consistent with `.codex/policies/governance-and-approvals.md`.
9. Report the full change set, the classification, any conflicts surfaced, and the outstanding approval requirement.

Do not edit files outside `schemas/`, the explicitly named governing docs, their example configs, and their tests. Do not fabricate an ADR, an approval record, or a versioning convention that does not already exist in the repository. Do not silently mutate a frozen schema's accepted-payload semantics without a versioning path.

Final contract-change proposal report:

```text
Contract change proposal

What changed
- Schema(s)/doc(s) touched and the field-level diff.

Why
- Requirement driving the change.

Classification
- Additive/backward-compatible or breaking, and the versioning mechanism used (if breaking) or the versioning gap recorded (if none exists).

Dependents updated
- Schemas, docs, example configs, and tests updated together; list each file and why.

Conflicts surfaced
- Any higher-precedence source in tension with this change and the affected invariant/ADR, or "none found."
- ADR hand-off: no ADR-drafting skill exists yet in this repository; recommend a human author/update an ADR before this proposal proceeds, if a conflict was surfaced.

Approval required
- This proposal activates nothing and satisfies no exit criterion by itself. Durable human review and approval, per governance-and-approvals, are required before any schema or configuration derived from it is treated as active.
```


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `change_classified`, `dependent_count`, `authority_conflict`, `versioning_gap`, `proposal_result`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
