---
title: "Get Historical Cutoff Timestamps - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:23.388Z"
---
Get Historical Cutoff Timestamps

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/cutoff
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/historical/cutoff"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/historical/cutoff', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/cutoff",
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

	url := "https://external-api.kalshi.com/trade-api/v2/historical/cutoff"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/cutoff")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/historical/cutoff")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "market_settled_ts": "2023-11-07T05:31:56Z",
  "trades_created_ts": "2023-11-07T05:31:56Z",
  "orders_updated_ts": "2023-11-07T05:31:56Z"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

historical

/

cutoff

Try it

Get Historical Cutoff Timestamps

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/cutoff
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/historical/cutoff"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/historical/cutoff', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/cutoff",
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

	url := "https://external-api.kalshi.com/trade-api/v2/historical/cutoff"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/cutoff")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/historical/cutoff")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "market_settled_ts": "2023-11-07T05:31:56Z",
  "trades_created_ts": "2023-11-07T05:31:56Z",
  "orders_updated_ts": "2023-11-07T05:31:56Z"
}
```

#### Response

200

application/json

Historical cutoff timestamps retrieved successfully

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps#response-market-settled-ts)

market\_settled\_ts

string<date-time>

required

Cutoff based on market settlement time. Markets and their candlesticks that settled before this timestamp must be accessed via `GET /historical/markets` and `GET /historical/markets/{ticker}/candlesticks`.

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps#response-trades-created-ts)

trades\_created\_ts

string<date-time>

required

Cutoff based on trade fill time. Fills that occurred before this timestamp must be accessed via `GET /historical/fills`.

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps#response-orders-updated-ts)

orders\_updated\_ts

string<date-time>

required

Cutoff based on order cancellation or execution time. Orders canceled or fully executed before this timestamp must be accessed via `GET /historical/orders`. Resting (active) orders are always available in `GET /portfolio/orders`.

[Get FCM Positions](https://docs.kalshi.com/api-reference/fcm/get-fcm-positions)[Get Historical Market Candlesticks](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks)
