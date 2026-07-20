---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-$anchor.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.009Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-$anchor.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-$anchor.html#x-jsonschema-anchor---the-json-schema-anchor-identifier-for-a-schema-resource-used-when-targeting-openapi-versions-that-do-not-directly-support-it)x-jsonschema-$anchor - The JSON Schema $anchor identifier for a schema resource, used when targeting OpenAPI versions that do not directly support it.

The `x-jsonschema-$anchor` extension mirrors the JSON Schema `$anchor` keyword by serializing it as `x-jsonschema-$anchor` when targeting OpenAPI versions where `$anchor` is not directly available.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-$anchor.html#schema)Schema

```
{"type"=>"string"}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-$anchor.html#example)Example

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
      x-jsonschema-$anchor: User
      properties:
        id:
          type: string
```
