# Implementation Status

Read this before planning or editing (per `CLAUDE.md`). Implement only
the active phase; do not build later-phase behavior early.

- **Branch:** `phase-zero-reconciliation` (5 commits ahead of
  `origin/main`; nothing pushed).
- **Active phase:** Phase 0 — Contracts and safety model.
- **Phase 0 state:** Delivered and objectively verified on this branch
  (see "Verification evidence" below) — **awaiting human architectural
  review and approval**. `docs/adr/0001-blueprint-v3-baseline.md`
  status is **Proposed**, not accepted. Objective verification (tests,
  static analysis, the demo-only scanner) is not a substitute for that
  human review, and this document does not treat it as one. Phase 1
  must not begin until human approval is durably recorded here.
- **AI phases:** not started (AI Phase A is gated on stable
  deterministic simulation, risk, ledger, and replay evidence —
  Phases 3+).

## How this branch got here

This branch reconciles two independently developed Phase 0 lines: an
`origin/main` bootstrap (kebab-case schemas, `docs/SAFETY_MODEL.md`,
`scripts/verify_demo_only.py`) and a local `phase-zero-wip` set of
additive contracts and tests, imported and then reconciled field-by-field
rather than unioned. Commits on this branch, oldest first:

| Commit | Summary |
| --- | --- |
| `361b117` | Additively imported the WIP docs, 4 new schemas, the demo-endpoint contract module, and their tests alongside the existing origin artifacts (net-additive; nothing removed). |
| `efdb64f` | Reconciled the 4 schema pairs left duplicated by the additive import (`risk-limits`, `market-archetype`, `quote-expectancy`, `experiment-registration`) by keeping the origin (kebab-case, fixed-point) shape as base and merging in only genuine WIP gaps; declared the `jsonschema`/`types-jsonschema` dev dependencies the tests already required. |
| `592c94e` | Fixed two false-positive test failures surfaced by the reconciliation: the "no trading code" allowlist didn't know about the newly-approved `demo_endpoints.py` module, and the hostname scanner flagged the negative test fixtures that exist specifically to prove rejection of lookalike hosts. |
| `14184b0` | Reconciled `ARCHITECTURE.md`, `DATA_MODEL.md`, `FAILURE_TAXONOMY.md`, `PAPER_TRADING_PROTOCOL.md`, and `SAFETY_MODEL.md` so the prose contracts describe the merged schema set. |
| `cdea5e7` | Deleted the 8 standalone WIP policy docs whose binding content was already folded into `MICROSTRUCTURE_CONTRACT.md`, `RESEARCH_PROTOCOL.md`, `RISK_MODEL.md`, and `STRATEGY_SPEC.md` by the prior commit, preserving the one unique statement (no network calls in Phase 0) into `MICROSTRUCTURE_CONTRACT.md` §5. |

## Delivered artifact inventory

### Docs (`docs/`, 14 files)

`ARCHITECTURE.md`, `CREDENTIAL_POLICY.md`, `DATA_MODEL.md`,
`DEMO_ENDPOINT_POLICY.md`, `FAILURE_TAXONOMY.md`,
`IMPLEMENTATION_STATUS.md` (this file), `MICROSTRUCTURE_CONTRACT.md`,
`ORDER_STATE_MACHINE.md`, `PAPER_TRADING_PROTOCOL.md`,
`RESEARCH_PROTOCOL.md`, `RISK_MODEL.md`, `SAFETY_MODEL.md`,
`STRATEGY_SPEC.md`, `adr/0001-blueprint-v3-baseline.md`.

`CREDENTIAL_POLICY.md` and `DEMO_ENDPOINT_POLICY.md` are not
duplicates of `SAFETY_MODEL.md` §1–§2: `SAFETY_MODEL.md` is the
consolidated summary and explicitly delegates full detail to them
(same layering `DATA_MODEL.md` §3 uses for `ORDER_STATE_MACHINE.md`).
Status: **implemented (prose contract), awaiting human approval**.

### Schemas (`schemas/`, 9 files — all kebab-case, verified)

`experiment-registration.schema.json`, `market-archetype.schema.json`,
`markout-toxicity.schema.json`, `order-state.schema.json`,
`queue-calibration.schema.json`, `quote-expectancy.schema.json`,
`risk-limits.schema.json`, `statistical-sufficiency.schema.json`,
`trade-intent.schema.json`.

Status: **contract-only, verified valid JSON Schema by
`tests/test_phase0_schemas_valid.py`, awaiting human approval**. No
runtime code loads, validates against, or persists these schemas yet.

### Demo-endpoint policy module (`src/kalshi_bot/`)

`src/kalshi_bot/__init__.py` (package marker) and
`src/kalshi_bot/contracts/__init__.py`,
`src/kalshi_bot/contracts/demo_endpoints.py` — the single approved
Phase 0 exception to "no trading code": two immutable hostname
constants and a pure, side-effect-free `validate_host` predicate, with
no I/O and no imports of any transport/execution-capable module.
Status: **implemented and verified** (proven pure by
`tests/unit/test_demo_only_policy.py`'s AST-based import check;
proven correct by `tests/test_demo_endpoint_policy.py`).

### Verification script (`scripts/verify_demo_only.py`)

Static scanner over `ENFORCED_PATHS`
(`src/`, `config/`, `schemas/`, `scripts/`, `tests/`, `migrations/`,
`pyproject.toml`, `.env.example`) that fails on any non-demo Kalshi
hostname, honoring a narrow `demo-scan: allow-negative-fixture` marker
that only suppresses scanning inside `tests/`. Status: **implemented
and verified** — see "Verification evidence" below.

### Tests (`tests/`)

`tests/test_demo_endpoint_policy.py` (33 tests),
`tests/test_phase0_schemas_valid.py` (29 tests),
`tests/unit/test_demo_only_policy.py` (7 tests, includes
`test_no_trading_code_exists_in_phase_0`). `tests/acceptance/`,
`tests/contract/`, `tests/integration/`, `tests/property/` are empty
placeholder directories (`.gitkeep` only) for phases that do not exist
yet. Status: **implemented and passing** (69/69).

### Config and examples (`config/`)

`config/demo.example.yaml` (illustrative runtime config — every
credential is an env-var reference, `environment.mode` is hard-locked
to `demo`, `active_strategy` and every phase-gated version field are
explicitly `null`), `config/risk/conservative.yaml`,
`config/strategies/passive_spread.yaml`. Status: **contract-only
example, not loaded or parsed by any code**.

### Package and toolchain files

`pyproject.toml` (declares `pytest`, `ruff`, `mypy`, `jsonschema`,
`types-jsonschema` as dev dependencies; `dependencies = []` — no
runtime dependency exists), `uv.lock`, `.env.example`. Status:
**implemented**. `migrations/` contains only `.gitkeep` — **deferred**
until Phase 2–3 introduces persistence.

## Phase 0 exit criteria

| Exit criterion | Evidence | Status |
| --- | --- | --- |
| Production endpoints are explicitly forbidden | `docs/SAFETY_MODEL.md` §1, `docs/DEMO_ENDPOINT_POLICY.md`; `scripts/verify_demo_only.py` scan passes (21 files scanned); rejection proven by `tests/unit/test_demo_only_policy.py` and `tests/test_demo_endpoint_policy.py` | **Verified** |
| All state transitions and invariants are documented | `docs/DATA_MODEL.md` §3 (order states), §4 (ledger), §6 (traceability); `docs/ORDER_STATE_MACHINE.md`; order-book quality states in `docs/MICROSTRUCTURE_CONTRACT.md`; failure states in `docs/FAILURE_TAXONOMY.md` | **Verified (contract-only; no runtime enforces these states yet)** |
| No trading code exists yet | `src/kalshi_bot/` contains only the package marker plus the one approved demo-endpoint policy exception; asserted by `test_no_trading_code_exists_in_phase_0`'s explicit allowlist plus an AST purity check | **Verified** |
| Signal confidence, fill probability, and expected net edge are separate fields | Distinct required fields in `schemas/trade-intent.schema.json` (`signal_confidence`, `expected_fill_probability`, `expected_net_edge_usd`) and `schemas/quote-expectancy.schema.json` (`fill_probability`, `expected_net_edge_usd`); schema validity proven by `tests/test_phase0_schemas_valid.py` | **Verified — see field-naming note below** |
| Passive-spread edge is defined by a versioned expectancy decomposition | `docs/STRATEGY_SPEC.md` §3; required `edge_model_version` in both schemas | **Verified** |
| Promotion requires sample and diversity gates in addition to elapsed time | `docs/PAPER_TRADING_PROTOCOL.md` §2, §4; `docs/RESEARCH_PROTOCOL.md` §3; `minimum_evidence` required in `schemas/experiment-registration.schema.json` | **Verified** |

### Field-naming clarification (as requested for this reconciliation)

- `TradeIntent.expected_fill_probability`
  (`schemas/trade-intent.schema.json`) and
  `QuoteExpectancyRecord.fill_probability`
  (`schemas/quote-expectancy.schema.json`) are **fields on two
  different schemas** with different names; they must not be read as
  the same field or conflated during implementation.
- `expected_net_edge_usd` is the one frozen field name used by
  **both** `trade-intent.schema.json` and `quote-expectancy.schema.json`,
  but each schema owns its own field: `TradeIntent`'s is the strategy
  engine's forward estimate at decision time; `QuoteExpectancyRecord`'s
  is the versioned decomposition persisted per quote. Neither aliases
  or derives from the other. `docs/DATA_MODEL.md` §2's field list
  previously spelled this `expected_net_edge` (without the `_usd`
  suffix); that prose drift has been corrected in this reconciliation
  to match the frozen schema.

## Verification evidence

All commands run from the repository root on this branch's current
commit (`cdea5e7`, working tree clean before this commit):

| Check | Command | Result |
| --- | --- | --- |
| Full test suite | `uv run pytest -q` | **69 passed**, 0 failed, 0 skipped |
| Lint | `uv run ruff check .` | **All checks passed!** |
| Type check | `uv run mypy .` | **Success: no issues found in 7 source files** |
| Demo-only scanner | `uv run python scripts/verify_demo_only.py` | **demo-only policy OK (21 files scanned)** |
| Schema validation | covered by `tests/test_phase0_schemas_valid.py` (29 of the 69 pytest cases) | all 9 schemas parse as valid JSON Schema and match their governing docs |
| Diff hygiene | `git diff --check` | clean, no whitespace/conflict-marker errors |

Additional evidence gathered for this reconciliation (not a repository-native command, done by direct inspection):

- Every schema filename matches `^[a-z0-9]+(-[a-z0-9]+)*\.schema\.json$` (kebab-case) — confirmed for all 9 files.
- No reference to any of the 8 deleted WIP policy docs remains anywhere in `docs/`, `schemas/`, `src/`, `tests/`, `config/`, `scripts/`, or `pyproject.toml`.
- No non-demo Kalshi hostname appears in `docs/`, `schemas/`, `src/`, or `config/` outside the two files that name production-looking hosts specifically as rejected negative examples (`docs/DEMO_ENDPOINT_POLICY.md`, `docs/SAFETY_MODEL.md`).
- `docs/adr/0001-blueprint-v3-baseline.md` line 3 reads `**Status:** Proposed — awaiting human approval`; this document does not represent it as accepted.
- **Test-count investigation (71 vs. 69):** `uv run pytest --collect-only -q` on this branch's current commit collects exactly 69 tests (33 + 29 + 7, matching the three test files listed above), the same total the full run in this table reports. No commit reachable from this branch, `local-phase-zero-wip`, or `origin/main` was found — by direct collection on each — to produce 71. The `local-phase-zero-wip` bootstrap collects 26 schema tests against 8 snake_case schema files before `kalshi_bot` is installed as a package (a different, non-comparable state), and the post-import, pre-reconciliation commit `361b117` collects 67 once its missing `jsonschema` dependency is supplied, not 71. No tracked commit message, test file, or document in this repository's history contains the figure "71". Classification: **reporting error** — the current 69 is reproducible and internally consistent (69/69 passing, 29 of them schema tests across the 9 canonical kebab-case schemas); the earlier "71" claim could not be reproduced against any commit and is treated as a stale/incorrect prior report, not evidence of accidental test loss.

## Explicit Phase 0 non-goals and absent capabilities

None of the following exist anywhere in this repository as of Phase 0:

- No Kalshi REST or WebSocket transport/client (only the pure hostname
  allowlist and predicate in `demo_endpoints.py`).
- No authentication or credential-loading code; no environment
  variable is read by any code in this repository.
- No order placement, amendment, or cancellation logic.
- No strategy runtime (no code produces a `TradeIntent`).
- No risk engine or risk-gateway enforcement.
- No reconciliation logic or ledger implementation.
- No database, ORM, or Alembic migration (`migrations/` is a
  `.gitkeep`-only placeholder).
- No AI control plane, agent runtime, or OpenRouter client.
- No network call of any kind, including to Binance, CoinGecko, or any
  other external reference source (`docs/MICROSTRUCTURE_CONTRACT.md`
  §5).

## Known gaps and deferred work

- `README.md` was intentionally removed by the repository owner and
  has not been recreated.
- `docs/RUNBOOK.md` is a Phase 6 deliverable (not started).
- Correlation-group definitions
  (`scenario.correlation_groups_version`) and the frozen
  `edge_model_version` are deliberately null until their owning phases
  (pre-Phase-5).
- Alembic is not configured yet; `migrations/` is a placeholder until
  Phase 2–3 introduces persistence.
- CI workflow wiring for `scripts/verify_demo_only.py` and pytest is
  not yet set up (no `.github/workflows/` exists in this repository).
- **Maintenance obligation:** any future Phase 0 policy module added
  under `src/kalshi_bot/` alongside `demo_endpoints.py` requires a
  synchronized update to both `ENFORCED_PATHS` in
  `scripts/verify_demo_only.py` (or it becomes an unscanned gap in the
  demo-only guarantee) and the explicit path allowlist in
  `test_no_trading_code_exists_in_phase_0` (or the "no trading code"
  exit criterion silently stops being checked for the new module).
  Neither list updates itself.

## Workflow and tooling provenance

`.claude/**` (agents, rules, skills, hooks, statusline) is Claude Code
orchestration tooling for *working on* this repository — it is not
part of the Phase 0 product foundation described above, has not been
through the human architectural review this document tracks for
product artifacts, and is not itself a Phase 0 deliverable. Treat any
automation, skill, or hook under `.claude/**` as unreviewed process
tooling, not as an approved contract, until a human review of that
directory is separately recorded. Reconciling `.claude/**` content
between the two merged Phase 0 lines is remaining work not covered by
this branch's commits.

## Human-review gates still open

- ADR-0001 acceptance (`docs/adr/0001-blueprint-v3-baseline.md`
  status is Proposed).
- Overall Phase 0 sign-off recorded in this document (this entry
  itself must be added by a human reviewer, not inferred or
  self-granted by any agent).
- `.claude/**` reconciliation and review (see previous section).

## Phase ledger

| Phase | Status |
| --- | --- |
| 0 — Contracts and safety model | Delivered and verified; pending human review |
| 1 — Read-only connectivity | Not started |
| 2 — Order-book integrity | Not started |
| 3 — Portfolio and simulated execution | Not started |
| 4 — Demo order lifecycle | Not started |
| 5 — Passive spread strategy | Not started |
| 6 — Evaluation and hardening | Not started |
| AI A–D | Not started (gated) |
