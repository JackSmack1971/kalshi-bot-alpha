---
title: "Get Fills - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/get-fills"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:10.551Z"
---
Get Fills

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/fills \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/fills"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/fills', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/fills",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/fills"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/fills")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/fills")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

```
{
  "fills": [
    {
      "fill_id": "<string>",
      "trade_id": "<string>",
      "order_id": "<string>",
      "ticker": "<string>",
      "market_ticker": "<string>",
      "count_fp": "10.00",
      "yes_price_dollars": "0.5600",
      "no_price_dollars": "0.5600",
      "is_taker": true,
      "fee_cost": "0.5600",
      "created_time": "2023-11-07T05:31:56Z",
      "subaccount_number": 123,
      "ts": 123
    }
  ],
  "cursor": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

fills

Try it

Get Fills

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/fills \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/fills"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/fills', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/fills",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/fills"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/fills")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/fills")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

```
{
  "fills": [
    {
      "fill_id": "<string>",
      "trade_id": "<string>",
      "order_id": "<string>",
      "ticker": "<string>",
      "market_ticker": "<string>",
      "count_fp": "10.00",
      "yes_price_dollars": "0.5600",
      "no_price_dollars": "0.5600",
      "is_taker": true,
      "fee_cost": "0.5600",
      "created_time": "2023-11-07T05:31:56Z",
      "subaccount_number": 123,
      "ts": 123
    }
  ],
  "cursor": "<string>"
}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-ticker)

ticker

string

Filter by market ticker

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-order-id)

order\_id

string

Filter by order ID

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-min-ts)

min\_ts

integer<int64>

Filter items after this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-max-ts)

max\_ts

integer<int64>

Filter items before this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-limit)

limit

integer<int64>

default:100

Number of results per page. Defaults to 100.

Required range: `1 <= x <= 1000`

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#parameter-subaccount)

subaccount

integer

Subaccount number (0 for primary, 1-63 for subaccounts). If omitted, defaults to all subaccounts.

#### Response

200

application/json

Fills retrieved successfully

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#response-fills)

fills

object\[\]

required

Show child attributes

[​

](https://docs.kalshi.com/api-reference/portfolio/get-fills#response-cursor)

cursor

string

required

[Get Total Resting Order Value](https://docs.kalshi.com/api-reference/portfolio/get-total-resting-order-value)[Get Communications ID](https://docs.kalshi.com/api-reference/communications/get-communications-id)
