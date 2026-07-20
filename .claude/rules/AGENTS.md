---
paths:
  - "**/.claude/agents/*.md"
---

# Sub-Agent File Rules

- Ground all work on files in `.claude/agents/` in `docs-dev/Claude Code Sub-Agent Methodology/Claude Code Sub-Agent Methodology.md`. Read it before creating or editing a sub-agent file.
- Treat that document and the sibling files in `docs-dev/` (workflows, skills, rules context) as authoritative. Do not silently edit them to make them agree with new agent code — a mismatch is an open question, not a rewrite target.
- When an open question is not covered there, do the research (spin up a sub-agent if needed), record the resulting assumption explicitly, and propose the source-of-truth update as a separate, reviewable change rather than folding it into the agent change that raised it.
