---
paths:
  - "src/agents/**/*.py"
  - "src/openrouter/**/*.py"
  - "src/agent_tools/**/*.py"
  - "src/evidence/**/*.py"
  - "src/proposals/**/*.py"
  - "tests/agents/**/*.py"
  - "tests/openrouter/**/*.py"
  - "tests/privacy/**/*.py"
  - "tests/adversarial/**/*.py"
---

# OpenRouter and agent governance

OpenRouter is the sole external inference provider. Do not add direct Anthropic, OpenAI, Google, xAI, or other vendor SDKs or clients.

The application-owned gateway must centralize authentication, model policy, provider routing, privacy controls, capability validation, timeout and retry policy, structured outputs, tool validation, evidence scoping, token/cost budgets, provenance, telemetry, redaction, and prompt-egress scanning.

Before changing OpenRouter behavior, verify current official OpenRouter documentation because capabilities, routing, fallback, and privacy controls can change.

Required behavior:

- Use pinned, reviewed model policies.
- Fail closed when required capabilities are unavailable.
- Reject unapproved fallback for authoritative workflows.
- Validate structured outputs strictly; reject unknown fields and evidence IDs.
- Record requested and actual model/provider metadata.
- Enforce tool and evidence scopes.
- Store outputs only in isolated proposal paths.
- Keep conclusions non-binding until required review.
- Never expose shell, arbitrary SQL, raw filesystem traversal, Kalshi transport, secret loading, ledger mutation, active configuration, or approval capabilities.
- Treat structured output as shape validation, not truth.
- Test schema failures, evidence-scope failures, prompt injection, secret egress, unapproved fallback, and agent-to-execution isolation.
