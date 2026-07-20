---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-propertyNames.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.753Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-propertyNames.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-propertyNames.html#x-jsonschema-propertynames---a-schema-applied-to-property-names-in-an-object-used-when-targeting-openapi-versions-that-do-not-directly-support-propertynames)x-jsonschema-propertyNames - A schema applied to property names in an object, used when targeting OpenAPI versions that do not directly support propertyNames.

JSON Schema draft-06 introduced the [`propertyNames`](https://json-schema.org/draft-06/json-schema-validation#rfc.section.6.22) keyword to define a schema that applies to property names in an object.

The `x-jsonschema-propertyNames` extension mirrors this JSON Schema keyword when targeting OpenAPI versions where the keyword is not directly available, serializing it as `x-jsonschema-propertyNames`.

Use this extension only with JSON Schema versions before draft-06; draft-06 and later define `propertyNames` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-propertyNames.html#schema)Schema

```
{"$ref"=>"#/$defs/schemaObject"}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-propertyNames.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    Metadata:
      type: object
      additionalProperties:
        type: string
      x-jsonschema-propertyNames:
        pattern: "^[a-z_]+$"
```
