---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-serializedValue.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.611Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-serializedValue.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-serializedValue.html#x-oai-serializedvalue---a-serialized-example-value-for-an-example-object-used-when-targeting-openapi-versions-prior-to-32)x-oai-serializedValue - A serialized example value for an Example Object, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the [`serializedValue`](https://spec.openapis.org/oas/v3.2.0.html#example-serialized-value) field on Example Objects to provide already-serialized example data.

The `x-oai-serializedValue` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to provide already-serialized example data on an Example Object.

Use this extension only with OpenAPI versions before 3.2; OpenAPI 3.2 and later define `serializedValue` directly.

It can appear as a property in the following objects: `["Example Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-serializedValue.html#schema)Schema

```
{"type"=>"string"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-serializedValue.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  examples:
    csvExample:
      summary: A CSV example
      x-oai-serializedValue: "id,name\n1,Ada"
```
