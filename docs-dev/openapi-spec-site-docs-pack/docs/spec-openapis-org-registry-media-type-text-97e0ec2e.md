---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/text"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:11.322Z"
---
# [](https://spec.openapis.org/registry/media-type/text#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/text#text-text-based-media-types)Text: Text-based media types

**Media Type(s):**

• text/\* ([IANA](https://www.iana.org/assignments/media-types/media-types.xhtml#text)) – [RFC2045](https://www.rfc-editor.org/rfc/rfc2045), [RFC2046 §4.1](https://www.rfc-editor.org/rfc/rfc2046#section-4.1)
• text/plain ([IANA](https://www.iana.org/assignments/media-types/text/plain)) – [RFC2046 §4.1.3](https://www.rfc-editor.org/rfc/rfc2046#section-4.1.3), [RFC3676](https://www.rfc-editor.org/rfc/rfc3676)

This page also applies to any unrecognized text-based (not just text/\*) media type.

**OAS References:**

• [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object)
• [Header Object](https://spec.openapis.org/oas/latest.html#header-object)
• [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)

## [](https://spec.openapis.org/registry/media-type/text#summary)Summary

A plain text document is modeled as a single string.

## [](https://spec.openapis.org/registry/media-type/text#remarks)Remarks

Note that unlike JSON strings, the contents of the string representing the plain text are not quoted when serializing to a document. While a Schema Object of `{type: string, const: foo}` for JSON validates the JSON value `"foo"`, for plain text it validates `foo`, without quotes.
