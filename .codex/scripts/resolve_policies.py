#!/usr/bin/env python3
"""Resolve exact path-scoped Codex repository policies from policy `paths:` frontmatter."""
from __future__ import annotations
from pathlib import Path
import argparse, json, re, sys

ROOT = Path(__file__).resolve().parents[2]
POLICY_ROOT = ROOT / ".codex" / "policies"

def parse_paths(text: str) -> list[str]:
    if not text.startswith("---\n"):
        return []
    parts = text.split("---", 2)
    if len(parts) < 3:
        return []
    out=[]; in_paths=False
    for line in parts[1].splitlines():
        if re.match(r"^paths:\s*$", line):
            in_paths=True; continue
        if in_paths:
            m=re.match(r'^\s+-\s+["\']?(.+?)["\']?\s*$', line)
            if m: out.append(m.group(1)); continue
            if line and not line[0].isspace(): break
    return out

def glob_regex(pattern: str) -> re.Pattern[str]:
    p=pattern.replace('\\','/').lstrip('./')
    out=['^']; i=0
    while i < len(p):
        if p.startswith('**/', i): out.append('(?:.*/)?'); i += 3
        elif p.startswith('**', i): out.append('.*'); i += 2
        elif p[i]=='*': out.append('[^/]*'); i += 1
        elif p[i]=='?': out.append('[^/]'); i += 1
        else: out.append(re.escape(p[i])); i += 1
    out.append('$')
    return re.compile(''.join(out))

def normalize(path: str) -> str:
    p=Path(path)
    try:
        if p.is_absolute(): p=p.resolve().relative_to(ROOT.resolve())
    except ValueError:
        pass
    return p.as_posix().lstrip('./')

def inventory():
    rows=[]
    for f in sorted(POLICY_ROOT.rglob('*.md')):
        pats=parse_paths(f.read_text(encoding='utf-8'))
        rows.append((f,pats,[(p,glob_regex(p)) for p in pats]))
    return rows

def resolve(paths: list[str]):
    inv=inventory(); result=[]
    for raw in paths:
        path=normalize(raw); matches=[]
        for f,pats,compiled in inv:
            matched=[pat for pat,rx in compiled if rx.fullmatch(path)]
            if matched:
                matches.append({'policy':f.relative_to(ROOT).as_posix(),'patterns':matched})
        result.append({'path':path,'matches':matches})
    return result

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--json', action='store_true')
    args=ap.parse_args()
    rows=resolve(args.paths)
    if args.json:
        print(json.dumps(rows, indent=2)); return 0
    for row in rows:
        print(row['path'])
        if not row['matches']:
            print('  (no path-specific policy)')
        for m in row['matches']:
            print('  '+m['policy'])
            for pat in m['patterns']: print('    <- '+pat)
    return 0
if __name__=='__main__': raise SystemExit(main())
