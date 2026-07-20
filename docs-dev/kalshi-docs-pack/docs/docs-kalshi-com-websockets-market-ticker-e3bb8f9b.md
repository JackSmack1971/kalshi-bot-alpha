---
title: "Market Ticker - API Documentation"
source_url: "https://docs.kalshi.com/websockets/market-ticker"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:58.361Z"
---
Messages

Ticker Update

```
{
  "type": "ticker",
  "sid": 11,
  "msg": {
    "market_ticker": "FED-23DEC-T3.00",
    "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
    "price_dollars": "0.480",
    "yes_bid_dollars": "0.450",
    "yes_ask_dollars": "0.530",
    "volume_fp": "33896.00",
    "open_interest_fp": "20422.00",
    "dollar_volume": 16948,
    "dollar_open_interest": 10211,
    "yes_bid_size_fp": "300.00",
    "yes_ask_size_fp": "150.00",
    "last_trade_size_fp": "25.00",
    "ts": 1669149841,
    "ts_ms": 1669149841000,
    "time": "2022-11-22T20:44:01Z"
  }
}
```

WSS

ticker

Messages

Ticker Update

```
{
  "type": "ticker",
  "sid": 11,
  "msg": {
    "market_ticker": "FED-23DEC-T3.00",
    "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
    "price_dollars": "0.480",
    "yes_bid_dollars": "0.450",
    "yes_ask_dollars": "0.530",
    "volume_fp": "33896.00",
    "open_interest_fp": "20422.00",
    "dollar_volume": 16948,
    "dollar_open_interest": 10211,
    "yes_bid_size_fp": "300.00",
    "yes_ask_size_fp": "150.00",
    "last_trade_size_fp": "25.00",
    "ts": 1669149841,
    "ts_ms": 1669149841000,
    "time": "2022-11-22T20:44:01Z"
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Ticker Update

type:object

show 3 properties

Market price ticker information

[Orderbook Updates](https://docs.kalshi.com/websockets/orderbook-updates)[CF Benchmarks Value Feed](https://docs.kalshi.com/websockets/cfbenchmarks-value)
