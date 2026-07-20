---
title: "Get Series Fee Changes - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:57.212Z"
---
Get Series Fee Changes

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/series/fee_changes
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/series/fee_changes"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/series/fee_changes', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/series/fee_changes",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/series/fee_changes"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/series/fee_changes")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/series/fee_changes")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "series_fee_change_arr": [
    {
      "id": "<string>",
      "series_ticker": "<string>",
      "fee_multiplier": 123,
      "scheduled_ts": "2023-11-07T05:31:56Z"
    }
  ]
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

fee\_changes

Try it

Get Series Fee Changes

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/series/fee_changes
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/series/fee_changes"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/series/fee_changes', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/series/fee_changes",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/series/fee_changes"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/series/fee_changes")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/series/fee_changes")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "series_fee_change_arr": [
    {
      "id": "<string>",
      "series_ticker": "<string>",
      "fee_multiplier": 123,
      "scheduled_ts": "2023-11-07T05:31:56Z"
    }
  ]
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

](https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes#parameter-series-ticker)

series\_ticker

string

[​

](https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes#parameter-show-historical)

show\_historical

boolean

default:false

#### Response

200

application/json

Series fee changes retrieved successfully

[​

](https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes#response-series-fee-change-arr)

series\_fee\_change\_arr

object\[\]

required

Show child attributes

[Get Exchange Status](https://docs.kalshi.com/api-reference/exchange/get-exchange-status)[Get Exchange Schedule](https://docs.kalshi.com/api-reference/exchange/get-exchange-schedule)
