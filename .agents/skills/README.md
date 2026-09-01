# Repository Codex skills

Codex discovers repository Skills from `.agents/skills/`. Eight reusable procedure Skills and six orchestration Skills preserve the original repository workflow boundaries while using Codex-native custom roles.

A Skill is procedural definition, not permission. Skill activation may recommend tools, scripts, or subagents, but actual capability and authorization remain runtime/policy decisions.

Each Skill declares `telemetry/schema.json`. Runtime quality telemetry is appended through `.codex/scripts/skill_telemetry.py`, ignored by Git, and excluded from the immutable control-plane definition snapshot. Telemetry schema v2 requires one `run_id` per Skill invocation, contiguous `sequence`, and hash-linked `parent_event_hash`/`event_hash` fields. Start one run, reuse its ID for consequential events, then finish that same run.

The shared validator checks schema/lifecycle integrity, redaction boundaries, stale role references, and observable completion/failure declarations. Routing cases live separately in `.codex/evals/skill-routing.json`; the larger 65-case control-plane corpus lives in `.codex/control-plane/evals/` and is validated/graded by `.codex/scripts/control_plane_eval.py`.

Multi-agent orchestration Skills intentionally require explicit swarm/multi-agent intent. The primary agent/orchestration Skill remains the supervisor; `phase-router` only returns a read-only task graph and never recursively dispatches workers. Ordinary implementation should route through `safe-change-preflight`, `implement-safe-change`, and `verify-change` without unnecessary subagents.
