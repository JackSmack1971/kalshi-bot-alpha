---
title: "Get Historical Market - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/historical/get-historical-market"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:13.988Z"
---
Get Historical Market

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

404

500

```
{
  "market": {
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
}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

historical

/

markets

/

{ticker}

Try it

Get Historical Market

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

404

500

```
{
  "market": {
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
}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market#parameter-ticker)

ticker

string

required

Market ticker

#### Response

200

application/json

Historical market retrieved successfully

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market#response-market)

market

object

required

Show child attributes

[Get Historical Markets](https://docs.kalshi.com/api-reference/historical/get-historical-markets)[CF Benchmarks REST Passthrough](https://docs.kalshi.com/cfbenchmarks/rest-passthrough)
