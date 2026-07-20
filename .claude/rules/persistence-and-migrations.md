---
paths:
  - "src/persistence/**/*.py"
  - "src/models/**/*.py"
  - "src/database/**/*.py"
  - "migrations/**/*.py"
  - "alembic/**/*.py"
  - "alembic.ini"
  - "tests/migrations/**/*.py"
  - "tests/persistence/**/*.py"
---

# Persistence and migrations

Before changing persistent models:

- Identify the owning domain invariant.
- Classify the data as authoritative, derived, immutable evidence, validated finding, or proposal.
- Preserve append-only behavior where required.
- Add an Alembic migration when schema changes are authorized.
- Test upgrade behavior from the prior schema.
- Preserve reproducibility, hashes, provenance, and version links.
- Do not rewrite historical evidence to fit a new schema.
- Prefer supersession/version links over destructive mutation.

Do not run destructive migrations, delete evidence, reset ledgers, or rewrite historical records without explicit authorization. Persistence failure during an authoritative mutation must fail closed. Test migration upgrade, rollback policy where supported, duplicate application, partial failure, and replay compatibility.
