---
title: "Extensions Registry"
source_url: "https://spec.openapis.org/registry/extension/index.html"
host: "spec.openapis.org"
depth: 1
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:36:54.225Z"
---
# [](https://spec.openapis.org/registry/extension/index.html#extensions-registry)Extensions Registry

## [](https://spec.openapis.org/registry/extension/index.html#master-issue)Master Issue

-   [#1351](https://github.com/OAI/OpenAPI-Specification/issues/1351)

## [](https://spec.openapis.org/registry/extension/index.html#contributing)Contributing

Please raise a [Pull-Request](https://github.com/OAI/spec.openapis.org/pulls) and follow the instructions in [`CONTRIBUTING.md`](https://github.com/OAI/spec.openapis.org/blob/main/CONTRIBUTING.md), or open an [Issue](https://github.com/OAI/OpenAPI-Specification/issues) to contribute or discuss a registry value.

## [](https://spec.openapis.org/registry/extension/index.html#values)Values

| Value | Description | Issue |
| --- | --- | --- |
| [x-agent-trust](https://spec.openapis.org/registry/extension/x-agent-trust.html) | Trust-level metadata block for agent-authenticated security schemes. Required by `apiKey` security schemes that use `Agent-Signature` as the header. Carries algorithm, trust level vocabulary, and JWKS endpoint for local verification. |   |
| [x-codeSamples](https://spec.openapis.org/registry/extension/x-codeSamples.html) | Provides custom code samples for an operation in one or more programming languages. |   |
| [x-jsonschema-$anchor](https://spec.openapis.org/registry/extension/x-jsonschema-$anchor.html) | The JSON Schema $anchor identifier for a schema resource, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-contains](https://spec.openapis.org/registry/extension/x-jsonschema-contains.html) | The JSON Schema contains subschema for array elements, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-contentEncoding](https://spec.openapis.org/registry/extension/x-jsonschema-contentEncoding.html) | The JSON Schema contentEncoding annotation, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-contentMediaType](https://spec.openapis.org/registry/extension/x-jsonschema-contentMediaType.html) | The JSON Schema contentMediaType annotation, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-contentSchema](https://spec.openapis.org/registry/extension/x-jsonschema-contentSchema.html) | The JSON Schema contentSchema subschema for decoded string content, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-dependentSchemas](https://spec.openapis.org/registry/extension/x-jsonschema-dependentSchemas.html) | A map of schemas that apply when corresponding properties are present, used when targeting OpenAPI versions that do not directly support dependentSchemas. |   |
| [x-jsonschema-else](https://spec.openapis.org/registry/extension/x-jsonschema-else.html) | The JSON Schema else conditional subschema, used with x-jsonschema-if when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-if](https://spec.openapis.org/registry/extension/x-jsonschema-if.html) | The JSON Schema if conditional subschema, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-maxContains](https://spec.openapis.org/registry/extension/x-jsonschema-maxContains.html) | The maximum number of array elements that may match contains, used when targeting OpenAPI versions that do not directly support maxContains. |   |
| [x-jsonschema-minContains](https://spec.openapis.org/registry/extension/x-jsonschema-minContains.html) | The minimum number of array elements that must match contains, used when targeting OpenAPI versions that do not directly support minContains. |   |
| [x-jsonschema-patternProperties](https://spec.openapis.org/registry/extension/x-jsonschema-patternProperties.html) | A map of regular expressions to schemas for matching property names, used when targeting OpenAPI versions that do not directly support patternProperties. |   |
| [x-jsonschema-propertyNames](https://spec.openapis.org/registry/extension/x-jsonschema-propertyNames.html) | A schema applied to property names in an object, used when targeting OpenAPI versions that do not directly support propertyNames. |   |
| [x-jsonschema-then](https://spec.openapis.org/registry/extension/x-jsonschema-then.html) | The JSON Schema then conditional subschema, used with x-jsonschema-if when targeting OpenAPI versions that do not directly support it. |   |
| [x-jsonschema-unevaluatedProperties](https://spec.openapis.org/registry/extension/x-jsonschema-unevaluatedProperties.html) | The JSON Schema unevaluatedProperties keyword, used when targeting OpenAPI versions that do not directly support it. |   |
| [x-oai-$self](https://spec.openapis.org/registry/extension/x-oai-$self.html) | The canonical absolute URI for an OpenAPI document, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-additionalOperations](https://spec.openapis.org/registry/extension/x-oai-additionalOperations.html) | Represents non-standard HTTP method operations on a Path Item when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-dataValue](https://spec.openapis.org/registry/extension/x-oai-dataValue.html) | A structured example value for an Example Object, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-deprecated](https://spec.openapis.org/registry/extension/x-oai-deprecated.html) | Indicates that a Security Scheme is deprecated, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-deviceAuthorization](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorization.html) | A device authorization OAuth2 flow, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-deviceAuthorizationUrl](https://spec.openapis.org/registry/extension/x-oai-deviceAuthorizationUrl.html) | The device authorization URL for an OAuth2 flow (RFC 8628), used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-encoding](https://spec.openapis.org/registry/extension/x-oai-encoding.html) | A map of nested encoding definitions for an Encoding Object, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-itemEncoding](https://spec.openapis.org/registry/extension/x-oai-itemEncoding.html) | Encoding properties for individual items in a multipart request part, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-itemSchema](https://spec.openapis.org/registry/extension/x-oai-itemSchema.html) | Schema for individual items in a multipart request part, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-name](https://spec.openapis.org/registry/extension/x-oai-name.html) | An identifier for a Server Object, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-prefixEncoding](https://spec.openapis.org/registry/extension/x-oai-prefixEncoding.html) | Encoding properties applied before the item encoding in a multipart request part, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-serializedValue](https://spec.openapis.org/registry/extension/x-oai-serializedValue.html) | A serialized example value for an Example Object, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-oai-summary](https://spec.openapis.org/registry/extension/x-oai-summary.html) | A short summary for a Response Object, used when targeting OpenAPI versions prior to 3.2. |   |
| [x-twitter](https://spec.openapis.org/registry/extension/x-twitter.html) | Used to hold a reference to the API provider’s Twitter account. |   |
