---
title: "Get Balance - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/get-balance"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:16.111Z"
---
Get Balance

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/balance \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/balance"

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

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/balance', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/balance",
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/balance"

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
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/balance")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/balance")

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

500

```
{
  "balance": 123,
  "balance_dollars": "0.5600",
  "portfolio_value": 123,
  "updated_ts": 123,
  "balance_breakdown": [
    {
      "exchange_index": 0,
      "balance": "0.5600"
    }
  ]
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

balance

Try it

Get Balance

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/balance \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/balance"

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

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/balance', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/balance",
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/balance"

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
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/balance")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/balance")

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

500

```
{
  "balance": 123,
  "balance_dollars": "0.5600",
  "portfolio_value": 123,
  "updated_ts": 123,
  "balance_breakdown": [
    {
      "exchange_index": 0,
      "balance": "0.5600"
    }
  ]
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

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#parameter-subaccount)

subaccount

integer

Subaccount number (0 for primary, 1-63 for subaccounts). Defaults to 0.

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#parameter-exchange-index)

exchange\_index

integer

Identifier for an exchange shard. Defaults to 0 if unspecified. Note: currently only 0 supported.

Example:

`0`

#### Response

200

application/json

Balance retrieved successfully

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#response-balance)

balance

integer<int64>

required

Member's available balance in cents. This represents the amount available for trading.

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#response-balance-dollars)

balance\_dollars

string

required

Member's available balance as a fixed-point dollar string. This represents the amount available for trading.

Example:

`"0.5600"`

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#response-portfolio-value)

portfolio\_value

integer<int64>

required

Member's portfolio value in cents. This is the current value of all positions held.

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#response-updated-ts)

updated\_ts

integer<int64>

required

Unix timestamp of the last update to the balance.

[​

](https://docs.kalshi.com/api-reference/portfolio/get-balance#response-balance-breakdown)

balance\_breakdown

object\[\]

Balance broken down per exchange index.

Show child attributes

[Update Order Group Limit](https://docs.kalshi.com/api-reference/order-groups/update-order-group-limit)[Intra Account Transfer](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer)
