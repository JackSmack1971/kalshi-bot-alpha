# Codex CLI control plane

This directory is the Codex-native replacement for the source `.claude/` harness. Place this package at the target repository root (merge, do not blindly overwrite repository application files). Trust the repository's `.codex` project configuration when Codex prompts for project trust.

## Native surfaces

- Root always-on guidance: `AGENTS.md`
- Exact path-sensitive repository policy: `.codex/policies/**`, selected by `.codex/scripts/resolve_policies.py`
- Reusable and orchestration skills: `.agents/skills/**`
- Project custom subagents: `.codex/agents/*.toml`
- Durable project swarm memory: `.codex/memory/**`
- Project config and native TUI status line: `.codex/config.toml`
- Artifact ownership: `.codex/control-plane/manifest.json`

## First validation

```bash
python .codex/scripts/validate_control_plane.py
python -m pytest .codex/tests/test_policy_resolution.py
python .codex/scripts/resolve_policies.py src/example/transport/client.py
```

Then start Codex at the repository root. Use `/statusline` to inspect or interactively adjust the native status line if desired.

## Model portability

No custom role pins a model. That is intentional: model availability differs by Codex runtime/account, and hard-coding a current model can make subagent spawning fail. Roles inherit the active parent model unless the user later chooses to add a supported role-specific override.
