---
title: "User Fills - API Documentation"
source_url: "https://docs.kalshi.com/websockets/user-fills"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:58.831Z"
---
Messages

Fill Update

```
{  "type": "fill",  "sid": 13,  "msg": {    "trade_id": "d91bc706-ee49-470d-82d8-11418bda6fed",    "order_id": "ee587a1c-8b87-4dcf-b721-9f6f790619fa",    "market_ticker": "HIGHNY-22DEC23-B53.5",    "is_taker": true,    "side": "yes",    "yes_price_dollars": "0.750",    "count_fp": "278.00",    "action": "buy",    "ts": 1671899397,    "ts_ms": 1671899397000,    "post_position_fp": "500.00",    "purchased_side": "yes",    "subaccount": 3  }}
```

WSS

fill

Messages

Fill Update

```
{  "type": "fill",  "sid": 13,  "msg": {    "trade_id": "d91bc706-ee49-470d-82d8-11418bda6fed",    "order_id": "ee587a1c-8b87-4dcf-b721-9f6f790619fa",    "market_ticker": "HIGHNY-22DEC23-B53.5",    "is_taker": true,    "side": "yes",    "yes_price_dollars": "0.750",    "count_fp": "278.00",    "action": "buy",    "ts": 1671899397,    "ts_ms": 1671899397000,    "post_position_fp": "500.00",    "purchased_side": "yes",    "subaccount": 3  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Fill Update

type:object

show 3 properties

Private fill information for authenticated user

[Public Trades](https://docs.kalshi.com/websockets/public-trades)[Market Positions](https://docs.kalshi.com/websockets/market-positions)
