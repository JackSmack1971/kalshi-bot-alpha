---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-dataValue.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.067Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-dataValue.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-dataValue.html#x-oai-datavalue---a-structured-example-value-for-an-example-object-used-when-targeting-openapi-versions-prior-to-32)x-oai-dataValue - A structured example value for an Example Object, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the [`dataValue`](https://spec.openapis.org/oas/v3.2.0.html#example-data-value) field on Example Objects to provide structured example data as any JSON value.

The `x-oai-dataValue` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to provide structured example data on an Example Object.

Use this extension only with OpenAPI versions before 3.2; OpenAPI 3.2 and later define `dataValue` directly.

It can appear as a property in the following objects: `["Example Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-dataValue.html#schema)Schema

```
{}
```

### [](https://spec.openapis.org/registry/extension/x-oai-dataValue.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  examples:
    userExample:
      summary: A user example
      x-oai-dataValue:
        id: 123
        name: Ada
```
