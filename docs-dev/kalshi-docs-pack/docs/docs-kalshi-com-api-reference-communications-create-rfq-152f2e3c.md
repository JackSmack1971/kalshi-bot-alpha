---
title: "Create RFQ - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/create-rfq"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:20.895Z"
---
Create RFQ

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/rfqs \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "market_ticker": "<string>",
  "rest_remainder": true,
  "contracts": 123,
  "contracts_fp": "10.00",
  "target_cost_centi_cents": 123,
  "target_cost_dollars": "0.5600",
  "replace_existing": false,
  "subtrader_id": "<string>",
  "subaccount": 123
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"payload = {    "market_ticker": "<string>",    "rest_remainder": True,    "contracts": 123,    "contracts_fp": "10.00",    "target_cost_centi_cents": 123,    "target_cost_dollars": "0.5600",    "replace_existing": False,    "subtrader_id": "<string>",    "subaccount": 123}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    market_ticker: '<string>',    rest_remainder: true,    contracts: 123,    contracts_fp: '10.00',    target_cost_centi_cents: 123,    target_cost_dollars: '0.5600',    replace_existing: false,    subtrader_id: '<string>',    subaccount: 123  })};fetch('https://external-api.kalshi.com/trade-api/v2/communications/rfqs', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/rfqs",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'market_ticker' => '<string>',    'rest_remainder' => true,    'contracts' => 123,    'contracts_fp' => '10.00',    'target_cost_centi_cents' => 123,    'target_cost_dollars' => '0.5600',    'replace_existing' => false,    'subtrader_id' => '<string>',    'subaccount' => 123  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"	payload := strings.NewReader("{\n  \"market_ticker\": \"<string>\",\n  \"rest_remainder\": true,\n  \"contracts\": 123,\n  \"contracts_fp\": \"10.00\",\n  \"target_cost_centi_cents\": 123,\n  \"target_cost_dollars\": \"0.5600\",\n  \"replace_existing\": false,\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 123\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"market_ticker\": \"<string>\",\n  \"rest_remainder\": true,\n  \"contracts\": 123,\n  \"contracts_fp\": \"10.00\",\n  \"target_cost_centi_cents\": 123,\n  \"target_cost_dollars\": \"0.5600\",\n  \"replace_existing\": false,\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 123\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"market_ticker\": \"<string>\",\n  \"rest_remainder\": true,\n  \"contracts\": 123,\n  \"contracts_fp\": \"10.00\",\n  \"target_cost_centi_cents\": 123,\n  \"target_cost_dollars\": \"0.5600\",\n  \"replace_existing\": false,\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 123\n}"response = http.request(request)puts response.read_body
```

201

400

401

409

500

```
{
  "id": "<string>"
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

communications

/

rfqs

Try it

Create RFQ

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/rfqs \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "market_ticker": "<string>",
  "rest_remainder": true,
  "contracts": 123,
  "contracts_fp": "10.00",
  "target_cost_centi_cents": 123,
  "target_cost_dollars": "0.5600",
  "replace_existing": false,
  "subtrader_id": "<string>",
  "subaccount": 123
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"payload = {    "market_ticker": "<string>",    "rest_remainder": True,    "contracts": 123,    "contracts_fp": "10.00",    "target_cost_centi_cents": 123,    "target_cost_dollars": "0.5600",    "replace_existing": False,    "subtrader_id": "<string>",    "subaccount": 123}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    market_ticker: '<string>',    rest_remainder: true,    contracts: 123,    contracts_fp: '10.00',    target_cost_centi_cents: 123,    target_cost_dollars: '0.5600',    replace_existing: false,    subtrader_id: '<string>',    subaccount: 123  })};fetch('https://external-api.kalshi.com/trade-api/v2/communications/rfqs', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/rfqs",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'market_ticker' => '<string>',    'rest_remainder' => true,    'contracts' => 123,    'contracts_fp' => '10.00',    'target_cost_centi_cents' => 123,    'target_cost_dollars' => '0.5600',    'replace_existing' => false,    'subtrader_id' => '<string>',    'subaccount' => 123  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/rfqs"	payload := strings.NewReader("{\n  \"market_ticker\": \"<string>\",\n  \"rest_remainder\": true,\n  \"contracts\": 123,\n  \"contracts_fp\": \"10.00\",\n  \"target_cost_centi_cents\": 123,\n  \"target_cost_dollars\": \"0.5600\",\n  \"replace_existing\": false,\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 123\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"market_ticker\": \"<string>\",\n  \"rest_remainder\": true,\n  \"contracts\": 123,\n  \"contracts_fp\": \"10.00\",\n  \"target_cost_centi_cents\": 123,\n  \"target_cost_dollars\": \"0.5600\",\n  \"replace_existing\": false,\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 123\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/rfqs")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"market_ticker\": \"<string>\",\n  \"rest_remainder\": true,\n  \"contracts\": 123,\n  \"contracts_fp\": \"10.00\",\n  \"target_cost_centi_cents\": 123,\n  \"target_cost_dollars\": \"0.5600\",\n  \"replace_existing\": false,\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 123\n}"response = http.request(request)puts response.read_body
```

201

400

401

409

500

```
{
  "id": "<string>"
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

](https://docs.kalshi.com/api-reference/communications/create-rfq#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-market-ticker)

market\_ticker

string

required

The ticker of the market for which to create an RFQ

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-rest-remainder)

rest\_remainder

boolean

required

Whether to rest the remainder of the RFQ after execution

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-contracts)

contracts

integer

Whole-contract count for the RFQ. Use contracts\_fp for partial contract values; if both are provided, they must match.

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-contracts-fp-one-of-0)

contracts\_fp

string | null

Fixed-point number of contracts for the RFQ. Supports partial contracts in 0.01-contract increments; if contracts is also provided, both values must match.

Example:

`"10.00"`

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-target-cost-centi-cents)

target\_cost\_centi\_cents

integer<int64>

deprecated

DEPRECATED: The target cost for the RFQ in centi-cents. Use target\_cost\_dollars instead.

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-target-cost-dollars)

target\_cost\_dollars

string

The target cost for the RFQ in dollars

Example:

`"0.5600"`

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-replace-existing)

replace\_existing

boolean

default:false

Whether to delete existing RFQs as part of this RFQ's creation

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-subtrader-id)

subtrader\_id

string

The subtrader to create the RFQ for (FCM members only)

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#body-subaccount)

subaccount

integer

The subaccount number to create the RFQ for (direct members only; 0 for primary, 1-63 for subaccounts)

#### Response

201

application/json

RFQ created successfully

[​

](https://docs.kalshi.com/api-reference/communications/create-rfq#response-id)

id

string

required

The ID of the newly created RFQ

[Get RFQs](https://docs.kalshi.com/api-reference/communications/get-rfqs)[Get RFQ](https://docs.kalshi.com/api-reference/communications/get-rfq)
