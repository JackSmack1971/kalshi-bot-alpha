---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/sf-boolean.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:09.918Z"
---
# [](https://spec.openapis.org/registry/format/sf-boolean.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/sf-boolean.html#sf-boolean---structured-fields-boolean-as-defined-in-rfc8941)sf-boolean - structured fields boolean as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-booleans)

JSON Data Type: `string`.

The `sf-boolean` format represents a structured fields boolean as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-booleans).

```abnf
sf-boolean = "?" boolean
boolean    = "0" / "1"
```

A Boolean is indicated with a leading “?” character followed by a “1” for a true value or “0” for false.

This format is appropriate for a header value that must conform to the sf-boolean structured field definition.
