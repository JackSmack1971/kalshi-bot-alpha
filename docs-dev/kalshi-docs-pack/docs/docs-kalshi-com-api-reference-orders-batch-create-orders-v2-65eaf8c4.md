---
title: "Batch Create Orders (V2) - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/orders/batch-create-orders-v2"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:05.662Z"
---
Batch Create Orders (V2)

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "orders": [
    {
      "ticker": "HIGHNY-24JAN01-T60",
      "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
      "side": "bid",
      "count": "10.00",
      "price": "0.5600",
      "time_in_force": "good_till_canceled",
      "self_trade_prevention_type": "taker_at_cross",
      "exchange_index": 0
    },
    {
      "ticker": "HIGHNY-24JAN01-T60",
      "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
      "side": "ask",
      "count": "5.00",
      "price": "0.5800",
      "time_in_force": "immediate_or_cancel",
      "self_trade_prevention_type": "maker",
      "exchange_index": 0
    }
  ]
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched"payload = { "orders": [        {            "ticker": "HIGHNY-24JAN01-T60",            "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",            "side": "bid",            "count": "10.00",            "price": "0.5600",            "time_in_force": "good_till_canceled",            "self_trade_prevention_type": "taker_at_cross",            "exchange_index": 0        },        {            "ticker": "HIGHNY-24JAN01-T60",            "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",            "side": "ask",            "count": "5.00",            "price": "0.5800",            "time_in_force": "immediate_or_cancel",            "self_trade_prevention_type": "maker",            "exchange_index": 0        }    ] }headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    orders: [      {        ticker: 'HIGHNY-24JAN01-T60',        client_order_id: '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',        side: 'bid',        count: '10.00',        price: '0.5600',        time_in_force: 'good_till_canceled',        self_trade_prevention_type: 'taker_at_cross',        exchange_index: 0      },      {        ticker: 'HIGHNY-24JAN01-T60',        client_order_id: '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',        side: 'ask',        count: '5.00',        price: '0.5800',        time_in_force: 'immediate_or_cancel',        self_trade_prevention_type: 'maker',        exchange_index: 0      }    ]  })};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'orders' => [        [                'ticker' => 'HIGHNY-24JAN01-T60',                'client_order_id' => '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',                'side' => 'bid',                'count' => '10.00',                'price' => '0.5600',                'time_in_force' => 'good_till_canceled',                'self_trade_prevention_type' => 'taker_at_cross',                'exchange_index' => 0        ],        [                'ticker' => 'HIGHNY-24JAN01-T60',                'client_order_id' => '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',                'side' => 'ask',                'count' => '5.00',                'price' => '0.5800',                'time_in_force' => 'immediate_or_cancel',                'self_trade_prevention_type' => 'maker',                'exchange_index' => 0        ]    ]  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched"	payload := strings.NewReader("{\n  \"orders\": [\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n      \"side\": \"bid\",\n      \"count\": \"10.00\",\n      \"price\": \"0.5600\",\n      \"time_in_force\": \"good_till_canceled\",\n      \"self_trade_prevention_type\": \"taker_at_cross\",\n      \"exchange_index\": 0\n    },\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n      \"side\": \"ask\",\n      \"count\": \"5.00\",\n      \"price\": \"0.5800\",\n      \"time_in_force\": \"immediate_or_cancel\",\n      \"self_trade_prevention_type\": \"maker\",\n      \"exchange_index\": 0\n    }\n  ]\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"orders\": [\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n      \"side\": \"bid\",\n      \"count\": \"10.00\",\n      \"price\": \"0.5600\",\n      \"time_in_force\": \"good_till_canceled\",\n      \"self_trade_prevention_type\": \"taker_at_cross\",\n      \"exchange_index\": 0\n    },\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n      \"side\": \"ask\",\n      \"count\": \"5.00\",\n      \"price\": \"0.5800\",\n      \"time_in_force\": \"immediate_or_cancel\",\n      \"self_trade_prevention_type\": \"maker\",\n      \"exchange_index\": 0\n    }\n  ]\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"orders\": [\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n      \"side\": \"bid\",\n      \"count\": \"10.00\",\n      \"price\": \"0.5600\",\n      \"time_in_force\": \"good_till_canceled\",\n      \"self_trade_prevention_type\": \"taker_at_cross\",\n      \"exchange_index\": 0\n    },\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n      \"side\": \"ask\",\n      \"count\": \"5.00\",\n      \"price\": \"0.5800\",\n      \"time_in_force\": \"immediate_or_cancel\",\n      \"self_trade_prevention_type\": \"maker\",\n      \"exchange_index\": 0\n    }\n  ]\n}"response = http.request(request)puts response.read_body
```

201

400

401

403

500

```
{
  "orders": [
    {
      "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
      "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
      "fill_count": "0.00",
      "remaining_count": "10.00",
      "ts_ms": 1715793600123
    },
    {
      "order_id": "a6d6010d-6d5f-40a1-a7e7-5501386bb621",
      "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
      "fill_count": "5.00",
      "remaining_count": "0.00",
      "average_fill_price": "0.5800",
      "average_fee_paid": "0.0012",
      "ts_ms": 1715793600456
    }
  ]
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

batched

Try it

Batch Create Orders (V2)

cURL

```
curl --request POST \
  --url https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched \
  --header 'Content-Type: application/json' \
  --header 'KALSHI-ACCESS-KEY: <api-key>' \
  --header 'KALSHI-ACCESS-SIGNATURE: <api-key>' \
  --header 'KALSHI-ACCESS-TIMESTAMP: <api-key>' \
  --data '
{
  "orders": [
    {
      "ticker": "HIGHNY-24JAN01-T60",
      "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
      "side": "bid",
      "count": "10.00",
      "price": "0.5600",
      "time_in_force": "good_till_canceled",
      "self_trade_prevention_type": "taker_at_cross",
      "exchange_index": 0
    },
    {
      "ticker": "HIGHNY-24JAN01-T60",
      "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
      "side": "ask",
      "count": "5.00",
      "price": "0.5800",
      "time_in_force": "immediate_or_cancel",
      "self_trade_prevention_type": "maker",
      "exchange_index": 0
    }
  ]
}
'
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched"payload = { "orders": [        {            "ticker": "HIGHNY-24JAN01-T60",            "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",            "side": "bid",            "count": "10.00",            "price": "0.5600",            "time_in_force": "good_till_canceled",            "self_trade_prevention_type": "taker_at_cross",            "exchange_index": 0        },        {            "ticker": "HIGHNY-24JAN01-T60",            "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",            "side": "ask",            "count": "5.00",            "price": "0.5800",            "time_in_force": "immediate_or_cancel",            "self_trade_prevention_type": "maker",            "exchange_index": 0        }    ] }headers = {    "KALSHI-ACCESS-KEY": "<api-key>",    "KALSHI-ACCESS-SIGNATURE": "<api-key>",    "KALSHI-ACCESS-TIMESTAMP": "<api-key>",    "Content-Type": "application/json"}response = requests.post(url, json=payload, headers=headers)print(response.text)
```

```
const options = {  method: 'POST',  headers: {    'KALSHI-ACCESS-KEY': '<api-key>',    'KALSHI-ACCESS-SIGNATURE': '<api-key>',    'KALSHI-ACCESS-TIMESTAMP': '<api-key>',    'Content-Type': 'application/json'  },  body: JSON.stringify({    orders: [      {        ticker: 'HIGHNY-24JAN01-T60',        client_order_id: '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',        side: 'bid',        count: '10.00',        price: '0.5600',        time_in_force: 'good_till_canceled',        self_trade_prevention_type: 'taker_at_cross',        exchange_index: 0      },      {        ticker: 'HIGHNY-24JAN01-T60',        client_order_id: '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',        side: 'ask',        count: '5.00',        price: '0.5800',        time_in_force: 'immediate_or_cancel',        self_trade_prevention_type: 'maker',        exchange_index: 0      }    ]  })};fetch('https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "POST",  CURLOPT_POSTFIELDS => json_encode([    'orders' => [        [                'ticker' => 'HIGHNY-24JAN01-T60',                'client_order_id' => '8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1',                'side' => 'bid',                'count' => '10.00',                'price' => '0.5600',                'time_in_force' => 'good_till_canceled',                'self_trade_prevention_type' => 'taker_at_cross',                'exchange_index' => 0        ],        [                'ticker' => 'HIGHNY-24JAN01-T60',                'client_order_id' => '2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a',                'side' => 'ask',                'count' => '5.00',                'price' => '0.5800',                'time_in_force' => 'immediate_or_cancel',                'self_trade_prevention_type' => 'maker',                'exchange_index' => 0        ]    ]  ]),  CURLOPT_HTTPHEADER => [    "Content-Type: application/json",    "KALSHI-ACCESS-KEY: <api-key>",    "KALSHI-ACCESS-SIGNATURE: <api-key>",    "KALSHI-ACCESS-TIMESTAMP: <api-key>"  ],]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"strings"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched"	payload := strings.NewReader("{\n  \"orders\": [\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n      \"side\": \"bid\",\n      \"count\": \"10.00\",\n      \"price\": \"0.5600\",\n      \"time_in_force\": \"good_till_canceled\",\n      \"self_trade_prevention_type\": \"taker_at_cross\",\n      \"exchange_index\": 0\n    },\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n      \"side\": \"ask\",\n      \"count\": \"5.00\",\n      \"price\": \"0.5800\",\n      \"time_in_force\": \"immediate_or_cancel\",\n      \"self_trade_prevention_type\": \"maker\",\n      \"exchange_index\": 0\n    }\n  ]\n}")	req, _ := http.NewRequest("POST", url, payload)	req.Header.Add("KALSHI-ACCESS-KEY", "<api-key>")	req.Header.Add("KALSHI-ACCESS-SIGNATURE", "<api-key>")	req.Header.Add("KALSHI-ACCESS-TIMESTAMP", "<api-key>")	req.Header.Add("Content-Type", "application/json")	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.post("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched")  .header("KALSHI-ACCESS-KEY", "<api-key>")  .header("KALSHI-ACCESS-SIGNATURE", "<api-key>")  .header("KALSHI-ACCESS-TIMESTAMP", "<api-key>")  .header("Content-Type", "application/json")  .body("{\n  \"orders\": [\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n      \"side\": \"bid\",\n      \"count\": \"10.00\",\n      \"price\": \"0.5600\",\n      \"time_in_force\": \"good_till_canceled\",\n      \"self_trade_prevention_type\": \"taker_at_cross\",\n      \"exchange_index\": 0\n    },\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n      \"side\": \"ask\",\n      \"count\": \"5.00\",\n      \"price\": \"0.5800\",\n      \"time_in_force\": \"immediate_or_cancel\",\n      \"self_trade_prevention_type\": \"maker\",\n      \"exchange_index\": 0\n    }\n  ]\n}")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/portfolio/events/orders/batched")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Post.new(url)request["KALSHI-ACCESS-KEY"] = '<api-key>'request["KALSHI-ACCESS-SIGNATURE"] = '<api-key>'request["KALSHI-ACCESS-TIMESTAMP"] = '<api-key>'request["Content-Type"] = 'application/json'request.body = "{\n  \"orders\": [\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1\",\n      \"side\": \"bid\",\n      \"count\": \"10.00\",\n      \"price\": \"0.5600\",\n      \"time_in_force\": \"good_till_canceled\",\n      \"self_trade_prevention_type\": \"taker_at_cross\",\n      \"exchange_index\": 0\n    },\n    {\n      \"ticker\": \"HIGHNY-24JAN01-T60\",\n      \"client_order_id\": \"2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a\",\n      \"side\": \"ask\",\n      \"count\": \"5.00\",\n      \"price\": \"0.5800\",\n      \"time_in_force\": \"immediate_or_cancel\",\n      \"self_trade_prevention_type\": \"maker\",\n      \"exchange_index\": 0\n    }\n  ]\n}"response = http.request(request)puts response.read_body
```

201

400

401

403

500

```
{
  "orders": [
    {
      "order_id": "3b23c1c7-f4ef-4f0d-8b9a-9e53c61f1a0d",
      "client_order_id": "8c35ecb3-328f-4f52-8c7c-0f4b9862f8d1",
      "fill_count": "0.00",
      "remaining_count": "10.00",
      "ts_ms": 1715793600123
    },
    {
      "order_id": "a6d6010d-6d5f-40a1-a7e7-5501386bb621",
      "client_order_id": "2a0e3fc9-b593-4aa3-96e5-82f7f7566c2a",
      "fill_count": "5.00",
      "remaining_count": "0.00",
      "average_fill_price": "0.5800",
      "average_fee_paid": "0.0012",
      "ts_ms": 1715793600456
    }
  ]
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

**Rate limit:** 10 tokens per order in the batch — billed per item, so total cost for a batch of N orders is N × 10. See `GET /trade-api/v2/account/endpoint_costs` for current non-default endpoint costs.

#### Authorizations

[​

](https://docs.kalshi.com/api-reference/orders/batch-create-orders-v2#authorization-kalshi-access-key)

KALSHI-ACCESS-KEY

string

header

required

Your API key ID

[​

](https://docs.kalshi.com/api-reference/orders/batch-create-orders-v2#authorization-kalshi-access-signature)

KALSHI-ACCESS-SIGNATURE

string

header

required

RSA-PSS signature of the request

[​

](https://docs.kalshi.com/api-reference/orders/batch-create-orders-v2#authorization-kalshi-access-timestamp)

KALSHI-ACCESS-TIMESTAMP

string

header

required

Request timestamp in milliseconds

#### Body

application/json

[​

](https://docs.kalshi.com/api-reference/orders/batch-create-orders-v2#body-orders)

orders

object\[\]

required

Show child attributes

#### Response

201

application/json

Batch order creation completed

[​

](https://docs.kalshi.com/api-reference/orders/batch-create-orders-v2#response-orders)

orders

object\[\]

required

Show child attributes

[Create Order (V2)](https://docs.kalshi.com/api-reference/orders/create-order-v2)[Batch Cancel Orders (V2)](https://docs.kalshi.com/api-reference/orders/batch-cancel-orders-v2)
