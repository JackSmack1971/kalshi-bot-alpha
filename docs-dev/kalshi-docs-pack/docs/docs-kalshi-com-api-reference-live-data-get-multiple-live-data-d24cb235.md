---
title: "Get Multiple Live Data - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/live-data/get-multiple-live-data"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:19.800Z"
---
Get Multiple Live Data

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/live_data/batch
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/live_data/batch"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/live_data/batch', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/live_data/batch",
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

	url := "https://external-api.kalshi.com/trade-api/v2/live_data/batch"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/live_data/batch")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/live_data/batch")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "live_datas": [
    {
      "type": "<string>",
      "details": {},
      "milestone_id": "<string>"
    }
  ]
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

live\_data

/

batch

Try it

Get Multiple Live Data

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/live_data/batch
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/live_data/batch"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/live_data/batch', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/live_data/batch",
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

	url := "https://external-api.kalshi.com/trade-api/v2/live_data/batch"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/live_data/batch")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/live_data/batch")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "live_datas": [
    {
      "type": "<string>",
      "details": {},
      "milestone_id": "<string>"
    }
  ]
}
```

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/live-data/get-multiple-live-data#parameter-milestone-ids)

milestone\_ids

string\[\]

required

Array of milestone IDs

Maximum array length: `100`

[​

](https://docs.kalshi.com/api-reference/live-data/get-multiple-live-data#parameter-include-player-stats)

include\_player\_stats

boolean

default:false

When true, includes player-level statistics in the live data response. Supported for Pro Football, Pro Basketball, and College Men's Basketball milestones that have player ID mappings configured. Has no effect for other sports or milestones without player mappings.

#### Response

200

application/json

Live data retrieved successfully

[​

](https://docs.kalshi.com/api-reference/live-data/get-multiple-live-data#response-live-datas)

live\_datas

object\[\]

required

Show child attributes

[Get Live Data (with type)](https://docs.kalshi.com/api-reference/live-data/get-live-data-with-type)[Get Game Stats](https://docs.kalshi.com/api-reference/live-data/get-game-stats)
