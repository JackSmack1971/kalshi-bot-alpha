---
title: "Connection Keep-Alive - API Documentation"
source_url: "https://docs.kalshi.com/margin-ws/websockets/connection-keep-alive"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.431Z"
---
Messages

Ping

```
""
```

Pong

```
""
```

Ping

```
"heartbeat"
```

Pong

```
""
```

WSS

wss://external-api-margin-ws.kalshi.comwss://external-api-margin-ws.demo.kalshi.co

/

Messages

Ping

```
""
```

Pong

```
""
```

Ping

```
"heartbeat"
```

Pong

```
""
```

Security Schemes

apiKey

type:apiKey

API key authentication required for margin WebSocket connections.

Send

Ping

type:string

Client sends Ping frame (0x9) to elicit Pong from Kalshi

Pong

type:string

Client replies to Ping with Pong Frame (0xA)

Receive

Ping

type:string

Kalshi sends Ping (0x9) with body 'heartbeat' to elicit Pong from client

Pong

type:string

Kalshi responds to client Ping with Pong frame (0xA)

[WebSocket Connection](https://docs.kalshi.com/margin-ws/websockets/websocket-connection)[Orderbook Updates](https://docs.kalshi.com/margin-ws/websockets/orderbook-updates)
