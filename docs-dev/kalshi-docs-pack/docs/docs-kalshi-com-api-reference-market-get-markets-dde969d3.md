---
title: "Get Markets - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/market/get-markets"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:57.017Z"
---
Get Markets

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/markets
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/markets"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/markets', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/markets",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/markets"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/markets")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/markets")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "markets": [
    {
      "ticker": "<string>",
      "event_ticker": "<string>",
      "yes_sub_title": "<string>",
      "no_sub_title": "<string>",
      "created_time": "2023-11-07T05:31:56Z",
      "updated_time": "2023-11-07T05:31:56Z",
      "open_time": "2023-11-07T05:31:56Z",
      "close_time": "2023-11-07T05:31:56Z",
      "latest_expiration_time": "2023-11-07T05:31:56Z",
      "settlement_timer_seconds": 123,
      "yes_bid_dollars": "0.5600",
      "yes_bid_size_fp": "10.00",
      "yes_ask_dollars": "0.5600",
      "yes_ask_size_fp": "10.00",
      "no_bid_dollars": "0.5600",
      "no_ask_dollars": "0.5600",
      "last_price_dollars": "0.5600",
      "volume_fp": "10.00",
      "volume_24h_fp": "10.00",
      "can_close_early": true,
      "open_interest_fp": "10.00",
      "notional_value_dollars": "0.5600",
      "previous_yes_bid_dollars": "0.5600",
      "previous_yes_ask_dollars": "0.5600",
      "previous_price_dollars": "0.5600",
      "expiration_value": "<string>",
      "rules_primary": "<string>",
      "rules_secondary": "<string>",
      "price_level_structure": "<string>",
      "price_ranges": [
        {
          "start": "<string>",
          "end": "<string>",
          "step": "<string>"
        }
      ],
      "title": "<string>",
      "subtitle": "<string>",
      "expected_expiration_time": "2023-11-07T05:31:56Z",
      "expiration_time": "2023-11-07T05:31:56Z",
      "liquidity_dollars": "0.5600",
      "settlement_value_dollars": "0.5600",
      "settlement_ts": "2023-11-07T05:31:56Z",
      "occurrence_datetime": "2023-11-07T05:31:56Z",
      "fee_waiver_expiration_time": "2023-11-07T05:31:56Z",
      "early_close_condition": "<string>",
      "floor_strike": 123,
      "cap_strike": 123,
      "functional_strike": "<string>",
      "custom_strike": {},
      "mve_collection_ticker": "<string>",
      "mve_selected_legs": [
        {
          "event_ticker": "<string>",
          "market_ticker": "<string>",
          "side": "<string>",
          "yes_settlement_value_dollars": "0.5600"
        }
      ],
      "primary_participant_key": "<string>",
      "is_provisional": true,
      "exchange_index": 0
    }
  ],
  "cursor": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

markets

Try it

Get Markets

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/markets
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/markets"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/markets', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/markets",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/markets"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/markets")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/markets")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "markets": [
    {
      "ticker": "<string>",
      "event_ticker": "<string>",
      "yes_sub_title": "<string>",
      "no_sub_title": "<string>",
      "created_time": "2023-11-07T05:31:56Z",
      "updated_time": "2023-11-07T05:31:56Z",
      "open_time": "2023-11-07T05:31:56Z",
      "close_time": "2023-11-07T05:31:56Z",
      "latest_expiration_time": "2023-11-07T05:31:56Z",
      "settlement_timer_seconds": 123,
      "yes_bid_dollars": "0.5600",
      "yes_bid_size_fp": "10.00",
      "yes_ask_dollars": "0.5600",
      "yes_ask_size_fp": "10.00",
      "no_bid_dollars": "0.5600",
      "no_ask_dollars": "0.5600",
      "last_price_dollars": "0.5600",
      "volume_fp": "10.00",
      "volume_24h_fp": "10.00",
      "can_close_early": true,
      "open_interest_fp": "10.00",
      "notional_value_dollars": "0.5600",
      "previous_yes_bid_dollars": "0.5600",
      "previous_yes_ask_dollars": "0.5600",
      "previous_price_dollars": "0.5600",
      "expiration_value": "<string>",
      "rules_primary": "<string>",
      "rules_secondary": "<string>",
      "price_level_structure": "<string>",
      "price_ranges": [
        {
          "start": "<string>",
          "end": "<string>",
          "step": "<string>"
        }
      ],
      "title": "<string>",
      "subtitle": "<string>",
      "expected_expiration_time": "2023-11-07T05:31:56Z",
      "expiration_time": "2023-11-07T05:31:56Z",
      "liquidity_dollars": "0.5600",
      "settlement_value_dollars": "0.5600",
      "settlement_ts": "2023-11-07T05:31:56Z",
      "occurrence_datetime": "2023-11-07T05:31:56Z",
      "fee_waiver_expiration_time": "2023-11-07T05:31:56Z",
      "early_close_condition": "<string>",
      "floor_strike": 123,
      "cap_strike": 123,
      "functional_strike": "<string>",
      "custom_strike": {},
      "mve_collection_ticker": "<string>",
      "mve_selected_legs": [
        {
          "event_ticker": "<string>",
          "market_ticker": "<string>",
          "side": "<string>",
          "yes_settlement_value_dollars": "0.5600"
        }
      ],
      "primary_participant_key": "<string>",
      "is_provisional": true,
      "exchange_index": 0
    }
  ],
  "cursor": "<string>"
}
```

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-limit)

limit

integer<int64>

default:100

Number of results per page. Defaults to 100. Maximum value is 1000.

Required range: `0 <= x <= 1000`

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-event-ticker)

event\_ticker

string

Event ticker to filter by. Only a single event ticker is supported.

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-series-ticker)

series\_ticker

string

Filter by series ticker

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-min-created-ts)

min\_created\_ts

integer<int64>

Filter items that created after this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-max-created-ts)

max\_created\_ts

integer<int64>

Filter items that created before this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-min-updated-ts)

min\_updated\_ts

integer<int64>

Return markets with metadata updated later than this Unix timestamp. Tracks non-trading changes only. Incompatible with any other filters except mve\_filter=exclude. May be combined with series\_ticker, which requires mve\_filter=exclude.

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-max-close-ts)

max\_close\_ts

integer<int64>

Filter items that close before this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-min-close-ts)

min\_close\_ts

integer<int64>

Filter items that close after this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-min-settled-ts)

min\_settled\_ts

integer<int64>

Filter items that settled after this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-max-settled-ts)

max\_settled\_ts

integer<int64>

Filter items that settled before this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-status)

status

enum<string>

Filter by market status. Leave empty to return markets with any status.

Available options:

`unopened`,

`open`,

`paused`,

`closed`,

`settled`

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-tickers)

tickers

string

Filter by specific market tickers. Comma-separated list of market tickers to retrieve.

[​

](https://docs.kalshi.com/api-reference/market/get-markets#parameter-mve-filter)

mve\_filter

enum<string>

Filter by multivariate events (combos). 'only' returns only multivariate events, 'exclude' excludes multivariate events.

Available options:

`only`,

`exclude`

#### Response

200

application/json

Markets retrieved successfully

[​

](https://docs.kalshi.com/api-reference/market/get-markets#response-markets)

markets

object\[\]

required

Show child attributes

[​

](https://docs.kalshi.com/api-reference/market/get-markets#response-cursor)

cursor

string

required

[Get Series List](https://docs.kalshi.com/api-reference/market/get-series-list)[Get Market](https://docs.kalshi.com/api-reference/market/get-market)
