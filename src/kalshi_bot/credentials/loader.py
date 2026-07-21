"""Load Kalshi demo credential material (Phase 1 PR 2).

This module is the sole reader of ``os.environ`` and the private-key
file for Kalshi credentials anywhere in this repository. It consumes a
:class:`~kalshi_bot.config.models.CredentialReferences` and produces a
:class:`LoadedDemoCredentials` -- an opaque type constructed only here.

Phase 1 PR 2 does not construct a signing capability: converting
``LoadedDemoCredentials`` into a ``RequestSigner`` is Phase 1 PR 3's
responsibility. Nothing in this module exposes the raw access-key ID
or private-key bytes to a caller.
"""

from __future__ import annotations

import os
from pathlib import Path

from kalshi_bot.config.models import CredentialReferences

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
    ``str`` never include the material.
    """

    __slots__ = ("_access_key_id", "_private_key_pem")

    def __init__(self, access_key_id: str, private_key_pem: bytes) -> None:
        self._access_key_id = access_key_id
        self._private_key_pem = private_key_pem

    def __repr__(self) -> str:
        return "LoadedDemoCredentials(<redacted>)"

    __str__ = __repr__


def load_credentials(refs: CredentialReferences) -> LoadedDemoCredentials:
    """Load Kalshi demo credential material referenced by ``refs``.

    Fails closed with a typed :class:`CredentialLoadError` on any
    missing environment variable, missing file, directory path, or
    unreadable file -- never falls back to an unauthenticated mode.
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

    return LoadedDemoCredentials(access_key_id, private_key_pem)
