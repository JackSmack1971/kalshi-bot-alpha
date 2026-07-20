---
title: "Get Structured Target - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/structured-targets/get-structured-target"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:12.258Z"
---
Get Structured Target

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "structured_target": {
    "id": "<string>",
    "name": "<string>",
    "type": "<string>",
    "details": {},
    "source_id": "<string>",
    "source_ids": {},
    "last_updated_ts": "2023-11-07T05:31:56Z"
  }
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

structured\_targets

/

{structured\_target\_id}

Try it

Get Structured Target

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/structured_targets/{structured_target_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "structured_target": {
    "id": "<string>",
    "name": "<string>",
    "type": "<string>",
    "details": {},
    "source_id": "<string>",
    "source_ids": {},
    "last_updated_ts": "2023-11-07T05:31:56Z"
  }
}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target#parameter-structured-target-id)

structured\_target\_id

string

required

Structured target ID

#### Response

200

application/json

Structured target retrieved successfully

[​

](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target#response-structured-target)

structured\_target

object

Show child attributes

[Get Structured Targets](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets)[Get Milestone](https://docs.kalshi.com/api-reference/milestone/get-milestone)
