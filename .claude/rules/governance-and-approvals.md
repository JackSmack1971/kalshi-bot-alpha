---
paths:
  - "src/approvals/**/*.py"
  - "src/governance/**/*.py"
  - "src/proposals/**/*.py"
  - "src/configuration/**/*.py"
  - "src/promotion/**/*.py"
  - "src/reconciliation/**/*.py"
  - "config/**/*.yaml"
  - "config/**/*.yml"
  - "config/**/*.toml"
  - "tests/approvals/**/*.py"
  - "tests/governance/**/*.py"
---

# Governance and human approvals

Durable human approval is required before changing strategy logic or parameters, changing risk limits, adding an allowlisted market or series, activating proposed configuration, accepting a reconciliation adjustment, promoting a strategy version, treating an AI conclusion as binding, expanding agent tools/evidence access, or weakening privacy, fallback, or model policy.

Approval records must include approver, timestamp, proposal hash, evidence scope, decision, and resulting code or configuration version.

Approval never directly mutates active runtime state. Normal reviewed engineering and deployment paths remain required.

Claude Code must never simulate, infer, fabricate, self-grant, or backfill approval. Proposal and approval storage must remain distinct from active configuration and authoritative runtime state. Tests must cover replay, hash mismatch, stale approval, scope mismatch, missing approver, and attempted direct activation.
