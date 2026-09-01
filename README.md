# Kalshi Crypto Paper-Trading Bot v3

Deterministic, demo-only Kalshi crypto paper-trading software for engineers and reviewers who need an auditable, fail-closed system.

> **DEMO ONLY.** This repository is not production-trading software. The current active phase is **Phase 3 — Portfolio and simulated execution**. Exchange mutation, live trading, and the AI control plane remain out of scope.

## What exists today

- Demo-only Kalshi REST and WebSocket clients with fixed demo endpoints.
- Deterministic market-data eligibility, order-book, risk, passive-spread, simulated-execution, persistence, and reconciliation modules.
- RSA-PSS request signing, demo credential loading, configuration validation, and structured log redaction.
- Typed REST/WebSocket models, normalization, reconnect handling, and read-only request validation.
- Nine frozen JSON Schema contracts covering trade intent, order state, risk limits, market archetypes, expectancy, queue calibration, markout toxicity, experiments, and statistical sufficiency.
- A static demo-only scanner and tests for endpoint, authority-boundary, schema, transport, credential, logging, and model behavior.

The target architecture and current limitations are described in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Phase status and exit evidence live in [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md).

## Quickstart

### Prerequisites

- Python 3.12 or newer (`pyproject.toml` declares `requires-python = ">=3.12"`).
- [uv](https://docs.astral.sh/uv/) for the locked development environment. [INFERRED from `uv.lock` and repository verification commands.]

### Install

```powershell
uv sync
```

### Run the verification suite

```powershell
uv run pytest -q
uv run ruff check .
uv run mypy .
uv run python scripts/verify_demo_only.py
```

These commands validate the deterministic demo-only runtime. The `demo-smoke-order --mock` command exercises simulated execution without credentials or network access.

## Safety boundaries

Only these Kalshi endpoints are allowed:

```text
REST:      https://external-api.demo.kalshi.co/trade-api/v2
WebSocket: wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2
```

The endpoint allowlist is hard-coded in [`src/kalshi_bot/contracts/demo_endpoints.py`](src/kalshi_bot/contracts/demo_endpoints.py), and [`scripts/verify_demo_only.py`](scripts/verify_demo_only.py) scans enforced paths for non-demo Kalshi hostnames. Production enablement is out of scope.

Credentials are process-isolated. A trading process may receive `KALSHI_DEMO_ACCESS_KEY` and `KALSHI_DEMO_PRIVATE_KEY_PATH`; it must not receive `OPENROUTER_API_KEY`. The separate future AI process may receive `OPENROUTER_API_KEY`, but no Kalshi credentials or execution capability. See [`docs/CREDENTIAL_POLICY.md`](docs/CREDENTIAL_POLICY.md) and [`docs/SAFETY_MODEL.md`](docs/SAFETY_MODEL.md).

Deterministic code owns calculation, authorization, execution, reconciliation, and accounting. AI output is non-authoritative and future human approvals remain required for strategy, risk, eligibility, configuration, reconciliation, and promotion changes.

## Architecture

The current runtime combines read-only market connectivity with a deterministic simulated-execution kernel:

```text
demo-only endpoint constants
        |
        +--> REST client --> typed market/status responses
        |
        +--> WebSocket client --> normalized ticker/trade frames
        |
        +--> auth signer + credential loader
        |
        +--> config validation + redacted observability
        +--> eligibility/order book -> strategy -> risk -> simulator -> ledger/reconciliation
```

The remaining production-like lifecycle is documented, but not implemented:

```text
market data -> eligibility -> order book -> features -> strategy
-> deterministic risk -> execution -> state machine -> ledger -> reconciliation
```

The future AI control plane is a separate process consuming sanitized evidence. It has no execution, active-configuration, ledger, or credential access.

## Repository layout

```text
src/kalshi_bot/       Python package: current read-only runtime modules
  auth/                RSA-PSS request signing
  config/              Pydantic configuration models and loader
  contracts/           demo endpoint allowlist
  credentials/         demo credential references and loader
  observability/       structured logging and redaction
  rest/                read-only REST client and response models
  ws/                  WebSocket client, models, and frame normalizer
schemas/               frozen JSON Schema contracts
config/                reviewed example runtime, risk, and strategy config
scripts/               repository safety verification scripts
tests/                 unit, contract, integration, and property tests
docs/                  architecture, safety, domain contracts, and phase status
docs-dev/              blueprint and reference documentation
migrations/            placeholder; persistence is deferred
```

## Configuration

Start from [`config/demo.example.yaml`](config/demo.example.yaml). It locks `environment.mode` to `demo`, references credentials by environment variable or external file, and displays the operator status `DEMO MODE`.

Use [`config/env.example`](config/env.example) as the safe variable template:

```text
KALSHI_DEMO_ACCESS_KEY=
KALSHI_DEMO_PRIVATE_KEY_PATH=
```

Never commit real credentials or place the private key inside the repository. The example intentionally does not define `OPENROUTER_API_KEY` for the trading process.

## Developer command center

| Purpose | Command |
| --- | --- |
| Full tests | `uv run pytest -q` |
| Lint | `uv run ruff check .` |
| Strict type checking | `uv run mypy .` |
| Demo-only policy scan | `uv run python scripts/verify_demo_only.py` |
| Run one test file | `uv run pytest tests/unit/test_rest_client.py -q` |

The project uses `pyproject.toml` and `uv.lock`; no CI workflow is currently present in the repository.

## Testing and verification

The repository-native verification gates are pytest, Ruff, mypy, and the demo-only scanner. The Phase 0 evidence recorded in [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) reports 69 passing tests, clean lint, successful strict type checking, and a passing demo-only scan. Re-run the commands above after changes; this README does not claim a fresh test run.

## Troubleshooting

| Symptom | Likely cause | Check or fix |
| --- | --- | --- |
| `uv` is not recognized | uv is not installed or not on `PATH` | Install uv, then rerun `uv sync`. |
| Configuration rejects startup | Mode, endpoint, or required field is invalid | Compare with `config/demo.example.yaml`; keep mode exactly `demo`. |
| Credential loading fails | Empty env reference, missing external key file, or unsafe file permissions | Set the two demo variables and keep the private key outside the repository. |
| Demo-only scanner reports a hostname | A non-allowlisted Kalshi hostname entered an enforced path | Remove it; only the two exact demo hosts are permitted. |
| WebSocket tests or reads fail | Connection, frame, ticker, or reconnect input is invalid | Inspect `src/kalshi_bot/ws/` and run the focused WebSocket tests. |

## Stack inventory

Versions and constraints come from [`pyproject.toml`](pyproject.toml) and [`uv.lock`](uv.lock):

- Python `>=3.12`
- Package version `0.0.0`
- Runtime libraries: `cryptography`, `httpx`, `pydantic`, `structlog`, `websockets`
- Development tools: `pytest`, `ruff`, `mypy`, `jsonschema`, `types-jsonschema`, `hypothesis`
- Build backend: Hatchling

Exact resolved versions are maintained in `uv.lock`; the README intentionally does not duplicate them.

## Reproducibility and maintenance

- Keep `uv.lock` synchronized with `pyproject.toml` when dependencies change.
- Keep endpoint constants and `ENFORCED_PATHS` synchronized when adding runtime or configuration paths.
- Treat schemas as frozen contracts; update their governing documentation and review the contract before changing fields.
- Read [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) before work and stay within the active phase.
- Use [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/SAFETY_MODEL.md`](docs/SAFETY_MODEL.md), and the relevant domain policy as the design references.

## Contributing and governance

Contributions must preserve demo isolation, credential privacy, deterministic authority, fail-closed behavior, auditability, and active-phase scope. Before submitting a change, run the verification commands and describe any unverified or deferred behavior.

Repository governance is defined by [`AGENTS.md`](AGENTS.md), [`CONTRIBUTING.md`](.github/CONTRIBUTING.md), [`SECURITY.md`](.github/SECURITY.md), and the policy files under [`.codex/policies/`](.codex/policies/). The blueprint is [`docs-dev/Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md`](docs-dev/Kalshi-Crypto-Paper-Trading-Bot-Blueprint-v3.md).

## Roadmap and status

Phase 0 contracts and safety model are accepted. Phase 3 portfolio and simulated execution is the active implementation phase. Later phases and the gated AI phases are recorded in [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md). This README does not add commitments beyond that phase ledger.

## License

This project is licensed under the [MIT License](LICENSE).
