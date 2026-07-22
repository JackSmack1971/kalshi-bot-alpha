"""Read-only demo Kalshi REST client (Phase 1 PR 4).

Public API: :class:`KalshiDemoRestClient` plus the response models and
typed error hierarchy it uses. There is no order, portfolio-mutation,
or generic ``request(method, path)`` surface anywhere in this package.
"""

from kalshi_bot.rest.client import KalshiDemoRestClient
from kalshi_bot.rest.errors import (
    DemoHostValidationError,
    KalshiApiError,
    KalshiAuthError,
    KalshiRestError,
    OperationNotAllowedError,
    PaginationError,
    ResponseDecodeError,
    ResponseValidationError,
    TransportExhaustedError,
)
from kalshi_bot.rest.models import (
    DailyOpenClose,
    ExchangeIndexStatus,
    ExchangeSchedule,
    ExchangeStatus,
    MaintenanceWindow,
    MarketListPage,
    MarketSummary,
    StandardHoursBlock,
)

__all__ = [
    "KalshiDemoRestClient",
    "DemoHostValidationError",
    "KalshiApiError",
    "KalshiAuthError",
    "KalshiRestError",
    "OperationNotAllowedError",
    "PaginationError",
    "ResponseDecodeError",
    "ResponseValidationError",
    "TransportExhaustedError",
    "DailyOpenClose",
    "ExchangeIndexStatus",
    "ExchangeSchedule",
    "ExchangeStatus",
    "MaintenanceWindow",
    "MarketListPage",
    "MarketSummary",
    "StandardHoursBlock",
]
