# Codex CLI control plane

This directory is the Codex-native project control plane for the target repository. Merge it into the repository root rather than blindly overwriting application files. Project `.codex` configuration participates only under the runtime's project-trust rules.

## Architectural boundary

```text
behavioral definition -> influences agent decisions
runtime/admin policy   -> authorizes effects
runtime                -> executes effects
Git                    -> identifies engineering change
audit/governance       -> explains observable decisions/effects
```

Skills, custom agents, tool registration/metadata, and repository instructions never grant filesystem, shell, network, credential, Git-history, external-write, deployment, or production authority.

## Native surfaces

- Root persistent behavioral policy: `AGENTS.md`
- Exact path-sensitive behavioral policy: `.codex/policies/**`, compiled by `.codex/scripts/resolve_policies.py`
- Reusable/orchestration Skills: `.agents/skills/**`
- Project custom roles: `.codex/agents/*.toml`
- Durable project coordination memory: `.codex/memory/**` (mutable runtime data, no authority; initialized from immutable seed when missing)
- Runtime-state seed: `.codex/control-plane/runtime-seed/**`
- Project config/status line: `.codex/config.toml`
- Definition/lifecycle ownership: `.codex/control-plane/manifest.json`
- External authority requirements: `.codex/control-plane/enforcement-contract.json`
- Immutable release identity: `.codex/control-plane/definition-snapshot.json` + `DEFINITION_HASHES.sha256`
- Runtime execution/audit state: `.control-plane-state/**` (excluded from release identity)
- Definition-only release packaging: `.codex/scripts/build_release_archive.py`

## Release validation

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/validate_control_plane.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider .codex/tests
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/skill_eval.py --validate
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/control_plane_eval.py --validate-corpus
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/build_definition_snapshot.py --verify
```

When changing definition files, validate the edited tree **without accepting the stale prior snapshot**, then regenerate the immutable release identity and run the strict release gate:

```bash
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/validate_control_plane.py --pre-snapshot
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider .codex/tests
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/skill_eval.py --validate
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/control_plane_eval.py --validate-corpus
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/build_definition_snapshot.py --write
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/validate_control_plane.py
PYTHONDONTWRITEBYTECODE=1 python .codex/scripts/build_definition_snapshot.py --verify
```

Do not include `.codex/memory/**`, live `telemetry/events.jsonl`, `.control-plane-state/**`, `__pycache__`, `*.pyc`, or `.pytest_cache/**` in definition hashes or release archives. `.codex/control-plane/runtime-state.ignore` contains recommended ignore patterns for the target repository.

## Fresh-install runtime state

Release archives intentionally omit mutable `.codex/memory/**`. After merging the control-plane definition into a repository that does not already have memory state, initialize the missing scaffolding from the immutable seed:

```bash
python .codex/scripts/initialize_runtime_state.py --initialize
python .codex/scripts/initialize_runtime_state.py --check
```

The initializer uses create-only writes. Existing memory is preserved byte-for-byte and is never replaced by release packaging or seed content.

## Deterministic release archive

After the strict release gate passes, build the distributable archive from the verified definition snapshot rather than zipping the checkout directly:

```bash
python .codex/scripts/build_release_archive.py \
  --output ../kalshi-bot-alpha-control-plane-v1.1.1-audit-hardened.zip
```

The archive contains exactly the files named by `definition-snapshot.json` plus `definition-snapshot.json` and `DEFINITION_HASHES.sha256`. It therefore omits Git metadata, historical swarm memory, live Skill telemetry, runtime execution state, bytecode, and test caches.

## Policy resolution snapshot

Human-readable selection:

```bash
python .codex/scripts/resolve_policies.py src/example/transport/client.py
```

Machine-readable, content-addressed selection:

```bash
python .codex/scripts/resolve_policies.py --json src/example/transport/client.py
```

The resolver canonicalizes repository-relative targets, rejects outside-repository paths, records matched patterns/content digests, and emits a deterministic `ResolvedPolicySet` digest. It resolves behavioral policy only.

## External enforcement contract

Supply a runtime/admin-derived authority-state JSON object and verify it:

```bash
python .codex/scripts/verify_enforcement_contract.py \
  .codex/control-plane/authority-state.example.json
```

The example demonstrates shape only. A PASS means the **supplied evidence** satisfies repository requirements; it does not create those permissions or prove that the evidence source is trustworthy.

## Git Unit of Work

In the actual Git repository, capture the baseline and intended write set before implementation:

```bash
python .codex/scripts/capture_uow.py \
  --intended-path src/risk/ \
  --intended-path tests/risk/ \
  --output .control-plane-state/runs/<run-id>/uow.json
```

This is an evidence object, not permission to edit those paths. The record uses `intended_delta`, not an authorization field. Git diff remains authoritative for the resulting engineering delta. Rename/copy baselines preserve both destination and original paths.

## Effective-state compilation

Compile the observable project definition together with externally resolved runtime evidence:

```bash
python .codex/scripts/compile_effective_state.py \
  --target-path src/risk/gateway.py \
  --authority-state path/to/authority-state.json \
  --capability-state path/to/capability-state.json \
  --environment-state path/to/environment-state.json \
  --uow-state .control-plane-state/runs/<run-id>/uow.json \
  --model <resolved-model> \
  --reasoning-effort <resolved-effort> \
  --output .control-plane-state/runs/<run-id>/execution-snapshot.json
```

Any external component not supplied is recorded as `UNVERIFIED`; the compiler never infers runtime authority from repository prose.

## Invocation-scoped Skill telemetry

Every Skill invocation uses one run ID:

```bash
python .codex/scripts/skill_telemetry.py start verify-change invocation_started \
  --reason-code requested

python .codex/scripts/skill_telemetry.py emit verify-change check_result \
  --run-id <same-id> --outcome passed --reason-code targeted-check

python .codex/scripts/skill_telemetry.py finish verify-change invocation_finished \
  --run-id <same-id> --outcome passed --reason-code complete
```

Sequence numbers and parent-event hashes are generated mechanically. Runs must begin with `invocation_started`, end with `invocation_finished`, and reject post-finish events. Skill telemetry remains lightweight quality telemetry and is excluded from release identity.

## Causal execution audit

`.codex/scripts/execution_audit.py` writes a separate hash-chained local audit stream beneath `.control-plane-state/runs/<run-id>/audit.jsonl`. Audit runs must begin with `run.started`, terminate with `run.completed`, and reject events after completion. It records observable actor/operation/policy/evidence/effect references rather than hidden model reasoning. Local audit state is not an off-host authoritative ledger; managed deployments should export/correlate it with durable organizational telemetry/audit systems.

## Model portability

No custom role pins a model. Roles inherit runtime model resolution unless a supported deployment intentionally overrides them. Reproducible runs should record the actually resolved model/reasoning in the execution snapshot rather than treating portability-oriented omission as reproducibility evidence.
