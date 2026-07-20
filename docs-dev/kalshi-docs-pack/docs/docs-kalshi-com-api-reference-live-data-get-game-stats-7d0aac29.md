---
title: "Get Game Stats - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/live-data/get-game-stats"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:19.964Z"
---
Get Game Stats

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats",
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

	url := "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "pbp": {
    "periods": [
      {
        "events": [
          {}
        ]
      }
    ]
  }
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

live\_data

/

milestone

/

{milestone\_id}

/

game\_stats

Try it

Get Game Stats

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats",
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

	url := "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}/game_stats")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "pbp": {
    "periods": [
      {
        "events": [
          {}
        ]
      }
    ]
  }
}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/live-data/get-game-stats#parameter-milestone-id)

milestone\_id

string

required

Milestone ID

#### Response

200

application/json

Game stats retrieved successfully

[​

](https://docs.kalshi.com/api-reference/live-data/get-game-stats#response-pbp)

pbp

object

Play-by-play data organized by period.

Show child attributes

[Get Multiple Live Data](https://docs.kalshi.com/api-reference/live-data/get-multiple-live-data)[Get Structured Targets](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets)
