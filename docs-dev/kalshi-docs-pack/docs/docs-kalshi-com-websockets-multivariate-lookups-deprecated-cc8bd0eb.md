---
title: "Multivariate Lookups (Deprecated) - API Documentation"
source_url: "https://docs.kalshi.com/websockets/multivariate-lookups-deprecated"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.363Z"
---
Messages

Multivariate Lookup (Deprecated)

```
{  "type": "multivariate_lookup",  "sid": 13,  "msg": {    "collection_ticker": "KXOSCARWINNERS-25",    "event_ticker": "KXOSCARWINNERS-25C0CE5",    "market_ticker": "KXOSCARWINNERS-25C0CE5-36353",    "selected_markets": [      {        "event_ticker": "KXOSCARACTO-25",        "market_ticker": "KXOSCARACTO-25-AB",        "side": "yes"      },      {        "event_ticker": "KXOSCARACTR-25",        "market_ticker": "KXOSCARACTR-25-DM",        "side": "yes"      }    ]  }}
```

WSS

multivariate

Messages

Multivariate Lookup (Deprecated)

```
{  "type": "multivariate_lookup",  "sid": 13,  "msg": {    "collection_ticker": "KXOSCARWINNERS-25",    "event_ticker": "KXOSCARWINNERS-25C0CE5",    "market_ticker": "KXOSCARWINNERS-25C0CE5-36353",    "selected_markets": [      {        "event_ticker": "KXOSCARACTO-25",        "market_ticker": "KXOSCARACTO-25-AB",        "side": "yes"      },      {        "event_ticker": "KXOSCARACTR-25",        "market_ticker": "KXOSCARACTR-25-DM",        "side": "yes"      }    ]  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Multivariate Lookup (Deprecated)

type:object

show 3 properties

Deprecated multivariate collection lookup notification

[Multivariate Market & Event Lifecycle](https://docs.kalshi.com/websockets/multivariate-market-and-event-lifecycle)[Communications](https://docs.kalshi.com/websockets/communications)
