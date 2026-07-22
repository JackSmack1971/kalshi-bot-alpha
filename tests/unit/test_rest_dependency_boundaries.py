"""Import/dependency-boundary check for kalshi_bot.rest (Phase 1 PR 4).

Proves, statically (AST-based, no import execution required), that
this package imports nothing from a later-phase capability package
(strategy, risk, order/execution, portfolio, ledger, reconciliation,
persistence, replay, AI/agent control plane -- none of which exist yet)
and that every ``kalshi_bot.*`` import it makes is one of the small set
of Phase 1 subpackages this client is legitimately allowed to depend
on.
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REST_PACKAGE_ROOT = REPO_ROOT / "src" / "kalshi_bot" / "rest"

_ALLOWED_KALSHI_BOT_SUBPACKAGES: frozenset[str] = frozenset(
    {"auth", "config", "contracts", "observability", "rest"}
)

_FORBIDDEN_MODULE_NAME_SUBSTRINGS: tuple[str, ...] = (
    "strategy",
    "strategies",
    "risk",
    "order",
    "execution",
    "portfolio",
    "position",
    "pnl",
    "ledger",
    "accounting",
    "reconciliation",
    "persistence",
    "migrations",
    "replay",
    "external_reference",
    "reference_data",
    "agent",
    "openrouter",
)


def _imported_module_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


def _rest_package_files() -> list[Path]:
    return sorted(REST_PACKAGE_ROOT.glob("*.py"))


def test_rest_package_exists_and_is_scanned() -> None:
    files = _rest_package_files()
    assert files, "expected kalshi_bot.rest source files to scan"


def test_rest_package_imports_no_later_phase_capability_module() -> None:
    violations: list[str] = []
    for path in _rest_package_files():
        for name in _imported_module_names(path):
            lowered = name.lower()
            for forbidden in _FORBIDDEN_MODULE_NAME_SUBSTRINGS:
                if forbidden in lowered:
                    violations.append(f"{path.name}: imports {name!r}")
    assert violations == [], "\n".join(violations)


def test_rest_package_only_imports_allowed_kalshi_bot_subpackages() -> None:
    violations: list[str] = []
    for path in _rest_package_files():
        for name in _imported_module_names(path):
            if name == "kalshi_bot" or name.startswith("kalshi_bot."):
                parts = name.split(".")
                if len(parts) < 2:
                    continue
                subpackage = parts[1]
                if subpackage not in _ALLOWED_KALSHI_BOT_SUBPACKAGES:
                    violations.append(f"{path.name}: imports {name!r}")
    assert violations == [], "\n".join(violations)
