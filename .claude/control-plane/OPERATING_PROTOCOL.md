# Operating Protocol

## Request classification

Choose one primary owner:

- reusable procedure → Skills Specialist;
- persistent declarative constraint → Rules Specialist;
- multi-stage orchestration or lifecycle control → Workflow Specialist.

For mixed requests, select the owner of the final integration surface. Other
specialists may provide interface analysis but must not write concurrently.

## Transaction sequence

1. `RECEIVED`
2. `CLASSIFIED`
3. `BASELINED`
4. `PLANNED`
5. `PLAN_VALIDATED`
6. `APPLYING`
7. `VERIFYING`
8. `COMMITTED`

Failure path:

1. `FAILED`
2. `ROLLED_BACK`

Cancellation may occur from any nonterminal state.

## Required evidence

Before mutation:

- normalized request;
- repository root;
- manifest hash;
- baseline hashes;
- approved write set;
- risk classification;
- rollback procedure.

After mutation:

- patch;
- deterministic validator output;
- behavioral evaluation results;
- independent verifier result;
- final artifact hashes;
- commit or rollback result.

## Retry policy

A failed verification must not be retried unchanged.

The next attempt must record:

- the failed assertion;
- diagnosis;
- changed hypothesis or implementation;
- new run ID;
- relationship to the previous run.

## Human approval

Human approval is required for:

- manifest ownership changes;
- expansion of allowed control-plane roots;
- agent-team enablement;
- nested delegation;
- changes to verifier capabilities;
- self-modification of a workflow;
- writes exceeding the manifest's file-count threshold;
- changes to permission or hook enforcement.
