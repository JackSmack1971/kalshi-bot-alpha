---
title: "WebSocket Connection - API Documentation"
source_url: "https://docs.kalshi.com/websockets/websocket-connection"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:57.967Z"
---
Messages

Subscribe Command

```
{
  "id": 1,
  "cmd": "subscribe",
  "params": {
    "channels": [
      "orderbook_delta"
    ],
    "market_ticker": "CPI-22DEC-TN0.1"
  }
}
```

Unsubscribe Command

```
{
  "id": 124,
  "cmd": "unsubscribe",
  "params": {
    "sids": [
      1,
      2
    ]
  }
}
```

List Subscriptions Command

```
{
  "id": 3,
  "cmd": "list_subscriptions"
}
```

Update Subscription - Add Markets

```
{
  "id": 124,
  "cmd": "update_subscription",
  "params": {
    "sids": [
      456
    ],
    "market_tickers": [
      "NEW-MARKET-1",
      "NEW-MARKET-2"
    ],
    "action": "add_markets"
  }
}
```

Update Subscription - Delete Markets

```
{
  "id": 125,
  "cmd": "update_subscription",
  "params": {
    "sids": [
      456
    ],
    "market_tickers": [
      "MARKET-TO-REMOVE-1",
      "MARKET-TO-REMOVE-2"
    ],
    "action": "delete_markets"
  }
}
```

Update Subscription - Single SID Format

```
{
  "id": 126,
  "cmd": "update_subscription",
  "params": {
    "sid": 456,
    "market_tickers": [
      "NEW-MARKET-3",
      "NEW-MARKET-4"
    ],
    "action": "add_markets"
  }
}
```

Update Subscription - CF Benchmarks Indices

```
{
  "id": 2,
  "cmd": "update_subscription",
  "params": {
    "sid": 1,
    "action": "indexlist"
  }
}
```

Update Subscription - Pyth Underlyings

```
{
  "id": 2,
  "cmd": "update_subscription",
  "params": {
    "sid": 1,
    "action": "underlying_list"
  }
}
```

Subscribed Response

```
{
  "id": 1,
  "type": "subscribed",
  "msg": {
    "channel": "orderbook_delta",
    "sid": 1
  }
}
```

Unsubscribed Response

```
{
  "id": 102,
  "sid": 2,
  "seq": 7,
  "type": "unsubscribed"
}
```

OK Response

```
{
  "id": 123,
  "sid": 456,
  "seq": 222,
  "type": "ok",
  "msg": {
    "market_tickers": [
      "MARKET-1",
      "MARKET-2",
      "MARKET-3"
    ]
  }
}
```

List Subscriptions Response

```
{
  "id": 3,
  "type": "ok",
  "msg": [
    {
      "channel": "orderbook_delta",
      "sid": 1
    },
    {
      "channel": "ticker",
      "sid": 2
    },
    {
      "channel": "fill",
      "sid": 3
    }
  ]
}
```

Error Response

```
{
  "id": 123,
  "type": "error",
  "msg": {
    "code": 6,
    "msg": "Already subscribed"
  }
}
```

WSS

/

Messages

Subscribe Command

```
{
  "id": 1,
  "cmd": "subscribe",
  "params": {
    "channels": [
      "orderbook_delta"
    ],
    "market_ticker": "CPI-22DEC-TN0.1"
  }
}
```

Unsubscribe Command

```
{
  "id": 124,
  "cmd": "unsubscribe",
  "params": {
    "sids": [
      1,
      2
    ]
  }
}
```

List Subscriptions Command

```
{
  "id": 3,
  "cmd": "list_subscriptions"
}
```

Update Subscription - Add Markets

```
{
  "id": 124,
  "cmd": "update_subscription",
  "params": {
    "sids": [
      456
    ],
    "market_tickers": [
      "NEW-MARKET-1",
      "NEW-MARKET-2"
    ],
    "action": "add_markets"
  }
}
```

Update Subscription - Delete Markets

```
{
  "id": 125,
  "cmd": "update_subscription",
  "params": {
    "sids": [
      456
    ],
    "market_tickers": [
      "MARKET-TO-REMOVE-1",
      "MARKET-TO-REMOVE-2"
    ],
    "action": "delete_markets"
  }
}
```

Update Subscription - Single SID Format

```
{
  "id": 126,
  "cmd": "update_subscription",
  "params": {
    "sid": 456,
    "market_tickers": [
      "NEW-MARKET-3",
      "NEW-MARKET-4"
    ],
    "action": "add_markets"
  }
}
```

Update Subscription - CF Benchmarks Indices

```
{
  "id": 2,
  "cmd": "update_subscription",
  "params": {
    "sid": 1,
    "action": "indexlist"
  }
}
```

Update Subscription - Pyth Underlyings

```
{
  "id": 2,
  "cmd": "update_subscription",
  "params": {
    "sid": 1,
    "action": "underlying_list"
  }
}
```

Subscribed Response

```
{
  "id": 1,
  "type": "subscribed",
  "msg": {
    "channel": "orderbook_delta",
    "sid": 1
  }
}
```

Unsubscribed Response

```
{
  "id": 102,
  "sid": 2,
  "seq": 7,
  "type": "unsubscribed"
}
```

OK Response

```
{
  "id": 123,
  "sid": 456,
  "seq": 222,
  "type": "ok",
  "msg": {
    "market_tickers": [
      "MARKET-1",
      "MARKET-2",
      "MARKET-3"
    ]
  }
}
```

List Subscriptions Response

```
{
  "id": 3,
  "type": "ok",
  "msg": [
    {
      "channel": "orderbook_delta",
      "sid": 1
    },
    {
      "channel": "ticker",
      "sid": 2
    },
    {
      "channel": "fill",
      "sid": 3
    }
  ]
}
```

Error Response

```
{
  "id": 123,
  "type": "error",
  "msg": {
    "code": 6,
    "msg": "Already subscribed"
  }
}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Bindings

method

type:string

GET

Send

Subscribe Command

type:object

show 3 properties

Subscribe to one or more channels

Unsubscribe Command

type:object

show 3 properties

Cancel one or more subscriptions

List Subscriptions Command

type:object

show 2 properties

List all active subscriptions

Update Subscription - Add Markets

type:object

show 3 properties

Add markets to an existing subscription

Update Subscription - Delete Markets

type:object

show 3 properties

Remove markets from an existing subscription

Update Subscription - Single SID Format

type:object

show 3 properties

Update subscription using sid parameter instead of sids array

Update Subscription - CF Benchmarks Indices

type:object

show 3 properties

Add or remove tracked index IDs, or list available indices, on a cfbenchmarks\_value subscription

Update Subscription - Pyth Underlyings

type:object

show 3 properties

Add or remove underlying tickers, or list available underlyings, on a pyth\_value subscription

Receive

Subscribed Response

type:object

show 3 properties

Confirmation that subscription was successful

Unsubscribed Response

type:object

show 4 properties

Confirmation that unsubscription was successful

OK Response

type:object

show 5 properties

Successful update operation response

List Subscriptions Response

type:object

show 3 properties

Response containing all active subscriptions

Error Response

type:object

show 3 properties

Error response for failed operations

[WebSocket API](https://docs.kalshi.com/websockets)[Connection Keep-Alive](https://docs.kalshi.com/websockets/connection-keep-alive)
