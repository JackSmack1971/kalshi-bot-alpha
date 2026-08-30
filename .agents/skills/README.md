# Repository Codex skills

Codex discovers repository skills from `.agents/skills/`. The eight procedure skills were migrated from the Claude control plane. Six former JavaScript workflow launchers were converted to Codex-native orchestration skills that use project-scoped custom subagents.

Multi-agent orchestration skills intentionally require explicit swarm/multi-agent intent, preserving the source control plane's opt-in fan-out boundary. Ordinary implementation should route through `safe-change-preflight`, `implement-safe-change`, and `verify-change` without unnecessary subagents.
