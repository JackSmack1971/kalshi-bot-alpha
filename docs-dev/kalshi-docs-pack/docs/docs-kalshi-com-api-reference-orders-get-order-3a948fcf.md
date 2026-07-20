---
title: "Get Order - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/orders/get-order"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:14.580Z"
---
Get Order

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id} \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}"

headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
const options = {
  method: 'GET',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'
  }
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "KALSHI-ACCESS-KEY: <api-key>",
    "KALSHI-ACCESS-SIGNATURE: <api-key>",
    "KALSHI-ACCESS-TIMESTAMP: <api-key>"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```
package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'

response = http.request(request)
puts response.read_body
```

200

401

404

500

```
{
  "order": {
    "order_id": "<string>",
    "user_id": "<string>",
    "client_order_id": "<string>",
    "ticker": "<string>",
    "yes_price_dollars": "0.5600",
    "no_price_dollars": "0.5600",
    "fill_count_fp": "10.00",
    "remaining_count_fp": "10.00",
    "initial_count_fp": "10.00",
    "taker_fill_cost_dollars": "0.5600",
    "maker_fill_cost_dollars": "0.5600",
    "taker_fees_dollars": "0.5600",
    "maker_fees_dollars": "0.5600",
    "expiration_time": "2023-11-07T05:31:56Z",
    "created_time": "2023-11-07T05:31:56Z",
    "last_update_time": "2023-11-07T05:31:56Z",
    "order_group_id": "<string>",
    "cancel_order_on_pause": true,
    "subaccount_number": 123,
    "exchange_index": 0
  }
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

orders

/

{order\_id}

Try it

Get Order

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id} \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}"

headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
const options = {
  method: 'GET',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'
  }
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "KALSHI-ACCESS-KEY: <api-key>",
    "KALSHI-ACCESS-SIGNATURE: <api-key>",
    "KALSHI-ACCESS-TIMESTAMP: <api-key>"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```
package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/orders/{order_id}")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'

response = http.request(request)
puts response.read_body
```

200

401

404

500

```
{
  "order": {
    "order_id": "<string>",
    "user_id": "<string>",
    "client_order_id": "<string>",
    "ticker": "<string>",
    "yes_price_dollars": "0.5600",
    "no_price_dollars": "0.5600",
    "fill_count_fp": "10.00",
    "remaining_count_fp": "10.00",
    "initial_count_fp": "10.00",
    "taker_fill_cost_dollars": "0.5600",
    "maker_fill_cost_dollars": "0.5600",
    "taker_fees_dollars": "0.5600",
    "maker_fees_dollars": "0.5600",
    "expiration_time": "2023-11-07T05:31:56Z",
    "created_time": "2023-11-07T05:31:56Z",
    "last_update_time": "2023-11-07T05:31:56Z",
    "order_group_id": "<string>",
    "cancel_order_on_pause": true,
    "subaccount_number": 123,
    "exchange_index": 0
  }
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

**Rate limit:** 2 tokens per request. See `GET /trade-api/v2/account/endpoint_costs` for current non-default endpoint costs.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/orders/get-order#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/orders/get-order#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/orders/get-order#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/orders/get-order#parameter-order-id)

order\_id

string

required

Order ID

#### Response

200

application/json

Order retrieved successfully

[​

](https://docs.kalshi.com/api-reference/orders/get-order#response-order)

order

object

required

Show child attributes

[Get Orders](https://docs.kalshi.com/api-reference/orders/get-orders)[Get Queue Positions for Orders](https://docs.kalshi.com/api-reference/orders/get-queue-positions-for-orders)
