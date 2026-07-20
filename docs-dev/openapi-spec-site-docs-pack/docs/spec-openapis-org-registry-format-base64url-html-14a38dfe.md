---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/base64url.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.779Z"
---
# [](https://spec.openapis.org/registry/format/base64url.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/base64url.html#base64url---binary-data-encoded-as-a-url-safe-string-as-defined-in-rfc4648)base64url - Binary data encoded as a url-safe string as defined in [RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-5)

JSON Data Type: `string`.

The `base64url` format is binary data encoded as a url-safe string as defined in [RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-5).

### [](https://spec.openapis.org/registry/format/base64url.html#remarks)Remarks

When using OpenAPI 3.1 it’s recommended not to use this format and instead use [`contentEncoding` with a value of `base64url`](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-contentencoding).
