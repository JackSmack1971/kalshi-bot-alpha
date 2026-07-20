<!--
Fill in every section from the actual diff. Do not include credentials, tokens,
API keys, internal hostnames, or any other secret material in this description —
see .claude/rules/credential-privacy.md.

Section order mirrors the "Final implementation report" produced by
.claude/skills/implement-safe-change/SKILL.md, so a completed change can be
pasted in with little rewriting.
-->

## Summary

- What changed and why.

## Type of change

- [ ] Contract/schema change (`schemas/**` or its governing docs) — link the `propose-contract-change` proposal this implements
- [ ] Safety-invariant-adjacent (transport, credentials, agent/OpenRouter code, authority boundaries) — link the `audit-safety-invariants` report
- [ ] Phase deliverable or exit-criterion work — link the `phase-exit-audit` report if this claims a phase advance
- [ ] Documentation, tooling, or process only — no runtime behavior change

## Safety and architecture impact

- Invariants preserved (demo-only, credential/process isolation, deterministic authority, human approval):
- Authority boundaries affected, if any:
- Approved contract or schema changes, if any:

## Files changed

- Exact paths and purpose.

## Verification

- Commands run and pass/fail results:
- Tests not run, and why:

## Remaining risks

- Limitations, unresolved evidence, or deferred work:

## Phase status

- Active phase (per `docs/IMPLEMENTATION_STATUS.md`):
- Exit criteria this advances, satisfies, or leaves incomplete:

## Reviewer checklist

- [ ] No non-demo Kalshi hostname, production switch, or dormant production path introduced
- [ ] No secret in source, logs, fixtures, telemetry, prompts, or AI evidence
- [ ] No new AI-reachable path to orders, risk approval, reconciliation, ledger mutation, allowlists, or configuration activation
- [ ] No later-phase behavior implemented opportunistically ahead of the active phase
- [ ] Required verification actually ran and passed — not skipped, mocked, or simulated
- [ ] No human approval simulated, inferred, fabricated, or self-granted by this change or its description
