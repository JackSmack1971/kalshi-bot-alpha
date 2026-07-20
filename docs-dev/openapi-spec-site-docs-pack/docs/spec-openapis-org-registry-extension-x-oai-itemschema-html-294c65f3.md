---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-itemSchema.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.434Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-itemSchema.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-itemSchema.html#x-oai-itemschema---schema-for-individual-items-in-a-multipart-request-part-used-when-targeting-openapi-versions-prior-to-32)x-oai-itemSchema - Schema for individual items in a multipart request part, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `itemSchema` field on Media Type Objects to define the schema for individual items within a media type, applicable to multipart or array-based content.

The `x-oai-itemSchema` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to define the schema for individual items within a media type.

It can appear as a property in the following objects: `["Media Type Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-itemSchema.html#schema)Schema

```
{"$ref"=>"#/$defs/schemaObject"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-itemSchema.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths:
  /upload:
    post:
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: array
              items:
                type: string
                format: binary
            x-oai-itemSchema:
              type: string
              format: binary
      responses:
        "200":
          description: Upload successful
```
