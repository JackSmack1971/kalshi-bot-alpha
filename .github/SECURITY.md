# Security Policy

## Scope

This repository contains a deterministic, demo-only Kalshi paper-trading
system. It must never be used to access production Kalshi endpoints or to
store credentials in the repository.

## Reporting a vulnerability

Please do not open a public issue for a suspected vulnerability. Report it
privately through GitHub's security advisory reporting flow for this
repository, or contact the repository owner through the GitHub account
`@JackSmack1971`. Include reproduction steps, affected paths, and impact,
but never include live credentials or private keys.

## Credential handling

- Never commit `.env` files, API keys, private keys, tokens, or credentials.
- Kalshi credentials are demo-only and process-isolated from the AI control
  plane.
- OpenRouter credentials must never be provided to the trading process.
- If a credential may have been exposed, revoke and rotate it immediately.

## Safe development

Run the repository verification commands in `CONTRIBUTING.md`, including the
demo-only endpoint scanner, before submitting a change.
