import argparse
import importlib.util
import json
import subprocess
import uuid
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_enforcement_contract_missing_is_unverified():
    mod = load("enforcement", ".codex/scripts/verify_enforcement_contract.py")
    result = mod.evaluate({})
    assert result["status"] == "UNVERIFIED"
    assert result["missing_required_evidence"]


def test_enforcement_contract_rejects_unrestricted_mode():
    mod = load("enforcement2", ".codex/scripts/verify_enforcement_contract.py")
    state = {
        "project_trust": True,
        "approval_policy": "never",
        "permission_profile": ":danger-full-access",
        "unrestricted_mode": True,
        "production_kalshi_credentials_present": False,
        "codex_has_kalshi_execution_credentials": False,
        "production_kalshi_network_enabled": False,
    }
    result = mod.evaluate(state)
    assert result["status"] == "FAIL"
    fields = {x["field"] for x in result["violations"]}
    assert {"approval_policy", "permission_profile", "unrestricted_mode"} <= fields


def test_definition_snapshot_excludes_runtime_state():
    mod = load("definition", ".codex/scripts/build_definition_snapshot.py")
    paths = {p.relative_to(ROOT).as_posix() for p in mod.definition_files()}
    assert not any(p.startswith(".codex/memory/") for p in paths)
    assert not any(p.endswith("/telemetry/events.jsonl") for p in paths)
    assert not any("__pycache__" in p or p.endswith(".pyc") for p in paths)


def test_definition_snapshot_rejects_recorded_metadata_tamper(tmp_path):
    mod = load("definition_metadata", ".codex/scripts/build_definition_snapshot.py")
    snapshot = mod.build()
    snapshot["file_count"] += 1
    mod.SNAPSHOT_FILE = tmp_path / "definition-snapshot.json"
    mod.HASH_FILE = tmp_path / "DEFINITION_HASHES.sha256"
    mod.SNAPSHOT_FILE.write_text(json.dumps(snapshot), encoding="utf-8")
    mod.HASH_FILE.write_text(
        "".join(f"{row['sha256']}  {row['path']}\n" for row in snapshot["files"]),
        encoding="utf-8",
    )
    ok, problems = mod.verify()
    assert ok is False
    assert "definition snapshot file_count mismatch" in problems


def test_effective_state_does_not_infer_external_authority():
    mod = load("compiler", ".codex/scripts/compile_effective_state.py")
    args = argparse.Namespace(
        target_path=["src/risk/gateway.py"], authority_state=None,
        capability_state=None, environment_state=None, uow_state=None,
        model=None, reasoning_effort=None, output=None,
        _allow_unreleased_definition=True,
    )
    snap = mod.compile_snapshot(args)
    assert snap["authority"]["status"] == "UNVERIFIED"
    assert snap["capabilities"]["status"] == "UNVERIFIED"
    assert snap["environment"]["status"] == "UNVERIFIED"
    assert snap["model"]["status"] == "UNVERIFIED"
    assert snap["snapshot_id"].startswith("sha256:")


def test_skill_telemetry_reuses_run_and_chains_events(tmp_path):
    mod = load("skilltelemetry", ".codex/scripts/skill_telemetry.py")
    source = ROOT / ".agents/skills/verify-change"
    fake_root = tmp_path
    dest = fake_root / ".agents/skills/verify-change/telemetry"
    dest.mkdir(parents=True)
    (dest.parent / "SKILL.md").write_bytes((source / "SKILL.md").read_bytes())
    (dest / "schema.json").write_bytes((source / "telemetry/schema.json").read_bytes())
    mod.ROOT = fake_root
    run_id = str(uuid.uuid4())
    a = mod.append_event("verify-change", "invocation_started", outcome="started", run_id=run_id)
    b = mod.append_event("verify-change", "check_result", outcome="passed", run_id=run_id, reason_code="targeted")
    c = mod.append_event("verify-change", "invocation_finished", outcome="passed", run_id=run_id, reason_code="complete")
    assert [a["sequence"], b["sequence"], c["sequence"]] == [1, 2, 3]
    assert b["parent_event_hash"] == a["event_hash"]
    assert c["parent_event_hash"] == b["event_hash"]
    assert len({a["run_id"], b["run_id"], c["run_id"]}) == 1


def test_skill_telemetry_enforces_lifecycle(tmp_path):
    mod = load("skilltelemetry_lifecycle", ".codex/scripts/skill_telemetry.py")
    source = ROOT / ".agents/skills/verify-change"
    dest = tmp_path / ".agents/skills/verify-change/telemetry"
    dest.mkdir(parents=True)
    (dest.parent / "SKILL.md").write_bytes((source / "SKILL.md").read_bytes())
    (dest / "schema.json").write_bytes((source / "telemetry/schema.json").read_bytes())
    mod.ROOT = tmp_path
    run_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match="must begin"):
        mod.append_event("verify-change", "check_result", outcome="passed", run_id=run_id)
    mod.append_event("verify-change", "invocation_started", outcome="started", run_id=run_id)
    mod.append_event("verify-change", "invocation_finished", outcome="passed", run_id=run_id)
    with pytest.raises(ValueError, match="already finished"):
        mod.append_event("verify-change", "check_result", outcome="passed", run_id=run_id)


def test_execution_audit_enforces_lifecycle(tmp_path):
    mod = load("execution_audit_lifecycle", ".codex/scripts/execution_audit.py")
    mod.STATE = tmp_path
    run_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match="must begin"):
        mod.append(
            run_id,
            "policy.resolved",
            actor_role="primary",
            operation="resolve",
            outcome="passed",
            reason_code="TEST",
        )
    mod.append(
        run_id,
        "run.started",
        actor_role="primary",
        operation="start",
        outcome="started",
        reason_code="STARTED",
    )
    mod.append(
        run_id,
        "run.completed",
        actor_role="primary",
        operation="complete",
        outcome="completed",
        reason_code="DONE",
    )
    with pytest.raises(ValueError, match="already completed"):
        mod.append(
            run_id,
            "verification.result",
            actor_role="primary",
            operation="late-check",
            outcome="passed",
            reason_code="LATE",
        )


def test_eval_corpus_is_executable_and_complete():
    mod = load("cpeval", ".codex/scripts/control_plane_eval.py")
    result = mod.validate_corpus()
    assert result["valid"] is True
    assert result["counts"] == {"routing": 50, "task": 10, "failure": 5}
    assert result["total"] == 65


def test_eval_grade_distinguishes_complete_from_passed(tmp_path):
    mod = load("cpeval_grade", ".codex/scripts/control_plane_eval.py")
    rows = []
    for kind, cases in mod.corpus().items():
        for case in cases:
            if kind == "routing":
                wrong = "__wrong__" if case.get("expected_skill") != "__wrong__" else None
                rows.append({"case_id": case["id"], "selected_skill": wrong})
            else:
                criteria = case["success"] if kind == "task" else [case["expected"]]
                rows.append({"case_id": case["id"], "assertions": {criterion: False for criterion in criteria}})
    observations = tmp_path / "all-wrong.jsonl"
    observations.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    result = mod.grade(observations)
    assert result["complete"] is True
    assert result["passed"] is False
    assert result["routing"]["accuracy"] == 0
    assert result["workflow_assertions"]["pass_rate"] == 0


def test_uow_rename_preserves_destination_and_source(tmp_path):
    mod = load("uow_rename", ".codex/scripts/capture_uow.py")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@local.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=tmp_path, check=True)
    (tmp_path / "old.txt").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "add", "old.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "baseline"], cwd=tmp_path, check=True)
    subprocess.run(["git", "mv", "old.txt", "new.txt"], cwd=tmp_path, check=True)
    mod.ROOT = tmp_path
    rows = mod._status_paths()
    assert rows == [{"status": "R ", "path": "new.txt", "orig_path": "old.txt"}]
    record = mod.capture(["new.txt"])
    assert record["intended_delta"] == ["new.txt"]
    assert "authorized_delta" not in record
    ok, problems = mod.verify(record)
    assert ok is True, problems


def test_effective_state_rejects_tampered_uow(tmp_path):
    uow_mod = load("uow_for_compiler", ".codex/scripts/capture_uow.py")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@local.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=tmp_path, check=True)
    (tmp_path / "a.txt").write_text("a\n", encoding="utf-8")
    subprocess.run(["git", "add", "a.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "baseline"], cwd=tmp_path, check=True)
    uow_mod.ROOT = tmp_path
    record = uow_mod.capture(["a.txt"])
    record["intended_delta"].append("tampered.txt")
    uow_path = tmp_path / "uow.json"
    uow_path.write_text(json.dumps(record), encoding="utf-8")
    compiler = load("compiler_reject_uow", ".codex/scripts/compile_effective_state.py")
    args = argparse.Namespace(
        target_path=[], authority_state=None, capability_state=None,
        environment_state=None, uow_state=uow_path, model=None,
        reasoning_effort=None, output=None,
        _allow_unreleased_definition=True,
    )
    with pytest.raises(ValueError, match="UoW state invalid"):
        compiler.compile_snapshot(args)


def test_runtime_state_initializer_is_create_only(tmp_path):
    mod = load("runtime_initializer", ".codex/scripts/initialize_runtime_state.py")
    mod.TARGET = tmp_path / ".codex/memory"
    result = mod.initialize()
    assert result["status"] == "READY"
    assert "INDEX.md" in result["created"]
    index = mod.TARGET / "INDEX.md"
    index.write_text(index.read_text(encoding="utf-8") + "\nCUSTOM-RUNTIME-ENTRY\n", encoding="utf-8")
    second = mod.initialize()
    assert second["status"] == "READY"
    assert "INDEX.md" in second["preserved_existing"]
    assert "CUSTOM-RUNTIME-ENTRY" in index.read_text(encoding="utf-8")


def test_memory_sync_refuses_uninitialized_runtime_state(tmp_path):
    mod = load("memory_sync_uninitialized", ".codex/scripts/memory_sync.py")
    mod.ROOT = tmp_path
    with pytest.raises(ValueError, match="runtime memory is not initialized"):
        mod.append(
            "risk",
            "task",
            "none",
            "none",
            "done",
            "notes",
            None,
        )
