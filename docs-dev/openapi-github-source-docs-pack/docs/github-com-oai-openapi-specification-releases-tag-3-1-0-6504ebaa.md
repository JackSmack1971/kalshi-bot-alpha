---
title: "OAS 3.1.0 Released!"
source_url: "https://github.com/OAI/OpenAPI-Specification/releases/tag/3.1.0"
host: "github.com"
depth: 2
selector: "article,main"
fetched_at: "2026-07-17T17:43:22.141Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# OAS 3.1.0 Released!

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
