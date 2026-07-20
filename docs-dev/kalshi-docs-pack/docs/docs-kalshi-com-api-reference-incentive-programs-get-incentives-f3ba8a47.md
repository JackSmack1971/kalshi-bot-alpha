---
title: "Get Incentives - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/incentive-programs/get-incentives"
host: "docs.kalshi.com"
depth: 5
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:25.681Z"
---
Get Incentives

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/incentive_programs
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/incentive_programs"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/incentive_programs', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/incentive_programs",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
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

	url := "https://external-api.kalshi.com/trade-api/v2/incentive_programs"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/incentive_programs")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/incentive_programs")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

400

500

```
{
  "incentive_programs": [
    {
      "id": "<string>",
      "market_id": "<string>",
      "market_ticker": "<string>",
      "incentive_description": "<string>",
      "start_date": "2023-11-07T05:31:56Z",
      "end_date": "2023-11-07T05:31:56Z",
      "period_reward": 123,
      "paid_out": true,
      "discount_factor_bps": 123,
      "target_size_fp": "10.00"
    }
  ],
  "next_cursor": "<string>"
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

incentive\_programs

Try it

Get Incentives

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/incentive_programs
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/incentive_programs"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/incentive_programs', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/incentive_programs",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
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

	url := "https://external-api.kalshi.com/trade-api/v2/incentive_programs"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/incentive_programs")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/incentive_programs")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

400

500

```
{
  "incentive_programs": [
    {
      "id": "<string>",
      "market_id": "<string>",
      "market_ticker": "<string>",
      "incentive_description": "<string>",
      "start_date": "2023-11-07T05:31:56Z",
      "end_date": "2023-11-07T05:31:56Z",
      "period_reward": 123,
      "paid_out": true,
      "discount_factor_bps": 123,
      "target_size_fp": "10.00"
    }
  ],
  "next_cursor": "<string>"
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

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#parameter-status)

status

enum<string>

Status filter. Can be "all", "active", "upcoming", "closed", or "paid\_out". Default is "all".

Available options:

`all`,

`active`,

`upcoming`,

`closed`,

`paid_out`

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#parameter-type)

type

enum<string>

Type filter. Can be "all", "liquidity", or "volume". Default is "all".

Available options:

`all`,

`liquidity`,

`volume`

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#parameter-incentive-description)

incentive\_description

string

Filter by exact incentive description.

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#parameter-limit)

limit

integer

Number of results per page. Defaults to 100. Maximum value is 10000.

Required range: `1 <= x <= 10000`

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#parameter-cursor)

cursor

string

Cursor for pagination

#### Response

200

application/json

Incentive programs retrieved successfully

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#response-incentive-programs)

incentive\_programs

object\[\]

required

Show child attributes

[​

](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives#response-next-cursor)

next\_cursor

string

Cursor for pagination to get the next page of results

[Lookup Tickers For Market In Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection)[Get FCM Orders](https://docs.kalshi.com/api-reference/fcm/get-fcm-orders)
