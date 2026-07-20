---
paths:
  - "**/.claude/agents/security-engineer.md"
  - "**/.claude/hooks/guard_idea_to_mvp_tool_use.py"
  - "**/.claude/hooks/validate_idea_to_mvp_state.py"
  - "**/.claude/skills/validate-performance-and-security/**"
  - "**/.claude/workflows/test-phase.*"
  - "**/.claude/workflows/launch-phase.*"
  - "**/.claude/workflows/idea-to-mvp.*"
  - "!**/.claude/skills/release-mvp/**"
---

# Security Policy Rules

- Treat trust boundaries, approval gates, and state validators as hard controls, not advisory prose.
- Never allow launch-facing actions when required human decisions or prerequisite quality evidence are missing.
- Security findings must remain visible through launch readiness. Do not collapse them into generic risk language.
- Avoid storing raw secrets, raw hook payloads, or sensitive operational data in persisted workflow artifacts.
- Any change that weakens guard behavior requires explicit evidence that equivalent or stronger enforcement remains in place.
