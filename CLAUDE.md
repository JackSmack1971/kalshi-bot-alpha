# CLAUDE.md

You are working on **Kalshi Crypto Paper-Trading Bot v3**: a deterministic, demo-only Kalshi paper-trading system with a separate OpenRouter-exclusive AI research and control plane. It must remain auditable, fail-closed, and structurally incapable of accidental production trading.

This file is the repository’s constitutional layer. The Version 3 blueprint governs product and architecture contracts. Path-scoped rules govern subsystem details. Skills govern multi-step work procedures.

## Governing authority split

```text
AI may observe, investigate, challenge, explain, and propose.

Deterministic code must calculate, authorize, execute, reconcile, and account.

Humans must approve strategy, risk, market eligibility, reconciliation,
active configuration, and promotion changes.
```

Preserve this split in every design, implementation, test, migration, tool, and report.

Priority order:

1. Safety
2. Determinism
3. Auditability
4. Correctness
5. Traceability
6. Maintainability
7. Delivery speed

Choose safety over speed, auditability over convenience, deterministic control over AI flexibility, explicit failure over silent degradation, and the smallest proven change over speculative abstraction.

## Source precedence

When sources disagree, apply this order:

1. Explicit current user instruction
2. Demo-only, credential, authority, accounting, and fail-closed invariants
3. Accepted architecture decisions, frozen schemas, and reviewed contracts
4. Active implementation phase and exit criteria
5. `Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md`
6. Current repository structure, tests, and established conventions
7. Recommendations, examples, and illustrative defaults

A lower-precedence source must never weaken a higher-precedence safety invariant. Do not silently reconcile authoritative conflicts. Preserve the safer behavior, identify the conflict and affected invariant, and require an architecture decision before implementing disputed behavior.

## Blueprint routing

Before changing a subsystem, read the relevant blueprint sections:

- Demo-only and credential isolation: §2
- Runtime and AI authority boundaries: §2.3 and §4.1
- Components and data ownership: §5
- Runtime sequencing: §6
- Failure handling: §7
- Testing: §10
- Repository layout: §11
- Delivery phases: §12
- Evaluation protocol: §13
- Definition of done: §14
- Market microstructure: §15
- OpenRouter policy: §16

The blueprint is authoritative for system contracts. This file is authoritative for Claude Code’s repository-wide behavior.

## Active-phase discipline

Read `docs/IMPLEMENTATION_STATUS.md` before planning or editing. Implement only the active phase unless the user explicitly authorizes broader scope. Do not opportunistically build later phases. Preserve future interfaces without implementing future behavior early.

A stub, TODO, mock-only path, skipped test, or interface declaration does not satisfy an exit criterion. Do not claim a phase complete without objective, reviewable evidence for every criterion.

When phase status is absent or unresolved, work conservatively and report the ambiguity. Do not create or alter project documentation unless the task permits it.

## Universal safety invariants

### Demo only

Only these Kalshi endpoints are permitted:

```text
REST:      https://external-api.demo.kalshi.co/trade-api/v2
WebSocket: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2
```

Reject every non-demo hostname. Do not add a production switch, dormant production endpoint, generic production-capable client, or configuration path that could activate live trading. Production enablement requires a separate project, architecture, security review, and explicit human approval. Keep operator-visible `DEMO MODE` status explicit.

### Credentials and process isolation

The trading process may receive Kalshi demo credentials but must never require `OPENROUTER_API_KEY`. The agent process may receive `OPENROUTER_API_KEY` but must never receive Kalshi credentials, authentication material, or execution capabilities.

Never place secrets in source control, prompts, logs, fixtures, snapshots, dashboards, telemetry, frontend processes, or AI evidence bundles.

### Deterministic authority

AI must never call Kalshi trading transports; create or cancel orders; approve or bypass risk; resolve reconciliation; mutate ledger or authoritative state; activate configuration; modify allowlists; or emit data accepted as an authoritative trading type.

Model output must use distinct proposal schemas, namespaces, storage, and validation paths. It must never deserialize into `TradeIntent`, an approved order plan, risk approval, reconciliation resolution, ledger event, or active configuration object.

Risk authorization must remain synchronous, centralized, deterministic, versioned, and non-bypassable. Strategy evaluation must not begin before reconciliation, market eligibility, data health, and stream health are deterministically confirmed.

### OpenRouter only

OpenRouter is the only external LLM inference provider. Do not add direct vendor SDKs or clients. AI output is always non-authoritative and outside the execution-critical path.

### Human approval

Claude Code must never simulate, infer, fabricate, or self-grant human approval. Approval never directly mutates active runtime state; normal reviewed engineering and deployment paths remain required.

## Repository conventions

Treat `pyproject.toml`, lockfiles, existing source, configuration, migrations, tests, and CI as the source of truth for the active stack and commands. Preserve blueprint-approved libraries and patterns. Do not introduce a competing framework, infrastructure library, configuration system, ORM, transport client, validation system, logging framework, or migration mechanism without an accepted architecture decision.

Keep modules small, typed, explicit, and composable. Keep side effects at narrow boundaries. Do not use convenience abstractions that erase strategy, risk, execution, reconciliation, accounting, credential, or AI-authority boundaries.

## Rule routing

Detailed subsystem constraints are in `.claude/rules/` and load conditionally by path:

- `kalshi-transport-safety.md` — demo endpoints, transport construction, mutation uncertainty
- `credential-privacy.md` — secrets, redaction, logging, telemetry, process-key isolation
- `architecture/dependency-boundaries.md` — package ownership, imports, authority reachability
- `runtime-lifecycle.md` — startup, shutdown, suspension, fail-closed recovery
- `market-data-and-eligibility.md` — allowlists, lifecycle checks, order-book health
- `accounting-and-domain-models.md` — fixed-point values, provenance, ledger, reconciliation
- `strategy-and-risk.md` — strategy limits, expectancy, deterministic risk controls
- `research-evaluation-integrity.md` — microstructure research and evaluation states
- `agents/openrouter-governance.md` — gateway, tools, evidence, routing, output validation
- `governance-and-approvals.md` — approvals, proposals, promotion, configuration activation
- `persistence-and-migrations.md` — schema changes, append-only history, migrations
- `security-adversarial-review.md` — threat review for sensitive surfaces

Multi-step procedures are in `.claude/skills/`:

- `safe-change-preflight`
- `implement-safe-change`
- `verify-change`

Use these skills for nontrivial repository modifications rather than duplicating their procedures here.

## Completion bar

A change is complete only when it preserves demo isolation, deterministic trading authority, AI and credential boundaries, reconciliation and accounting invariants, provenance, auditability, and active-phase scope; includes relevant failure-mode tests; and passes the required verification.

Never claim completion when required verification failed or was not run. Distinguish precisely between implemented, tested, mocked, simulated, partially implemented, unverified, and deferred behavior.
