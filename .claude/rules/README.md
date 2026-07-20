---
paths:
  - "**/.claude/rules/**/*.md"
---

# Rules Directory

Use this directory for modular Claude Code rules — always-relevant repository
conventions and constraints, not procedures.

- Give every rule file top-of-file `paths:` frontmatter naming the exact files or
  directories it governs. Prefer the narrowest glob that still covers the intended
  surface, and add a negative (`!...`) entry when a broader glob would otherwise
  catch files the rule should not touch.
- Keep rule bodies concise and testable: statements an agent (or reviewer) can
  check against a diff, not prose or tutorials.
- Do not place long procedural workflows here — route multi-step procedures to
  `.claude/skills/` and multi-stage orchestration to `.claude/workflows/`.
- `.claude/control-plane/scripts/validate.py` enforces non-empty, `.claude/`-scoped
  `paths:` frontmatter and at least one negative boundary for the rules listed in
  its `REQUIRED_RULES` table. `.claude/control-plane/evals/rules-cases.yaml` records
  narrative behavioral-eval scenarios reviewed during control-plane changes — it does
  not run automated glob-matching tests, so check a new `paths:` pattern against real
  positive and negative file paths yourself before committing it.
