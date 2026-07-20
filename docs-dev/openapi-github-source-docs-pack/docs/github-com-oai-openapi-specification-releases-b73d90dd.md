---
title: "Releases: OAI/OpenAPI-Specification"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases?page=2"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:17.823Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# Releases: OAI/OpenAPI-Specification


## Release list

[Previous](https://github.com/OAI/OpenAPI-Specification/releases?page=1) Next

Jump to release

-   [OAS 3.0.0 Released!](https://github.com/OAI/OpenAPI-Specification/releases?page=2#release-3.0.0)
-   [OAS 3.0.0-rc2 Released!](https://github.com/OAI/OpenAPI-Specification/releases?page=2#release-3.0.0-rc2)
-   [OAS 3.0.0-rc1 Released!](https://github.com/OAI/OpenAPI-Specification/releases?page=2#release-3.0.0-rc1)
-   [OAS 3.0.0-rc0 Released!](https://github.com/OAI/OpenAPI-Specification/releases?page=2#release-3.0.0-rc0)

[Previous](https://github.com/OAI/OpenAPI-Specification/releases?page=1) Next

## OAS 3.0.0 Released!

[OAS 3.0.0 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.0)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 26 Jul 07:31

[3.0.0](https://github.com/OAI/OpenAPI-Specification/tree/3.0.0)

[`e9c539d`](https://github.com/OAI/OpenAPI-Specification/commit/e9c539d86f080f133aa35c3e7db33ef004496625)

# OAS 3.0.0 Change Log

The OAI is pleased to announce the official release of the OpenAPI Specification 3.0.0!

The list below reflect the changes since the last release candidate.

## Schema Changes

-   The `headers` map under the Encoding Object can now also reference headers.

## Descriptive Changes

-   Reworded descriptions for clearer intent (no change of meaning).
-   The OpenAPI Definition File has been renamed as the OpenAPI Document.
-   Changes to better conform to RFC 2119.
-   Elaborated Request Body's and Response's content field support media type ranges.
-   Fixed descriptions of `operationRef` and `operationId` under the Link Object. Also clarified that a Link MUST contain one of them.
-   Added links to OAuth2's and OpenID Connect's specifications.

## Document Changes

-   Some example fixes.

Check it out! [https://github.com/OAI/OpenAPI-Specification/blob/3.0.0/versions/3.0.0.md](https://github.com/OAI/OpenAPI-Specification/blob/3.0.0/versions/3.0.0.md)

Assets 2

Loading


## OAS 3.0.0-rc2 Released!

[OAS 3.0.0-rc2 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.0-rc2) Pre-release

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


## OAS 3.0.0-rc1 Released!

[OAS 3.0.0-rc1 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.0-rc1) Pre-release

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


## OAS 3.0.0-rc0 Released!

[OAS 3.0.0-rc0 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.0-rc0) Pre-release

Pre-release

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 01 Mar 01:04

[3.0.0-rc0](https://github.com/OAI/OpenAPI-Specification/tree/3.0.0-rc0)

[`d232e6d`](https://github.com/OAI/OpenAPI-Specification/commit/d232e6d3e1ea4038a533329a82876ae868e9cf13)

We're happy to announce the release of the first Implementer's Draft of OAS 3.0.0, known as 3.0.0-rc0.

A lot of changes in this release, as a first one goes, so expect the change log to be updated. An initial list of changes, in no particular order:

-   Changed the versioning scheme of the spec.
-   Reusable definitions in the spec has been expanded and reorganized under the Components Object.
-   Added support for operation callbacks.
-   Added support for a new static linking between responses and operations.
-   Reworked parameters - removed formData parameters, added cookie parameters, changed body parameters to Request Body Objects as a separate entity.
-   Parameters now support complex types.
-   Responses support multiple media type specifications.
-   Reworked file support. Dropped `file` as a type, but provided better handling for file uploads and downloads.
-   Reworked security definitions to allow for support for more schemes.
-   Improved support for examples throughout the spec.
-   Added support for defining multiple servers hosting the API, including URL variables.

Check it out! [https://github.com/OAI/OpenAPI-Specification/blob/3.0.0-rc0/versions/3.0.md](https://github.com/OAI/OpenAPI-Specification/blob/3.0.0-rc0/versions/3.0.md)

Our [blog post](https://www.openapis.org/blog/2017/03/01/openapi-spec-3-implementers-draft-released) contains more details of the process and next steps.

Assets 2

Loading


[Previous](https://github.com/OAI/OpenAPI-Specification/releases?page=1) [1](https://github.com/OAI/OpenAPI-Specification/releases?page=1) [2](https://github.com/OAI/OpenAPI-Specification/releases?page=2) Next

[Previous](https://github.com/OAI/OpenAPI-Specification/releases?page=1) Next
