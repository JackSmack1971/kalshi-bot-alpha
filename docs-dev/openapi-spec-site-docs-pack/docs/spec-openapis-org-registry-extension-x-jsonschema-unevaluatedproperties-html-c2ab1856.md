---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-unevaluatedProperties.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.869Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-unevaluatedProperties.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-unevaluatedProperties.html#x-jsonschema-unevaluatedproperties---the-json-schema-unevaluatedproperties-keyword-used-when-targeting-openapi-versions-that-do-not-directly-support-it)x-jsonschema-unevaluatedProperties - The JSON Schema unevaluatedProperties keyword, used when targeting OpenAPI versions that do not directly support it.

JSON Schema 2019-09 introduced the [`unevaluatedProperties`](https://json-schema.org/draft/2019-09/json-schema-core#unevaluatedProperties) keyword to apply a schema to object properties not already evaluated by adjacent keywords.

The `x-jsonschema-unevaluatedProperties` extension mirrors the JSON Schema `unevaluatedProperties` keyword by serializing it as `x-jsonschema-unevaluatedProperties` when targeting OpenAPI versions where `unevaluatedProperties` is not directly available.

Use this extension only with JSON Schema versions before 2019-09; 2019-09 and later define `unevaluatedProperties` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-unevaluatedProperties.html#schema)Schema

```
{"oneOf"=>[{"type"=>"boolean"}, {"$ref"=>"#/$defs/schemaObject"}]}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-unevaluatedProperties.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    ExtensibleResource:
      type: object
      patternProperties:
        ^x-: true

    Invoice:
      type: object
      allOf:
        - $ref: '#/components/schemas/ExtensibleResource'
      properties:
        id:
          type: string
        total:
          type: number
          format: double
      x-jsonschema-unevaluatedProperties: false
```
