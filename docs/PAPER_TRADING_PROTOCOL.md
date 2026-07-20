# Paper-Trading Evaluation Protocol

Normative Phase 0 contract. Source: blueprint §6, §13. Statistical
machinery is defined in `docs/RESEARCH_PROTOCOL.md`. This protocol is
demo-only end to end: no production endpoint, credential, or code path
exists or may be added (see `docs/DEMO_ENDPOINT_POLICY.md`,
`docs/CREDENTIAL_POLICY.md`, `docs/SAFETY_MODEL.md` §1). There is no
live-trading transition anywhere in this protocol or this project;
production enablement would require a separate project, architecture,
security review, and explicit human approval.

## 1. Startup preconditions (blueprint §6, §2.1)

The runtime must refuse to start unless, at minimum:

- The configured host is validated against the demo allowlist
  (`src/kalshi_bot/contracts/demo_endpoints.py`,
  `docs/DEMO_ENDPOINT_POLICY.md`).
- Credentials are present, well-formed, and sourced from an approved
  location (`docs/CREDENTIAL_POLICY.md`).
- System time drift is within the configured authentication
  tolerance.
- No unresolved prior shutdown or reconciliation failure is recorded
  in persistent state.

## 2. Decision cycle ordering (blueprint §6)

Strategy evaluation must not begin before reconciliation, market
eligibility, data health, and stream health are deterministically
confirmed. This ordering is load-bearing: a strategy that evaluates
against stale, unreconciled, or ineligible-market state produces
intents that the risk gateway must then reject, wasting the one
synchronous risk-decision boundary on avoidable rejections and
obscuring genuine risk violations in the log. This is the deterministic
authority boundary in practice — see `docs/SAFETY_MODEL.md` §3.

## 3. Frozen evaluation record

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

## 4. Minimum evidence (time AND volume)

- At least **30 calendar days**, and
- every sample and diversity gate from `docs/RESEARCH_PROTOCOL.md` §3
  (preregistered minimum quote opportunities, quotes, fills, fills per
  archetype, settlement events, adverse-selection observations, clean
  restarts, effective sample size; maximum unresolved data gaps;
  multiple market types and expirations).

Calendar duration alone never suffices.

## 5. Primary metrics

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

## 6. Promotion gates (ordered; operational correctness before profit)

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
requires durable human approval (`docs/SAFETY_MODEL.md` §5) and never
happens automatically.

## 7. AI evaluation (separate from strategy profitability)

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

## 8. Shutdown sequence

See `docs/FAILURE_TAXONOMY.md` §4 for the full seven-step shutdown
contract, including the nonzero-exit-on-unclean-reconciliation
requirement. A nonzero exit on unclean reconciliation is intentional:
it forces operator attention rather than allowing a paper-trading run
to appear to have ended cleanly when it did not.

## 9. Historical research mode (blueprint §12 "Historical research mode")

A separate replay command must, when built:

1. Load historical trades and candlesticks.
2. Reconstruct only the market information actually available at each
   timestamp.
3. Apply the same feature and strategy interfaces used in paper mode.
4. Use an explicit fill model (see `docs/RESEARCH_PROTOCOL.md` §6
   fill-model hierarchy).
5. Record assumptions and coverage limitations.
6. Produce deterministic results from a fixed dataset and
   configuration.

Replay must never share a code path with live paper trading in a way
that could let replay-mode assumptions leak into a live decision, or
vice versa.

## 10. Demo-environment acceptance tests (blueprint §10)

Acceptance tests that exercise real demo Kalshi order lifecycle are
explicitly out of Phase 0 scope and must not be run without demo
credentials configured and explicit authorization. This protocol
records that constraint for later phases; no such test exists yet
(`tests/acceptance/` is currently empty).

## Non-goals of this phase

No supervisor, decision-cycle loop, shutdown handler, or replay command
exists yet. This protocol fixes the sequencing and safety obligations
that the phase introducing the runtime must implement and test
against; nothing above describes current runtime behavior.
