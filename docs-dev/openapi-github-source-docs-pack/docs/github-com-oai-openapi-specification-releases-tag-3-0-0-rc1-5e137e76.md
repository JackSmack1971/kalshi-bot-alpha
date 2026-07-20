---
title: "OAS 3.0.0-rc1 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.0-rc1"
host: "github.com"
depth: 3
selector: "article,main"
fetched_at: "2026-07-17T17:43:50.458Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.0.0-rc1 Released!

Pre-release

Pre-release

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 28 Apr 02:12

[3.0.0-rc1](https://github.com/OAI/OpenAPI-Specification/tree/3.0.0-rc1)

[`0686522`](https://github.com/OAI/OpenAPI-Specification/commit/0686522d8bf6aa81ab84070a3af498d083d08d8b)

# OAS 3.0.0-rc1 Change Log

## Schema Changes

-   `url` is now **required** under the Server Object.
-   Server Variable Object's `enum` and `default` values are now `string` only (were any `primitive`).
-   `servers` under the Path Item Object and Operation Object has been fixed to be an array of Server Objects and not a single one.
-   The `example` and `examples` fields have been reworked, alongside the Example Object. There is no longer `examples` field under the Schema Object. Where `examples` exist, they are now a map of named examples with additional metadata for each example. The Example Object now has defined fields and is not free-form.
-   `content` is now **required** under the Request Body Object.
-   `href` under the Link Object has been renamed to `operationRef`, its description is clarified as well.
-   The `deprecated` field under the Schema Object now defaults to `false`.
-   The `flow` field under the Security Scheme Object has been renamed to `flows`.
-   Request Body's `required` now defaults to `false`.
-   Added `allowReserved` to the Encoding Property Object.

## Descriptive Changes

-   `termsOfService` now MUST be in the form of a URL.
-   all `description` fields now support CommonMark.
-   Clarified that specific response codes (`200` for example) take precedence over response ranges (`2XX` for example).
-   Clarified that for Parameter Object, either `schema` or `content` are required.
-   `pattern` under the Schema Object now specifies the regex flavor.
-   Added header restrictions. "Accept", "Content-Type", "Authorization" header paramters and "Content-Type" response headers will now be ignored.
-   Referenced a specific version of supported CommonMark.
-   Added clarifications to `null` not being a type (as opposed to a value).

## Document Changes

-   ToC has been updated to reflect changes.
-   Fixed various anchors in the document.
-   Various examples have been fixed.

Check it out! [https://github.com/OAI/OpenAPI-Specification/blob/3.0.0-rc1/versions/3.0.md](https://github.com/OAI/OpenAPI-Specification/blob/3.0.0-rc1/versions/3.0.md)

Assets 2

Loading
