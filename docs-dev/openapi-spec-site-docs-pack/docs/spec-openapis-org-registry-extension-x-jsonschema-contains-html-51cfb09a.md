---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-contains.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.071Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-contains.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-contains.html#x-jsonschema-contains---the-json-schema-contains-subschema-for-array-elements-used-when-targeting-openapi-versions-that-do-not-directly-support-it)x-jsonschema-contains - The JSON Schema contains subschema for array elements, used when targeting OpenAPI versions that do not directly support it.

JSON Schema draft-06 introduced the [`contains`](https://json-schema.org/draft-06/json-schema-validation#rfc.section.6.14) keyword to describe a subschema that at least one array element should match.

The `x-jsonschema-contains` extension mirrors this JSON Schema keyword when targeting OpenAPI versions where the keyword is not directly available, serializing it as `x-jsonschema-contains`.

Use this extension only with JSON Schema versions before draft-06; draft-06 and later define `contains` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-contains.html#schema)Schema

```
{"$ref"=>"#/$defs/schemaObject"}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-contains.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    Roles:
      type: array
      items:
        type: string
      x-jsonschema-contains:
        const: admin
```
