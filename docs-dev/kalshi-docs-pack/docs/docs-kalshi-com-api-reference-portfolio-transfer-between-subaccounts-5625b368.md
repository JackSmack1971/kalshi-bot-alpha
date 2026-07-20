---
title: "Transfer Between Subaccounts - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:16.582Z"
---
Transfer Between Subaccounts

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "client_transfer_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
  "from_subaccount": 123,
  "to_subaccount": 123,
  "amount_cents": 123,
  "exchange_index": 0
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer"

payload = {
    "client_transfer_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
    "from_subaccount": 123,
    "to_subaccount": 123,
    "amount_cents": 123,
    "exchange_index": 0
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
    client_transfer_id: '3c90c3cc-0d44-4b50-8888-8dd25736052a',
    from_subaccount: 123,
    to_subaccount: 123,
    amount_cents: 123,
    exchange_index: 0
  })
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'client_transfer_id' => '3c90c3cc-0d44-4b50-8888-8dd25736052a',
    'from_subaccount' => 123,
    'to_subaccount' => 123,
    'amount_cents' => 123,
    'exchange_index' => 0
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer"

	payload := strings.NewReader("{\n  \"client_transfer_id\": \"3c90c3cc-0d44-4b50-8888-8dd25736052a\",\n  \"from_subaccount\": 123,\n  \"to_subaccount\": 123,\n  \"amount_cents\": 123,\n  \"exchange_index\": 0\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"client_transfer_id\": \"3c90c3cc-0d44-4b50-8888-8dd25736052a\",\n  \"from_subaccount\": 123,\n  \"to_subaccount\": 123,\n  \"amount_cents\": 123,\n  \"exchange_index\": 0\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"client_transfer_id\": \"3c90c3cc-0d44-4b50-8888-8dd25736052a\",\n  \"from_subaccount\": 123,\n  \"to_subaccount\": 123,\n  \"amount_cents\": 123,\n  \"exchange_index\": 0\n}"

response = http.request(request)
puts response.read_body
```

200

400

401

500

```
{}
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

portfolio

/

subaccounts

/

transfer

Try it

Transfer Between Subaccounts

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "client_transfer_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
  "from_subaccount": 123,
  "to_subaccount": 123,
  "amount_cents": 123,
  "exchange_index": 0
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer"

payload = {
    "client_transfer_id": "3c90c3cc-0d44-4b50-8888-8dd25736052a",
    "from_subaccount": 123,
    "to_subaccount": 123,
    "amount_cents": 123,
    "exchange_index": 0
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
    client_transfer_id: '3c90c3cc-0d44-4b50-8888-8dd25736052a',
    from_subaccount: 123,
    to_subaccount: 123,
    amount_cents: 123,
    exchange_index: 0
  })
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'client_transfer_id' => '3c90c3cc-0d44-4b50-8888-8dd25736052a',
    'from_subaccount' => 123,
    'to_subaccount' => 123,
    'amount_cents' => 123,
    'exchange_index' => 0
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer"

	payload := strings.NewReader("{\n  \"client_transfer_id\": \"3c90c3cc-0d44-4b50-8888-8dd25736052a\",\n  \"from_subaccount\": 123,\n  \"to_subaccount\": 123,\n  \"amount_cents\": 123,\n  \"exchange_index\": 0\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"client_transfer_id\": \"3c90c3cc-0d44-4b50-8888-8dd25736052a\",\n  \"from_subaccount\": 123,\n  \"to_subaccount\": 123,\n  \"amount_cents\": 123,\n  \"exchange_index\": 0\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/transfer")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"client_transfer_id\": \"3c90c3cc-0d44-4b50-8888-8dd25736052a\",\n  \"from_subaccount\": 123,\n  \"to_subaccount\": 123,\n  \"amount_cents\": 123,\n  \"exchange_index\": 0\n}"

response = http.request(request)
puts response.read_body
```

200

400

401

500

```
{}
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

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#body-client-transfer-id)

client\_transfer\_id

string<uuid>

required

Unique client-provided transfer ID for idempotency.

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#body-from-subaccount)

from\_subaccount

integer

required

Source subaccount number (0 for primary, 1-63 for numbered subaccounts).

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#body-to-subaccount)

to\_subaccount

integer

required

Destination subaccount number (0 for primary, 1-63 for numbered subaccounts).

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#body-amount-cents)

amount\_cents

integer<int64>

required

Amount to transfer in cents.

[​

](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts#body-exchange-index)

exchange\_index

integer

Identifier for an exchange shard. Defaults to 0 if unspecified.

Example:

`0`

#### Response

200

application/json

Transfer completed successfully

Empty response indicating successful transfer.

[Create Subaccount](https://docs.kalshi.com/api-reference/portfolio/create-subaccount)[Get All Subaccount Balances](https://docs.kalshi.com/api-reference/portfolio/get-all-subaccount-balances)
