---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/sf-decimal.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:09.983Z"
---
# [](https://spec.openapis.org/registry/format/sf-decimal.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/sf-decimal.html#sf-decimal---structured-fields-decimal-as-defined-in-rfc8941)sf-decimal - structured fields decimal as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-decimals)

JSON Data Type: `number`.

The `sf-decimal` format represents a structured fields decimal as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-decimals).

```abnf
sf-decimal  = ["-"] 1*12DIGIT "." 1*3DIGIT
```

Decimals are numbers with an integer and a fractional component. The integer component has at most 12 digits; the fractional component has at most three digits.

This format is appropriate for a header value that must conform to the sf-decimal structured field definition.
