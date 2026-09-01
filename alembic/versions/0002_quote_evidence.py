"""Persist passive quote evidence."""

from alembic import op

revision = "0002_quote_evidence"
down_revision = "0001_financial_truth"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """CREATE TABLE queue_state_snapshots (
            queue_state_snapshot_id TEXT PRIMARY KEY,
            intent_id TEXT NOT NULL REFERENCES strategy_intents(intent_id),
            market_ticker TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            captured_at TEXT NOT NULL)"""
    )
    op.execute(
        """CREATE TABLE quote_expectancy_records (
            quote_expectancy_id TEXT PRIMARY KEY,
            intent_id TEXT NOT NULL REFERENCES strategy_intents(intent_id),
            queue_state_snapshot_id TEXT NOT NULL
            REFERENCES queue_state_snapshots(queue_state_snapshot_id),
            market_ticker TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL)"""
    )


def downgrade() -> None:
    raise RuntimeError("Quote evidence migrations are append-only and cannot be downgraded")
