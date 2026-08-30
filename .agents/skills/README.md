# Repository Codex skills

Codex discovers repository skills from `.agents/skills/`. The eight procedure skills were migrated from the Claude control plane. Six former JavaScript workflow launchers were converted to Codex-native orchestration skills that use project-scoped custom subagents.

Each skill declares a local `telemetry/schema.json`; runtime events are appended
through `.codex/scripts/skill_telemetry.py` and ignored by Git. The shared
validator checks schemas, redaction boundaries, stale role references, and
observable completion/failure declarations. Routing cases live separately in
`.codex/evals/skill-routing.json` so revisions can be compared against the same
positive and negative corpus.

Multi-agent orchestration skills intentionally require explicit swarm/multi-agent intent, preserving the source control plane's opt-in fan-out boundary. Ordinary implementation should route through `safe-change-preflight`, `implement-safe-change`, and `verify-change` without unnecessary subagents.
