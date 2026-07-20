---
title: "OAS 3.0.4 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.0.4"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:21.153Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.0.4 Released!

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
