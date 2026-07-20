---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/sf-token.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:10.166Z"
---
# [](https://spec.openapis.org/registry/format/sf-token.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/sf-token.html#sf-token---structured-fields-token-as-defined-in-rfc8941)sf-token - structured fields token as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-tokens)

JSON Data Type: `string`.

The `sf-token` format represents a structured fields token as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-tokens).

```abnf
sf-token = ( ALPHA / "*" ) *( tchar / ":" / "/" )
```

Tokens are short textual words; their abstract model is identical to their expression in the HTTP field value serialization.

This format is appropriate for a header value that must conform to the sf-token structured field definition.
