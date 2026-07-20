---
title: "OAS 3.1.1 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.1"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:20.214Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.1.1 Released!

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
