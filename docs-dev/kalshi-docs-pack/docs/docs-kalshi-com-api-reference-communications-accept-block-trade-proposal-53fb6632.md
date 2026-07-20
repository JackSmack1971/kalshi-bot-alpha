---
title: "Accept Block Trade Proposal - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:20.566Z"
---
Accept Block Trade Proposal

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "subtrader_id": "<string>",
  "subaccount": 31
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept"payload = {    "subtrader_id": "<string>",    "subaccount": 31}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({subtrader_id: '<string>', subaccount: 31})};fetch('https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'subtrader_id' => '<string>',    'subaccount' => 31  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept"	payload := strings.NewReader("{\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 31\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 31\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 31\n}"response = http.request(request)puts response.read_body
```

400

401

404

500

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
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

block-trade-proposals

/

{block\_trade\_proposal\_id}

/

accept

Try it

Accept Block Trade Proposal

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "subtrader_id": "<string>",
  "subaccount": 31
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept"payload = {    "subtrader_id": "<string>",    "subaccount": 31}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({subtrader_id: '<string>', subaccount: 31})};fetch('https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'subtrader_id' => '<string>',    'subaccount' => 31  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept"	payload := strings.NewReader("{\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 31\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 31\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/communications/block-trade-proposals/{block_trade_proposal_id}/accept")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"subtrader_id\": \"<string>\",\n  \"subaccount\": 31\n}"response = http.request(request)puts response.read_body
```

400

401

404

500

```
{
  "code": "<string>",
  "message": "<string>",
  "details": "<string>",
  "service": "<string>"
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

](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Path Parameters

[​

](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal#parameter-block-trade-proposal-id)

block\_trade\_proposal\_id

string

required

Block trade proposal ID

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal#body-subtrader-id)

subtrader\_id

string

Subtrader ID to accept as. Provide either this or subaccount, not both.

[​

](https://docs.kalshi.com/api-reference/communications/accept-block-trade-proposal#body-subaccount)

subaccount

integer

User-managed subaccount number to accept as (0 for primary, 1-63 for numbered subaccounts). Provide either this or subtrader\_id, not both.

Required range: `0 <= x <= 63`

#### Response

204

Block trade proposal accepted successfully

[Propose Block Trade](https://docs.kalshi.com/api-reference/communications/propose-block-trade)[Get RFQs](https://docs.kalshi.com/api-reference/communications/get-rfqs)
