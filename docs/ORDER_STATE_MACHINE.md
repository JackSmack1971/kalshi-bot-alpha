# Order State Machine

## States and transitions (blueprint SS5.11)

```text
INTENT_CREATED
    |
RISK_APPROVED
    |
SUBMISSION_PENDING
    |
    +--> REJECTED
    |
    +--> OUTCOME_UNKNOWN --> RECONCILING
    |
ACKNOWLEDGED
    |
    +--> OPEN
    |      |
    |      +--> PARTIALLY_FILLED
    |      |       |
    |      |       +--> FILLED
    |      |       +--> CANCEL_PENDING
    |      |
    |      +--> CANCEL_PENDING
    |
    +--> FILLED
    +--> CANCELLED
    +--> EXPIRED
```

**State changes must be driven by exchange evidence, not assumptions.**
This is the single governing invariant of this state machine: no
transition record may be written without a citable evidence reference
(an API response, a reconciliation result), and no state may be
inferred from elapsed time, expected behavior, or absence of an error.

## Uncertain-result rule (blueprint SS5.10)

A timeout after request transmission does not mean the order failed.
On uncertainty:

1. Mark the local command `OUTCOME_UNKNOWN`.
2. Stop strategy actions for that market.
3. Query orders using the client order ID.
4. Reconcile exchange state.
5. Resume only after a deterministic result.

This is why `OUTCOME_UNKNOWN --> RECONCILING` exists as an explicit
path rather than being collapsed into `REJECTED` or `ACKNOWLEDGED`.

## Executable contract

`schemas/order-state.schema.json` defines the shape of one transition
record:

- `state` / `previous_state` — drawn from the closed enum of thirteen
  states above; `previous_state` is `null` only for the initial
  `INTENT_CREATED` transition.
- `client_order_id` — UUID-based, per blueprint SS5.10's requirement
  that the execution engine generate UUID-based client order IDs.
- `evidence_reference` — required on every record; the identifier of
  the deterministic exchange evidence that justified the transition.
- `transitioned_at` — an explicit timestamp, so transition ordering is
  auditable independent of write order.

`tests/test_phase0_schemas_valid.py` validates a minimal conforming
example (an `INTENT_CREATED` record with `previous_state: null`) and a
deliberately invalid example (an unrecognized `state` value) against
this schema.

## Non-goals of this phase

No order-state transition logic, no order-book builder, no execution
engine, and no reconciliation service exist yet. This document and its
schema fix the target shape and invariants; a later phase implements
the state machine against them.
