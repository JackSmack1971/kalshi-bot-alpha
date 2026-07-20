---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/sse"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:11.252Z"
---
# [](https://spec.openapis.org/registry/media-type/sse#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/sse#server-sent-events-event-streams-for-sse)Server-Sent Events: Event streams for SSE

**Media Type(s):**

• text/event-stream (not IANA-registered) – [WHATWG HTML §Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#parsing-an-event-stream), [WHATWG HTML §IANA](https://html.spec.whatwg.org/multipage/iana.html#text/event-stream)

**OAS References:**

• [Sequential Media Types](https://spec.openapis.org/oas/latest.html#sequential-media-types) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))
• [Special Considerations for Server-Sent Events](https://spec.openapis.org/oas/latest.html#special-considerations-for-server-sent-events) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))
• [Server-Sent Event Stream (Examples)](https://spec.openapis.org/oas/latest.html#server-sent-event-streams) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))

## [](https://spec.openapis.org/registry/media-type/sse#summary)Summary

Server-Sent Events use the `text/event-stream` media type to stream events. Each event is modeled as if it were a JSON object with fields and types as given in the SSE specification, ignoring comments (fields with an empty string for the name) and any variations in serialization that represent the same event content.

## [](https://spec.openapis.org/registry/media-type/sse#remarks)Remarks

A complete event stream can be modeled as if it were a JSON array of such objects in the `schema` field, but the more common use case is to use the `itemSchema` field to apply the same schema to each event as it is streamed.

Note that application-level conventions regarding event usage (e.g. “sentinel events”) that are not part of the media type specification are not modeled, as the OAS does not currently (as of OAS v3.2) work with semantics above the media type level.
