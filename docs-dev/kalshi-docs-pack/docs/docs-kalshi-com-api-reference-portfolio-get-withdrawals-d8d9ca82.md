---
title: "Get Withdrawals - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/get-withdrawals"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:17.972Z"
---
Get Withdrawals

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

400

401

500

```
{
  "withdrawals": [
    {
      "id": "<string>",
      "amount_cents": 123,
      "fee_cents": 123,
      "created_ts": 123,
      "finalized_ts": 123
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

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

withdrawals

Try it

Get Withdrawals

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/withdrawals")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

400

401

500

```
{
  "withdrawals": [
    {
      "id": "<string>",
      "amount_cents": 123,
      "fee_cents": 123,
      "created_ts": 123,
      "finalized_ts": 123
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

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#parameter-limit)

limit

integer<int64>

default:100

Number of results per page. Defaults to 100. Maximum value is 500.

Required range: `1 <= x <= 500`

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

#### Response

200

application/json

Withdrawals retrieved successfully

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#response-withdrawals)

withdrawals

object\[\]

required

Show child attributes

[​

](https://docs.kalshi.com/api-reference/portfolio/get-withdrawals#response-cursor)

cursor

string

[Get Deposits](https://docs.kalshi.com/api-reference/portfolio/get-deposits)[Get Total Resting Order Value](https://docs.kalshi.com/api-reference/portfolio/get-total-resting-order-value)
