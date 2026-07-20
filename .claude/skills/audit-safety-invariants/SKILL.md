---
name: audit-safety-invariants
description: Use for a standalone cross-cutting audit of CLAUDE.md's universal safety invariants (demo-only transport, credential/process isolation, AI/deterministic authority boundary, human approval) whenever a change touches Kalshi transport or endpoints, credentials or secrets, agent/OpenRouter code, or authority-sensitive areas mapped by kalshi-transport-safety.md, credential-privacy.md, agents/openrouter-governance.md, governance-and-approvals.md, or architecture/dependency-boundaries.md. Trigger on requests to audit safety, check invariants, review authority boundaries, or before verify-change declares such a diff complete. Runs in addition to, not instead of, verify-change's test/lint/static-analysis suite. NOT for checking whether a phase's deliverables/exit criteria are met (use phase-exit-audit) and NOT for evolving a frozen schema contract (use propose-contract-change).
---

# Audit safety invariants

Perform this workflow whenever a diff or area of work maps to a safety-invariant rule file, or before completion is declared for such a diff:

1. Identify the diff scope: `git status`/`git diff` and the list of changed or newly added files.
2. Map changed files against the four safety-invariant rule files by their declared `paths` patterns: `.claude/rules/kalshi-transport-safety.md`, `.claude/rules/credential-privacy.md`, `.claude/rules/agents/openrouter-governance.md` plus `.claude/rules/governance-and-approvals.md`, and `.claude/rules/architecture/dependency-boundaries.md`. Treat a category as in-scope if any changed file, new schema field, or new config matches its pattern or purpose.
3. **Demo-only transport** (in scope for transport/client/config code, endpoint constants, or fixtures):
   - Run `python scripts/verify_demo_only.py` and record its exit code and output verbatim.
   - Independently inspect changed files for any Kalshi hostname; confirm only `external-api.demo.kalshi.co` and `external-api-ws.demo.kalshi.co` appear anywhere reachable.
   - Confirm no `environment=production` parameter, dormant production constant, generic `KalshiClient(environment)`-style abstraction, or config path that could select a non-demo host was introduced.
   - Confirm mutating-call safety per `kalshi-transport-safety.md`: unique `client_order_id` values, no blind retry of a mutating request, and an uncertain outcome routed to `OUTCOME_UNKNOWN` with suspension and reconciliation rather than assumed success or failure.
4. **Credential and process isolation** (in scope for auth/credentials/secrets/logging/telemetry/config/openrouter/agents code, `.env*`, or any `*config*` file):
   - Confirm trading-process code never requires `OPENROUTER_API_KEY` and agent-process code never receives Kalshi credentials, authentication material, or execution capability.
   - Grep changed files, fixtures, snapshots, logs, prompts, dashboards, telemetry, and AI evidence bundles for secret material; confirm test fixtures use synthetic markers, not realistic-looking secrets.
   - Confirm redaction coverage for access-key IDs, signatures, auth headers, private-key material, and serialized request payloads through logging, exceptions, retries, and nested structures where changed.
5. **AI / deterministic authority boundary** (in scope for `agents/`, `openrouter/`, `agent_tools/`, `evidence/`, `proposals/`, or any code adjacent to execution, risk, reconciliation, ledger, or configuration activation):
   - Confirm no AI/agent code path can call a Kalshi trading transport, create or cancel an order, approve or bypass risk, resolve reconciliation, mutate ledger or authoritative state, activate configuration, or modify an allowlist.
   - Confirm model output cannot deserialize into `TradeIntent`, an approved order plan, a risk approval, a reconciliation resolution, a ledger event, or an active configuration object; confirm distinct proposal schemas/namespaces/storage/validation paths are used instead.
   - Confirm the forbidden-reachability list in `architecture/dependency-boundaries.md` still holds (trading-runtime packages do not depend on agent packages; `strategies` does not import Kalshi clients or execution; `risk` does not call exchange transports; agent packages do not import execution transports, ledger mutation APIs, active-configuration writers, secret loaders, or unrestricted database sessions).
6. **Human approval** (in scope whenever approval, promotion, or configuration-activation code or docs changed):
   - Confirm nothing in the diff simulates, infers, fabricates, backfills, or self-grants human approval.
   - Confirm an approval record, if introduced, cannot by itself mutate active runtime state — a normal reviewed engineering/deployment path is still required.
7. For any category judged out of scope for this diff, mark it "not applicable" in the report with a one-line reason; do not silently omit a category.
8. Cite concrete evidence (file path, line, command output) for every pass or fail — do not assert a status without evidence.

Do not run this skill's checks as a substitute for `verify-change`'s test/lint/static-analysis suite; run both when a diff qualifies for both. Do not edit code, weaken a check, or reinterpret a failing invariant as a warning to obtain a pass. Do not mark a category "not applicable" merely because checking it is inconvenient.

Final audit report:

```text
Safety invariant audit — <diff or area under audit>

Demo-only transport
- Status: pass | fail | not applicable
- Evidence: command(s) run, output, files inspected.

Credential and process isolation
- Status: pass | fail | not applicable
- Evidence: files inspected, redaction checks performed.

AI / deterministic authority boundary
- Status: pass | fail | not applicable
- Evidence: imports/paths inspected, schema/deserialization checks performed.

Human approval
- Status: pass | fail | not applicable
- Evidence: approval-path code/docs inspected.

Overall result: pass | blocked
Blocking findings (if any):
- Invariant, file:line, and why it fails.
```

A failed check blocks completion. It cannot be waived, downgraded, or deferred to obtain an overall "pass" — report it as blocking and stop.
