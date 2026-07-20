---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-deviceAuthorization.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.190Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorization.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorization.html#x-oai-deviceauthorization---a-device-authorization-oauth2-flow-used-when-targeting-openapi-versions-prior-to-32)x-oai-deviceAuthorization - A device authorization OAuth2 flow, used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the [`deviceAuthorization`](https://spec.openapis.org/oas/v3.2.0.html#oauth-flows-device-authorization) field on OAuth Flows Objects to define a device authorization OAuth2 flow.

The `x-oai-deviceAuthorization` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to define a device authorization OAuth2 flow.

Use this extension only with OpenAPI versions before 3.2; OpenAPI 3.2 and later define `deviceAuthorization` directly.

It can appear as a property in the following objects: `["OAuth Flows Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorization.html#schema)Schema

```
{"$ref"=>"#/$defs/oauthFlowObject"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorization.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
paths: {}
components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        x-oai-deviceAuthorization:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          x-oai-deviceAuthorizationUrl: https://auth.example.com/device
          scopes:
            read: Read access
```
