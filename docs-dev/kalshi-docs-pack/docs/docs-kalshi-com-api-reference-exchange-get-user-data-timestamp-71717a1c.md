---
title: "Get User Data Timestamp - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/exchange/get-user-data-timestamp"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:57.568Z"
---
Get User Data Timestamp

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "as_of_time": "2023-11-07T05:31:56Z"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

exchange

/

user\_data\_timestamp

Try it

Get User Data Timestamp

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/exchange/user_data_timestamp")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "as_of_time": "2023-11-07T05:31:56Z"
}
```

#### Response

200

application/json

User data timestamp retrieved successfully

[​

](https://docs.kalshi.com/api-reference/exchange/get-user-data-timestamp#response-as-of-time)

as\_of\_time

string<date-time>

required

Timestamp when user data was last updated.

[Get Exchange Schedule](https://docs.kalshi.com/api-reference/exchange/get-exchange-schedule)[Get Market Candlesticks](https://docs.kalshi.com/api-reference/market/get-market-candlesticks)
