---
title: "List Non-Default Endpoint Costs - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/account/list-non-default-endpoint-costs"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:05.531Z"
---
List Non-Default Endpoint Costs

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "default_cost": 123,
  "endpoint_costs": [
    {
      "method": "<string>",
      "path": "<string>",
      "cost": 123
    }
  ]
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

account

/

endpoint\_costs

Try it

List Non-Default Endpoint Costs

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/account/endpoint_costs")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "default_cost": 123,
  "endpoint_costs": [
    {
      "method": "<string>",
      "path": "<string>",
      "cost": 123
    }
  ]
}
```

#### Response

200

application/json

Non-default endpoint costs retrieved successfully

[​

](https://docs.kalshi.com/api-reference/account/list-non-default-endpoint-costs#response-default-cost)

default\_cost

integer

required

Default token cost applied to endpoints that are not listed in `endpoint_costs`. This is currently 10.

[​

](https://docs.kalshi.com/api-reference/account/list-non-default-endpoint-costs#response-endpoint-costs)

endpoint\_costs

object\[\]

required

API v2 endpoints whose configured token cost differs from `default_cost`. Endpoints that use the default cost are omitted.

Show child attributes

[Get Account API Usage Level Volume Progress](https://docs.kalshi.com/api-reference/account/get-account-api-usage-level-volume-progress)[Get Tags for Series Categories](https://docs.kalshi.com/api-reference/search/get-tags-for-series-categories)
