---
title: "Market Data - API Documentation"
source_url: "https://docs.kalshi.com/fix/market-data"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:01.234Z"
---
Market data is available on the dedicated **KalshiMD** session. It supports order book snapshots, incremental updates, and per-market trading-status changes via [Security Status](https://docs.kalshi.com/fix/market-data#security-status). Subscriptions are identified by `Symbol<55>`. `KalshiMD` does not support message retransmission. Use `ResetSeqNumFlag<141>=Y` on Logon.

##

[​

](https://docs.kalshi.com/fix/market-data#message-flow)

Message Flow

##

[​

](https://docs.kalshi.com/fix/market-data#market-data-request-35=v)

Market Data Request (35=V)

| Tag | Name | Type | Required | Description |
| --- | --- | --- | --- | --- |
| 263 | SubscriptionRequestType | Char | Y | `0`\=Snapshot, `1`\=Snapshot plus updates, `2`\=Disable previous snapshot plus update request |
| 146 | NoRelatedSym | Integer | C | Number of `55=Symbol` entries in the repeating group that follows. Required for `263=0` and `263=1`. For `263=2`, the listed symbols are unsubscribed; omit to cancel all of the session’s subscriptions. |
| 55 | Symbol | String | C | Repeating group field. The market tickers to subscribe to or cancel. |

Example snapshot request

```
8=FIXT.1.1|35=V|49=your-api-key|56=KalshiMD|263=0|146=1|55=KXNBAGAME-26MAY25NYKCLE-NYK|
```

Example snapshot-plus-updates subscription

```
8=FIXT.1.1|35=V|49=your-api-key|56=KalshiMD|263=1|146=1|55=KXNBAGAME-26MAY25NYKCLE-NYK|
```

Example cancel a symbol

```
8=FIXT.1.1|35=V|49=your-api-key|56=KalshiMD|263=2|146=1|55=KXNBAGAME-26MAY25NYKCLE-NYK|
```

Example cancel all subscriptions

```
8=FIXT.1.1|35=V|49=your-api-key|56=KalshiMD|263=2|
```

##

[​

](https://docs.kalshi.com/fix/market-data#market-data-snapshot-full-refresh-35=w)

Market Data Snapshot Full Refresh (35=W)

Sent in response to a snapshot request and immediately after a snapshot-plus-updates subscription is accepted. Correlate by `Symbol<55>`.

| Tag | Name | Type | Required | Description |
| --- | --- | --- | --- | --- |
| 55 | Symbol | String | Y | Market ticker. |
| 268 | NoMDEntries | Integer | Y | Number of book levels. |
| 269 | MDEntryType | Char | Y | Repeating group field. `0`\=Bid, `1`\=Offer |
| 270 | MDEntryPx | Price | Y | Book level price in dollars. |
| 271 | MDEntrySize | Quantity | Y | Book level size in contracts. |

Example snapshot response

```
8=FIXT.1.1|35=W|49=KalshiMD|56=your-api-key|55=KXNBAGAME-26MAY25NYKCLE-NYK|268=2|269=0|270=0.3500|271=10.00|269=1|270=0.6500|271=5.00|
```

##

[​

](https://docs.kalshi.com/fix/market-data#market-data-incremental-refresh-35=x)

Market Data Incremental Refresh (35=X)

Sent after a subscribed market’s aggregated book levels change or a trade occurs. Correlate by `Symbol<55>` on each entry.

| Tag | Name | Type | Required | Description |
| --- | --- | --- | --- | --- |
| 268 | NoMDEntries | Integer | Y | Number of market data entries. |
| 279 | MDUpdateAction | Char | Y | Repeating group field. `0`\=New, `1`\=Change, `2`\=Delete. |
| 55 | Symbol | String | Y | Repeating group field. Market ticker. |
| 269 | MDEntryType | Char | Y | Repeating group field. `0`\=Bid, `1`\=Offer, `2`\=Trade |
| 270 | MDEntryPx | Price | Y | Price in dollars. |
| 271 | MDEntrySize | Quantity | Y | Size in contracts. |
| 2446 | AggressorSide | Char | C | Trade entries only. `1`\=Buy, `2`\=Sell. |

Example incremental update

```
8=FIXT.1.1|35=X|49=KalshiMD|56=your-api-key|268=1|279=1|55=KXNBAGAME-26MAY25NYKCLE-NYK|269=0|270=0.3500|271=15.00|
```

Example trade update

```
8=FIXT.1.1|35=X|49=KalshiMD|56=your-api-key|268=1|279=0|55=KXNBAGAME-26MAY25NYKCLE-NYK|269=2|270=0.6500|271=3.00|2446=1|
```

##

[​

](https://docs.kalshi.com/fix/market-data#market-data-request-reject-35=y)

Market Data Request Reject (35=Y)

Sent when a market data request cannot be accepted. Unknown market tickers are not currently rejected; the server sends an empty snapshot if it has no order book for the requested symbol.

| Tag | Name | Type | Required | Description |
| --- | --- | --- | --- | --- |
| 281 | MDReqRejReason | Char | N | Reject reason. |
| 58 | Text | String | N | Human-readable rejection detail. |

###

[​

](https://docs.kalshi.com/fix/market-data#common-reject-reasons-281)

Common Reject Reasons (281)

-   `2`\=Insufficient bandwidth, including request or session symbol limits
-   `4`\=Unsupported `SubscriptionRequestType`

##

[​

](https://docs.kalshi.com/fix/market-data#security-status)

Security Status

`KalshiMD` also streams per-market trading-status changes as `SecurityStatus<35=f>`. Subscribe by `Symbol<55>` with `SecurityStatusRequest<35=e>`. Updates are changes-only; no initial status is sent on subscribe.

###

[​

](https://docs.kalshi.com/fix/market-data#security-status-request-35=e)

Security Status Request (35=e)

| Tag | Name | Type | Required | Description |
| --- | --- | --- | --- | --- |
| 263 | SubscriptionRequestType | Char | Y | `1`\=Subscribe, `2`\=Unsubscribe. |
| 55 | Symbol | String | Y | The single market ticker to subscribe to or unsubscribe. |

Example subscribe

```
8=FIXT.1.1|35=e|49=your-api-key|56=KalshiMD|263=1|55=KXNBAGAME-26MAY25NYKCLE-NYK|
```

Example unsubscribe

```
8=FIXT.1.1|35=e|49=your-api-key|56=KalshiMD|263=2|55=KXNBAGAME-26MAY25NYKCLE-NYK|
```

###

[​

](https://docs.kalshi.com/fix/market-data#security-status-35=f)

Security Status (35=f)

Streamed when a subscribed market changes trading state. Correlate by `Symbol<55>`.

| Tag | Name | Type | Required | Description |
| --- | --- | --- | --- | --- |
| 55 | Symbol | String | Y | Market ticker. |
| 326 | SecurityTradingStatus | Int | Y | See [Trading Status Lifecycle](https://docs.kalshi.com/fix/market-data#trading-status-lifecycle-326). |

Example trading halt

```
8=FIXT.1.1|35=f|49=KalshiMD|56=your-api-key|55=KXNBAGAME-26MAY25NYKCLE-NYK|326=2|
```

###

[​

](https://docs.kalshi.com/fix/market-data#trading-status-lifecycle-326)

Trading Status Lifecycle (326)

-   `3`\=Resume: the market was activated and is open for trading
-   `2`\=Trading halt: the market was deactivated
-   `100`\=Kalshi determined: the market was determined; trading has ended and the result is known
-   `101`\=Kalshi settled: the market settled. The subscription for that symbol is then dropped.

Scheduled (time-based) opens and closes are not emitted as discrete events and are not reported here.

[Order Groups](https://docs.kalshi.com/fix/order-groups)[RFQ](https://docs.kalshi.com/fix/rfq-messages)
