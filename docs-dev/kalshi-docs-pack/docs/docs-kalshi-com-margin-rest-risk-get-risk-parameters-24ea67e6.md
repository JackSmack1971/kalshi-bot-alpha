---
title: "Get Risk Parameters - API Documentation"
source_url: "https://docs.kalshi.com/margin-rest/risk/get-risk-parameters"
host: "docs.kalshi.com"
depth: 6
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:26.270Z"
---
Get Risk Parameters

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "liquidation_margin_ratio_threshold": 123,
  "queue_entry_margin_ratio_threshold": 123,
  "initial_margin_multiplier": {}
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2

/

margin

/

risk\_parameters

Try it

Get Risk Parameters

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/risk_parameters")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "liquidation_margin_ratio_threshold": 123,
  "queue_entry_margin_ratio_threshold": 123,
  "initial_margin_multiplier": {}
}
```

#### Response

200 - application/json

Margin risk parameters retrieved successfully

[​

](https://docs.kalshi.com/margin-rest/risk/get-risk-parameters#response-liquidation-margin-ratio-threshold)

liquidation\_margin\_ratio\_threshold

number<double>

required

Margin ratio at which a position is liquidated.

[​

](https://docs.kalshi.com/margin-rest/risk/get-risk-parameters#response-queue-entry-margin-ratio-threshold)

queue\_entry\_margin\_ratio\_threshold

number<double>

required

Margin ratio at which a position enters the liquidation queue.

[​

](https://docs.kalshi.com/margin-rest/risk/get-risk-parameters#response-initial-margin-multiplier)

initial\_margin\_multiplier

object

required

Map of market ticker to initial margin multiplier. The initial margin requirement is the maintenance margin multiplied by this value.

Show child attributes

[Get Enabled Status](https://docs.kalshi.com/margin-rest/exchange/get-enabled-status)[Get Notional Risk Limit](https://docs.kalshi.com/margin-rest/risk/get-notional-risk-limit)
