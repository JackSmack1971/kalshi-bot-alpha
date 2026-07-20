# Control-Plane Trust Model

## Governing thesis

Specialization does not create trust. Trust comes from bounded authority, explicit
interfaces, independent verification, deterministic checks, and reversible changes.

## Trusted components

The control plane may trust:

- the repository root resolved by the host process;
- the committed ownership manifest after human review;
- deterministic validators whose source is included in the repository;
- immutable input evidence captured before mutation;
- schema-valid run events in a verified hash chain;
- human approval recorded outside the authoring agent's own output.

## Untrusted components

The control plane must treat as untrusted:

- an author's confidence or summary;
- a specialist's claim that tests passed without evidence;
- inferred path ownership not present in the manifest;
- same-context self-review;
- model-generated token estimates presented as exact;
- hook payloads that fail schema validation;
- status files without run identity or sequence ordering;
- memory derived from failed or rolled-back runs;
- nested delegation not bounded by the parent harness.

## Core invariants

### CP-01 — Explicit artifact boundary

Resolve and classify each proposed path before mutation. Deny paths outside the
manifest, symlink escapes, absolute paths outside the repository, and path traversal.

### CP-02 — Single primary owner

Each transaction has exactly one primary specialist and no concurrent writers.

### CP-03 — Plan before mutation

The author must produce a schema-valid change plan with an immutable write set.

### CP-04 — No same-run self-authorization

The author may not independently approve its own change.

### CP-05 — Deterministic checks first

Mechanical facts must be checked by scripts before semantic model judgment.

### CP-06 — Evidence-gated completion

Completion requires passing assertions, preserved evidence, a verifier identity
bound to the immutable baseline snapshot of `.claude/agents/control-plane-verifier.md`,
and terminal event hashes that match `baseline.json`, `plan.json`,
`verification.json`, and `result.json`.

### CP-07 — Atomicity and rollback

Capture baselines before mutation and restore them after failed verification.

### CP-08 — No unbounded recursion

Nested delegation is disabled by default and must be bounded by the parent harness.

### CP-09 — Verified learning only

Persistent lessons may be accepted only from committed transactions.

### CP-10 — Measured minimality

Artifacts must justify their context, capability, and maintenance cost with measured
behavioral value.

## Failure posture

Fail closed for:

- writes outside the approved write set;
- forbidden-root access;
- malformed plans;
- illegal workflow transitions;
- missing verification evidence;
- unknown ownership;
- unresolved schema versions.

Return `INDETERMINATE` rather than guessing when semantic authority cannot be
established.
