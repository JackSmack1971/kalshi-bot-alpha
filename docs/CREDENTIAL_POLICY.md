# Credential Policy

## Process isolation model (blueprint SS2.2, SS2.3)

```text
paper-trader process:
  KALSHI_DEMO_ACCESS_KEY
  KALSHI_DEMO_PRIVATE_KEY_PATH
  no OPENROUTER_API_KEY required

agent-control-plane process:
  OPENROUTER_API_KEY
  no Kalshi credentials
  read-only sanitized evidence access
```

The trading process may receive Kalshi demo credentials but must never
require `OPENROUTER_API_KEY`. The agent process may receive
`OPENROUTER_API_KEY` but must never receive Kalshi credentials,
authentication material, or execution capabilities. If process
separation is temporarily unavailable in some future deployment,
equivalent operating-system and application-level controls must prove
that the agent runtime cannot read Kalshi secrets or invoke execution
capabilities — that proof is a review gate, not a default assumption.

## Handling rules (binding on every later phase)

Use:

- Environment variables or an operating-system secret store.
- A demo-only API key.
- A local private-key file kept outside the repository.
- File permissions restricted to the current user.
- Redaction of access-key identifiers and signatures from logs.

Never:

- Commit keys.
- Paste keys into prompts.
- Store keys in strategy configuration.
- Return signatures in error telemetry.
- Expose credentials through a dashboard or frontend process.

Kalshi authenticated requests require an access-key ID, an RSA-PSS
request signature, and a millisecond timestamp; none of these may
appear in logs, prompts, fixtures, snapshots, or AI evidence bundles.

## AI-agent credential boundary (blueprint SS2.3)

AI agents must never:

- Access Kalshi API credentials, private keys, signatures, or raw
  authentication headers.
- Execute arbitrary shell commands or arbitrary SQL.

The agent subsystem must refuse a request when prompt-egress scanning
detects credentials, signatures, private-key material, raw environment
dumps, or prohibited personal data.

## Phase 0 scope

This phase reads, requests, and stores no credentials of any kind. No
environment variable is read by any code in this repository. This
document fixes the policy that all later phases — starting with
whichever phase first constructs a Kalshi transport client or an
OpenRouter client — must implement before touching real credential
material.

## Non-goals of this phase

No secret loading, no environment-variable reads, no credential
validation code, and no OpenRouter client configuration (model
routing, API-key env-var binding) exist in this repository as of
Phase 0.
