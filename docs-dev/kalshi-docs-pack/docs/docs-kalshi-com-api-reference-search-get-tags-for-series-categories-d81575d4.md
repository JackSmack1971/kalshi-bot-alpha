---
title: "Get Tags for Series Categories - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/search/get-tags-for-series-categories"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:13.094Z"
---
Get Tags for Series Categories

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories",
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

	url := "https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "tags_by_categories": {}
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

search

/

tags\_by\_categories

Try it

Get Tags for Series Categories

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories",
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

	url := "https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/search/tags_by_categories")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "tags_by_categories": {}
}
```

#### Response

200

application/json

Tags retrieved successfully

[​

](https://docs.kalshi.com/api-reference/search/get-tags-for-series-categories#response-tags-by-categories)

tags\_by\_categories

object

required

Mapping of series categories to their associated tags

Show child attributes

[List Non-Default Endpoint Costs](https://docs.kalshi.com/api-reference/account/list-non-default-endpoint-costs)[Get Filters for Sports](https://docs.kalshi.com/api-reference/search/get-filters-for-sports)
