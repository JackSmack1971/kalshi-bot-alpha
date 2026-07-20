---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-name.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.496Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-name.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-name.html#x-oai-name---an-identifier-for-a-server-object-used-when-targeting-openapi-versions-prior-to-32)x-oai-name - An identifier for a Server Object, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `name` field on Server Objects to provide a unique identifier for a server.

The `x-oai-name` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to provide a unique identifier for a Server Object.

It can appear as a property in the following objects: `["Server Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-name.html#schema)Schema

```
{"type"=>"string"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-name.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
servers:
  - url: https://api.example.com
    x-oai-name: production
    description: Production server
  - url: https://staging.example.com
    x-oai-name: staging
    description: Staging server
```
