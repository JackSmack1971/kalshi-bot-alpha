from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import re
from typing import Any, Iterable

REPO_SENTINELS = (".git", "CLAUDE.md", ".claude")
HEX64_RE = re.compile(r"^[a-f0-9]{64}$")
TRUSTED_VERIFIER_PATH = ".claude/agents/control-plane-verifier.md"
REQUIRED_TERMINAL_ARTIFACTS = (
    "baseline.json",
    "plan.json",
    "verification.json",
    "result.json",
)

def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if any((candidate / sentinel).exists() for sentinel in REPO_SENTINELS):
            return candidate
    raise RuntimeError("Unable to locate repository root.")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class StableFileFingerprint:
    size_bytes: int
    sha256: str
    text: str | None = None


def normalize_text_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def stable_file_fingerprint(path: Path) -> StableFileFingerprint:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return StableFileFingerprint(size_bytes=len(data), sha256=hashlib.sha256(data).hexdigest())

    normalized = normalize_text_newlines(text)
    encoded = normalized.encode("utf-8")
    return StableFileFingerprint(
        size_bytes=len(encoded),
        sha256=hashlib.sha256(encoded).hexdigest(),
        text=normalized,
    )

def normalize_rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required for YAML parsing.") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def simple_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    block = text[4:end].splitlines()
    result: dict[str, Any] = {}
    key = None
    for raw in block:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z0-9_-]+:", raw):
            k, v = raw.split(":", 1)
            key = k.strip()
            value = v.strip()
            if value:
                result[key] = value.strip('"\'')
            else:
                result[key] = []
        elif key and raw.lstrip().startswith("- "):
            if not isinstance(result.get(key), list):
                result[key] = []
            result[key].append(raw.lstrip()[2:].strip())
    return result

def iter_control_plane_files(root: Path) -> Iterable[Path]:
    runs_root = root / ".claude/control-plane/runs"
    candidates = [root / "CLAUDE.md", root / ".claude"]
    for candidate in candidates:
        if candidate.is_file():
            yield candidate
        elif candidate.is_dir():
            for path in candidate.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                try:
                    path.relative_to(runs_root)
                except ValueError:
                    pass
                else:
                    continue
                if path.suffix.lower() in {".pyc", ".pyo"}:
                    continue
                if path in {
                    root / ".claude/control-plane/inventory.json",
                    root / ".claude/control-plane/context-estimate.json",
                }:
                    continue
                if path.name.endswith(".tmp"):
                    continue
                yield path


def build_inventory_document(root: Path) -> dict[str, Any]:
    records = []
    names: dict[str, list[str]] = {}

    for path in iter_control_plane_files(root):
        rel = normalize_rel(root, path)
        fingerprint = stable_file_fingerprint(path)
        record: dict[str, Any] = {
            "path": rel,
            "bytes": fingerprint.size_bytes,
            "sha256": fingerprint.sha256,
        }
        if fingerprint.text is None:
            record["binary"] = True
        else:
            fm = simple_frontmatter(fingerprint.text) if path.suffix.lower() == ".md" else {}
            record["estimated_tokens"] = rough_tokens(fingerprint.text)
            record["frontmatter"] = fm
            if fm.get("name"):
                names.setdefault(str(fm["name"]), []).append(rel)
        records.append(record)

    duplicates = {name: paths for name, paths in names.items() if len(paths) > 1}
    return {
        "schema_version": 1,
        "repository_root": ".",
        "files": sorted(records, key=lambda record: record["path"]),
        "duplicate_frontmatter_names": duplicates,
    }

def rough_tokens(text: str) -> int:
    # Deliberately labeled as an estimate. This is not a tokenizer.
    return max(1, round(len(text) / 4))


def portable_path_identity(value: str) -> str:
    return "/".join(
        part.rstrip(" .").casefold()
        for part in value.replace("\\", "/").split("/")
        if part not in {"", "."}
    )


def validate_change_plan_semantics(plan: dict[str, Any]) -> None:
    artifacts = plan.get("artifacts")
    if isinstance(artifacts, list):
        seen_artifact_paths: set[str] = set()
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                continue
            path = artifact.get("path")
            if not isinstance(path, str):
                continue
            identity = portable_path_identity(path)
            if identity in seen_artifact_paths:
                raise ValueError(f"Duplicate artifact path identity: {path}")
            seen_artifact_paths.add(identity)

    read_artifacts = plan.get("read_artifacts")
    if isinstance(read_artifacts, list):
        seen_read_paths: set[str] = set()
        for path in read_artifacts:
            if not isinstance(path, str):
                continue
            identity = portable_path_identity(path)
            if identity in seen_read_paths:
                raise ValueError(f"Duplicate read_artifact path identity: {path}")
            seen_read_paths.add(identity)


def validate_verifier_binding(
    run_dir: Path, baseline: dict[str, Any], verification: dict[str, Any]
) -> None:
    if verification.get("author_context_separate") is not True:
        raise ValueError("Verification must prove author-context separation")

    evidence = verification.get("evidence")
    if not isinstance(evidence, dict):
        raise ValueError("Verification evidence must be an object")
    verifier_identity = evidence.get("verifier_identity")
    if not isinstance(verifier_identity, dict):
        raise ValueError("Verification evidence must bind verifier identity")

    verifier_path = verifier_identity.get("path")
    verifier_sha256 = verifier_identity.get("sha256")
    if verifier_path != TRUSTED_VERIFIER_PATH:
        raise ValueError("Verifier identity must reference the trusted verifier agent")
    if not isinstance(verifier_sha256, str) or HEX64_RE.fullmatch(verifier_sha256) is None:
        raise ValueError("Verifier identity must include a sha256 digest")

    artifacts = baseline.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("Baseline artifacts must be an array")
    artifact_index = {
        artifact.get("path"): artifact
        for artifact in artifacts
        if isinstance(artifact, dict) and isinstance(artifact.get("path"), str)
    }
    artifact = artifact_index.get(verifier_path)
    if not isinstance(artifact, dict):
        raise ValueError("Baseline is missing the verifier artifact")
    if artifact.get("kind") != "file":
        raise ValueError("Verifier artifact must be a file")
    snapshot_path = artifact.get("snapshot_path")
    if not isinstance(snapshot_path, str):
        raise ValueError("Verifier artifact must have an immutable snapshot")
    if artifact.get("sha256") != verifier_sha256 or artifact.get("snapshot_sha256") != verifier_sha256:
        raise ValueError("Verifier identity does not match the baseline snapshot hash")

    snapshot = run_dir / snapshot_path
    if not snapshot.is_file() or sha256_file(snapshot) != verifier_sha256:
        raise ValueError("Verifier snapshot bytes do not match the recorded hash")
    verifier_name = simple_frontmatter(snapshot.read_text(encoding="utf-8")).get("name")
    if not isinstance(verifier_name, str) or verifier_name != verification.get("verifier"):
        raise ValueError("Verifier name does not match the trusted verifier snapshot")


def validate_terminal_artifact_hashes(run_dir: Path, terminal_event: dict[str, Any]) -> None:
    artifact_hashes = terminal_event.get("artifact_hashes")
    if not isinstance(artifact_hashes, dict):
        raise ValueError("Terminal event must include artifact hashes")

    for artifact_name in REQUIRED_TERMINAL_ARTIFACTS:
        expected = artifact_hashes.get(artifact_name)
        if not isinstance(expected, str) or HEX64_RE.fullmatch(expected) is None:
            raise ValueError(f"Terminal event is missing hash for {artifact_name}")
        artifact_path = run_dir / artifact_name
        if not artifact_path.is_file():
            raise ValueError(f"Terminal event references missing artifact {artifact_name}")
        if sha256_file(artifact_path) != expected:
            raise ValueError(f"Terminal event hash mismatch for {artifact_name}")
