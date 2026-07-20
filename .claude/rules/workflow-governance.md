---
paths:
  - "**/.claude/workflows/idea-to-mvp.md"
  - "**/.claude/workflows/idea-to-mvp.js"
  - "**/.claude/workflows/*-phase.md"
  - "**/.claude/workflows/*-phase.js"
  - "**/.claude/workflows/change-impact-loop.*"
  - "**/.claude/workflows/feedback-loop.*"
  - "!**/.claude/workflows/self-improvement.*"
---

# Workflow Governance Rules

- Keep workflow contracts in Markdown and execution logic in JavaScript. Do not move control flow into Markdown prose.
- The orchestrator owns eligibility, branching, retries, persistence, and approval stops. Specialists produce bounded outputs; they do not advance phases on their own authority.
- Stop at explicit human decision boundaries for product direction, MVP scope, release readiness, and any manifest change touching the control-plane trust boundary.
- Reopen only affected downstream work when upstream evidence changes. Do not regenerate the full workflow by default.
- Return structured status when blocked, awaiting approval, resume-ready, or learning-ready. Do not treat document existence as proof of completion.
