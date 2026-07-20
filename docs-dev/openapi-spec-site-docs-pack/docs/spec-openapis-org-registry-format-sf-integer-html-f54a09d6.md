---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/sf-integer.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:10.041Z"
---
# [](https://spec.openapis.org/registry/format/sf-integer.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/sf-integer.html#sf-integer---structured-fields-integer-as-defined-in-rfc8941)sf-integer - structured fields integer as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-integers)

JSON Data Type: `number`.

The `sf-integer` format represents a structured fields integer as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-integers).

```abnf
sf-integer = ["-"] 1*15DIGIT
```

Integers have a range of -999,999,999,999,999 to 999,999,999,999,999 inclusive (i.e., up to fifteen digits, signed), for IEEE 754 compatibility [IEEE754](https://ieeexplore.ieee.org/document/8766229).

This format is appropriate for a header value that must conform to the sf-integer structured field definition.
