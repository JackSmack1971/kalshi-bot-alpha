#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, tomllib
ROOT=Path(__file__).resolve().parents[2]
errors=[]; warnings=[]

def err(x): errors.append(x)
def warn(x): warnings.append(x)

required=['AGENTS.md','.codex/config.toml','.codex/control-plane/manifest.json','.codex/scripts/resolve_policies.py']
for p in required:
    if not (ROOT/p).is_file(): err(f'missing required file: {p}')

# TOML syntax and agent contract
try: tomllib.loads((ROOT/'.codex/config.toml').read_text(encoding='utf-8'))
except Exception as e: err(f'config TOML invalid: {e}')
agent_names=set()
for p in sorted((ROOT/'.codex/agents').glob('*.toml')):
    try: d=tomllib.loads(p.read_text(encoding='utf-8'))
    except Exception as e: err(f'{p.relative_to(ROOT)} invalid TOML: {e}'); continue
    for k in ('name','description','developer_instructions'):
        if not d.get(k): err(f'{p.relative_to(ROOT)} missing {k}')
    n=d.get('name')
    if n in agent_names: err(f'duplicate agent name: {n}')
    agent_names.add(n)
    if 'model' in d: warn(f'{p.relative_to(ROOT)} pins a model; portability may be reduced')

# Skill discovery/routing basics
skill_names=set()
for d in sorted((ROOT/'.agents/skills').iterdir()):
    if not d.is_dir(): continue
    p=d/'SKILL.md'
    if not p.is_file(): err(f'{d.relative_to(ROOT)} missing SKILL.md'); continue
    t=p.read_text(encoding='utf-8')
    if not t.startswith('---\n'): err(f'{p.relative_to(ROOT)} missing frontmatter'); continue
    fm=t.split('---',2)[1]
    nm=re.search(r'^name:\s*(.+)$',fm,re.M); ds=re.search(r'^description:\s*(.+)$',fm,re.M)
    if not nm or not ds: err(f'{p.relative_to(ROOT)} needs name and description'); continue
    name=nm.group(1).strip().strip('"\'')
    if name in skill_names: err(f'duplicate skill name: {name}')
    skill_names.add(name)
    desc=ds.group(1).strip()
    if len(desc)<50: warn(f'{p.relative_to(ROOT)} routing description is unusually short')

# Manifest references
try:
    m=json.loads((ROOT/'.codex/control-plane/manifest.json').read_text(encoding='utf-8'))
    for n in m.get('orchestration_skills',[]):
        if n not in skill_names: err(f'manifest orchestration skill missing: {n}')
except Exception as e: err(f'manifest invalid: {e}')

# Policy frontmatter must have paths and no empty pattern set
for p in sorted((ROOT/'.codex/policies').rglob('*.md')):
    t=p.read_text(encoding='utf-8')
    if not t.startswith('---\npaths:\n'): err(f'{p.relative_to(ROOT)} lacks paths frontmatter')
    if not re.search(r'^\s+-\s+"?.+"?$', t.split('---',2)[1], re.M): err(f'{p.relative_to(ROOT)} has no paths')

# No live Claude harness paths in operational artifacts. Migration report is exempt.
for base in [ROOT/'AGENTS.md', ROOT/'.agents', ROOT/'.codex/agents', ROOT/'.codex/memory']:
    files=[base] if base.is_file() else list(base.rglob('*'))
    for p in files:
        if not p.is_file(): continue
        t=p.read_text(encoding='utf-8',errors='ignore')
        if '.claude/' in t or 'CLAUDE.md' in t:
            err(f'live Claude harness reference remains: {p.relative_to(ROOT)}')

# Native statusline values are deliberately a conservative subset verified against current Codex.
try:
    cfg=tomllib.loads((ROOT/'.codex/config.toml').read_text(encoding='utf-8'))
    allowed={'model','model-name','model-with-reasoning','reasoning','current-dir','project','project-root','project-name','hostname','git-branch','pull-request-number','branch-changes','run-state','status','permissions','approval-mode','approval','context-remaining','context-used','context-usage','five-hour-limit','weekly-limit','codex-version','context-window-size','used-tokens','total-input-tokens','total-output-tokens','thread-credits','estimated-thread-cost','thread-id','session-id','fast-mode','raw-output','thread-title','workspace-headline','task-progress'}
    for item in cfg.get('tui',{}).get('status_line',[]):
        if item not in allowed: err(f'unsupported status_line item in package validator: {item}')
except Exception: pass

print(f'control-plane validation: {len(errors)} error(s), {len(warnings)} warning(s)')
for x in errors: print('ERROR:',x)
for x in warnings: print('WARN:',x)
raise SystemExit(1 if errors else 0)
