---
title: "Get Multivariate Event Collections - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:12.834Z"
---
Get Multivariate Event Collections

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "multivariate_contracts": [
    {
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
  ],
  "cursor": "<string>"
}
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

Try it

Get Multivariate Event Collections

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "multivariate_contracts": [
    {
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
  ],
  "cursor": "<string>"
}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#parameter-status)

status

enum<string>

Only return collections of a certain status. Can be unopened, open, or closed.

Available options:

`unopened`,

`open`,

`closed`

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#parameter-associated-event-ticker)

associated\_event\_ticker

string

Only return collections associated with a particular event ticker.

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#parameter-series-ticker)

series\_ticker

string

Only return collections with a particular series ticker.

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#parameter-limit)

limit

integer<int32>

Specify the maximum number of results.

Required range: `1 <= x <= 200`

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#parameter-cursor)

cursor

string

The Cursor represents a pointer to the next page of records in the pagination. This optional parameter, when filled, should be filled with the cursor string returned in a previous request to this end-point.

#### Response

200

application/json

Collections retrieved successfully

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#response-multivariate-contracts)

multivariate\_contracts

object\[\]

required

List of multivariate event collections.

Show child attributes

[​

](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections#response-cursor)

cursor

string

The Cursor represents a pointer to the next page of records in the pagination. Use the value returned here in the cursor query parameter for this end-point to get the next page containing limit records. An empty value of this field indicates there is no next page.

[Create Market In Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/create-market-in-multivariate-event-collection)[Lookup Tickers For Market In Multivariate Event Collection](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection)
