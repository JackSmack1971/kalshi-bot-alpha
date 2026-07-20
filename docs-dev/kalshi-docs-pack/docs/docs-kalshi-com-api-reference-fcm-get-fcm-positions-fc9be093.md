---
title: "Get FCM Positions - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/fcm/get-fcm-positions"
host: "docs.kalshi.com"
depth: 5
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:25.842Z"
---
Get FCM Positions

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/fcm/positions \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/fcm/positions"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/fcm/positions', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/fcm/positions",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/fcm/positions"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/fcm/positions")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/fcm/positions")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

```
{
  "market_positions": [
    {
      "ticker": "<string>",
      "total_traded_dollars": "0.5600",
      "position_fp": "10.00",
      "market_exposure_dollars": "0.5600",
      "realized_pnl_dollars": "0.5600",
      "fees_paid_dollars": "0.5600",
      "last_updated_ts": "2023-11-07T05:31:56Z"
    }
  ],
  "event_positions": [
    {
      "event_ticker": "<string>",
      "total_cost_dollars": "0.5600",
      "total_cost_shares_fp": "10.00",
      "event_exposure_dollars": "0.5600",
      "realized_pnl_dollars": "0.5600",
      "fees_paid_dollars": "0.5600"
    }
  ],
  "cursor": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

fcm

/

positions

Try it

Get FCM Positions

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/fcm/positions \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/fcm/positions"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/fcm/positions', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/fcm/positions",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/fcm/positions"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/fcm/positions")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/fcm/positions")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

```
{
  "market_positions": [
    {
      "ticker": "<string>",
      "total_traded_dollars": "0.5600",
      "position_fp": "10.00",
      "market_exposure_dollars": "0.5600",
      "realized_pnl_dollars": "0.5600",
      "fees_paid_dollars": "0.5600",
      "last_updated_ts": "2023-11-07T05:31:56Z"
    }
  ],
  "event_positions": [
    {
      "event_ticker": "<string>",
      "total_cost_dollars": "0.5600",
      "total_cost_shares_fp": "10.00",
      "event_exposure_dollars": "0.5600",
      "realized_pnl_dollars": "0.5600",
      "fees_paid_dollars": "0.5600"
    }
  ],
  "cursor": "<string>"
}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-subtrader-id)

subtrader\_id

string

required

Restricts the response to positions for a specific subtrader (FCM members only)

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-ticker)

ticker

string

Ticker of desired positions

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-event-ticker)

event\_ticker

string

Event ticker of desired positions

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-count-filter)

count\_filter

string

Restricts the positions to those with any of following fields with non-zero values, as a comma separated list

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-settlement-status)

settlement\_status

enum<string>

Settlement status of the markets to return. Defaults to unsettled

Available options:

`all`,

`unsettled`,

`settled`

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-limit)

limit

integer

Parameter to specify the number of results per page. Defaults to 100

Required range: `1 <= x <= 1000`

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#parameter-cursor)

cursor

string

The Cursor represents a pointer to the next page of records in the pagination

#### Response

200

application/json

Positions retrieved successfully

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#response-market-positions)

market\_positions

object\[\]

required

List of market positions

Show child attributes

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#response-event-positions)

event\_positions

object\[\]

required

List of event positions

Show child attributes

[​

](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions#response-cursor)

cursor

string

The Cursor represents a pointer to the next page of records in the pagination. Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records. An empty value of this field indicates there is no next page.

[Get FCM Orders](https://docs.kalshi.com/api-reference/fcm/get-fcm-orders)[Get Historical Cutoff Timestamps](https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps)
