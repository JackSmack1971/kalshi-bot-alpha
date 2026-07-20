---
title: "OAS 3.0.3 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.3"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:24.980Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.0.3 Released!

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 21 Feb 01:37

[3.0.3](https://github.com/OAI/OpenAPI-Specification/tree/3.0.3)

[`c8e90df`](https://github.com/OAI/OpenAPI-Specification/commit/c8e90dfa4ccf8054db1539f7a104c5ccfb1913c3)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**. The key has expired.

GPG key ID: 4AEE18F83AFDEB23

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

# OAS 3.0.3 Change Log

The OAI is pleased to announce the official release of the OpenAPI Specification 3.0.3!

As a patch release, the following changes were made to improve the specification in terms of readability and accuracy. None of these modifications change the behavior of the spec.

-   Clarified how Path Templating works.
-   Clarified the meaning of Semantic Versioning as it applies to the OpenAPI Specification (note, this is the `openapi` field, not the `version` field).
-   Changed some hyperlinks from `http` to `https`.
-   Clarified add the notion of optional security on operations.
-   Added an explanation that the `Server Variable Object`'s `enum` should not be empty. This is not a breaking change but should be considered as guidance for a more explicit restriction in the next major version.
-   Clarified paths under the `Paths Object` should start with a forward slash.
-   Clarified `Path Item Object`'s `$ref` behavior with sibling fields.
-   Fixed a few examples.
-   Clarified the map structure of `callbacks` under the `Operation Object`.
-   Clarified how path parameters are being matched.
-   Clarified `example`/`examples` value(s) in the `Parameter Object`.
-   Fixed example for `pipeDelimited` `object` value.
-   Fixed `Callback Object` description.
-   Clarified `Link Object`'s `operationDef`'s description.
-   Improved ABNF for `Runtime Expressions`.
-   Clarified valid regex for `pattern` under `Schema Object`.
-   Clarified the behavior of `nullable` under `Schema Object`.
-   Fixed names of OAuth2 flows in the description of `Security Scheme Object`.
-   Improved description of `Security Filtering` section.

Assets 2

Loading
