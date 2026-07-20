---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-contentSchema.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.257Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-contentSchema.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-contentSchema.html#x-jsonschema-contentschema---the-json-schema-contentschema-subschema-for-decoded-string-content-used-when-targeting-openapi-versions-that-do-not-directly-support-it)x-jsonschema-contentSchema - The JSON Schema contentSchema subschema for decoded string content, used when targeting OpenAPI versions that do not directly support it.

JSON Schema 2019-09 introduced the [`contentSchema`](https://json-schema.org/draft/2019-09/json-schema-validation#rfc.section.8.5) annotation to describe the schema for decoded string content.

The `x-jsonschema-contentSchema` extension mirrors this JSON Schema keyword when targeting OpenAPI versions where the keyword is not directly available, serializing it as `x-jsonschema-contentSchema`.

Use this extension only with JSON Schema versions before 2019-09; 2019-09 and later define `contentSchema` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-contentSchema.html#schema)Schema

```
{"$ref"=>"#/$defs/schemaObject"}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-contentSchema.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    EncodedPayload:
      type: string
      x-jsonschema-contentEncoding: base64
      x-jsonschema-contentMediaType: application/json
      x-jsonschema-contentSchema:
        type: object
        required:
          - id
        properties:
          id:
            type: string
```
