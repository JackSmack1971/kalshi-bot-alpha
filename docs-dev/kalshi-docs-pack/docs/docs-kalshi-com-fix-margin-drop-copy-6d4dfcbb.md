---
title: "Drop Copy Session - API Documentation"
source_url: "https://docs.kalshi.com/fix-margin/drop-copy"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:03.861Z"
---
**This is not a traditional drop copy session.** Kalshi’s Drop Copy uses a request-response pattern for querying historical execution reports. For a real-time streaming feed, use a [Listener Session](https://docs.kalshi.com/fix-margin/listener-sessions) on KalshiRT instead.

Lookback window is limited to the last 3 hours. Only ExecutionReport (35=8) messages are returned. Rejects and pending orders (ExecID `"-1;-1"`) are excluded.

Resent messages have new FIX sequence numbers, different from their original numbers on the trading session. Use ExecID to reconcile.

##

[​

](https://docs.kalshi.com/fix-margin/drop-copy#eventresendrequest-35=u1)

EventResendRequest (35=U1)

Request execution reports within a specified ExecID range.

| Tag | Name | Description | Required |
| --- | --- | --- | --- |
| 21001 | BeginExecID | Starting ExecID (inclusive) | Yes |
| 21002 | EndExecID | Ending ExecID (inclusive). Defaults to latest ExecID if omitted. | No |

**Example:**

```
8=FIXT.1.1|35=U1|21001=12345;67890|21002=12350;67895|
```

##

[​

](https://docs.kalshi.com/fix-margin/drop-copy#eventresendcomplete-35=u2)

EventResendComplete (35=U2)

Sent after all requested events have been resent.

| Tag | Name | Description | Required |
| --- | --- | --- | --- |
| 45 | RefSeqNum | MsgSeqNum of the EventResendRequest | Yes |
| 21003 | ResendEventCount | Total number of events resent | Yes |

##

[​

](https://docs.kalshi.com/fix-margin/drop-copy#eventresendreject-35=u3)

EventResendReject (35=U3)

Sent when a resend request cannot be fulfilled.

| Tag | Name | Description | Required |
| --- | --- | --- | --- |
| 45 | RefSeqNum | MsgSeqNum of the EventResendRequest | Yes |
| 21004 | EventResendRejectReason | Rejection code: `1`\=Too many resend requests, `2`\=Server error, `3`\=BeginExecID too small (outside window), `4`\=EndExecID too large | Yes |

[Market Data](https://docs.kalshi.com/fix-margin/market-data)[Listener Sessions](https://docs.kalshi.com/fix-margin/listener-sessions)
