---
paths:
  - "**/.claude/**"
  - "!**/.claude/control-plane/runs/**"
  - "!**/.claude/skills/writing-great-skills/**"
---

# Repository Boundary Rules

- Keep idea-to-MVP operating-system changes inside `.claude/` and approved root documentation unless the user explicitly expands scope.
- Treat `.claude/control-plane/manifest.yaml` as approval-gated. Do not edit it without explicit human approval.
- Existing files under `.claude/control-plane/runs/` are append-only evidence. Do not rewrite or delete them.
- Use one primary writer per transaction and keep the write set explicit before editing.
- When a change needs new repository surface outside these boundaries, stop and request approval instead of spilling into application code by default.
