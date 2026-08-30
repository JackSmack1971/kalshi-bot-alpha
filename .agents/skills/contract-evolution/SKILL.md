---
name: contract-evolution
description: Use only when the user explicitly asks for a multi-agent review of a frozen schema/contract change. Drafts a proposal, then independently checks breaking-change versioning, downstream dependents, and authority-sensitive fields before handing the result to a human. Never activates configuration or fabricates approval.
---

# Multi-agent contract evolution

## Propose

Follow `propose-contract-change` for the user's requested schema/contract change. Produce a reviewable proposal only. If higher-precedence authority blocks the change, stop and report the conflict.

## Check

After the proposal exists, run three independent checks concurrently and wait for all:

1. A general reviewer decides whether the proposal is breaking and, if so, whether it uses an already-established explicit versioning mechanism rather than in-place semantic mutation.
2. `architecture-boundary-verifier` checks all existing source, tests, downstream schemas, docs, examples, and fixtures that depend on the touched field(s), including whether dependents were updated coherently.
3. `security-adversarial-reviewer` checks authority-sensitive fields: risk limits, approval/promotion state, credential/transport config, and the AI/deterministic-authority boundary.

Each check reports `pass`, `fail`, or `needs-human-approval`, with concrete findings. A failed or indeterminate check blocks the proposal from being described as review-ready. No result is itself human approval.
