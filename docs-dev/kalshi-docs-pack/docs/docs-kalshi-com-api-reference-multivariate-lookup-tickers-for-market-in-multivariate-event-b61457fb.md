---
title: "Lookup Tickers For Market In Multivariate Event Collection - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:23.253Z"
---
Lookup Tickers For Market In Multivariate Event Collection

cURL

```
curl --request PUT \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "selected_markets": [
    {
      "market_ticker": "<string>",
      "event_ticker": "<string>"
    }
  ]
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup"

payload = { "selected_markets": [
        {
            "market_ticker": "<string>",
            "event_ticker": "<string>"
        }
    ] }
headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```

```
const options = {
  method: 'PUT',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({selected_markets: [{market_ticker: '<string>', event_ticker: '<string>'}]})
};

fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "PUT",
  CURLOPT_POSTFIELDS => json_encode([
    'selected_markets' => [
        [
                'market_ticker' => '<string>',
                'event_ticker' => '<string>'
        ]
    ]
  ]),
  CURLOPT_HTTPHEADER => [
    "Content-Type: application/json",
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
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup"

	payload := strings.NewReader("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ]\n}")

	req, _ := http.NewRequest("PUT", url, payload)

	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
	req.Header.Add("Content-Type", "application/json")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.put("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ]\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Put.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ]\n}"

response = http.request(request)
puts response.read_body
```

200

400

401

404

500

```
{
  "event_ticker": "<string>",
  "market_ticker": "<string>"
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

PUT

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

multivariate\_event\_collections

/

{collection\_ticker}

/

lookup

Try it

Lookup Tickers For Market In Multivariate Event Collection

cURL

```
curl --request PUT \
  --url https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "selected_markets": [
    {
      "market_ticker": "<string>",
      "event_ticker": "<string>"
    }
  ]
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup"

payload = { "selected_markets": [
        {
            "market_ticker": "<string>",
            "event_ticker": "<string>"
        }
    ] }
headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.put(url, json=payload, headers=headers)

print(response.text)
```

```
const options = {
  method: 'PUT',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({selected_markets: [{market_ticker: '<string>', event_ticker: '<string>'}]})
};

fetch('https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "PUT",
  CURLOPT_POSTFIELDS => json_encode([
    'selected_markets' => [
        [
                'market_ticker' => '<string>',
                'event_ticker' => '<string>'
        ]
    ]
  ]),
  CURLOPT_HTTPHEADER => [
    "Content-Type: application/json",
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
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup"

	payload := strings.NewReader("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ]\n}")

	req, _ := http.NewRequest("PUT", url, payload)

	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")
	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
	req.Header.Add("Content-Type", "application/json")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(string(body))

}
```

```
HttpResponse<String> response = Unirest.put("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ]\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/multivariate_event_collections/{collection_ticker}/lookup")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Put.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"selected_markets\": [\n    {\n      \"market_ticker\": \"<string>\",\n      \"event_ticker\": \"<string>\"\n    }\n  ]\n}"

response = http.request(request)
puts response.read_body
```

200

400

401

404

500

```
{
  "event_ticker": "<string>",
  "market_ticker": "<string>"
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

This endpoint is deprecated and predates RFQs. Do not use it for new integrations.

**Rate limit:** 2 tokens per request. See `GET /trade-api/v2/account/endpoint_costs` for current non-default endpoint costs.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#parameter-collection-ticker)

collection\_ticker

string

required

Collection ticker

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#body-selected-markets)

selected\_markets

object\[\]

required

List of selected markets that act as parameters to determine which market is produced.

Show child attributes

#### Response

200

application/json

Market looked up successfully

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#response-event-ticker)

event\_ticker

string

required

Event ticker for the looked up market.

[​

](https://docs.kalshi.com/api-reference/multivariate/lookup-tickers-for-market-in-multivariate-event-collection#response-market-ticker)

market\_ticker

string

required

Market ticker for the looked up market.

[Get Multivariate Event Collections](https://docs.kalshi.com/api-reference/multivariate/get-multivariate-event-collections)[Get Incentives](https://docs.kalshi.com/api-reference/incentive-programs/get-incentives)
