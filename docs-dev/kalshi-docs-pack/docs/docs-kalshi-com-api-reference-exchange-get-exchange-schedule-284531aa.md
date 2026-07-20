---
title: "Get Exchange Schedule - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/exchange/get-exchange-schedule"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:57.403Z"
---
Get Exchange Schedule

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/exchange/schedule
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/exchange/schedule"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/exchange/schedule', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/exchange/schedule",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/exchange/schedule"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/exchange/schedule")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/exchange/schedule")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "schedule": {
    "standard_hours": [
      {
        "start_time": "2023-11-07T05:31:56Z",
        "end_time": "2023-11-07T05:31:56Z",
        "monday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "tuesday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "wednesday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "thursday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "friday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "saturday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "sunday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ]
      }
    ],
    "maintenance_windows": [
      {
        "start_datetime": "2023-11-07T05:31:56Z",
        "end_datetime": "2023-11-07T05:31:56Z"
      }
    ]
  }
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

exchange

/

schedule

Try it

Get Exchange Schedule

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/exchange/schedule
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/exchange/schedule"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/exchange/schedule', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/exchange/schedule",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/exchange/schedule"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/exchange/schedule")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/exchange/schedule")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "schedule": {
    "standard_hours": [
      {
        "start_time": "2023-11-07T05:31:56Z",
        "end_time": "2023-11-07T05:31:56Z",
        "monday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "tuesday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "wednesday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "thursday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "friday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "saturday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ],
        "sunday": [
          {
            "open_time": "<string>",
            "close_time": "<string>"
          }
        ]
      }
    ],
    "maintenance_windows": [
      {
        "start_datetime": "2023-11-07T05:31:56Z",
        "end_datetime": "2023-11-07T05:31:56Z"
      }
    ]
  }
}
```

#### Response

200

application/json

Exchange schedule retrieved successfully

[​

](https://docs.kalshi.com/api-reference/exchange/get-exchange-schedule#response-schedule)

schedule

object

required

Show child attributes

[Get Series Fee Changes](https://docs.kalshi.com/api-reference/exchange/get-series-fee-changes)[Get User Data Timestamp](https://docs.kalshi.com/api-reference/exchange/get-user-data-timestamp)
