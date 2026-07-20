---
title: "User Orders - API Documentation"
source_url: "https://docs.kalshi.com/websockets/user-orders"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.723Z"
---
Messages

User Order Update

```
{  "type": "user_order",  "sid": 22,  "msg": {    "order_id": "ee587a1c-8b87-4dcf-b721-9f6f790619fa",    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",    "ticker": "FED-23DEC-T3.00",    "status": "resting",    "side": "yes",    "is_yes": true,    "yes_price_dollars": "0.3500",    "fill_count_fp": "0.00",    "remaining_count_fp": "10.00",    "initial_count_fp": "10.00",    "taker_fill_cost_dollars": "0.0000",    "maker_fill_cost_dollars": "0.0000",    "client_order_id": "my-order-1",    "order_group_id": "og_123",    "self_trade_prevention_type": "taker_at_cross",    "created_time": "2024-12-01T10:00:00Z",    "created_ts_ms": 1733047200000,    "expiration_time": "2024-12-01T11:00:00Z",    "expiration_ts_ms": 1733050800000,    "subaccount_number": 0  }}
```

WSS

user\_orders

Messages

User Order Update

```
{  "type": "user_order",  "sid": 22,  "msg": {    "order_id": "ee587a1c-8b87-4dcf-b721-9f6f790619fa",    "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",    "ticker": "FED-23DEC-T3.00",    "status": "resting",    "side": "yes",    "is_yes": true,    "yes_price_dollars": "0.3500",    "fill_count_fp": "0.00",    "remaining_count_fp": "10.00",    "initial_count_fp": "10.00",    "taker_fill_cost_dollars": "0.0000",    "maker_fill_cost_dollars": "0.0000",    "client_order_id": "my-order-1",    "order_group_id": "og_123",    "self_trade_prevention_type": "taker_at_cross",    "created_time": "2024-12-01T10:00:00Z",    "created_ts_ms": 1733047200000,    "expiration_time": "2024-12-01T11:00:00Z",    "expiration_ts_ms": 1733050800000,    "subaccount_number": 0  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

User Order Update

type:object

show 3 properties

Real-time order updates for authenticated user

[Order Group Updates](https://docs.kalshi.com/websockets/order-group-updates)[Common Components](https://docs.kalshi.com/fix/common-components)
