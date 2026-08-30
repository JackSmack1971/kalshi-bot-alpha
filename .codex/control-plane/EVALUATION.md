# Static evaluation — Codex CLI control plane v1.0.0

**Claimed workflow:** This control plane exists to safely route and execute repository engineering, verification, cross-domain orchestration, and control-plane maintenance for the Kalshi Crypto Paper-Trading Bot v3 when Codex CLI is operating in the repository.

## Critical gates

| Gate | Result | Static evidence |
|---|---|---|
| G1 Routing boundary | PASS | Root `AGENTS.md`, 14 skill descriptions with positive/negative boundaries, 16 custom-role descriptions, and a 50-case routing corpus. |
| G2 Material decision value | PASS | Demo-only endpoints, deterministic authority, human approval, accounting/persistence constraints, exact path-policy resolver, and domain ownership materially change decisions. |
| G3 Observable definition of done | PASS | Verification skills require exact command/evidence reporting; orchestration workflows gate completion on verifier/test results. |
| G4 Failure/autonomy controls | PASS | Human approval is non-delegable; destructive/production actions are prohibited; security fixes require explicit authorization; read-heavy review is separated from writes. |
| G5 Empirical value | UNVALIDATED | No Codex CLI executable/authenticated target-repository runtime was available in this build environment, so no with-skill vs no-skill agent trials were run. |

## Design Readiness

| Dimension | Max | Score | Rationale |
|---|---:|---:|---|
| Workflow ownership & routing | 8 | 8 | Clear artifact/workflow ownership and explicit multi-agent opt-in neighbors. |
| Decision-changing information | 8 | 8 | High-density repository-specific safety/architecture/domain policy. |
| Loading & scope architecture | 5 | 5 | Always-on root is <10 KB; policies/skills/agents load by need; exact policy matching is externalized. |
| Decision envelope | 7 | 6 | Mandatory/prohibited/judgment regions are strong; per-agent tool allowlists from Claude have no exact hard Codex equivalent and are retained as policy except read-only verifier sandboxing. |
| Deterministic mechanisms | 5 | 5 | Policy resolution and control-plane validation are scripted and unit-tested. |
| Evidence & completion | 7 | 6 | Completion gates are explicit; application-level commands cannot be executed here because the archive contains only the control plane, not the target application repository. |
| Failure handling & autonomy | 6 | 5 | Major blockers/permissions/fan-out/write-conflict branches are covered; runtime subagent failure recovery still needs empirical testing. |
| Context efficiency | 4 | 3 | Root context is compact relative to Codex limits and branch detail is deferred, but some safety invariants intentionally repeat between constitutional guidance and specialized policies for defense in depth. |
| **Total** | **50** | **46** | **Design Readiness: 46/50 — UNVALIDATED** |

**Validated Performance:** NOT YET TESTED.

## Validation executed in this package build

- `python .codex/scripts/validate_control_plane.py`
- `python -m pytest -q .codex/tests/test_policy_resolution.py`
- resolver smoke tests across overlapping transport/security, risk/architecture, and research paths
- TOML parse of project config plus all custom-agent files
- stale Claude-harness reference scan

The provided eval corpus is ready for repeated Codex routing/task/failure trials against a no-skill baseline. Do not convert this static score into `/100` or claim G5 until those trials exist.
