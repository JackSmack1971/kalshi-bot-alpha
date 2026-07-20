---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/uint64.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:10.498Z"
---
# [](https://spec.openapis.org/registry/format/uint64.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/uint64.html#uint64---unsigned-64-bit-integer)uint64 - unsigned 64-bit integer

JSON Data Type: `number, string`.

The `uint64` format represents an unsigned 64-bit integer, with the range 0 to 18446744073709551615.

Representation as a JSON string is recommended for values outside the 53-bit range (0 through 9007199254740991) as this avoids problems with recipients that parse JSON numbers into [binary64](https://en.wikipedia.org/wiki/Double-precision_floating-point_format) memory representation.

### [](https://spec.openapis.org/registry/format/uint64.html#github-issue)GitHub Issue

-   [#4564](https://github.com/OAI/OpenAPI-Specification/issues/4564)
