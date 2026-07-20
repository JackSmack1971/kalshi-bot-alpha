---
paths:
  - "**/.claude/workflows/idea-to-mvp.*"
  - "**/.claude/workflows/change-impact-loop.*"
  - "**/.claude/hooks/*.py"
  - "**/.claude/control-plane/scripts/idea_to_mvp_state.py"
  - "**/.claude/control-plane/scripts/self_improvement_evidence.py"
  - "!**/.claude/hooks/AGENTS.md"
---

# Evidence Policy Rules

- Separate verified evidence, assumptions, estimates, and unresolved gaps. Do not flatten them into one summary.
- When evidence is missing, return blocked, conditional, or re-entry status instead of inventing coverage.
- Keep run and state artifacts append-only where the workflow contract says they are append-only.
- Record diagnostics and validation failures without storing raw sensitive payloads or prompt contents.
- Compare new behavior against persisted evidence when the workflow supports resume, audit, or change-impact modes.
