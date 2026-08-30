---
name: control-plane-change
description: Use only when the user explicitly asks for multi-agent author-and-verify work on this Codex CLI control plane: AGENTS.md, .codex policies/config/agents/hooks/control-plane files, or .agents skills. Routes to the correct control-plane specialist, authors within its owned write set, then uses an independent read-only verifier. Never for application code under src/.
---

# Multi-agent Codex control-plane change

Read `.codex/control-plane/manifest.json` first.

## Route

Classify the request to exactly one primary owner:

- `rules-specialist`: `AGENTS.md`, `.codex/policies/**`, policy resolver and its tests.
- `skills-specialist`: reusable non-orchestration `.agents/skills/**`.
- `workflow-specialist`: `.codex/agents/**`, `.codex/config.toml`, hooks/control-plane infrastructure, and orchestration skills listed in the manifest.

If the request necessarily crosses owners, stop pretending it is single-owner: produce an ordered multi-owner plan and process one bounded owner transaction at a time, verifying each before the next.

## Author

Spawn the selected specialist with the original request and exact target files. Require the smallest coherent change and prohibit files outside the manifest-owned write set.

## Verify

After the author returns, spawn `control-plane-verifier`. It is independent and read-only. Give it the original request, target write set, and resulting diff/evidence. It must return PASS, FAIL, or INDETERMINATE and must not repair the change.

A FAIL or INDETERMINATE verdict blocks completion. Do not ask the author to self-certify. Run `.codex/scripts/validate_control_plane.py` before reporting PASS.
