---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-oai-deviceAuthorizationUrl.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.249Z"
---
# [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorizationUrl.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorizationUrl.html#x-oai-deviceauthorizationurl---the-device-authorization-url-for-an-oauth2-flow-rfc-8628-used-when-targeting-openapi-versions-prior-to-32)x-oai-deviceAuthorizationUrl - The device authorization URL for an OAuth2 flow (RFC 8628), used when targeting OpenAPI versions prior to 3.2.

OpenAPI 3.2 introduced the `deviceAuthorizationUrl` field on OAuth Flow Objects to specify the URL to be used for device authorization as defined in [RFC 8628](https://www.rfc-editor.org/rfc/rfc8628).

The `x-oai-deviceAuthorizationUrl` extension brings this same capability to OpenAPI versions prior to 3.2, allowing you to specify the device authorization URL for an OAuth2 flow.

It can appear as a property in the following objects: `["OAuth Flow Object"]`.

Used by: (informational)

-   [Microsoft.OpenApi](https://github.com/microsoft/OpenAPI.NET) (.NET OpenAPI library)

### [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorizationUrl.html#schema)Schema

```
{"type"=>"string", "format"=>"uri"}
```

### [](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorizationUrl.html#example)Example

```
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
components:
  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: https://auth.example.com/token
          x-oai-deviceAuthorizationUrl: https://auth.example.com/device
          scopes:
            read: Read access
```
