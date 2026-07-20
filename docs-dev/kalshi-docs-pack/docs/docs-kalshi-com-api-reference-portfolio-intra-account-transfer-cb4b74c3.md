---
title: "Intra Account Transfer - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:16.235Z"
---
Intra Account Transfer

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "amount": 123,
  "source_exchange_shard": 0,
  "destination_exchange_shard": 0
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer"

payload = {
    "amount": 123,
    "source_exchange_shard": 0,
    "destination_exchange_shard": 0
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
  body: JSON.stringify({amount: 123, source_exchange_shard: 0, destination_exchange_shard: 0})
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'amount' => 123,
    'source_exchange_shard' => 0,
    'destination_exchange_shard' => 0
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer"

	payload := strings.NewReader("{\n  \"amount\": 123,\n  \"source_exchange_shard\": 0,\n  \"destination_exchange_shard\": 0\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"amount\": 123,\n  \"source_exchange_shard\": 0,\n  \"destination_exchange_shard\": 0\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"amount\": 123,\n  \"source_exchange_shard\": 0,\n  \"destination_exchange_shard\": 0\n}"

response = http.request(request)
puts response.read_body
```

200

400

401

403

500

```
{
  "transfer_id": "<string>"
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

portfolio

/

intra\_exchange\_instance\_transfer

Try it

Intra Account Transfer

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "amount": 123,
  "source_exchange_shard": 0,
  "destination_exchange_shard": 0
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer"

payload = {
    "amount": 123,
    "source_exchange_shard": 0,
    "destination_exchange_shard": 0
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
  body: JSON.stringify({amount: 123, source_exchange_shard: 0, destination_exchange_shard: 0})
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'amount' => 123,
    'source_exchange_shard' => 0,
    'destination_exchange_shard' => 0
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer"

	payload := strings.NewReader("{\n  \"amount\": 123,\n  \"source_exchange_shard\": 0,\n  \"destination_exchange_shard\": 0\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"amount\": 123,\n  \"source_exchange_shard\": 0,\n  \"destination_exchange_shard\": 0\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/intra_exchange_instance_transfer")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"amount\": 123,\n  \"source_exchange_shard\": 0,\n  \"destination_exchange_shard\": 0\n}"

response = http.request(request)
puts response.read_body
```

200

400

401

403

500

```
{
  "transfer_id": "<string>"
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

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#body-source)

source

enum<string>

required

The source exchange instance

Available options:

`event_contract`,

`margined`

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#body-destination)

destination

enum<string>

required

The destination exchange instance

Available options:

`event_contract`,

`margined`

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#body-amount)

amount

integer<int64>

required

The amount to transfer in centicents

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#body-source-exchange-shard)

source\_exchange\_shard

integer

default:0

Source exchange shard index (default 0)

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#body-destination-exchange-shard)

destination\_exchange\_shard

integer

default:0

Destination exchange shard index (default 0)

#### Response

200

application/json

Transfer request accepted. The transfer is processed asynchronously.

[​

](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer#response-transfer-id)

transfer\_id

string

required

The ID of the transfer that was created

[Get Balance](https://docs.kalshi.com/api-reference/portfolio/get-balance)[Create Subaccount](https://docs.kalshi.com/api-reference/portfolio/create-subaccount)
