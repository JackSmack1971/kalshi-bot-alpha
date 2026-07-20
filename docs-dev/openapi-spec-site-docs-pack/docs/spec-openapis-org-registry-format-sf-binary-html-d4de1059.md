---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/sf-binary.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:09.856Z"
---
# [](https://spec.openapis.org/registry/format/sf-binary.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/sf-binary.html#sf-binary---structured-fields-byte-sequence-as-defined-in-rfc8941)sf-binary - structured fields byte sequence as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-byte-sequences)

JSON Data Type: `string`.

The `sf-binary` format represents a structured fields byte sequence as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-byte-sequences).

```abnf
sf-binary = ":" *(base64) ":"
base64    = ALPHA / DIGIT / "+" / "/" / "="
```

A Byte Sequence is delimited with colons and encoded using base64 ([RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-4), Section 4).

This format is appropriate for a header value that must conform to the sf-binary structured field definition.
