---
title: "OAS 3.0.0-rc2 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.0-rc2"
host: "github.com"
depth: 3
selector: "article,main"
fetched_at: "2026-07-17T17:43:48.777Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.0.0-rc2 Released!

Pre-release

Pre-release

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 17 Jun 00:19

[3.0.0-rc2](https://github.com/OAI/OpenAPI-Specification/tree/3.0.0-rc2)

[`9c08338`](https://github.com/OAI/OpenAPI-Specification/commit/9c083382b39148f909b9dce768740f43e4a61a66)

# OAS 3.0.0-rc2 Change Log

## Schema Changes

-   The following objects have been removed from the specification: Server Variables, Content, Encoding, Callbacks, Headers, Links, Link Parameters, Scopes. They have all been replaced by the `Map` construct being effectively what they are. Clarifies that specification extensions are not allowed, as they did not make sense.
-   The Encoding Property Object has been renamed to the Encoding Object. This is a result of the above change.
-   The Encoding Object now specifies to which media type each property is applicable.
-   The Encoding Object now defines `headers` as a map of Header Objects.
-   The different components under the `Components Object` can now either be defined inline or referenced.
-   For parameters using `content`, now only one media type can be used at most.
-   The `headers` property under the Link Object has been removed.
-   Link Object has a new `requestBody` property to allow passing a request body.
-   The Schema Object's `discriminator` property has been completely reworked to utilize the newly supported `oneOf` and `anyOf`. A new `Discriminator Object` has been added to support these changes.
-   The XML Object's `namespace` now MUST be an absolute URI.
-   The `apiKey` security scheme can now also be in `cookie`.

## Descriptive Changes

-   The `Rich Text Formatting` section has been reworded to ease the requirements.
-   Added OpenAPI Definition File definition.
-   Clarified that an empty or nonexisting `servers` would default to a single Server with the `url` value of `/`.
-   Reworded the section explaining the specification's versioning scheme.
-   Server Variable `enum`'s description has been fixed to state it can only be a string (the type was correct).
-   Added clarification + examples how path matching works for paths defined under the `Paths Object`.
-   Removed recommendation for a 120 character limit for the `summary` field under the Operation Object.
-   Further details added to the `form` and `simple` types of `style`.
-   Clarified that the Encoding Object applies to both `multipart` and `application/x-www-form-urlencoded` and only those.
-   Clarified the possible response code wildcards are only `1XX`, `2XX`, `3XX`, `4XX` or `5XX`.
-   Variable Expressions have been renamed to Runtime Expressions. They have been unified between Links and Callbacks, and have a dedicated section. Various examples have been moved and removed as a result.
-   Runtime expressions now use curly braces when found inside strings.
-   Link Object's `parameters` now defines how to deal with cases of parameter name ambiguity.

## Document Changes

-   ToC has been updated to reflect changes.
-   Fixed various anchors in the document.
-   Various examples have been fixed.
-   Various editorial changes were made to make the document more readable.

Check it out! [https://github.com/OAI/OpenAPI-Specification/blob/3.0.0-rc2/versions/3.0.md](https://github.com/OAI/OpenAPI-Specification/blob/3.0.0-rc2/versions/3.0.md)

Assets 2

Loading
