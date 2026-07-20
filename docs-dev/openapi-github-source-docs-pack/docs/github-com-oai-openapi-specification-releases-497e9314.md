---
title: "Releases: OAI/OpenAPI-Specification"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases"
host: "github.com"
depth: 1
selector: "article,main"
fetched_at: "2026-07-17T17:42:47.712Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# Releases: OAI/OpenAPI-Specification


## Release list

Previous [Next](https://github.com/OAI/OpenAPI-Specification/releases?page=2)

Jump to release

-   [OAS 3.2.0 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.2.0)
-   [OAS 3.1.2 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.1.2)
-   [OAS 3.1.1 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.1.1)
-   [OAS 3.0.4 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.0.4)
-   [OAS 3.1.0 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.1.0)
-   [OAS 3.1.0-rc1 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.1.0-rc1)
-   [OAS 3.1.0-rc0 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.1.0-rc0)
-   [OAS 3.0.3 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.0.3)
-   [OAS 3.0.2 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.0.2)
-   [OAS 3.0.1 Released!](https://github.com/OAI/OpenAPI-Specification/releases#release-3.0.1)

Previous [Next](https://github.com/OAI/OpenAPI-Specification/releases?page=2)

## OAS 3.2.0 Released!

[OAS 3.2.0 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.2.0) [Latest](https://github.com/OAI/OpenAPI-Specification/releases/latest)

[Latest](https://github.com/OAI/OpenAPI-Specification/releases/latest)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@lornajane](https://avatars.githubusercontent.com/u/172607?s=40&v=4) [lornajane](https://github.com/lornajane) released this 19 Sep 16:20

[3.2.0](https://github.com/OAI/OpenAPI-Specification/tree/3.2.0)

[`99710bc`](https://github.com/OAI/OpenAPI-Specification/commit/99710bcb26cbe4be646565eebeb04348f02374b5)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

### Headline features

-   Multipurpose tags, with nesting

    -   `summary` field to allow short descriptions, used when displaying lists of tags.
    -   `parent` field to point to the tag that this tag is nested under.
    -   `kind` field to allow a tag to be classified into a category such as navigation, or audience.
        The `kind` field is free-form text, however there are some expected/conventional values such as `nav` (in line with the most common current usage as grouping for documentation output).
    -   A [registry](https://spec.openapis.org/registry/tag-kind/index.html) to establish conventions for values used in `kind`.
-   Support for additional HTTP methods

    -   Support the new `query` method alongside the existing `get`/`post`/`put`/`delete`/`options`/`head`/`patch`/`trace`.
    -   Under an `additionalOperations` entry in a Path, use any other methods not listed as keys using the correct capitalization, e.g. `LINK`. Do NOT add `HEAD` under this, use the existing sibling `head`.
-   Document identity and URL resolution

    -   Additional top-level field `$self` is added to allow users to define the base URI of the document, used to resolve relative references.
    -   More explanation and examples regarding URL resolution.

### Data modeling and representation

-   Streaming support: sequential media types including SSE

    -   Support for sequential media types such as `text/event-stream` for server-sent events (SSE) and `multipart/mixed`, `application/jsonl`, `application/json-seq` and others for sequential data.
    -   Responses can be a repeating data structure, and are treated as if they are an array of Schema Objects.
    -   Use `itemSchema` in a mediatype entry to describe each item.
    -   A media types registry is published to give more context for each of the media types.
-   Parameter and header changes

    -   Additional parameter location `querystring`, to allow parsing the entire query string as a single field similar to the way a request body is handled, using the `content` field.
    -   Parameters can therefore be `in` the `querystring` as an alternative to the existing `header`, `cookie`, `query` and `path` values.
    -   `allowReserved` field is now permitted on headers and on parameters with any value of `in`, and applies where the combination of `in` and `style` automatically percent-encode the value.
-   New `style` option for cookies

    -   Additional `style` option `cookie` for content in a cookie, which uses semicolon as a separator and does not encode data values.
-   Additions to support multipart media types

    -   New `itemSchema` field, for the schema that describes each of the items in a sequential media type.
    -   New fields `prefixEncoding` and `itemEncoding` can be used instead of `encoding` for multipart media types.
    -   The specification also contains examples of sequential JSON and Server-Sent events that show these fields in use.
-   Improvements for APIs using XML as a content format

    -   New `nodeType` field allows mapping schemas to common XML node types: `element`, `attribute`, `text`, `cdata`, or `none`.
    -   `attribute: true` is now deprecated in favor of `nodeType: attribute`.
    -   `wrapped: true` is now deprecated in favor of `nodeType: element` (as `nodeType` defaults to `none` for arrays to preserve compatibility).
    -   The `xml` keyword can be used in any Schema Object.
    -   XML namespaces can be IRIs (rather than URIs).
    -   Explanation and examples for many use cases including handling `null`, handling arrays, replacing the name, and handling ordered elements.
    -   Clarify that the root schema of an XML Object should use the component name.
-   Examples as either structured or serialized values

    -   The Example Object (used in `examples` fields) gets two new fields: `dataValue` and `serializedValue`.
    -   `dataValue` describes the example in structured format.
    -   `serializedValue` shows how the example will be formatted when it is sent/received by the API.
    -   The existing `externalValue` field can still be used to give a reference to an example, but this is now clearly documented as being a serialized value.

### Additional features

-   Updated security schemes

    -   Support for [OAuth2 Device Authorization flow](https://datatracker.ietf.org/doc/html/rfc8628) with additional `deviceAuthorization` field in the `flows` object and for the individual flow, a new field `deviceAuthorizationUrl` alongside `tokenUrl`.
    -   Additional security scheme field: `oauth2MetadataUrl` URL for auth server metadata, as described by the [OAuth2 Server Metadata Standard](https://datatracker.ietf.org/doc/html/rfc8414).
    -   Additional `deprecated` field for security schemes (indicating that the scheme may still be supported, but that it should not be used).
    -   Ability to reference a security scheme by URI rather than declaring it in components.
-   Improvements to the Server Object

    -   Clarify that server URLs should not include fragment or query.
    -   Support new `name` field alongside `description`, `url` and `variables`.
    -   Formal ABNF syntax for the allowed variable substitution in server urls, alongside guidance that each variable can only be used once in a URL.
-   Better polymorphic support

    -   The discriminator `propertyName` can now be an optional field.
    -   New field `defaultMapping` to indicate which schema to use if the `propertyName` is not set, or if the value is unrecognized.
-   Templates with formal syntax

    -   The specification now includes **ABNF** (Augmented Backus–Naur Form) for path templating, server variables, and runtime expressions in the Link Object.
-   Flexible metadata fields in the Response Object

    -   `description` field for responses is now optional.
    -   Additional `summary` field for responses.
-   Additional updates

    -   A new key `mediaTypes` is supported under `components` to support re-use of Media Type Objects.
-   Updates to referenced standards

    -   Update to [https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html) of JSON Schema Specification.
    -   Update to [https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html) of JSON Schema Validation Specification.
    -   Use [RFC8529](https://tools.ietf.org/html/rfc8259) for JSON.
    -   Use [RFC9110](https://tools.ietf.org/html/rfc9110) for HTTP.
-   Editorial changes

    -   Extensive additions around media types, encoding, sequential media types, SSE examples, working with binary data.
    -   Streamlined to YAML examples (unless something specific to another format) to try to make it easier to follow.
    -   Better explanation and examples for using Encoding and Serialization, and a note not to apply percent-encoding to headers.
    -   Clarify that Request Body Objects need to specify at least one media type to be meaningful.
    -   How to more clearly indicate that responses will not have a body.
    -   Explanation and examples of headers including `Link` and `Set-Cookie`.
    -   Detailed explanation of percent-encoding and -decoding, updated examples and references to match, including the Style Examples table.
    -   Extensive additional notes on parsing and serializing JSON and non-JSON data formats.

Assets 2

Loading


👍 20 hanspagel, hammerlink, YohanSciubukgian, dannysheridan, valerii15298, SamuelMarks, MarkRosemaker, sorbonad, H1Gdev, glarrain, and 10 more reacted with thumbs up emoji 🎉 20 hkosova, marclave, hellobudha, cameronrohani, hanspagel, daveshanley, valerii15298, at146, sebastienlevert, MarkRosemaker, and 10 more reacted with hooray emoji ❤️ 14 mrlubos, marclave, hellobudha, cameronrohani, hanspagel, daveshanley, valerii15298, at146, MarkRosemaker, Rangarajanl-OpenSource, and 4 more reacted with heart emoji 🚀 10 hanspagel, daveshanley, valerii15298, at146, MarkRosemaker, minskimm, MokoGuy, usadamasa, dasdawidt, and baywet reacted with rocket emoji 👀 5 hanspagel, valerii15298, minskimm, ThomasMasak, and sukhmel reacted with eyes emoji

47 people reacted

## OAS 3.1.2 Released!

[OAS 3.1.2 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.2)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@lornajane](https://avatars.githubusercontent.com/u/172607?s=40&v=4) [lornajane](https://github.com/lornajane) released this 19 Sep 15:45

[3.1.2](https://github.com/OAI/OpenAPI-Specification/tree/3.1.2)

[`8260336`](https://github.com/OAI/OpenAPI-Specification/commit/82603363df271c104c8f527f0fe641ea67da93fd)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

Version 3.1.2 has no material changes but does contain editorial fixes, additional examples, and clarifications.

-   Clarify that `$ref` in a Schema Object is a JSON Schema `$ref` keyword.
-   Detailed explanation of percent-encoding and -decoding, updated examples and references to match, including the Style Examples table.
-   Better explanation and examples for using Encoding and Serialization, and a note not to apply percent-encoding to headers.
-   Clarify that Request Body Objects need to specify at least one media type to be meaningful.
-   How to more clearly indicate that no response will have a body.
-   How to handle `null` in XML as an advisory note; since the functionality cannot be changed it is implementation-defined for 3.1 tooling.
-   Clarify that the root schema of an XML object should use the component name.

Assets 2

Loading


🎉 3 YOU54F, char0n, and mrtn78 reacted with hooray emoji

3 people reacted

## OAS 3.1.1 Released!

[OAS 3.1.1 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.1)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@lornajane](https://avatars.githubusercontent.com/u/172607?s=40&v=4) [lornajane](https://github.com/lornajane) released this 24 Oct 17:37

[3.1.1](https://github.com/OAI/OpenAPI-Specification/tree/3.1.1)

[`69d8b79`](https://github.com/OAI/OpenAPI-Specification/commit/69d8b7953c3259e243cf746388a0951b89649763)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

# Release Notes

While the 3.1.1 release makes no changes to requirements of the OpenAPI 3.1.0 specification, it does introduce a number of notable improvements, including:

-   Expands and clarifies a number of explanations, including several new appendices with supplementary details
-   Focuses on technical specifics by moving examples and additional documentation now published at [learn.openapis.org](https://learn.openapis.org/)
-   Declares that the HTML specifications at [spec.openapis.org](https://spec.openapis.org/) are now the authoritative versions (formerly it was the Markdown source on GitHub)

OpenAPI Description writers should mark their OpenAPI Descriptions with the version of the OpenAPI specification they used to write their specification, updating where possible.

Tooling maintainers should expect minimal work to support 3.1.1; however, we recommend checking the list of changes below.

## Clearer Definitions

Introduce consistent language around OpenAPI Document/Description/Definition:

-   OpenAPI Description means the OpenAPI description of an API, whether it is in one or many files.
-   A document means a single file.
-   An "entry document" is where the OpenAPI Description for an API starts; it may reference other documents.

Improved language regarding schemas, explaining the difference between the OpenAPI schema, the schemas used within the OpenAPI schema, and the use of a non-authoritative JSON Schema to supplement the written spec.

Added guidance around use of schema dialects.

## References

Additional guidance for resolving references and parsing documents was added, resolving component names, tags, and operationIds are clarified.
The adoption of JSON Schema in 3.1.x changed the parsing and referencing, and a new section was added to cover the changes in more depth than in 3.1.0.

Improved explanation of URLs and URIs, and made clear which to use for each URL/URI field.
Clarified that Markdown links are resolved in relation to their rendered context.

## Data Types

Extensive clarifications on data types and encoding.

Added a section on handling binary data.

## Security

Added a note that a `security` array that is empty or missing does not indicate that no security arrangements exist for this API.

Updated references to other standards where newer versions are available, and added more explanation for OpenIDConnect.

Added a "Security Concerns" section containing advice for implementers and users of OpenAPI.

## Request Data

Extensive refactoring of the parameters section
Examples were updated, improved, and explanations added.

Headers have their own section with examples and specific information.

Improves and expands on OpenAPI `example` and `examples` and adds a "Working with Examples" section with a clearer description and examples.

Clarifies and expands on file uploads, form-urlencoded request bodies, and multipart content, and moves them to a refactored `Encoding Object` section to provide better coverage of edge cases and more examples.

Assets 2

Loading


👍 17 i0tool5, Spokeek, jeremyfiel, hendriknielaender, at146, DevYeom, rafalkrupinski, mrlubos, Mohammad-Alavi, Stranger6667, and 7 more reacted with thumbs up emoji 😄 2 Meleleka676 and SharkG-max reacted with laugh emoji 🎉 18 ralfhandl, badsyntax, Cyrus-Kiprop, i0tool5, jeremyfiel, hendriknielaender, LasneF, mrlubos, Stranger6667, paulRbr, and 8 more reacted with hooray emoji ❤️ 10 jeremyfiel, hendriknielaender, i0tool5, mrlubos, antlio, Meleleka676, emmanuelgautier, Andibeethoven, Mohammad-Alavi, and SharkG-max reacted with heart emoji 🚀 11 i0tool5, hendriknielaender, monitaurus, mrlubos, Stranger6667, frankkilcommins, rlebran, Meleleka676, Mohammad-Alavi, SharkG-max, and Chrissymars reacted with rocket emoji 👀 6 Homedefense78, victorbalssa, Meleleka676, Andibeethoven, SharkG-max, and Elmago34 reacted with eyes emoji

36 people reacted

## OAS 3.0.4 Released!

[OAS 3.0.4 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.4)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@lornajane](https://avatars.githubusercontent.com/u/172607?s=40&v=4) [lornajane](https://github.com/lornajane) released this 24 Oct 17:36

[3.0.4](https://github.com/OAI/OpenAPI-Specification/tree/3.0.4)

[`b895310`](https://github.com/OAI/OpenAPI-Specification/commit/b8953109f2eb4d9eebcc7f702f70456b2e074567)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

# Release Notes

While the 3.0.4 release makes no changes to requirements of the OpenAPI 3.0.3 specification, it does introduce a number of notable improvements, including:

-   Expands and clarifies a number of explanations, including several new appendices with supplementary details
-   Focuses on technical specifics by moving examples and additional documentation now published at [learn.openapis.org](https://learn.openapis.org/)
-   Declares that the HTML specifications at [spec.openapis.org](https://spec.openapis.org/) are now the authoritative versions (formerly it was the Markdown source on GitHub)

OpenAPI Description writers should mark their OpenAPI Descriptions with the version of the OpenAPI specification they used to write their specification, updating where possible.

Tooling maintainers should expect minimal work to support 3.0.4; however, we recommend checking the list of changes below.

## Clearer Definitions

Introduce consistent language around OpenAPI Document/Description/Definition:

-   OpenAPI Description means the OpenAPI description of an API, whether it is in one or many files.
-   A document means a single file.
-   An "entry document" is where the OpenAPI Description for an API starts; it may reference other documents.

Improved language regarding schemas, explaining the difference between the OpenAPI schema, the schemas used within the OpenAPI schema, and the use of a non-authoritative JSON Schema to supplement the written spec.

## References

Additional guidance for resolving references and parsing documents was added, resolving component names, tags, and operationIds are clarified.
Clarified that Markdown links are resolved in relation to their rendered context.

## Data Types

Extensive clarifications on data types and encoding.

Added a section on handling binary data.

## Security

Added a note that a `security` array that is empty or missing does not indicate that no security arrangements exist for this API.

Updated references to other standards where newer versions are available, and added more explanation for OpenIDConnect.

Added a "Security Concerns" section containing advice for implementers and users of OpenAPI.

## Request Data

Extensive refactoring of the parameters section
Examples were updated, improved, and explanations added.

Headers have their own section with examples and specific information.

Improves and expands on OpenAPI `example` and `examples` and adds a "Working with Examples" section with a clearer description and examples.

Clarifies and expands on file uploads, form-urlencoded request bodies, and multipart content, and moves them to a refactored `Encoding Object` section to provide better coverage of edge cases and more examples.

Assets 2

Loading


👍 4 jeremyfiel, i0tool5, rafalkrupinski, and preet-adhikari reacted with thumbs up emoji 🎉 3 ralfhandl, jeremyfiel, and Elkiwa reacted with hooray emoji ❤️ 2 jeremyfiel and i0tool5 reacted with heart emoji 🚀 2 jeremyfiel and frankkilcommins reacted with rocket emoji

7 people reacted

## OAS 3.1.0 Released!

[OAS 3.1.0 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 16 Feb 19:33

[3.1.0](https://github.com/OAI/OpenAPI-Specification/tree/3.1.0)

[`42a9e3d`](https://github.com/OAI/OpenAPI-Specification/commit/42a9e3d4eddade52363a5c4fac852e80681c2fe5)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**. The key has expired.

GPG key ID: 4AEE18F83AFDEB23

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

The OAI is pleased to announce the official release of the OpenAPI Specification 3.1.0!

## Changelog

See [3.1.0-rc1](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc1) for previous changes in 3.1.0, including the explanation of why there are breaking changes.

### Additions

-   Added the `jsonSchemaDialect` top-level field to allow the definition of a default $schema value for Schema Objects.

### Updates

-   Updated some links to more accurate locations.
-   Updates JSON Schema support to the latest [2020-12 draft](https://tools.ietf.org/html/draft-bhutton-json-schema-00).
-   Revamped relative reference resolution under both URIs and URLs.
-   Reworked file upload description to take into account new JSON Schema capabilities. This contains breaking changes.
-   Both `x-oai-` and `x-oas-` prefixes for Specification Extensions are now reserved to be defined by the OpenAPI Initiative.

### Clarifications

-   Path parameter values cannot contain the unescaped characters `/`, `?` or `#`.
-   Further explanation of where Reference Object and JSON Schema's reference should be used.
-   Unified wording when values are URLs/URIs.
-   Reworded Path Item's `$ref` to take into account reference and component changes.
-   Fixed some examples.
-   Minor text changes to improve consistency and readability.
-   The description of the Reference Object has been updated to further clarify its behavior.
-   Further updated Schema Object's description to take into account the latest draft, and the default use of [https://spec.openapis.org/oas/3.1/dialect/base](https://spec.openapis.org/oas/3.1/dialect/base) as the default OAS dialect.
-   Reworded "Schema Vocabularies" to "Schema dialects"

Assets 2

Loading


👍 15 alex-feel, RaphC, VadimKulagin, seralekseenko, buchi-busireddy, brylie, alexted, Saud96525, binbjz, Molkree, and 5 more reacted with thumbs up emoji 🎉 22 roy2220, gwerbin, mcobzarenco, runiq, derekwayne, fenric, dgmike, xpXZAKURAXpq, muraikenta, 1995parham, and 12 more reacted with hooray emoji ❤️ 9 pH-7, xpXZAKURAXpq, UdittLamba, alexted, Saud96525, eugeniocaroccicastoredc, kiryuxabas, mrlubos, and massto reacted with heart emoji 🚀 5 alexted, Saud96525, binbjz, kozi, and kiryuxabas reacted with rocket emoji 👀 3 alexted, Saud96525, and binbjz reacted with eyes emoji

37 people reacted

## OAS 3.1.0-rc1 Released!

[OAS 3.1.0-rc1 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc1) Pre-release

Pre-release

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 09 Oct 01:31

[3.1.0-rc1](https://github.com/OAI/OpenAPI-Specification/tree/3.1.0-rc1)

[`f8449d1`](https://github.com/OAI/OpenAPI-Specification/commit/f8449d1a893cc6a811c6f3d87e88b05761dc5397)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**. The key has expired.

GPG key ID: 4AEE18F83AFDEB23

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

## Changelog

See [3.1.0-rc0](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc0) for previous changes in 3.1.0, including the explanation of why there are breaking changes.

### Breaking changes

-   *Server Variable*'s `enum` now MUST not be empty (changed from SHOULD).
-   *Server Variable*'s `default` now MUST exist in the `enum` values, if such values are defined (changed from SHOULD).
-   `responses` are no longer required to be defined under the *Operation Object*.

### Clarifications

-   It is now clarified when path template expression may not have a corresponding path parameter.
-   Data types (and just primitive data types) now correspond to JSON Schema.
-   Various cosmetic fixes.
-   A new section was added to address how to handle the `$schema` keyword (implicitly and explicitly).

Assets 2

Loading


👍 3 binbjz, massto, and tammynewbie reacted with thumbs up emoji ❤️ 3 binbjz, massto, and tammynewbie reacted with heart emoji

3 people reacted

## OAS 3.1.0-rc0 Released!

[OAS 3.1.0-rc0 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc0) Pre-release

Pre-release

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 18 Jun 23:58

[3.1.0-rc0](https://github.com/OAI/OpenAPI-Specification/tree/3.1.0-rc0)

[`53c50e1`](https://github.com/OAI/OpenAPI-Specification/commit/53c50e159d2ac4e545a029a598a86f747ffe2d33)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**. The key has expired.

GPG key ID: 4AEE18F83AFDEB23

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

## Changelog

As part of this release, we have decided to not follow SemVer anymore, and as such introduce breaking changes. These changes are documented as part of the release notes.

### Additions

-   Introduced a new top-level field - `webhooks`. This allows describing out-of-band webhooks that are available as part of the API.
-   The *Info Object* has a new `summary` field.
-   The *License Object* now has a new `identifier` field for SPDX licenses.
-   *Components Object* now has a new entry `pathItems`, to allow for reusable `Path Item Object`s to be defined within a valid OpenAPI document.

### Extended Functionality

-   Updated primitive types to be based on [JSON Schema Specification Draft 2019-09](http://json-schema.org/draft/2019-09/json-schema-core.html#rfc.section.4.2). This now includes type `null`.
-   Lifted the restriction of allowing *Request Body* only in HTTP methods where the HTTP 1.1 specification [RFC7231](https://tools.ietf.org/html/rfc7231#section-4.3.1) has explicitly defined semantics for. While allowed in other methods, it is not recommended.
-   Added support to `object` `type` for `spaceDelimited` and `pipeDelimited` `style` values.
-   The *Encoding Object* now supports `style`, `explode` and `allowReserved` for `multipart/form-data` media type as well.
-   To enable better `webhooks` support, expressions in the `Callback Object` can now also reference `Path Item Object`s.
-   When using the *Reference Object*, `summary` and `description` fields can now be overridden.
-   The *Schema Object* is now fully compliant with JSON Schema draft 2019-09 (see [JSON Schema Core](https://json-schema.org/draft/2019-09/json-schema-core.html) and [JSON Schema Validation](https://json-schema.org/draft/2019-09/json-schema-validation.html)). See also, `Breaking Changes`
-   The *Discriminator Object* can now be extended with Specification Extensions.
-   Added support for mutual TLS (`mutualTLS`) as a security scheme.
-   Used security requirements can now define an array of roles that are required for execution (and not only scopes for OAuth 2.0 security schemes).

### Changes

-   An OpenAPI Document now requires at least one of `paths`, `components` or `webhooks` to exist at the top level. While previous versions required `paths`, now a valid OpenAPI Document can describe only webhooks, or even only reusable components. Thus, an OpenAPI Document no longer necessarily describes an API.
-   Anywhere in the 3.0.0 Specification that had a type of [Schema Object](https://github.com/OAI/OpenAPI-Specification/releases#schemaObject) | [Reference Object](https://github.com/OAI/OpenAPI-Specification/releases#referenceObject) has been replaced to be [Schema Object](https://github.com/OAI/OpenAPI-Specification/releases#schemaObject) only. With the move to full JSON Schema support, `$ref` is inherently part of the `Schema Object` and has its own defined behavior.
-   Extensions prefixed with `x-oas-` are now reserved for the OpenAPI Initiative.
-   `format` is now not validated by default.

### Breaking changes

-   The specification versioning no longer follows SemVer.
-   The `nullable` keyword has been removed from the `Schema Object` (`null` can be used as a type value).
-   `exclusiveMaximum` and `exclusiveMinimum` cannot accept `boolean` values (following JSON Schema).
-   Due to the compliance with JSON Schema, there is no longer interaction between `required` and `readOnly`/`writeOnly` in relation to requests and responses.
-   `format` (whether `byte`, `binary`, or `base64`) is no longer used to describe file payloads. As part of JSON Schema compliance, now `contentEncoding` and `contentMediaType` can be used for such specification.

### Clarifications

-   Reworded the definition of *OpenAPI Document* to reflect that a document no longer must describe paths, but can describe either paths, webhooks, components or any combination of them.
-   Dropped the term RESTful APIs in favor of HTTP APIs
-   Resolution of relative references has been redefined and clarified. Note there's a difference in resolution between Schema Object References and all others.
-   Modification of examples to improve them and provide context for new fields/objects.

Assets 2

Loading


🚀 2 moritz-baecker-integra and lghiur reacted with rocket emoji

2 people reacted

## OAS 3.0.3 Released!

[OAS 3.0.3 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.3)

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


## OAS 3.0.2 Released!

[OAS 3.0.2 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.2)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 08 Oct 16:31

[3.0.2](https://github.com/OAI/OpenAPI-Specification/tree/3.0.2)

[`98138c7`](https://github.com/OAI/OpenAPI-Specification/commit/98138c7b4c153f780a38907f3472a7a5996692d4)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**. The key has expired.

GPG key ID: 4AEE18F83AFDEB23

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

# OAS 3.0.2 Change Log

The OAI is pleased to announce the official release of the OpenAPI Specification 3.0.2!

As a patch release, the following changes were made to improve the specification in terms of readability and accuracy. None of these modifications change the behavior of the spec.

-   Added clarification to case sensitivity of keys in maps.
-   Reworked the Data Type table, removing the `Common Name` to reduce potential confusion.
-   Clarified the description of the `Server Variable Object`'s `default` field.
-   Fixed various examples.
-   Clarified `operationId` is case sensitive.
-   Clarified the default value of the `Parameter Object`'s `deprecated` field is `false`.
-   Added recommendation to not use the `Parameter Object`'s `allowEmptyValue` field as it will be removed in a future version.
-   Fixed the description of the `Media Type Object`'s `schema` field.
-   Clarified the description of the `Responses Object`'s response codes field description.
-   Clarified that the `Schema Object`'s `additionalProperties` field has a default value of `true`.
-   Fixed a small wording issue in the `Discriminator Object` description.
-   Fixed the `Security Scheme Object` description to include reference to the use of API Keys in cookies.
-   Fixed the description of the `Security Requirement Object`.

Assets 2

Loading


👍 1 Nitika2334 reacted with thumbs up emoji

1 person reacted

## OAS 3.0.1 Released!

[OAS 3.0.1 Released!](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.1)

Compare

# Choose a tag to compare

Filter

[View all tags](https://github.com/OAI/OpenAPI-Specification/tags)

![@webron](https://avatars.githubusercontent.com/u/241629?s=40&v=4) [webron](https://github.com/webron) released this 07 Dec 06:06

[3.0.1](https://github.com/OAI/OpenAPI-Specification/tree/3.0.1)

[`1adcb88`](https://github.com/OAI/OpenAPI-Specification/commit/1adcb8830aab48506b1ffd876330ab8c22820ad6)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**. The key has expired.

GPG key ID: 4AEE18F83AFDEB23

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

# OAS 3.0.1 Change Log

The OAI is pleased to announce the official release of the OpenAPI Specification 3.0.1!

This our first patch release since 3.0.0, containing the following updates:

## Specification Changes

-   Updated document links to HTTPS where applicable.
-   `example` and `examples` fields descriptions were updated to reference them as 'fields' and not 'objects'.
-   Fixed various examples (indentation, field names, comments).
-   Removed the Examples Object as it was left over during editing of v3.0.0. It was not used or referenced to by any other object in the specification.
-   Various typo fixes.

## Additional Changes

-   Clarified the roles and processes in the Technical Steering Committee (TSC, formerly the TDC).
-   Improvements to the development guidelines.

Assets 2

Loading


Previous [1](https://github.com/OAI/OpenAPI-Specification/releases?page=1) [2](https://github.com/OAI/OpenAPI-Specification/releases?page=2) [Next](https://github.com/OAI/OpenAPI-Specification/releases?page=2)

Previous [Next](https://github.com/OAI/OpenAPI-Specification/releases?page=2)
