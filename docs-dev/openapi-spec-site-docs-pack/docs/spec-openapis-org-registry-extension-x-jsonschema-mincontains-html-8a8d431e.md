---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-jsonschema-minContains.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.638Z"
---
# [](https://spec.openapis.org/registry/extension/x-jsonschema-minContains.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-jsonschema-minContains.html#x-jsonschema-mincontains---the-minimum-number-of-array-elements-that-must-match-contains-used-when-targeting-openapi-versions-that-do-not-directly-support-mincontains)x-jsonschema-minContains - The minimum number of array elements that must match contains, used when targeting OpenAPI versions that do not directly support minContains.

JSON Schema 2019-09 introduced the [`minContains`](https://json-schema.org/draft/2019-09/json-schema-validation#rfc.section.6.4.5) keyword to set the minimum number of array elements that must match `contains`.

The `x-jsonschema-minContains` extension mirrors this JSON Schema keyword when targeting OpenAPI versions where the keyword is not directly available, serializing it as `x-jsonschema-minContains`.

Use this extension only with JSON Schema versions before 2019-09; 2019-09 and later define `minContains` directly.

It can appear as a property in the following objects: `["Schema Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-jsonschema-minContains.html#schema)Schema

```
{"type"=>"integer", "minimum"=>0}
```

### [](https://spec.openapis.org/registry/extension/x-jsonschema-minContains.html#example)Example

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
      x-jsonschema-minContains: 1
```
