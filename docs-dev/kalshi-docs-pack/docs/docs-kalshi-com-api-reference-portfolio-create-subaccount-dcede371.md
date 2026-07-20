---
title: "Create Subaccount - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/create-subaccount"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:16.440Z"
---
Create Subaccount

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "exchange_index": 0
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts"

payload = { "exchange_index": 0 }
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
  body: JSON.stringify({exchange_index: 0})
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts"

	payload := strings.NewReader("{\n  \"exchange_index\": 0\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"exchange_index\": 0\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"exchange_index\": 0\n}"

response = http.request(request)
puts response.read_body
```

201

400

401

500

```
{
  "subaccount_number": 123
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

subaccounts

Try it

Create Subaccount

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "exchange_index": 0
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts"

payload = { "exchange_index": 0 }
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
  body: JSON.stringify({exchange_index: 0})
};

fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
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

	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts"

	payload := strings.NewReader("{\n  \"exchange_index\": 0\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"exchange_index\": 0\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"exchange_index\": 0\n}"

response = http.request(request)
puts response.read_body
```

201

400

401

500

```
{
  "subaccount_number": 123
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

](https://docs.kalshi.com/api-reference/portfolio/create-subaccount#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/create-subaccount#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/create-subaccount#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/portfolio/create-subaccount#body-exchange-index)

exchange\_index

integer

Identifier for an exchange shard. Defaults to 0 if unspecified.

Example:

`0`

#### Response

201

application/json

Subaccount created successfully

[​

](https://docs.kalshi.com/api-reference/portfolio/create-subaccount#response-subaccount-number)

subaccount\_number

integer

required

The sequential number assigned to this subaccount (1-63).

[Intra Account Transfer](https://docs.kalshi.com/api-reference/portfolio/intra-account-transfer)[Transfer Between Subaccounts](https://docs.kalshi.com/api-reference/portfolio/transfer-between-subaccounts)
