---
title: "Market Settlement - API Documentation"
source_url: "https://docs.kalshi.com/getting_started/market_settlement"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:56.652Z"
---
Settlement occurs when a market’s outcome is determined. Positions are automatically resolved and funds transferred.

##

[​

](https://docs.kalshi.com/getting_started/market_settlement#how-it-works)

How It Works

-   **Yes outcome**: Yes contract holders receive $1 per contract
-   **No outcome**: No contract holders receive $1 per contract
-   Only net positions are settled (after netting)

##

[​

](https://docs.kalshi.com/getting_started/market_settlement#settlement-timing)

Settlement Timing

Markets typically settle shortly after expiration, but timing can vary based on market type, data source availability, and manual review requirements.

##

[​

](https://docs.kalshi.com/getting_started/market_settlement#fees)

Fees

Settlement fees are zero for simple yes/no determinations but may apply for sub-cent scalar settlement. The actual payout (`CollateralAmountChange`) is rounded to whole cents. `CollateralAmountChange + MiscFeeAmt` equals the pre-rounding settlement value.

##

[​

](https://docs.kalshi.com/getting_started/market_settlement#protocol-specific-details)

Protocol-Specific Details

-   [FIX Market Settlement Messages](https://docs.kalshi.com/fix/market-settlement)

[Maintenance and Pauses](https://docs.kalshi.com/getting_started/maintenance_and_pauses)[Request for Quote (RFQ)](https://docs.kalshi.com/getting_started/rfqs)
