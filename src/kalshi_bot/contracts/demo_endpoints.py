"""Demo-only endpoint allowlist (blueprint SS2.1).

This module is the single narrow exception to "no trading code" in
Phase 0. It is pure and side-effect-free: two immutable hostname
constants and a deterministic validator. It performs no I/O, opens no
socket or file, constructs no HTTP or WebSocket client, and contains no
strategy, risk, execution, reconciliation, or ledger logic.

The two hostnames below are the *only* Kalshi endpoints ever permitted
by this codebase:

    REST:      https://external-api.demo.kalshi.co/trade-api/v2
    WebSocket: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2

They are hard-coded constants, never configuration. Phase 0 must not
introduce an environment-selector, mode flag, or config key that could
route to a non-demo or production host (see
docs/DEMO_ENDPOINT_POLICY.md and docs/CREDENTIAL_POLICY.md).
"""

from __future__ import annotations

__all__ = ["DEMO_REST_HOST", "DEMO_WS_HOST", "ALLOWED_DEMO_HOSTS", "validate_host"]

#: The only permitted Kalshi demo REST hostname.
DEMO_REST_HOST: str = "external-api.demo.kalshi.co"

#: The only permitted Kalshi demo WebSocket hostname.
DEMO_WS_HOST: str = "external-api-ws.demo.kalshi.co"

#: Immutable allowlist of every hostname this codebase may ever contact.
ALLOWED_DEMO_HOSTS: frozenset[str] = frozenset({DEMO_REST_HOST, DEMO_WS_HOST})


def validate_host(host: str) -> bool:
    """Return ``True`` only if ``host`` is exactly one of the two demo hosts.

    This check is intentionally strict and fail-closed:

    - Comparison is an exact, case-sensitive string match against the
      immutable allowlist. No lowercasing, stripping, or normalization
      is performed, so case-variant and whitespace-padded smuggling
      attempts (for example ``"EXTERNAL-API.DEMO.KALSHI.CO"`` or
      ``" external-api.demo.kalshi.co"``) are rejected rather than
      silently accepted.
    - Any value that is not exactly one of the two allowed hostnames is
      rejected, including production-looking hostnames, empty strings,
      malformed hosts, and hosts that merely embed a demo-looking
      prefix or suffix (for example a value that starts with an allowed
      demo hostname but continues with additional, attacker-controlled
      labels).
    - Non-string input is rejected rather than raising, so callers in a
      fail-closed startup path can treat this function as a pure
      predicate.

    This function performs no I/O and makes no network, DNS, or client
    calls; it is a pure string comparison.
    """
    if not isinstance(host, str):
        return False
    return host in ALLOWED_DEMO_HOSTS
