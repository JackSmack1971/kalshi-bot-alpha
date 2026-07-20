---
title: "Namespace Registry"
source_url: "https://spec.openapis.org/registry/namespace/index.html"
host: "spec.openapis.org"
depth: 1
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:36:54.450Z"
---
# [](https://spec.openapis.org/registry/namespace/index.html#namespace-registry)Namespace Registry

To allow for creators of OpenAPI descriptions to define new extensions without the risk of name collisions, a namespace registry is maintained by OAI. The namespace registry is a simple list of unique identifiers that are used as part of a prefix for extensions to ensure uniqueness. A prefix has the format `x-{namespace}-` where `{namespace}` is a unique string associated to the creator of the extensions within the namespace. Namespace identifiers MUST be registered as lowercase identifiers.

## [](https://spec.openapis.org/registry/namespace/index.html#contributing)Contributing

Please raise a [Pull-Request](https://github.com/OAI/spec.openapis.org/pulls) and follow the instructions in [`CONTRIBUTING.md`](https://github.com/OAI/spec.openapis.org/blob/main/CONTRIBUTING.md), or open an [Issue](https://github.com/OAI/OpenAPI-Specification/issues) to contribute or discuss a registry value.

## [](https://spec.openapis.org/registry/namespace/index.html#values)Values

| Value | Prefix | Description | Registry |
| --- | --- | --- | --- |
| [fdx](https://spec.openapis.org/registry/namespace/fdx.html) | x-fdx- | Extensions created and used by [Financial Data Exchange (FDX)](https://financialdataexchange.org/) | [Link](https://spec.openapis.org/registry/extension/index.html) |
| [ms](https://spec.openapis.org/registry/namespace/ms.html) | x-ms- | Extensions created and used by Microsoft | [Link](https://github.com/microsoft/OpenAPI/blob/main/extensions/index.md) |
| [oai](https://spec.openapis.org/registry/namespace/oai.html) | x-oai- | Reserved for uses defined by the OAI | [Link](https://spec.openapis.org/registry/extension/index.html) |
| [oas-draft](https://spec.openapis.org/registry/namespace/oas-draft.html) | x-oas-draft- | Extensions created by OAI to indicate proposed changes to the OAS specification | [Link](https://spec.openapis.org/registry/extension/index.html) |
| [oas](https://spec.openapis.org/registry/namespace/oas.html) | x-oas- | Reserved for uses defined by the OAI | [Link](https://spec.openapis.org/registry/extension/index.html) |
| [sap](https://spec.openapis.org/registry/namespace/sap.html) | x-sap- | Extensions created and used by SAP | [Link](https://github.com/SAP/openapi-specification) |
| [scalar](https://spec.openapis.org/registry/namespace/scalar.html) | x-scalar- | Extensions created and used by Scalar | [Link](https://guides.scalar.com/scalar/scalar-api-references/openapi#openapi-specification__custom-specification-extensions) |
