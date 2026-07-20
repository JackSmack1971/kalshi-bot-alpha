---
title: "Public Trades - API Documentation"
source_url: "https://docs.kalshi.com/websockets/public-trades"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:58.727Z"
---
Messages

Trade Update

```
{
  "type": "trade",
  "sid": 11,
  "msg": {
    "trade_id": "d91bc706-ee49-470d-82d8-11418bda6fed",
    "market_ticker": "HIGHNY-22DEC23-B53.5",
    "yes_price_dollars": "0.360",
    "no_price_dollars": "0.640",
    "count_fp": "136.00",
    "taker_side": "no",
    "ts": 1669149841,
    "ts_ms": 1669149841000
  }
}
```

WSS

trade

Messages

Trade Update

```
{
  "type": "trade",
  "sid": 11,
  "msg": {
    "trade_id": "d91bc706-ee49-470d-82d8-11418bda6fed",
    "market_ticker": "HIGHNY-22DEC23-B53.5",
    "yes_price_dollars": "0.360",
    "no_price_dollars": "0.640",
    "count_fp": "136.00",
    "taker_side": "no",
    "ts": 1669149841,
    "ts_ms": 1669149841000
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Trade Update

type:object

show 3 properties

Public trade information

[Pyth Value Feed](https://docs.kalshi.com/websockets/pyth-value)[User Fills](https://docs.kalshi.com/websockets/user-fills)
