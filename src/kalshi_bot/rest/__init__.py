"""Narrow demo Kalshi REST lifecycle client.

The client exposes only the reviewed order and portfolio operations; it has
no generic ``request(method, path)`` escape hatch.
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
    TransportFailureError,
    PreTransmissionFailure,
    AmbiguousOutcomeError,
    DuplicateSubmissionError,
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
    Order,
    OrderList,
    Fill,
    FillList,
    Position,
    PositionList,
    Balance,
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
    "TransportFailureError",
    "PreTransmissionFailure",
    "AmbiguousOutcomeError",
    "DuplicateSubmissionError",
    "DailyOpenClose",
    "ExchangeIndexStatus",
    "ExchangeSchedule",
    "ExchangeStatus",
    "MaintenanceWindow",
    "MarketListPage",
    "MarketSummary",
    "StandardHoursBlock",
    "Order",
    "OrderList",
    "Fill",
    "FillList",
    "Position",
    "PositionList",
    "Balance",
]
