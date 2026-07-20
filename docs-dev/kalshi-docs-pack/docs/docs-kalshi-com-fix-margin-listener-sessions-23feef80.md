---
title: "Listener Sessions - API Documentation"
source_url: "https://docs.kalshi.com/fix-margin/listener-sessions"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:03.966Z"
---
##

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#overview)

Overview

A listener session provides a **real-time, read-only stream** of execution reports from your margin trading session. This is what most exchanges refer to as a “drop copy”: a live shadow feed of all fills and order state changes. Kalshi’s [Drop Copy session](https://docs.kalshi.com/fix-margin/drop-copy) (KalshiDC) is a separate request-response tool for querying historical execution reports, not a live feed.

##

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#how-it-works)

How It Works

A listener session is not a separate endpoint. It is a **mode** enabled on a standard KalshiNR or KalshiRT order entry session by setting `ListenerSession=Y` (tag 20126) during Logon. Once connected, the listener session receives the same execution reports as your active trading session in real time, but **cannot send any orders or modifications**. Listener sessions connect to the same KalshiNR or KalshiRT endpoints listed on the [Connectivity](https://docs.kalshi.com/fix-margin/connectivity) page. A **separate API key** is required (read-only scope is sufficient).

##

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#logon-configuration)

Logon Configuration

###

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#required-logon-fields)

Required Logon Fields

| Tag | Name | Value | Description |
| --- | --- | --- | --- |
| 20126 | ListenerSession | Y | Enables listen-only mode |
| 21011 | SkipPendingExecReports | Y | Required when ListenerSession=Y |

###

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#restrictions)

Restrictions

The following Logon flags are **not compatible** with listener sessions:

| Tag | Name | Restriction |
| --- | --- | --- |
| 8013 | CancelOrdersOnDisconnect | Must be N (or omitted) |

##

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#what-you-receive)

What You Receive

Listener sessions receive **ExecutionReport (35=8)** messages for all order activity on your account, including:

-   New order acknowledgements
-   Fills and partial fills
-   Order cancellations
-   Order replacements

##

[​

](https://docs.kalshi.com/fix-margin/listener-sessions#what-you-cannot-do)

What You Cannot Do

Listener sessions are strictly read-only. The following message types will be **rejected**:

-   NewOrderSingle (35=D)
-   OrderCancelRequest (35=F)
-   OrderCancelReplaceRequest (35=G)
-   OrderMassCancelRequest (35=q)

[Drop Copy Session](https://docs.kalshi.com/fix-margin/drop-copy)[Error Handling](https://docs.kalshi.com/fix-margin/error-handling)
