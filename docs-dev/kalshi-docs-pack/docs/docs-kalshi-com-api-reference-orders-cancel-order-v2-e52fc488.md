---
title: "Cancel Order (V2) - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/orders/cancel-order-v2"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:15.236Z"
---
Cancel Order (V2)

cURL

```
curl --request DELETE \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id} \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.delete(url, headers=headers)print(response.text)
```

```
const options = {  method: 'DELETE',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "DELETE",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}"	req, _ := http.NewRequest("DELETE", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.delete("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Delete.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

401

404

500

```
{
  "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
  "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
  "reduced_by": "10.00",
  "ts_ms": 1715793660456
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

DELETE

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

events

/

orders

/

{order\_id}

Try it

Cancel Order (V2)

cURL

```
curl --request DELETE \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id} \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}"headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>"}response = requests.delete(url, headers=headers)print(response.text)
```

```
const options = {  method: 'DELETE',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>'  }};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "DELETE",  CURLOPT_HTTPHEADER => [    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}"	req, _ := http.NewRequest("DELETE", url, nil)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.delete("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/{order_id}")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Delete.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'response = http.request(request)puts response.read_body
```

200

401

404

500

```
{
  "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
  "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
  "reduced_by": "10.00",
  "ts_ms": 1715793660456
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

**Rate limit:** 2 tokens per request. See `GET /trade-api/v2/account/endpoint_costs` for current non-default endpoint costs.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#parameter-order-id)

order\_id

string

required

Order ID

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#parameter-subaccount)

subaccount

integer

Subaccount number (0 for primary, 1-63 for subaccounts). Defaults to 0.

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#parameter-exchange-index)

exchange\_index

integer

Identifier for an exchange shard. Defaults to 0 if unspecified. Note: currently only 0 supported.

Example:

`0`

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#parameter-market-ticker)

market\_ticker

string

Market ticker. Required when exchange\_index is -1 (auto).

#### Response

200

application/json

Order cancelled successfully

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#response-order-id)

order\_id

string

required

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#response-reduced-by)

reduced\_by

string

required

Number of contracts that were canceled (i.e. the remaining count at time of cancellation).

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#response-ts-ms)

ts\_ms

integer<int64>

required

Matching engine timestamp at which the cancellation was processed, as Unix epoch milliseconds.

[​

](https://docs.kalshi.com/api-reference/orders/cancel-order-v2#response-client-order-id)

client\_order\_id

string

[Batch Cancel Orders (V2)](https://docs.kalshi.com/api-reference/orders/batch-cancel-orders-v2)[Amend Order (V2)](https://docs.kalshi.com/api-reference/orders/amend-order-v2)
