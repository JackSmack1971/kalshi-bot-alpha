---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/decimal128.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:08.290Z"
---
# [](https://spec.openapis.org/registry/format/decimal128.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/decimal128.html#decimal128---a-decimal-floating-point-number-with-34-significant-decimal-digits)decimal128 - A decimal floating-point number with 34 significant decimal digits

JSON Data Type: `string, number`.

The `decimal128` format represents a [128-bit decimal floating-point number](https://en.wikipedia.org/wiki/Decimal128_floating-point_format) as defined by IEEE 754 2008 and ISO/IEC/IEEE 60559:2011.

Representation as a JSON string is preferred as this avoids problems with recipients that parse JSON numbers into [binary64](https://en.wikipedia.org/wiki/Double-precision_floating-point_format) memory representation.

String representation allows expressing the special values `NaN`, `-INF`, and `INF` that cannot be expressed as JSON numbers.
