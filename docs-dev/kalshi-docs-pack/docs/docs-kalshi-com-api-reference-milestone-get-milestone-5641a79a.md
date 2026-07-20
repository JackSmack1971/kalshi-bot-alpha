---
title: "Get Milestone - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/milestone/get-milestone"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:11.850Z"
---
Get Milestone

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}",
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

	url := "https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "milestone": {
    "id": "<string>",
    "category": "Sports",
    "type": "football_game",
    "start_date": "2023-11-07T05:31:56Z",
    "related_event_tickers": [
      "<string>"
    ],
    "title": "<string>",
    "notification_message": "<string>",
    "details": {},
    "primary_event_tickers": [
      "<string>"
    ],
    "last_updated_ts": "2023-11-07T05:31:56Z",
    "end_date": "2023-11-07T05:31:56Z",
    "source_id": "<string>",
    "source_ids": {}
  }
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

milestones

/

{milestone\_id}

Try it

Get Milestone

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}",
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

	url := "https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/milestones/{milestone_id}")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "milestone": {
    "id": "<string>",
    "category": "Sports",
    "type": "football_game",
    "start_date": "2023-11-07T05:31:56Z",
    "related_event_tickers": [
      "<string>"
    ],
    "title": "<string>",
    "notification_message": "<string>",
    "details": {},
    "primary_event_tickers": [
      "<string>"
    ],
    "last_updated_ts": "2023-11-07T05:31:56Z",
    "end_date": "2023-11-07T05:31:56Z",
    "source_id": "<string>",
    "source_ids": {}
  }
}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestone#parameter-milestone-id)

milestone\_id

string

required

Milestone ID

#### Response

200

application/json

Milestone retrieved successfully

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestone#response-milestone)

milestone

object

required

The milestone data.

Show child attributes

[Get Structured Target](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target)[Get Milestones](https://docs.kalshi.com/api-reference/milestone/get-milestones)
