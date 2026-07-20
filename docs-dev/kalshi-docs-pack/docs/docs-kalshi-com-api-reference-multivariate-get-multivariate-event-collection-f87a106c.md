---
title: "Get Multivariate Event Collection - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:19.305Z"
---
Get Multivariate Event Collection

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

404

500

```
{
  "multivariate_contract": {
    "collection_ticker": "<string>",
    "series_ticker": "<string>",
    "title": "<string>",
    "description": "<string>",
    "open_date": "2023-11-07T05:31:56Z",
    "close_date": "2023-11-07T05:31:56Z",
    "associated_events": [
      {
        "ticker": "<string>",
        "is_yes_only": true,
        "active_quoters": [
          "<string>"
        ],
        "size_max": 123,
        "size_min": 123
      }
    ],
    "associated_event_tickers": [
      "<string>"
    ],
    "is_ordered": true,
    "is_single_market_per_event": true,
    "is_all_yes": true,
    "size_min": 123,
    "size_max": 123,
    "functional_description": "<string>"
  }
}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

multivariate\_event\_collections

/

{collection\_ticker}

Try it

Get Multivariate Event Collection

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

404

500

```
{
  "multivariate_contract": {
    "collection_ticker": "<string>",
    "series_ticker": "<string>",
    "title": "<string>",
    "description": "<string>",
    "open_date": "2023-11-07T05:31:56Z",
    "close_date": "2023-11-07T05:31:56Z",
    "associated_events": [
      {
        "ticker": "<string>",
        "is_yes_only": true,
        "active_quoters": [
          "<string>"
        ],
        "size_max": 123,
        "size_min": 123
      }
    ],
    "associated_event_tickers": [
      "<string>"
    ],
    "is_ordered": true,
    "is_single_market_per_event": true,
    "is_all_yes": true,
    "size_min": 123,
    "size_max": 123,
    "functional_description": "<string>"
  }
}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection#parameter-collection-ticker)

collection\_ticker

string

required

Collection ticker

#### Response

200

application/json

Collection retrieved successfully

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collection#response-multivariate-contract)

multivariate\_contract

object

required

The multivariate event collection.

Show child attributes

[Get Milestones](https://docs.kalshi.com/api-reference/milestone/get-milestones)[Create Market In Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection)
