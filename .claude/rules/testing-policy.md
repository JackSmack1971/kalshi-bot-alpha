---
paths:
  - "**/.claude/agents/qa-engineer.md"
  - "**/.claude/skills/conduct-uat-and-usability-validation/**"
  - "**/.claude/skills/create-test-plan/**"
  - "**/.claude/skills/diagnose-and-fix-defects/**"
  - "**/.claude/skills/execute-functional-testing/**"
  - "**/.claude/skills/prepare-test-record/**"
  - "**/.claude/skills/validate-performance-and-security/**"
  - "**/.claude/workflows/test-phase.*"
  - "!**/.claude/workflows/build-phase.*"
---

# Testing Policy Rules

- The test phase must prove the approved slice, not just exercise happy paths.
- Test plans, execution records, UAT findings, defect loops, performance results, and security results must remain separate artifacts with explicit dependencies.
- Failed or incomplete quality evidence blocks launch. Do not downgrade failures into narrative caveats.
- Defect rework must cite the failing evidence that triggered it.
- Performance and security checks are required launch inputs, not optional polish work.
