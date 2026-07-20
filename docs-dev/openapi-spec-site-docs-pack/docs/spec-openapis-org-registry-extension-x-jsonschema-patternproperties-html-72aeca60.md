---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-patternProperties.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.696Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-patternProperties.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-patternProperties.html#x-jsonschema-patternproperties---a-map-of-regular-expressions-to-schemas-for-matching-property-names-used-when-targeting-openapi-versions-that-do-not-directly-support-patternproperties)x-jsonschema-patternProperties - A map of regular expressions to schemas for matching property names, used when targeting OpenAPI versions that do not directly support patternProperties.

JSON Schema draft-03 introduced the [`patternProperties`](https://json-schema.org/draft-03/draft-zyp-json-schema-03.pdf#page=8) keyword to map regular expressions to schemas for matching property names.

The `x-jsonschema-patternProperties` extension mirrors the JSON Schema `patternProperties` keyword by serializing it as `x-jsonschema-patternProperties` when targeting OpenAPI versions where `patternProperties` is not directly available.

Use this extension only with JSON Schema versions before draft-03; draft-03 and later define `patternProperties` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-patternProperties.html#schema)Schema

```
{"type"=>"object", "additionalProperties"=>{"$ref"=>"#/$defs/schemaObject"}}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-patternProperties.html#example)Example

```
openapi: 3.0.4
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  schemas:
    User:
      type: object
      x-jsonschema-patternProperties:
        "^S_":
          type: string
```
