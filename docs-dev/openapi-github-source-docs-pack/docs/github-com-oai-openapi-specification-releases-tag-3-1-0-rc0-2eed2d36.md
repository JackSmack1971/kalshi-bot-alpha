---
title: "OAS 3.1.0-rc0 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc0"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:24.102Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.1.0-rc0 Released!

Pre-release

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
-   Anywhere in the 3.0.0 Specification that had a type of [Schema Object](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc0#schemaObject) | [Reference Object](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc0#referenceObject) has been replaced to be [Schema Object](https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc0#schemaObject) only. With the move to full JSON Schema support, `$ref` is inherently part of the `Schema Object` and has its own defined behavior.
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
