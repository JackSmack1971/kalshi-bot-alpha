---
title: "Create API Key - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/api-keys/create-api-key"
host: "docs.kalshi.com"
depth: 5
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:25.392Z"
---
Create API Key

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/api_keys \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "name": "<string>",
  "public_key": "<string>",
  "scopes": [],
  "subaccount": 31
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/api_keys"

payload = {
    "name": "<string>",
    "public_key": "<string>",
    "scopes": [],
    "subaccount": 31
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
  body: JSON.stringify({name: '<string>', public_key: '<string>', scopes: [], subaccount: 31})
};

fetch('https://external-api.kalshi.com/trade-api/v2/api_keys', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/api_keys",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'name' => '<string>',
    'public_key' => '<string>',
    'scopes' => [

    ],
    'subaccount' => 31
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

	url := "https://external-api.kalshi.com/trade-api/v2/api_keys"

	payload := strings.NewReader("{\n  \"name\": \"<string>\",\n  \"public_key\": \"<string>\",\n  \"scopes\": [],\n  \"subaccount\": 31\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/api_keys")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"name\": \"<string>\",\n  \"public_key\": \"<string>\",\n  \"scopes\": [],\n  \"subaccount\": 31\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/api_keys")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"name\": \"<string>\",\n  \"public_key\": \"<string>\",\n  \"scopes\": [],\n  \"subaccount\": 31\n}"

response = http.request(request)
puts response.read_body
```

201

```
{
  "api_key_id": "<string>"
}
```

POST

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

api\_keys

Try it

Create API Key

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/api_keys \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "name": "<string>",
  "public_key": "<string>",
  "scopes": [],
  "subaccount": 31
}
'
```

```
import requests

url = "https://external-api.kalshi.com/trade-api/v2/api_keys"

payload = {
    "name": "<string>",
    "public_key": "<string>",
    "scopes": [],
    "subaccount": 31
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
  body: JSON.stringify({name: '<string>', public_key: '<string>', scopes: [], subaccount: 31})
};

fetch('https://external-api.kalshi.com/trade-api/v2/api_keys', options)
  .then(res => res.json())
  .then(res => console.log(res))
  .catch(err => console.error(err));
```

```
<?php

$curl = curl_init();

curl_setopt_array($curl, [
  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/api_keys",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => json_encode([
    'name' => '<string>',
    'public_key' => '<string>',
    'scopes' => [

    ],
    'subaccount' => 31
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

	url := "https://external-api.kalshi.com/trade-api/v2/api_keys"

	payload := strings.NewReader("{\n  \"name\": \"<string>\",\n  \"public_key\": \"<string>\",\n  \"scopes\": [],\n  \"subaccount\": 31\n}")

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
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/api_keys")
  .header("KALSHI-ACCESS-KEY", "<api-key>")
  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")
  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")
  .header("Content-Type", "application/json")
  .body("{\n  \"name\": \"<string>\",\n  \"public_key\": \"<string>\",\n  \"scopes\": [],\n  \"subaccount\": 31\n}")
  .asString();
```

```
require 'uri'
require 'net/http'

url = URI("https://external-api.kalshi.com/trade-api/v2/api_keys")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["KALSHI-ACCESS-KEY"] = '<api-key>'
request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'
request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"name\": \"<string>\",\n  \"public_key\": \"<string>\",\n  \"scopes\": [],\n  \"subaccount\": 31\n}"

response = http.request(request)
puts response.read_body
```

201

```
{
  "api_key_id": "<string>"
}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#body-name)

name

string

required

Name for the API key. This helps identify the key's purpose

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#body-public-key)

public\_key

string

required

RSA public key in PEM format. This will be used to verify signatures on API requests

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#body-scopes)

scopes

enum<string>\[\]

List of scopes to grant to the API key. If the broad `write` parent scope is included, `read` must also be included. Child scopes may be granted without the broad parent scope. Defaults to full access (`read`, `write`) if not provided.

Scope granted to an API key. Parent scopes grant broad access; for example, `read` grants all read endpoints and `write` grants all write endpoints. Child scopes such as `read::block_trade_accept`, `read::portfolio_balance`, `write::trade`, `write::transfer`, and `write::block_trade_accept` grant only their specific endpoint group and can be granted without the parent scope.

Available options:

`read`,

`write`,

`read::block_trade_accept`,

`read::portfolio_balance`,

`write::trade`,

`write::transfer`,

`write::block_trade_accept`

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#body-subaccount)

subaccount

integer

If set, restricts the API key to a single sub-account (0-63) that you own. A restricted key may only read and trade on that sub-account; it cannot act on other sub-accounts, transfer funds between sub-accounts, or create sub-accounts. Omit to leave the key unrestricted.

Required range: `0 <= x <= 63`

#### Response

201

application/json

API key created successfully

[​

](https://docs.kalshi.com/api-reference/api-keys/create-api-key#response-api-key-id)

api\_key\_id

string

required

Unique identifier for the newly created API key

[Get API Keys](https://docs.kalshi.com/api-reference/api-keys/get-api-keys)[Generate API Key](https://docs.kalshi.com/api-reference/api-keys/generate-api-key)
