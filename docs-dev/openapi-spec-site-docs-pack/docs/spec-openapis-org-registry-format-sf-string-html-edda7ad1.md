---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/sf-string.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:10.100Z"
---
# [](https://spec.openapis.org/registry/format/sf-string.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/sf-string.html#sf-string---structured-fields-string-as-defined-in-rfc8941)sf-string - structured fields string as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-strings)

JSON Data Type: `string`.

The `sf-string` format represents a structured fields string as defined in [RFC8941](https://www.rfc-editor.org/rfc/rfc8941#name-strings).

```abnf
sf-string = DQUOTE *chr DQUOTE
chr       = unescaped / escaped
unescaped = %x20-21 / %x23-5B / %x5D-7E
escaped   = "\" ( DQUOTE / "\" )
```

Strings are zero or more printable ASCII \[RFC0020\] characters (i.e., the range %x20 to %x7E). Note that this excludes tabs, newlines, carriage returns, etc.

Strings are delimited with double quotes, using a backslash (“") to escape double quotes and backslashes.

This format is appropriate for a header value that must conform to the sf-string structured field definition.
