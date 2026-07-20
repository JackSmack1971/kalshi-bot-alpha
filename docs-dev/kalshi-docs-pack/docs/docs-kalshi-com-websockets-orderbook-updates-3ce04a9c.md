---
title: "Orderbook Updates - API Documentation"
source_url: "https://docs.kalshi.com/websockets/orderbook-updates"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:58.237Z"
---
Messages

Orderbook Snapshot

```
{
  "type": "orderbook_snapshot",
  "sid": 2,
  "seq": 2,
  "msg": {
    "market_ticker": "FED-23DEC-T3.00",
    "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
    "yes_dollars_fp": [
      [
        "0.0800",
        "300.00"
      ],
      [
        "0.2200",
        "333.00"
      ]
    ],
    "no_dollars_fp": [
      [
        "0.5400",
        "20.00"
      ],
      [
        "0.5600",
        "146.00"
      ]
    ]
  }
}
```

Orderbook Delta

```
{
  "type": "orderbook_delta",
  "sid": 2,
  "seq": 3,
  "msg": {
    "market_ticker": "FED-23DEC-T3.00",
    "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
    "price_dollars": "0.960",
    "delta_fp": "-54.00",
    "side": "yes",
    "ts": "2022-11-22T20:44:01Z",
    "ts_ms": 1669149841000
  }
}
```

WSS

orderbook\_delta

Messages

Orderbook Snapshot

```
{
  "type": "orderbook_snapshot",
  "sid": 2,
  "seq": 2,
  "msg": {
    "market_ticker": "FED-23DEC-T3.00",
    "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
    "yes_dollars_fp": [
      [
        "0.0800",
        "300.00"
      ],
      [
        "0.2200",
        "333.00"
      ]
    ],
    "no_dollars_fp": [
      [
        "0.5400",
        "20.00"
      ],
      [
        "0.5600",
        "146.00"
      ]
    ]
  }
}
```

Orderbook Delta

```
{
  "type": "orderbook_delta",
  "sid": 2,
  "seq": 3,
  "msg": {
    "market_ticker": "FED-23DEC-T3.00",
    "market_id": "9b0f6b43-5b68-4f9f-9f02-9a2d1b8ac1a1",
    "price_dollars": "0.960",
    "delta_fp": "-54.00",
    "side": "yes",
    "ts": "2022-11-22T20:44:01Z",
    "ts_ms": 1669149841000
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Orderbook Snapshot

type:object

show 4 properties

Complete view of the order book's aggregated price levels

Orderbook Delta

type:object

show 4 properties

Update to be applied to the current order book view

[Connection Keep-Alive](https://docs.kalshi.com/websockets/connection-keep-alive)[Market Ticker](https://docs.kalshi.com/websockets/market-ticker)
