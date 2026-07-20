---
title: "Propose Block Trade - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/propose-block-trade"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:20.374Z"
---
Propose Block Trade

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "buyer_user_id": "<string>",
  "seller_user_id": "<string>",
  "market_ticker": "<string>",
  "price_centi_cents": 2,
  "centicount": 2,
  "expiration_ts": "2023-11-07T05:31:56Z",
  "buyer_subtrader_id": "<string>",
  "buyer_subaccount": 31,
  "seller_subtrader_id": "<string>",
  "seller_subaccount": 31
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"

payload = {
    "buyer_user_id": "<string>",
    "seller_user_id": "<string>",
    "market_ticker": "<string>",
    "price_centi_cents": 2,
    "centicount": 2,
    "expiration_ts": "2023-11-07T05:31:56Z",
    "buyer_subtrader_id": "<string>",
    "buyer_subaccount": 31,
    "seller_subtrader_id": "<string>",
    "seller_subaccount": 31
}
headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```

```
const options = {
  method: 'POST',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    buyer_user_id: '<string>',
    seller_user_id: '<string>',
    market_ticker: '<string>',
    price_centi_cents: 2,
    centicount: 2,
    expiration_ts: '2023-11-07T05:31:56Z',
    buyer_subtrader_id: '<string>',
    buyer_subaccount: 31,
    seller_subtrader_id: '<string>',
    seller_subaccount: 31
  })
};

fetch('https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'buyer_user_id' => '<string>',
    'seller_user_id' => '<string>',
    'market_ticker' => '<string>',
    'price_centi_cents' => 2,
    'centicount' => 2,
    'expiration_ts' => '2023-11-07T05:31:56Z',
    'buyer_subtrader_id' => '<string>',
    'buyer_subaccount' => 31,
    'seller_subtrader_id' => '<string>',
    'seller_subaccount' => 31
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

	url := "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"

	payload := strings.NewReader("{\n  \"buyer_user_id\": \"<string>\",\n  \"seller_user_id\": \"<string>\",\n  \"market_ticker\": \"<string>\",\n  \"price_centi_cents\": 2,\n  \"centicount\": 2,\n  \"expiration_ts\": \"2023-11-07T05:31:56Z\",\n  \"buyer_subtrader_id\": \"<string>\",\n  \"buyer_subaccount\": 31,\n  \"seller_subtrader_id\": \"<string>\",\n  \"seller_subaccount\": 31\n}")

	req, _ := http.NewRequest("POST", url, payload)

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"buyer_user_id\": \"<string>\",\n  \"seller_user_id\": \"<string>\",\n  \"market_ticker\": \"<string>\",\n  \"price_centi_cents\": 2,\n  \"centicount\": 2,\n  \"expiration_ts\": \"2023-11-07T05:31:56Z\",\n  \"buyer_subtrader_id\": \"<string>\",\n  \"buyer_subaccount\": 31,\n  \"seller_subtrader_id\": \"<string>\",\n  \"seller_subaccount\": 31\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"buyer_user_id\": \"<string>\",\n  \"seller_user_id\": \"<string>\",\n  \"market_ticker\": \"<string>\",\n  \"price_centi_cents\": 2,\n  \"centicount\": 2,\n  \"expiration_ts\": \"2023-11-07T05:31:56Z\",\n  \"buyer_subtrader_id\": \"<string>\",\n  \"buyer_subaccount\": 31,\n  \"seller_subtrader_id\": \"<string>\",\n  \"seller_subaccount\": 31\n}"

response = http.request(request)
puts response.read_body
```

201

400

401

403

500

```
{
  "block_trade_proposal_id": "<string>"
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

POST

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

communications

/

block-trade-proposals

Try it

Propose Block Trade

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "buyer_user_id": "<string>",
  "seller_user_id": "<string>",
  "market_ticker": "<string>",
  "price_centi_cents": 2,
  "centicount": 2,
  "expiration_ts": "2023-11-07T05:31:56Z",
  "buyer_subtrader_id": "<string>",
  "buyer_subaccount": 31,
  "seller_subtrader_id": "<string>",
  "seller_subaccount": 31
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"

payload = {
    "buyer_user_id": "<string>",
    "seller_user_id": "<string>",
    "market_ticker": "<string>",
    "price_centi_cents": 2,
    "centicount": 2,
    "expiration_ts": "2023-11-07T05:31:56Z",
    "buyer_subtrader_id": "<string>",
    "buyer_subaccount": 31,
    "seller_subtrader_id": "<string>",
    "seller_subaccount": 31
}
headers = {
    "KALSHI-ACCESS-KEY": "<api-key>",
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
```

```
const options = {
  method: 'POST',
  headers: {
    'KALSHI-ACCESS-KEY': '<api-key>',
    'KALSHI-ACCESS-SIGNATURE': '<api-key>',
    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    buyer_user_id: '<string>',
    seller_user_id: '<string>',
    market_ticker: '<string>',
    price_centi_cents: 2,
    centicount: 2,
    expiration_ts: '2023-11-07T05:31:56Z',
    buyer_subtrader_id: '<string>',
    buyer_subaccount: 31,
    seller_subtrader_id: '<string>',
    seller_subaccount: 31
  })
};

fetch('https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'buyer_user_id' => '<string>',
    'seller_user_id' => '<string>',
    'market_ticker' => '<string>',
    'price_centi_cents' => 2,
    'centicount' => 2,
    'expiration_ts' => '2023-11-07T05:31:56Z',
    'buyer_subtrader_id' => '<string>',
    'buyer_subaccount' => 31,
    'seller_subtrader_id' => '<string>',
    'seller_subaccount' => 31
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

	url := "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals"

	payload := strings.NewReader("{\n  \"buyer_user_id\": \"<string>\",\n  \"seller_user_id\": \"<string>\",\n  \"market_ticker\": \"<string>\",\n  \"price_centi_cents\": 2,\n  \"centicount\": 2,\n  \"expiration_ts\": \"2023-11-07T05:31:56Z\",\n  \"buyer_subtrader_id\": \"<string>\",\n  \"buyer_subaccount\": 31,\n  \"seller_subtrader_id\": \"<string>\",\n  \"seller_subaccount\": 31\n}")

	req, _ := http.NewRequest("POST", url, payload)

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"buyer_user_id\": \"<string>\",\n  \"seller_user_id\": \"<string>\",\n  \"market_ticker\": \"<string>\",\n  \"price_centi_cents\": 2,\n  \"centicount\": 2,\n  \"expiration_ts\": \"2023-11-07T05:31:56Z\",\n  \"buyer_subtrader_id\": \"<string>\",\n  \"buyer_subaccount\": 31,\n  \"seller_subtrader_id\": \"<string>\",\n  \"seller_subaccount\": 31\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"buyer_user_id\": \"<string>\",\n  \"seller_user_id\": \"<string>\",\n  \"market_ticker\": \"<string>\",\n  \"price_centi_cents\": 2,\n  \"centicount\": 2,\n  \"expiration_ts\": \"2023-11-07T05:31:56Z\",\n  \"buyer_subtrader_id\": \"<string>\",\n  \"buyer_subaccount\": 31,\n  \"seller_subtrader_id\": \"<string>\",\n  \"seller_subaccount\": 31\n}"

response = http.request(request)
puts response.read_body
```

201

400

401

403

500

```
{
  "block_trade_proposal_id": "<string>"
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

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-buyer-user-id)

buyer\_user\_id

string

required

User ID of the buyer

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-seller-user-id)

seller\_user\_id

string

required

User ID of the seller

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-market-ticker)

market\_ticker

string

required

The ticker of the market for this block trade

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-price-centi-cents)

price\_centi\_cents

integer<int64>

required

Price in centi-cents

Required range: `x >= 1`

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-centicount)

centicount

integer<int64>

required

Number of contracts in centicounts

Required range: `x >= 1`

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-maker-side)

maker\_side

enum<string>

required

The maker side of the trade

Available options:

`yes`,

`no`

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-expiration-ts)

expiration\_ts

string<date-time>

required

Expiration time of the proposal

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-buyer-subtrader-id)

buyer\_subtrader\_id

string

Subtrader ID of the buyer. Provide either this or buyer\_subaccount, not both.

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-buyer-subaccount)

buyer\_subaccount

integer

User-managed subaccount number of the buyer (0 for primary, 1-63 for numbered subaccounts). Provide either this or buyer\_subtrader\_id, not both.

Required range: `0 <= x <= 63`

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-seller-subtrader-id)

seller\_subtrader\_id

string

Subtrader ID of the seller. Provide either this or seller\_subaccount, not both.

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#body-seller-subaccount)

seller\_subaccount

integer

User-managed subaccount number of the seller (0 for primary, 1-63 for numbered subaccounts). Provide either this or seller\_subtrader\_id, not both.

Required range: `0 <= x <= 63`

#### Response

201

application/json

Block trade proposal created successfully

[​

](https://docs.kalshi.com/api-reference/communications/propose-block-trade#response-block-trade-proposal-id)

block\_trade\_proposal\_id

string

required

The ID of the newly created block trade proposal

[Get Block Trade Proposals](https://docs.kalshi.com/api-reference/communications/get-block-trade-proposals)[Accept Block Trade Proposal](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal)
