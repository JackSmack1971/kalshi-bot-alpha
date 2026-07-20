---
title: "Get Funding Rate Estimate - API Documentation"
source_url: "https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate"
host: "docs.kalshi.com"
depth: 5
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:26.001Z"
---
Get Funding Rate Estimate

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate",
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

	url := "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate")

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
  "next_funding_time": "2023-11-07T05:31:56Z",
  "market_ticker": "<string>",
  "computed_time": "2023-11-07T05:31:56Z",
  "funding_rate": 123,
  "mark_price": "0.5600"
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

https://external-api.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2

/

margin

/

funding\_rates

/

estimate

Try it

Get Funding Rate Estimate

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate",
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

	url := "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/estimate")

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
  "next_funding_time": "2023-11-07T05:31:56Z",
  "market_ticker": "<string>",
  "computed_time": "2023-11-07T05:31:56Z",
  "funding_rate": 123,
  "mark_price": "0.5600"
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

](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate#parameter-ticker)

ticker

string

required

Market ticker

#### Response

200

application/json

Funding rate estimate retrieved successfully

[​

](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate#response-next-funding-time)

next\_funding\_time

string<date-time>

required

Timestamp of the next scheduled funding event

[​

](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate#response-market-ticker)

market\_ticker

string

Ticker of the margin market

[​

](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate#response-computed-time)

computed\_time

string<date-time>

Timestamp when this estimate was computed

[​

](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate#response-funding-rate)

funding\_rate

number<double>

Estimated funding rate for the in-progress period

[​

](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate#response-mark-price)

mark\_price

string

Mark price at the time the estimate was computed

Example:

`"0.5600"`

[Get Historical Funding Rates](https://docs.kalshi.com/margin-rest/funding/get-historical-funding-rates)[Get Order Groups](https://docs.kalshi.com/margin-rest/order-groups/get-order-groups)
