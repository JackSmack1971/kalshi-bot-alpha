---
paths:
  - "**/.claude/agents/*.md"
  - "**/.claude/workflows/idea-to-mvp.*"
  - "**/.claude/workflows/*-phase.*"
  - "**/.claude/workflows/change-impact-loop.*"
  - "**/.claude/workflows/feedback-loop.*"
  - "!**/.claude/agents/control-plane-verifier.md"
---

# Decision Authority Rules

- The orchestrator decides what is eligible to run next and when human approval is required.
- Product strategy decisions belong to product specialists and human product owners, not engineering validators.
- Technical feasibility and architecture decisions require architecture or technical-lead authority plus recorded rationale.
- A specialist must not be the only validator of its own authoritative output.
- Release authorization is separate from deployment readiness. Do not treat operational evidence as product-owner approval.
