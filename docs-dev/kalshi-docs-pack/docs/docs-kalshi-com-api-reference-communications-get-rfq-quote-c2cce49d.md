---
title: "Get RFQ Quote - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/get-rfq-quote"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:21.489Z"
---
Get RFQ Quote

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id} \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

401

404

500

```
{
  "quote": {
    "id": "<string>",
    "rfq_id": "<string>",
    "creator_id": "<string>",
    "rfq_creator_id": "<string>",
    "market_ticker": "<string>",
    "contracts_fp": "10.00",
    "yes_bid_dollars": "0.5600",
    "no_bid_dollars": "0.5600",
    "created_ts": "2023-11-07T05:31:56Z",
    "updated_ts": "2023-11-07T05:31:56Z",
    "accepted_ts": "2023-11-07T05:31:56Z",
    "confirmed_ts": "2023-11-07T05:31:56Z",
    "executed_ts": "2023-11-07T05:31:56Z",
    "cancelled_ts": "2023-11-07T05:31:56Z",
    "rest_remainder": true,
    "post_only": true,
    "cancellation_reason": "<string>",
    "creator_user_id": "<string>",
    "rfq_creator_user_id": "<string>",
    "rfq_target_cost_dollars": "0.5600",
    "rfq_creator_order_id": "<string>",
    "creator_order_id": "<string>",
    "creator_subaccount": 123,
    "rfq_creator_subaccount": 123,
    "yes_contracts_fp": "10.00",
    "no_contracts_fp": "10.00"
  }
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

rfqs

/

{rfq\_id}

/

quotes

/

{quote\_id}

Try it

Get RFQ Quote

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id} \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/rfqs/{rfq_id}/quotes/{quote_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

401

404

500

```
{
  "quote": {
    "id": "<string>",
    "rfq_id": "<string>",
    "creator_id": "<string>",
    "rfq_creator_id": "<string>",
    "market_ticker": "<string>",
    "contracts_fp": "10.00",
    "yes_bid_dollars": "0.5600",
    "no_bid_dollars": "0.5600",
    "created_ts": "2023-11-07T05:31:56Z",
    "updated_ts": "2023-11-07T05:31:56Z",
    "accepted_ts": "2023-11-07T05:31:56Z",
    "confirmed_ts": "2023-11-07T05:31:56Z",
    "executed_ts": "2023-11-07T05:31:56Z",
    "cancelled_ts": "2023-11-07T05:31:56Z",
    "rest_remainder": true,
    "post_only": true,
    "cancellation_reason": "<string>",
    "creator_user_id": "<string>",
    "rfq_creator_user_id": "<string>",
    "rfq_target_cost_dollars": "0.5600",
    "rfq_creator_order_id": "<string>",
    "creator_order_id": "<string>",
    "creator_subaccount": 123,
    "rfq_creator_subaccount": 123,
    "yes_contracts_fp": "10.00",
    "no_contracts_fp": "10.00"
  }
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

**Rate limit:** 2 tokens per request. See `GET /trade-api/v2/account/endpoint_costs` for current non-default endpoint costs.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/communications/get-rfq-quote#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/get-rfq-quote#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/get-rfq-quote#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/communications/get-rfq-quote#parameter-rfq-id)

rfq\_id

string

required

RFQ ID

[​

](https://docs.kalshi.com/api-reference/communications/get-rfq-quote#parameter-quote-id)

quote\_id

string

required

Quote ID

#### Response

200

application/json

Quote retrieved successfully

[​

](https://docs.kalshi.com/api-reference/communications/get-rfq-quote#response-quote)

quote

object

required

The details of the requested quote

Show child attributes

[Delete RFQ](https://docs.kalshi.com/api-reference/communications/delete-rfq)[Delete RFQ Quote](https://docs.kalshi.com/api-reference/communications/delete-rfq-quote)
