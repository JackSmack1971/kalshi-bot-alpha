---
paths:
  - "**/.claude/workflows/idea-to-mvp.*"
  - "**/.claude/workflows/change-impact-loop.*"
  - "**/.claude/hooks/validate_idea_to_mvp_state.py"
  - "**/.claude/control-plane/scripts/idea_to_mvp_state.py"
  - "**/.claude/control-plane/schemas/*artifact*.json"
  - "**/.claude/control-plane/schemas/*handoff*.json"
  - "**/.claude/control-plane/schemas/*gate-result*.json"
  - "**/.claude/control-plane/schemas/*decision-record*.json"
  - "!**/.claude/control-plane/schemas/run-*.json"
---

# Artifact Contract Rules

- Every non-root artifact must declare its direct upstream dependencies in persisted state.
- Artifact IDs, paths, phases, owners, and status values must stay deterministic across workflow runs.
- Handoffs, gate results, and decision records are contracts, not free-form notes. Keep field names stable and schema-valid.
- Persisted state must distinguish draft, approved, blocked, stale, and superseded outcomes explicitly.
- Do not silently overwrite prior authoritative artifacts. Record the new state and preserve the dependency chain.
