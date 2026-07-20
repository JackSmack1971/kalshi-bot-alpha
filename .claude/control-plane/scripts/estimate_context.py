from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path

from common import find_repo_root, rough_tokens

IMPORT_RE = re.compile(r"(?m)^\s*@([^\s]+)\s*$")
DEFAULT_OUTPUT = Path(".claude/control-plane/context-estimate.json")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def build_report(root: Path) -> dict[str, object]:
    report: dict[str, object] = {
        "schema_version": 1,
        "warning": "Token counts are rough character-based estimates, not model-tokenizer output.",
        "unconditional": [],
        "imports": [],
        "path_scoped": [],
        "skills": [],
    }

    claude = root / "CLAUDE.md"
    if claude.exists():
        text = read_text(claude)
        report["unconditional"].append({
            "path": "CLAUDE.md",
            "estimated_tokens": rough_tokens(text),
        })
        for target in IMPORT_RE.findall(text):
            imported = (root / target).resolve()
            if imported.exists() and imported.is_file():
                imported_text = read_text(imported)
                report["imports"].append({
                    "path": imported.relative_to(root).as_posix(),
                    "estimated_tokens": rough_tokens(imported_text),
                })

    rules_dir = root / ".claude/rules"
    if rules_dir.exists():
        for path in rules_dir.rglob("*.md"):
            text = read_text(path)
            scoped = "paths:" in text[:1000]
            report["path_scoped" if scoped else "unconditional"].append({
                "path": path.relative_to(root).as_posix(),
                "estimated_tokens": rough_tokens(text),
            })

    skills_dir = root / ".claude/skills"
    if skills_dir.exists():
        for path in skills_dir.rglob("SKILL.md"):
            text = read_text(path)
            report["skills"].append({
                "path": path.relative_to(root).as_posix(),
                "estimated_tokens": rough_tokens(text),
            })

    totals = {
        key: sum(item["estimated_tokens"] for item in report[key])
        for key in ("unconditional", "imports", "path_scoped", "skills")
    }
    report["totals"] = totals
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate control-plane context size without writing files by default."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=f"Optional path for writing the JSON report, for example {DEFAULT_OUTPUT.as_posix()}.",
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="Verify that the default report path is not created by read-only report generation.",
    )
    return parser.parse_args()


def run_self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".claude/rules").mkdir(parents=True)
        (root / ".claude/skills/example").mkdir(parents=True)
        (root / "CLAUDE.md").write_text("# Test\n", encoding="utf-8")
        (root / ".claude/rules/test.md").write_text("# Rule\n", encoding="utf-8")
        (root / ".claude/skills/example/SKILL.md").write_text("# Skill\n", encoding="utf-8")

        output_path = root / DEFAULT_OUTPUT
        build_report(root)
        if output_path.exists():
            raise AssertionError(f"default invocation wrote {output_path}")


def main() -> int:
    args = parse_args()
    if args.self_check:
        run_self_check()
        print("self-check passed: default report generation does not write files")
        return 0

    root = find_repo_root()
    report = build_report(root)
    rendered = json.dumps(report, indent=2) + "\n"
    print(rendered, end="")

    if args.output:
        out = args.output if args.output.is_absolute() else root / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
        print(f"Wrote {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
