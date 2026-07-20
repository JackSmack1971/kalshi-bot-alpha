---
title: "Get Historical Market Candlesticks - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:23.516Z"
---
Get Historical Market Candlesticks

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks",
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

	url := "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "ticker": "<string>",
  "candlesticks": [
    {
      "end_period_ts": 123,
      "yes_bid": {
        "open": "0.5600",
        "low": "0.5600",
        "high": "0.5600",
        "close": "0.5600"
      },
      "yes_ask": {
        "open": "0.5600",
        "low": "0.5600",
        "high": "0.5600",
        "close": "0.5600"
      },
      "price": {
        "open": "0.5600",
        "low": "0.5600",
        "high": "0.5600",
        "close": "0.5600",
        "mean": "0.5600",
        "previous": "0.5600"
      },
      "volume": "10.00",
      "open_interest": "10.00"
    }
  ]
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

historical

/

markets

/

{ticker}

/

candlesticks

Try it

Get Historical Market Candlesticks

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks",
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

	url := "https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/historical/markets/{ticker}/candlesticks")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "ticker": "<string>",
  "candlesticks": [
    {
      "end_period_ts": 123,
      "yes_bid": {
        "open": "0.5600",
        "low": "0.5600",
        "high": "0.5600",
        "close": "0.5600"
      },
      "yes_ask": {
        "open": "0.5600",
        "low": "0.5600",
        "high": "0.5600",
        "close": "0.5600"
      },
      "price": {
        "open": "0.5600",
        "low": "0.5600",
        "high": "0.5600",
        "close": "0.5600",
        "mean": "0.5600",
        "previous": "0.5600"
      },
      "volume": "10.00",
      "open_interest": "10.00"
    }
  ]
}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks#parameter-ticker)

ticker

string

required

Market ticker - unique identifier for the specific market

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks#parameter-start-ts)

start\_ts

integer<int64>

required

Start timestamp (Unix timestamp). Candlesticks will include those ending on or after this time.

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks#parameter-end-ts)

end\_ts

integer<int64>

required

End timestamp (Unix timestamp). Candlesticks will include those ending on or before this time.

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks#parameter-period-interval)

period\_interval

enum<integer>

required

Time period length of each candlestick in minutes. Valid values are 1 (1 minute), 60 (1 hour), or 1440 (1 day).

Available options:

`1`,

`60`,

`1440`

#### Response

200

application/json

Candlesticks retrieved successfully

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks#response-ticker)

ticker

string

required

Unique identifier for the market.

[​

](https://docs.kalshi.com/api-reference/historical/get-historical-market-candlesticks#response-candlesticks)

candlesticks

object\[\]

required

Array of candlestick data points for the specified time range.

Show child attributes

[Get Historical Cutoff Timestamps](https://docs.kalshi.com/api-reference/historical/get-historical-cutoff-timestamps)[Get Historical Fills](https://docs.kalshi.com/api-reference/historical/get-historical-fills)
