---
title: "Pyth Value Feed - API Documentation"
source_url: "https://docs.kalshi.com/websockets/pyth-value"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:58.589Z"
---
Messages

Pyth Value Update

```
{  "type": "pyth_value",  "sid": 1,  "seq": 42,  "msg": {    "underlying_ticker": "Metal.XAU/USD",    "value_usd": "2365.12345000",    "source_ts_ms": 1710000000100,    "received_at": 1710000000123  }}
```

Pyth Underlying List

```
{  "type": "pyth_value_underlying_list",  "id": 2,  "sid": 1,  "seq": 1,  "msg": {    "underlying_tickers": [      "Metal.XAG/USD",      "Metal.XAU/USD"    ]  }}
```

WSS

pyth\_value

Messages

Pyth Value Update

```
{  "type": "pyth_value",  "sid": 1,  "seq": 42,  "msg": {    "underlying_ticker": "Metal.XAU/USD",    "value_usd": "2365.12345000",    "source_ts_ms": 1710000000100,    "received_at": 1710000000123  }}
```

Pyth Underlying List

```
{  "type": "pyth_value_underlying_list",  "id": 2,  "sid": 1,  "seq": 1,  "msg": {    "underlying_tickers": [      "Metal.XAG/USD",      "Metal.XAU/USD"    ]  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

Pyth Value Update

type:object

show 4 properties

Deduplicated real-time Pyth price for an underlying ticker

Pyth Underlying List

type:object

show 5 properties

Recently streamed Pyth underlying tickers

[CF Benchmarks Value Feed](https://docs.kalshi.com/websockets/cfbenchmarks-value)[Public Trades](https://docs.kalshi.com/websockets/public-trades)
