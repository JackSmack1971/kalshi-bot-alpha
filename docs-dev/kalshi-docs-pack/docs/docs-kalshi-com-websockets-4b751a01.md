---
title: "WebSocket API - API Documentation"
source_url: "https://docs.kalshi.com/websockets"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:57.826Z"
---
Use the dedicated Trade API WebSocket hosts for new integrations:

| Environment | WebSocket URL | Shared host, also supported |
| --- | --- | --- |
| Production | `wss://external-api-ws.kalshi.com/trade-api/ws/v2` | `wss://api.elections.kalshi.com/trade-api/ws/v2` |
| Demo | `wss://external-api-ws.demo.kalshi.co/trade-api/ws/v2` | `wss://demo-api.kalshi.co/trade-api/ws/v2` |

WebSocket connections use the same API key authentication and signing path as before. Only the hostname changes for the dedicated Trade API path.

-   For connection and subscription examples, see [Quick Start: WebSockets](https://docs.kalshi.com/getting_started/quick_start_websockets).
-   For all REST and WebSocket base URLs, see [API Environments and Endpoints](https://docs.kalshi.com/getting_started/api_environments).
-   To generate clients or inspect channel payloads directly, download the [AsyncAPI specification](https://docs.kalshi.com/asyncapi.yaml).
-   For detailed CF Benchmarks channel usage (`cfbenchmarks_value`), see [CF Benchmarks Value Feed](https://docs.kalshi.com/websockets/cfbenchmarks-value).
-   For real-time Pyth prices (`pyth_value`), see [Pyth Value Feed](https://docs.kalshi.com/websockets/pyth-value).

[CF Benchmarks REST Passthrough](https://docs.kalshi.com/cfbenchmarks/rest-passthrough)[WebSocket Connection](https://docs.kalshi.com/websockets/websocket-connection)
