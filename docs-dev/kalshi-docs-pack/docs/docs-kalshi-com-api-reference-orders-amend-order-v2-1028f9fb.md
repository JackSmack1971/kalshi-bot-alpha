---
title: "Amend Order (V2) - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/orders/amend-order-v2"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:15.435Z"
---
Amend Order (V2)

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "ticker": "HIGHNY-24JAN01-T60",
  "side": "bid",
  "price": "0.5700",
  "count": "8.00",
  "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
  "updated_client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
  "exchange_index": 0
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend"payload = {    "ticker": "HIGHNY-24JAN01-T60",    "side": "bid",    "price": "0.5700",    "count": "8.00",    "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",    "updated_client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",    "exchange_index": 0}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    ticker: 'HIGHNY-24JAN01-T60',    side: 'bid',    price: '0.5700',    count: '8.00',    client_order_id: '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',    updated_client_order_id: '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',    exchange_index: 0  })};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'ticker' => 'HIGHNY-24JAN01-T60',    'side' => 'bid',    'price' => '0.5700',    'count' => '8.00',    'client_order_id' => '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',    'updated_client_order_id' => '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',    'exchange_index' => 0  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend"	payload := strings.NewReader("{\n  \"ticker\": \"HIGHNY-24JAN01-T60\",\n  \"side\": \"bid\",\n  \"price\": \"0.5700\",\n  \"count\": \"8.00\",\n  \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n  \"updated_client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n  \"exchange_index\": 0\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"ticker\": \"HIGHNY-24JAN01-T60\",\n  \"side\": \"bid\",\n  \"price\": \"0.5700\",\n  \"count\": \"8.00\",\n  \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n  \"updated_client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n  \"exchange_index\": 0\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"ticker\": \"HIGHNY-24JAN01-T60\",\n  \"side\": \"bid\",\n  \"price\": \"0.5700\",\n  \"count\": \"8.00\",\n  \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n  \"updated_client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n  \"exchange_index\": 0\n}"response = http.request(request)puts response.read_body
```

200

400

401

404

500

```
{
  "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
  "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
  "remaining_count": "8.00",
  "fill_count": "0.00",
  "ts_ms": 1715793690123
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

amend

Try it

Amend Order (V2)

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "ticker": "HIGHNY-24JAN01-T60",
  "side": "bid",
  "price": "0.5700",
  "count": "8.00",
  "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
  "updated_client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
  "exchange_index": 0
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend"payload = {    "ticker": "HIGHNY-24JAN01-T60",    "side": "bid",    "price": "0.5700",    "count": "8.00",    "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",    "updated_client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",    "exchange_index": 0}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    ticker: 'HIGHNY-24JAN01-T60',    side: 'bid',    price: '0.5700',    count: '8.00',    client_order_id: '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',    updated_client_order_id: '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',    exchange_index: 0  })};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'ticker' => 'HIGHNY-24JAN01-T60',    'side' => 'bid',    'price' => '0.5700',    'count' => '8.00',    'client_order_id' => '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',    'updated_client_order_id' => '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',    'exchange_index' => 0  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend"	payload := strings.NewReader("{\n  \"ticker\": \"HIGHNY-24JAN01-T60\",\n  \"side\": \"bid\",\n  \"price\": \"0.5700\",\n  \"count\": \"8.00\",\n  \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n  \"updated_client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n  \"exchange_index\": 0\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"ticker\": \"HIGHNY-24JAN01-T60\",\n  \"side\": \"bid\",\n  \"price\": \"0.5700\",\n  \"count\": \"8.00\",\n  \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n  \"updated_client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n  \"exchange_index\": 0\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}/amend")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"ticker\": \"HIGHNY-24JAN01-T60\",\n  \"side\": \"bid\",\n  \"price\": \"0.5700\",\n  \"count\": \"8.00\",\n  \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n  \"updated_client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n  \"exchange_index\": 0\n}"response = http.request(request)puts response.read_body
```

200

400

401

404

500

```
{
  "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
  "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
  "remaining_count": "8.00",
  "fill_count": "0.00",
  "ts_ms": 1715793690123
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

Amending a resting order preserves queue position only when the amendment decreases size. All other amendments — like increasing size or changing price forfeit queue position and place the order at the back of the queue.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#parameter-order-id)

order\_id

string

required

Order ID

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#parameter-subaccount)

subaccount

integer

Subaccount number (0 for primary, 1-63 for subaccounts). Defaults to 0.

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-ticker)

ticker

string

required

Market ticker

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-side)

side

enum<string>

required

Side of the order

Available options:

`bid`,

`ask`

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-price)

price

string

required

Updated price for the order in fixed-point dollars.

Example:

`"0.5600"`

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-count)

count

string

required

Updated total/max fillable count for the order. Set this to the order's already filled count plus the desired resting remaining count after the amend.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-client-order-id)

client\_order\_id

string

The original client-specified order ID to be amended

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-updated-client-order-id)

updated\_client\_order\_id

string

The new client-specified order ID after amendment

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#body-exchange-index)

exchange\_index

integer

default:0

Identifier for an exchange shard. Defaults to 0 if unspecified. Note: currently only 0 supported.

Example:

`0`

#### Response

200

application/json

Order amended successfully

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-order-id)

order\_id

string

required

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-ts-ms)

ts\_ms

integer<int64>

required

Matching engine timestamp at which the amend was processed, as Unix epoch milliseconds.

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-client-order-id)

client\_order\_id

string

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-remaining-count-one-of-0)

remaining\_count

string | null

Number of resting contracts remaining after the amend. This is the actual post-amend resting quantity, not the request's total/max fillable count. Only present when the amend caused a fill or changed the resting size.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-fill-count-one-of-0)

fill\_count

string | null

Number of contracts filled as a result of the amend crossing the book. Only present when fills occurred or remaining size changed.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-average-fill-price-one-of-0)

average\_fill\_price

string | null

Volume-weighted average fill price for fills resulting from the amend. Only present when fills occurred.

Example:

`"0.5600"`

[​

](https://docs.kalshi.com/api-reference/orders/amend-order-v2#response-average-fee-paid-one-of-0)

average\_fee\_paid

string | null

Volume-weighted average fee paid per contract for fills resulting from the amend. Only present when fills occurred.

Example:

`"0.5600"`

[Cancel Order (V2)](https://docs.kalshi.com/api-reference/orders/cancel-order-v2)[Decrease Order (V2)](https://docs.kalshi.com/api-reference/orders/decrease-order-v2)
