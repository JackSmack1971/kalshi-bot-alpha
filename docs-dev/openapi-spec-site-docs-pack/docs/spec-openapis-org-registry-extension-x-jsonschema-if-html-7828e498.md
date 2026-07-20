---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-if.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.438Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-if.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-if.html#x-jsonschema-if---the-json-schema-if-conditional-subschema-used-when-targeting-openapi-versions-that-do-not-directly-support-it)x-jsonschema-if - The JSON Schema if conditional subschema, used when targeting OpenAPI versions that do not directly support it.

JSON Schema draft-07 introduced the [`if`](https://json-schema.org/draft-07/json-schema-validation#rfc.section.6.6.1) keyword to define a conditional subschema that controls whether `then` or `else` applies.

The `x-jsonschema-if` extension mirrors the JSON Schema `if` keyword when targeting OpenAPI versions where the keyword is not directly available. It is serialized as `x-jsonschema-if` so tools can preserve and process the conditional subschema.

Use this extension only with JSON Schema versions before draft-07; draft-07 and later define `if` directly.

Although OpenAPI 3.0 used JSON Schema draft-07, it [prohibited this keyword](https://spec.openapis.org/oas/v3.0.4.html#json-schema-keywords), so use this extension with OpenAPI 3.0.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-if.html#schema)Schema

```
{"$ref"=>"#/$defs/schemaObject"}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-if.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    Address:
      type: object
      properties:
        country:
          type: string
        postalCode:
          type: string
      x-jsonschema-if:
        properties:
          country:
            const: US
        required:
          - country
```
