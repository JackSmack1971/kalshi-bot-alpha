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


## Observable workflow and telemetry

Create exactly one telemetry run per Skill invocation. Start with `python .codex/scripts/skill_telemetry.py start <skill> invocation_started --reason-code <reason>` and capture the returned `run_id`. Reuse that same `run_id` for every `emit` event and for `finish <skill> invocation_finished --run-id <id> --outcome <terminal>`. Never generate a new run ID for each event. When an execution snapshot or UoW ID exists, attach it to the same run. Emit only the consequential events below; do not log generic tool calls, prompts, transcripts, secrets, or arbitrary model prose.

Declared events: `check_selected`, `check_result`, `required_check_skipped`, `credential_gate`, `final_verdict`.

Completion requires the workflow report, objective evidence, and a terminal telemetry record. If a required tool, worker, policy, or evidence source fails, record the relevant event with failed or blocked, preserve the failure, and stop or report the unresolved gap; never convert missing evidence into a pass.
