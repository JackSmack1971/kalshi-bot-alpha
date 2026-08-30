# Skill evaluation corpus

`skill-routing.json` is the stable routing and boundary corpus for the 14
repository skills. It is intentionally separate from skill packages so
description revisions can be compared without changing the evaluated target.

Run the deterministic corpus check with:

```text
python .codex/scripts/skill_eval.py --validate
```

Runtime paired evaluation records may be compared with:

```text
python .codex/scripts/skill_eval.py --compare baseline.json with-skill.json
```

The records must use the same prompts, mode, permissions, timeout, and working
directory. These are explicit/applicability results, not measurements of
implicit host discovery. Missing records are reported as unknown, never as a
pass.
