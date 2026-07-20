---
title: "User Fills - API Documentation"
source_url: "https://docs.kalshi.com/margin-ws/websockets/user-fills"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.919Z"
---
Messages

Fill Update

```
{  "type": "<string>",  "sid": 123,  "msg": {    "trade_id": "<string>",    "order_id": "<string>",    "client_order_id": "<string>",    "market_ticker": "<string>",    "is_taker": true,    "side": "<string>",    "ts_ms": 123,    "price": "<string>",    "count": "<string>",    "fee_cost": "<string>",    "post_position": "<string>",    "subaccount": 123  }}
```

WSS

wss://external-api-margin-ws.kalshi.comwss://external-api-margin-ws.demo.kalshi.co

fill

Messages

Fill Update

```
{  "type": "<string>",  "sid": 123,  "msg": {    "trade_id": "<string>",    "order_id": "<string>",    "client_order_id": "<string>",    "market_ticker": "<string>",    "is_taker": true,    "side": "<string>",    "ts_ms": 123,    "price": "<string>",    "count": "<string>",    "fee_cost": "<string>",    "post_position": "<string>",    "subaccount": 123  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for margin WebSocket connections.

Receive

Fill Update

type:object

show 3 properties

Private margin fill information for the authenticated user

[Public Trades](https://docs.kalshi.com/margin-ws/websockets/public-trades)[User Orders](https://docs.kalshi.com/margin-ws/websockets/user-orders)
