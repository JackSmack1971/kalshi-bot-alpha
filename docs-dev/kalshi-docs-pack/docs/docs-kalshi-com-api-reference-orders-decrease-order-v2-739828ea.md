---
title: "Decrease Order (V2) - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/orders/decrease-order-v2"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:15.646Z"
---
Decrease Order (V2)

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "reduce_by": "2.00",
  "exchange_index": 0
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease"payload = {    "reduce_by": "2.00",    "exchange_index": 0}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({reduce_by: '2.00', exchange_index: 0})};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'reduce_by' => '2.00',    'exchange_index' => 0  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease"	payload := strings.NewReader("{\n  \"reduce_by\": \"2.00\",\n  \"exchange_index\": 0\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"reduce_by\": \"2.00\",\n  \"exchange_index\": 0\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"reduce_by\": \"2.00\",\n  \"exchange_index\": 0\n}"response = http.request(request)puts response.read_body
```

200

400

401

404

500

```
{
  "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
  "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
  "remaining_count": "8.00",
  "ts_ms": 1715793680789
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

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

POST

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

events

/

orders

/

{order\_id}

/

decrease

Try it

Decrease Order (V2)

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "reduce_by": "2.00",
  "exchange_index": 0
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease"payload = {    "reduce_by": "2.00",    "exchange_index": 0}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({reduce_by: '2.00', exchange_index: 0})};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'reduce_by' => '2.00',    'exchange_index' => 0  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease"	payload := strings.NewReader("{\n  \"reduce_by\": \"2.00\",\n  \"exchange_index\": 0\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"reduce_by\": \"2.00\",\n  \"exchange_index\": 0\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/decrease")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"reduce_by\": \"2.00\",\n  \"exchange_index\": 0\n}"response = http.request(request)puts response.read_body
```

200

400

401

404

500

```
{
  "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
  "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
  "remaining_count": "8.00",
  "ts_ms": 1715793680789
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

```
{  "code": "<string>",  "message": "<string>",  "details": "<string>",  "service": "<string>"}
```

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#parameter-order-id)

order\_id

string

required

Order ID

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#parameter-subaccount)

subaccount

integer

Subaccount number (0 for primary, 1-63 for subaccounts). Defaults to 0.

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#body-reduce-by-one-of-0)

reduce\_by

string | null

String representation of the number of contracts to reduce by. Exactly one of `reduce_by` or `reduce_to` must be provided.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#body-reduce-to-one-of-0)

reduce\_to

string | null

String representation of the number of contracts to reduce to. Exactly one of `reduce_by` or `reduce_to` must be provided.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#body-exchange-index)

exchange\_index

integer

default:0

Identifier for an exchange shard. Defaults to 0 if unspecified. Note: currently only 0 supported.

Example:

`0`

#### Response

200

application/json

Order decreased successfully

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#response-order-id)

order\_id

string

required

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#response-remaining-count)

remaining\_count

string

required

Number of contracts remaining after the decrease.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#response-ts-ms)

ts\_ms

integer<int64>

required

Matching engine timestamp at which the decrease was processed, as Unix epoch milliseconds.

[​

](https://docs.kalshi.com/api-reference/orders/decrease-order-v2#response-client-order-id)

client\_order\_id

string

[Amend Order (V2)](https://docs.kalshi.com/api-reference/orders/amend-order-v2)[Get Order Groups](https://docs.kalshi.com/api-reference/order-groups/get-order-groups)
