---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-itemEncoding.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.371Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-itemEncoding.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-itemEncoding.html#x-oai-itemencoding---encoding-properties-for-individual-items-in-a-multipart-request-part-used-when-targeting-openapi-versions-prior-to-32)x-oai-itemEncoding - Encoding properties for individual items in a multipart request part, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `itemEncoding` field on Media Type Objects to define the encoding for individual items within a media type, applicable to multipart or array-based content.

The `x-oai-itemEncoding` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to define the encoding for individual items within a media type.

It can appear as a property in the following objects: `["Media Type Object","Encoding Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-itemEncoding.html#schema)Schema

```
{"$ref"=>"#/$defs/encodingObject"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-itemEncoding.html#example)Example

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
            x-oai-itemEncoding:
              contentType: application/octet-stream
      responses:
        "200":
          description: Upload successful
```
