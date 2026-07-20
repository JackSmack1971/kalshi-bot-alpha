---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:12.078Z"
---
# [](https://spec.openapis.org/registry/media-type/#media-type-registry)Media Type Registry

This registry lists the non-JSON media types addressed by the OpenAPI Specification (OAS), and links to the appropriate OAS sections and external specifications. See [Parsing and Serializing](https://spec.openapis.org/oas/latest.html#parsing-and-serializing) for a discussion of serialized, schema-ready, and application forms of data, and how to convert among the forms.

## [](https://spec.openapis.org/registry/media-type/#specification-versions)Specification Versions

This registry is for and [linked from](https://spec.openapis.org/oas/latest.html#media-types) version 3.2 and later of the OAS. Earlier versions and other specifications such as Arazzo MAY support approaches added in this registry, as long as the necessary Objects and fields are available in those versions.

## [](https://spec.openapis.org/registry/media-type/#contributing)Contributing

Please open a [discussion](https://github.com/OAI/OpenAPI-Specification/discussions) explaining your ***use cases*** for any media type(s) you would like to see added.

## [](https://spec.openapis.org/registry/media-type/#media-types)Media Types

**Note:** Media types with a structured suffix are handled the same way as the media type corresponding to the suffix (e.g. all `+json` media types are handled as `application/json`).

| Group | Description | Media Types |
| --- | --- | --- |
| [Binary](https://spec.openapis.org/registry/media-type/binary) | Non-text-based media types | application/octet-stream
audio/\*
image/\*
video/\*
any unrecognized binary media type |
| [Forms](https://spec.openapis.org/registry/media-type/forms) | Ordered name-value pairs | application/x-www-form-urlencoded
multipart/form-data |
| [Link Sets](https://spec.openapis.org/registry/media-type/linksets) | Sets of RFC8288 Web Links | application/linkset
application/linkset+json |
| [Sequential JSON](https://spec.openapis.org/registry/media-type/sequential_json) | Multiple concatenated JSON documents suitable for streaming | application/jsonl
application/json-seq
application/x-ndjson |
| [Sequential Multipart](https://spec.openapis.org/registry/media-type/sequential_multipart) | Multipart subtypes with unnamed parts | multipart/\*
multipart/mixed
multipart/alternative
multipart/related
multipart/byteranges |
| [Server-Sent Events](https://spec.openapis.org/registry/media-type/sse) | Event streams for SSE | text/event-stream |
| [Text](https://spec.openapis.org/registry/media-type/text) | Text-based media types | text/\*
text/plain
any unrecognized text-based (not just text/\*) media type |
| [Token-Oriented Object Notation (TOON)](https://spec.openapis.org/registry/media-type/toon) | Compact encoding of the JSON data model for LLM prompts | text/toon |
| [XML](https://spec.openapis.org/registry/media-type/xml) | Extensible markup language | application/xml |
