---
title: "Communications - API Documentation"
source_url: "https://docs.kalshi.com/websockets/communications"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.476Z"
---
Messages

RFQ Created

```
{
  "type": "rfq_created",
  "sid": 15,
  "msg": {
    "id": "rfq_123",
    "creator_id": "",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "contracts_fp": "100.00",
    "target_cost_dollars": "0.35",
    "created_ts": "2024-12-01T10:00:00Z"
  }
}
```

RFQ Deleted

```
{
  "type": "rfq_deleted",
  "sid": 15,
  "msg": {
    "id": "rfq_123",
    "creator_id": "comm_abc123",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "contracts_fp": "100.00",
    "target_cost_dollars": "0.35",
    "deleted_ts": "2024-12-01T10:05:00Z"
  }
}
```

Quote Created

```
{
  "type": "quote_created",
  "sid": 15,
  "msg": {
    "quote_id": "quote_456",
    "rfq_id": "rfq_123",
    "quote_creator_id": "comm_def456",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "yes_bid_dollars": "0.35",
    "no_bid_dollars": "0.65",
    "yes_contracts_offered_fp": "100.00",
    "no_contracts_offered_fp": "200.00",
    "rfq_target_cost_dollars": "0.35",
    "created_ts": "2024-12-01T10:02:00Z"
  }
}
```

Quote Accepted

```
{
  "type": "quote_accepted",
  "sid": 15,
  "msg": {
    "quote_id": "quote_456",
    "rfq_id": "rfq_123",
    "quote_creator_id": "comm_def456",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "yes_bid_dollars": "0.35",
    "no_bid_dollars": "0.65",
    "accepted_side": "yes",
    "contracts_accepted_fp": "50.00",
    "yes_contracts_offered_fp": "100.00",
    "no_contracts_offered_fp": "200.00",
    "rfq_target_cost_dollars": "0.35"
  }
}
```

Quote Executed

```
{
  "type": "quote_executed",
  "sid": 15,
  "msg": {
    "quote_id": "quote_456",
    "rfq_id": "rfq_123",
    "quote_creator_id": "a1b2c3d4e5f6...",
    "rfq_creator_id": "f6e5d4c3b2a1...",
    "order_id": "order_789",
    "client_order_id": "my_client_order_123",
    "market_ticker": "FED-23DEC-T3.00",
    "executed_ts": "2024-12-01T10:05:00Z"
  }
}
```

WSS

communications

Messages

RFQ Created

```
{
  "type": "rfq_created",
  "sid": 15,
  "msg": {
    "id": "rfq_123",
    "creator_id": "",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "contracts_fp": "100.00",
    "target_cost_dollars": "0.35",
    "created_ts": "2024-12-01T10:00:00Z"
  }
}
```

RFQ Deleted

```
{
  "type": "rfq_deleted",
  "sid": 15,
  "msg": {
    "id": "rfq_123",
    "creator_id": "comm_abc123",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "contracts_fp": "100.00",
    "target_cost_dollars": "0.35",
    "deleted_ts": "2024-12-01T10:05:00Z"
  }
}
```

Quote Created

```
{
  "type": "quote_created",
  "sid": 15,
  "msg": {
    "quote_id": "quote_456",
    "rfq_id": "rfq_123",
    "quote_creator_id": "comm_def456",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "yes_bid_dollars": "0.35",
    "no_bid_dollars": "0.65",
    "yes_contracts_offered_fp": "100.00",
    "no_contracts_offered_fp": "200.00",
    "rfq_target_cost_dollars": "0.35",
    "created_ts": "2024-12-01T10:02:00Z"
  }
}
```

Quote Accepted

```
{
  "type": "quote_accepted",
  "sid": 15,
  "msg": {
    "quote_id": "quote_456",
    "rfq_id": "rfq_123",
    "quote_creator_id": "comm_def456",
    "market_ticker": "FED-23DEC-T3.00",
    "event_ticker": "FED-23DEC",
    "yes_bid_dollars": "0.35",
    "no_bid_dollars": "0.65",
    "accepted_side": "yes",
    "contracts_accepted_fp": "50.00",
    "yes_contracts_offered_fp": "100.00",
    "no_contracts_offered_fp": "200.00",
    "rfq_target_cost_dollars": "0.35"
  }
}
```

Quote Executed

```
{
  "type": "quote_executed",
  "sid": 15,
  "msg": {
    "quote_id": "quote_456",
    "rfq_id": "rfq_123",
    "quote_creator_id": "a1b2c3d4e5f6...",
    "rfq_creator_id": "f6e5d4c3b2a1...",
    "order_id": "order_789",
    "client_order_id": "my_client_order_123",
    "market_ticker": "FED-23DEC-T3.00",
    "executed_ts": "2024-12-01T10:05:00Z"
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

RFQ Created

type:object

show 3 properties

Notification when an RFQ is created

RFQ Deleted

type:object

show 3 properties

Notification when an RFQ is deleted

Quote Created

type:object

show 3 properties

Notification when a quote is created on an RFQ

Quote Accepted

type:object

show 3 properties

Notification when a quote is accepted

Quote Executed

type:object

show 3 properties

Notification when a quote is executed and orders are placed

[Multivariate Lookups (Deprecated)](https://docs.kalshi.com/websockets/multivariate-lookups-deprecated)[Order Group Updates](https://docs.kalshi.com/websockets/order-group-updates)
