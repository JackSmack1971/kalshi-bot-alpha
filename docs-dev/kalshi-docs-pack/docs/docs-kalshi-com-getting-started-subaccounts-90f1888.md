---
title: "Subaccounts - API Documentation"
source_url: "https://docs.kalshi.com/getting_started/subaccounts"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:55.836Z"
---
Subaccounts let a **Direct** account partition its balance and positions into independent buckets under one set of API credentials. Every account has a primary subaccount (number `0`) and may use numbered subaccounts `1`–`63`.

Subaccounts are currently an **API-only** feature — they are not yet supported in the Kalshi web or mobile app. Numbered-subaccount balances and positions are managed through the trade API.

##

[​

](https://docs.kalshi.com/getting_started/subaccounts#numbering)

Numbering

| Number | Meaning |
| --- | --- |
| `0` | Primary subaccount (the default account) |
| `1`–`63` | User-managed numbered subaccounts |

##

[​

](https://docs.kalshi.com/getting_started/subaccounts#transfers)

Transfers

You can move cash between your own subaccounts with `POST /portfolio/subaccounts/transfer` (amounts in cents). Transfers net to zero at the account level — nothing leaves your account. Transfers are idempotent on a client-supplied `client_transfer_id`: retrying with the same value returns `409` instead of applying the transfer twice.

##

[​

](https://docs.kalshi.com/getting_started/subaccounts#listing-transfers)

Listing transfers

`GET /portfolio/subaccounts/transfers` returns your subaccount transfers, paginated.

[Order Groups](https://docs.kalshi.com/getting_started/order_groups)[Fixed-Point Migration](https://docs.kalshi.com/getting_started/fixed_point_migration)
