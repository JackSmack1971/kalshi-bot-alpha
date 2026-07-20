# Paper-Trading Evaluation Protocol

Normative Phase 0 contract. Source: blueprint §13. Statistical machinery
is defined in `docs/RESEARCH_PROTOCOL.md`.

## 1. Frozen evaluation record

Each strategy version is frozen before evaluation. The evaluation record
captures:

```text
strategy version                 configuration hash
code commit                      market-selection rules
risk limits                      starting bankroll
evaluation start and end         planned exclusions
known data limitations           agent policy version
agent prompt version             OpenRouter model ID + actual provider/model
provider-routing/fallback policy structured-output schema version
tool-registry version            evidence-manifest hash
```

No parameter changes are permitted during the scored period.
Development and evaluation periods are separate. Daily reconciliation
and weekly incident review are mandatory.

## 2. Minimum evidence (time AND volume)

- At least **30 calendar days**, and
- every sample and diversity gate from `docs/RESEARCH_PROTOCOL.md` §3
  (preregistered minimum quote opportunities, quotes, fills, fills per
  archetype, settlement events, adverse-selection observations, clean
  restarts, effective sample size; maximum unresolved data gaps;
  multiple market types and expirations).

Calendar duration alone never suffices.

## 3. Primary metrics

Net paper P&L after fees; maximum drawdown; return on maximum capital at
risk; fill rate; adverse selection; exposure concentration; order
rejection rate; reconciliation incidents; strategy uptime; performance
by market type, archetype, and time-to-close bucket; fill-probability
calibration; queue completion and queue-conditioned fill rates; markout
distribution, tail expected shortfall, and toxicity rate; gross spread /
fees / inventory markout / settlement P&L / net-edge decomposition;
profit per submitted order, per fill, and per API mutation; maximum
correlated scenario loss; confidence intervals and effective sample
size; full multiple-testing and variant-disclosure record.

These roll up into the five **independent** daily scorecard dimensions —
data integrity, execution quality, adverse selection, strategy
economics, risk concentration — which are never collapsed into one
composite score.

## 4. Promotion gates (ordered; operational correctness before profit)

1. No production access.
2. No unresolved accounting differences.
3. No risk-limit bypass.
4. Stable market-data processing.
5. Deterministic restart recovery.
6. Only then evaluate strategy performance.
7. Performance satisfies the preregistered **sample, diversity,
   uncertainty, holdout, and multiple-testing** requirements.
8. Positive aggregate results are rejected when driven by one archetype,
   one settlement event, or an unrealistic fill model.

The evaluation concludes in exactly one statistical decision state
(`docs/RESEARCH_PROTOCOL.md` §5). Promotion of a strategy version
requires durable human approval and never happens automatically.

## 5. AI evaluation (separate from strategy profitability)

Agent quality is measured on a frozen corpus (known incidents, clean
runs, ambiguous cases, prompt-injection and exfiltration attempts,
conflicting hypotheses, statistically weak reports) across: evidence
citation validity, root-cause accuracy, unsupported-claim rate,
missing-evidence detection, policy-violation rate, structured-output
success, human acceptance/correction rate, rerun consistency, latency,
tokens, cost, and net analyst time saved after review burden. An agent
workflow is promotable only when it provides repeatable value **without
receiving greater authority** — higher model quality never justifies
broader trading permissions.
