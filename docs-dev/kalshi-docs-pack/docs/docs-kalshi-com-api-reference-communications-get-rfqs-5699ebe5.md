---
title: "Get RFQs - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/get-rfqs"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:20.747Z"
---
Get RFQs

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/rfqs \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/communications/rfqs', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/rfqs",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

401

500

```
{
  "rfqs": [
    {
      "id": "<string>",
      "creator_id": "<string>",
      "market_ticker": "<string>",
      "contracts_fp": "10.00",
      "created_ts": "2023-11-07T05:31:56Z",
      "target_cost_dollars": "0.5600",
      "mve_collection_ticker": "<string>",
      "mve_selected_legs": [
        {
          "event_ticker": "<string>",
          "market_ticker": "<string>",
          "side": "<string>",
          "yes_settlement_value_dollars": "0.5600"
        }
      ],
      "rest_remainder": true,
      "cancellation_reason": "<string>",
      "creator_user_id": "<string>",
      "creator_subaccount": 123,
      "cancelled_ts": "2023-11-07T05:31:56Z",
      "updated_ts": "2023-11-07T05:31:56Z"
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

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

communications

/

rfqs

Try it

Get RFQs

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/rfqs \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.get(url, headers=headers)print(response.text)
```

```
const options = {  method: 'GET',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/communications/rfqs', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/rfqs",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"	req, _ := http.NewRequest("GET", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

401

500

```
{
  "rfqs": [
    {
      "id": "<string>",
      "creator_id": "<string>",
      "market_ticker": "<string>",
      "contracts_fp": "10.00",
      "created_ts": "2023-11-07T05:31:56Z",
      "target_cost_dollars": "0.5600",
      "mve_collection_ticker": "<string>",
      "mve_selected_legs": [
        {
          "event_ticker": "<string>",
          "market_ticker": "<string>",
          "side": "<string>",
          "yes_settlement_value_dollars": "0.5600"
        }
      ],
      "rest_remainder": true,
      "cancellation_reason": "<string>",
      "creator_user_id": "<string>",
      "creator_subaccount": 123,
      "cancelled_ts": "2023-11-07T05:31:56Z",
      "updated_ts": "2023-11-07T05:31:56Z"
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

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-event-ticker)

event\_ticker

string

Event ticker to filter by. Only a single event ticker is supported.

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-market-ticker)

market\_ticker

string

Filter by market ticker

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-subaccount)

subaccount

integer

Subaccount number (0 for primary, 1-63 for subaccounts). If omitted, defaults to all subaccounts.

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-limit)

limit

integer<int32>

default:100

Parameter to specify the number of results per page. Defaults to 100.

Required range: `1 <= x <= 100`

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-status)

status

string

Filter RFQs by status

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-creator-user-id)

creator\_user\_id

string

Filter RFQs by creator user ID

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#parameter-user-filter)

user\_filter

enum<string>

Omit or leave empty to return all results. Use `self` to filter by the authenticated user.

Available options:

`self`

#### Response

200

application/json

RFQs retrieved successfully

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#response-rfqs)

rfqs

object\[\]

required

List of RFQs matching the query criteria

Show child attributes

[​

](https://docs.kalshi.com/api-reference/communications/get-rfqs#response-cursor)

cursor

string

Cursor for pagination to get the next page of results

[Accept Block Trade Proposal](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal)[Create RFQ](https://docs.kalshi.com/api-reference/communications/create-rfq)
