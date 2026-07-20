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
window begins.** The registry entry's `immutable_after` timestamp
marks the instant after which no field of the record may be mutated;
any correction after that point requires a new, separately registered
experiment, not an edit in place.

## Executable contract

`schemas/experiment_registry.schema.json` fixes:

- Every pre-registration field listed above as required.
- `versions` as a nested required object naming each of
  `strategy_version`, `feature_version`, `expectancy_model_version`,
  `archetype_classifier_version`, and `fill_model_version` (with an
  optional `agent_policy_version` once an agent policy exists),
  satisfying blueprint Phase 0 exit criterion "Promotion requires
  sample-size and diversity gates in addition to elapsed time" by
  making every promotion-relevant version explicit and traceable.
- `is_exploratory` as a required boolean, so exploratory-versus-
  confirmatory status is never left implicit.
- `immutable_after` as a required timestamp, fixing the point past
  which the record must not be mutated (enforced by the phase that
  implements registry persistence; not itself expressible as a JSON
  Schema constraint, and therefore documented here as a binding
  invariant on the implementation, mirrored by the property-test
  obligation "Confirmatory experiment records are immutable after the
  scored window begins" in blueprint SS10).

## Non-goals of this phase

No registry persistence, no immutability enforcement, and no
promotion workflow exist yet. This policy and schema fix the target
shape; a later phase implements append-only persistence for these
records (see `.claude/rules/persistence-and-migrations.md`).
