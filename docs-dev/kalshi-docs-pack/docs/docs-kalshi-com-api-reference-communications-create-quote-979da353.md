---
title: "Create Quote - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/create-quote"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:22.269Z"
---
Create Quote

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/quotes \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "rfq_id": "<string>",
  "yes_bid": "0.5600",
  "no_bid": "0.5600",
  "rest_remainder": true,
  "post_only": true,
  "subaccount": 123
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/quotes"payload = {    "rfq_id": "<string>",    "yes_bid": "0.5600",    "no_bid": "0.5600",    "rest_remainder": True,    "post_only": True,    "subaccount": 123}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    rfq_id: '<string>',    yes_bid: '0.5600',    no_bid: '0.5600',    rest_remainder: true,    post_only: true,    subaccount: 123  })};fetch('https://external-api.kalshi.com/trade-api/v2/communications/quotes', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/quotes",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'rfq_id' => '<string>',    'yes_bid' => '0.5600',    'no_bid' => '0.5600',    'rest_remainder' => true,    'post_only' => true,    'subaccount' => 123  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/quotes"	payload := strings.NewReader("{\n  \"rfq_id\": \"<string>\",\n  \"yes_bid\": \"0.5600\",\n  \"no_bid\": \"0.5600\",\n  \"rest_remainder\": true,\n  \"post_only\": true,\n  \"subaccount\": 123\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/quotes")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"rfq_id\": \"<string>\",\n  \"yes_bid\": \"0.5600\",\n  \"no_bid\": \"0.5600\",\n  \"rest_remainder\": true,\n  \"post_only\": true,\n  \"subaccount\": 123\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/quotes")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"rfq_id\": \"<string>\",\n  \"yes_bid\": \"0.5600\",\n  \"no_bid\": \"0.5600\",\n  \"rest_remainder\": true,\n  \"post_only\": true,\n  \"subaccount\": 123\n}"response = http.request(request)puts response.read_body
```

201

400

401

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

POST

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

communications

/

quotes

Try it

Create Quote

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/quotes \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "rfq_id": "<string>",
  "yes_bid": "0.5600",
  "no_bid": "0.5600",
  "rest_remainder": true,
  "post_only": true,
  "subaccount": 123
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/quotes"payload = {    "rfq_id": "<string>",    "yes_bid": "0.5600",    "no_bid": "0.5600",    "rest_remainder": True,    "post_only": True,    "subaccount": 123}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    rfq_id: '<string>',    yes_bid: '0.5600',    no_bid: '0.5600',    rest_remainder: true,    post_only: true,    subaccount: 123  })};fetch('https://external-api.kalshi.com/trade-api/v2/communications/quotes', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/quotes",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'rfq_id' => '<string>',    'yes_bid' => '0.5600',    'no_bid' => '0.5600',    'rest_remainder' => true,    'post_only' => true,    'subaccount' => 123  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/quotes"	payload := strings.NewReader("{\n  \"rfq_id\": \"<string>\",\n  \"yes_bid\": \"0.5600\",\n  \"no_bid\": \"0.5600\",\n  \"rest_remainder\": true,\n  \"post_only\": true,\n  \"subaccount\": 123\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/quotes")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"rfq_id\": \"<string>\",\n  \"yes_bid\": \"0.5600\",\n  \"no_bid\": \"0.5600\",\n  \"rest_remainder\": true,\n  \"post_only\": true,\n  \"subaccount\": 123\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/quotes")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"rfq_id\": \"<string>\",\n  \"yes_bid\": \"0.5600\",\n  \"no_bid\": \"0.5600\",\n  \"rest_remainder\": true,\n  \"post_only\": true,\n  \"subaccount\": 123\n}"response = http.request(request)puts response.read_body
```

201

400

401

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

**Rate limit:** 2 tokens per request. See `GET /trade-api/v2/account/endpoint_costs` for current non-default endpoint costs.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#body-rfq-id)

rfq\_id

string

required

The ID of the RFQ to quote on

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#body-yes-bid)

yes\_bid

string

required

The bid price for YES contracts, in dollars

Example:

`"0.5600"`

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#body-no-bid)

no\_bid

string

required

The bid price for NO contracts, in dollars

Example:

`"0.5600"`

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#body-rest-remainder)

rest\_remainder

boolean

required

Whether to rest the remainder of the quote after execution

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#body-post-only)

post\_only

boolean

If true, the quote creator's resting order will be cancelled rather than crossed if it would take liquidity. Defaults to false.

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#body-subaccount)

subaccount

integer

Optional subaccount number to place the quote under (0 for primary, 1-63 for subaccounts)

#### Response

201

application/json

Quote created successfully

[​

](https://docs.kalshi.com/api-reference/communications/create-quote#response-id)

id

string

required

The ID of the newly created quote

[Get Quotes](https://docs.kalshi.com/api-reference/communications/get-quotes)[Get Quote](https://docs.kalshi.com/api-reference/communications/get-quote)
