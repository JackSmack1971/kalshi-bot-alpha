# Runtime state seed

This directory is immutable release definition. It seeds mutable `.codex/memory/**` runtime coordination state through `initialize_runtime_state.py`. The initializer only creates missing files and never overwrites existing memory. Runtime memory itself is intentionally excluded from release archives and definition identity.
