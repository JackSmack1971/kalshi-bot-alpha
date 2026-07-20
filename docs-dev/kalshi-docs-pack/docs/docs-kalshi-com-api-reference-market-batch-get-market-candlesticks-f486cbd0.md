---
title: "Batch Get Market Candlesticks - API Documentation"
source_url: "https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks"
host: "docs.kalshi.com"
depth: 3
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:50:13.838Z"
---
Batch Get Market Candlesticks

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/markets/candlesticks
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/markets/candlesticks"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/markets/candlesticks', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/markets/candlesticks",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/markets/candlesticks"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/markets/candlesticks")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/markets/candlesticks")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "markets": [
    {
      "market_ticker": "<string>",
      "candlesticks": [
        {
          "end_period_ts": 123,
          "yes_bid": {
            "open_dollars": "0.5600",
            "low_dollars": "0.5600",
            "high_dollars": "0.5600",
            "close_dollars": "0.5600"
          },
          "yes_ask": {
            "open_dollars": "0.5600",
            "low_dollars": "0.5600",
            "high_dollars": "0.5600",
            "close_dollars": "0.5600"
          },
          "price": {
            "open_dollars": "0.5600",
            "low_dollars": "0.5600",
            "high_dollars": "0.5600",
            "close_dollars": "0.5600",
            "mean_dollars": "0.5600",
            "previous_dollars": "0.5600",
            "min_dollars": "0.5600",
            "max_dollars": "0.5600"
          },
          "volume_fp": "10.00",
          "open_interest_fp": "10.00"
        }
      ]
    }
  ]
}
```

GET

https://external-api.kalshi.com/trade-api/v2https://api.elections.kalshi.com/trade-api/v2https://external-api.demo.kalshi.co/trade-api/v2https://demo-api.kalshi.co/trade-api/v2

/

markets

/

candlesticks

Try it

Batch Get Market Candlesticks

cURL

```
curl --request GET \
  --url https://external-api.kalshi.com/trade-api/v2/markets/candlesticks
```

```
import requestsurl = "https://external-api.kalshi.com/trade-api/v2/markets/candlesticks"response = requests.get(url)print(response.text)
```

```
const options = {method: 'GET'};fetch('https://external-api.kalshi.com/trade-api/v2/markets/candlesticks', options)  .then(res => res.json())  .then(res => console.log(res))  .catch(err => console.error(err));
```

```
<?php$curl = curl_init();curl_setopt_array($curl, [  CURLOPT_URL => "https://external-api.kalshi.com/trade-api/v2/markets/candlesticks",  CURLOPT_RETURNTRANSFER => true,  CURLOPT_ENCODING => "",  CURLOPT_MAXREDIRS => 10,  CURLOPT_TIMEOUT => 30,  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,  CURLOPT_CUSTOMREQUEST => "GET",]);$response = curl_exec($curl);$err = curl_error($curl);curl_close($curl);if ($err) {  echo "cURL Error #:" . $err;} else {  echo $response;}
```

```
package mainimport (	"fmt"	"net/http"	"io")func main() {	url := "https://external-api.kalshi.com/trade-api/v2/markets/candlesticks"	req, _ := http.NewRequest("GET", url, nil)	res, _ := http.DefaultClient.Do(req)	defer res.Body.Close()	body, _ := io.ReadAll(res.Body)	fmt.Println(string(body))}
```

```
HttpResponse<String> response = Unirest.get("https://external-api.kalshi.com/trade-api/v2/markets/candlesticks")  .asString();
```

```
require 'uri'require 'net/http'url = URI("https://external-api.kalshi.com/trade-api/v2/markets/candlesticks")http = Net::HTTP.new(url.host, url.port)http.use_ssl = truerequest = Net::HTTP::Get.new(url)response = http.request(request)puts response.read_body
```

200

```
{
  "markets": [
    {
      "market_ticker": "<string>",
      "candlesticks": [
        {
          "end_period_ts": 123,
          "yes_bid": {
            "open_dollars": "0.5600",
            "low_dollars": "0.5600",
            "high_dollars": "0.5600",
            "close_dollars": "0.5600"
          },
          "yes_ask": {
            "open_dollars": "0.5600",
            "low_dollars": "0.5600",
            "high_dollars": "0.5600",
            "close_dollars": "0.5600"
          },
          "price": {
            "open_dollars": "0.5600",
            "low_dollars": "0.5600",
            "high_dollars": "0.5600",
            "close_dollars": "0.5600",
            "mean_dollars": "0.5600",
            "previous_dollars": "0.5600",
            "min_dollars": "0.5600",
            "max_dollars": "0.5600"
          },
          "volume_fp": "10.00",
          "open_interest_fp": "10.00"
        }
      ]
    }
  ]
}
```

#### Query Parameters

[​

](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks#parameter-market-tickers)

market\_tickers

string

required

Comma-separated list of market tickers (maximum 100)

[​

](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks#parameter-start-ts)

start\_ts

integer<int64>

required

Start timestamp in Unix seconds

[​

](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks#parameter-end-ts)

end\_ts

integer<int64>

required

End timestamp in Unix seconds

[​

](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks#parameter-period-interval)

period\_interval

integer<int32>

required

Candlestick period interval in minutes

Required range: `x >= 1`

[​

](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks#parameter-include-latest-before-start)

include\_latest\_before\_start

boolean

default:false

If true, prepends the latest candlestick available before the start\_ts. This synthetic candlestick is created by:

1.  Finding the most recent real candlestick before start\_ts
2.  Projecting it forward to the first period boundary (calculated as the next period interval after start\_ts)
3.  Setting all OHLC prices to null, and `previous_price` to the close price from the real candlestick

#### Response

200

application/json

Market candlesticks retrieved successfully

[​

](https://docs.kalshi.com/api-reference/market/batch-get-market-candlesticks#response-markets)

markets

object\[\]

required

Array of market candlestick data, one entry per requested market.

Show child attributes

[Get Market](https://docs.kalshi.com/api-reference/market/get-market)[Get Event Candlesticks](https://docs.kalshi.com/api-reference/events/get-event-candlesticks)
