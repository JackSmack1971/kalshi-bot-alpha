---
title: "Get Quotes - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/get-quotes"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:22.125Z"
---
Get Quotes

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/quotes \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/communications/quotes"

headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
const options = {
  method: 'GET',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'
  }
};

fetch('https://external-api.kalshi.com/trade-api/v2/communications/quotes', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/quotes",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "KALSHI-ACCESS-KEY: <api-key>",
    "KALSHI-ACCESS-SIGNATURE: <api-key>",
    "KALSHI-ACCESS-TIMESTAMP: <api-key>"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```
package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "https://external-api.kalshi.com/trade-api/v2/communications/quotes"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/quotes")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/communications/quotes")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'

response = http.request(request)
puts response.read_body
```

200

401

500

```
{
  "quotes": [
    {
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
  ],
  "cursor": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

communications

/

quotes

Try it

Get Quotes

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/communications/quotes \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/communications/quotes"

headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"
}

response = requests.get(url, headers=headers)

print(response.text)
```

```
const options = {
  method: 'GET',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'
  }
};

fetch('https://external-api.kalshi.com/trade-api/v2/communications/quotes', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/quotes",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_HTTPHEADER => [
    "KALSHI-ACCESS-KEY: <api-key>",
    "KALSHI-ACCESS-SIGNATURE: <api-key>",
    "KALSHI-ACCESS-TIMESTAMP: <api-key>"
  ],
]);

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}
```

```
package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "https://external-api.kalshi.com/trade-api/v2/communications/quotes"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/communications/quotes")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/communications/quotes")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'

response = http.request(request)
puts response.read_body
```

200

401

500

```
{
  "quotes": [
    {
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
  ],
  "cursor": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-cursor)

cursor

string

Pagination cursor. Use the cursor value returned from the previous response to get the next page of results. Leave empty for the first page.

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-min-ts)

min\_ts

integer<int64>

Restricts the response to quotes last updated after a timestamp, formatted as a Unix Timestamp

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-max-ts)

max\_ts

integer<int64>

Restricts the response to quotes last updated before a timestamp, formatted as a Unix Timestamp

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-limit)

limit

integer<int32>

default:500

Parameter to specify the number of results per page. Defaults to 500.

Required range: `1 <= x <= 500`

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-status)

status

string

Filter quotes by status

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-quote-creator-user-id)

quote\_creator\_user\_id

string

Filter quotes by quote creator user ID

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-user-filter)

user\_filter

enum<string>

Filter for quotes created by the authenticated user. Omit or leave empty to return all results. Use `self` to filter by the authenticated user.

Available options:

`self`

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-rfq-user-filter)

rfq\_user\_filter

enum<string>

Filter for quotes responding to RFQs created by the authenticated user. Omit or leave empty to return all results. Use `self` to filter by the authenticated user.

Available options:

`self`

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-rfq-creator-user-id)

rfq\_creator\_user\_id

string

Filter quotes by RFQ creator user ID

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-rfq-creator-subtrader-id)

rfq\_creator\_subtrader\_id

string

Filter quotes by RFQ creator subtrader ID (FCM members only)

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#parameter-rfq-id)

rfq\_id

string

Filter quotes by RFQ ID

#### Response

200

application/json

Quotes retrieved successfully

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#response-quotes)

quotes

object\[\]

required

List of quotes matching the query criteria

Show child attributes

[​

](https://docs.kalshi.com/api-reference/communications/get-quotes#response-cursor)

cursor

string

Cursor for pagination to get the next page of results

[Confirm RFQ Quote](https://docs.kalshi.com/api-reference/communications/confirm-rfq-quote)[Create Quote](https://docs.kalshi.com/api-reference/communications/create-quote)
