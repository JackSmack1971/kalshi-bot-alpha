---
title: "Kalshi SDKs - API Documentation"
source_url: "https://docs.kalshi.com/sdks/overview"
host: "docs.kalshi.com"
depth: 0
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:52.769Z"
---
Kalshi publishes Python and TypeScript SDKs to help you get started quickly.

SDKs are updated periodically and may lag the API. Active traders should treat the REST [OpenAPI specification](https://docs.kalshi.com/openapi.yaml) and WebSocket [AsyncAPI specification](https://docs.kalshi.com/asyncapi.yaml) as the source of truth. For production, we recommend generating your own client from those specs — or integrating directly — for full control over your implementation.

##

[​

](https://docs.kalshi.com/sdks/overview#packages)

Packages

## Python (sync)

`pip install kalshi_python_sync`

## Python (async)

`pip install kalshi_python_async`

## TypeScript

`npm install kalshi-typescript`

The old `kalshi-python` package is deprecated — use `kalshi_python_sync` or `kalshi_python_async`.

SDK releases track the [OpenAPI specification](https://docs.kalshi.com/openapi.yaml) and are generally published Tuesday–Wednesday each week, ahead of the corresponding API changes; check the package pages and the [API Changelog](https://docs.kalshi.com/changelog) for updates. All SDKs authenticate with an API key and RSA-PSS request signing — see [API Keys](https://docs.kalshi.com/getting_started/api_keys) for setup.

[Quick Start: WebSockets](https://docs.kalshi.com/getting_started/quick_start_websockets)
