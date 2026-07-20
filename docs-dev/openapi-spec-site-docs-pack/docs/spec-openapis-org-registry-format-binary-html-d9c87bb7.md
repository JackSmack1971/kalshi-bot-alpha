---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/binary.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.834Z"
---
# [](https://spec.openapis.org/registry/format/binary.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/binary.html#binary---any-sequence-of-octets)binary - any sequence of octets

JSON Data Type: `string`.

The `binary` format represents any sequence of octets. This format entry is to ensure future versions of OpenAPI maintain compatibility with [OpenAPI 3.0.x](https://spec.openapis.org/oas/v3.0.0).

### [](https://spec.openapis.org/registry/format/binary.html#remarks)Remarks

In OpenAPI 3.1, instead set the media type appropriately and do not use a schema property. Note that only complete HTTP message bodies or complete parts in a multipart media type can accommodate binary data. JSON strings and URL path components cannot.
