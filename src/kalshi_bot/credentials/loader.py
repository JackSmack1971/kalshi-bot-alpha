"""Load Kalshi demo credential material (Phase 1 PR 2).

This module is the sole reader of ``os.environ`` and the private-key
file for Kalshi credentials anywhere in this repository. It consumes a
:class:`~kalshi_bot.config.models.CredentialReferences` and produces a
:class:`LoadedDemoCredentials` -- an opaque type constructed only here.

Phase 1 PR 2 does not construct a signing capability or implement any
cryptography. It does define the narrow internal seam Phase 1 PR 3
will use to build a ``RequestSigner`` from the loaded material:
:func:`_reveal_for_signer_construction`. That function is not public
(not in ``__all__``), takes a caller-supplied factory rather than
returning the raw material directly, and is documented as reserved for
``kalshi_bot.auth.signer`` alone -- REST and WebSocket clients must
depend only on the signer, never on this seam or on
``LoadedDemoCredentials`` directly. See that function's docstring for
the explicit limits of this boundary: it is architectural and
convention-enforced, not a language-level security guarantee.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from kalshi_bot.config.models import CredentialReferences
from kalshi_bot.observability.logging import _register_sensitive_value

__all__ = ["CredentialLoadError", "LoadedDemoCredentials", "load_credentials"]

_T = TypeVar("_T")


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
    and not serializable (pickling raises) -- the only sanctioned way
    to reach the underlying material is
    :func:`_reveal_for_signer_construction`, reserved for Phase 1 PR
    3's signer construction. See that function's docstring for why
    this is an architectural and convention-enforced boundary, not a
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


def _reveal_for_signer_construction(
    credentials: LoadedDemoCredentials, factory: Callable[[str, bytes], _T]
) -> _T:
    """Module-private seam for Phase 1 PR 3's signer construction only.

    ``factory`` receives the access-key ID and private-key PEM bytes
    and must return a signing-capability object (Phase 1 PR 3's
    ``kalshi_bot.auth.signer.RequestSigner``) -- this function does
    not itself return the raw material to a caller that only wants the
    signer.

    **Limitations of this boundary, stated explicitly:**

    - Python's single-underscore naming is a convention, not an
      enforced access boundary. Nothing at the language level stops
      another module in this repository from importing and calling
      this function directly.
    - The callback pattern does not make misuse impossible: a
      maliciously or carelessly written ``factory`` could retain,
      log, or return the raw ``access_key_id``/``private_key_pem`` it
      is handed instead of transforming them into a signer. This
      function cannot detect or prevent that.
    - What actually restricts who calls this today is architecture
      (only ``kalshi_bot.credentials`` and, once added,
      ``kalshi_bot.auth.signer`` have a legitimate reason to), import
      discipline, code review, and the static import-boundary test in
      ``tests/unit/test_credential_loader.py`` -- not a runtime or
      language-level guarantee.
    - Phase 1 PR 3 must replace this generic callback seam with a
      signer-specific construction path (for example, a function that
      takes only a ``LoadedDemoCredentials`` and returns exactly a
      ``RequestSigner``, with no caller-supplied callback). This
      generic callback-based seam must not remain reachable by REST,
      WebSocket, or any other downstream module once PR 3 lands.
    """
    return factory(credentials._access_key_id, credentials._private_key_pem)


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
