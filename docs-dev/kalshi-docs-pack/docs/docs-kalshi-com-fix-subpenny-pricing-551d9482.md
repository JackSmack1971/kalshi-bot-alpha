---
title: "Subpenny Pricing - API Documentation"
source_url: "https://docs.kalshi.com/fix/subpenny-pricing"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:02.020Z"
---
For the general overview of fixed-point pricing and contract quantities across REST and WebSocket APIs, see [Fixed-Point Migration](https://docs.kalshi.com/getting_started/fixed_point_migration).

##

[​

](https://docs.kalshi.com/fix/subpenny-pricing#technical-specification)

Technical Specification

To enable subpenny precision, include tag **21005** in your Logon message:

| Tag | Name | Description | Value |
| --- | --- | --- | --- |
| 21005 | UseDollars | Enable dollar-based price format | Y |

Overview:

-   **Legacy Format (Cents)**: Prices given in whole cents. E.g. 72 cents = `72`.
-   **New Format (Dollars)**: Prices normalized to dollars with fixed precision (up to 4 decimal places).

Examples:

| Cents | FIX Decimal | String Representation |
| --- | --- | --- |
| 1.23¢ | Decimal(123, -4) | 0.0123 |
| 72.5¢ | Decimal(7250, -4) | 0.725 |
| 99¢ | Decimal(9900, -4) | 0.99 |

Affected Tags:

| Tag | Field Name | Description |
| --- | --- | --- |
| 6 | AvgPx | Average price of fills |
| 31 | LastPx | Price of last fill |
| 44 | Price | Order limit price |
| 132 | BidPx | Quote bid price |
| 133 | OfferPx | Quote ask price |

##

[​

](https://docs.kalshi.com/fix/subpenny-pricing#sample-messages)

Sample Messages

logon

```
8=FIXT.1.1|9=300|35=A|34=1|52=20250926-21:54:07.001|
96=QhA8659Mhygcm+xE/wb1m...|21005=Y|
                            ^^ Enable dollar format
```

new order single

```
8=FIXT.1.1|9=200|35=D|34=2|52=20250926-21:54:16.040|
38=100.0|40=2|44=0.7500|54=1|60=20250926-21:54:16.040|
              ^^ price
10=092|
```

execution report

```
8=FIXT.1.1|9=400|35=8|34=4|52=20250926-21:54:16.159|
6=0.6600|14=100|31=0.7000|32=60|38=100.0000|39=2|44=0.7500|
^^ avgPx        ^^ lastPx                        ^^ price
```

[Error Handling](https://docs.kalshi.com/fix/error-handling)
