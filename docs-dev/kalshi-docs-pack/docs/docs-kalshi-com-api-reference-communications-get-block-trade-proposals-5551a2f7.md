---
title: "Get Block Trade Proposals - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:20.208Z"
---
Get Block Trade Proposals

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

400

401

500

```
{
  "block_trade_proposals": [
    {
      "id": "<string>",
      "proposer_user_id": "<string>",
      "buyer_user_id": "<string>",
      "seller_user_id": "<string>",
      "market_ticker": "<string>",
      "price_centi_cents": 123,
      "centicount": 123,
      "expiration_ts": "2023-11-07T05:31:56Z",
      "status": "<string>",
      "created_ts": "2023-11-07T05:31:56Z",
      "updated_ts": "2023-11-07T05:31:56Z",
      "buyer_accepted": true,
      "seller_accepted": true,
      "buyer_subtrader_id": "<string>",
      "seller_subtrader_id": "<string>",
      "buyer_accepted_ts": "2023-11-07T05:31:56Z",
      "seller_accepted_ts": "2023-11-07T05:31:56Z",
      "executed_ts": "2023-11-07T05:31:56Z",
      "buyer_order_id": "<string>",
      "seller_order_id": "<string>"
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

communications

/

block-trade-proposals

Try it

Get Block Trade Proposals

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

400

401

500

```
{
  "block_trade_proposals": [
    {
      "id": "<string>",
      "proposer_user_id": "<string>",
      "buyer_user_id": "<string>",
      "seller_user_id": "<string>",
      "market_ticker": "<string>",
      "price_centi_cents": 123,
      "centicount": 123,
      "expiration_ts": "2023-11-07T05:31:56Z",
      "status": "<string>",
      "created_ts": "2023-11-07T05:31:56Z",
      "updated_ts": "2023-11-07T05:31:56Z",
      "buyer_accepted": true,
      "seller_accepted": true,
      "buyer_subtrader_id": "<string>",
      "seller_subtrader_id": "<string>",
      "buyer_accepted_ts": "2023-11-07T05:31:56Z",
      "seller_accepted_ts": "2023-11-07T05:31:56Z",
      "executed_ts": "2023-11-07T05:31:56Z",
      "buyer_order_id": "<string>",
      "seller_order_id": "<string>"
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

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#parameter-market-ticker)

market\_ticker

string

Filter by market ticker

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#parameter-limit)

limit

integer<int32>

default:100

Parameter to specify the number of results per page. Defaults to 100.

Required range: `1 <= x <= 100`

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#parameter-status)

status

string

Filter block trade proposals by status

#### Response

200

application/json

Block trade proposals retrieved successfully

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#response-block-trade-proposals)

block\_trade\_proposals

object\[\]

required

List of block trade proposals

Show child attributes

[​

](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals#response-cursor)

cursor

string

Cursor for pagination to get the next page of results

[Get Communications ID](https://docs.kalshi.com/api-reference/communications/get-communications-id)[Propose Block Trade](https://docs.kalshi.com/api-reference/communications/propose-block-trade)
