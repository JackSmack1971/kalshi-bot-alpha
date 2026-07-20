---
title: "Get Historical Trades - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/historical/get-historical-trades"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:23.984Z"
---
Get Historical Trades

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/trades
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/historical/trades"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/historical/trades', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/trades",
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

	url := "https://external-api.kalshi.com/trade-api/v2/historical/trades"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/trades")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/historical/trades")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

400

404

500

```
{
  "trades": [
    {
      "trade_id": "<string>",
      "ticker": "<string>",
      "count_fp": "10.00",
      "yes_price_dollars": "0.5600",
      "no_price_dollars": "0.5600",
      "created_time": "2023-11-07T05:31:56Z",
      "is_block_trade": true
    }
  ],
  "cursor": "<string>"
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

historical

/

trades

Try it

Get Historical Trades

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/trades
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/historical/trades"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/historical/trades', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/trades",
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

	url := "https://external-api.kalshi.com/trade-api/v2/historical/trades"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/trades")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/historical/trades")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

400

404

500

```
{
  "trades": [
    {
      "trade_id": "<string>",
      "ticker": "<string>",
      "count_fp": "10.00",
      "yes_price_dollars": "0.5600",
      "no_price_dollars": "0.5600",
      "created_time": "2023-11-07T05:31:56Z",
      "is_block_trade": true
    }
  ],
  "cursor": "<string>"
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

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#parameter-ticker)

ticker

string

Filter by market ticker

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#parameter-min-ts)

min\_ts

integer<int64>

Filter items after this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#parameter-max-ts)

max\_ts

integer<int64>

Filter items before this Unix timestamp

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#parameter-limit)

limit

integer<int64>

default:100

Number of results per page. Defaults to 100. Maximum value is 1000.

Required range: `0 <= x <= 1000`

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#parameter-is-block-trade)

is\_block\_trade

boolean

Filter trades by whether they are block trades. Omit to return all trades. Set to `true` to return only block trades. Set to `false` to return only non-block trades.

#### Response

200

application/json

Historical trades retrieved successfully

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#response-trades)

trades

object\[\]

required

Show child attributes

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-trades#response-cursor)

cursor

string

required

[Get Historical Orders](https://docs.kalshi.com/api-reference/historical/get-historical-orders)[Get Historical Markets](https://docs.kalshi.com/api-reference/historical/get-historical-markets)
