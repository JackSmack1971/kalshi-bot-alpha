---
title: "Market & Event Lifecycle - API Documentation"
source_url: "https://docs.kalshi.com/websockets/market-and-event-lifecycle"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:59.133Z"
---
Messages

Market Lifecycle V2

```
{  "type": "market_lifecycle_v2",  "sid": 13,  "msg": {    "market_ticker": "INXD-23SEP14-B4487",    "event_type": "created",    "open_ts": 1694635200,    "close_ts": 1694721600,    "price_level_structure": "linear_cent",    "additional_metadata": {      "name": "S&P 500 daily return on Sep 14",      "title": "S&P 500 closes up by 0.02% or more",      "yes_sub_title": "S&P 500 closes up 0.02%+",      "no_sub_title": "S&P 500 closes up <0.02%",      "rules_primary": "The S&P 500 index level at 4:00 PM ET...",      "rules_secondary": "",      "can_close_early": true,      "event_ticker": "INXD-23SEP14",      "expected_expiration_ts": 1694721600,      "strike_type": "greater",      "floor_strike": 4487    }  }}
```

Event Lifecycle

```
{  "type": "event_lifecycle",  "sid": 5,  "msg": {    "event_ticker": "KXQUICKSETTLE-26JAN25H2150",    "title": "What will 1+1 equal on Jan 25 at 21:50?",    "subtitle": "Jan 25 at 21:50",    "collateral_return_type": "MECNET",    "series_ticker": "KXQUICKSETTLE"  }}
```

Event Fee Override Update

```
{  "type": "event_fee_update",  "sid": 5,  "msg": {    "event_ticker": "KXBTCD-26MAY2018",    "fee_type_override": "quadratic",    "fee_multiplier_override": 1  }}
```

WSS

market\_lifecycle\_v2

Messages

Market Lifecycle V2

```
{  "type": "market_lifecycle_v2",  "sid": 13,  "msg": {    "market_ticker": "INXD-23SEP14-B4487",    "event_type": "created",    "open_ts": 1694635200,    "close_ts": 1694721600,    "price_level_structure": "linear_cent",    "additional_metadata": {      "name": "S&P 500 daily return on Sep 14",      "title": "S&P 500 closes up by 0.02% or more",      "yes_sub_title": "S&P 500 closes up 0.02%+",      "no_sub_title": "S&P 500 closes up <0.02%",      "rules_primary": "The S&P 500 index level at 4:00 PM ET...",      "rules_secondary": "",      "can_close_early": true,      "event_ticker": "INXD-23SEP14",      "expected_expiration_ts": 1694721600,      "strike_type": "greater",      "floor_strike": 4487    }  }}
```

Event Lifecycle

```
{  "type": "event_lifecycle",  "sid": 5,  "msg": {    "event_ticker": "KXQUICKSETTLE-26JAN25H2150",    "title": "What will 1+1 equal on Jan 25 at 21:50?",    "subtitle": "Jan 25 at 21:50",    "collateral_return_type": "MECNET",    "series_ticker": "KXQUICKSETTLE"  }}
```

Event Fee Override Update

```
{  "type": "event_fee_update",  "sid": 5,  "msg": {    "event_ticker": "KXBTCD-26MAY2018",    "fee_type_override": "quadratic",    "fee_multiplier_override": 1  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Market Lifecycle V2

type:object

show 3 properties

Market lifecycle events (created, activated, deactivated, close\_date\_updated, determined, settled, price\_level\_structure\_updated, metadata\_updated)

Event Lifecycle

type:object

show 3 properties

Event creation notification

Event Fee Override Update

type:object

show 3 properties

Emitted when an event-level fee override is set or cleared

[Market Positions](https://docs.kalshi.com/websockets/market-positions)[Multivariate Market & Event Lifecycle](https://docs.kalshi.com/websockets/multivariate-market-and-event-lifecycle)
