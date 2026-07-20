---
title: "Get Series - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/market/get-series"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:04.197Z"
---
Get Series

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "series": {
    "ticker": "<string>",
    "frequency": "<string>",
    "title": "<string>",
    "category": "<string>",
    "tags": [
      "<string>"
    ],
    "settlement_sources": [
      {
        "name": "<string>",
        "url": "<string>"
      }
    ],
    "contract_url": "<string>",
    "contract_terms_url": "<string>",
    "fee_multiplier": 123,
    "additional_prohibitions": [
      "<string>"
    ],
    "product_metadata": {},
    "volume_fp": "10.00",
    "last_updated_ts": "2023-11-07T05:31:56Z"
  }
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

series

/

{series\_ticker}

Try it

Get Series

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/series/{series_ticker}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "series": {
    "ticker": "<string>",
    "frequency": "<string>",
    "title": "<string>",
    "category": "<string>",
    "tags": [
      "<string>"
    ],
    "settlement_sources": [
      {
        "name": "<string>",
        "url": "<string>"
      }
    ],
    "contract_url": "<string>",
    "contract_terms_url": "<string>",
    "fee_multiplier": 123,
    "additional_prohibitions": [
      "<string>"
    ],
    "product_metadata": {},
    "volume_fp": "10.00",
    "last_updated_ts": "2023-11-07T05:31:56Z"
  }
}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/market/get-series#parameter-series-ticker)

series\_ticker

string

required

The ticker of the series to retrieve

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/market/get-series#parameter-include-volume)

include\_volume

boolean

default:false

If true, includes the total volume traded across all events in this series.

#### Response

200

application/json

Series retrieved successfully

[​

](https://docs.kalshi.com/api-reference/market/get-series#response-series)

series

object

required

Show child attributes

[Get Multiple Market Orderbooks](https://docs.kalshi.com/api-reference/market/get-multiple-market-orderbooks)[Get Series List](https://docs.kalshi.com/api-reference/market/get-series-list)
