---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/binary"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:10.933Z"
---
# [](https://spec.openapis.org/registry/media-type/binary#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/binary#binary-non-text-based-media-types)Binary: Non-text-based media types

**Media Type(s):**

• application/octet-stream ([IANA](https://www.iana.org/assignments/media-types/application/octet-stream)) – [RFC2045](https://www.rfc-editor.org/rfc/rfc2045), [RFC2046 §4.5.1](https://www.rfc-editor.org/rfc/rfc2046#section-4.5.1)
• audio/\* ([IANA](https://www.iana.org/assignments/media-types/media-types.xhtml#audio)) – [RFC2045](https://www.rfc-editor.org/rfc/rfc2045), [RFC2046 §4.2](https://www.rfc-editor.org/rfc/rfc2046#section-4.3)
• image/\* ([IANA](https://www.iana.org/assignments/media-types/media-types.xhtml#image)) – [RFC2045](https://www.rfc-editor.org/rfc/rfc2045), [RFC2046 §4.2](https://www.rfc-editor.org/rfc/rfc2046#section-4.2)
• video/\* ([IANA](https://www.iana.org/assignments/media-types/media-types.xhtml#video)) – [RFC2045](https://www.rfc-editor.org/rfc/rfc2045), [RFC2046 §4.4](https://www.rfc-editor.org/rfc/rfc2046#section-4.4)

This page also applies to any unrecognized binary media type.

**OAS References:**

• [Working with Binary Data](https://spec.openapis.org/oas/latest.html#working-with-binary-data) ([Schema Object](https://spec.openapis.org/oas/latest.html#schema-object))
• [Binary Streams](https://spec.openapis.org/oas/latest.html#binary-streams) ([Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object))
• [`Content-Transfer-Encoding` and `contentEncoding`](https://spec.openapis.org/oas/latest.html#content-transfer-encoding-and-contentencoding) ([Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object))

## [](https://spec.openapis.org/registry/media-type/binary#summary)Summary

As of OAS v3.1, binary data is modeled using an empty Schema Object, in accordance with JSON Schema’s guidance regarding [non-JSON instances](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#name-non-json-instances).

## [](https://spec.openapis.org/registry/media-type/binary#remarks)Remarks

As specified in [Working with Binary Data](https://spec.openapis.org/oas/latest.html#working-with-binary-data), modeling binary data that has been encoded into a string is handled differently from raw binary data, with two variations: with the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object)’s `contentMediaType` and `contentEncoding`, or with a `Content-Transfer-Encoding` header in the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) (for media types that use Encoding Objects). Consult the specification for how these two mechanisms interact when they both apply.

In OAS v3.0, raw binary content was modeled as `type: string, format: binary`, while `type: string, format: byte` was used for base64-encoded binary. This was dropped in favor of JSON Schema draft 2020-12’s support because it did not allow specifying the media type along with the binary encoding.
