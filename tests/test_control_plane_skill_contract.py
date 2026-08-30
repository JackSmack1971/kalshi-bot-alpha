import json
import importlib.util
import subprocess
import sys
from typing import Any
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_telemetry() -> Any:
    spec = importlib.util.spec_from_file_location(
        "skill_telemetry", ROOT / ".codex/scripts/skill_telemetry.py"
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_control_plane_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, ".codex/scripts/validate_control_plane.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_each_skill_has_consequential_telemetry_schema() -> None:
    for skill_dir in sorted((ROOT / ".agents/skills").iterdir()):
        if not skill_dir.is_dir():
            continue
        schema = json.loads((skill_dir / "telemetry/schema.json").read_text())
        assert schema["properties"]["skill"]["const"] == skill_dir.name
        events = schema["properties"]["event"]["enum"]
        assert events and not {"tool_used", "step_completed"}.intersection(events)
        assert "events.jsonl" in (skill_dir / "telemetry/.gitignore").read_text()


def test_memory_protocol_uses_native_toml_roles() -> None:
    protocol = (ROOT / ".codex/memory/PROTOCOL.md").read_text()
    assert "*.toml" in protocol
    assert "*-engineer.md" not in protocol


def test_telemetry_rejects_reserved_and_sensitive_fields() -> None:
    telemetry = load_telemetry()
    import pytest

    with pytest.raises(ValueError, match="undeclared"):
        telemetry.append_event(
            "verify-change", "check_selected", outcome="started", schema_version=99
        )
    with pytest.raises(ValueError, match="sensitive"):
        telemetry.append_event(
            "verify-change", "check_selected", outcome="started", api_key="synthetic"
        )
