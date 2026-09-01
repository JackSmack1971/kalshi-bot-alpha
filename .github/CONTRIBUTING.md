# Contributing

## Before opening a pull request

Read `AGENTS.md`, `docs/IMPLEMENTATION_STATUS.md`, and the applicable policy
files under `.codex/policies/`. Keep changes within the active phase and
preserve demo-only operation, deterministic trading authority, credential
privacy, reconciliation, accounting, and fail-closed behavior.

Run:

```text
uv run pytest -q
uv run ruff check .
uv run mypy .
uv run python scripts/verify_demo_only.py
git diff --check
```

Do not run credentialed acceptance tests unless demo credentials are
explicitly configured and the test is authorized.

## Pull requests

Use a focused pull request with a concise description of the behavior,
affected invariants, verification evidence, and any unverified or deferred
work. Preserve existing user changes and avoid unrelated formatting.

The repository's durable history uses squash merge by default. Preserve
individual commits only when their boundaries have lasting value for
reverting, migration sequencing, or bisecting. Do not force-push or merge
remotely without explicit authorization.

## Reporting security issues

Use [SECURITY.md](SECURITY.md) for vulnerability reports; do not disclose
secrets in issues or pull requests.
