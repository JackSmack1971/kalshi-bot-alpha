---
title: "Get Milestones - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/milestone/get-milestones"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:11.992Z"
---
Get Milestones

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/milestones
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/milestones"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/milestones', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/milestones",
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

	url := "https://external-api.kalshi.com/trade-api/v2/milestones"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/milestones")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/milestones")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "milestones": [
    {
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
  ],
  "cursor": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

milestones

Try it

Get Milestones

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/milestones
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/milestones"

response = requests.get(url)

print(response.text)
```

```
const options = {method: 'GET'};

fetch('https://external-api.kalshi.com/trade-api/v2/milestones', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/milestones",
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

	url := "https://external-api.kalshi.com/trade-api/v2/milestones"

	req, _ := http.NewRequest("GET", url, nil)

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/milestones")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/milestones")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)

response = http.request(request)
puts response.read_body
```

200

```
{
  "milestones": [
    {
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
  ],
  "cursor": "<string>"
}
```

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-limit)

limit

integer

required

Number of milestones to return per page

Required range: `1 <= x <= 500`

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-minimum-start-date)

minimum\_start\_date

string<date-time>

Minimum start date to filter milestones. Format RFC3339 timestamp

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-category)

category

string

Filter by milestone category. E.g. Sports, Elections, Esports, Crypto.

Example:

`"Sports"`

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-competition)

competition

string

Filter by competition. E.g. Pro Football, Pro Basketball (M), Pro Baseball, Pro Hockey, College Football.

Example:

`"Pro Football"`

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-source-id)

source\_id

string

Filter by source id

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-type)

type

string

Filter by milestone type. E.g. football\_game, basketball\_game, soccer\_tournament\_multi\_leg, baseball\_game, hockey\_match, political\_race.

Example:

`"football_game"`

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-related-event-ticker)

related\_event\_ticker

string

Filter by related event ticker

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#parameter-min-updated-ts)

min\_updated\_ts

integer<int64>

Filter milestones with metadata updated after this Unix timestamp (in seconds). Use this to efficiently poll for changes.

#### Response

200

application/json

Milestones retrieved successfully

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#response-milestones)

milestones

object\[\]

required

List of milestones.

Show child attributes

[​

](https://docs.kalshi.com/api-reference/milestone/get-milestones#response-cursor)

cursor

string

Cursor for pagination.

[Get Milestone](https://docs.kalshi.com/api-reference/milestone/get-milestone)[Get Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection)
