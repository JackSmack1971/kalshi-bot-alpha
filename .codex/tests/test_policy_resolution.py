import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('resolver', ROOT/'.codex/scripts/resolve_policies.py')
r=importlib.util.module_from_spec(spec); spec.loader.exec_module(r)

def policies(path):
    return {m['policy'] for m in r.resolve([path])[0]['matches']}

def test_transport_positive_and_negative():
    assert '.codex/policies/kalshi-transport-safety.md' in policies('src/foo/transport/client.py')
    assert '.codex/policies/kalshi-transport-safety.md' in policies('tests/unit/test_kalshi_transport.py')
    assert '.codex/policies/kalshi-transport-safety.md' not in policies('src/research/model.py')

def test_overlapping_sensitive_policy():
    ps=policies('src/foo/transport/auth.py')
    assert '.codex/policies/kalshi-transport-safety.md' in ps
    assert '.codex/policies/security-adversarial-review.md' in ps

def test_domain_policies():
    assert '.codex/policies/strategy-and-risk.md' in policies('src/risk/gateway.py')
    assert '.codex/policies/persistence-and-migrations.md' in policies('migrations/versions/001.py')
    assert '.codex/policies/research-evaluation-integrity.md' in policies('notebooks/analysis.ipynb')
