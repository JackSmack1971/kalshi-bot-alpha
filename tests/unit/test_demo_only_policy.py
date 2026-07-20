"""Phase 0 exit-criterion tests: production endpoints are explicitly forbidden.

Forbidden hostnames in this file are assembled at runtime so the static
scan of the test source itself stays clean.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parents[2]

# Semantic allowlist of src/ modules approved for Phase 0. This is not a
# filename or directory substring heuristic: each entry is an exact
# repository-relative path, and every non-marker entry is additionally
# verified (see _assert_pure_policy_module) to import none of the
# transport/execution-capable modules a trading component would require.
# Extending this set requires both the explicit path and passing that
# purity check -- it cannot be satisfied by merely adding a file.
_PACKAGE_MARKERS: frozenset[str] = frozenset(
    {
        "__init__.py",
        "contracts/__init__.py",
    }
)
APPROVED_PHASE_0_POLICY_MODULES: frozenset[str] = frozenset(
    {
        "contracts/demo_endpoints.py",
    }
)

# Import roots that would indicate I/O, networking, process execution, or
# other transport/trading capability -- forbidden in a pure Phase 0 policy
# module (blueprint SS2.1: constants and a deterministic validator only).
_FORBIDDEN_IMPORT_ROOTS: frozenset[str] = frozenset(
    {
        "socket",
        "ssl",
        "http",
        "urllib",
        "requests",
        "httpx",
        "aiohttp",
        "websocket",
        "websockets",
        "asyncio",
        "subprocess",
        "os",
    }
)


def _assert_pure_policy_module(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        module_names: list[str] = []
        if isinstance(node, ast.Import):
            module_names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            module_names = [node.module]
        for name in module_names:
            root = name.split(".")[0]
            assert root not in _FORBIDDEN_IMPORT_ROOTS, (
                f"{path}: Phase 0 policy module must not import "
                f"transport/execution-capable module {name!r}"
            )


def _load_verifier() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "verify_demo_only", REPO_ROOT / "scripts" / "verify_demo_only.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("verify_demo_only", module)
    spec.loader.exec_module(module)
    return module


verifier = _load_verifier()


def test_repository_contains_no_non_demo_kalshi_hostnames() -> None:
    violations = verifier.scan_repository(REPO_ROOT)
    assert violations == [], (
        "Non-demo Kalshi hostnames found in enforced paths: "
        + ", ".join(f"{v.path}:{v.line}:{v.hostname}" for v in violations)
    )


def test_demo_hosts_are_allowed() -> None:
    text = (
        "rest: https://external-api.demo.kalshi.co/trade-api/v2\n"
        "ws: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2\n"
    )
    assert verifier.find_violations_in_text(text) == []


def test_production_style_hosts_are_detected() -> None:
    kalshi = "kalshi"
    forbidden_samples = [
        f"https://api.elections.{kalshi}.com/trade-api/v2",
        f"https://trading-api.{kalshi}.com/trade-api/v2",
        f"wss://api.{kalshi}.com/trade-api/ws/v2",
        f"{kalshi}.com",
        f"{kalshi}.co",  # bare apex domain is not on the allowlist either
        f"demo.{kalshi}.co",  # only the two exact demo hosts are allowed
    ]
    for sample in forbidden_samples:
        violations = verifier.find_violations_in_text(sample)
        assert violations, f"expected detection for: {sample}"


def test_detection_is_case_insensitive() -> None:
    kalshi_upper = "KALSHI"
    violations = verifier.find_violations_in_text(f"https://API.{kalshi_upper}.COM/x")
    assert violations


def test_allowlist_contains_only_the_two_demo_hosts() -> None:
    assert verifier.ALLOWED_HOSTS == frozenset(
        {"external-api.demo.kalshi.co", "external-api-ws.demo.kalshi.co"}
    )


def test_enforced_paths_cover_source_config_schemas_and_tests() -> None:
    for required in ("src", "config", "schemas", "scripts", "tests", "migrations"):
        assert required in verifier.ENFORCED_PATHS


def test_no_trading_code_exists_in_phase_0() -> None:
    """Phase 0 exit criterion: src/ contains only package markers plus the
    explicitly approved, purity-checked demo-only policy module."""
    src_root = REPO_ROOT / "src" / "kalshi_bot"
    src_files = {
        str(p.relative_to(src_root)).replace("\\", "/") for p in src_root.rglob("*.py")
    }
    approved = _PACKAGE_MARKERS | APPROVED_PHASE_0_POLICY_MODULES
    assert src_files == approved, (
        "Phase 0 must contain only package markers and the approved policy "
        "module allowlist; found: " + ", ".join(sorted(src_files))
    )
    for relative in APPROVED_PHASE_0_POLICY_MODULES:
        _assert_pure_policy_module(src_root / relative)
