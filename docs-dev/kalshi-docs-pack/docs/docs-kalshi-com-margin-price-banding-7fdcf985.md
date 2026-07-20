---
title: "Price Banding - API Documentation"
source_url: "https://docs.kalshi.com/margin/price-banding"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.161Z"
---
For perpetual markets, prices move in `0.0001` dollar ticks. Bids must be at least the lower of 80% of the best bid or 1,000 ticks below the best bid. Asks must be at most the higher of 120% of the best ask or 1,000 ticks above the best ask. **Notes**

-   Resting orders will not be canceled due to the price band movement.
-   If there are no resting orders on that side, there is no band limit for that side.
-   Order amends outside the price band are not allowed.

[Perps API](https://docs.kalshi.com/margin)[Get Perps Account API Limits](https://docs.kalshi.com/margin-rest/account/get-perps-account-api-limits)
