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

## 2026-07-22 — transport-safety — PR #9 review-finding fixes: WS client resubscribe/queue/filtering/redaction hardening
Task: fix 5 automated-reviewer findings on `src/kalshi_bot/ws/client.py`
  from PR #9 (commit 27027e6) plus one self-identified adjacent
  robustness gap (RecursionError from pathologically nested JSON, and
  the disconnect()-with-a-full-queue consequence of the new bounded
  queue), all in the same worktree/branch as the original PR 5 entry
  above. Coordinator independently confirmed all findings as genuine
  bugs before requesting fixes.
Touched: src/kalshi_bot/ws/client.py, src/kalshi_bot/ws/normalizer.py;
  tests/unit/test_websocket_client.py, tests/unit/test_subscriptions.py,
  tests/contract/test_ws_message_schema.py.
Verified: `uv run pytest tests/unit/test_websocket_client.py
  tests/unit/test_subscriptions.py tests/contract/test_ws_message_schema.py
  tests/integration/test_websocket_reconnect.py` — 81 passed;
  `uv run pytest -q` — 456 passed; `uv run ruff check .` — All checks
  passed!; `uv run mypy .` — Success: no issues found in 42 source
  files; `uv run python scripts/verify_demo_only.py` — demo-only policy
  OK (56 files scanned); `git diff --check` against commit 27027e6 —
  clean (exit 0, only benign CRLF-normalization advisories, no
  whitespace/conflict errors).
Status: done
Notes: (1) A resubscribe-command send failure right after a successful
  reconnect no longer kills the background supervisor task uncaught —
  it is now treated as another dropped connection via a new
  `_reconnect_until_stable` helper (close, log, record, retry
  indefinitely), proven by
  `test_resubscribe_failure_after_reconnect_does_not_kill_supervisor`.
  (2) An abandoned subscription (iterator exits without a replacement
  call) now clears `_active_channel_tickers[channel]` in
  `_subscribe_channel`'s `finally`, reusing the existing queue-identity
  guard (both entries are set atomically together, so the same identity
  check safely covers both) rather than a separate per-call token,
  proven by `test_abandoned_subscription_is_not_resubscribed_after_reconnect`.
  (3) Per-channel delivery queues are now bounded
  (`_MAX_CHANNEL_QUEUE_SIZE = 1000`, drop-oldest-on-overflow, counted via
  the new `queue_full_drop_count` property), proven by
  `test_channel_queue_is_bounded_and_drops_oldest_on_overflow`; this
  also required hardening `disconnect()`'s stop-sentinel delivery
  (`_put_stop_sentinel`) since a full queue would otherwise make
  `put_nowait(_STOP)` raise `QueueFull` — proven by
  `test_disconnect_with_full_channel_queue_still_delivers_stop_sentinel`.
  (4) `_route_to_queue` now filters by the channel's currently active
  ticker set (new `unmatched_ticker_drop_count` counter) so an
  in-flight frame for a ticker set a caller has since replaced can
  never leak into a newer, unrelated consumer, proven by
  `test_replacing_subscription_does_not_leak_old_ticker_set_updates`.
  (5) The `error` frame's server-controlled `msg.msg` text is no longer
  logged (only the fixed small-integer `code`), proven by
  `test_error_frame_message_text_never_logged`. (6, self-identified
  while fixing the above, not one of the 5 numbered findings but a
  matching robustness gap): `kalshi_bot.ws.normalizer.parse_frame` now
  has an outer catch-all converting any unexpected decode failure
  (concretely: `RecursionError` from pathologically deep JSON nesting,
  a `RuntimeError` subclass the prior narrower `except (ValueError,
  TypeError)` did not catch) into `MalformedFrame` instead of
  propagating; `_supervise_connection`'s receive-loop call now also has
  a defense-in-depth `except Exception` treating any unforeseen
  dispatch failure as a dropped connection, and `disconnect()` no
  longer re-raises if the supervisor task had already ended with a
  non-cancellation exception. Proven by
  `test_deeply_nested_frame_does_not_crash_receive_loop_or_disconnect`,
  `test_unexpected_dispatch_exception_is_treated_as_a_dropped_connection`,
  and two normalizer-level contract tests. No
  `.claude/rules/kalshi-transport-safety.md`/`credential-privacy.md`
  invariant was weakened by any of these fixes; `orderbook_delta`
  remains structurally unreachable throughout. Not committed — left
  uncommitted per task instructions; orchestrating session reviews the
  diff, then commits and pushes.

## 2026-07-23 — transport-safety — PR #9 re-review (commit f6c53f4): 2 new gaps from the prior fix round
Task: fix 2 automated-reviewer findings on `src/kalshi_bot/ws/client.py`
  exposed by the previous fix round (commit f6c53f4, which the
  reviewer confirmed resolved the original 5 findings without
  re-flagging any of them). Coordinator independently confirmed both
  new findings as genuine before requesting fixes. Same worktree/branch
  as both prior entries above.
Touched: src/kalshi_bot/ws/client.py; tests/unit/test_subscriptions.py.
Verified: `uv run pytest tests/unit/test_websocket_client.py
  tests/unit/test_subscriptions.py tests/contract/test_ws_message_schema.py
  tests/integration/test_websocket_reconnect.py` — 83 passed;
  `uv run pytest -q` — 458 passed; `uv run ruff check .` — All checks
  passed!; `uv run mypy .` — Success: no issues found in 42 source
  files; `uv run python scripts/verify_demo_only.py` — demo-only policy
  OK (56 files scanned); `git diff --check` against commit f6c53f4 —
  clean (exit 0, only a benign CRLF-normalization advisory on
  client.py, no whitespace/conflict errors).
Status: done
Notes: (1) `_subscribe_channel` overwriting `_channel_queues[channel]`
  for a second `subscribe_ticker`/`subscribe_trades` call on the same
  channel left the OLD iterator permanently blocked on `await
  queue.get()` -- nothing would ever push to the now-orphaned queue
  object again, contradicting the class's own documented "the older
  iterator stops receiving further items" semantics (it must *stop*,
  not hang). Fixed by pushing `_STOP` onto the old queue (via the
  existing `_put_stop_sentinel` helper) before installing the new one.
  Proven by
  `test_replacing_subscription_ends_old_iterator_instead_of_hanging`
  (dedicated) and an updated
  `test_replacing_subscription_does_not_leak_old_ticker_set_updates`
  (which previously asserted the old task stayed pending forever --
  that assertion encoded the bug and had to be corrected to assert
  `StopAsyncIteration` instead, now that the fix makes the old iterator
  end promptly). (2) `disconnect()` pushed stop sentinels but left
  `_active_channel_tickers`/`_channel_queues` populated until each
  generator's own `finally` block happened to run; a `connect()` called
  again on the same instance before that cleanup completed would
  resubscribe to a channel the caller had already ended via
  `_resubscribe_all()`. Fixed by having `disconnect()` synchronously
  clear both dicts right after queuing the stop sentinels (the
  generators' own later `finally` guard becomes a harmless no-op once
  already cleared). Proven by
  `test_reconnect_after_disconnect_does_not_resubscribe_ended_channel`.
  No `.claude/rules/kalshi-transport-safety.md`/`credential-privacy.md`
  invariant was weakened. Not committed — left uncommitted per task
  instructions; orchestrating session reviews the diff, then commits.

## 2026-07-23 — transport-safety — PR #9 re-review (commit 014cc94): 1 P1 architectural gap + 3 P2 findings
Task: fix 4 automated-reviewer findings on `src/kalshi_bot/ws/client.py`
  (1 P1, 3 P2) from the re-review of commit 014cc94. Coordinator
  independently confirmed the P1 by reading the code before requesting
  fixes; flagged as the last expected round for this PR. Same
  worktree/branch as all four prior entries above.
Touched: src/kalshi_bot/ws/client.py; tests/unit/test_subscriptions.py,
  tests/unit/test_websocket_client.py.
Verified: `uv run pytest tests/unit/test_websocket_client.py
  tests/unit/test_subscriptions.py tests/contract/test_ws_message_schema.py
  tests/integration/test_websocket_reconnect.py` — 88 passed;
  `uv run pytest -q` — 463 passed; `uv run ruff check .` — All checks
  passed!; `uv run mypy .` — Success: no issues found in 42 source
  files; `uv run python scripts/verify_demo_only.py` — demo-only policy
  OK (56 files scanned); `git diff --check` against commit 014cc94 —
  clean (exit 0, only a benign CRLF-normalization advisory on
  client.py, no whitespace/conflict errors).
Status: done
Notes: (1, P1 — the real architectural gap the earlier client-side
  ticker-filter fix only band-aided) Replacing an active channel
  subscription while still connected previously just sent a second
  bare `subscribe` command, which Kalshi's documented WS protocol does
  not treat as a replacement (can create a duplicate server-side
  subscription or return error 6 "Already subscribed" — the new ticker
  set might never actually get established server-side). Fixed by
  tracking each channel's server-assigned `sid` (from the `subscribed`
  ack, now recorded in a new `_channel_sids` dict) and, when a known
  sid exists on the *current* connection, sending `unsubscribe` for it
  before the fresh `subscribe`. `_channel_sids` is cleared on every new
  dial (both `connect()` and `_reconnect_until_stable`) since a sid
  from a superseded connection is meaningless on a fresh socket — a
  reconnect's own `_resubscribe_all()` therefore always sends plain
  `subscribe`, never `unsubscribe`, matching the plan's explicit
  requirement. Proven by
  `test_replacing_subscription_with_known_sid_sends_unsubscribe_then_subscribe`
  and `test_resubscribe_after_reconnect_never_sends_unsubscribe_for_stale_sid`.
  (2, P2) The initial subscribe-send (`_subscribe_channel`'s first
  `_send_subscribe`/now also possible `_send_unsubscribe` call) runs
  before that call's own try/finally block is entered; a send failure
  there previously left the channel's queue/ticker-set entries
  orphaned for a later reconnect to pick up. Fixed by wrapping that
  initial send in its own try/except that cleans up via a new shared
  `_clear_channel_state_if_owned` helper (factored out of the
  pre-existing `finally` block's identity-guarded cleanup, now used in
  both places) before re-raising unchanged. Proven by
  `test_initial_subscribe_send_failure_cleans_up_tracked_state`. (3,
  P2) A `disconnect()` racing ahead of an in-flight `connect()` dial
  (before any connection/task was stored) previously left `connect()`
  free to unconditionally publish and supervise the socket once its
  dial completed, even though the caller had already been told
  shutdown succeeded — a live, unmanaged connection. Fixed by
  rechecking `self._closing` in `connect()` immediately after a
  successful dial; if set, the freshly dialed connection is closed via
  `_safe_close` and `WebSocketClientStateError` is raised instead of
  publishing it. Explicitly scoped/documented as covering this one
  narrow race, not a general mutual-exclusion guarantee across every
  interleaving of this class's lifecycle methods. Proven by
  `test_disconnect_racing_with_in_flight_connect_dial_closes_the_socket`
  (a gated test connector deterministically controls when the dial
  "completes" relative to the concurrent `disconnect()` call). (4, P2)
  `UnknownChannelFrame`'s raw, unbounded, server-controlled `frame_type`
  was logged verbatim (same class of issue as the earlier `ErrorFrame`
  message fix). Fixed with a new `_sanitize_frame_type_for_logging`
  helper (bounds to `_MAX_LOGGED_FRAME_TYPE_LENGTH` = 64 chars,
  replaces every non-alphanumeric/`_`/`-`/`.` character with `?`).
  Proven by `test_unknown_frame_type_is_sanitized_and_bounded_in_logs`.
  Also fixed, while touching these test files: two pre-existing
  duplicate trailing `asyncio.run(run())` lines (harmless but sloppy
  leftovers from earlier edit rounds) in
  `tests/unit/test_subscriptions.py` and
  `tests/unit/test_websocket_client.py`, and updated one pre-existing
  test (`test_replacing_subscription_does_not_leak_old_ticker_set_updates`)
  whose old assertion (`not old_task.done()`) had encoded a bug fixed
  in the prior round (the old iterator hanging forever) — it now
  correctly asserts `StopAsyncIteration`. No
  `.claude/rules/kalshi-transport-safety.md`/`credential-privacy.md`
  invariant was weakened by any of these fixes. Not committed — left
  uncommitted per task instructions; orchestrating session reviews the
  diff, then commits.
