---
title: "Market Positions - API Documentation"
source_url: "https://docs.kalshi.com/websockets/market-positions"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.016Z"
---
Messages

Market Position Update

```
{
  "type": "market_position",
  "sid": 14,
  "msg": {
    "user_id": "user123",
    "market_ticker": "FED-23DEC-T3.00",
    "position_fp": "100.00",
    "position_cost_dollars": "50.0000",
    "realized_pnl_dollars": "10.0000",
    "fees_paid_dollars": "1.0000",
    "position_fee_cost_dollars": "0.5000",
    "volume_fp": "15.00"
  }
}
```

WSS

market\_positions

Messages

Market Position Update

```
{
  "type": "market_position",
  "sid": 14,
  "msg": {
    "user_id": "user123",
    "market_ticker": "FED-23DEC-T3.00",
    "position_fp": "100.00",
    "position_cost_dollars": "50.0000",
    "realized_pnl_dollars": "10.0000",
    "fees_paid_dollars": "1.0000",
    "position_fee_cost_dollars": "0.5000",
    "volume_fp": "15.00"
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Market Position Update

type:object

show 3 properties

Real-time position updates for authenticated user

[User Fills](https://docs.kalshi.com/websockets/user-fills)[Market & Event Lifecycle](https://docs.kalshi.com/websockets/market-and-event-lifecycle)
