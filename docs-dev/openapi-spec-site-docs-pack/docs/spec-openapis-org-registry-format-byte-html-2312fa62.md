---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/byte.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.888Z"
---
# [](https://spec.openapis.org/registry/format/byte.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/byte.html#byte---base64-encoded-data-as-defined-in-rfc4648)byte - base64 encoded data as defined in [RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-4)

JSON Data Type: `string`.

The `byte` format represents any sequence of octets encoded as a base64 string as defined in [RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-4). This format entry is to ensure future versions of OpenAPI maintain compatibility with [OpenAPI 3.0.x](https://spec.openapis.org/oas/v3.0.0).

### [](https://spec.openapis.org/registry/format/byte.html#remarks)Remarks

In OpenAPI 3.1, instead use [`contentEncoding: base64`](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-contentencoding), optionally alongside [contentMediaType](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-contentmediatype).
