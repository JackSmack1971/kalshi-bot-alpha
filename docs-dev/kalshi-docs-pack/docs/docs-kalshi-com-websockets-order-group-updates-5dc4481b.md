---
title: "Order Group Updates - API Documentation"
source_url: "https://docs.kalshi.com/websockets/order-group-updates"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.616Z"
---
Messages

Order Group Updates

```
{  "type": "order_group_updates",  "sid": 21,  "seq": 7,  "msg": {    "event_type": "limit_updated",    "order_group_id": "og_123",    "contracts_limit_fp": "150.00"  }}
```

WSS

order\_group\_updates

Messages

Order Group Updates

```
{  "type": "order_group_updates",  "sid": 21,  "seq": 7,  "msg": {    "event_type": "limit_updated",    "order_group_id": "og_123",    "contracts_limit_fp": "150.00"  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Order Group Updates

type:object

show 4 properties

Order group lifecycle and limit updates for authenticated user

[Communications](https://docs.kalshi.com/websockets/communications)[User Orders](https://docs.kalshi.com/websockets/user-orders)
