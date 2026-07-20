---
title: "Public Trades - API Documentation"
source_url: "https://docs.kalshi.com/margin-ws/websockets/public-trades"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.813Z"
---
Messages

Trade Update

```
{
  "type": "<string>",
  "sid": 123,
  "msg": {
    "trade_id": "<string>",
    "market_ticker": "<string>",
    "price": "<string>",
    "count": "<string>",
    "taker_side": "<string>",
    "ts_ms": 123
  }
}
```

WSS

wss://external-api-margin-ws.kalshi.comwss://external-api-margin-ws.demo.kalshi.co

trade

Messages

Trade Update

```
{
  "type": "<string>",
  "sid": 123,
  "msg": {
    "trade_id": "<string>",
    "market_ticker": "<string>",
    "price": "<string>",
    "count": "<string>",
    "taker_side": "<string>",
    "ts_ms": 123
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for margin WebSocket connections.

Receive

Trade Update

type:object

show 3 properties

Public margin trade information

[Market Ticker](https://docs.kalshi.com/margin-ws/websockets/market-ticker)[User Fills](https://docs.kalshi.com/margin-ws/websockets/user-fills)
