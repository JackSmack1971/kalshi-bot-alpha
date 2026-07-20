---
title: "Get Filters for Sports - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/search/get-filters-for-sports"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:20.080Z"
---
Get Filters for Sports

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "filters_by_sports": {},
  "sport_ordering": [
    "<string>"
  ]
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

search

/

filters\_by\_sport

Try it

Get Filters for Sports

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/search/filters_by_sport")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "filters_by_sports": {},
  "sport_ordering": [
    "<string>"
  ]
}
```

#### Response

200

application/json

Filters retrieved successfully

[​

](https://docs.kalshi.com/api-reference/search/get-filters-for-sports#response-filters-by-sports)

filters\_by\_sports

object

required

Mapping of sports to their filter details

Show child attributes

[​

](https://docs.kalshi.com/api-reference/search/get-filters-for-sports#response-sport-ordering)

sport\_ordering

string\[\]

required

Ordered list of sports for display

[Get Tags for Series Categories](https://docs.kalshi.com/api-reference/search/get-tags-for-series-categories)[Get Live Data](https://docs.kalshi.com/api-reference/live-data/get-live-data)
