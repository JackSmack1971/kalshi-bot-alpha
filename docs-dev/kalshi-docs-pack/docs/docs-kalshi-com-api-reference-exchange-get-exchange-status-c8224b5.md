---
title: "Get Exchange Status - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/exchange/get-exchange-status"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:05.345Z"
---
Get Exchange Status

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/exchange/status
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/exchange/status"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/exchange/status', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/exchange/status",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/exchange/status"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/exchange/status")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/exchange/status")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

500

503

504

```
{
  "exchange_active": true,
  "trading_active": true,
  "intra_exchange_transfers_active": true,
  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",
  "exchange_index_statuses": [
    {
      "exchange_index": 0,
      "exchange_active": true,
      "trading_active": true,
      "intra_exchange_transfers_active": true
    }
  ]
}
```

```
{  "exchange_active": true,  "trading_active": true,  "intra_exchange_transfers_active": true,  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",  "exchange_index_statuses": [    {      "exchange_index": 0,      "exchange_active": true,      "trading_active": true,      "intra_exchange_transfers_active": true    }  ]}
```

```
{  "exchange_active": true,  "trading_active": true,  "intra_exchange_transfers_active": true,  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",  "exchange_index_statuses": [    {      "exchange_index": 0,      "exchange_active": true,      "trading_active": true,      "intra_exchange_transfers_active": true    }  ]}
```

```
{  "exchange_active": true,  "trading_active": true,  "intra_exchange_transfers_active": true,  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",  "exchange_index_statuses": [    {      "exchange_index": 0,      "exchange_active": true,      "trading_active": true,      "intra_exchange_transfers_active": true    }  ]}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

exchange

/

status

Try it

Get Exchange Status

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/exchange/status
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/exchange/status"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/exchange/status', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/exchange/status",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/exchange/status"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/exchange/status")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/exchange/status")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

500

503

504

```
{
  "exchange_active": true,
  "trading_active": true,
  "intra_exchange_transfers_active": true,
  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",
  "exchange_index_statuses": [
    {
      "exchange_index": 0,
      "exchange_active": true,
      "trading_active": true,
      "intra_exchange_transfers_active": true
    }
  ]
}
```

```
{  "exchange_active": true,  "trading_active": true,  "intra_exchange_transfers_active": true,  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",  "exchange_index_statuses": [    {      "exchange_index": 0,      "exchange_active": true,      "trading_active": true,      "intra_exchange_transfers_active": true    }  ]}
```

```
{  "exchange_active": true,  "trading_active": true,  "intra_exchange_transfers_active": true,  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",  "exchange_index_statuses": [    {      "exchange_index": 0,      "exchange_active": true,      "trading_active": true,      "intra_exchange_transfers_active": true    }  ]}
```

```
{  "exchange_active": true,  "trading_active": true,  "intra_exchange_transfers_active": true,  "exchange_estimated_resume_time": "2023-11-07T05:31:56Z",  "exchange_index_statuses": [    {      "exchange_index": 0,      "exchange_active": true,      "trading_active": true,      "intra_exchange_transfers_active": true    }  ]}
```

#### Response

200

application/json

Exchange status retrieved successfully

[​

](https://docs.kalshi.com/api-reference/exchange/get-exchange-status#response-exchange-active)

exchange\_active

boolean

required

False if the core Kalshi exchange is no longer taking any state changes at all. This includes but is not limited to trading, new users, and transfers. True unless we are under maintenance.

[​

](https://docs.kalshi.com/api-reference/exchange/get-exchange-status#response-trading-active)

trading\_active

boolean

required

True if we are currently permitting trading on the exchange. This is true during trading hours and false outside exchange hours. Kalshi reserves the right to pause at any time in case issues are detected.

[​

](https://docs.kalshi.com/api-reference/exchange/get-exchange-status#response-intra-exchange-transfers-active)

intra\_exchange\_transfers\_active

boolean

True if intra-exchange transfers are currently permitted. False when transfers are temporarily blocked.

[​

](https://docs.kalshi.com/api-reference/exchange/get-exchange-status#response-exchange-estimated-resume-time-one-of-0)

exchange\_estimated\_resume\_time

string<date-time> | null

Estimated downtime for the current exchange maintenance window. However, this is not guaranteed and can be extended.

[​

](https://docs.kalshi.com/api-reference/exchange/get-exchange-status#response-exchange-index-statuses)

exchange\_index\_statuses

object\[\]

Status of each exchange index. The top-level fields above reflect the default exchange index (0). Absent when the per-index breakdown is unavailable.

Show child attributes

[Get Series Fee Changes](https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes)
