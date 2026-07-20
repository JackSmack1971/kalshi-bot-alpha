---
title: "CF Benchmarks Value Feed - API Documentation"
source_url: "https://docs.kalshi.com/websockets/cfbenchmarks-value"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:58.468Z"
---
Messages

CF Benchmarks Value Update

```
{  "type": "cfbenchmarks_value",  "sid": 1,  "seq": 42,  "msg": {    "index_id": "BRTI",    "received_at": 1710000000123,    "data": "{\"type\":\"value\",\"id\":\"BRTI\",\"time\":1710000000123,\"value\":\"68000.12\"}",    "avg_60s_data": {      "value": "68000.12000000",      "window_size": 3,      "window_start_ts_ms": 1709999940123,      "window_end_ts_exclusive": 1710000000123    },    "last_60s_windowed_average_15min": {      "value": "68000.23000000",      "window_size": 14,      "window_start_ts_ms": 1709999980000,      "window_end_ts_exclusive": 1710000000123    }  }}
```

CF Benchmarks Index List

```
{  "type": "cfbenchmarks_value_indexlist",  "id": 2,  "sid": 1,  "seq": 1,  "msg": {    "index_ids": [      "BRTI",      "ETHUSD_RTI"    ]  }}
```

WSS

cfbenchmarks\_value

Messages

CF Benchmarks Value Update

```
{  "type": "cfbenchmarks_value",  "sid": 1,  "seq": 42,  "msg": {    "index_id": "BRTI",    "received_at": 1710000000123,    "data": "{\"type\":\"value\",\"id\":\"BRTI\",\"time\":1710000000123,\"value\":\"68000.12\"}",    "avg_60s_data": {      "value": "68000.12000000",      "window_size": 3,      "window_start_ts_ms": 1709999940123,      "window_end_ts_exclusive": 1710000000123    },    "last_60s_windowed_average_15min": {      "value": "68000.23000000",      "window_size": 14,      "window_start_ts_ms": 1709999980000,      "window_end_ts_exclusive": 1710000000123    }  }}
```

CF Benchmarks Index List

```
{  "type": "cfbenchmarks_value_indexlist",  "id": 2,  "sid": 1,  "seq": 1,  "msg": {    "index_ids": [      "BRTI",      "ETHUSD_RTI"    ]  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for WebSocket connections. The API key should be provided during the WebSocket handshake.

Receive

CF Benchmarks Value Update

type:object

show 4 properties

Real-time CF Benchmarks index value with trailing 60-second and quarter-hour averages

CF Benchmarks Index List

type:object

show 5 properties

The set of available CF Benchmarks index IDs, sent in response to an indexlist action

[Market Ticker](https://docs.kalshi.com/websockets/market-ticker)[Pyth Value Feed](https://docs.kalshi.com/websockets/pyth-value)
