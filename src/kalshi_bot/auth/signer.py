"""Kalshi request signing per the documented RSA-PSS scheme (Phase 1 PR 3).

Grounded in the local official Kalshi documentation:
``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-getting-started-api-keys-425c8167.md``
and
``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-getting-started-quick-start-authenticated-requests-837b7955.md``.
Both worked Python examples agree on the scheme implemented here:

- Canonical message: ``str(timestamp_ms) + method + path`` (path without
  query parameters), UTF-8 encoded.
- Signature: RSA-PSS, ``MGF1(SHA-256)``, ``salt_length=PSS.DIGEST_LENGTH``,
  hash ``SHA-256``, base64-encoded.
- Headers: ``KALSHI-ACCESS-KEY`` (access-key ID), ``KALSHI-ACCESS-SIGNATURE``
  (base64 signature), ``KALSHI-ACCESS-TIMESTAMP`` (timestamp in
  milliseconds, as a decimal string).

**Route-prefix decision:** every worked example in the local docs signs a
path that happens to start with ``/trade-api/v2/`` (Kalshi's actual API
root), but neither document states that prefix as a requirement of the
*signing scheme* itself -- it is simply how Kalshi's real endpoints are
routed. This module therefore does not hard-code or enforce that
prefix; it only requires a nonempty, non-absolute, fragment-free path
starting with ``/``. Constructing the correct full path (including the
``/trade-api/v2`` root) is a transport-client concern, left to the
REST/WebSocket clients added in later Phase 1 PRs.

**2048-bit RSA key size** is enforced because the local FIX-authentication
doc (``docs-dev/kalshi-docs-pack/docs/docs-kalshi-com-fix-authentication-ade32229.md``)
states Kalshi API keys are 2048-bit RSA and are the same keypair used
for both REST and FIX.

No network, filesystem, or environment access occurs anywhere in this
module. ``RequestSigner`` is constructed only from an already-loaded
:class:`~kalshi_bot.credentials.loader.LoadedDemoCredentials` via
:meth:`RequestSigner.from_credentials`, which delegates to the
credential module's private
:func:`~kalshi_bot.credentials.loader._build_request_signer`. That
function is the sole caller of this module's private
:class:`_RequestSignerBuilder`, which is the sole place raw
access-key/PEM material is turned into a signer. Neither module
imports the other at module-load time (each uses a local, function-
scoped import of the other) to avoid a circular import while keeping
the dependency one-way in spirit: this module never reads raw
credential material except through ``_RequestSignerBuilder``.
"""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from kalshi_bot.observability.logging import _register_transient_sensitive_value

if TYPE_CHECKING:
    from kalshi_bot.credentials.loader import LoadedDemoCredentials

__all__ = ["RequestSigner", "SignedHeaders", "SigningError"]

_REQUIRED_RSA_KEY_SIZE_BITS = 2048

# Nonempty, uppercase-only HTTP method token. Kalshi's REST API only
# ever uses standard verbs (GET/POST/PUT/DELETE); this is a deliberate
# simplification of RFC 7230's full token grammar, not an attempt to
# accept every syntactically valid HTTP method.
_METHOD_TOKEN_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*$")


class SigningError(Exception):
    """Raised when a request cannot be signed or a key cannot be used.

    Messages never include raw private-key material, the access-key
    ID, the signature, or verbatim third-party library exception text
    (which can itself embed key-shaped detail).
    """


@dataclass(frozen=True, slots=True, repr=False)
class SignedHeaders:
    """The three headers Kalshi requires on every authenticated request.

    ``repr`` and ``str`` are fixed and redacted (never include
    ``access_key`` or ``signature``) so that logging this object
    directly -- including nested inside a dict or list, where
    structlog's JSON renderer falls back to ``repr()`` for values it
    cannot serialize natively -- cannot leak either value. Field
    access, equality, and immutability are unaffected; only the
    dataclass-generated ``__repr__`` is replaced.
    """

    access_key: str
    signature: str
    timestamp_ms: int

    def __repr__(self) -> str:
        return "SignedHeaders(<redacted>)"

    __str__ = __repr__


def _canonical_message(method: str, path: str, timestamp_ms: int) -> bytes:
    """Build the exact byte string Kalshi's signing scheme requires.

    Returns ``str(timestamp_ms) + method + path_without_query`` encoded
    as UTF-8. Raises :class:`SigningError` if any input is malformed;
    never silently normalizes ``method``'s case or ``path``'s
    percent-encoding.
    """
    if isinstance(timestamp_ms, bool) or not isinstance(timestamp_ms, int):
        raise SigningError("timestamp_ms must be an int, not bool or another type")
    if timestamp_ms <= 0:
        raise SigningError("timestamp_ms must be a positive number of milliseconds")

    if not isinstance(method, str) or not _METHOD_TOKEN_PATTERN.match(method):
        raise SigningError("method must be a nonempty uppercase HTTP token")

    if not isinstance(path, str) or not path:
        raise SigningError("path must be a nonempty string")
    if "#" in path:
        raise SigningError("path must not include a fragment")
    if path.startswith("//") or "://" in path:
        raise SigningError("path must not be an absolute URL")
    if not path.startswith("/"):
        raise SigningError("path must start with '/'")

    path_without_query = path.split("?", 1)[0]

    message = f"{timestamp_ms}{method}{path_without_query}"
    return message.encode("utf-8")


class _SignerConstructionToken:
    """Module-private sentinel gating :class:`RequestSigner` construction.

    Only :class:`_RequestSignerBuilder` holds a reference to the single
    instance below (``_CONSTRUCTION_TOKEN``). This is conventional
    Python encapsulation -- it stops *accidental* direct construction
    of ``RequestSigner`` (which would bypass ``_RequestSignerBuilder``'s
    key-size and type validation), not a language-level security
    boundary: any in-process code that imports this module can still
    reach ``_CONSTRUCTION_TOKEN`` directly. It restricts what supported,
    reviewed call sites do, the same way the single-underscore names
    throughout this module and ``kalshi_bot.credentials.loader`` do.
    """

    __slots__ = ()


_CONSTRUCTION_TOKEN = _SignerConstructionToken()


class RequestSigner:
    """Signs Kalshi requests with RSA-PSS. Holds the parsed private key.

    Constructed only via :meth:`from_credentials` (which delegates to
    :class:`_RequestSignerBuilder`). Opaque: ``repr`` and ``str`` never
    include key material; not pickled or serialized.
    """

    __slots__ = ("_access_key_id", "_private_key")

    def __init__(
        self,
        access_key_id: str,
        private_key: rsa.RSAPrivateKey,
        *,
        _construction_token: _SignerConstructionToken,
    ) -> None:
        """Construct a signer. Not a supported public entry point.

        Requires the private ``_construction_token`` sentinel that only
        :class:`_RequestSignerBuilder` supplies, so
        ``RequestSigner(access_key_id, private_key)`` called directly
        (without the keyword-only token) raises ``TypeError`` before
        this body runs, and a caller who does obtain the token still
        cannot bypass this constructor's own key-size and type
        validation -- it duplicates, rather than trusts,
        ``_RequestSignerBuilder``'s checks so that no path into a
        constructed ``RequestSigner`` skips them.
        """
        if _construction_token is not _CONSTRUCTION_TOKEN:
            raise TypeError(
                "RequestSigner must not be constructed directly; use "
                "RequestSigner.from_credentials() instead"
            )
        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise SigningError("only RSA private keys are supported")
        if private_key.key_size != _REQUIRED_RSA_KEY_SIZE_BITS:
            raise SigningError(
                f"Kalshi requires a {_REQUIRED_RSA_KEY_SIZE_BITS}-bit RSA key"
            )
        if not isinstance(access_key_id, str) or not access_key_id:
            raise SigningError("access_key_id must be a nonempty string")

        self._access_key_id = access_key_id
        self._private_key = private_key

    def __repr__(self) -> str:
        return "RequestSigner(<redacted>)"

    __str__ = __repr__

    def __reduce__(self) -> tuple[object, ...]:
        raise TypeError("RequestSigner must not be pickled or serialized")

    @classmethod
    def from_credentials(cls, credentials: LoadedDemoCredentials) -> RequestSigner:
        """Build a signer from already-loaded demo credential material.

        Delegates to the credential module's private
        ``_build_request_signer``, which is the only function that
        ever touches ``credentials``' raw fields. This classmethod
        never sees the raw access-key ID or PEM bytes itself. Raises a
        sanitized :class:`SigningError` for malformed, encrypted,
        unsupported, non-RSA, or wrong-size keys -- never including
        the raw PEM bytes, the access-key ID, or verbatim third-party
        exception text.
        """
        from kalshi_bot.credentials.loader import _build_request_signer

        return _build_request_signer(credentials)

    def sign(self, method: str, path: str, timestamp_ms: int) -> SignedHeaders:
        """Sign ``method``/``path``/``timestamp_ms`` and return the headers.

        Registers the resulting base64 signature with the internal
        bounded, expiring transient-redaction registry before
        returning, so it is redacted if it ever reaches emitted log
        output. Uses transient (not persistent) registration because a
        fresh signature is produced on every call: unlike the
        long-lived access-key ID, retaining every historical signature
        forever would grow the redaction registry and per-log-line
        redaction cost without bound over a long-running client's
        lifetime.
        """
        message = _canonical_message(method, path, timestamp_ms)

        signature_bytes = self._private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH,
            ),
            hashes.SHA256(),
        )
        signature_b64 = base64.b64encode(signature_bytes).decode("ascii")

        _register_transient_sensitive_value(signature_b64)

        return SignedHeaders(
            access_key=self._access_key_id,
            signature=signature_b64,
            timestamp_ms=timestamp_ms,
        )


class _RequestSignerBuilder:
    """Private, non-exported seam: the only place raw credential
    material is parsed into a :class:`RequestSigner`.

    Not in ``__all__`` and not importable as part of this package's
    public surface -- reserved for
    ``kalshi_bot.credentials.loader._build_request_signer``, which is
    itself the only caller of :meth:`from_raw_material`. This class
    takes raw material as constructor *arguments* (never returns it),
    so raw values cross the module boundary exactly once, during this
    fixed construction step, and are never handed back out.
    """

    @staticmethod
    def from_raw_material(access_key_id: str, private_key_pem: bytes) -> RequestSigner:
        """Parse ``private_key_pem`` and return a :class:`RequestSigner`.

        Raises a sanitized :class:`SigningError` for malformed,
        encrypted, unsupported, non-RSA, or wrong-size keys -- never
        including the raw PEM bytes, the access-key ID, or verbatim
        third-party exception text.
        """
        try:
            private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        except TypeError:
            raise SigningError(
                "private key material is encrypted; encrypted keys are not supported"
            ) from None
        except ValueError:
            raise SigningError("private key material is malformed or empty") from None
        except UnsupportedAlgorithm:
            raise SigningError(
                "private key material uses an unsupported key format or algorithm"
            ) from None

        if not isinstance(private_key, rsa.RSAPrivateKey):
            raise SigningError("only RSA private keys are supported")

        if private_key.key_size != _REQUIRED_RSA_KEY_SIZE_BITS:
            raise SigningError(
                f"Kalshi requires a {_REQUIRED_RSA_KEY_SIZE_BITS}-bit RSA key"
            )

        return RequestSigner(
            access_key_id, private_key, _construction_token=_CONSTRUCTION_TOKEN
        )
