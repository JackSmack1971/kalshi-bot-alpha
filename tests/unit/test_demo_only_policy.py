"""Demo-only host-policy tests, plus the trading-authority boundary check.

Production endpoints are explicitly forbidden (a permanent invariant,
not phase-scoped): this file covers that repository-wide, plus the
authority-boundary invariant described below.

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

APPROVED_PHASE_0_POLICY_MODULES: frozenset[str] = frozenset(
    {
        "contracts/demo_endpoints.py",
    }
)

# Phase 0's exit criterion ("no trading code exists yet") was verified by
# an exact src/kalshi_bot/ file allowlist: only package markers plus this
# one approved, purity-checked policy module. Phase 0 is now accepted and
# closed (docs/IMPLEMENTATION_STATUS.md, docs/adr/0001-blueprint-v3-
# baseline.md) and Phase 1 (read-only connectivity) is activated per
# docs/PHASE1_PLAN.md, which legitimately adds observability/config/
# credentials modules (and, in later Phase 1 PRs, auth/kalshi/market_data)
# under src/kalshi_bot/. An exact allowlist of every permitted file would
# recreate the same brittle maintenance problem the old allowlist comment
# warned about, so the continuing executable invariant is no longer
# "no runtime code exists" -- it is "no trading-mutation authority or
# later-phase capability exists yet": no order creation/amendment/
# cancellation, execution, strategy, risk authorization, portfolio/
# positions/P&L/ledger, reconciliation, persistence/migrations-as-
# runtime-code, replay, external-reference ingestion, or AI/agent
# control-plane package may exist under src/kalshi_bot/ until its own
# phase authorizes it. See
# test_no_trading_authority_or_later_phase_code_exists_in_phase_1 below.
_FORBIDDEN_LATER_PHASE_PACKAGE_NAMES: frozenset[str] = frozenset(
    {
        # Order mutation / execution
        "orders",
        "order_management",
        "execution",
        # Strategy
        "strategy",
        "strategies",
        # Risk authorization
        "risk",
        # Portfolio / positions / P&L / accounting / ledger
        "portfolio",
        "positions",
        "pnl",
        "ledger",
        "accounting",
        # Reconciliation
        "reconciliation",
        # Persistence / migrations implemented as runtime code
        "persistence",
        "migrations",
        # Replay
        "replay",
        # External-reference ingestion
        "external_reference",
        "external_references",
        "reference_data",
        # AI / agent control plane
        "agents",
        "agent_tools",
        "openrouter",
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


def test_no_trading_authority_or_later_phase_code_exists_in_phase_1() -> None:
    """Phase 1 invariant: no trading-mutation authority or later-phase
    package/module exists under src/kalshi_bot/ before its governing
    phase is activated.

    Replaces the former Phase 0 exit-criterion test
    (``test_no_trading_code_exists_in_phase_0``), which asserted an
    exact src/ file allowlist -- see the module-level comment above
    for why that check no longer fits now that Phase 1 legitimately
    adds runtime code here. This test does not enumerate every
    permitted Phase 1 file (that would recreate the same brittle
    allowlist); it asserts the durable capability boundary instead.
    """
    src_root = REPO_ROOT / "src" / "kalshi_bot"
    found_forbidden: list[str] = []
    for path in src_root.rglob("*"):
        if path.is_dir():
            name = path.name
        elif path.suffix == ".py":
            name = path.stem
        else:
            continue
        if name.lower() in _FORBIDDEN_LATER_PHASE_PACKAGE_NAMES:
            found_forbidden.append(str(path.relative_to(src_root)).replace("\\", "/"))

    assert found_forbidden == [], (
        "Trading-mutation authority or later-phase package/module found "
        "under src/kalshi_bot/ before its governing phase is activated: "
        + ", ".join(sorted(found_forbidden))
    )

    # The Phase 0 approved policy module's purity check is preserved
    # unchanged and is not extended to any Phase 1 PR 2 module.
    for relative in APPROVED_PHASE_0_POLICY_MODULES:
        _assert_pure_policy_module(src_root / relative)
