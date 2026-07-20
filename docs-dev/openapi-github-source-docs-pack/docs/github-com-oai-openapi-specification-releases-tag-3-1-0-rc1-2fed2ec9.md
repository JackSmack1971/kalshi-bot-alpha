---
title: "OAS 3.1.0-rc1 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0-rc1"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:23.056Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.1.0-rc1 Released!

Pre-release

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
