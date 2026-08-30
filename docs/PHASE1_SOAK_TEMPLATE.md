# Phase 1 soak evidence template

The operator-only runner writes one immutable directory per UTC start time:

```text
artifacts/phase1/soak/<run-id>/
  report.json
  report.md
```

`report.json` has `report_schema_version: 1` and contains only sanitized
operational metadata, hashes, counters, timestamps, and evidence references.
It must not contain credentials, private keys, signatures, authorization
headers, or raw request/response bodies. `reconnects.local_mock_reconnects`
references standard-gate mock-server evidence; `reconnects.live_soak_reconnects`
references the one client-side-triggered reconnect from the live run. These
values are intentionally separate.

The live runner is never invoked by pytest or normal CI. A human operator must
explicitly invoke it with `--live-demo`; no four-hour run or human approval is
fabricated by the tooling.
