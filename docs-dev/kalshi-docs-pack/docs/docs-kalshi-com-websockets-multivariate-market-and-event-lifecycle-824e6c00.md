---
title: "Multivariate Market & Event Lifecycle - API Documentation"
source_url: "https://docs.kalshi.com/websockets/multivariate-market-and-event-lifecycle"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.255Z"
---
Messages

Multivariate Market Lifecycle

```
{  "type": "multivariate_market_lifecycle",  "sid": 14,  "msg": {    "market_ticker": "KXMVE-TEST-EVENT-M1",    "event_type": "created",    "open_ts": 1773936000,    "close_ts": 1774022400,    "additional_metadata": {      "name": "MVE One",      "title": "Market 1",      "yes_sub_title": "YES 1",      "no_sub_title": "NO 1",      "rules_primary": "Rule 1",      "rules_secondary": "Rule 2",      "can_close_early": true,      "event_ticker": "KXMVE-TEST-EVENT",      "expected_expiration_ts": 1774029600    }  }}
```

Event Lifecycle

```
{  "type": "event_lifecycle",  "sid": 5,  "msg": {    "event_ticker": "KXQUICKSETTLE-26JAN25H2150",    "title": "What will 1+1 equal on Jan 25 at 21:50?",    "subtitle": "Jan 25 at 21:50",    "collateral_return_type": "MECNET",    "series_ticker": "KXQUICKSETTLE"  }}
```

WSS

multivariate\_market\_lifecycle

Messages

Multivariate Market Lifecycle

```
{  "type": "multivariate_market_lifecycle",  "sid": 14,  "msg": {    "market_ticker": "KXMVE-TEST-EVENT-M1",    "event_type": "created",    "open_ts": 1773936000,    "close_ts": 1774022400,    "additional_metadata": {      "name": "MVE One",      "title": "Market 1",      "yes_sub_title": "YES 1",      "no_sub_title": "NO 1",      "rules_primary": "Rule 1",      "rules_secondary": "Rule 2",      "can_close_early": true,      "event_ticker": "KXMVE-TEST-EVENT",      "expected_expiration_ts": 1774029600    }  }}
```

Event Lifecycle

```
{  "type": "event_lifecycle",  "sid": 5,  "msg": {    "event_ticker": "KXQUICKSETTLE-26JAN25H2150",    "title": "What will 1+1 equal on Jan 25 at 21:50?",    "subtitle": "Jan 25 at 21:50",    "collateral_return_type": "MECNET",    "series_ticker": "KXQUICKSETTLE"  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Multivariate Market Lifecycle

Multivariate market lifecycle events (created, activated, deactivated, close\_date\_updated, determined, settled)

Event Lifecycle

type:object

show 3 properties

Event creation notification

[Market & Event Lifecycle](https://docs.kalshi.com/websockets/market-and-event-lifecycle)[Multivariate Lookups (Deprecated)](https://docs.kalshi.com/websockets/multivariate-lookups-deprecated)
