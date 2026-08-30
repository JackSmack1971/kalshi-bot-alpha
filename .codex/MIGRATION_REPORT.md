# Claude Code → Codex CLI migration report

## Semantic mapping

| Source mechanism | Codex control-plane result | Parity |
|---|---|---|
| `CLAUDE.md` | root `AGENTS.md` | native |
| `.claude/rules/*.md` path globs | `.codex/policies/*.md` + deterministic resolver invoked by `AGENTS.md`/preflight | functional redesign |
| `.claude/skills/*/SKILL.md` | `.agents/skills/*/SKILL.md` | native |
| `.claude/agents/*.md` | `.codex/agents/*.toml` | native role format |
| `.claude/workflows/*.js` + Claude Workflow tool | six orchestration `SKILL.md` workflows using Codex subagents | functional redesign |
| `.claude/memory/**` | `.codex/memory/**` repository-owned durable memory | direct data migration |
| command-backed PowerShell status line | native `[tui].status_line` config | native subset |

## Intentional non-1:1 mappings

1. **Do not rename Claude path rules to `.codex/rules/*.rules`.** In Codex, `.rules` are Starlark command execution policy, not behavioral/path-scoped instruction markdown. Exact original globs are retained as policy metadata and matched by a deterministic resolver.
2. **No JavaScript `Workflow` runtime is carried forward.** Codex multi-agent orchestration is expressed as workflow skills that spawn project custom roles. This keeps execution in the supported CLI harness and removes an unavailable source-specific tool dependency.
3. **Claude `tools`, `disallowedTools`, `maxTurns`, `permissionMode`, and `model: sonnet` frontmatter are not copied as fake Codex fields.** Role behavior is encoded in `developer_instructions`; the truly read-only `control-plane-verifier` additionally uses `sandbox_mode = "read-only"`. Other roles inherit the session sandbox/approval/model rather than risk an unsupported escalation or model pin.
4. **Status-line parity is bounded by Codex's native item set.** Model/reasoning, run state, directory, Git branch, permissions, approval mode, context remaining, usage limits, used tokens, and estimated thread cost are mapped. Claude-specific API-duration, context-velocity, theme/powerline renderer, health-check, and update-check logic had no equivalent command-backed extension point in the current native status-line model and were not carried as dead code.
5. **The source specialist agents referenced a missing `.claude/control-plane/manifest.yaml`.** The migration supplies `.codex/control-plane/manifest.json`, eliminating that broken dependency and making artifact ownership explicit.
6. **Parallel writes are narrowed.** Independent read-heavy auditors still run concurrently. Domain implementation follows dependency order, and security auto-fixes are sequential where overlap is possible. This preserves review parallelism without creating avoidable write conflicts.

## Trust and enforcement

Project-scoped Codex configuration is trust-sensitive. Repository policy prose and approved write sets guide behavior but are not claimed as cryptographic enforcement. Use Codex sandbox/approval settings for platform enforcement. Hooks can supplement this later, but this migration does not add a hook merely to simulate a complete security boundary.
