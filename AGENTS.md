# AGENTS.md

You are working on **Kalshi Crypto Paper-Trading Bot v3**: a deterministic, demo-only Kalshi paper-trading system with a separate OpenRouter-exclusive AI research and control plane. It must remain auditable, fail-closed, and structurally incapable of accidental production trading.

This file is the repository’s constitutional layer. The Version 3 blueprint governs product and architecture contracts. Repository policies govern subsystem details. Skills govern multi-step work procedures. Codex subagents provide bounded specialist contexts.

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

## Behavioral authority and task specificity

Do not collapse behavioral-policy authority and task specificity into one linear precedence list. Resolve them in this order:

1. **Constitutional repository constraints** — demo-only operation, credential/process isolation, deterministic authority, accounting integrity, human-approval integrity, and fail-closed behavior. These constraints define the behavioral envelope and cannot be weakened by task intent.
2. **Accepted architecture decisions, frozen schemas, and reviewed contracts.**
3. **Current user task intent inside that envelope** — the user selects the objective, may narrow scope, may authorize broader phase scope where repository policy permits, and may choose among permitted alternatives. Task intent does not grant runtime authority or override constitutional constraints.
4. **Active implementation phase and exit criteria.**
5. **`Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md`.**
6. **Current repository structure, tests, and established conventions.**
7. **Recommendations, examples, and illustrative defaults.**

Within the same authority layer, prefer the more specific applicable repository instruction or reviewed contract. A more local, later, or task-specific instruction is not automatically more authoritative. Do not silently reconcile authoritative conflicts: preserve the higher-authority constraint, identify the conflict and affected invariant, and require a reviewed architecture/policy decision when the contract itself must change.

This is behavioral policy only. Instructions influence decisions; sandbox, approvals, command/tool policy, network policy, credentials, environment capability, and user authorization control effects.

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

The blueprint is authoritative for system contracts. This file is authoritative for Codex CLI repository-wide behavior.

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

Codex CLI must never simulate, infer, fabricate, or self-grant human approval. Approval never directly mutates active runtime state; normal reviewed engineering and deployment paths remain required.

## Repository conventions

Treat `pyproject.toml`, lockfiles, existing source, configuration, migrations, tests, and CI as the source of truth for the active stack and commands. Preserve blueprint-approved libraries and patterns. Do not introduce a competing framework, infrastructure library, configuration system, ORM, transport client, validation system, logging framework, or migration mechanism without an accepted architecture decision.

Keep modules small, typed, explicit, and composable. Keep side effects at narrow boundaries. Do not use convenience abstractions that erase strategy, risk, execution, reconciliation, accounting, credential, or AI-authority boundaries.

## Policy and workflow routing

Codex does not interpret Claude-style YAML path globs as native scoped instructions. This repository therefore keeps exact path-sensitive policy in `.codex/policies/` and resolves it deterministically.

**Before editing any repository path**, once the candidate write set is known, run:

```bash
python .codex/scripts/resolve_policies.py <path> [<path> ...]
```

Read every policy file it returns before editing. If the write set changes, resolve policies again for the newly added paths. A policy file's `paths:` frontmatter is data for the resolver; it is not a Codex-native instruction mechanism. Do not move these files to `.codex/rules/*.rules`: Codex reserves that location for Starlark command execution policy, which is a different mechanism.

Policy domains:

- `.codex/policies/kalshi-transport-safety.md` — demo endpoints, transport construction, mutation uncertainty
- `.codex/policies/credential-privacy.md` — secrets, redaction, logging, telemetry, process-key isolation
- `.codex/policies/architecture/dependency-boundaries.md` — package ownership, imports, authority reachability
- `.codex/policies/runtime-lifecycle.md` — startup, shutdown, suspension, fail-closed recovery
- `.codex/policies/market-data-and-eligibility.md` — allowlists, lifecycle checks, order-book health
- `.codex/policies/accounting-and-domain-models.md` — fixed-point values, provenance, ledger, reconciliation
- `.codex/policies/strategy-and-risk.md` — strategy limits, expectancy, deterministic risk controls
- `.codex/policies/research-evaluation-integrity.md` — microstructure research and evaluation states
- `.codex/policies/agents/openrouter-governance.md` — gateway, tools, evidence, routing, output validation
- `.codex/policies/governance-and-approvals.md` — approvals, proposals, promotion, configuration activation
- `.codex/policies/persistence-and-migrations.md` — schema changes, append-only history, migrations
- `.codex/policies/security-adversarial-review.md` — threat review for sensitive surfaces

Reusable procedures are in `.agents/skills/`. Use `safe-change-preflight`, `implement-safe-change`, and `verify-change` for nontrivial modifications, plus the domain-specific audit/contract/phase/memory skills when their descriptions match.

The former Claude JavaScript workflow launchers are native Codex orchestration skills under `.agents/skills/`: `implement-feature`, `phase-readiness-gate`, `swarm-standup`, `control-plane-change`, `contract-evolution`, and `security-sweep`. Their descriptions intentionally require explicit multi-agent/swarm intent where the original control plane required opt-in orchestration. They compose project-scoped custom roles in `.codex/agents/*.toml`; they do not replace human approval, deterministic authority, or active-phase discipline.

Durable swarm memory is mutable repository runtime data under `.codex/memory/`. It is not Codex product memory and is not part of the control-plane release archive or release identity. For a fresh installation, initialize only missing memory scaffolding from the immutable seed with `python .codex/scripts/initialize_runtime_state.py --initialize`; never overwrite existing memory during installation. Follow `.codex/memory/PROTOCOL.md` and the `memory-domain-sync` skill after initialization.

Control-plane ownership and artifact classes are declared in `.codex/control-plane/manifest.json`. The immutable release identity is `.codex/control-plane/definition-snapshot.json` plus `DEFINITION_HASHES.sha256`; mutable `.codex/memory/**`, runtime telemetry, and `.control-plane-state/**` are intentionally outside that release digest.

`.codex/control-plane/enforcement-contract.json` declares external authority state that must be present for governed execution. It does not grant that authority. When execution-state evidence is available, compile it with `.codex/scripts/compile_effective_state.py`; missing external authority evidence remains `UNVERIFIED`, never implicitly satisfied.

## Completion bar

A change is complete only when it preserves demo isolation, deterministic trading authority, AI and credential boundaries, reconciliation and accounting invariants, provenance, auditability, and active-phase scope; includes relevant failure-mode tests; and passes the required verification.

Never claim completion when required verification failed or was not run. Distinguish precisely between implemented, tested, mocked, simulated, partially implemented, unverified, and deferred behavior.
