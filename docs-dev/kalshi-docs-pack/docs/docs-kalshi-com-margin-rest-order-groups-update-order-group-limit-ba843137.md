---
title: "Update Order Group Limit - API Documentation"
source_url: "https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:14.149Z"
---
Update Order Group Limit

cURL

```
curl --request PUT \
  --url https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "contracts_limit": 2,
  "contracts_limit_fp": "10.00"
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit"payload = {    "contracts_limit": 2,    "contracts_limit_fp": "10.00"}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.put(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'PUT',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({contracts_limit: 2, contracts_limit_fp: '10.00'})};fetch('https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "PUT",  CURLOPT_POSTFIELDS => json_encode([    'contracts_limit' => 2,    'contracts_limit_fp' => '10.00'  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit"	payload := strings.NewReader("{\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\"\n}")	req, _ := http.NewRequest("PUT", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.put("https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\"\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Put.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\"\n}"response = http.request(request)puts response.read_body
```

200

400

401

404

500

```
{}
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

PUT

https://external-api.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2

/

margin

/

order\_groups

/

{order\_group\_id}

/

limit

Try it

Update Order Group Limit

cURL

```
curl --request PUT \
  --url https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "contracts_limit": 2,
  "contracts_limit_fp": "10.00"
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit"payload = {    "contracts_limit": 2,    "contracts_limit_fp": "10.00"}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.put(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'PUT',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({contracts_limit: 2, contracts_limit_fp: '10.00'})};fetch('https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "PUT",  CURLOPT_POSTFIELDS => json_encode([    'contracts_limit' => 2,    'contracts_limit_fp' => '10.00'  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit"	payload := strings.NewReader("{\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\"\n}")	req, _ := http.NewRequest("PUT", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.put("https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\"\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/margin/order_groups/{order_group_id}/limit")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Put.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"contracts_limit\": 2,\n  \"contracts_limit_fp\": \"10.00\"\n}"response = http.request(request)puts response.read_body
```

200

400

401

404

500

```
{}
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

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#parameter-order-group-id)

order\_group\_id

string

required

Order group ID

#### Query Parameters

[​

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#parameter-subaccount)

subaccount

integer

default:0

Subaccount number (0 for primary, 1-63 for subaccounts). Defaults to 0.

Required range: `x >= 0`

#### Body

application/json

[​

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#body-contracts-limit)

contracts\_limit

integer<int64>

New maximum number of contracts that can be matched within this group over a rolling 15-second window. Whole contracts only. Provide contracts\_limit or contracts\_limit\_fp; if both provided they must match.

Required range: `x >= 1`

[​

](https://docs.kalshi.com/margin-rest/order-groups/update-order-group-limit#body-contracts-limit-fp-one-of-0)

contracts\_limit\_fp

string | null

String representation of the new maximum number of contracts that can be matched within this group over a rolling 15-second window. Provide contracts\_limit or contracts\_limit\_fp; if both provided they must match.

Example:

`"10.00"`

#### Response

200

application/json

Order group limit updated successfully

An empty response body

[Trigger Order Group](https://docs.kalshi.com/margin-rest/order-groups/trigger-order-group)[WebSocket Connection](https://docs.kalshi.com/margin-ws/websockets/websocket-connection)
