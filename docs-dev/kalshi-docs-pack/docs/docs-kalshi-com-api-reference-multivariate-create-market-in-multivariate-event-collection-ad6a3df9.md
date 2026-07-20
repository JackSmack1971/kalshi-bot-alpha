---
title: "Create Market In Multivariate Event Collection - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:23.080Z"
---
Create Market In Multivariate Event Collection

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker} \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "selected_markets": [
    {
      "market_ticker": "<string>",
      "event_ticker": "<string>"
    }
  ],
  "with_market_payload": true
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"payload = {    "selected_markets": [        {            "market_ticker": "<string>",            "event_ticker": "<string>"        }    ],    "with_market_payload": True}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    selected_markets: [{market_ticker: '<string>', event_ticker: '<string>'}],    with_market_payload: true  })};fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'selected_markets' => [        [                'market_ticker' => '<string>',                'event_ticker' => '<string>'        ]    ],    'with_market_payload' => true  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"	payload := strings.NewReader("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ],\n  \"with_market_payload\": true\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ],\n  \"with_market_payload\": true\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ],\n  \"with_market_payload\": true\n}"response = http.request(request)puts response.read_body
```

200

400

401

429

500

```
{
  "event_ticker": "<string>",
  "market_ticker": "<string>",
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

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

POST

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

multivariate\_event\_collections

/

{collection\_ticker}

Try it

Create Market In Multivariate Event Collection

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker} \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "selected_markets": [
    {
      "market_ticker": "<string>",
      "event_ticker": "<string>"
    }
  ],
  "with_market_payload": true
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"payload = {    "selected_markets": [        {            "market_ticker": "<string>",            "event_ticker": "<string>"        }    ],    "with_market_payload": True}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    selected_markets: [{market_ticker: '<string>', event_ticker: '<string>'}],    with_market_payload: true  })};fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'selected_markets' => [        [                'market_ticker' => '<string>',                'event_ticker' => '<string>'        ]    ],    'with_market_payload' => true  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"	payload := strings.NewReader("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ],\n  \"with_market_payload\": true\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ],\n  \"with_market_payload\": true\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ],\n  \"with_market_payload\": true\n}"response = http.request(request)puts response.read_body
```

200

400

401

429

500

```
{
  "event_ticker": "<string>",
  "market_ticker": "<string>",
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

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#parameter-collection-ticker)

collection\_ticker

string

required

Collection ticker

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#body-selected-markets)

selected\_markets

object\[\]

required

List of selected markets that act as parameters to determine which market is created.

Show child attributes

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#body-with-market-payload)

with\_market\_payload

boolean

Whether to include the market payload in the response.

#### Response

200

application/json

Market created successfully

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#response-event-ticker)

event\_ticker

string

required

Event ticker for the created market.

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#response-market-ticker)

market\_ticker

string

required

Market ticker for the created market.

[​

](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection#response-market)

market

object

Market payload of the created market.

Show child attributes

[Get Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection)[Get Multivariate Event Collections](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections)
