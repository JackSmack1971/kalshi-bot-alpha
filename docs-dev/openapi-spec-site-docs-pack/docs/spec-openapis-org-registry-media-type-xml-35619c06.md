---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/xml"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:11.444Z"
---
# [](https://spec.openapis.org/registry/media-type/xml#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/xml#xml-extensible-markup-language)XML: Extensible markup language

**Media Type(s):**

• application/xml ([IANA](https://www.iana.org/assignments/media-types/application/xml)) – [RFC7303](https://www.rfc-editor.org/rfc/rfc7303), [XML 1.0](https://www.w3.org/TR/xml/) (commonly used), [XML 1.1](https://www.w3.org/TR/xml11/) (rarely used), [WHATWG DOM](https://dom.spec.whatwg.org/)

**OAS References:**

• [XML Object](https://spec.openapis.org/oas/latest.html#xml-object)
• [XML Modeling](https://spec.openapis.org/oas/latest.html#xml-modeling) ([Schema Object](https://spec.openapis.org/oas/latest.html#schema-object))

## [](https://spec.openapis.org/registry/media-type/xml#summary)Summary

XML is modeled using the OAS’s `xml` extension keyword for JSON Schema, which has an XML Object as its value.

## [](https://spec.openapis.org/registry/media-type/xml#remarks)Remarks

As of OAS v3.2, the [XML Object](https://spec.openapis.org/oas/latest.html#xml-object) uses the `nodeType` field to determine the type of [interface node](https://dom.spec.whatwg.org/#interface-node) to which a given Schema Object corresponds: `element`, `attribute`, `text`, `cdata`, or `none`. If `nodeType` is set to `none`, a Schema Object does not correspond to anything and the nodes corresponding to its immediate subschemas are placed directly under the node of its parent schema.

Certain behaviors are retained for compatibility with OAS v3.1, including implicit text nodes for elements with a primitive type, and somewhat complex rules for the default value of `nodeType`. In OAS v3.1 and earlier, only elements, their implicit primitive-type text nodes, and attributes were supported, with the now-deprecated `attribute` and `wrapped` flags as controls.
