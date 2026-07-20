---
title: "Targets & Milestones - API Documentation"
source_url: "https://docs.kalshi.com/getting_started/targets_and_milestones"
host: "docs.kalshi.com"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T16:49:56.298Z"
---
Kalshi exposes two related metadata objects that are useful when working with event and market data:

-   `milestones` describe a real-world occurrence tied to one or more events
-   `structured_targets` describe a real-world entity that a milestone or market can reference

If you need to group related events, start with milestones. If you need to identify a team, player, or other entity referenced by a market, use structured targets.

##

[​

](https://docs.kalshi.com/getting_started/targets_and_milestones#milestones)

Milestones

A milestone links Kalshi events to a real-world occurrence. Useful fields on a milestone include:

-   `id`, `type`, `title`, `start_date`, `end_date`
-   `primary_event_tickers` for the milestone’s core markets
-   `related_event_tickers` for the broader set of events tied to the same occurrence
-   `details` for type-specific metadata
-   `source_id` and `source_ids` when external identifiers are available

`details` is flexible JSON and varies by milestone type. For sports milestones, it commonly contains structured target IDs such as `home_team_id` or `away_team_id`. In practice, `related_event_tickers` is often a superset of `primary_event_tickers`. For example, a recent `Wyoming General Elections` `one_off_milestone` in Redshift had:

-   `primary_event_tickers`: `SENATEWY-26`
-   `related_event_tickers`: `SENATEWY-26`, `GOVPARTYWY-26`, and `KXHOUSERACE-WYAL-26`

Those are event tickers, not display titles. In this case they point to the Wyoming Senate, Wyoming Governor, and Wyoming at-large House race events. That broader grouping is useful when you want all of the markets tied to one real-world occurrence. For milestone types that expose live updates, the same milestone ID is also the key used by the live data API.

###

[​

](https://docs.kalshi.com/getting_started/targets_and_milestones#fetch-milestones)

Fetch milestones

Use the [Get Milestone](https://docs.kalshi.com/api-reference/milestone/get-milestone) and [Get Milestones](https://docs.kalshi.com/api-reference/milestone/get-milestones) endpoint docs for the supported parameters and response shape. If you want milestones returned alongside events, use [Get Events](https://docs.kalshi.com/api-reference/events/get-events) with `with_milestones=true`. The events response includes a top-level `milestones` array alongside `events`.

###

[​

](https://docs.kalshi.com/getting_started/targets_and_milestones#use-milestones-to-group-events)

Use milestones to group events

A milestone is often the easiest way to find other events tied to the same occurrence. Query by `related_event_ticker`, then read `related_event_tickers` or `primary_event_tickers` from the returned milestone. Once you have the right milestone, use [Get Live Data](https://docs.kalshi.com/api-reference/live-data/get-live-data) when that milestone type supports live updates.

##

[​

](https://docs.kalshi.com/getting_started/targets_and_milestones#structured-targets)

Structured Targets

A structured target identifies a real-world entity that can be referenced elsewhere in the API. Useful fields on a structured target include:

-   `id`, `name`, `type`
-   `details` for type-specific metadata
-   `source_id` and `source_ids` when external identifiers are available

Like milestone `details`, structured target `details` is flexible JSON and depends on the target type.

###

[​

](https://docs.kalshi.com/getting_started/targets_and_milestones#fetch-structured-targets)

Fetch structured targets

Use the [Get Structured Target](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target) and [Get Structured Targets](https://docs.kalshi.com/api-reference/structured-targets/get-structured-targets) endpoint docs for the supported parameters and response shape. `type` values are not a short fixed list. Integrations should filter by the values they need rather than hardcoding a small allowlist.

##

[​

](https://docs.kalshi.com/getting_started/targets_and_milestones#how-they-connect-to-markets)

How They Connect To Markets

Markets can reference structured targets through `custom_strike`.

```
{
  "strike_type": "structured",
  "custom_strike": {
    "basketball_team": "2ef4d31c-0b46-4f43-a403-f44d62489034"
  }
}
```

For `strike_type: "structured"`, the value inside `custom_strike` is a structured target ID. You can resolve it with the [Get Structured Target](https://docs.kalshi.com/api-reference/structured-targets/get-structured-target) endpoint. For numeric strike types, use `floor_strike` and `cap_strike` instead of `custom_strike`.

[Historical Data](https://docs.kalshi.com/getting_started/historical_data)[Market Lifecycle](https://docs.kalshi.com/getting_started/market_lifecycle)
