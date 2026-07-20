# Idea-to-MVP State

This directory holds persisted operating-system state for the Claude Code
idea-to-MVP workflow.

Tracked files:

- `workflow-state.json`
- `artifact-manifest.json`
- `artifact-dependency-graph.json`
- `risk-register.json`
- `assumptions-register.json`
- `gate-results.jsonl`
- `decision-records.jsonl`
- `artifacts/`
- `handoffs/`

Use `python .claude/control-plane/scripts/idea_to_mvp_state.py bootstrap` to
initialize missing files and `... validate` to check integrity.

Handoff packets are stored as JSON files under `handoffs/`.
