---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-additionalOperations.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.009Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-additionalOperations.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-additionalOperations.html#x-oai-additionaloperations---represents-non-standard-http-method-operations-on-a-path-item-when-targeting-openapi-versions-prior-to-32)x-oai-additionalOperations - Represents non-standard HTTP method operations on a Path Item when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `additionalOperations` field on Path Item Objects to represent operations for HTTP methods that are not part of the standard set defined by the Path Item Object of the target OpenAPI version. For example, the non-standard `POLL` method has no standard operation in OpenAPI 3.2, so it can be represented as an entry in the `additionalOperations` field.

The `x-oai-additionalOperations` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to represent operations for HTTP methods that are not part of the standard set defined by the Path Item Object of the target OpenAPI version. For example, the HTTP QUERY method has no standard operation in OpenAPI 3.0 or 3.1, so it can be represented as an entry in the `x-oai-additionalOperations` extension.

Each key in the object is an HTTP method name (e.g. `QUERY`) and the value is an Operation Object.

It can appear as a property in the following objects: `["Path Item Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-additionalOperations.html#schema)Schema

```
{"type"=>"object", "additionalProperties"=>{"$ref"=>"#/$defs/operationObject"}}
```

### [](https://spec.openapis.org/registry/extension/x-oai-additionalOperations.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths:
  /search:
    x-oai-additionalOperations:
      QUERY:
        summary: Search with a request body
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                  q:
                    type: string
        responses:
          "200":
            description: Search results
```
