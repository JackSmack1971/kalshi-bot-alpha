---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-dependentSchemas.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.314Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-dependentSchemas.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-dependentSchemas.html#x-jsonschema-dependentschemas---a-map-of-schemas-that-apply-when-corresponding-properties-are-present-used-when-targeting-openapi-versions-that-do-not-directly-support-dependentschemas)x-jsonschema-dependentSchemas - A map of schemas that apply when corresponding properties are present, used when targeting OpenAPI versions that do not directly support dependentSchemas.

JSON Schema 2019-09 introduced the [`dependentSchemas`](https://json-schema.org/draft/2019-09/json-schema-core#rfc.section.9.2.2.4) keyword to map property names to schemas that apply when the corresponding property is present.

The `x-jsonschema-dependentSchemas` extension mirrors this JSON Schema keyword when targeting OpenAPI versions where the keyword is not directly available, serializing it as `x-jsonschema-dependentSchemas`.

Use this extension only with JSON Schema versions before 2019-09; 2019-09 and later define `dependentSchemas` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-dependentSchemas.html#schema)Schema

```
{"type"=>"object", "additionalProperties"=>{"$ref"=>"#/$defs/schemaObject"}}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-dependentSchemas.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    Payment:
      type: object
      properties:
        creditCard:
          type: string
        billingAddress:
          type: string
      x-jsonschema-dependentSchemas:
        creditCard:
          required:
            - billingAddress
```
