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

Create the 20 surface × lens review tasks. Run them through `security-adversarial-reviewer` in **bounded batches of at most four concurrent subagents**. Wait for and finish each batch before launching the next. A reviewer may report zero findings; never manufacture one.

Each raw finding must include title, file/location, severity (`low|medium|high|critical`), description, surface, lens, and owner.

## Independent refutation

For every raw finding, launch a fresh `security-adversarial-reviewer` context whose job is to reproduce/substantiate or refute that finding. Process in bounded batches of at most four. Treat an unsubstantiated finding as refuted/unverified, not confirmed. Preserve raw and refutation evidence.

## Optional fix

Do **not** modify code unless the user's current request explicitly authorizes remediation/auto-fix. If not authorized, stop after reporting confirmed findings.

When authorized, route confirmed findings to their owning domain engineer. Apply fixes sequentially when findings could overlap a file or invariant; parallel writes are prohibited. Every fix must follow `implement-safe-change`, add a regression test where feasible, and follow `memory-domain-sync`.

## Reverify

If any fixes were made, run `verify-change` over the resulting diff and re-run the relevant threat lens on each fixed finding. Report exact evidence. A failed re-verification remains blocking.
