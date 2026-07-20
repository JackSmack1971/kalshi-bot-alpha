---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/sequential_json"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:11.132Z"
---
# [](https://spec.openapis.org/registry/media-type/sequential_json#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/sequential_json#sequential-json-multiple-concatenated-json-documents-suitable-for-streaming)Sequential JSON: Multiple concatenated JSON documents suitable for streaming

**Media Type(s):**

• application/jsonl (not IANA-registered) – [JSON Lines](https://jsonlines.org/)
• application/json-seq ([IANA](https://www.iana.org/assignments/media-types/application/json-seq)) – [RFC7464](https://www.rfc-editor.org/rfc/rfc7464), [RFC8091](https://www.rfc-editor.org/rfc/rfc8091)
• application/x-ndjson (not IANA-registered) – [Newline Delimited JSON](https://github.com/ndjson/ndjson-spec)

**OAS References:**

• [Sequential Media Types](https://spec.openapis.org/oas/latest.html#sequential-media-types) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))
• [Streaming Sequential Media Types](https://spec.openapis.org/oas/latest.html#streaming-sequential-media-types) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))
• [Sequential JSON](https://spec.openapis.org/oas/latest.html#sequential-json) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))

## [](https://spec.openapis.org/registry/media-type/sequential_json#summary)Summary

Sequential JSON media types concatenate multiple JSON documents into one document or stream, and only vary in their choices of delimiter and the restrictions on what whitespace is allowed between JSON syntax tokens.

## [](https://spec.openapis.org/registry/media-type/sequential_json#remarks)Remarks

All sequential JSON media types support the same two approaches:

-   Use the `schema` field to model the whole document as if it were a JSON array
-   Use `itemSchema` to model one item at a time for streaming purposes, where all items use the same schema
