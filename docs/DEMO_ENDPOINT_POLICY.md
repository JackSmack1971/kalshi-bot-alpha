# Demo Endpoint Policy

## Policy

Only these two Kalshi endpoints are ever permitted by this codebase:

```text
REST:      https://external-api.demo.kalshi.co/trade-api/v2
WebSocket: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2
```

Every non-demo hostname is rejected. This is a hard-coded, immutable
constant policy, never a configuration value. There is no
environment-selector abstraction, no `KALSHI_ENV`, no
`environment: str` parameter, and no generic
`KalshiClient(environment=...)` shape anywhere in this repository,
including as illustrative documentation text.

## Enforcement in Phase 0

`src/kalshi_bot/contracts/demo_endpoints.py` defines:

- `DEMO_REST_HOST = "external-api.demo.kalshi.co"`
- `DEMO_WS_HOST = "external-api-ws.demo.kalshi.co"`
- `ALLOWED_DEMO_HOSTS` — the immutable two-element allowlist.
- `validate_host(host: str) -> bool` — a pure, side-effect-free
  predicate performing an exact, case-sensitive string match against
  the allowlist. No I/O, no DNS resolution, no client construction.

`validate_host` intentionally performs **no normalization**: it does
not lowercase or strip its input before comparing. This means
case-variant and whitespace-padded values are rejected rather than
silently accepted, closing off a class of smuggling attempt where an
attacker relies on the validator "helpfully" normalizing a
look-alike host into an accepted one.

`tests/test_demo_endpoint_policy.py` proves rejection of:

- Production-looking hostnames (`api.kalshi.co`, `trading-api.kalshi.co`, etc.).
- Empty and malformed strings, non-string input.
- Case-variant smuggling attempts (`EXTERNAL-API.DEMO.KALSHI.CO`).
- Whitespace-variant smuggling attempts (leading/trailing space, tabs, newlines).
- Hosts that graft a demo-looking prefix onto a non-demo suffix or vice
  versa (`external-api.demo.kalshi.co.evil.com`).

## Required fail-closed controls (binding on later phases)

Once a runtime exists, the bot must refuse to start when:

- A configured host is not on the demo allowlist.
- A production hostname appears anywhere in runtime configuration.
- Credentials are absent, malformed, or sourced from an unsafe location.
- Environment mode is unset or ambiguous.
- System time drift exceeds the configured authentication tolerance.
- A strategy attempts to bypass the central execution gateway.
- Persistent state indicates an unresolved prior shutdown or
  reconciliation failure.

## Production isolation (binding on later phases)

Use a demo-specific transport implementation, for example
`KalshiDemoRestClient` and `KalshiDemoWebSocketClient`. Do not
implement a generic, environment-parameterized client. This makes
accidental production enablement require an explicit architectural
change — a new class, a new ADR, a new review — rather than a
configuration typo or an added enum value.

## Non-goals of this phase

No REST or WebSocket client exists yet. This policy and its executable
validator exist so that the demo-only invariant is provable before any
transport code is written, per blueprint Phase 0 exit criterion
"Production endpoints are explicitly forbidden."
