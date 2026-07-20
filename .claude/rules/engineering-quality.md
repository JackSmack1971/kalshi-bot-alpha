---
paths:
  - "**/.claude/agents/backend-engineer.md"
  - "**/.claude/agents/frontend-engineer.md"
  - "**/.claude/agents/integration-engineer.md"
  - "**/.claude/agents/technical-lead.md"
  - "**/.claude/skills/bootstrap-project-and-tooling/**"
  - "**/.claude/skills/implement-backend-capabilities/**"
  - "**/.claude/skills/implement-frontend-experience/**"
  - "**/.claude/skills/integrate-product-components/**"
  - "**/.claude/skills/review-code-and-architecture/**"
  - "**/.claude/workflows/build-phase.*"
  - "!**/.claude/workflows/test-phase.*"
---

# Engineering Quality Rules

- Implementation must stay inside the approved MVP scope and design handoff. Do not expand product scope inside engineering work.
- Prefer repository-native patterns and the smallest correct diff over new abstractions.
- Integration evidence must identify cross-surface assumptions, not just successful local code generation.
- Code and architecture review artifacts must record material risks, limitations, and follow-ups explicitly.
- Build outputs are not phase-complete until architecture, implementation, integration, and review evidence agree on the same bounded slice.
