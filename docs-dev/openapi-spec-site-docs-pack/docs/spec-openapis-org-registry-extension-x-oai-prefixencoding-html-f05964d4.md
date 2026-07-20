---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-prefixEncoding.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.554Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-prefixEncoding.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-prefixEncoding.html#x-oai-prefixencoding---encoding-properties-applied-before-the-item-encoding-in-a-multipart-request-part-used-when-targeting-openapi-versions-prior-to-32)x-oai-prefixEncoding - Encoding properties applied before the item encoding in a multipart request part, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `prefixEncoding` field on Media Type Objects to define an ordered list of encodings applied before the item encoding within a media type.

The `x-oai-prefixEncoding` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to define an ordered list of encodings applied before the item encoding.

It can appear as a property in the following objects: `["Media Type Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-prefixEncoding.html#schema)Schema

```
{"type"=>"array", "items"=>{"$ref"=>"#/$defs/encodingObject"}}
```

### [](https://spec.openapis.org/registry/extension/x-oai-prefixEncoding.html#example)Example

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
            x-oai-prefixEncoding:
              - contentType: application/json
      responses:
        "200":
          description: Upload successful
```
