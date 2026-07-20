---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/int64.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:09.042Z"
---
# [](https://spec.openapis.org/registry/format/int64.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/int64.html#int64---signed-64-bit-integer)int64 - signed 64-bit integer

JSON Data Type: `number, string`.

The `int64` format represents a signed 64-bit integer, with the range -9223372036854775808 through 9223372036854775807. This format entry is to ensure future versions of OpenAPI maintain compatibility with [OpenAPI 3.0.x](https://spec.openapis.org/oas/v3.0.0).

Representation as a JSON string is recommended for values outside the 53-bit range (-9007199254740991 through 9007199254740991) as this avoids problems with recipients that parse JSON numbers into [binary64](https://en.wikipedia.org/wiki/Double-precision_floating-point_format) memory representation.
