---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-$self.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:06.943Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-$self.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-$self.html#x-oai-self---the-canonical-absolute-uri-for-an-openapi-document-used-when-targeting-openapi-versions-prior-to-32)x-oai-$self - The canonical absolute URI for an OpenAPI document, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the [`$self`](https://spec.openapis.org/oas/v3.2.0.html#oas-self) field on OpenAPI Objects to identify the canonical absolute URI for an OpenAPI document.

The `x-oai-$self` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to identify the canonical absolute URI for an OpenAPI document.

Use this extension only with OpenAPI versions before 3.2; OpenAPI 3.2 and later define `$self` directly.

It can appear as a property in the following objects: `["OpenAPI Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-$self.html#schema)Schema

```
{"type"=>"string", "format"=>"uri"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-$self.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
x-oai-$self: https://example.org/api/openapi.json
paths: {}
```
