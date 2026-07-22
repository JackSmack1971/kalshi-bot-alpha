"""Canonical structured logging with global secret redaction (Phase 1 PR 2).

This is the permanent logging interface for the repository, not a
temporary stub: every logger, structlog-bound or stdlib/third-party,
is wired through the same processor chain so that access-key IDs,
signatures, authorization headers, and private-key material can never
reach emitted output, per ``docs/PHASE1_PLAN.md`` PR 2 and
``.claude/rules/credential-privacy.md``.

Redaction combines three narrow, precise mechanisms rather than a
broad content scan:

1. Recursive **exact-key** redaction over dict/list-shaped event data
   -- a fixed set of known-sensitive field names (``access_key``,
   ``signature``, ``authorization``, ``private_key``, ``api_key``,
   ``secret``, ``password``, ``token``, ``bearer_token``, and their
   documented variants), matched by normalized exact name so that
   legitimate fields such as ``input_token_count`` or ``secretary_id``
   are never caught by accident.
2. A narrow **PEM-block marker scan** (``-----BEGIN ...-----`` /
   ``-----END ...-----``) over string values and rendered exception
   text, so private-key material embedded in a message or traceback is
   still caught.
3. **Exact registered sensitive values**, split into two registries so
   a long-running client's memory and per-log-line redaction cost stay
   bounded:

   - **Persistent** values (the loaded access-key ID, registered by
     ``kalshi_bot.credentials.loader``) are few, long-lived for the
     process, and registered once via the private
     ``_register_sensitive_value`` hook.
   - **Transient** values (the per-request RSA-PSS signature computed
     by ``kalshi_bot.auth.signer``) are registered via the private
     ``_register_transient_sensitive_value`` hook in a bounded,
     time-expiring registry: entries older than
     ``_TRANSIENT_VALUE_TTL_SECONDS`` are pruned, and the registry
     never grows past ``_MAX_TRANSIENT_VALUES`` entries (oldest
     evicted first), so a client that signs many requests over a long
     session does not retain every historical signature forever.

   Both registries are redacted wherever their values appear in
   emitted text, including free-form messages and exception text,
   across both structlog and stdlib/third-party logging paths.
   Registration is internal, not a public production API: only the
   credential-loading and signing boundaries register values.

There is intentionally no generic base64/hex value-shape regex: that
would also redact legitimate hashes, IDs, and evidence values that are
not secrets.
"""

from __future__ import annotations

import logging
import re
import threading
import time
from collections.abc import Mapping, MutableMapping
from typing import IO, Any

import structlog

__all__ = ["configure_logging", "get_logger"]

# Exact, normalized (lowercase, hyphens -> underscores) field names
# redacted regardless of nesting depth. Deliberately not substring or
# generic-suffix matching: "token_budget", "input_token_count", and
# "secretary_id" must never be redacted, so only names identical to an
# entry below (after normalization) match.
_SENSITIVE_EXACT_KEYS: frozenset[str] = frozenset(
    {
        "access_key",
        "access_key_id",
        "api_key",
        "authorization",
        "authorization_header",
        "signature",
        "private_key",
        "private_key_pem",
        "password",
        "secret",
        "token",
        "bearer",
        "bearer_token",
    }
)

_PEM_BLOCK_PATTERN = re.compile(
    r"-----BEGIN [A-Z0-9 ]+-----.*?-----END [A-Z0-9 ]+-----",
    re.DOTALL,
)

_REDACTED = "[REDACTED]"
_REDACTED_PEM = "[REDACTED-PEM]"

# Minimum length for a registered sensitive value before it is used for
# substring redaction. Short values would over-match unrelated text;
# real access-key IDs and signatures are always well above this length.
_MIN_REGISTERED_VALUE_LENGTH = 8

# Conservative Phase 1 constants for the transient (per-request-signature)
# registry. A signature is only ever needed for redaction while a request
# it was computed for might still appear in in-flight logs; 10 minutes and
# 4096 entries comfortably outlast any single request's log lifetime while
# keeping worst-case memory and per-log-line redaction cost bounded for a
# long-running client. Module-private: not user configuration in PR 3.
_TRANSIENT_VALUE_TTL_SECONDS = 600.0
_MAX_TRANSIENT_VALUES = 4096

_registry_lock = threading.Lock()

# Long-lived values (e.g. the access-key ID): retained for process
# lifetime, deduplicated by set membership.
_persistent_sensitive_values: set[str] = set()

# Short-lived values (e.g. a per-request signature): value -> monotonic
# expiry time. A plain dict is used (not a set) so each entry carries its
# own expiry, and insertion order is preserved so the oldest entry can be
# evicted first when the registry is at capacity.
_transient_sensitive_values: dict[str, float] = {}


def _monotonic() -> float:
    """Indirection point so tests can inject a deterministic clock.

    Real code always resolves this to :func:`time.monotonic`; tests may
    monkeypatch this module attribute to advance time without sleeping.
    Monotonic time is used (not wall-clock time) so registry expiry is
    unaffected by system clock adjustments.
    """
    return time.monotonic()


def _prune_expired_transient_values_locked(now: float) -> None:
    """Remove expired transient entries. Caller must hold ``_registry_lock``."""
    expired = [value for value, expires_at in _transient_sensitive_values.items() if expires_at <= now]
    for value in expired:
        del _transient_sensitive_values[value]


def _register_sensitive_value(value: str) -> None:
    """Register a long-lived exact runtime secret value for redaction.

    Internal hook, not part of the public ``kalshi_bot.observability``
    API (not in ``__all__``, not re-exported from ``__init__.py``).
    ``kalshi_bot.credentials.loader`` imports this function directly
    because it is the sole credential-loading boundary; no other
    module should call it without an equivalent narrow justification.
    For values that change on every call (such as a computed request
    signature), use :func:`_register_transient_sensitive_value`
    instead -- this persistent registry never expires or evicts
    entries, so it must only ever hold a small, fixed number of
    long-lived values such as the access-key ID.

    Call this once, immediately after loading or computing a real
    secret value -- for example the access-key ID returned by
    :func:`kalshi_bot.credentials.loader.load_credentials` -- and
    never log the value yourself in the interim. Once registered, the
    exact value is redacted wherever it appears in emitted output:
    plain messages, exception text, and nested structures, across both
    structlog and stdlib/third-party logging paths.

    Registered values cannot be read back through this module; there
    is no accessor. Values shorter than
    ``_MIN_REGISTERED_VALUE_LENGTH`` characters are ignored (too short
    to safely value-redact without over-matching unrelated text), as
    are empty or whitespace-only values. Registering the same value
    more than once is harmless (the registry is a set).
    """
    if not value or not value.strip() or len(value) < _MIN_REGISTERED_VALUE_LENGTH:
        return
    with _registry_lock:
        _persistent_sensitive_values.add(value)


def _register_transient_sensitive_value(value: str) -> None:
    """Register a short-lived exact runtime secret value for redaction.

    Internal hook, not part of the public ``kalshi_bot.observability``
    API (not in ``__all__``, not re-exported from ``__init__.py``).
    ``kalshi_bot.auth.signer`` imports this function directly because
    it is the sole per-request-signature boundary; no other module
    should call it without an equivalent narrow justification.

    Unlike :func:`_register_sensitive_value`, entries registered here
    expire after ``_TRANSIENT_VALUE_TTL_SECONDS`` of monotonic time and
    the registry never holds more than ``_MAX_TRANSIENT_VALUES``
    entries -- the oldest entry is evicted first once that capacity is
    exceeded. Expired entries are pruned both here (on registration)
    and whenever a redaction snapshot is taken, so a long-running
    client that signs many requests does not retain every historical
    signature forever, and the per-log-line redaction scan does not
    grow unbounded.

    Registered values cannot be read back through this module; there
    is no accessor. Values shorter than
    ``_MIN_REGISTERED_VALUE_LENGTH`` characters are ignored, as are
    empty or whitespace-only values. Registering the same value more
    than once is harmless and does not reset its original expiry or
    eviction order.
    """
    if not value or not value.strip() or len(value) < _MIN_REGISTERED_VALUE_LENGTH:
        return
    now = _monotonic()
    with _registry_lock:
        _prune_expired_transient_values_locked(now)
        if value not in _transient_sensitive_values:
            _transient_sensitive_values[value] = now + _TRANSIENT_VALUE_TTL_SECONDS
            while len(_transient_sensitive_values) > _MAX_TRANSIENT_VALUES:
                oldest_value = next(iter(_transient_sensitive_values))
                del _transient_sensitive_values[oldest_value]


def _reset_registered_sensitive_values_for_tests() -> None:
    """Test-only: clear both registries so tests do not leak across cases.

    Not part of the public API (not in ``__all__``); import it
    directly from this module only from test fixtures.
    """
    with _registry_lock:
        _persistent_sensitive_values.clear()
        _transient_sensitive_values.clear()


def _transient_registry_size_for_tests() -> int:
    """Test-only: return the current transient-registry entry count.

    Not part of the public API (not in ``__all__``); exists solely so
    tests can assert capacity/eviction behavior without a public
    inspection API.
    """
    with _registry_lock:
        return len(_transient_sensitive_values)


def _is_sensitive_key(key: str) -> bool:
    normalized = key.strip().lower().replace("-", "_")
    return normalized in _SENSITIVE_EXACT_KEYS


def _redact_string(value: str) -> str:
    if _PEM_BLOCK_PATTERN.search(value):
        value = _PEM_BLOCK_PATTERN.sub(_REDACTED_PEM, value)

    now = _monotonic()
    with _registry_lock:
        _prune_expired_transient_values_locked(now)
        snapshot = tuple(_persistent_sensitive_values) + tuple(_transient_sensitive_values)
    # Lock released before scanning: redaction never holds the lock
    # while running string replacement, so a concurrent registration
    # or reset cannot block or race with in-flight log rendering. This
    # keeps the scan itself proportional to the registries' bounded
    # size (persistent values are few; transient values are capped at
    # _MAX_TRANSIENT_VALUES and pruned of expired entries above), not
    # to every signature ever computed over the process lifetime.

    # Longest-first: if one registered value is a prefix/substring of
    # another (e.g. an older and a rotated access-key ID that happen to
    # share a prefix), redacting the shorter one first would leave the
    # longer value's unmatched suffix behind as plaintext. Processing
    # longest-first guarantees the full longer value is replaced before
    # any shorter value could partially match inside it.
    for secret_value in sorted(snapshot, key=len, reverse=True):
        if secret_value in value:
            value = value.replace(secret_value, _REDACTED)
    return value


def _redact_value(value: Any) -> Any:
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, Mapping):
        return _redact_mapping(value)
    if isinstance(value, (list, tuple)):
        return type(value)(_redact_value(item) for item in value)
    return value


def _redact_mapping(mapping: Mapping[Any, Any]) -> dict[Any, Any]:
    redacted: dict[Any, Any] = {}
    for key, value in mapping.items():
        if isinstance(key, str) and _is_sensitive_key(key):
            redacted[key] = _REDACTED
        else:
            redacted[key] = _redact_value(value)
    return redacted


def _redact_processor(
    logger: Any, method_name: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    return _redact_mapping(event_dict)


def _build_shared_processors() -> list[Any]:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.ExtraAdder(),
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        _redact_processor,
    ]


def configure_logging(level: str = "INFO", *, stream: IO[str] | None = None) -> None:
    """Configure the one canonical, redacted, JSON-structured logging pipeline.

    Wires ``structlog``-bound loggers and stdlib/third-party
    ``logging.Logger`` records through the identical processor chain
    (including ``_redact_processor``), so no logging path in the
    process can bypass redaction.

    ``stream`` is exposed only so tests can capture rendered output
    without touching internals; production callers should omit it.
    """
    resolved_level = getattr(logging, level.upper(), logging.INFO)
    shared_processors = _build_shared_processors()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(stream) if stream is not None else logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(resolved_level)


def get_logger(name: str) -> Any:
    """Return a logger built from the canonical configured pipeline.

    Callers must never construct a logger any other way (no
    ``logging.getLogger`` call sites, no ``print``) so nothing bypasses
    ``configure_logging``'s redaction wiring.
    """
    return structlog.get_logger(name)
