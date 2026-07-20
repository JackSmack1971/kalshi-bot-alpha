---
title: "Extension Field Registry"
source_url: "https://spec.openapis.org/registry/extension/x-twitter.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:07.724Z"
---
# [](https://spec.openapis.org/registry/extension/x-twitter.html#extension-field-registry)[Extension Field Registry](https://spec.openapis.org/registry/extension/)

## [](https://spec.openapis.org/registry/extension/x-twitter.html#x-twitter---used-to-hold-a-reference-to-the-api-providers-twitter-account)x-twitter - Used to hold a reference to the API provider’s Twitter account.

The `x-twitter` extension is used to hold a reference to the API provider’s Twitter account. It can appear as a property in the following objects: `["contactObject"]`.

### [](https://spec.openapis.org/registry/extension/x-twitter.html#schema)Schema

```
{"type"=>"string"}
```

### [](https://spec.openapis.org/registry/extension/x-twitter.html#example)Example

```
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
  contact:
    x-twitter: APIs-guru
```

Used by: (informational)

-   APIs.guru
