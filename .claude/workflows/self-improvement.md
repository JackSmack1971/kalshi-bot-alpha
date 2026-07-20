# Recursive Control-Plane Self-Improvement Workflow

## Trigger

- **Primary hook:** `.claude/settings.json` registers a `UserPromptSubmit` command hook that runs `.claude/control-plane/scripts/self_improvement_evidence.py --hook`.
- **Selection rule:** the hook selects this workflow when the submitted prompt contains `.claude/workflows/self-improvement.md`, `self-improvement.md`, `self-improvement`, `self improvement`, `recursive improvement`, `recursive control-plane`, `improve the control plane`, or `control-plane improvement`.
- **Injected context:** the hook adds latest-run evidence and the instruction to invoke this workflow.
- **Malformed payload diagnostics:** invalid hook JSON is recorded once per distinct stdin payload hash in `.claude/control-plane/runs/malformed-payload-diagnostics.jsonl`; raw prompt or payload text is never stored.
- **Manual trigger:** a user may explicitly request this workflow by path.

## States

1. `received` — prompt matched a natural-language trigger or named this workflow by path.
2. `evidence-loaded` — latest-run evidence was produced.
3. `baseline-checked` — manifest, inventory, schemas, and workflow evals were read.
4. `candidate-planned` — a bounded change plan and explicit write set were declared.
5. `approval-gate` — required only when the candidate touches `manifest.yaml` or forbidden roots.
6. `candidate-applied` — approved changes were written by one primary writer.
7. `replay-checked` — deterministic validation and eval replay completed.
8. `verified` — independent verifier requirements were satisfied.
9. `recorded` — append-only run evidence was written under `.claude/control-plane/runs/` when a run ledger is part of the task.
10. `done` — changes are complete and summarized.
11. `failed` — validation, approval, or verification failed.
12. `rolled-back` — failed changes were reverted when required.

## Legal Transitions

- `received -> evidence-loaded -> baseline-checked -> candidate-planned`.
- `candidate-planned -> approval-gate` when manifest or forbidden-root changes are proposed.
- `candidate-planned -> candidate-applied` when no approval gate is required.
- `approval-gate -> candidate-applied` only after explicit human approval.
- `approval-gate -> failed` when approval is denied or unavailable.
- `candidate-applied -> replay-checked -> verified -> recorded -> done`.
- Any state may transition to `failed` with a diagnosis event.
- `failed -> rolled-back` when rollback is required by `manifest.yaml`.

## Inputs

- User prompt and hook payload.
- `.claude/control-plane/scripts/self_improvement_evidence.py` output.
- `.claude/control-plane/manifest.yaml` ownership, forbidden roots, budgets, and verification policy.
- Current workflow, hook, rule, skill, agent, schema, and eval files.
- Latest run artifact when evidence reports `latest-run-found`.

## Outputs

- Candidate change plan with owner, read set, write set, risk, and approval status.
- Updated control-plane files within the approved write set.
- Replay and baseline check results.
- Verification summary.
- Optional append-only run evidence under `.claude/control-plane/runs/`.
- Malformed-payload diagnostics at `.claude/control-plane/runs/malformed-payload-diagnostics.jsonl` as JSON Lines with stable keys: `error`, `event`, `hook_name`, `payload_sha256`, and `timestamp`.

## Read Set

- `AGENTS.md` and nested `.claude/**/AGENTS.md` files in scope.
- `.claude/control-plane/manifest.yaml`.
- `.claude/control-plane/scripts/**`.
- `.claude/control-plane/evals/**`.
- `.claude/workflows/**`.
- `.claude/hooks/**`.
- `.claude/settings.json`.
- `.claude/control-plane/runs/**` for evidence only.

## Write Set

- `.claude/workflows/**`.
- `.claude/hooks/**`.
- `.claude/settings.json`.
- `.claude/control-plane/scripts/**`.
- `.claude/control-plane/evals/workflow-*.yaml`.
- `.claude/control-plane/runs/**` only for append-only evidence.

## Forbidden Writes

- Do not edit forbidden roots listed in `.claude/control-plane/manifest.yaml`.
- Do not edit `.claude/control-plane/manifest.yaml` without explicit approval.
- Do not rewrite or delete existing files under `.claude/control-plane/runs/`.
- Append malformed-payload diagnostics only to `.claude/control-plane/runs/malformed-payload-diagnostics.jsonl`; never include raw stdin, prompt contents, or payload contents.

## Budgets

- Primary writer: `workflow-specialist`.
- Concurrent writers: `1`.
- Nested agent depth: `0` unless the manifest explicitly changes.
- Maximum changed files without explicit approval: `12`.
- Default turn budget: `28`.
- Retry budget: one replay retry after a deterministic failure; unchanged malformed hook payloads are identified by `payload_sha256` and must not append duplicate diagnostics or trigger retry loops.

## Approval Gates

- Manifest changes require explicit human approval before editing.
- Forbidden-root changes require explicit human approval and manifest reconciliation before editing.
- Budget increases require explicit human approval before editing.
- Approval evidence must be cited in the change plan or run ledger.

## Replay and Baseline Checks

- Run `python .claude/control-plane/scripts/self_improvement_evidence.py` before changes.
- Run `python .claude/control-plane/scripts/validate.py` after changes.
- Run `python .claude/control-plane/scripts/inventory.py` when file structure changes.
- Check `.claude/control-plane/evals/workflow-cases.yaml` contains positive and negative cases for trigger selection, approval gating, and malformed-payload diagnostics.
- Compare candidate behavior against latest-run evidence when a latest run exists.

## Latest-Run and First-Run Behavior

- If evidence state is `first-run`, treat the run as bootstrap: create baseline trigger, hook, and eval coverage without relying on prior run memory.
- If evidence state is `latest-run-found`, read the latest run artifact and preserve verified improvements unless the new replay proves they regress behavior.
- If the latest run recommends manifest changes, pause at `approval-gate` and request explicit approval before modifying `manifest.yaml`.


## Malformed Hook Payload Diagnostics

- On `json.JSONDecodeError`, `.claude/control-plane/scripts/self_improvement_evidence.py --hook` blocks deterministically and appends at most one JSONL event for the malformed stdin payload.
- Diagnostic location: `.claude/control-plane/runs/malformed-payload-diagnostics.jsonl`. This append-only file is diagnostics evidence, not a run ledger.
- Diagnostic event format uses sorted JSON keys and contains exactly this information: `event` (`malformed-hook-payload`), `timestamp` (UTC ISO-8601 seconds), `hook_name` (`UserPromptSubmit`), `error` (decoder message), and `payload_sha256` (SHA-256 of stdin).
- The event must not contain raw stdin, prompt text, or payload text.
- If the same malformed stdin payload is observed again, match it by `payload_sha256`, keep the existing diagnostic event, and do not append another event.
