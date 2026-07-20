from __future__ import annotations

from pathlib import Path
import argparse
import datetime as dt
import hashlib
import os
import json
import secrets
import subprocess
import tempfile

from common import find_repo_root, iter_control_plane_files, normalize_rel, sha256_file

def canonical_hash(event: dict) -> str:
    payload = dict(event)
    payload.pop("event_hash", None)
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

def git_identity(root: Path) -> dict:
    status = run_git(root, "status", "--porcelain=v1")
    lines = [line for line in status.splitlines() if line.strip()]
    changed_paths: list[str] = []
    staged_count = 0
    unstaged_count = 0
    untracked_count = 0

    for line in lines:
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        changed_paths.append(path)
        if code == "??":
            untracked_count += 1
            continue
        if code[0] != " ":
            staged_count += 1
        if code[1] != " ":
            unstaged_count += 1

    diff_hash = sha256_text("\n".join(sorted(lines)))
    branch = run_git(root, "branch", "--show-current") or run_git(root, "rev-parse", "--abbrev-ref", "HEAD")

    return {
        "commit_sha": run_git(root, "rev-parse", "HEAD"),
        "branch": branch,
        "dirty": bool(lines),
        "dirty_summary": {
            "changed_paths": sorted(dict.fromkeys(changed_paths)),
            "staged_count": staged_count,
            "unstaged_count": unstaged_count,
            "untracked_count": untracked_count,
            "diff_hash": diff_hash,
        },
    }

def baseline_artifacts(root: Path, run_dir: Path) -> list[dict]:
    roots = [root / "AGENTS.md", root / "CLAUDE.md", root / "README.md"]
    paths = list(iter_control_plane_files(root))
    for extra in roots:
        if extra.exists():
            paths.append(extra)

    artifacts: list[dict] = []
    unique_paths = {
        p.relative_to(root).as_posix() if p.is_symlink() else normalize_rel(root, p): p
        for p in paths
    }
    for rel, path in sorted(unique_paths.items()):
        is_symlink = path.is_symlink()
        within_repo = False
        if is_symlink:
            link_target = os.readlink(path)
            target = Path(link_target)
            if target.is_absolute():
                resolved = target.resolve(strict=False)
            else:
                resolved = (path.parent / target).resolve(strict=False)
            try:
                resolved.relative_to(root.resolve())
                within_repo = True
            except ValueError as exc:
                raise ValueError(f"Baseline symlink escapes repository: {rel} -> {link_target}") from exc

            link_bytes = link_target.encode("utf-8")
            digest = hashlib.sha256(link_bytes).hexdigest()
            size_bytes = len(link_bytes)
        else:
            path.resolve(strict=False).relative_to(root.resolve())
            within_repo = True
            data = path.read_bytes()
            digest = hashlib.sha256(data).hexdigest()
            size_bytes = len(data)
            snapshot_path = Path("baseline-artifacts") / digest
            (run_dir / snapshot_path).parent.mkdir(parents=True, exist_ok=True)
            write_bytes_exclusive(run_dir / snapshot_path, data)

        artifact = {
            "path": rel,
            "sha256": digest,
            "size_bytes": size_bytes,
            "kind": "symlink" if is_symlink else "file",
            "source": "root-doc" if rel in {"AGENTS.md", "CLAUDE.md", "README.md"} else "control-plane-tree",
            "reason_included": "managed boundary plus dependencies",
            "resolved_within_repository": within_repo,
        }
        if is_symlink:
            artifact["link_target"] = link_target
        else:
            artifact["snapshot_path"] = snapshot_path.as_posix()
            artifact["snapshot_sha256"] = digest
        artifacts.append(artifact)
    return artifacts

def write_json_atomic(path: Path, data: dict) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)

def _sync_published_entry(path: Path) -> None:
    if os.name == "nt":
        # Windows exposes no portable directory handle; flushing the linked file
        # is the strongest stdlib durability barrier for its new directory entry.
        with path.open("r+b") as published:
            os.fsync(published.fileno())
        return
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    directory_fd = os.open(path.parent, flags)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)

def write_json_exclusive(path: Path, data: dict) -> None:
    tmp_path = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
    try:
        with tmp_path.open("x", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.link(tmp_path, path)
        _sync_published_entry(path)
    finally:
        tmp_path.unlink(missing_ok=True)

def write_bytes_exclusive(path: Path, data: bytes) -> None:
    tmp_path = path.with_name(f".{path.name}.{secrets.token_hex(8)}.tmp")
    try:
        with tmp_path.open("xb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        try:
            os.link(tmp_path, path)
            _sync_published_entry(path)
        except FileExistsError:
            if path.read_bytes() != data:
                raise
    finally:
        tmp_path.unlink(missing_ok=True)

def append_event(path: Path, event: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def _capture_baseline(
    root: Path,
    run_dir: Path,
    run_id: str,
    manifest: Path,
    identity: dict,
    parent_event_hash: str,
) -> dict:
    baseline = {
        "schema_version": 1,
        "run_id": run_id,
        "repository_root": str(root),
        "manifest_hash": sha256_file(manifest),
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "git_identity": identity,
        "artifacts": baseline_artifacts(root, run_dir),
    }
    write_json_atomic(run_dir / "baseline.json", baseline)

    baseline_event = {
        "schema_version": 1,
        "run_id": run_id,
        "sequence": 1,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "state": "BASELINED",
        "actor": "new_run.py",
        "event_type": "baseline_captured",
        "message": "baseline.json captured",
        "artifact_hashes": {
            "request.json": sha256_file(run_dir / "request.json"),
            "baseline.json": sha256_file(run_dir / "baseline.json"),
        },
        "assertion_results": [],
        "parent_event_hash": parent_event_hash,
    }
    baseline_event["event_hash"] = canonical_hash(baseline_event)
    append_event(run_dir / "events.jsonl", baseline_event)
    return baseline

def _self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".claude").mkdir()
        (root / ".claude" / "alpha.txt").write_bytes(b"alpha")
        (root / ".claude" / "alpha-link.txt").symlink_to("alpha.txt")
        workflow_run = root / ".claude" / "workflows" / "runs" / "example.md"
        workflow_run.parent.mkdir(parents=True)
        workflow_run.write_text("# Example workflow run\n", encoding="utf-8")
        control_plane_run_file = root / ".claude" / "control-plane" / "runs" / "foo"
        control_plane_run_file.parent.mkdir(parents=True)
        control_plane_run_file.write_text("excluded\n", encoding="utf-8")
        iter_paths = {normalize_rel(root, path) for path in iter_control_plane_files(root)}
        assert ".claude/workflows/runs/example.md" in iter_paths
        assert ".claude/control-plane/runs/foo" not in iter_paths
        (root / "AGENTS.md").write_bytes(b"agents")
        manifest = root / ".claude" / "control-plane" / "manifest.yaml"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text("schema_version: 1\n", encoding="utf-8")
        identity = {
            "commit_sha": "0" * 40,
            "branch": "main",
            "dirty": False,
            "dirty_summary": {
                "changed_paths": [],
                "staged_count": 0,
                "unstaged_count": 0,
                "untracked_count": 0,
                "diff_hash": sha256_text(""),
            },
        }

        failed_run = root / ".claude" / "control-plane" / "runs" / "failed"
        failed_run.mkdir(parents=True)
        (failed_run / "request.json").write_text("{}\n", encoding="utf-8")
        original_writer = globals()["write_bytes_exclusive"]
        writes = 0

        def fail_second_write(path: Path, data: bytes) -> None:
            nonlocal writes
            writes += 1
            if writes == 2:
                raise OSError("injected snapshot failure")
            original_writer(path, data)

        globals()["write_bytes_exclusive"] = fail_second_write
        try:
            try:
                _capture_baseline(root, failed_run, "failed", manifest, identity, "0" * 64)
            except OSError:
                pass
            else:
                raise AssertionError("snapshot failure must abort baseline publication")
        finally:
            globals()["write_bytes_exclusive"] = original_writer
        assert not (failed_run / "baseline.json").exists()
        assert "BASELINED" not in (failed_run / "events.jsonl").read_text(encoding="utf-8") if (failed_run / "events.jsonl").exists() else True

        escape_run = root / ".claude" / "control-plane" / "runs" / "escape"
        escape_run.mkdir(parents=True)
        (escape_run / "request.json").write_text("{}\n", encoding="utf-8")
        outside = root.parent / "outside.txt"
        outside.write_bytes(b"outside")
        escape_link = root / ".claude" / "escape-link.txt"
        escape_link.symlink_to(os.path.relpath(outside, escape_link.parent))
        try:
            _capture_baseline(root, escape_run, "escape", manifest, identity, "0" * 64)
        except ValueError as exc:
            assert "Baseline symlink escapes repository" in str(exc)
        else:
            raise AssertionError("escaping symlink must abort baseline publication")
        assert not (escape_run / "baseline.json").exists()
        escape_link.unlink()

        run_dir = root / ".claude" / "control-plane" / "runs" / "complete"
        run_dir.mkdir(parents=True)
        (run_dir / "request.json").write_text("{}\n", encoding="utf-8")
        baseline = _capture_baseline(root, run_dir, "complete", manifest, identity, "0" * 64)
        paths = [item["path"] for item in baseline["artifacts"]]
        assert paths == sorted(paths)
        symlink_items = [item for item in baseline["artifacts"] if item["kind"] == "symlink"]
        assert any(item["path"] == ".claude/alpha-link.txt" for item in symlink_items)
        for item in baseline["artifacts"]:
            assert item["resolved_within_repository"] is True
            if item["kind"] == "symlink":
                link_target = os.readlink(root / item["path"])
                assert item["link_target"] == link_target
                assert hashlib.sha256(link_target.encode("utf-8")).hexdigest() == item["sha256"]
                assert item["size_bytes"] == len(link_target.encode("utf-8"))
                continue
            snapshot = run_dir / item["snapshot_path"]
            assert snapshot.read_bytes() == (root / item["path"]).read_bytes()
            assert sha256_file(snapshot) == item["sha256"] == item["snapshot_sha256"]
        assert json.loads((run_dir / "baseline.json").read_text(encoding="utf-8")) == baseline
        events = (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines()
        assert json.loads(events[-1])["state"] == "BASELINED"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--owner", choices=["skills-specialist","rules-specialist","workflow-specialist"])
    parser.add_argument("--request")
    args = parser.parse_args(argv)

    if args.self_check:
        _self_check()
        print("new_run self-check: ok")
        return 0

    if not args.owner or not args.request:
        parser.error("--owner and --request are required unless --self-check is used")

    root = find_repo_root()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"cp-{stamp}-{secrets.token_hex(3)}"
    run_dir = root / ".claude/control-plane/runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    manifest = root / ".claude/control-plane/manifest.yaml"
    identity = git_identity(root)
    request = {
        "schema_version": 1,
        "run_id": run_id,
        "owner": args.owner,
        "request": args.request,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "repository_root": str(root),
        "manifest_hash": sha256_file(manifest),
        "git_identity": identity,
    }
    (run_dir / "request.json").write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")

    event = {
        "schema_version": 1,
        "run_id": run_id,
        "sequence": 0,
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "state": "RECEIVED",
        "actor": "new_run.py",
        "event_type": "run_created",
        "message": args.request,
        "artifact_hashes": {"request.json": sha256_file(run_dir / "request.json")},
        "assertion_results": [],
        "parent_event_hash": None,
    }
    event["event_hash"] = canonical_hash(event)
    append_event(run_dir / "events.jsonl", event)

    _capture_baseline(root, run_dir, run_id, manifest, identity, event["event_hash"])

    for name, default in [
        ("plan.json", {}),
        ("proposed.patch", ""),
        ("verification.json", {}),
        ("result.json", {}),
    ]:
        content = json.dumps(default, indent=2) + "\n" if isinstance(default, dict) else default
        (run_dir / name).write_text(content, encoding="utf-8")

    print(run_id)
    print(run_dir)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
