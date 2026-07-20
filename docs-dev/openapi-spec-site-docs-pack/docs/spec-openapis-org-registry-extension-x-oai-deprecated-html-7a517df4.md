---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-deprecated.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.133Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-deprecated.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-deprecated.html#x-oai-deprecated---indicates-that-a-security-scheme-is-deprecated-used-when-targeting-openapi-versions-prior-to-32)x-oai-deprecated - Indicates that a Security Scheme is deprecated, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `deprecated` field on Security Scheme Objects to indicate that a security scheme is deprecated and SHOULD be transitioned out of usage.

The `x-oai-deprecated` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to indicate that a Security Scheme Object is deprecated and SHOULD be transitioned out of usage.

It can appear as a property in the following objects: `["Security Scheme Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-deprecated.html#schema)Schema

```
{"type"=>"boolean"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-deprecated.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
components:
  securitySchemes:
    legacyApiKey:
      type: apiKey
      in: header
      name: X-API-Key
      x-oai-deprecated: true
```
