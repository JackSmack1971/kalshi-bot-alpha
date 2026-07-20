# Immutable Experiment Registry Policy

## Pre-registration (blueprint "Experiment registry and statistical discipline")

Before confirmatory strategy analysis, an experiment must be
registered with:

- Hypothesis and falsification criteria.
- Primary metric.
- Secondary metrics.
- Fixed parameter grid.
- Included and excluded market archetypes.
- Training, development, and holdout windows.
- Minimum sample and diversity requirements.
- Multiple-comparison correction.
- Planned missing-data treatment.
- Strategy, feature, expectancy, archetype, fill-model, and
  agent-policy versions.

## Exploratory versus confirmatory discipline

Exploratory analysis must be labeled exploratory. All tested variants
must be retained, not only winners — a registry that only records
winning variants cannot support honest multiple-comparison correction
and is not compliant with this policy. Confirmatory evidence requires
a holdout period or market set that was not used to formulate the
hypothesis.

## Immutability

**Confirmatory experiment records are immutable after the scored
window begins.** The registry entry's optional `scored_window_started_at`
timestamp, once set, marks the instant after which no field of the
record may be mutated; any correction after that point requires a new,
separately registered experiment version with a `supersedes_experiment_version`
link, not an edit in place.

## Executable contract

`schemas/experiment-registration.schema.json` fixes:

- Every pre-registration field listed above as required.
- `experiment_version` (with an optional `supersedes_experiment_version`
  link) as a required integer, so a correction to a preregistered
  experiment always creates a new, traceable version rather than a
  mutation.
- `analysis_class` as a required closed enum
  (`exploratory`, `confirmatory`), so exploratory-versus-confirmatory
  status is never left implicit.
- `minimum_evidence` as a nested required object naming each of the
  sample and diversity gates in §3 above (`min_calendar_days`,
  `min_eligible_quote_opportunities`, `min_submitted_quotes`,
  `min_fills`, `min_fills_per_included_archetype`,
  `min_distinct_settlement_events`, `min_adverse_selection_observations`,
  `min_clean_restarts`, `max_unresolved_data_gaps`, and
  `min_effective_sample_size`), so promotion gates are individually
  traceable rather than collapsed into one sample-size number.
- `multiple_comparison_correction` as a nested required object naming
  both the correction `method` and the `declared_variant_count` it was
  applied over, so the preregistered variant count referenced in §4
  above is always explicit and auditable.
- `frozen_versions` as a nested required object naming each of
  `strategy_version`, `feature_version`, `expectancy_model_version`,
  `archetype_classifier_version`, and `fill_model_version` (with
  optional `agent_policy_version`, `agent_prompt_version`,
  `agent_schema_version`, and `agent_tool_registry_version` once an
  agent policy exists), satisfying blueprint Phase 0 exit criterion
  "Promotion requires sample-size and diversity gates in addition to
  elapsed time" by making every promotion-relevant version explicit
  and traceable.
- `scored_window_started_at` as an optional timestamp, set only once the
  scored window actually begins, fixing the point past which the
  record must not be mutated (enforced by the phase that implements
  registry persistence; not itself expressible as a JSON Schema
  constraint, and therefore documented here as a binding invariant on
  the implementation, mirrored by the property-test obligation
  "Confirmatory experiment records are immutable after the scored
  window begins" in blueprint §10).

## Non-goals of this phase

No registry persistence, no immutability enforcement, and no
promotion workflow exist yet. This policy and schema fix the target
shape; a later phase implements append-only persistence for these
records (see `.claude/rules/persistence-and-migrations.md`).
