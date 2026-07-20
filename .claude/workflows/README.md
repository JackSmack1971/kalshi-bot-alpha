# Workflows Directory

Store workflow definitions, state-machine documentation, and resumable orchestration
contracts here.

Executable workflows live in `.js` files. Human-readable workflow contracts live in
paired `.md` files with the same basename.

Example:

- `idea-to-mvp.js` runs the orchestration.
- `idea-to-mvp.md` defines the contract, gates, and state model.

Every workflow must declare:

- states and legal transitions;
- typed inputs and outputs;
- read and write sets;
- success and failure criteria;
- turn, fan-out, recursion, retry, and timeout budgets;
- cancellation, resume, and rollback semantics;
- observability events;
- human approval points.

Every `.js` workflow must export a `meta` object with at least:

- `name`;
- `description`.

Standalone phase workflows for the idea-to-MVP system must also expose a
standard resumable cursor in their return shape:

- `currentPhase`;
- `status`;
- `completedNodes`;
- `eligibleNodes`;
- `blockedNodes`;
- `artifacts`;
- `requiredHumanDecisions`;
- `activeRisks`.
