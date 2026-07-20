---
title: "Get Live Data - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/live-data/get-live-data"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:12.115Z"
---
Get Live Data

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "live_data": {
    "type": "<string>",
    "details": {},
    "milestone_id": "<string>"
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

Try it

Get Live Data

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/live_data/milestone/{milestone_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "live_data": {
    "type": "<string>",
    "details": {},
    "milestone_id": "<string>"
  }
}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/live-data/get-live-data#parameter-milestone-id)

milestone\_id

string

required

Milestone ID

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/live-data/get-live-data#parameter-include-player-stats)

include\_player\_stats

boolean

default:false

When true, includes player-level statistics in the live data response. Supported for Pro Football, Pro Basketball, and College Men's Basketball milestones that have player ID mappings configured. Has no effect for other sports or milestones without player mappings.

#### Response

200

application/json

Live data retrieved successfully

[​

](https://docs.kalshi.com/api-reference/live-data/get-live-data#response-live-data)

live\_data

object

required

Show child attributes

[Get Filters for Sports](https://docs.kalshi.com/api-reference/search/get-filters-for-sports)[Get Live Data (with type)](https://docs.kalshi.com/api-reference/live-data/get-live-data-with-type)
