---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-encoding.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.308Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-encoding.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-encoding.html#x-oai-encoding---a-map-of-nested-encoding-definitions-for-an-encoding-object-used-when-targeting-openapi-versions-prior-to-32)x-oai-encoding - A map of nested encoding definitions for an Encoding Object, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `encoding` field on Encoding Objects to define nested encoding information.

The `x-oai-encoding` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to define nested encoding information on an Encoding Object.

Each key in the object is the name of a nested property and the value is an Encoding Object.

It can appear as a property in the following objects: `["Encoding Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-encoding.html#schema)Schema

```
{"type"=>"object", "additionalProperties"=>{"$ref"=>"#/$defs/encodingObject"}}
```

### [](https://spec.openapis.org/registry/extension/x-oai-encoding.html#example)Example

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
              type: object
              properties:
                file:
                  type: string
                  format: binary
            encoding:
              file:
                contentType: application/octet-stream
                x-oai-encoding:
                  nested:
                    contentType: text/plain
      responses:
        "200":
          description: Upload successful
```
