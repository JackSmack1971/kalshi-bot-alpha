---
title: "Get Structured Targets - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:12.397Z"
---
Get Structured Targets

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/structured_targets
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/structured_targets"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/structured_targets', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/structured_targets",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/structured_targets"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/structured_targets")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/structured_targets")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "structured_targets": [
    {
      "id": "<string>",
      "name": "<string>",
      "type": "<string>",
      "details": {},
      "source_id": "<string>",
      "source_ids": {},
      "last_updated_ts": "2023-11-07T05:31:56Z"
    }
  ],
  "cursor": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

structured\_targets

Try it

Get Structured Targets

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/structured_targets
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/structured_targets"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/structured_targets', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/structured_targets",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/structured_targets"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/structured_targets")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/structured_targets")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "structured_targets": [
    {
      "id": "<string>",
      "name": "<string>",
      "type": "<string>",
      "details": {},
      "source_id": "<string>",
      "source_ids": {},
      "last_updated_ts": "2023-11-07T05:31:56Z"
    }
  ],
  "cursor": "<string>"
}
```

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#parameter-ids)

ids

string\[\]

Filter by specific structured target IDs. Pass multiple IDs by repeating the parameter (e.g. `?ids=uuid1&ids=uuid2`).

Maximum array length: `2000`

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#parameter-type)

type

string

Filter by structured target type

Example:

`"basketball_player"`

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#parameter-competition)

competition

string

Filter by competition. Matches against the league, conference, division, or tour in the structured target details.

Example:

`"NBA"`

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#parameter-page-size)

page\_size

integer<int32>

default:100

Number of items per page (min 1, max 2000, default 100)

Required range: `1 <= x <= 2000`

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#parameter-cursor)

cursor

string

Pagination cursor

#### Response

200

application/json

Structured targets retrieved successfully

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#response-structured-targets)

structured\_targets

object\[\]

Show child attributes

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets#response-cursor)

cursor

string

Pagination cursor for the next page. Empty if there are no more results.

[Get Game Stats](https://docs.kalshi.com/api-reference/live-data/get-game-stats)[Get Structured Target](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target)
