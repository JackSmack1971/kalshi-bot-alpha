---
title: "Get Series List - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/market/get-series-list"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:12.970Z"
---
Get Series List

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/series
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/series"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/series', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/series",
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

	url := "https://external-api.kalshi.com/trade-api/v2/series"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/series")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/series")

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
  "series": [
    {
      "ticker": "<string>",
      "frequency": "<string>",
      "title": "<string>",
      "category": "<string>",
      "tags": [
        "<string>"
      ],
      "settlement_sources": [
        {
          "name": "<string>",
          "url": "<string>"
        }
      ],
      "contract_url": "<string>",
      "contract_terms_url": "<string>",
      "fee_multiplier": 123,
      "additional_prohibitions": [
        "<string>"
      ],
      "product_metadata": {},
      "volume_fp": "10.00",
      "last_updated_ts": "2023-11-07T05:31:56Z"
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

series

Try it

Get Series List

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/series
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/series"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/series', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/series",
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

	url := "https://external-api.kalshi.com/trade-api/v2/series"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/series")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/series")

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
  "series": [
    {
      "ticker": "<string>",
      "frequency": "<string>",
      "title": "<string>",
      "category": "<string>",
      "tags": [
        "<string>"
      ],
      "settlement_sources": [
        {
          "name": "<string>",
          "url": "<string>"
        }
      ],
      "contract_url": "<string>",
      "contract_terms_url": "<string>",
      "fee_multiplier": 123,
      "additional_prohibitions": [
        "<string>"
      ],
      "product_metadata": {},
      "volume_fp": "10.00",
      "last_updated_ts": "2023-11-07T05:31:56Z"
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

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/market/get-series-list#parameter-category)

category

string

[​

](https://docs.kalshi.com/api-reference/market/get-series-list#parameter-tags)

tags

string

[​

](https://docs.kalshi.com/api-reference/market/get-series-list#parameter-include-product-metadata)

include\_product\_metadata

boolean

default:false

[​

](https://docs.kalshi.com/api-reference/market/get-series-list#parameter-include-volume)

include\_volume

boolean

default:false

If true, includes the total volume traded across all events in each series.

[​

](https://docs.kalshi.com/api-reference/market/get-series-list#parameter-min-updated-ts)

min\_updated\_ts

integer<int64>

Filter series with metadata updated after this Unix timestamp (in seconds). Use this to efficiently poll for changes.

#### Response

200

application/json

Series list retrieved successfully

[​

](https://docs.kalshi.com/api-reference/market/get-series-list#response-series)

series

object\[\]

required

Show child attributes

[Get Series](https://docs.kalshi.com/api-reference/market/get-series)[Get Markets](https://docs.kalshi.com/api-reference/market/get-markets)
