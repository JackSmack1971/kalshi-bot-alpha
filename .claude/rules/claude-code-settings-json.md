---
paths:
  - "**/.claude/settings.json"
  - "**/.claude/settings.local.json"
---

# Claude Code settings.json Rules

Local conventions for this repository's project (`.claude/settings.json`) and
local (`.claude/settings.local.json`) settings files. For the authoritative field
list, precedence rules, and hook schema, see
https://code.claude.com/docs/en/settings, https://code.claude.com/docs/en/permissions,
and https://code.claude.com/docs/en/hooks — this file states only repository
policy on top of them.

## Conventions

- Start the file with `"$schema": "https://json.schemastore.org/claude-code-settings.json"`
  as the first key. `.claude/control-plane/scripts/validate.py` checks for this
  in `.claude/settings.json`.
- `permissions` is an object with `allow` / `deny` / `ask` arrays of permission-rule
  strings (`Tool`, `Tool(specifier)`, or `mcp__*`), plus scalars such as `defaultMode`
  and `additionalDirectories`. It is never a top-level array.
- `hooks` is an object keyed by lifecycle event name (`PreToolUse`, `PostToolUse`,
  `SessionStart`, `Stop`, `Notification`, `ConfigChange`, etc.), each value an array
  of `{matcher, hooks: [{type, command, args, if, timeout}]}` entries. It is never a
  top-level array.
- Put only Claude-Code-relevant variables in `env` (string values). Never store
  secrets there — use `apiKeyHelper` or an external secret manager.
- Managed-only keys (`allowManagedPermissionRulesOnly`, `allowedMcpServers`,
  `claudeMd`, `blockedMarketplaces`, etc.) belong in managed settings, not here;
  they are ignored or rejected at project/local scope.

## Precedence (informational)

Within these two files: Local (`.claude/settings.local.json`) overrides Project
(`.claude/settings.json`). Managed settings and command-line argument overrides
sit above both and cannot be overridden from here. Permission `allow`/`deny`/`ask`
entries merge across scopes rather than one scope replacing another; most other
scalar keys take the value from the highest-precedence file that sets them.

## Advisory guidance vs. enforcement

This file is advisory; it does not stop a malformed or unsafe `settings.json` from
being written. What actually enforces behavior:
- Claude Code's own parser: an invalid project or local settings file is rejected
  as a whole (managed settings parse tolerantly instead and strip only the invalid
  entry).
- `PreToolUse` command hooks that exit non-zero or return
  `permissionDecision: "deny"` for anything that must be blocked outright —
  `permissions.deny` alone is a soft rule an agent can still be argued out of.

## Validation

- After editing, run `claude doctor` to surface stripped or invalid entries.
- Open the file in an editor with SchemaStore support to confirm autocomplete and
  validation match the schema. A validation warning on a field documented at
  https://code.claude.com/docs/en/settings but not yet in the published SchemaStore
  schema does not mean the config is invalid — prefer the docs over schema lag.
