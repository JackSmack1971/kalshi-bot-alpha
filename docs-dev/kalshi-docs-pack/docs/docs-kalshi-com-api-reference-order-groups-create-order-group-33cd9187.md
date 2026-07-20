---
title: "Create Order Group - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/order-groups/create-order-group"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:18.431Z"
---
Create Order Group

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "subaccount": 0,
  "contracts_limit": 2,
  "contracts_limit_fp": "10.00",
  "exchange_index": 0
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create"payload = {    "subaccount": 0,    "contracts_limit": 2,    "contracts_limit_fp": "10.00",    "exchange_index": 0}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    subaccount: 0,    contracts_limit: 2,    contracts_limit_fp: '10.00',    exchange_index: 0  })};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'subaccount' => 0,    'contracts_limit' => 2,    'contracts_limit_fp' => '10.00',    'exchange_index' => 0  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create"	payload := strings.NewReader("{\n  \"subaccount\": 0,\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\",\n  \"exchange_index\": 0\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"subaccount\": 0,\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\",\n  \"exchange_index\": 0\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"subaccount\": 0,\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\",\n  \"exchange_index\": 0\n}"response = http.request(request)puts response.read_body
```

201

400

401

500

```
{
  "order_group_id": "<string>",
  "subaccount": 1,
  "exchange_index": 0
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

POST

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

order\_groups

/

create

Try it

Create Order Group

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "subaccount": 0,
  "contracts_limit": 2,
  "contracts_limit_fp": "10.00",
  "exchange_index": 0
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create"payload = {    "subaccount": 0,    "contracts_limit": 2,    "contracts_limit_fp": "10.00",    "exchange_index": 0}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    subaccount: 0,    contracts_limit: 2,    contracts_limit_fp: '10.00',    exchange_index: 0  })};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'subaccount' => 0,    'contracts_limit' => 2,    'contracts_limit_fp' => '10.00',    'exchange_index' => 0  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create"	payload := strings.NewReader("{\n  \"subaccount\": 0,\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\",\n  \"exchange_index\": 0\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"subaccount\": 0,\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\",\n  \"exchange_index\": 0\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/order_groups/create")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"subaccount\": 0,\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\",\n  \"exchange_index\": 0\n}"response = http.request(request)puts response.read_body
```

201

400

401

500

```
{
  "order_group_id": "<string>",
  "subaccount": 1,
  "exchange_index": 0
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

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#body-subaccount)

subaccount

integer

default:0

Optional subaccount number to use for this order group (0 for primary, 1-63 for subaccounts)

Required range: `x >= 0`

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#body-contracts-limit)

contracts\_limit

integer<int64>

Specifies the maximum number of contracts that can be matched within this group over a rolling 15-second window. Whole contracts only. Provide contracts\_limit or contracts\_limit\_fp; if both provided they must match.

Required range: `x >= 1`

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#body-contracts-limit-fp-one-of-0)

contracts\_limit\_fp

string | null

String representation of the maximum number of contracts that can be matched within this group over a rolling 15-second window. Provide contracts\_limit or contracts\_limit\_fp; if both provided they must match.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#body-exchange-index)

exchange\_index

integer

default:0

Identifier for an exchange shard. Defaults to 0 if unspecified. Note: currently only 0 supported.

Example:

`0`

#### Response

201

application/json

Order group created successfully

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#response-order-group-id)

order\_group\_id

string

required

The unique identifier for the created order group

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#response-subaccount)

subaccount

integer

required

Subaccount number that owns the created order group (0 for primary, 1-63 for subaccounts).

Required range: `x >= 0`

[​

](https://docs.kalshi.com/api-reference/order-groups/create-order-group#response-exchange-index)

exchange\_index

integer

Identifier for an exchange shard. Defaults to 0 if unspecified. Note: currently only 0 supported.

Example:

`0`

[Get Order Groups](https://docs.kalshi.com/api-reference/order-groups/get-order-groups)[Get Order Group](https://docs.kalshi.com/api-reference/order-groups/get-order-group)
