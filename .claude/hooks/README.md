# Hooks Directory

Hooks supplement the control plane but are not its sole security boundary.

Every hook must define:

- lifecycle event;
- matcher;
- timeout;
- input and output schema;
- fail-open or fail-closed policy;
- malformed-payload behavior;
- diagnosis and retry behavior.
