# Evaluation — Codex CLI control plane v1.1.1

**Status:** mechanically improved and statically validated; empirical Codex behavior remains **UNVALIDATED** until actual target-repository trials are captured and graded.

The former `46/50` design-readiness score is retained only as historical context in the migration/audit record. It is **not** a release gate and must not be presented as validated runtime performance.

## Release gates

A v1.1.1 control-plane release is mechanically acceptable only when all of the following pass:

1. `python .codex/scripts/validate_control_plane.py`
2. `python -m pytest -q -p no:cacheprovider .codex/tests`
3. `python .codex/scripts/skill_eval.py --validate`
4. `python .codex/scripts/control_plane_eval.py --validate-corpus`
5. `python .codex/scripts/build_definition_snapshot.py --verify`

The release snapshot deliberately excludes mutable `.codex/memory/**`, live Skill telemetry, `.control-plane-state/**`, and generated Python bytecode.

The distributable zip must be built with `build_release_archive.py`; directly zipping an active checkout can reintroduce mutable runtime state that is intentionally outside the release identity.

## Critical gates

| Gate | Current result | Mechanical evidence |
|---|---|---|
| G1 Routing boundary | PASS — static | Root behavioral policy, bounded Skill descriptions, specialized custom roles, and 50 routing cases. |
| G2 Material decision value | PASS — static | Demo-only, credential isolation, deterministic authority, approval integrity, path-scoped policy, ownership boundaries. |
| G3 Observable definition of done | PASS — static | Completion/failure contracts plus exact validation/evidence requirements. |
| G4 Failure/autonomy controls | PASS — static | Read-only router/reviewers, single primary orchestration owner, no self-granted approval, blocked/indeterminate states preserved. |
| G5 Empirical value | UNVALIDATED | The package contains an executable corpus validator/grader, but no authenticated Codex target-repository trial results are bundled. |
| G6 Release identity | PASS when snapshot verifies | `definition-snapshot.json` + `DEFINITION_HASHES.sha256`, generated after validation and excluding mutable state. |
| G7 Audit causality | PASS for local mechanism | Skill telemetry uses one run ID per invocation with sequence/hash chaining; execution audit has a separate chained ledger. Off-host durability still belongs to deployment governance. |
| G8 External authority evidence | UNVERIFIED unless supplied | `enforcement-contract.json` is checked against supplied runtime/admin evidence; missing evidence stays UNVERIFIED and never becomes a permission grant. |

## Empirical trial contract

The 65-case corpus is now executable as a grading contract:

```bash
python .codex/scripts/control_plane_eval.py --validate-corpus
python .codex/scripts/control_plane_eval.py --grade path/to/observed-results.jsonl
```

Observed results must come from actual Codex runs in the intended target repository/runtime to count as empirical evidence. The grader accepts routing selections and exact boolean assertions keyed by the corpus criteria. Corpus presence or schema validity alone is not a behavioral PASS.

The grader now distinguishes **complete** from **passed**. `complete=true` means every corpus case supplied a structurally usable observation. `passed=true` additionally requires every routing expectation and every workflow/failure assertion to pass. The CLI exits non-zero for a complete-but-failing observation set, so CI cannot mistake mere coverage for success.

For baseline-vs-candidate evaluation, capture separate observed-result files for the no-candidate and candidate configurations and compare the resulting routing/assertion metrics externally. Do not infer model behavior from Skill text.

## Authority statement

Repository instructions, Skills, tool metadata, custom-agent definitions, snapshots, and the enforcement contract do not grant authority. Runtime authorization remains the intersection of identity/admin requirements, sandbox/permission profile, command/tool policy, network policy, credentials, environment capability, user authorization, and invocation-time decisions.
