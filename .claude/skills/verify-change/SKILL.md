---
name: verify-change
description: Use after implementation to select and run repository-native validation, safety suites, static analysis, and diff review, then report exact evidence. Trigger on verify, test, validate, check, completion, or before merge. NOT for demo order acceptance tests unless explicitly authorized and demo credentials are configured.
---

# Verify a repository change

Use repository-native commands from `pyproject.toml`, task runners, scripts, and CI as authoritative. When no wrapper exists, run applicable checks such as:

```bash
ruff check .
ruff format --check .
mypy src
bandit -r src
pytest tests/unit
pytest tests/property
pytest tests/contract
pytest tests/integration
```

For affected AI code, also run applicable suites:

```bash
pytest tests/agents
pytest tests/openrouter
pytest tests/privacy
pytest tests/adversarial
```

Verification sequence:

1. Run targeted tests for changed behavior.
2. Run every directly affected contract and integration suite.
3. Run demo-only endpoint and authority-boundary tests.
4. Run relevant static analysis on changed files or the repository-defined scope.
5. Run migration upgrade tests when persistence changed.
6. Inspect the diff and repository status.
7. Report every command, exit result, failure, skipped suite, and reason.

Never claim “all tests pass” unless the full stated suite actually ran and passed. Never run credentialed demo acceptance tests unless explicitly authorized and configured for demo-only operation. A failed required check blocks completion; do not weaken the check to obtain a pass.
