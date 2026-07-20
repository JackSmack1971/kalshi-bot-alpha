"""Phase 0 contracts subpackage.

Holds pure, side-effect-free constants and validators that make
safety invariants testable before any transport, strategy, risk,
execution, reconciliation, or ledger code exists.
"""

from kalshi_bot.contracts.demo_endpoints import (
    DEMO_REST_HOST,
    DEMO_WS_HOST,
    validate_host,
)

__all__ = ["DEMO_REST_HOST", "DEMO_WS_HOST", "validate_host"]
