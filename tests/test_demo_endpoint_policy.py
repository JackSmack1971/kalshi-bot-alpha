"""Tests for the demo-only endpoint allowlist (blueprint SS2.1).

Proves, executably, that production endpoints are forbidden and that
only the two exact Kalshi demo hostnames are ever accepted.
"""

from __future__ import annotations

import pytest

from kalshi_bot.contracts.demo_endpoints import (
    ALLOWED_DEMO_HOSTS,
    DEMO_REST_HOST,
    DEMO_WS_HOST,
    validate_host,
)


def test_allowlist_contains_exactly_the_two_demo_hosts() -> None:
    assert ALLOWED_DEMO_HOSTS == {
        "external-api.demo.kalshi.co",
        "external-api-ws.demo.kalshi.co",
    }


def test_demo_rest_host_constant_is_exact() -> None:
    assert DEMO_REST_HOST == "external-api.demo.kalshi.co"


def test_demo_ws_host_constant_is_exact() -> None:
    assert DEMO_WS_HOST == "external-api-ws.demo.kalshi.co"


@pytest.mark.parametrize("host", ["external-api.demo.kalshi.co", "external-api-ws.demo.kalshi.co"])
def test_validate_host_accepts_exact_demo_hosts(host: str) -> None:
    assert validate_host(host) is True


@pytest.mark.parametrize(
    "host",
    [
        # Production-looking hostnames.
        "api.kalshi.co",
        "trading-api.kalshi.co",
        "external-api.kalshi.co",
        "external-api-ws.kalshi.co",
        "kalshi.co",
        "www.kalshi.co",
        # Empty / malformed.
        "",
        " ",
        "not a host",
        "http://external-api.demo.kalshi.co",
        "external-api.demo.kalshi.co/trade-api/v2",
        "external-api.demo.kalshi.co:443",
        None,
        123,
        b"external-api.demo.kalshi.co",
        # Case-variant smuggling attempts.
        "EXTERNAL-API.DEMO.KALSHI.CO",
        "External-Api.Demo.Kalshi.Co",
        "EXTERNAL-API-WS.DEMO.KALSHI.CO",
        # Whitespace-variant smuggling attempts.
        " external-api.demo.kalshi.co",
        "external-api.demo.kalshi.co ",
        "\texternal-api.demo.kalshi.co",
        "external-api.demo.kalshi.co\n",
        # Demo-looking prefix grafted onto a non-demo suffix, or vice versa.
        "external-api.demo.kalshi.co.evil.com",
        "evil.com.external-api.demo.kalshi.co",
        "external-api.demo.kalshi.co.attacker.net",
        "external-api-ws.demo.kalshi.co.attacker.net",
        "sub.external-api.demo.kalshi.co",
        "external-api.demo.kalshi.co-attacker.net",
    ],
)
def test_validate_host_rejects_non_demo_and_smuggling_attempts(host: object) -> None:
    assert validate_host(host) is False  # type: ignore[arg-type]
