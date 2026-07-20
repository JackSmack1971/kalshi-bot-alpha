---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-contentMediaType.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.194Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-contentMediaType.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-contentMediaType.html#x-jsonschema-contentmediatype---the-json-schema-contentmediatype-annotation-used-when-targeting-openapi-versions-that-do-not-directly-support-it)x-jsonschema-contentMediaType - The JSON Schema contentMediaType annotation, used when targeting OpenAPI versions that do not directly support it.

JSON Schema defines the `contentMediaType` annotation to describe the media type of a string value’s decoded content.

The `x-jsonschema-contentMediaType` extension mirrors this JSON Schema keyword when targeting OpenAPI versions where the keyword is not directly available, serializing it as `x-jsonschema-contentMediaType`.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-contentMediaType.html#schema)Schema

```
{"type"=>"string"}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-contentMediaType.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    PngImage:
      type: string
      x-jsonschema-contentEncoding: base64
      x-jsonschema-contentMediaType: image/png
```
