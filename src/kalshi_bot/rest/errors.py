"""Typed error hierarchy for the Kalshi demo REST client (Phase 1 PR 4).

Every error message here is deliberately narrow: operation name, HTTP
status code, attempt/page counters, and (for response-validation
failures) a sanitized pydantic error summary built the same way
``kalshi_bot.config.loader._sanitize_validation_error`` does --
field location, the stable pydantic error-type code, and pydantic's
fixed message template. No message anywhere in this module ever
includes an authorization header, access-key ID, signature, complete
request headers, a raw response body, or a verbatim third-party
exception's ``str()``/``repr()`` (which can itself embed header- or
body-shaped detail this client does not control).
"""

from __future__ import annotations

__all__ = [
    "KalshiRestError",
    "DemoHostValidationError",
    "OperationNotAllowedError",
    "TransportExhaustedError",
    "KalshiApiError",
    "KalshiAuthError",
    "ResponseDecodeError",
    "ResponseValidationError",
    "PaginationError",
]


class KalshiRestError(Exception):
    """Base for every error raised by :mod:`kalshi_bot.rest`.

    Catching this catches every failure mode the demo REST client can
    produce. Never carries credential-bearing or full-response-body
    text -- see the module docstring for the exact policy.
    """


class DemoHostValidationError(KalshiRestError):
    """Raised if the fixed demo REST host ever fails ``validate_host``.

    This should be unreachable in ordinary operation: the host passed
    to ``validate_host`` is the same ``DEMO_REST_HOST`` constant that
    function checks against. The check still runs, unconditionally, at
    :class:`~kalshi_bot.rest.client.KalshiDemoRestClient` construction
    time -- before any ``httpx.Client`` or socket is created -- per
    ``.claude/rules/kalshi-transport-safety.md``'s requirement that
    demo-host validation happen before any I/O, and so that a future
    edit that ever loosens this constant fails closed instead of
    silently constructing a client against an unvalidated host.
    """


class OperationNotAllowedError(KalshiRestError):
    """Raised when a request would violate the read-only operation allowlist.

    Covers a non-``GET`` HTTP method, an absolute-URL request path, and
    any path that is not exactly one of the three allowlisted read-only
    operation paths. Raised by an internal policy gate before any
    transport execution -- this client has no public method through
    which a caller could ever trigger this today (there is no generic
    ``request(method, path)`` entry point), but the gate itself is
    still an explicit, independently testable check, not merely "we
    never call it."
    """


class TransportExhaustedError(KalshiRestError):
    """Raised when every configured retry attempt has been exhausted.

    Carries only the operation name and the number of attempts made --
    never the underlying transport exception's full text, which can
    embed connection-string or header detail this client does not
    control.
    """


class KalshiApiError(KalshiRestError):
    """Raised for a non-2xx, non-auth, non-retryable-exhausted HTTP response.

    Carries only the operation name and the HTTP status code -- never
    the raw response body.
    """

    def __init__(self, operation: str, status_code: int) -> None:
        self.operation = operation
        self.status_code = status_code
        super().__init__(f"{operation}: HTTP {status_code}")


class KalshiAuthError(KalshiRestError):
    """Raised for a 401 or 403 response. Never retried.

    Carries only the operation name and the HTTP status code -- never
    any header or body content that might have accompanied the
    authentication failure.
    """

    def __init__(self, operation: str, status_code: int) -> None:
        self.operation = operation
        self.status_code = status_code
        super().__init__(f"{operation}: authentication failed with HTTP {status_code}")


class ResponseDecodeError(KalshiRestError):
    """Raised when a 2xx response body cannot be decoded as JSON.

    Never includes the raw (non-JSON) response text, which is
    unstructured and could contain anything.
    """


class ResponseValidationError(KalshiRestError):
    """Raised when a decoded JSON response fails schema validation.

    Carries only a sanitized summary (field location, pydantic error
    type, pydantic's fixed message template) -- never the rejected
    field values themselves, which come from the network and are not
    controlled by this client.
    """


class PaginationError(KalshiRestError):
    """Raised for a pagination invariant violation.

    Covers a repeated cursor, exceeding the maximum page count, and a
    duplicate market ticker observed across pages. Raising this error
    always means the caller receives no partial list: pagination
    invariant failures never surface a silently truncated result.
    """
