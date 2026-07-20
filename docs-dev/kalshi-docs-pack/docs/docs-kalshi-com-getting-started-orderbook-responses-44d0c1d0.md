---
title: "Orderbook Responses - API Documentation"
source_url: "https://docs.kalshi.com/getting_started/orderbook_responses"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:55.442Z"
---
##

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#getting-orderbook-data)

Getting Orderbook Data

The [Get Market Orderbook](https://docs.kalshi.com/api-reference/market/get-market-order-book) endpoint returns the current state of bids for a specific market.

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#request-format)

Request Format

```
GET /markets/{ticker}/orderbook
```

No authentication is required for this endpoint.

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#example-request)

Example Request

Python

JavaScript

cURL

```
import requests

# Get orderbook for a specific market
market_ticker = "KXHIGHNY-24JAN01-T60"
url = f"https://external-api.kalshi.com/trade-api/v2/markets/{market_ticker}/orderbook"

response = requests.get(url)
orderbook_data = response.json()
```

```
// Get orderbook for a specific market
const marketTicker = "KXHIGHNY-24JAN01-T60";
const url = `https://external-api.kalshi.com/trade-api/v2/markets/${marketTicker}/orderbook`;

fetch(url)
  .then(response => response.json())
  .then(data => console.log(data));
```

```
curl -X GET "https://external-api.kalshi.com/trade-api/v2/markets/KXHIGHNY-24JAN01-T60/orderbook"
```

##

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#response-structure)

Response Structure

The orderbook response is wrapped in an `orderbook_fp` object containing two arrays of bids: `yes_dollars` for YES positions and `no_dollars` for NO positions. Each bid is a two-element string array: `[price_dollars, count_fp]`.

-   **`price_dollars`**: Price as a dollar string (e.g., `"0.4200"` = $0.42)
-   **`count_fp`**: Number of contracts as a fixed-point string (e.g., `"13.00"` = 13 contracts)

Both values are strings to support subpenny pricing and fractional contract sizes. See [Fixed-Point Migration](https://docs.kalshi.com/getting_started/fixed_point_migration) for details.

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#example-response)

Example Response

```
{
  "orderbook_fp": {
    "yes_dollars": [
      ["0.0100", "200.00"],
      ["0.1500", "100.00"],
      ["0.2000", "50.00"],
      ["0.2500", "20.00"],
      ["0.3000", "11.00"],
      ["0.3100", "10.00"],
      ["0.3200", "10.00"],
      ["0.3300", "11.00"],
      ["0.3400", "9.00"],
      ["0.3500", "11.00"],
      ["0.4100", "10.00"],
      ["0.4200", "13.00"]
    ],
    "no_dollars": [
      ["0.0100", "100.00"],
      ["0.1600", "3.00"],
      ["0.2500", "50.00"],
      ["0.2800", "19.00"],
      ["0.3600", "5.00"],
      ["0.3700", "50.00"],
      ["0.3800", "300.00"],
      ["0.4400", "29.00"],
      ["0.4500", "20.00"],
      ["0.5600", "17.00"]
    ]
  }
}
```

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#understanding-the-arrays)

Understanding the Arrays

-   **First element**: Price in dollars as a string (e.g., `"0.4200"`)
-   **Second element**: Number of contracts as a fixed-point string (e.g., `"13.00"`)
-   Arrays are sorted by price in **ascending order**
-   The **highest** bid (best bid) is the **last** element in each array

##

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#why-only-bids)

Why Only Bids?

**Important**: Kalshi’s orderbook only returns bids, not asks. This is because in binary prediction markets, there’s a reciprocal relationship between YES and NO positions.

In binary prediction markets, every position has a complementary opposite:

-   A **YES BID** at price X is equivalent to a **NO ASK** at price ($1.00 - X)
-   A **NO BID** at price Y is equivalent to a **YES ASK** at price ($1.00 - Y)

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#the-reciprocal-relationship)

The Reciprocal Relationship

Since binary markets must sum to $1.00, these relationships always hold:

| Action | Equivalent To | Why |
| --- | --- | --- |
| YES BID at $0.60 | NO ASK at $0.40 | Willing to pay 0.60forYES\=Willingtoreceive0.60 for YES = Willing to receive 0.40 to take NO |
| NO BID at $0.30 | YES ASK at $0.70 | Willing to pay 0.30forNO\=Willingtoreceive0.30 for NO = Willing to receive 0.70 to take YES |

This reciprocal nature means that by showing only bids, the orderbook provides complete market information while avoiding redundancy.

##

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#calculating-spreads)

Calculating Spreads

To find the bid-ask spread for a market:

1.  **YES spread**:
    -   Best YES bid: Highest price in the `yes_dollars` array
    -   Best YES ask: $1.00 - (Highest price in the `no_dollars` array)
    -   Spread = Best YES ask - Best YES bid
2.  **NO spread**:
    -   Best NO bid: Highest price in the `no_dollars` array
    -   Best NO ask: $1.00 - (Highest price in the `yes_dollars` array)
    -   Spread = Best NO ask - Best NO bid

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#example-calculation)

Example Calculation

```
from decimal import Decimal

# Using the example orderbook above
best_yes_bid = Decimal("0.4200")  # Highest YES bid (last in array)
best_yes_ask = Decimal("1.00") - Decimal("0.5600")  # $1.00 - highest NO bid = $0.44

spread = best_yes_ask - best_yes_bid  # $0.44 - $0.42 = $0.02

# The spread is $0.02
# You can buy YES at $0.44 (implied ask) and sell at $0.42 (bid)
```

##

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#working-with-orderbook-data)

Working with Orderbook Data

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#display-best-prices)

Display Best Prices

Python

JavaScript

```
from decimal import Decimal

def display_best_prices(orderbook_data):
    """Display the best bid prices and implied asks"""
    ob = orderbook_data['orderbook_fp']

    # Best bids (if any exist)
    if ob.get('yes_dollars'):
        best_yes_bid = ob['yes_dollars'][-1][0]  # Last element is highest
        print(f"Best YES Bid: ${best_yes_bid}")

    if ob.get('no_dollars'):
        best_no_bid = ob['no_dollars'][-1][0]  # Last element is highest
        best_yes_ask = Decimal("1.00") - Decimal(best_no_bid)
        print(f"Best YES Ask: ${best_yes_ask} (implied from NO bid)")

    print()

    if ob.get('no_dollars'):
        best_no_bid = ob['no_dollars'][-1][0]  # Last element is highest
        print(f"Best NO Bid: ${best_no_bid}")

    if ob.get('yes_dollars'):
        best_yes_bid = ob['yes_dollars'][-1][0]  # Last element is highest
        best_no_ask = Decimal("1.00") - Decimal(best_yes_bid)
        print(f"Best NO Ask: ${best_no_ask} (implied from YES bid)")
```

```
function displayBestPrices(orderbookData) {
  const ob = orderbookData.orderbook_fp;

  // Best bids (if any exist)
  if (ob.yes_dollars && ob.yes_dollars.length > 0) {
    const bestYesBid = ob.yes_dollars[ob.yes_dollars.length - 1][0];
    console.log(`Best YES Bid: $${bestYesBid}`);
  }

  if (ob.no_dollars && ob.no_dollars.length > 0) {
    const bestNoBid = ob.no_dollars[ob.no_dollars.length - 1][0];
    const bestYesAsk = (1 - parseFloat(bestNoBid)).toFixed(4);
    console.log(`Best YES Ask: $${bestYesAsk} (implied from NO bid)`);
  }

  console.log();

  if (ob.no_dollars && ob.no_dollars.length > 0) {
    const bestNoBid = ob.no_dollars[ob.no_dollars.length - 1][0];
    console.log(`Best NO Bid: $${bestNoBid}`);
  }

  if (ob.yes_dollars && ob.yes_dollars.length > 0) {
    const bestYesBid = ob.yes_dollars[ob.yes_dollars.length - 1][0];
    const bestNoAsk = (1 - parseFloat(bestYesBid)).toFixed(4);
    console.log(`Best NO Ask: $${bestNoAsk} (implied from YES bid)`);
  }
}
```

###

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#calculate-market-depth)

Calculate Market Depth

```
from decimal import Decimal

def calculate_depth(orderbook_data, depth_dollars="0.05"):
    """Calculate total volume within X dollars of best bid"""
    ob = orderbook_data['orderbook_fp']
    depth = Decimal(depth_dollars)

    yes_depth = Decimal("0")
    no_depth = Decimal("0")

    # YES side depth (iterate backwards from best bid)
    if ob.get('yes_dollars'):
        best_yes = Decimal(ob['yes_dollars'][-1][0])
        for price_str, count_str in reversed(ob['yes_dollars']):
            if best_yes - Decimal(price_str) <= depth:
                yes_depth += Decimal(count_str)
            else:
                break

    # NO side depth (iterate backwards from best bid)
    if ob.get('no_dollars'):
        best_no = Decimal(ob['no_dollars'][-1][0])
        for price_str, count_str in reversed(ob['no_dollars']):
            if best_no - Decimal(price_str) <= depth:
                no_depth += Decimal(count_str)
            else:
                break

    return {"yes_depth": str(yes_depth), "no_depth": str(no_depth)}
```

##

[​

](https://docs.kalshi.com/getting_started/orderbook_responses#next-steps)

Next Steps

-   Learn about [making authenticated requests](https://docs.kalshi.com/getting_started/api_keys) to place orders
-   Explore [WebSocket connections](https://docs.kalshi.com/websockets) for real-time orderbook updates
-   Read about [market mechanics](https://kalshi.com/learn) on the Kalshi website

[Understanding Pagination](https://docs.kalshi.com/getting_started/pagination)[Order direction (outcome\_side and book\_side)](https://docs.kalshi.com/getting_started/order_direction)
