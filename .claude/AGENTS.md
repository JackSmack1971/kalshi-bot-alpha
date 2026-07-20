# `.claude` Intent Layer

Read this file first for work under `.claude/`.

## Scope

- `.claude/control-plane/`: manifest, bootstrap, protocols, schemas,
  validators, and run ledger.
- `.claude/agents/`, `.claude/rules/`, `.claude/skills/`, `.claude/workflows/`,
  `.claude/hooks/`: specialist-facing instruction surfaces and orchestration
  assets.

## Rules

- Follow `.claude/control-plane/manifest.yaml` before editing any control-plane
  artifact.
- Use one primary writer, an explicit write set, deterministic validation,
  independent verification, and rollback on failure.
- Do not write application-source changes from this subtree.
