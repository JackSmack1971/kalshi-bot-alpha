# Domain log — transport-safety

Append-only. See `.claude/memory/PROTOCOL.md` for format and rules.
Owning agent: `.claude/agents/transport-safety-engineer.md`.

## 2026-07-22 — transport-safety — Phase 1 PR 5: demo WebSocket client, reconnect, ticker/trade subscriptions
Task: implement docs/PHASE1_PLAN.md PR 5 (KalshiDemoWebSocketClient:
  demo-only WS handshake/signing, ticker/trade subscriptions, typed
  frame normalization, bounded-jittered reconnect lifecycle) in worktree
  `phase1-pr5-websocket-client`, branch `phase1/pr5-websocket-client`.
Touched: src/kalshi_bot/ws/__init__.py, src/kalshi_bot/ws/client.py,
  src/kalshi_bot/ws/models.py, src/kalshi_bot/ws/errors.py,
  src/kalshi_bot/ws/normalizer.py; tests/unit/test_websocket_client.py,
  tests/unit/test_subscriptions.py, tests/contract/test_ws_message_schema.py,
  tests/integration/test_websocket_reconnect.py; pyproject.toml (added
  `websockets>=15.0`, resolved to 16.1.1); uv.lock (regenerated via
  `uv lock`).
Verified: `uv run pytest tests/unit/test_websocket_client.py
  tests/unit/test_subscriptions.py tests/contract/test_ws_message_schema.py
  tests/integration/test_websocket_reconnect.py` — 71 passed;
  `uv run pytest -q` — 446 passed; `uv run ruff check .` — All checks
  passed!; `uv run mypy .` — Success: no issues found in 42 source
  files; `uv run python scripts/verify_demo_only.py` — demo-only policy
  OK (56 files scanned); `git diff --check` — clean (exit 0, only a
  benign CRLF-normalization advisory on uv.lock, no whitespace/conflict
  errors).
Status: done
Notes: Deviated from PHASE1_PLAN.md's literal PR5 paths
  (`src/kalshi_bot/kalshi/websocket_client.py` +
  `src/kalshi_bot/market_data/normalizer.py`) — followed the same
  already-merged deviation PR4 made for the REST client, landing a
  single cohesive `src/kalshi_bot/ws/` package
  (client.py/models.py/errors.py/normalizer.py/__init__.py) mirroring
  `src/kalshi_bot/rest/`'s shape. Documented in `ws/__init__.py`'s
  module docstring. Test paths are exactly as PHASE1_PLAN.md specifies
  — no deviation there. `orderbook_delta` and every channel other than
  `ticker`/`trade` is unreachable by construction (`_Channel` enum has
  only two members; no generic `subscribe(channels, tickers)` method
  exists) and is proven unknown/ignored by
  `tests/contract/test_ws_message_schema.py`. Reconnect uses a pure,
  independently-testable `ReconnectPolicy` (bounded exponential +
  jitter) and retries indefinitely post-initial-connect (no attempt-count
  cutoff, per config's bounded-seconds-only fields) but the *initial*
  `connect()` fails fast (typed `WebSocketConnectionError`, no retry) —
  a considered, disclosed design choice for fail-closed startup, not
  specified either way by the plan text. Stale-connection-generation
  frame dropping is proven at both a unit level (direct `_dispatch_frame`
  calls) and an integration level (whitebox call against the real
  running client + real local-server connection, documented inline as
  a targeted proof of the invariant rather than a live-race
  reproduction, since this client's sequential reconnect design never
  dials two connections concurrently). Handoff to
  accounting-ledger-engineer for `OUTCOME_UNKNOWN` reconciliation
  mechanics was not needed here — this PR is read-only market data,
  no mutating calls. No `.claude/rules/kalshi-transport-safety.md` or
  `credential-privacy.md` invariant was weakened; redaction is proven
  by dedicated tests in `tests/unit/test_websocket_client.py`
  (`test_no_secret_leakage_during_connect_reconnect_and_failure_paths`)
  covering handshake, reconnect, and initial-connect-failure paths.
  Not committed — left uncommitted per task instructions; orchestrating
  session handles commit/PR.
