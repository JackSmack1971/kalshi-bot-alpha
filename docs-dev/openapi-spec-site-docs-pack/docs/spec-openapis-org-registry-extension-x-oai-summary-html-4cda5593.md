---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-summary.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.669Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-summary.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-summary.html#x-oai-summary---a-short-summary-for-a-response-object-used-when-targeting-openapi-versions-prior-to-32)x-oai-summary - A short summary for a Response Object, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `summary` field on Response Objects to provide a short summary of a response.

The `x-oai-summary` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to provide a short summary of a response.

It can appear as a property in the following objects: `["Response Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-summary.html#schema)Schema

```
{"type"=>"string"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-summary.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths:
  /widgets:
    get:
      responses:
        "200":
          description: A list of widgets
          x-oai-summary: Widget list
```
