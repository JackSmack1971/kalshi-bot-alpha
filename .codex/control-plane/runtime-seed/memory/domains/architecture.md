# Domain log — architecture

Append-only. See `.codex/memory/PROTOCOL.md` for format and rules.
Recorder: parent/orchestrator via `memory-domain-sync`; evidence source is normally `.codex/agents/architecture-boundary-verifier.toml`.
