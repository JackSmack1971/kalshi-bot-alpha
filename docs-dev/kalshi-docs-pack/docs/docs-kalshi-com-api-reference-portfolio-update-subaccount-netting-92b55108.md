---
title: "Update Subaccount Netting - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/portfolio/update-subaccount-netting"
host: "docs.kalshi.com"
depth: 4
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:17.328Z"
---
Update Subaccount Netting

cURL

```
curl --request PUT \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "subaccount_number": 123,
  "enabled": true
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting"payload = {    "subaccount_number": 123,    "enabled": True}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.put(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'PUT',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({subaccount_number: 123, enabled: true})};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "PUT",  CURLOPT_POSTFIELDS => json_encode([    'subaccount_number' => 123,    'enabled' => true  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting"	payload := strings.NewReader("{\n  \"subaccount_number\": 123,\n  \"enabled\": true\n}")	req, _ := http.NewRequest("PUT", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.put("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"subaccount_number\": 123,\n  \"enabled\": true\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Put.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"subaccount_number\": 123,\n  \"enabled\": true\n}"response = http.request(request)puts response.read_body
```

400

401

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

PUT

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

portfolio

/

subaccounts

/

netting

Try it

Update Subaccount Netting

cURL

```
curl --request PUT \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "subaccount_number": 123,
  "enabled": true
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting"payload = {    "subaccount_number": 123,    "enabled": True}headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.put(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'PUT',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({subaccount_number: 123, enabled: true})};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "PUT",  CURLOPT_POSTFIELDS => json_encode([    'subaccount_number' => 123,    'enabled' => true  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting"	payload := strings.NewReader("{\n  \"subaccount_number\": 123,\n  \"enabled\": true\n}")	req, _ := http.NewRequest("PUT", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.put("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"subaccount_number\": 123,\n  \"enabled\": true\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/subaccounts/netting")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Put.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"subaccount_number\": 123,\n  \"enabled\": true\n}"response = http.request(request)puts response.read_body
```

400

401

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

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/portfolio/update-subaccount-netting#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/portfolio/update-subaccount-netting#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/portfolio/update-subaccount-netting#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/portfolio/update-subaccount-netting#body-subaccount-number)

subaccount\_number

integer

required

Subaccount number (0 for primary, 1-63 for subaccounts).

[​

](https://docs.kalshi.com/api-reference/portfolio/update-subaccount-netting#body-enabled)

enabled

boolean

required

Whether netting is enabled for this subaccount.

#### Response

200

Netting setting updated successfully

[Get Subaccount Netting](https://docs.kalshi.com/api-reference/portfolio/get-subaccount-netting)[Get Positions](https://docs.kalshi.com/api-reference/portfolio/get-positions)
