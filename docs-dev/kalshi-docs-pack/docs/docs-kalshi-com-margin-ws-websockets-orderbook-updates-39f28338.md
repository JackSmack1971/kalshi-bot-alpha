---
title: "Orderbook Updates - API Documentation"
source_url: "https://docs.kalshi.com/margin-ws/websockets/orderbook-updates"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.554Z"
---
Messages

Orderbook Snapshot

```
No examples found
```

Orderbook Delta

```
{  "type": "<string>",  "sid": 123,  "seq": 123,  "msg": {    "market_ticker": "<string>",    "price": "<string>",    "delta": "<string>",    "side": "<string>",    "last_update_reason": "<string>",    "client_order_id": "<string>",    "subaccount": 123,    "ts_ms": 123  }}
```

WSS

wss://external-api-margin-ws.kalshi.comwss://external-api-margin-ws.demo.kalshi.co

orderbook\_delta

Messages

Orderbook Snapshot

```
No examples found
```

Orderbook Delta

```
{  "type": "<string>",  "sid": 123,  "seq": 123,  "msg": {    "market_ticker": "<string>",    "price": "<string>",    "delta": "<string>",    "side": "<string>",    "last_update_reason": "<string>",    "client_order_id": "<string>",    "subaccount": 123,    "ts_ms": 123  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for margin WebSocket connections.

Receive

Orderbook Snapshot

type:object

show 4 properties

Complete view of the margin order book's aggregated price levels

Orderbook Delta

type:object

show 4 properties

Update to be applied to the current margin order book view

[Connection Keep-Alive](https://docs.kalshi.com/margin-ws/websockets/connection-keep-alive)[Market Ticker](https://docs.kalshi.com/margin-ws/websockets/market-ticker)
