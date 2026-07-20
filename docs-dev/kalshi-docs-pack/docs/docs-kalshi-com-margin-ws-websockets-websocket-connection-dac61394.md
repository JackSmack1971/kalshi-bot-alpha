---
title: "WebSocket Connection - API Documentation"
source_url: "https://docs.kalshi.com/margin-ws/websockets/websocket-connection"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.297Z"
---
Messages

Subscribe Command

```
No examples found
```

Unsubscribe Command

```
No examples found
```

List Subscriptions Command

```
{  "id": 123,  "cmd": "<string>"}
```

Update Subscription - Add Markets

```
No examples found
```

Update Subscription - Delete Markets

```
No examples found
```

Update Subscription - Single SID

```
No examples found
```

Subscribed Response

```
{  "id": 123,  "type": "<string>",  "msg": {    "channel": "<string>",    "sid": 123  }}
```

Unsubscribed Response

```
{  "id": 123,  "sid": 123,  "seq": 123,  "type": "<string>"}
```

OK Response

```
No examples found
```

List Subscriptions Response

```
{  "id": 123,  "type": "<string>",  "msg": {    "channel": "<string>",    "sid": 123  }}
```

Error Response

```
{  "id": 123,  "type": "<string>",  "msg": {    "code": 123,    "msg": "<string>",    "market_ticker": "<string>"  }}
```

WSS

wss://external-api-margin-ws.kalshi.comwss://external-api-margin-ws.demo.kalshi.co

/

Messages

Subscribe Command

```
No examples found
```

Unsubscribe Command

```
No examples found
```

List Subscriptions Command

```
{  "id": 123,  "cmd": "<string>"}
```

Update Subscription - Add Markets

```
No examples found
```

Update Subscription - Delete Markets

```
No examples found
```

Update Subscription - Single SID

```
No examples found
```

Subscribed Response

```
{  "id": 123,  "type": "<string>",  "msg": {    "channel": "<string>",    "sid": 123  }}
```

Unsubscribed Response

```
{  "id": 123,  "sid": 123,  "seq": 123,  "type": "<string>"}
```

OK Response

```
No examples found
```

List Subscriptions Response

```
{  "id": 123,  "type": "<string>",  "msg": {    "channel": "<string>",    "sid": 123  }}
```

Error Response

```
{  "id": 123,  "type": "<string>",  "msg": {    "code": 123,    "msg": "<string>",    "market_ticker": "<string>"  }}
```

Security Schemes

apiKey

type:apiKey

API key authentication required for margin WebSocket connections.

Bindings

method

type:string

GET

Send

Subscribe Command

type:object

show 3 properties

Subscribe to one or more margin channels

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

Update Subscription - Single SID

type:object

show 3 properties

Update a subscription using `sid` rather than `sids`

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

[Update Order Group Limit](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit)[Connection Keep-Alive](https://docs.kalshi.com/margin-ws/websockets/connection-keep-alive)
