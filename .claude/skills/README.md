# Skills Directory

Each skill should live in its own directory:

```text
.claude/skills/<skill-name>/
  SKILL.md
  scripts/      # optional
  references/   # optional
  assets/       # optional
  evals/        # optional
```

Require `name` and `description` as project policy. Evaluate routing separately from
execution behavior.

The current skill inventory is enumerated in `CLAUDE.md`'s "Rule routing" section, which
is the source of truth — do not duplicate that list here, to avoid the two going out of
sync as skills are added or retired.
