"""Create the minimal financial truth schema."""

from alembic import op

revision = "0001_financial_truth"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    statements = (
        """CREATE TABLE strategy_intents (
            intent_id TEXT PRIMARY KEY, strategy_id TEXT NOT NULL,
            market_ticker TEXT NOT NULL, market_archetype_id TEXT NOT NULL,
            payload_json TEXT NOT NULL, created_at TEXT NOT NULL)""",
        """CREATE TABLE feature_snapshots (
            snapshot_id TEXT PRIMARY KEY, market_ticker TEXT NOT NULL,
            market_archetype_id TEXT NOT NULL, payload_json TEXT NOT NULL,
            captured_at TEXT NOT NULL)""",
        """CREATE TABLE risk_decisions (
            risk_decision_id TEXT PRIMARY KEY, intent_id TEXT NOT NULL
            REFERENCES strategy_intents(intent_id), approved INTEGER NOT NULL
            CHECK (approved IN (0, 1)), payload_json TEXT NOT NULL,
            decided_at TEXT NOT NULL)""",
        """CREATE TABLE orders (
            client_order_id TEXT PRIMARY KEY, intent_id TEXT NOT NULL
            REFERENCES strategy_intents(intent_id), feature_snapshot_id TEXT NOT NULL
            REFERENCES feature_snapshots(snapshot_id), risk_decision_id TEXT NOT NULL
            REFERENCES risk_decisions(risk_decision_id), market_ticker TEXT NOT NULL,
            side TEXT NOT NULL, quantity TEXT NOT NULL, price TEXT NOT NULL,
            state TEXT NOT NULL, created_at TEXT NOT NULL)""",
        """CREATE TABLE order_state_transitions (
            transition_id TEXT PRIMARY KEY, client_order_id TEXT NOT NULL
            REFERENCES orders(client_order_id), previous_state TEXT, state TEXT NOT NULL,
            evidence_reference TEXT NOT NULL, transitioned_at TEXT NOT NULL)""",
        """CREATE TABLE fills (
            fill_id TEXT PRIMARY KEY, client_order_id TEXT NOT NULL
            REFERENCES orders(client_order_id), exchange_fill_id TEXT NOT NULL UNIQUE,
            quantity TEXT NOT NULL, price TEXT NOT NULL, fee TEXT NOT NULL,
            filled_at TEXT NOT NULL)""",
        """CREATE TABLE ledger_entries (
            event_id TEXT PRIMARY KEY, idempotency_key TEXT NOT NULL UNIQUE,
            event_type TEXT NOT NULL, market_ticker TEXT, client_order_id TEXT,
            side TEXT, direction TEXT NOT NULL, quantity TEXT NOT NULL, price TEXT NOT NULL,
            amount TEXT NOT NULL, event_at TEXT NOT NULL)""",
        """CREATE TABLE positions (
            market_ticker TEXT NOT NULL, side TEXT NOT NULL, quantity TEXT NOT NULL,
            average_entry_price TEXT NOT NULL, realized_pnl TEXT NOT NULL,
            mark_price TEXT, unrealized_pnl TEXT NOT NULL, fees TEXT NOT NULL,
            PRIMARY KEY (market_ticker, side))""",
        """CREATE TABLE reconciliation_runs (
            reconciliation_id TEXT PRIMARY KEY, status TEXT NOT NULL,
            evidence_reference TEXT NOT NULL, started_at TEXT NOT NULL,
            completed_at TEXT)""",
    )
    for statement in statements:
        op.execute(statement)


def downgrade() -> None:
    raise RuntimeError("Financial truth migrations are append-only and cannot be downgraded")
