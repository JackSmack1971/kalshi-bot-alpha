---
title: "Get Historical Funding Rates - API Documentation"
source_url: "https://docs.kalshi.com/margin-rest/funding/get-historical-funding-rates"
host: "docs.kalshi.com"
depth: 6
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:26.721Z"
---
Get Historical Funding Rates

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "funding_rates": [
    {
      "market_ticker": "<string>",
      "funding_time": "2023-11-07T05:31:56Z",
      "funding_rate": 123,
      "mark_price": "0.5600"
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

https://external-api.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2

/

margin

/

funding\_rates

/

historical

Try it

Get Historical Funding Rates

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/funding_rates/historical")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

400

500

```
{
  "funding_rates": [
    {
      "market_ticker": "<string>",
      "funding_time": "2023-11-07T05:31:56Z",
      "funding_rate": 123,
      "mark_price": "0.5600"
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

](https://docs.kalshi.com/margin-rest/funding/get-historical-funding-rates#parameter-ticker)

ticker

string

Market ticker. Leave empty to query across all markets.

[​

](https://docs.kalshi.com/margin-rest/funding/get-historical-funding-rates#parameter-start-ts)

start\_ts

integer<int64>

Start timestamp (Unix timestamp in seconds). If omitted, defaults to the earliest available data.

[​

](https://docs.kalshi.com/margin-rest/funding/get-historical-funding-rates#parameter-end-ts)

end\_ts

integer<int64>

End timestamp (Unix timestamp in seconds). If omitted, defaults to the current time.

#### Response

200

application/json

Historical funding rates retrieved successfully

[​

](https://docs.kalshi.com/margin-rest/funding/get-historical-funding-rates#response-funding-rates)

funding\_rates

object\[\]

required

Array of historical funding rate entries

Show child attributes

[Get Funding History](https://docs.kalshi.com/margin-rest/funding/get-funding-history)[Get Funding Rate Estimate](https://docs.kalshi.com/margin-rest/funding/get-funding-rate-estimate)
