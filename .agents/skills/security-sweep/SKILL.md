---
name: security-sweep
description: Use only when the user explicitly asks for a multi-agent adversarial security sweep of sensitive repository surfaces. Reviews transport, agents/OpenRouter, governance, and persistence through five threat lenses; independently tries to refute each raw finding; optionally fixes only when the user explicitly requests remediation/auto-fix; then re-verifies. Not for routine single-diff safety checks; use audit-safety-invariants.
---

# Multi-agent security sweep

Surfaces and owning fix roles:

- transport: Kalshi endpoint/transport/client code -> `transport-safety-engineer`
- agents/OpenRouter: `src/agents`, `src/openrouter`, `src/agent_tools`, `src/evidence`, `src/proposals` -> `openrouter-agent-engineer`
- governance: `src/approvals`, `src/governance`, `src/promotion` -> `governance-approvals-engineer`
- persistence: `src/persistence`, `src/ledger`, `src/reconciliation`, migrations -> `accounting-ledger-engineer`

Threat lenses: injection; credential leakage; capability escalation; replay/idempotency; prompt injection.

## Sweep

Create the 20 surface × lens review tasks. Run them through `security-finding-reviewer` in **bounded batches of at most four concurrent subagents**. Wait for and finish each batch before launching the next. A reviewer may report zero findings; never manufacture one.

Each raw finding must include title, file/location, severity (`low|medium|high|critical`), description, surface, lens, and owner.

For each surface/lens cell, emit `surface_lens_result` with `count`, `confirmed`,
and `refuted`. Report the confirmed/refuted ratio, retries, and repeated-finding
count at the end. This measures yield but never reduces mandatory 20-cell
coverage. A failed reviewer or partial batch is blocking, not an empty result.

## Independent refutation

For every raw finding, launch a fresh `security-finding-reviewer` context whose job is to independently substantiate or refute that finding from repository evidence. Process in bounded batches of at most four. Treat an unsubstantiated finding as refuted/unverified, not confirmed. Preserve raw and refutation evidence. If a finding cannot be resolved without new executable test evidence, return that reproduction requirement to the parent; do not let the read-only reviewer widen its own authority.

When the user's requested scope permits adding security tests, the parent may route a bounded reproduction to `security-test-author`. That role may author only adversarial/security tests by behavioral contract and never repairs `src/**`. The resulting test evidence returns to a fresh `security-finding-reviewer` or the parent for adjudication; the test author never self-certifies the finding or fix.

## Optional fix

Do **not** modify code unless the user's current request explicitly authorizes remediation/auto-fix. If not authorized, stop after reporting confirmed findings.

When authorized, route confirmed findings to their owning domain engineer. Apply fixes sequentially when findings could overlap a file or invariant; parallel writes are prohibited. Every fix must follow `implement-safe-change`, add a regression test where feasible, and follow `memory-domain-sync`.

## Reverify

If any fixes were made, run `verify-change` over the resulting diff and re-run the relevant threat lens on each fixed finding. Report exact evidence. A failed re-verification remains blocking.


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `surface_lens_result`, `finding_recorded`, `finding_refuted`, `fix_authorization`, `reverification_result`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
