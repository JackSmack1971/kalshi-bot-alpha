"""Load Kalshi demo credential material (Phase 1 PR 2).

This module is the sole reader of ``os.environ`` and the private-key
file for Kalshi credentials anywhere in this repository. It consumes a
:class:`~kalshi_bot.config.models.CredentialReferences` and produces a
:class:`LoadedDemoCredentials` -- an opaque type constructed only here.

This module also defines the narrow internal seam Phase 1 PR 3 uses to
build a signer from the loaded material: :func:`_build_request_signer`.
That function is not public (not in ``__all__``), takes no callback or
factory of any kind, and returns only a fully constructed
``kalshi_bot.auth.signer.RequestSigner`` -- never the raw access-key ID
or PEM bytes. Raw material crosses into ``kalshi_bot.auth.signer``
exactly once, inside this function, via a local import of that
module's private ``_RequestSignerBuilder``. REST and WebSocket clients
must depend only on the ``RequestSigner`` this function returns, never
on this seam or on ``LoadedDemoCredentials`` directly. See this
function's docstring for the explicit limits of this boundary: it is
architectural and convention-enforced, not a language-level security
guarantee.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

from kalshi_bot.config.models import CredentialReferences
from kalshi_bot.observability.logging import _register_sensitive_value

if TYPE_CHECKING:
    from kalshi_bot.auth.signer import RequestSigner

__all__ = ["CredentialLoadError", "LoadedDemoCredentials", "load_credentials"]


class CredentialLoadError(Exception):
    """Raised when Kalshi demo credential material cannot be loaded.

    The message names which reference (environment-variable name or
    file path) failed and why -- never the credential value itself.
    """


class LoadedDemoCredentials:
    """Opaque Kalshi demo credential material.

    Constructed only by :func:`load_credentials`. Exposes no public
    accessor for the access-key ID or private-key bytes; ``repr`` and
    ``str`` never include the material. Not iterable, not mappable,
    and not serializable (pickling raises). The only sanctioned
    conversion is :func:`_build_request_signer`, which returns a
    ``kalshi_bot.auth.signer.RequestSigner`` -- never the raw
    material itself. See that function's docstring for why this is an
    architectural and convention-enforced boundary, not a
    language-level guarantee.
    """

    __slots__ = ("_access_key_id", "_private_key_pem")

    def __init__(self, access_key_id: str, private_key_pem: bytes) -> None:
        self._access_key_id = access_key_id
        self._private_key_pem = private_key_pem

    def __repr__(self) -> str:
        return "LoadedDemoCredentials(<redacted>)"

    __str__ = __repr__

    def __reduce__(self) -> tuple[object, ...]:
        raise TypeError("LoadedDemoCredentials must not be pickled or serialized")


def _build_request_signer(credentials: LoadedDemoCredentials) -> RequestSigner:
    """Module-private seam: the sole path from credentials to a signer.

    Returns a fully constructed
    ``kalshi_bot.auth.signer.RequestSigner`` -- never the raw
    access-key ID or PEM bytes, and never a tuple, dict, or other
    reusable container of raw material. The raw material crosses into
    ``kalshi_bot.auth.signer`` exactly once, inside this call, via a
    local (function-scoped) import of that module's private
    ``_RequestSignerBuilder.from_raw_material``. The import is local
    rather than top-level to avoid a circular import: ``auth.signer``
    also depends on this module (for the ``LoadedDemoCredentials``
    type and to call this function from
    ``RequestSigner.from_credentials``), so neither module may import
    the other at module-load time.

    There is deliberately no callback or factory parameter anywhere in
    this path: a caller-supplied callback would let arbitrary code run
    with the raw material inside this module's frame, which is a
    strictly wider surface than this fixed, one-shot construction.

    **Limitations of this boundary, stated explicitly:**

    - Python's single-underscore naming is a convention, not an
      enforced access boundary. Nothing at the language level stops
      another module in this repository from importing and calling
      this function, or ``credentials._access_key_id`` /
      ``credentials._private_key_pem`` directly -- this protects
      against *accidental* misuse (an unrelated module reaching for
      credentials it should not touch), not against a *malicious*
      in-process caller, which Python cannot defend against once code
      runs in the same interpreter.
    - What actually restricts who calls this today is architecture
      (only ``kalshi_bot.credentials`` and ``kalshi_bot.auth`` have a
      legitimate reason to), import discipline, code review, and the
      static import-boundary test in
      ``tests/unit/test_credential_loader.py``, which asserts this
      name (and ``_RequestSignerBuilder``) is referenced nowhere
      outside those two packages -- not a runtime or language-level
      guarantee.
    - REST, WebSocket, and every other downstream module must depend
      only on the ``RequestSigner`` this function returns, never on
      this function, ``_RequestSignerBuilder``, or
      ``LoadedDemoCredentials`` directly.
    """
    from kalshi_bot.auth.signer import _RequestSignerBuilder

    return _RequestSignerBuilder.from_raw_material(
        credentials._access_key_id, credentials._private_key_pem
    )


def load_credentials(refs: CredentialReferences) -> LoadedDemoCredentials:
    """Load Kalshi demo credential material referenced by ``refs``.

    Fails closed with a typed :class:`CredentialLoadError` on any
    missing environment variable, missing file, directory path, or
    unreadable file -- never falls back to an unauthenticated mode.
    On success, registers the loaded access-key ID with the internal
    ``kalshi_bot.observability.logging._register_sensitive_value``
    hook so it is redacted if it ever reaches emitted log output.
    """
    access_key_id = os.environ.get(refs.access_key_env)
    if not access_key_id:
        raise CredentialLoadError(
            f"environment variable {refs.access_key_env!r} is not set"
        )

    key_path_str = os.environ.get(refs.private_key_path_env)
    if not key_path_str:
        raise CredentialLoadError(
            f"environment variable {refs.private_key_path_env!r} is not set"
        )

    key_path = Path(key_path_str)

    if key_path.is_dir():
        raise CredentialLoadError(
            f"private key path referenced by {refs.private_key_path_env!r} is a directory, "
            "not a file"
        )

    if not key_path.is_file():
        raise CredentialLoadError(
            f"private key file referenced by {refs.private_key_path_env!r} does not exist"
        )

    try:
        private_key_pem = key_path.read_bytes()
    except OSError as exc:
        raise CredentialLoadError(
            f"private key file referenced by {refs.private_key_path_env!r} could not be read"
        ) from exc

    if not private_key_pem.strip():
        raise CredentialLoadError(
            f"private key file referenced by {refs.private_key_path_env!r} is empty"
        )

    _register_sensitive_value(access_key_id)

    return LoadedDemoCredentials(access_key_id, private_key_pem)
