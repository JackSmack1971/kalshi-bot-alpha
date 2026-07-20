---
title: "Get Exchange Status - API Documentation"
source_url: "https://docs.kalshi.com/margin-rest/exchange/get-exchange-status"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:15.817Z"
---
Get Exchange Status

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/exchange/status
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/exchange/status"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/margin/exchange/status', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/exchange/status",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/exchange/status"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/exchange/status")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/exchange/status")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

500

503

504

```
{
  "exchange_active": true,
  "trading_active": true
}
```

```
{  "exchange_active": true,  "trading_active": true}
```

```
{  "exchange_active": true,  "trading_active": true}
```

```
{  "exchange_active": true,  "trading_active": true}
```

GET

https://external-api.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2

/

margin

/

exchange

/

status

Try it

Get Exchange Status

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/exchange/status
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/exchange/status"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/margin/exchange/status', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/exchange/status",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/exchange/status"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/exchange/status")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/exchange/status")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

500

503

504

```
{
  "exchange_active": true,
  "trading_active": true
}
```

```
{  "exchange_active": true,  "trading_active": true}
```

```
{  "exchange_active": true,  "trading_active": true}
```

```
{  "exchange_active": true,  "trading_active": true}
```

#### Response

200

application/json

Margin exchange status retrieved successfully

[​

](https://docs.kalshi.com/margin-rest/exchange/get-exchange-status#response-exchange-active)

exchange\_active

boolean

required

False if the exchange is no longer taking any state changes at all. True unless under maintenance.

[​

](https://docs.kalshi.com/margin-rest/exchange/get-exchange-status#response-trading-active)

trading\_active

boolean

required

True if trading is currently permitted on the exchange. False outside exchange hours or during pauses.

[Get Perps Account API Limits](https://docs.kalshi.com/margin-rest/account/get-perps-account-api-limits)[Get Enabled Status](https://docs.kalshi.com/margin-rest/exchange/get-enabled-status)
