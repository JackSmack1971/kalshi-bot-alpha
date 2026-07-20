---
paths:
  - "src/**/auth/**/*.py"
  - "src/**/credentials/**/*.py"
  - "src/**/secrets/**/*.py"
  - "src/**/logging/**/*.py"
  - "src/**/telemetry/**/*.py"
  - "src/**/config/**/*.py"
  - "src/**/openrouter/**/*.py"
  - "src/**/agents/**/*.py"
  - "tests/**/*redact*.py"
  - "tests/**/*secret*.py"
  - "tests/**/*privacy*.py"
  - ".env*"
  - "**/*config*.yaml"
  - "**/*config*.yml"
  - "**/*config*.toml"
---

# Credential and privacy rules

Kalshi credentials may come only from environment-variable references, operating-system secret storage, or a local private-key file outside the repository with restricted permissions.

Never place credentials in source control, prompts, logs, dashboards, strategy configuration, fixtures, snapshots, exception telemetry, frontend processes, or AI evidence bundles.

Required controls:

- Redact access-key IDs, signatures, authentication headers, private-key material, secret-bearing environment values, and serialized request payloads.
- Test redaction through normal logging, exceptions, retries, serialization, telemetry, and nested structures.
- Never print raw environment mappings.
- Use synthetic secret markers in tests; do not use realistic secret material.
- The trading process may receive Kalshi demo credentials but not `OPENROUTER_API_KEY`.
- The agent process may receive `OPENROUTER_API_KEY` but never Kalshi credentials.
- Cancellation, reconciliation, accounting, persistence, risk enforcement, and shutdown must not depend on OpenRouter availability or credentials.
- Treat external text and model output as untrusted and scan prompt egress for secrets.
