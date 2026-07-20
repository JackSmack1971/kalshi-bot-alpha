---
title: "OpenAPI Specification"
source_url: "https://spec.openapis.org/oas/"
host: "spec.openapis.org"
depth: 0
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:36:53.760Z"
---
# [](https://spec.openapis.org/oas/#openapi-specification)OpenAPI Specification

## [](https://spec.openapis.org/oas/#specification-versions)Specification Versions

-   **[v3.2.0](https://spec.openapis.org/oas/v3.2.0.html)**
-   **[v3.1.2](https://spec.openapis.org/oas/v3.1.2.html)**, [v3.1.1](https://spec.openapis.org/oas/v3.1.1.html), [v3.1.0](https://spec.openapis.org/oas/v3.1.0.html)
-   **[v3.0.4](https://spec.openapis.org/oas/v3.0.4.html)**, [v3.0.3](https://spec.openapis.org/oas/v3.0.3.html), [v3.0.2](https://spec.openapis.org/oas/v3.0.2.html), [v3.0.1](https://spec.openapis.org/oas/v3.0.1.html), [v3.0.0](https://spec.openapis.org/oas/v3.0.0.html)
-   **[v2.0](https://spec.openapis.org/oas/v2.0.html)**

## [](https://spec.openapis.org/oas/#schema-iterations)Schema Iterations

*Note that while schemas can catch many errors, they are not guaranteed to catch all specification violations. In the event of a disagreement between the schemas and the corresponding specification text, the specification text is presumed to be correct.*

A minor release (e.g. v3.1) has one or more published schemas, identified with the release 3.1 and a revision date like 2021-03-02. All schemas for a given minor release apply to all patch releases within that minor release (e.g. 3.1.0, 3.1.1, 3.1.2, etc.). The dates are purely a way to uniquely identify the revision, and are not intended to be correlated with patch release publication dates. The latest date within a minor release is always the most correct schema for all patch releases, and previous revisions are obsolete.

Note that the v3.1+ `schema/YYYY-MM-DD` schemas do *not* validate the Schema Object, as they make no assumptions about the JSON Schema dialect in use. The v3.1+ `schema-base/YYYY-MM-DD` schemas *do* validate the Schema Object, and require that if `jsonSchemaDialect` or `$schema` are present, that they use the appropriate `dialect/YYYY-MM-DD`. The name `schema-base` comes from the JSON Schema dialect including the OAS extensions being referred to as the “base dialect” in the specification.

See [issue #4147](https://github.com/OAI/OpenAPI-Specification/issues/4147) for discussion of other possible JSON Schema dialect options, [issue #4152](https://github.com/OAI/OpenAPI-Specification/issues/4152) for programmatic access to the latest schemas, and [issue #4141](https://github.com/OAI/OpenAPI-Specification/issues/4141) for discussions on possibly providing linting schemas that could catch likely problems that do not directly violate the specification.

-   **v3.2**
    -   view [**schema/2025-11-23**](https://spec.openapis.org/oas/3.2/schema/2025-11-23.html)
        download iteration: [2025‑11‑23](https://spec.openapis.org/oas/3.2/schema/2025-11-23), [2025‑09‑17](https://spec.openapis.org/oas/3.2/schema/2025-09-17)
    -   view [**schema-base/2025-11-23**](https://spec.openapis.org/oas/3.2/schema-base/2025-11-23.html)
        download iteration: [2025‑11‑23](https://spec.openapis.org/oas/3.2/schema-base/2025-11-23), [2025‑09‑17](https://spec.openapis.org/oas/3.2/schema-base/2025-09-17)
    -   view [**meta/2025-09-17**](https://spec.openapis.org/oas/3.2/meta/2025-09-17.html)
        download iteration: [2025‑09‑17](https://spec.openapis.org/oas/3.2/meta/2025-09-17)
    -   view [**dialect/2025-09-17**](https://spec.openapis.org/oas/3.2/dialect/2025-09-17.html)
        download iteration: [2025‑09‑17](https://spec.openapis.org/oas/3.2/dialect/2025-09-17)
-   **v3.1**
    -   view [**schema/2025-11-23**](https://spec.openapis.org/oas/3.1/schema/2025-11-23.html)
        download iteration: [2025‑11‑23](https://spec.openapis.org/oas/3.1/schema/2025-11-23), [2025‑09‑15](https://spec.openapis.org/oas/3.1/schema/2025-09-15), [2025‑08‑31](https://spec.openapis.org/oas/3.1/schema/2025-08-31), [2025‑02‑13](https://spec.openapis.org/oas/3.1/schema/2025-02-13), [2024‑11‑14](https://spec.openapis.org/oas/3.1/schema/2024-11-14), [2022‑10‑07](https://spec.openapis.org/oas/3.1/schema/2022-10-07), [2022‑02‑27](https://spec.openapis.org/oas/3.1/schema/2022-02-27), [2021‑09‑28](https://spec.openapis.org/oas/3.1/schema/2021-09-28), [2021‑05‑20](https://spec.openapis.org/oas/3.1/schema/2021-05-20), [2021‑04‑15](https://spec.openapis.org/oas/3.1/schema/2021-04-15), [2021‑03‑02](https://spec.openapis.org/oas/3.1/schema/2021-03-02)
    -   view [**schema-base/2025-11-23**](https://spec.openapis.org/oas/3.1/schema-base/2025-11-23.html)
        download iteration: [2025‑11‑23](https://spec.openapis.org/oas/3.1/schema-base/2025-11-23), [2025‑09‑15](https://spec.openapis.org/oas/3.1/schema-base/2025-09-15), [2025‑08‑31](https://spec.openapis.org/oas/3.1/schema-base/2025-08-31), [2025‑02‑13](https://spec.openapis.org/oas/3.1/schema-base/2025-02-13), [2024‑11‑14](https://spec.openapis.org/oas/3.1/schema-base/2024-11-14), [2022‑10‑07](https://spec.openapis.org/oas/3.1/schema-base/2022-10-07), [2022‑02‑27](https://spec.openapis.org/oas/3.1/schema-base/2022-02-27), [2021‑09‑28](https://spec.openapis.org/oas/3.1/schema-base/2021-09-28), [2021‑05‑20](https://spec.openapis.org/oas/3.1/schema-base/2021-05-20), [2021‑04‑15](https://spec.openapis.org/oas/3.1/schema-base/2021-04-15), [2021‑03‑02](https://spec.openapis.org/oas/3.1/schema-base/2021-03-02)
    -   view [**meta/2024-11-10**](https://spec.openapis.org/oas/3.1/meta/2024-11-10.html)
        download iteration: [2024‑11‑10](https://spec.openapis.org/oas/3.1/meta/2024-11-10), [2024‑10‑25](https://spec.openapis.org/oas/3.1/meta/2024-10-25)
    -   view [**dialect/2024-11-10**](https://spec.openapis.org/oas/3.1/dialect/2024-11-10.html)
        download iteration: [2024‑11‑10](https://spec.openapis.org/oas/3.1/dialect/2024-11-10), [2024‑10‑25](https://spec.openapis.org/oas/3.1/dialect/2024-10-25)
-   **v3.0**
    -   view [**schema/2024-10-18**](https://spec.openapis.org/oas/3.0/schema/2024-10-18.html)
        download iteration: [2024‑10‑18](https://spec.openapis.org/oas/3.0/schema/2024-10-18), [2021‑09‑28](https://spec.openapis.org/oas/3.0/schema/2021-09-28)
-   **v2.0**
    -   view [**schema/2017-08-27**](https://spec.openapis.org/oas/2.0/schema/2017-08-27.html)
        download iteration: [2017‑08‑27](https://spec.openapis.org/oas/2.0/schema/2017-08-27)
