---
title: "User Orders - API Documentation"
source_url: "https://docs.kalshi.com/margin-ws/websockets/user-orders"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:03.030Z"
---
Messages

User Order Update

```
{  "type": "<string>",  "sid": 123,  "msg": {    "order_id": "<string>",    "user_id": "<string>",    "client_order_id": "<string>",    "ticker": "<string>",    "side": "<string>",    "price": "<string>",    "fill_count": "<string>",    "remaining_count": "<string>",    "self_trade_prevention_type": "<string>",    "order_group_id": "<string>",    "expiration_ts_ms": 123,    "created_ts_ms": 123,    "last_updated_ts_ms": 123,    "subaccount_number": 123  }}
```

WSS

wss://external-api-margin-ws.kalshi.comwss://external-api-margin-ws.demo.kalshi.co

user\_orders

Messages

User Order Update

```
{  "type": "<string>",  "sid": 123,  "msg": {    "order_id": "<string>",    "user_id": "<string>",    "client_order_id": "<string>",    "ticker": "<string>",    "side": "<string>",    "price": "<string>",    "fill_count": "<string>",    "remaining_count": "<string>",    "self_trade_prevention_type": "<string>",    "order_group_id": "<string>",    "expiration_ts_ms": 123,    "created_ts_ms": 123,    "last_updated_ts_ms": 123,    "subaccount_number": 123  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for margin WebSocket connections.

Receive

User Order Update

type:object

show 3 properties

Private margin order create/update notifications

[User Fills](https://docs.kalshi.com/margin-ws/websockets/user-fills)[Order Group Updates](https://docs.kalshi.com/margin-ws/websockets/order-group-updates)
