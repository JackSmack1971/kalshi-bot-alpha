"""Isolated Kalshi demo credential loading (Phase 1 PR 2)."""

from kalshi_bot.credentials.loader import (
    CredentialLoadError,
    LoadedDemoCredentials,
    load_credentials,
)

__all__ = ["CredentialLoadError", "LoadedDemoCredentials", "load_credentials"]
