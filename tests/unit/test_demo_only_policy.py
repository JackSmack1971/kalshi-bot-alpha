"""Phase 0 exit-criterion tests: production endpoints are explicitly forbidden.

Forbidden hostnames in this file are assembled at runtime so the static
scan of the test source itself stays clean.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_verifier():
    spec = importlib.util.spec_from_file_location(
        "verify_demo_only", REPO_ROOT / "scripts" / "verify_demo_only.py"
    )
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
    """Phase 0 exit criterion: src/ contains only the package marker."""
    src_files = [p for p in (REPO_ROOT / "src").rglob("*.py")]
    assert [p.name for p in src_files] == ["__init__.py"], (
        "Phase 0 must not contain trading code; found: "
        + ", ".join(str(p.relative_to(REPO_ROOT)) for p in src_files)
    )
