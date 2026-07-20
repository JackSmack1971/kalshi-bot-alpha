---
title: "OpenAPI Specification v3.2.0"
source_url: "https://spec.openapis.org/oas/latest.html"
host: "spec.openapis.org"
depth: 1
selector: "body"
fetched_at: "2026-07-17T17:36:54.564Z"
---
[![OpenAPI Initiative](https://raw.githubusercontent.com/OAI/OpenAPI-Style-Guide/master/graphics/bitmap/OpenAPI_Logo_Pantone.png)](https://openapis.org/)

# OpenAPI Specification v3.2.0

## Version 3.2.0

19 September 2025

More details about this document

This version:

[https://spec.openapis.org/oas/v3.2.0.html](https://spec.openapis.org/oas/v3.2.0.html)

Latest published version:

[https://spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)

Latest editor's draft:

[https://github.com/OAI/OpenAPI-Specification/](https://github.com/OAI/OpenAPI-Specification/)

Editors:

Henry Andrews

Jeremy Whitlock

Karen Etheridge

Lorna Mitchell

Marsh Gardiner

Miguel Quintero

Mike Kistler

Ralf Handl

Vincent Biret

Former editors:

Ron Ratovsky

Darrel Miller

Mike Ralphson

Uri Sarid

Jason Harmon

Tony Tam

Other versions:

[https://spec.openapis.org/oas/v3.1.2.html](https://spec.openapis.org/oas/v3.1.2.html)

[https://spec.openapis.org/oas/v3.1.1.html](https://spec.openapis.org/oas/v3.1.1.html)

[https://spec.openapis.org/oas/v3.1.0.html](https://spec.openapis.org/oas/v3.1.0.html)

[https://spec.openapis.org/oas/v3.0.4.html](https://spec.openapis.org/oas/v3.0.4.html)

[https://spec.openapis.org/oas/v3.0.3.html](https://spec.openapis.org/oas/v3.0.3.html)

[https://spec.openapis.org/oas/v3.0.2.html](https://spec.openapis.org/oas/v3.0.2.html)

[https://spec.openapis.org/oas/v3.0.1.html](https://spec.openapis.org/oas/v3.0.1.html)

[https://spec.openapis.org/oas/v3.0.0.html](https://spec.openapis.org/oas/v3.0.0.html)

[https://spec.openapis.org/oas/v2.0.html](https://spec.openapis.org/oas/v2.0.html)

Participate

[GitHub OAI/OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/)

[File a bug](https://github.com/OAI/OpenAPI-Specification/issues)

[Commit history](https://github.com/OAI/OpenAPI-Specification/commits/main/versions/3.2.0.md)

[Pull requests](https://github.com/OAI/OpenAPI-Specification/pulls)

Copyright © 2025 the Linux Foundation

* * *

## What is the OpenAPI Specification?

The OpenAPI Specification (OAS) defines a standard, programming language-agnostic interface description for HTTP APIs, which allows both humans and computers to discover and understand the capabilities of a service without requiring access to source code, additional documentation, or inspection of network traffic. When properly defined via OpenAPI, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. Similar to what interface descriptions have done for lower-level programming, the OpenAPI Specification removes guesswork in calling a service.

## Status of This Document

The source-of-truth for this specification is the HTML file referenced above as *This version*.

## 1\. OpenAPI Specification

[](https://spec.openapis.org/oas/latest.html#openapi-specification)

### 1.1 Version 3.2.0

[](https://spec.openapis.org/oas/latest.html#conformance)

The key words “*MUST*”, “*MUST NOT*”, “*REQUIRED*”, “*SHALL*”, “*SHALL NOT*”, “*SHOULD*”, “*SHOULD NOT*”, “*RECOMMENDED*”, “*NOT RECOMMENDED*”, “*MAY*”, and “*OPTIONAL*” in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14) \[[RFC2119](https://spec.openapis.org/oas/latest.html#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://spec.openapis.org/oas/latest.html#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

This document is licensed under [The Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

## 2\. Introduction

[](https://spec.openapis.org/oas/latest.html#introduction)

The OpenAPI Specification (OAS) defines a standard, language-agnostic interface to HTTP APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. When properly defined, a consumer can understand and interact with the remote service by [parsing and serializing](https://spec.openapis.org/oas/latest.html#parsing-and-serializing) HTTP messages to and from a [data model](https://spec.openapis.org/oas/latest.html#data-types) with a minimal amount of implementation logic.

An [OpenAPI Description](https://spec.openapis.org/oas/latest.html#openapi-description-structure) (OAD) can then be used by documentation generation tools to display the API, code generation tools to generate servers and clients in various programming languages, testing tools, and many other use cases.

For examples of OpenAPI usage and additional documentation, please visit \[[OpenAPI-Learn](https://spec.openapis.org/oas/latest.html#bib-openapi-learn "OpenAPI - Getting started, and the specification explained")\].

For extension registries and other specifications published by the OpenAPI Initiative, as well as the authoritative rendering of this specification, please visit [spec.openapis.org](https://spec.openapis.org/).

### 2.1 Versions and Deprecation

[](https://spec.openapis.org/oas/latest.html#versions-and-deprecation)

The OpenAPI Specification is versioned using a `major`.`minor`.`patch` versioning scheme. The `major`.`minor` portion of the version string (for example `3.1`) *SHALL* designate the OAS feature set. *`.patch`* versions address errors in, or provide clarifications to, this document, not the feature set. Tooling which supports OAS 3.1 *SHOULD* be compatible with all OAS 3.1.\* versions. The patch version *SHOULD NOT* be considered by tooling, making no distinction between `3.1.0` and `3.1.1` for example.

Certain fields or features may be marked **Deprecated**. These fields and features remain part of the specification and can be used like any other field or feature. However, OpenAPI Description authors should use newer fields and features documented to replace the deprecated ones whenever possible.

At this time, such elements are expected to remain part of the OAS until the next major version, although a future minor version of this specification may define a policy for later removal of deprecated elements.

Occasionally, non-backwards compatible changes may be made in `minor` versions of the OAS where impact is believed to be low relative to the benefit provided.

### 2.2 Undefined and Implementation-Defined Behavior

[](https://spec.openapis.org/oas/latest.html#undefined-and-implementation-defined-behavior)

This specification deems certain situations to have either *undefined* or *implementation-defined* behavior.

Behavior described as *undefined* is likely, at least in some circumstances, to result in outcomes that contradict the specification. This description is used when detecting the contradiction is impossible or impractical. Implementations *MAY* support undefined scenarios for historical reasons, including ambiguous text in prior versions of the specification. This support might produce correct outcomes in many cases, but relying on it is *NOT RECOMMENDED* as there is no guarantee that it will work across all tools or with future specification versions, even if those versions are otherwise strictly compatible with this one.

Behavior described as *implementation-defined* allows implementations to choose which of several different-but-compliant approaches to a requirement to implement. This documents ambiguous requirements that API description authors are *RECOMMENDED* to avoid in order to maximize interoperability. Unlike undefined behavior, it is safe to rely on implementation-defined behavior if *and only if* it can be guaranteed that all relevant tools support the same behavior.

## 3\. Format

[](https://spec.openapis.org/oas/latest.html#format)

An OpenAPI document that conforms to the OpenAPI Specification is itself a JSON object, which may be represented either in [JSON](https://spec.openapis.org/oas/latest.html#bib-rfc8259 "The JavaScript Object Notation (JSON) Data Interchange Format") or [YAML](https://spec.openapis.org/oas/latest.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2") format. Examples in this specification will be shown in YAML for brevity.

All field names in the specification are **case-sensitive**. This includes all fields that are used as keys in a map, except where explicitly noted that keys are **case-insensitive**.

OAS [Objects](https://spec.openapis.org/oas/latest.html#objects-and-fields) expose two types of fields: *fixed fields*, which have a declared name, and *patterned fields*, which have a declared pattern for the field name.

Patterned fields *MUST* have unique names within the containing object.

**Note:** While APIs may be described by OpenAPI Descriptions in either YAML or JSON format, the API request and response bodies and other content are not required to be JSON or YAML.

### 3.1 JSON and YAML Compatibility

[](https://spec.openapis.org/oas/latest.html#json-and-yaml-compatibility)

In order to preserve the ability to round-trip between YAML and JSON formats, [YAML version 1.2](https://spec.openapis.org/oas/latest.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2") is *RECOMMENDED* along with the additional constraints listed in \[[RFC9512](https://spec.openapis.org/oas/latest.html#bib-rfc9512 "YAML Media Type")\] [Section 3.4](https://tools.ietf.org/html/rfc9512#name-yaml-and-json).

The recommendation in previous versions of this specification to restrict YAML to its “JSON” [schema ruleset](https://yaml.org/spec/1.2/spec.html#id2803231) allowed for the inclusion of certain values that (despite the name) cannot be represented in JSON. OAD authors *SHOULD NOT* rely on any such JSON-incompatible YAML values.

### 3.2 Case Sensitivity

[](https://spec.openapis.org/oas/latest.html#case-sensitivity)

As most field names and values in the OpenAPI Specification are case-sensitive, this document endeavors to call out any case-insensitive names and values. However, the case sensitivity of field names and values that map directly to HTTP concepts follow the case sensitivity rules of HTTP, even if this document does not make a note of every concept.

### 3.3 Rich Text Formatting

[](https://spec.openapis.org/oas/latest.html#rich-text-formatting)

Throughout the specification `description` fields are noted as supporting \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] markdown formatting. Where OpenAPI tooling renders rich text it *MUST* support, at a minimum, markdown syntax as described by \[[CommonMark-0.27](https://spec.openapis.org/oas/latest.html#bib-commonmark-0.27 "CommonMark Spec, Version 0.27")\]. Tooling *MAY* choose to ignore some CommonMark or extension features to address security concerns.

While the framing of CommonMark 0.27 as a minimum requirement means that tooling *MAY* choose to implement extensions on top of it, note that any such extensions are by definition implementation-defined and will not be interoperable. OpenAPI Description authors *SHOULD* consider how text using such extensions will be rendered by tools that offer only the minimum support.

## 4\. Objects and Fields

[](https://spec.openapis.org/oas/latest.html#objects-and-fields)

This section describes the structure of the OpenAPI Description format. This text is the only normative description of the format. A JSON Schema is hosted on [spec.openapis.org](https://spec.openapis.org/) for informational purposes. If the JSON Schema differs from this section, then this section *MUST* be considered authoritative.

In the following description, if a field is not explicitly ***REQUIRED*** or described with a *MUST* or *SHALL*, it can be considered *OPTIONAL*.

### 4.1 OpenAPI Object

[](https://spec.openapis.org/oas/latest.html#openapi-object)

This is the root object of the [OpenAPI Description](https://spec.openapis.org/oas/latest.html#openapi-description-structure).

#### 4.1.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields)

In addition to the required fields, at least one of the `components`, `paths`, or `webhooks` fields *MUST* be present.

| Field Name | Type | Description |
| --- | --- | --- |
| openapi | `string` | ***REQUIRED***. This string *MUST* be the [version number](https://spec.openapis.org/oas/latest.html#versions-and-deprecation) of the OpenAPI Specification that the OpenAPI document uses. The `openapi` field *SHOULD* be used by tooling to interpret the OpenAPI document. This is *not* related to the [`info.version`](https://spec.openapis.org/oas/latest.html#info-version) string, which describes the OpenAPI document’s version. |
| $self | `string` | This string *MUST* be in the form of a URI reference as defined by \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.1](https://tools.ietf.org/html/rfc3986#section-4.1). The `$self` field provides the self-assigned URI of this document, which also serves as its base URI in accordance with \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.1](https://tools.ietf.org/html/rfc3986#section-5.1.1). Implementations *MUST* support identifying the targets of [API description URIs](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris) using the URI defined by this field when it is present. See [Establishing the Base URI](https://spec.openapis.org/oas/latest.html#establishing-the-base-uri) for the base URI behavior when `$self` is absent or relative, and see [Appendix F](https://spec.openapis.org/oas/latest.html#appendix-f-examples-of-base-uri-determination-and-reference-resolution) for examples of using `$self` to resolve references. |
| info | [Info Object](https://spec.openapis.org/oas/latest.html#info-object) | ***REQUIRED***. Provides metadata about the API. The metadata *MAY* be used by tooling as required. |
| jsonSchemaDialect | `string` | The default value for the `$schema` keyword within [Schema Objects](https://spec.openapis.org/oas/latest.html#schema-object) contained within this OAS document. This *MUST* be in the form of a URI. |
| servers | \[[Server Object](https://spec.openapis.org/oas/latest.html#server-object)\] | An array of Server Objects, which provide connectivity information to a target server. If the `servers` field is not provided, or is an empty array, the default value would be an array consisting of a single [Server Object](https://spec.openapis.org/oas/latest.html#server-object) with a [url](https://spec.openapis.org/oas/latest.html#server-url) value of `/`. |
| paths | [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object) | The available paths and operations for the API. |
| webhooks | Map\[`string`, [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object)\] | The incoming webhooks that *MAY* be received as part of this API and that the API consumer *MAY* choose to implement. Closely related to the `callbacks` feature, this section describes requests initiated other than by an API call, for example by an out of band registration. The key name is a unique string to refer to each webhook, while the (optionally referenced) Path Item Object describes a request that may be initiated by the API provider and the expected responses. An [example](https://learn.openapis.org/examples/v3.1/webhook-example.html) is available. |
| components | [Components Object](https://spec.openapis.org/oas/latest.html#components-object) | An element to hold various Objects for the OpenAPI Description. |
| security | \[[Security Requirement Object](https://spec.openapis.org/oas/latest.html#security-requirement-object)\] | A declaration of which security mechanisms can be used across the API. The list of values includes alternative Security Requirement Objects that can be used. Only one of the Security Requirement Objects need to be satisfied to authorize a request. Individual operations can override this definition. The list can be incomplete, up to being empty or absent. To make security explicitly optional, an empty security requirement (`{}`) can be included in the array. |
| tags | \[[Tag Object](https://spec.openapis.org/oas/latest.html#tag-object)\] | A list of tags used by the OpenAPI Description with additional metadata. The order of the tags can be used to reflect on their order by the parsing tools. Not all tags that are used by the [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) must be declared. The tags that are not declared *MAY* be organized randomly or based on the tools’ logic. Each tag name in the list *MUST* be unique. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/latest.html#external-documentation-object) | Additional external documentation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

To ensure interoperability, references *MUST* use the target document’s `$self` URI if the `$self` field is present. Implementations *MAY* choose to support referencing by other URIs such as the retrieval URI even when `$self` is present, however this behavior is not interoperable and relying on it is *NOT RECOMMENDED*.

#### 4.1.2 OpenAPI Description Structure

[](https://spec.openapis.org/oas/latest.html#openapi-description-structure)

An **OpenAPI Description** (**OAD**) formally describes the surface of an API and its semantics. An OAD *MAY* be made up of a single document, or be distributed across multiple documents that are connected by various fields using [URI references](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris) and [implicit connections](https://spec.openapis.org/oas/latest.html#resolving-implicit-connections).

In order for parsing behavior to be well-defined, all documents in an OAD *MUST* have either an OpenAPI Object or a Schema Object at the root, and *MUST* be parsed as complete documents, as described in the next section.

Documents with a different Object at the root, or that mix OAD content with other content, *MAY* be supported, but will have implementation-defined or, potentially, undefined behavior as described in [Appendix G: Parsing and Resolution Guidance](https://spec.openapis.org/oas/latest.html#appendix-g-parsing-and-resolution-guidance). Throughout this specification, documents are assumed to have either an OpenAPI Object or Schema Object at the root unless otherwise specified.

In a multi-document OAD, the document containing the OpenAPI Object where parsing begins is known as that OAD’s **entry document**. It is *RECOMMENDED* that the entry document of an OAD be named `openapi.json` or `openapi.yaml`.

An OpenAPI Object *MAY* be embedded in another format, called the **embedding format**, just as JSON Schema is embedded in the OAS in the form of Schema Objects. It is the responsibility of an embedding format to define how to parse embedded content, and OAS implementations that do not document support for an embedding format cannot be expected to parse embedded OAS content correctly.

##### 4.1.2.1 Parsing Documents

[](https://spec.openapis.org/oas/latest.html#parsing-documents)

Each document in an OAD *MUST* be fully parsed in order to locate possible reference targets. This includes the parsing requirements of [JSON Schema Specification Draft 2020-12](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-9), with appropriate modifications regarding base URIs as specified in [Relative References In URIs](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris). Reference targets are defined by fields including the OpenAPI Object’s [`$self`](https://spec.openapis.org/oas/latest.html#oas-self) field and the [Schema Object’s](https://spec.openapis.org/oas/latest.html#schema-object) `$id`, `$anchor`, and `$dynamicAnchor` keywords.

Implementations *MUST NOT* treat a reference as unresolvable before completely parsing all documents provided to the implementation as possible parts of the OAD.

If only the referenced part of the document is parsed when resolving a reference, the resulting behavior can be implementation-defined or undefined; see [Warnings Regarding Fragmentary Parsing](https://spec.openapis.org/oas/latest.html#warnings-regarding-fragmentary-parsing) in [Appendix G](https://spec.openapis.org/oas/latest.html#appendix-g-parsing-and-resolution-guidance) for details.

##### 4.1.2.2 Relative References in API Description URIs

[](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris)

URIs used as references within an OpenAPI Description, or to external documentation or other supplementary information such as a license, are resolved as *identifiers*, and described by this specification as ***URIs***, in contrast with [API URLs](https://spec.openapis.org/oas/latest.html#relative-references-in-api-urls). Note that some URI fields are named `url` for historical reasons, but the descriptive text for those fields uses the correct “URI” terminology.

As noted under [Parsing Documents](https://spec.openapis.org/oas/latest.html#parsing-documents), several fields can be used to associate an OpenAPI document or a Schema Object with a URI, which might not match the document’s or schema’s location. This allows the same references to be used in different deployment environments, including local filesystems or networks restricted by security policies or connectivity limitations.

Unless specified otherwise, all fields that are URIs *MAY* be relative references as defined by \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://tools.ietf.org/html/rfc3986#section-4.2).

###### 4.1.2.2.1 Establishing the Base URI

[](https://spec.openapis.org/oas/latest.html#establishing-the-base-uri)

Relative URI references are resolved using the appropriate base URI, which *MUST* be determined in accordance with \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.1 – 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.1) and, for Schema objects, [JSON Schema draft 2020-12 Section 8.2](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-8.2), as illustrated by the examples in [Appendix F: Examples of Base URI Determination and Reference Resolution](https://spec.openapis.org/oas/latest.html#appendix-f-examples-of-base-uri-determination-and-reference-resolution).

If `$self` is a relative URI reference, it is resolved against the next possible base URI source (\[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.2 – 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.2)) before being used for the resolution of other relative URI references.

The most common base URI source that is used in the event of a missing or relative `$self` (in the [OpenAPI Object](https://spec.openapis.org/oas/latest.html#openapi-object)) and (for [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object)) `$id` is the retrieval URI. Implementations *MAY* support document retrieval, although see the [Security Considerations](https://spec.openapis.org/oas/latest.html#security-considerations) sections for additional guidance. Even if retrieval is supported, it may be impossible due to network configuration or server unavailability (including the server hosting an older version while a new version is in development), or undesirable due to performance impacts. Therefore, all implementations *SHOULD* allow users to provide documents with their intended retrieval URIs so that references can be resolved as if retrievals were performed.

###### 4.1.2.2.2 Resolving URI fragments

[](https://spec.openapis.org/oas/latest.html#resolving-uri-fragments)

If a URI contains a fragment identifier, then the fragment should be resolved per the fragment resolution mechanism of the referenced document. If the representation of the referenced document is JSON or YAML, then the fragment identifier *SHOULD* be interpreted as a JSON Pointer as per \[[RFC6901](https://spec.openapis.org/oas/latest.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\].

###### 4.1.2.2.3 Relative URI References in CommonMark Fields

[](https://spec.openapis.org/oas/latest.html#relative-uri-references-in-commonmark-fields)

Relative references in CommonMark hyperlinks are resolved in their rendered context, which might differ from the context of the API description.

##### 4.1.2.3 Resolving Implicit Connections

[](https://spec.openapis.org/oas/latest.html#resolving-implicit-connections)

Several features of this specification require resolution of non-URI-based connections to some other part of the OpenAPI Description (OAD).

These connections are unambiguously resolved in single-document OADs, but the resolution process in multi-document OADs is *implementation-defined*, within the constraints described in this section. In some cases, an unambiguous URI-based alternative is available, and OAD authors are *RECOMMENDED* to use the alternative to maximize interoperability.

For resolving [Components Object](https://spec.openapis.org/oas/latest.html#components-object) and [Tag Object](https://spec.openapis.org/oas/latest.html#tag-object) names from a referenced (non-entry) document, it is *RECOMMENDED* that tools resolve from the entry document, rather than the current document. For resolving an [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) based on an `operationId`, it is *RECOMMENDED* to consider all Operation Objects from all parsed documents.

Note that no aspect of implicit connection resolution changes how [URIs are resolved](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris), or restricts their possible targets.

See [Appendix G: Parsing and Resolution Guidance](https://spec.openapis.org/oas/latest.html#appendix-g-parsing-and-resolution-guidance) for more details, including a list of Objects and fields using implicit connections.

### 4.2 Info Object

[](https://spec.openapis.org/oas/latest.html#info-object)

The object provides metadata about the API. The metadata *MAY* be used by the clients if needed, and *MAY* be presented in editing or documentation generation tools for convenience.

#### 4.2.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-0)

| Field Name | Type | Description |
| --- | --- | --- |
| title | `string` | ***REQUIRED***. The title of the API. |
| summary | `string` | A short summary of the API. |
| description | `string` | A description of the API. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| termsOfService | `string` | A URI for the Terms of Service for the API. This *MUST* be in the form of a URI. |
| contact | [Contact Object](https://spec.openapis.org/oas/latest.html#contact-object) | The contact information for the exposed API. |
| license | [License Object](https://spec.openapis.org/oas/latest.html#license-object) | The license information for the exposed API. |
| version | `string` | ***REQUIRED***. The version of the OpenAPI document (which is distinct from the [OpenAPI Specification version](https://spec.openapis.org/oas/latest.html#oas-version) or the version of the API being described or the version of the OpenAPI Description). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.2.2 Info Object Example

[](https://spec.openapis.org/oas/latest.html#info-object-example)

```
title: Example Pet Store App
summary: A pet store manager.
description: This is an example server for a pet store.
termsOfService: https://example.com/terms/
contact:
  name: API Support
  url: https://www.example.com/support
  email: support@example.com
license:
  name: Apache 2.0
  url: https://www.apache.org/licenses/LICENSE-2.0.html
version: 1.0.1
```

### 4.3 Contact Object

[](https://spec.openapis.org/oas/latest.html#contact-object)

Contact information for the exposed API.

#### 4.3.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-1)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | The identifying name of the contact person/organization. |
| url | `string` | The URI for the contact information. This *MUST* be in the form of a URI. |
| email | `string` | The email address of the contact person/organization. This *MUST* be in the form of an email address. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.3.2 Contact Object Example

[](https://spec.openapis.org/oas/latest.html#contact-object-example)

```
name: API Support
url: https://www.example.com/support
email: support@example.com
```

### 4.4 License Object

[](https://spec.openapis.org/oas/latest.html#license-object)

License information for the exposed API.

#### 4.4.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-2)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The license name used for the API. |
| identifier | `string` | An \[[SPDX-Licenses](https://spec.openapis.org/oas/latest.html#bib-spdx-licenses "SPDX License List")\] expression for the API. The `identifier` field is mutually exclusive of the `url` field. |
| url | `string` | A URI for the license used for the API. This *MUST* be in the form of a URI. The `url` field is mutually exclusive of the `identifier` field. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.4.2 License Object Example

[](https://spec.openapis.org/oas/latest.html#license-object-example)

```
name: Apache 2.0
identifier: Apache-2.0
```

### 4.5 Server Object

[](https://spec.openapis.org/oas/latest.html#server-object)

An object representing a Server.

#### 4.5.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-3)

| Field Name | Type | Description |
| --- | --- | --- |
| url | `string` | ***REQUIRED***. A URL to the target host. This URL supports Server Variables and *MAY* be relative, to indicate that the host location is relative to the location where the document containing the Server Object is being served. Query and fragment *MUST NOT* be part of this URL. Variable substitutions will be made when a variable is named in `{`braces`}`. |
| description | `string` | An optional string describing the host designated by the URL. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| name | `string` | An optional unique string to refer to the host designated by the URL. |
| variables | Map\[`string`, [Server Variable Object](https://spec.openapis.org/oas/latest.html#server-variable-object)\] | A map between a variable name and its value. The value is used for substitution in the server’s URL template. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.5.2 Relative References in API URLs

[](https://spec.openapis.org/oas/latest.html#relative-references-in-api-urls)

API endpoints are by definition accessed as locations, and are described by this specification as ***URLs***.

Unless specified otherwise, all fields that are URLs *MAY* be relative references as defined by \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://datatracker.ietf.org/doc/html/rfc3986#section-4.2).

Because the API is a distinct entity from the OpenAPI document, RFC3986’s base URI rules for the OpenAPI document do not apply. Unless specified otherwise, relative references are resolved using the URLs defined in the [Server Object](https://spec.openapis.org/oas/latest.html#server-object) as a base URL. Note that these themselves *MAY* be relative to the referring document.

##### 4.5.2.1 Examples of API Base URL Determination

[](https://spec.openapis.org/oas/latest.html#examples-of-api-base-url-determination)

Assume a retrieval URI of `https://device1.example.com` for the following OpenAPI document:

```
openapi: 3.2.0
$self: https://apidescriptions.example.com/foo
info:
  title: Example API
  version: 1.0
servers:
- url: .
  description: The production API on this device
- url: ./test
  description: The test API on this device
```

For API URLs the `$self` field, which identifies the OpenAPI document, is ignored and the retrieval URI is used instead. This produces a normalized production URL of `https://device1.example.com`, and a normalized test URL of `https://device1.example.com/test`.

#### 4.5.3 Server Object Example

[](https://spec.openapis.org/oas/latest.html#server-object-example)

A single server would be described as:

```
url: https://development.gigantic-server.com/v1
description: Development server
name: dev
```

The following shows how multiple servers can be described, for example, at the OpenAPI Object’s [`servers`](https://spec.openapis.org/oas/latest.html#oas-servers):

```
servers:
  - url: https://development.gigantic-server.com/v1
    description: Development server
    name: dev
  - url: https://staging.gigantic-server.com/v1
    description: Staging server
    name: staging
  - url: https://api.gigantic-server.com/v1
    description: Production server
    name: prod
```

The following shows how variables can be used for a server configuration:

```
servers:
  - url: https://{username}.gigantic-server.com:{port}/{basePath}
    description: The production API server
    name: prod
    variables:
      username:
        # note! no enum here means it is an open value
        default: demo
        description: A user-specific subdomain. Use `demo` for a free sandbox environment.
      port:
        enum:
          - '8443'
          - '443'
        default: '8443'
      basePath:
        # open meaning there is the opportunity to use special base paths as assigned by the provider, default is "v2"
        default: v2
```

### 4.6 Server Variable Object

[](https://spec.openapis.org/oas/latest.html#server-variable-object)

An object representing a Server Variable for server URL template substitution.

The server URL templating is defined by the following \[[ABNF](https://spec.openapis.org/oas/latest.html#bib-abnf "Augmented BNF for Syntax Specifications: ABNF")\] syntax.

```
server-url-template  = 1*( literals / server-variable )
server-variable      = "{" server-variable-name "}"
server-variable-name = 1*( %x00-7A / %x7C / %x7E-10FFFF ) ; every Unicode character except { and }

literals       = 1*( %x21 / %x23-24 / %x26-3B / %x3D / %x3F-5B
               / %x5D / %x5F / %x61-7A / %x7E / ucschar / iprivate
               / pct-encoded)
                    ; any Unicode character except: CTL, SP,
                    ;  DQUOTE, "%" (aside from pct-encoded),
                    ;  "<", ">", "\", "^", "`", "{", "|", "}"
pct-encoded    =  "%" HEXDIG HEXDIG
ucschar        =  %xA0-D7FF / %xF900-FDCF / %xFDF0-FFEF
               /  %x10000-1FFFD / %x20000-2FFFD / %x30000-3FFFD
               /  %x40000-4FFFD / %x50000-5FFFD / %x60000-6FFFD
               /  %x70000-7FFFD / %x80000-8FFFD / %x90000-9FFFD
               /  %xA0000-AFFFD / %xB0000-BFFFD / %xC0000-CFFFD
               /  %xD0000-DFFFD / %xE1000-EFFFD
iprivate       =  %xE000-F8FF / %xF0000-FFFFD / %x100000-10FFFD
```

Here, `literals`, `pct-encoded`, `ucschar` and `iprivate` definitions are taken from \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\], incorporating the corrections specified in [Errata 6937](https://www.rfc-editor.org/errata/eid6937) for `literals`.

Each server variable *MUST NOT* appear more than once in the URL template.

See the [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object) for guidance on constructing full request URLs.

#### 4.6.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-4)

| Field Name | Type | Description |
| --- | --- | --- |
| enum | \[`string`\] | An enumeration of string values to be used if the substitution options are from a limited set. The array *MUST NOT* be empty. |
| default | `string` | ***REQUIRED***. The default value to use for substitution, which *SHALL* be sent if an alternate value is *not* supplied. If the [`enum`](https://spec.openapis.org/oas/latest.html#server-variable-enum) is defined, the value *MUST* exist in the enum’s values. Note that this behavior is different from the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object)’s `default` keyword, which documents the receiver’s behavior rather than inserting the value into the data. |
| description | `string` | An optional description for the server variable. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

### 4.7 Components Object

[](https://spec.openapis.org/oas/latest.html#components-object)

Holds a set of reusable objects for different aspects of the OAS. All objects defined within the Components Object will have no effect on the API unless they are explicitly referenced from outside the Components Object.

#### 4.7.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-5)

| Field Name | Type | Description |
| --- | --- | --- |
| schemas | Map\[`string`, [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object)\] | An object to hold reusable [Schema Objects](https://spec.openapis.org/oas/latest.html#schema-object). |
| responses | Map\[`string`, [Response Object](https://spec.openapis.org/oas/latest.html#response-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Response Objects](https://spec.openapis.org/oas/latest.html#response-object). |
| parameters | Map\[`string`, [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Parameter Objects](https://spec.openapis.org/oas/latest.html#parameter-object). |
| examples | Map\[`string`, [Example Object](https://spec.openapis.org/oas/latest.html#example-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Example Objects](https://spec.openapis.org/oas/latest.html#example-object). |
| requestBodies | Map\[`string`, [Request Body Object](https://spec.openapis.org/oas/latest.html#request-body-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Request Body Objects](https://spec.openapis.org/oas/latest.html#request-body-object). |
| headers | Map\[`string`, [Header Object](https://spec.openapis.org/oas/latest.html#header-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Header Objects](https://spec.openapis.org/oas/latest.html#header-object). |
| securitySchemes | Map\[`string`, [Security Scheme Object](https://spec.openapis.org/oas/latest.html#security-scheme-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Security Scheme Objects](https://spec.openapis.org/oas/latest.html#security-scheme-object). |
| links | Map\[`string`, [Link Object](https://spec.openapis.org/oas/latest.html#link-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Link Objects](https://spec.openapis.org/oas/latest.html#link-object). |
| callbacks | Map\[`string`, [Callback Object](https://spec.openapis.org/oas/latest.html#callback-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Callback Objects](https://spec.openapis.org/oas/latest.html#callback-object). |
| pathItems | Map\[`string`, [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object)\] | An object to hold reusable [Path Item Objects](https://spec.openapis.org/oas/latest.html#path-item-object). |
| mediaTypes | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | An object to hold reusable [Media Type Objects](https://spec.openapis.org/oas/latest.html#media-type-object). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

All the fixed fields declared above are objects that *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`.

Field Name Examples:

```
User
User_1
User_Name
user-name
my.org.User
```

#### 4.7.2 Components Object Example

[](https://spec.openapis.org/oas/latest.html#components-object-example)

```
components:
  schemas:
    GeneralError:
      type: object
      properties:
        code:
          type: integer
          format: int32
        message:
          type: string
    Category:
      type: object
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
    Tag:
      type: object
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
  parameters:
    skipParam:
      name: skip
      in: query
      description: number of items to skip
      required: true
      schema:
        type: integer
        format: int32
    limitParam:
      name: limit
      in: query
      description: max records to return
      required: true
      schema:
        type: integer
        format: int32
  responses:
    NotFound:
      description: Entity not found.
    IllegalInput:
      description: Illegal input for operation.
    GeneralError:
      description: General Error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/GeneralError'
  securitySchemes:
    api_key:
      type: apiKey
      name: api-key
      in: header
    petstore_auth:
      type: oauth2
      flows:
        implicit:
          authorizationUrl: https://example.org/api/oauth/dialog
          scopes:
            write:pets: modify pets in your account
            read:pets: read your pets
```

### 4.8 Paths Object

[](https://spec.openapis.org/oas/latest.html#paths-object)

Holds the relative paths to the individual endpoints and their operations. The path is appended to the URL from the [Server Object](https://spec.openapis.org/oas/latest.html#server-object) in order to construct the full URL. The Paths Object *MAY* be empty, due to [Access Control List (ACL) constraints](https://spec.openapis.org/oas/latest.html#security-filtering).

#### 4.8.1 Patterned Fields

[](https://spec.openapis.org/oas/latest.html#patterned-fields)

| Field Pattern | Type | Description |
| --- | --- | --- |
| /{path} | [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object) | A relative path to an individual endpoint. The field name *MUST* begin with a forward slash (`/`). The URL from the [Server Object](https://spec.openapis.org/oas/latest.html#server-object)’s `url` field, resolved and with template variables substituted, has the path **appended** (no relative URL resolution) to it in order to construct the full URL. [Path templating](https://spec.openapis.org/oas/latest.html#path-templating) is allowed. When matching URLs, concrete (non-templated) paths would be matched before their templated counterparts. Templated paths with the same hierarchy but different templated names *MUST NOT* exist as they are identical. In case of ambiguous matching, it’s up to the tooling to decide which one to use. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.8.2 Path Templating

[](https://spec.openapis.org/oas/latest.html#path-templating)

Path templating refers to the usage of template expressions, delimited by curly braces (`{}`), to mark a section of a URL path as replaceable using path parameters.

Each template expression in the path *MUST* correspond to a path parameter that is included in the [Path Item](https://spec.openapis.org/oas/latest.html#path-item-object) itself and/or in each of the Path Item’s [Operations](https://spec.openapis.org/oas/latest.html#operation-object). An exception is if the path item is empty, for example due to ACL constraints, matching path parameters are not required.

The value for these path parameters *MUST NOT* contain any unescaped “generic syntax” characters described by \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 3](https://datatracker.ietf.org/doc/html/rfc3986#section-3): forward slashes (`/`), question marks (`?`), or hashes (`#`). See [URL Percent-Encoding](https://spec.openapis.org/oas/latest.html#url-percent-encoding) for additional guidance on escaping characters.

The path templating is defined by the following \[[ABNF](https://spec.openapis.org/oas/latest.html#bib-abnf "Augmented BNF for Syntax Specifications: ABNF")\] syntax

```
path-template                  = "/" *( path-segment "/" ) [ path-segment ]
path-segment                   = 1*( path-literal / template-expression )
path-literal                   = 1*pchar
template-expression            = "{" template-expression-param-name "}"
template-expression-param-name = 1*( %x00-7A / %x7C / %x7E-10FFFF ) ; every Unicode character except { and }

pchar               = unreserved / pct-encoded / sub-delims / ":" / "@"
unreserved          = ALPHA / DIGIT / "-" / "." / "_" / "~"
pct-encoded         = "%" HEXDIG HEXDIG
sub-delims          = "!" / "$" / "&" / "'" / "(" / ")"
                    / "*" / "+" / "," / ";" / "="
```

Here, `pchar`, `unreserved`, `pct-encoded` and `sub-delims` definitions are taken from \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\]. The `path-template` is directly derived from [RFC 3986, section 3.3](https://tools.ietf.org/html/rfc3986#section-3.3).

Each template expression *MUST NOT* appear more than once in a single path template.

See also [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

##### 4.8.2.1 Path Templating Matching

[](https://spec.openapis.org/oas/latest.html#path-templating-matching)

Assuming the following paths, the concrete definition, `/pets/mine`, will be matched first if used:

```
  /pets/{petId}
  /pets/mine
```

The following paths are considered identical and invalid:

```
  /pets/{petId}
  /pets/{name}
```

The following may lead to ambiguous resolution:

```
  /{entity}/me
  /books/{id}
```

#### 4.8.3 Paths Object Example

[](https://spec.openapis.org/oas/latest.html#paths-object-example)

```
/pets:
  get:
    description: Returns all pets from the system that the user has access to
    responses:
      '200':
        description: A list of pets.
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/pet'
```

### 4.9 Path Item Object

[](https://spec.openapis.org/oas/latest.html#path-item-object)

Describes the operations available on a single path. A Path Item *MAY* be empty, due to [ACL constraints](https://spec.openapis.org/oas/latest.html#security-filtering). The path itself is still exposed to the documentation viewer but they will not know which operations and parameters are available.

#### 4.9.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-6)

| Field Name | Type | Description |
| --- | --- | --- |
| $ref | `string` | Allows for a referenced definition of this path item. The value *MUST* be in the form of a URI, and the referenced structure *MUST* be in the form of a [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object). In case a Path Item Object field appears both in the defined object and the referenced object, the behavior is undefined. See the rules for resolving [Relative References](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris).

***Note:** The behavior of `$ref` with adjacent properties is likely to change in future versions of this specification to bring it into closer alignment with the behavior of the [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object).* |
| summary | `string` | An optional string summary, intended to apply to all operations in this path. |
| description | `string` | An optional string description, intended to apply to all operations in this path. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| get | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a GET operation on this path. |
| put | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a PUT operation on this path. |
| post | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a POST operation on this path. |
| delete | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a DELETE operation on this path. |
| options | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a OPTIONS operation on this path. |
| head | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a HEAD operation on this path. |
| patch | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a PATCH operation on this path. |
| trace | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a TRACE operation on this path. |
| query | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) | A definition of a QUERY operation, as defined in the most recent IETF draft ([draft-ietf-httpbis-safe-method-w-body-08](https://www.ietf.org/archive/id/draft-ietf-httpbis-safe-method-w-body-11.html) as of this writing) or its RFC successor, on this path. |
| additionalOperations | Map\[`string`, [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object)\] | A map of additional operations on this path. The map key is the HTTP method with the same capitalization that is to be sent in the request. This map *MUST NOT* contain any entry for the methods that can be defined by other fixed fields with Operation Object values (e.g. no `POST` entry, as the `post` field is used for this method). |
| servers | \[[Server Object](https://spec.openapis.org/oas/latest.html#server-object)\] | An alternative `servers` array to service all operations in this path. If a `servers` array is specified at the [OpenAPI Object](https://spec.openapis.org/oas/latest.html#oas-servers) level, it will be overridden by this value. |
| parameters | \[[Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the operation level, but cannot be removed there. The list *MUST NOT* include duplicated parameters. A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/latest.html#parameter-name) and [location](https://spec.openapis.org/oas/latest.html#parameter-in). The list can use the [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object) to link to parameters that are defined in the [OpenAPI Object’s `components.parameters`](https://spec.openapis.org/oas/latest.html#components-parameters). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.9.2 Path Item Object Example

[](https://spec.openapis.org/oas/latest.html#path-item-object-example)

```
get:
  description: Returns pets based on ID
  summary: Find pets by ID
  operationId: getPetsById
  responses:
    '200':
      description: pet response
      content:
        '*/*':
          schema:
            type: array
            items:
              $ref: '#/components/schemas/Pet'
    default:
      description: error payload
      content:
        text/html:
          schema:
            $ref: '#/components/schemas/ErrorModel'
parameters:
  - name: id
    in: path
    description: ID of pet to use
    required: true
    schema:
      type: array
      items:
        type: string
    style: simple
additionalOperations:
  COPY:
    description: Copies pet information based on ID
    summary: Copies pets by ID
    operationId: copyPetsById
    responses:
      '200':
        description: pet response
        content:
          '*/*':
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Pet'
      default:
        description: error payload
        content:
          text/html:
            schema:
              $ref: '#/components/schemas/ErrorModel'
```

### 4.10 Operation Object

[](https://spec.openapis.org/oas/latest.html#operation-object)

Describes a single API operation on a path.

#### 4.10.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-7)

| Field Name | Type | Description |
| --- | --- | --- |
| tags | \[`string`\] | A list of tags for API documentation control. Tags can be used for logical grouping of operations by resources or any other qualifier. |
| summary | `string` | A short summary of what the operation does. |
| description | `string` | A verbose explanation of the operation behavior. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/latest.html#external-documentation-object) | Additional external documentation for this operation. |
| operationId | `string` | Unique string used to identify the operation. The id *MUST* be unique among all operations described in the API. The operationId value is **case-sensitive**. Tools and libraries *MAY* use the operationId to uniquely identify an operation, therefore, it is *RECOMMENDED* to follow common programming naming conventions. |
| parameters | \[[Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A list of parameters that are applicable for this operation. If a parameter is already defined at the [Path Item](https://spec.openapis.org/oas/latest.html#path-item-parameters), the new definition will override it but can never remove it. The list *MUST NOT* include duplicated parameters. A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/latest.html#parameter-name) and [location](https://spec.openapis.org/oas/latest.html#parameter-in). The list can use the [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object) to link to parameters that are defined in the [OpenAPI Object’s `components.parameters`](https://spec.openapis.org/oas/latest.html#components-parameters). |
| requestBody | [Request Body Object](https://spec.openapis.org/oas/latest.html#request-body-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object) | The request body applicable for this operation. The `requestBody` is fully supported in HTTP methods where the HTTP specification \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 9.3](https://datatracker.ietf.org/doc/html/rfc9110#section-9.3) has explicitly defined semantics for request bodies. In other cases where the HTTP spec discourages message content (such as [GET](https://tools.ietf.org/html/rfc9110#section-9.3.1) and [DELETE](https://tools.ietf.org/html/rfc9110#section-9.3.5)), `requestBody` is permitted but does not have well-defined semantics and *SHOULD* be avoided if possible. |
| responses | [Responses Object](https://spec.openapis.org/oas/latest.html#responses-object) | The list of possible responses as they are returned from executing this operation. |
| callbacks | Map\[`string`, [Callback Object](https://spec.openapis.org/oas/latest.html#callback-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A map of possible out-of band callbacks related to the parent operation. The key is a unique identifier for the Callback Object. Each value in the map is a [Callback Object](https://spec.openapis.org/oas/latest.html#callback-object) that describes a request that may be initiated by the API provider and the expected responses. |
| deprecated | `boolean` | Declares this operation to be deprecated. Consumers *SHOULD* refrain from usage of the declared operation. Default value is `false`. |
| security | \[[Security Requirement Object](https://spec.openapis.org/oas/latest.html#security-requirement-object)\] | A declaration of which security mechanisms can be used for this operation. The list of values includes alternative Security Requirement Objects that can be used. Only one of the Security Requirement Objects need to be satisfied to authorize a request. To make security optional, an empty security requirement (`{}`) can be included in the array. This definition overrides any declared top-level [`security`](https://spec.openapis.org/oas/latest.html#oas-security). To remove a top-level security declaration, an empty array can be used. |
| servers | \[[Server Object](https://spec.openapis.org/oas/latest.html#server-object)\] | An alternative `servers` array to service this operation. If a `servers` array is specified at the [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-servers) or [OpenAPI Object](https://spec.openapis.org/oas/latest.html#oas-servers) level, it will be overridden by this value. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.10.2 Operation Object Example

[](https://spec.openapis.org/oas/latest.html#operation-object-example)

```
tags:
  - pet
summary: Updates a pet in the store with form data
operationId: updatePetWithForm
parameters:
  - name: petId
    in: path
    description: ID of pet that needs to be updated
    required: true
    schema:
      type: string
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        type: object
        properties:
          name:
            description: Updated name of the pet
            type: string
          status:
            description: Updated status of the pet
            type: string
        required:
          - status
responses:
  '200':
    description: Pet updated.
    content:
      application/json: {}
      application/xml: {}
  '405':
    description: Method Not Allowed
    content:
      application/json: {}
      application/xml: {}
security:
  - petstore_auth:
      - write:pets
      - read:pets
```

### 4.11 External Documentation Object

[](https://spec.openapis.org/oas/latest.html#external-documentation-object)

Allows referencing an external resource for extended documentation.

#### 4.11.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-8)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A description of the target documentation. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| url | `string` | ***REQUIRED***. The URI for the target documentation. This *MUST* be in the form of a URI. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.11.2 External Documentation Object Example

[](https://spec.openapis.org/oas/latest.html#external-documentation-object-example)

```
description: Find more info here
url: https://example.com
```

### 4.12 Parameter Object

[](https://spec.openapis.org/oas/latest.html#parameter-object)

Describes a single operation parameter.

A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/latest.html#parameter-name) and [location](https://spec.openapis.org/oas/latest.html#parameter-in).

See [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns, including interactions with the `application/x-www-form-urlencoded` query string format.

#### 4.12.1 Parameter Locations

[](https://spec.openapis.org/oas/latest.html#parameter-locations)

There are five possible parameter locations specified by the `in` field:

-   path - Used together with [Path Templating](https://spec.openapis.org/oas/latest.html#path-templating), where the parameter value is actually part of the operation’s URL. This does not include the host or base path of the API. For example, in `/items/{itemId}`, the path parameter is `itemId`.
-   query - Parameters that are appended to the URL. For example, in `/items?id=###`, the query parameter is `id`; *MUST NOT* appear in the same operation (or in the operation’s path-item) as an `in: "querystring"` parameter.
-   querystring - A parameter that treats the entire URL query string as a value which *MUST* be specified using the `content` field, most often with media type `application/x-www-form-urlencoded` using [Encoding Objects](https://spec.openapis.org/oas/latest.html#encoding-object) in the same way as with request bodies of that media type; *MUST NOT* appear more than once, and *MUST NOT* appear in the same operation (or in the operation’s path-item) as any `in: "query"` parameters.
-   header - Custom headers that are expected as part of the request. Note that \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 5.1](https://datatracker.ietf.org/doc/html/rfc9110#section-5.1) states header names are case-insensitive.
-   cookie - Used to pass a specific cookie value to the API.

#### 4.12.2 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-9)

The rules for serialization of the parameter are specified in one of two ways. Parameter Objects *MUST* include either a `content` field or a `schema` field, but not both. See [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion) for a discussion of converting values of various types to string representations.

##### 4.12.2.1 Common Fixed Fields

[](https://spec.openapis.org/oas/latest.html#common-fixed-fields)

These fields *MAY* be used with either `content` or `schema`.

The `example` and `examples` fields are mutually exclusive; see [Working with Examples](https://spec.openapis.org/oas/latest.html#working-with-examples) for guidance on validation requirements.

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the parameter. Parameter names are *case-sensitive*.
-   If [`in`](https://spec.openapis.org/oas/latest.html#parameter-in) is `"path"`, the `name` field *MUST* correspond to a single template expression occurring within the [path](https://spec.openapis.org/oas/latest.html#paths-path) field in the [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object). See [Path Templating](https://spec.openapis.org/oas/latest.html#path-templating) for further information.
-   If [`in`](https://spec.openapis.org/oas/latest.html#parameter-in) is `"header"` and the `name` field is `"Accept"`, `"Content-Type"` or `"Authorization"`, the parameter definition *SHALL* be ignored.
-   If `in` is `"querystring"`, or for [certain combinations](https://spec.openapis.org/oas/latest.html#style-examples) of [`style`](https://spec.openapis.org/oas/latest.html#parameter-style) and [`explode`](https://spec.openapis.org/oas/latest.html#parameter-explode), the value of `name` is not used in the parameter serialization.
-   For all other cases, the `name` corresponds to the parameter name used by the [`in`](https://spec.openapis.org/oas/latest.html#parameter-in) field.

 |
| in | `string` | ***REQUIRED***. The location of the parameter. Possible values are `"query"`, `"querystring"`, `"header"`, `"path"` or `"cookie"`. |
| description | `string` | A brief description of the parameter. This could contain examples of use. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| required | `boolean` | Determines whether this parameter is mandatory. If the [parameter location](https://spec.openapis.org/oas/latest.html#parameter-in) is `"path"`, this field is ***REQUIRED*** and its value *MUST* be `true`. Otherwise, the field *MAY* be included and its default value is `false`. |
| deprecated | `boolean` | Specifies that a parameter is deprecated and *SHOULD* be transitioned out of usage. Default value is `false`. |
| allowEmptyValue | `boolean` | If `true`, clients *MAY* pass a zero-length string value in place of parameters that would otherwise be omitted entirely, which the server *SHOULD* interpret as the parameter being unused. Default value is `false`. If [`style`](https://spec.openapis.org/oas/latest.html#parameter-style) is used, and if [behavior is *n/a* (cannot be serialized)](https://spec.openapis.org/oas/latest.html#style-examples), the value of `allowEmptyValue` *SHALL* be ignored. Interactions between this field and the parameter’s [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) are implementation-defined. This field is valid only for `query` parameters.

**Deprecated:** Use of this field is *NOT RECOMMENDED*, and it is likely to be removed in a later revision. |
| example | Any | Example of the parameter’s potential value; see [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples). |
| examples | Map\[ `string`, [Example Object](https://spec.openapis.org/oas/latest.html#example-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | Examples of the parameter’s potential value; see [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

Note that while `"Cookie"` as a `name` is not forbidden if `in` is `"header"`, the effect of defining a cookie parameter that way is undefined; use `in: "cookie"` instead.

##### 4.12.2.2 Fixed Fields for use with `schema`

[](https://spec.openapis.org/oas/latest.html#fixed-fields-for-use-with-schema)

For simpler scenarios, a [`schema`](https://spec.openapis.org/oas/latest.html#parameter-schema) and [`style`](https://spec.openapis.org/oas/latest.html#parameter-style) can describe the structure and syntax of the parameter.

These fields *MUST NOT* be used with `in: "querystring"`.

Care is needed for parameters with `schema` that have `in: "header"` or `in: "cookie", style: "cookie"`:

-   When serializing these values, URI percent-encoding *MUST NOT* be applied.
-   When parsing these parameters, any apparent percent-encoding *MUST NOT* be decoded.
-   If using an RFC6570 implementation that automatically performs encoding or decoding steps, the steps *MUST* be undone before use.

In these cases, implementations *MUST* pass values through unchanged rather than attempting to quote or escape them, as the quoting rules for headers and escaping conventions for cookies vary too widely to be performed automatically; see [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for guidance on quoting and escaping.

| Field Name | Type | Description |
| --- | --- | --- |
| style | `string` | Describes how the parameter value will be serialized depending on the type of the parameter value. Default values (based on value of `in`): for `"query"` - `"form"`; for `"path"` - `"simple"`; for `"header"` - `"simple"`; for `"cookie"` - `"form"` (for compatibility reasons; note that `style: "cookie"` *SHOULD* be used with `in: "cookie"`; see [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for details). |
| explode | `boolean` | When this is true, parameter values of type `array` or `object` generate separate parameters for each value of the array or key-value pair of the map. For other types of parameters, or when [`style`](https://spec.openapis.org/oas/latest.html#parameter-style) is `"deepObject"`, this field has no effect. When `style` is `"form"` or `"cookie"`, the default value is `true`. For all other styles, the default value is `false`. |
| allowReserved | `boolean` | When this is true, parameter values are serialized using reserved expansion, as defined by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 3.2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3), which allows [RFC3986’s reserved character set](https://tools.ietf.org/html/rfc3986#section-2.2), as well as percent-encoded triples, to pass through unchanged, while still percent-encoding all other disallowed characters (including `%` outside of percent-encoded triples). Applications are still responsible for percent-encoding reserved characters that are not allowed by the rules of the `in` destination or media type, or are [not allowed in the path by this specification](https://spec.openapis.org/oas/latest.html#path-templating); see [URL Percent-Encoding](https://spec.openapis.org/oas/latest.html#url-percent-encoding) for details. The default value is `false`. This field only applies to `in` and `style` values that automatically percent-encode. |
| schema | [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) | The schema defining the type used for the parameter. |

See also [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

##### 4.12.2.3 Fixed Fields for use with `content`

[](https://spec.openapis.org/oas/latest.html#fixed-fields-for-use-with-content)

For more complex scenarios, the [`content`](https://spec.openapis.org/oas/latest.html#parameter-content) field can define the media type and schema of the parameter, as well as give examples of its use.

For use with `in: "querystring"` and `application/x-www-form-urlencoded`, see [Encoding the `x-www-form-urlencoded` Media Type](https://spec.openapis.org/oas/latest.html#encoding-the-x-www-form-urlencoded-media-type).

| Field Name | Type | Description |
| --- | --- | --- |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A map containing the representations for the parameter. The key is the media type and the value describes it. The map *MUST* only contain one entry. |

#### 4.12.3 Style Values

[](https://spec.openapis.org/oas/latest.html#style-values)

In order to support common ways of serializing simple parameters, a set of `style` values are defined. Combinations not represented in this table are not permitted.

| `style` | [`type`](https://spec.openapis.org/oas/latest.html#data-types) | `in` | Comments |
| --- | --- | --- | --- |
| `matrix` | primitive, `array`, `object` | `path` | Path-style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 3.2.7](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.7) |
| `label` | primitive, `array`, `object` | `path` | Label style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 3.2.5](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.5) |
| `simple` | primitive, `array`, `object` | `path`, `header` | Simple style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 3.2.2](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.2). This option replaces `collectionFormat` with a `csv` value from OpenAPI 2.0. |
| `form` | primitive, `array`, `object` | `query`, `cookie` | Form style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 3.2.8](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.8). This option replaces `collectionFormat` with a `csv` (when `explode` is false) or `multi` (when `explode` is true) value from OpenAPI 2.0. |
| `spaceDelimited` | `array`, `object` | `query` | Space separated array values or object properties and values. This option replaces `collectionFormat` equal to `ssv` from OpenAPI 2.0. |
| `pipeDelimited` | `array`, `object` | `query` | Pipe separated array values or object properties and values. This option replaces `collectionFormat` equal to `pipes` from OpenAPI 2.0. |
| `deepObject` | `object` | `query` | Allows objects with scalar properties to be represented using form parameters. The representation of array or object properties is not defined (but see [Extending Support for Querystring Formats](https://spec.openapis.org/oas/latest.html#extending-support-for-querystring-formats) for alternatives). |
| `cookie` | primitive, `array`, `object` | `cookie` | Analogous to `form`, but following \[[RFC6265](https://spec.openapis.org/oas/latest.html#bib-rfc6265 "HTTP State Management Mechanism")\] `Cookie` syntax rules, meaning that name-value pairs are separated by a semicolon followed by a single space (e.g. `n1=v1; n2=v2`), and no percent-encoding or other escaping is applied; data values that require any sort of escaping *MUST* be provided in escaped form. |

#### 4.12.4 URL Percent-Encoding

[](https://spec.openapis.org/oas/latest.html#url-percent-encoding)

All API URLs *MUST* successfully parse and percent-decode using \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] rules.

Content in the `application/x-www-form-urlencoded` format, including query strings produced by [Parameter Objects](https://spec.openapis.org/oas/latest.html#parameter-object) with `in: "query"`, *MUST* also successfully parse and percent-decode using \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\] rules, including treating non-percent-encoded `+` as an escaped space character.

These requirements are specified in terms of percent-*decoding* rules, which are consistently tolerant across different versions of the various standards that apply to URIs.

Percent-*encoding* is performed in several places:

-   By \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] implementations (or simulations thereof; see [Appendix C](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization))
-   By the Parameter or [Encoding](https://spec.openapis.org/oas/latest.html#encoding-object) Objects when incorporating a value serialized with a [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) for a media type that does not already incorporate URI percent-encoding
-   By the user, prior to passing data through RFC6570’s reserved expansion process

When percent-encoding, the safest approach is to percent-encode all characters not in RFC3986’s “unreserved” set, and for `form-urlencoded` to also percent-encode the tilde character (`~`) to align with historical requirements that are traced back to \[[RFC1738](https://spec.openapis.org/oas/latest.html#bib-rfc1738 "Uniform Resource Locators (URL)")\], the URI RFC at the time `form-urlencoded` was created. This approach is used in examples in this specification.

For `form-urlencoded`, while the encoding algorithm given by \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\] requires escaping the space character as `+`, percent-encoding it as `%20` also meets the above requirements. Examples in this specification will prefer `%20` when using RFC6570’s default (non-reserved) form-style expansion, and `+` otherwise.

Reserved characters *MUST NOT* be percent-encoded when being used for reserved purposes such as `&=+` for `form-urlencoded` or `,` for delimiting non-exploded array and object values in RFC6570 expansions. The result of inserting non-percent-encoded delimiters into data using manual percent-encoding, including via RFC6570’s reserved expansion rules, is undefined and will likely prevent implementations from parsing the results back into the correct data structures. In some cases, such as inserting `/` into path parameter values, doing so is [explicitly forbidden](https://spec.openapis.org/oas/latest.html#path-templating) by this specification.

See also:

-   [Appendix C](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for guidance on using or simulating/extending RFC6570 implementations.
-   [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for guidance on percent-encoding and cookies, as well as other escaping approaches for headers and cookies.
-   [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for a thorough discussion of percent-encoding options, compatibility, and handling OAS-defined delimiters that are not allowed by RFC3986.

#### 4.12.5 Serialization and Examples

[](https://spec.openapis.org/oas/latest.html#serialization-and-examples)

The rules in this section apply to both the Parameter and [Header](https://spec.openapis.org/oas/latest.html#header-object) Objects, both of which use the same mechanisms.

When showing serialized examples, such as with the [Example Object’s](https://spec.openapis.org/oas/latest.html#example-object) `serializedValue` or `externalValue` fields, in most cases the value to show is just the value, with all relevant percent-encoding or other encoding/escaping applied, and also including any delimiters produced by the `style` and `explode` configuration.

In cases where the name is an inherent part of constructing the serialization, such as the `name=value` pairs produced by `style: "form"` or the combination of `style: "simple", explode: true`, the name and any delimiter between the name and value *MUST* be included.

The `matrix` and `label` styles produce a leading delimiter which is always a valid part of the serialization and *MUST* be included. The RFC6570 operators corresponding to `style: "form"` produce a leading delimiter of either `?` or `&` depending on the exact syntax used. As the suitability of either delimiter depends on where in the query string the parameter occurs, as well as whether it is in a URI or in `application/x-www-form-urlencoded` content, this leading delimiter *MUST NOT* be included in examples of individual parameters or media type documents. For `in: "cookie", style: "form"`, neither the `&` nor `?` delimiters are ever correct; see [Appendix D: Serializing Headers and Cookies](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for more details.

For headers, the header name *MUST NOT* be included as part of the serialization, as it is never part of the RFC6570-derived result. However, names produced by `style: "simple", explode: "true"` are included as they appear within the header value, not as separate headers. See the [Header Object](https://spec.openapis.org/oas/latest.html#header-object) for special rules for showing examples of the `Set-Cookie` response header, which violates the normal rules for multiple header values.

#### 4.12.6 Style Examples

[](https://spec.openapis.org/oas/latest.html#style-examples)

Assume a parameter named `color` has one of the following values, where the value to the right of the `->` is what would be shown in the `dataValue` field of an Example Object:

```
   string -> "blue"
   array -> ["blue", "black", "brown"]
   object -> { "R": 100, "G": 200, "B": 150 }
```

The following table shows serialized examples, as would be shown with the `serializedValue` field of an Example Object, of the different serializations for each value.

-   The value *empty* denotes the empty string, and is unrelated to the `allowEmptyValue` field.
-   The behavior of combinations marked *n/a* is undefined.
-   The `undefined` column replaces the `empty` column in previous versions of this specification in order to better align with \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-2.3) terminology, which describes certain values including but not limited to `null` as “undefined” values with special handling; notably, the empty string is *not* undefined.
-   For `form` and the non-RFC6570 query string styles `spaceDelimited`, `pipeDelimited`, and `deepObject`, see [Appendix C](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for more information on constructing query strings from multiple parameters, and [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for warnings regarding `form` and `cookie` parameters.
-   The examples are percent-encoded as explained in the [URL Percent-Encoding](https://spec.openapis.org/oas/latest.html#url-percent-encoding) section above; see [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for a thorough discussion of percent-encoding concerns, including why unencoded `|` (`%7C`), `[` (`%5B`), and `]` (`%5D`) seem to work in some environments despite not being compliant.

| [`style`](https://spec.openapis.org/oas/latest.html#style-values) | `explode` | `undefined` | `string` | `array` | `object` |
| --- | --- | --- | --- | --- | --- |
| matrix | false | ;color | ;color=blue | ;color=blue,black,brown | ;color=R,100,G,200,B,150 |
| matrix | true | ;color | ;color=blue | ;color=blue;color=black;color=brown | ;R=100;G=200;B=150 |
| label | false | . | .blue | .blue,black,brown | .R,100,G,200,B,150 |
| label | true | . | .blue | .blue.black.brown | .R=100.G=200.B=150 |
| simple | false | *empty* | blue | blue,black,brown | R,100,G,200,B,150 |
| simple | true | *empty* | blue | blue,black,brown | R=100,G=200,B=150 |
| form | false | color= | color=blue | color=blue,black,brown | color=R,100,G,200,B,150 |
| form | true | color= | color=blue | color=blue&color=black&color=brown | R=100&G=200&B=150 |
| spaceDelimited | false | *n/a* | *n/a* | color=blue%20black%20brown | color=R%20100%20G%20200%20B%20150 |
| spaceDelimited | true | *n/a* | *n/a* | *n/a* | *n/a* |
| pipeDelimited | false | *n/a* | *n/a* | color=blue%7Cblack%7Cbrown | color=R%7C100%7CG%7C200%7CB%7C150 |
| pipeDelimited | true | *n/a* | *n/a* | *n/a* | *n/a* |
| deepObject | *n/a* | *n/a* | *n/a* | *n/a* | color%5BR%5D=100&color%5BG%5D=200&color%5BB%5D=150 |
| cookie | false | color= | color=blue | color=blue,black,brown | color=R,100,G,200,B,150 |
| cookie | true | color= | color=blue | color=blue; color=black; color=brown | R=100; G=200; B=150 |

#### 4.12.7 Extending Support for Querystring Formats

[](https://spec.openapis.org/oas/latest.html#extending-support-for-querystring-formats)

Many frameworks define query string syntax for complex values, such as appending array indices to parameter names or indicating multiple levels of of nested objects, which go well beyond the capabilities of the `deepObject` style.

As these are not standards, and often contradict each other, the OAS does not attempt to support them directly. Two avenues are available for supporting such formats with `in: "querystring"`:

-   Use `content` and `text/plain` with a schema of `type: "string"` and define the format outside of OpenAPI. While this requires more work to document and construct or parse the format, which is seen as a plain string from the OpenAPI perspective, it provides the easiest flexible option
-   Define a media type (which need not necessarily be [IANA-registered](https://tools.ietf.org/html/rfc6838)) and a process for mapping in-memory data to the serialized media type. To increase the likelihood of support across multiple tools, submit a registration for the media type and process to the OpenAPI Initiative’s [Media Type Registry](https://spec.openapis.org/oas/latest.html#openapi-media-type-registry).

#### 4.12.8 Parameter Object Examples

[](https://spec.openapis.org/oas/latest.html#parameter-object-examples)

A header parameter with an array of 64-bit integer numbers:

```
name: X-Token
in: header
description: token to be passed as a header
required: true
schema:
  type: array
  items:
    type: integer
    format: int64
style: simple
examples:
  Tokens:
    dataValue:
      - 12345678
      - 90099
    serializedValue: "12345678,90099"
```

A cookie parameter with an exploded object (the default for `style: "cookie"`):

```
name: cookie
in: cookie
style: cookie
schema:
  type: object
  properties:
    greeting:
      type: string
    code:
      type: integer
      minimum: 0
examples:
  Object:
    description: |
        Note that the comma (,) has been pre-percent-encoded
        to "%2C" in the data, as it is forbidden in
        cookie values.  However, the exclamation point (!)
        is legal in cookies, so it can be left unencoded.
    dataValue:
      greeting: Hello%2C world!
      code: 42
    serializedValue: "greeting=Hello%2C world!; code=42"
```

A cookie parameter relying on the percent-encoding behavior of the default `style: "form"`:

```
name: greeting
in: cookie
schema:
  type: string
examples:
  Greeting:
    description: |
      Note that in this approach, RFC6570's percent-encoding
      process applies, so unsafe characters are not
      pre-percent-encoded.  This results in all non-URL-safe
      characters, rather than just the one non-cookie-safe
      character, getting percent-encoded.
    dataValue: Hello, world!
    serializedValue: "greeting=Hello%2C%20world%21"
```

A path parameter of a string value:

```
name: username
in: path
description: username to fetch
required: true
schema:
  type: string
examples:
  "Edsger Dijkstra":
    dataValue: edijkstra
    serializedValue: edijkstra
  Diṅnāga:
    dataValue: diṅnāga
    serializedValue: di%E1%B9%85n%C4%81ga
  Al-Khwarizmi:
    dataValue: "الخوارزميّ"
    serializedValue: "%D8%A7%D9%84%D8%AE%D9%88%D8%A7%D8%B1%D8%B2%D9%85%D9%8A%D9%91"
```

An optional query parameter of a string value, allowing multiple values by repeating the query parameter (Note that we use `"%20"` in place of `" "` (space) because that is how RFC6570 handles it; for guidance on using `+` to represent the space character, see [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for more guidance on these escaping options):

```
name: thing
in: query
required: false
schema:
  type: array
  items:
    type: string
style: form
explode: true
examples:
  ObjectList:
    dataValue:
      - one thing
      - another thing
    serializedValue: "thing=one%20thing&thing=another%20thing"
```

A free-form query parameter, allowing arbitrary parameters of `type: "integer"`:

```
in: query
name: freeForm
schema:
  type: object
  additionalProperties:
    type: integer
style: form
examples:
  Pagination:
    dataValue:
      page: 4
      pageSize: 50
    serializeValue: page=4&pageSize=50
```

A complex parameter using `content` to define serialization, with multiple levels and types of examples shown to make the example usage options clear — note that `dataValue` is the same at both levels and does not need to be shown in both places in normal usage, but `serializedValue` is different:

```
in: query
name: coordinates
content:
  application/json:
    schema:
      type: object
      required:
        - lat
        - long
      properties:
        lat:
          type: number
        long:
          type: number
    examples:
      dataValue:
        lat: 10
        long: 60
      serializedValue: '{"lat":10,"long":60}'
examples:
  dataValue:
    lat: 10
    long: 60
  serializedValue: coordinates=%7B%22lat%22%3A10%2C%22long%22%3A60%7D
```

A querystring parameter using regular form encoding, but managed with a Media Type Object. This shows spaces being handled per the `application/x-www-form-urlencoded` media type rules (encode as `+`) rather than the RFC6570 process (encode as `%20`); see [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for further guidance on this distinction. Examples are shown at both the media type and parameter level to emphasize that, since `application/x-www-form-urlencoded` is suitable for use in query strings by definition, no further encoding or escaping is applied to the serialized media type value:

```
in: querystring
content:
  application/x-www-form-urlencoded:
    schema:
      type: object
      properties:
        foo:
          type: string
        bar:
          type: boolean
    examples:
      spacesAndPluses:
        description: Note handling of spaces and "+" per media type.
        dataValue:
          foo: a + b
          bar: true
        serializedValue: foo=a+%2B+b&bar=true
examples:
  spacesAndPluses:
    description: |
      Note that no additional percent encoding is done, as this
      media type is URI query string-ready by definition.
    dataValue:
      foo: a + b
      bar: true
    serializedValue: foo=a+%2B+b&bar=true
```

A querystring parameter that uses JSON for the entire string (not as a single query parameter value). The `dataValue` field is shown at both levels to fully illustrate both ways of providing an example. As seen below, this is redundant and need not be done in practice:

```
in: querystring
name: json
content:
  application/json:
    schema:
      type: object
      properties:
        numbers:
          type: array
          items:
            type: integer
        flag:
          type: [boolean, "null"]
    examples:
      TwoNoFlag:
        description: Serialize with minimized whitespace
        dataValue:
          numbers:
            - 1
            - 2
          flag: null
        serializedValue: '{"numbers":[1,2],"flag":null}'
examples:
  TwoNoFlag:
    dataValue:
      numbers:
        - 1
        - 2
      flag: null
    serializedValue: "%7B%22numbers%22%3A%5B1%2C2%5D%2C%22flag%22%3Anull%7D"
```

Assuming a path of `/foo`, a server of `https://example.com`, the full URL incorporating the value from `serializedValue` would be:

```
https://example.com/foo?%7B%22numbers%22%3A%5B1%2C2%5D%2C%22flag%22%3Anull%7D
```

A querystring parameter that uses [JSONPath](https://spec.openapis.org/oas/latest.html#bib-rfc9535 "JSONPath: Query Expressions for JSON"). Note that in this example we not only do not repeat `dataValue`, but we use the shorthand `example` because the `application/jsonpath` value is a string that, at the media type level, is serialized as-is:

```
in: querystring
name: selector
content:
  application/jsonpath:
    schema:
      type: string
    example: $.a.b[1:1]
examples:
  Selector:
    serializedValue: "%24.a.b%5B1%3A1%5D"
```

As there is not, as of this writing, a [registered](https://spec.openapis.org/oas/latest.html#openapi-media-type-registry) mapping between the JSON Schema data model and JSONPath, the details of the string’s allowed structure would need to be conveyed either in a human-readable `description` field, or through a mechanism outside of the OpenAPI Description, such as a JSON Schema for the data structure to be queried.

Assuming a path of `/foo` and a server of `https://example.com`, the full URL incorporating the value from `serializedValue` would be:

```
https://example.com/foo?%24.a.b%5B1%3A1%5D
```

### 4.13 Request Body Object

[](https://spec.openapis.org/oas/latest.html#request-body-object)

Describes a single request body.

#### 4.13.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-10)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A brief description of the request body. This could contain examples of use. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | ***REQUIRED***. The content of the request body. The key is a media type or [media type range](https://tools.ietf.org/html/rfc9110#appendix-A) and the value describes it. The map *SHOULD* have at least one entry; if it does not, the behavior is implementation-defined. For requests that match multiple keys, only the most specific key is applicable. e.g. `"text/plain"` overrides `"text/*"` |
| required | `boolean` | Determines if the request body is required in the request. Defaults to `false`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.13.2 Request Body Examples

[](https://spec.openapis.org/oas/latest.html#request-body-examples)

A request body with a referenced schema definition.

```
description: user to add to the system
content:
  application/json:
    schema:
      $ref: '#/components/schemas/User'
    examples:
      user:
        summary: User example
        externalValue: https://foo.bar/examples/user-example.json
  application/xml:
    schema:
      $ref: '#/components/schemas/User'
    examples:
      user:
        summary: User example in XML
        externalValue: https://foo.bar/examples/user-example.xml
  text/plain:
    examples:
      user:
        summary: User example in plain text
        externalValue: https://foo.bar/examples/user-example.txt
  '*/*':
    examples:
      user:
        summary: User example in other format
        externalValue: https://foo.bar/examples/user-example.whatever
```

### 4.14 Media Type Object

[](https://spec.openapis.org/oas/latest.html#media-type-object)

Each Media Type Object describes content structured in accordance with the media type identified by its key. Multiple Media Type Objects can be used to describe content that can appear in any of several different media types.

When `example` or `examples` are provided, the example *SHOULD* match the specified schema and be in the correct format as specified by the media type and its encoding. The `example` and `examples` fields are mutually exclusive. See [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples) for further guidance regarding the different ways of specifying examples, including non-JSON/YAML values.

#### 4.14.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-11)

| Field Name | Type | Description |
| --- | --- | --- |
| schema | [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) | A schema describing the complete content of the request, response, parameter, or header. |
| itemSchema | [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) | A schema describing each item within a [sequential media type](https://spec.openapis.org/oas/latest.html#sequential-media-types). |
| example | Any | Example of the media type; see [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples). |
| examples | Map\[ `string`, [Example Object](https://spec.openapis.org/oas/latest.html#example-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | Examples of the media type; see [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples). |
| encoding | Map\[`string`, [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)\] | A map between a property name and its encoding information, as defined under [Encoding By Name](https://spec.openapis.org/oas/latest.html#encoding-by-name). The `encoding` field *SHALL* only apply when the media type is `multipart` or `application/x-www-form-urlencoded`. If no Encoding Object is provided for a property, the behavior is determined by the default values documented for the Encoding Object. This field *MUST NOT* be present if `prefixEncoding` or `itemEncoding` are present. |
| prefixEncoding | \[[Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)\] | An array of positional encoding information, as defined under [Encoding By Position](https://spec.openapis.org/oas/latest.html#encoding-by-position). The `prefixEncoding` field *SHALL* only apply when the media type is `multipart`. If no Encoding Object is provided for a property, the behavior is determined by the default values documented for the Encoding Object. This field *MUST NOT* be present if `encoding` is present. |
| itemEncoding | [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) | A single Encoding Object that provides encoding information for multiple array items, as defined under [Encoding By Position](https://spec.openapis.org/oas/latest.html#encoding-by-position). The `itemEncoding` field *SHALL* only apply when the media type is `multipart`. If no Encoding Object is provided for a property, the behavior is determined by the default values documented for the Encoding Object. This field *MUST NOT* be present if `encoding` is present. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.14.2 Media Types

[](https://spec.openapis.org/oas/latest.html#media-types)

Media types are publicly registered with the [IANA media types registry](https://www.iana.org/assignments/media-types/media-types.xhtml), through process documented in \[[RFC6838](https://spec.openapis.org/oas/latest.html#bib-rfc6838 "Media Type Specifications and Registration Procedures")\].

APIs also sometimes define private media types such as GitHub’s `application/vnd.github.v3+json`, which are not registered, and other media types such as `application/schema+json` become widely used before an intended registration.

See [Parsing and Serializing](https://spec.openapis.org/oas/latest.html#parsing-and-serializing) under the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) for guidance on using schemas with a variety of media types.

##### 4.14.2.1 OpenAPI Media Type Registry

[](https://spec.openapis.org/oas/latest.html#openapi-media-type-registry)

The OpenAPI Initiative maintains a [Media Type Registry](https://spec.openapis.org/registry/media-type/) summarizing media type support expected by this specification and providing an index to which sections address which media types. It also links to IANA registrations (where they exist) and to the most notable specification document(s) related to each media type. Any additional media types added to this registry as extensions or for later versions of this or other OpenAPI specifications *MAY* be supported by implementations of this version of the OAS.

#### 4.14.3 Complete vs Streaming Content

[](https://spec.openapis.org/oas/latest.html#complete-vs-streaming-content)

The `schema` field *MUST* be applied to the complete content, as defined by the media type and the context ([Request Body Object](https://spec.openapis.org/oas/latest.html#request-body-object), [Response Object](https://spec.openapis.org/oas/latest.html#response-object), [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object), or [Header Object](https://spec.openapis.org/oas/latest.html#header-object). Because this requires loading the content into memory in its entirety, it poses a challenge for streamed content. Use cases where clients are intended to choose when to stop reading are particularly challenging as there is no well-defined end to the stream.

##### 4.14.3.1 Sequential Media Types

[](https://spec.openapis.org/oas/latest.html#sequential-media-types)

Within this specification, a *sequential media type* is defined as any media type that consists of a repeating structure, without any sort of header, footer, envelope, or other metadata in addition to the sequence.

Some examples of sequential media types (including some that are not IANA-registered but are in common use) are:

```
  application/jsonl
  application/x-ndjson
  application/json-seq
  application/geo+json-seq
  text/event-stream
  multipart/mixed
```

In the first three above, the repeating structure is any [JSON value](https://tools.ietf.org/html/rfc8259#section-3). The fourth repeats `application/geo+json`\-structured values, while `text/event-stream` repeats a custom text format related to Server-Sent Events. The final media type listed above, `multipart/mixed`, provides an ordered list of documents of any media type, and is sometimes streamed. Note that while `multipart` formats technically allow a preamble and an epilogue, the RFC directs that they are to be ignored, making them effectively comments, and this specification does not model them.

Implementations *MUST* support mapping sequential media types into the JSON Schema data model by treating them as if the values were in an array in the same order.

See [Complete vs Streaming Content](https://spec.openapis.org/oas/latest.html#complete-vs-streaming-content) for more information on handling sequential media types in a streaming context, including special considerations for `text/event-stream` content. For `multipart` types, see also [Encoding By Position](https://spec.openapis.org/oas/latest.html#encoding-by-position).

###### 4.14.3.1.1 Streaming Sequential Media Types

[](https://spec.openapis.org/oas/latest.html#streaming-sequential-media-types)

The `itemSchema` field is provided to support streaming use cases for sequential media types, with `itemEncoding` as a corresponding encoding mechanism for streaming [positional `multipart` media types](https://spec.openapis.org/oas/latest.html#encoding-by-position).

Unlike `schema`, which is applied to the complete content (treated as an array as described in the [sequential media types](https://spec.openapis.org/oas/latest.html#sequential-media-types) section), `itemSchema` *MUST* be applied to each item in the stream independently, which supports processing each item as it is read from the stream.

Both `schema` and `itemSchema` *MAY* be used in the same Media Type Object. However, doing so is unlikely to have significant advantages over using the `items` keyword within the `schema` field.

##### 4.14.3.2 Binary Streams

[](https://spec.openapis.org/oas/latest.html#binary-streams)

The `maxLength` keyword *MAY* be used to set an expected upper bound on the length of a streaming payload that consists of either string data, including encoded binary data, or unencoded binary data. For unencoded binary data, the length is the number of octets. For this use case, `maxLength` *MAY* be implemented outside of regular JSON Schema evaluation as JSON Schema does not directly apply to binary data, and an encoded binary stream may be impractical to store in memory in its entirety.

#### 4.14.4 Special Considerations for Server-Sent Events

[](https://spec.openapis.org/oas/latest.html#special-considerations-for-server-sent-events)

For `text/event-stream`, implementations *MUST* work with event data after it has been parsed according to the [`text/event-stream` specification](https://html.spec.whatwg.org/multipage/server-sent-events.html#parsing-an-event-stream), including all guidance on ignoring certain fields (including comments) and/or values, and on combining values split across multiple lines.

Field value types *MUST* be handled as specified by the `text/event-stream` specification (e.g. the `retry` field value is modeled as a JSON number that is expected to be of JSON Schema `type: integer`), and fields not given an explicit value type *MUST* be handled as strings.

Some users of `text/event-stream` use a format such as JSON for field values, particularly the `data` field. Use JSON Schema’s keywords for working with the [contents of string-encoded data](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#name-a-vocabulary-for-the-conten), particularly `contentMediaType` and `contentSchema`, to describe and validate such fields with more detail than string-related validation keywords such as `pattern` can support. Note that `contentSchema` is [not automatically validated by default](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#name-implementation-requirements-2) (see also the [Non-validating constraint keywords](https://spec.openapis.org/oas/latest.html#non-validating-constraint-keywords) section of this specification).

The following Schema Object is a generic schema for the `text/event-stream` media type as documented by the \[[HTML](https://spec.openapis.org/oas/latest.html#bib-html "HTML Standard")\] specification as of the time of this writing:

```
type: object
required:
- data
properties:
  data:
    type: string
  event:
    type: string
  id:
    type: string
  retry:
    type: integer
    minimum: 0
```

#### 4.14.5 Encoding Usage and Restrictions

[](https://spec.openapis.org/oas/latest.html#encoding-usage-and-restrictions)

These encoding fields define how to map each [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) to a specific value in the data. Each field has its own set of media types with which it can be used; for all other media types all three fields *SHALL* be ignored.

##### 4.14.5.1 Encoding By Name

[](https://spec.openapis.org/oas/latest.html#encoding-by-name)

The behavior of the `encoding` field is designed to support web forms, and is therefore only defined for media types structured as name-value pairs that allow repeat values, most notably `application/x-www-form-urlencoded` and `multipart/form-data`.

To use the `encoding` field, each key under the field *MUST* exist as a property; `encoding` entries with no corresponding property *SHALL* be ignored. Array properties *MUST* be handled by applying the given Encoding Object to produce one encoded value per array item, each with the same `name`, as is recommended by \[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.3](https://tools.ietf.org/html/rfc7578#section-4.3) for supplying multiple values per form field. For all other value types for both top-level non-array properties and for values, including array values, within a top-level array, the Encoding Object *MUST* be applied to the entire value. The order of these name-value pairs in the target media type is implementation-defined.

For `application/x-www-form-urlencoded`, the encoding keys *MUST* map to parameter names, with the values produced according to the rules of the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object). See [Encoding the `x-www-form-urlencoded` Media Type](https://spec.openapis.org/oas/latest.html#encoding-the-x-www-form-urlencoded-media-type) for guidance and examples, both with and without the `encoding` field.

For `multipart`, the encoding keys *MUST* map to the [`name` parameter](https://tools.ietf.org/html/rfc7578#section-4.2) of the `Content-Disposition: form-data` header of each part, as is defined for `multipart/form-data` in \[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\]. See \[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 5](https://tools.ietf.org/html/rfc7578#section-5) for guidance regarding non-ASCII part names.

See [Encoding `multipart` Media Types](https://spec.openapis.org/oas/latest.html#encoding-multipart-media-types) for further guidance and examples, both with and without the `encoding` field.

##### 4.14.5.2 Encoding By Position

[](https://spec.openapis.org/oas/latest.html#encoding-by-position)

Most `multipart` media types, including `multipart/mixed` which defines the underlying rules for parsing all `multipart` types, do not have named parts. Data for these media types are modeled as an array, with one item per part, in order.

To use the `prefixEncoding` and/or `itemEncoding` fields, either `itemSchema` or an array `schema` *MUST* be present. These fields are analogous to the `prefixItems` and `items` JSON Schema keywords, with `prefixEncoding` (if present) providing an array of Encoding Objects that are each applied to the value at the same position in the data array, and `itemEncoding` applying its single Encoding Object to all remaining items in the array. As with `prefixItems`, it is *not* an error if the instance array is shorter than the `prefixEncoding` array; the additional Encoding Objects *SHALL* be ignored.

The `itemEncoding` field can also be used with `itemSchema` to support streaming `multipart` content.

##### 4.14.5.3 Additional Encoding Approaches

[](https://spec.openapis.org/oas/latest.html#additional-encoding-approaches)

The `prefixEncoding` field can be used with any `multipart` content to require a fixed part order. This includes `multipart/form-data`, for which the Encoding Object’s `headers` field *MUST* be used to provide the `Content-Disposition` and part name, as no property names exist to provide the names automatically.

Prior versions of this specification advised using the [`name` parameter](https://tools.ietf.org/html/rfc7578#section-4.2) of the `Content-Disposition: form-data` header of each part with `multipart` media types other than `multipart/form-data` in order to work around the limitations of the `encoding` field. Implementations *MAY* choose to support this workaround, but as this usage is not common, implementations of non-`form-data` `multipart` media types are unlikely to support it.

#### 4.14.6 Media Type Examples

[](https://spec.openapis.org/oas/latest.html#media-type-examples-0)

For form-related and `multipart` media type examples, see the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object).

##### 4.14.6.1 JSON

[](https://spec.openapis.org/oas/latest.html#json)

Note that since this example is written in YAML, the Example Object’s `value` field can be formatted as YAML due to the trivial conversion to JSON. This avoids needing to embed JSON as a string.

```
application/json:
  schema:
    $ref: '#/components/schemas/Pet'
  examples:
    cat:
      summary: An example of a cat
      value:
        name: Fluffy
        petType: Cat
        color: White
        gender: male
        breed: Persian
    dog:
      summary: An example of a dog with a cat's name
      value:
        name: Puma
        petType: Dog
        color: Black
        gender: Female
        breed: Mixed
    frog:
      $ref: '#/components/examples/frog-example'
```

Alternatively, since all JSON is valid YAML, the example value can use JSON syntax within a YAML document:

```
application/json:
  schema:
    $ref: '#/components/schemas/Pet'
  examples:
    cat:
      summary: An example of a cat
      value: {
        "name": "Fluffy",
        "petType": "Cat",
        "color": "White",
        "gender": "male",
        "breed": "Persian"
      }
    dog:
      summary: An example of a dog with a cat's name
      value: {
        "name": "Puma",
        "petType": "Dog",
        "color": "Black",
        "gender": "Female",
        "breed": "Mixed"
      }
    frog:
      $ref: '#/components/examples/frog-example'
```

##### 4.14.6.2 Sequential JSON

[](https://spec.openapis.org/oas/latest.html#sequential-json)

For any [sequential media type](https://spec.openapis.org/oas/latest.html#sequential-media-types) where the items in the sequence are JSON values, no conversion of each value is required. JSON Text Sequences (\[[RFC7464](https://spec.openapis.org/oas/latest.html#bib-rfc7464 "JavaScript Object Notation (JSON) Text Sequences")\] `application/json-seq` and \[[RFC8091](https://spec.openapis.org/oas/latest.html#bib-rfc8091 "A Media Type Structured Syntax Suffix for JSON Text Sequences")\] the `+json-seq` structured suffix), [JSON Lines](https://jsonlines.org/) (`application/jsonl`), and [NDJSON](https://github.com/ndjson/ndjson-spec) (`application/x-ndjson`) are all in this category. Note that the media types for JSON Lines and NDJSON are not registered with the IANA, but are in common use.

The following example shows Media Type Objects for both streaming log entries and returning a fixed-length set in response to a query. This shows the relationship between `schema` and `itemSchema`, and when to use each even though the `examples` field is the same either way.

```
components:
  schemas:
    LogEntry:
      type: object
      properties:
        timestamp:
          type: string
          format: date-time
        level:
          type: integer
          minimum: 0
        message:
          type: string
    Log:
      type: array
      items:
        $ref: "#/components/schemas/LogEntry"
      maxItems: 100
  examples:
    LogJSONSeq:
      summary: Log entries in application/json-seq
      # JSON Text Sequences require an unprintable character
      # that cannot be escaped in a YAML string, and therefore
      # must be placed in an external document shown below
      externalValue: examples/log.json-seq
    LogJSONPerLine:
      summary: Log entries in application/jsonl or application/x-ndjson
      description: JSONL and NDJSON are identical for this example
      # Note that the value must be written as a string with newlines,
      # as JSONL and NDJSON are not valid YAML
      value: |
        {"timestamp": "1985-04-12T23:20:50.52Z", "level": 1, "message": "Hi!"}
        {"timestamp": "1985-04-12T23:20:51.37Z", "level": 1, "message": "Bye!"}
  responses:
    LogStream:
      description: |
        A stream of JSON-format log messages that can be read
        for as long as the application is running, and is available
        in any of the sequential JSON media types.
      content:
        application/json-seq:
          itemSchema:
            $ref: "#/components/schemas/LogEntry"
          examples:
            JSON-SEQ:
              $ref: "#/components/examples/LogJSONSeq"
        application/jsonl:
          itemSchema:
            $ref: "#/components/schemas/LogEntry"
          examples:
            JSONL:
              $ref: "#/components/examples/LogJSONPerLine"
        application/x-ndjson:
          itemSchema:
            $ref: "#/components/schemas/LogEntry"
          examples:
            NDJSON:
              $ref: "#/components/examples/LogJSONPerLine"
    LogExcerpt:
      description: |
        A response consisting of no more than 100 log records,
        generally as a result of a query of the historical log,
        available in any of the sequential JSON media types.
      content:
        application/json-seq:
          schema:
            $ref: "#/components/schemas/Log"
          examples:
            JSON-SEQ:
              $ref: "#/components/examples/LogJSONSeq"
        application/jsonl:
          schema:
            $ref: "#/components/schemas/Log"
          examples:
            JSONL:
              $ref: "#/components/examples/LogJSONPerLine"
        application/x-ndjson:
          schema:
            $ref: "#/components/schemas/Log"
          examples:
            NDJSON:
              $ref: "#/components/examples/LogJSONPerLine"
```

Our `application/json-seq` example has to be an external document because of the use of both newlines and of the unprintable Record Separator (`0x1E`) character, which cannot be escaped in YAML block literals:

```
0x1E{
  "timestamp": "1985-04-12T23:20:50.52Z",
  "level": 1,
  "message": "Hi!"
}
0x1E{
  "timestamp": "1985-04-12T23:20:51.37Z",
  "level": 1,
  "message": "Bye!"
}
```

##### 4.14.6.3 Server-Sent Event Streams

[](https://spec.openapis.org/oas/latest.html#server-sent-event-streams)

For this example, assume that the generic event schema provided in the [Special Considerations for Server-Sent Events](https://spec.openapis.org/oas/latest.html#special-considerations-for-server-sent-events) section is available at `#/components/schemas/Event`:

```
description: A request body to add a stream of typed data.
required: true
content:
  text/event-stream:
    itemSchema:
      $ref: "#/components/schemas/Event"
      required: [event]
      oneOf:
      - properties:
          event:
            const: addString
      - properties:
          event:
            const: addInt64
          data:
            $comment: |
              Since the `data` field is a string,
              we need a format to signal that it
              should be handled as a 64-bit integer.
            format: int64
      - properties:
          event:
            const: addJson
          data:
            $comment: |
              These content fields indicate
              that the string value should
              be parsed and validated as a
              JSON document (since JSON is not
              a binary format, `contentEncoding`
              is not needed)
            contentMediaType: application/json
            contentSchema:
              type: object
              required: [foo]
              properties:
                foo:
                  type: integer
```

The following `text/event-stream` document is an example of a valid request body for the above example:

```
event: addString
data: This data is formatted
data: across two lines
retry: 5

event: addInt64
data: 1234.5678
unknownField: this is ignored

: This is a comment
event: addJSON
data: {"foo": 42}
```

To more clearly see how this stream is handled, the following is the equivalent JSON Lines document, which shows how the numeric and JSON data are handled as strings, and how unknown fields and comments are ignored and not passed to schema validation:

```
{"event": "addString", "data": "This data is formatted\nacross two lines", "retry": 5}
{"event": "addInt64", "data": "1234.5678"}
{"event": "addJSON", "data": "{\"foo\": 42}"}
```

#### 4.14.7 Considerations for File Uploads

[](https://spec.openapis.org/oas/latest.html#considerations-for-file-uploads)

In contrast to OpenAPI 2.0, `file` input/output content in OAS 3.x is described with the same semantics as any other schema type.

In contrast to OAS 3.0, the `format` keyword has no effect on the content-encoding of the schema in OAS 3.1. Instead, JSON Schema’s `contentEncoding` and `contentMediaType` keywords are used. See [Working With Binary Data](https://spec.openapis.org/oas/latest.html#working-with-binary-data) for how to model various scenarios with these keywords, and how to migrate from the previous `format` usage.

Examples:

Content transferred in binary (octet-stream) *MAY* omit `schema`:

```
# a PNG image as a binary file:
content:
  image/png: {}
```

```
# an arbitrary binary file:
content:
  application/octet-stream: {}
```

```
# arbitrary JSON without constraints beyond being syntactically valid:
content:
  application/json: {}
```

These examples apply to either input payloads of file uploads or response payloads.

A `requestBody` for submitting a file in a `POST` operation may look like the following example:

```
requestBody:
  content:
    application/octet-stream: {}
```

In addition, specific media types *MAY* be specified:

```
# multiple, specific media types may be specified:
requestBody:
  content:
    # a binary file of type png or jpeg
    image/jpeg: {}
    image/png: {}
```

To upload multiple files, a `multipart` media type *MUST* be used as shown under [Example: Multipart Form with Multiple Files](https://spec.openapis.org/oas/latest.html#example-multipart-form-with-multiple-files).

### 4.15 Encoding Object

[](https://spec.openapis.org/oas/latest.html#encoding-object)

A single encoding definition applied to a single value, with the mapping of Encoding Objects to values determined by the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) as described under [Encoding Usage and Restrictions](https://spec.openapis.org/oas/latest.html#encoding-usage-and-restrictions).

See [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion) for a discussion of converting values of various types to string representations.

See [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns for form media types.

#### 4.15.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-12)

##### 4.15.1.1 Common Fixed Fields

[](https://spec.openapis.org/oas/latest.html#common-fixed-fields-0)

These fields *MAY* be used either with or without the RFC6570-style serialization fields defined in the next section below.

| Field Name | Type | Description |
| --- | --- | --- |
| contentType | `string` | The `Content-Type` for encoding a specific property. The value is a comma-separated list, each element of which is either a specific media type (e.g. `image/png`) or a wildcard media type (e.g. `image/*`). The default value depends on the type as shown in the table below. |
| headers | Map\[`string`, [Header Object](https://spec.openapis.org/oas/latest.html#header-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A map allowing additional information to be provided as headers. `Content-Type` is described separately and *SHALL* be ignored in this section. This field *SHALL* be ignored if the media type is not a `multipart`. |
| encoding | Map\[`string`, [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)\] | Applies nested Encoding Objects in the same manner as the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object)’s `encoding` field. |
| prefixEncoding | \[[Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)\] | Applies nested Encoding Objects in the same manner as the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object)’s `prefixEncoding` field. |
| itemEncoding | [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) | Applies nested Encoding Objects in the same manner as the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object)’s `itemEncoding` field. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

The default values for `contentType` are as follows, where an *n/a* in the `contentEncoding` column means that the presence or value of `contentEncoding` is irrelevant. This table is based on the value to which the Encoding Object is being applied as defined under [Encoding Usage and Restrictions](https://spec.openapis.org/oas/latest.html#encoding-usage-and-restrictions). Note that in the case of [Encoding By Name](https://spec.openapis.org/oas/latest.html#encoding-by-name), this value is the array item for properties of type `"array"`, and the entire value for all other types. Therefore the `array` row in this table applies only to array values inside of a top-level array when encoding by name.

| `type` | `contentEncoding` | Default `contentType` |
| --- | --- | --- |
| [*absent*](https://spec.openapis.org/oas/latest.html#working-with-binary-data) | *n/a* | `application/octet-stream` |
| `string` | *present* | `application/octet-stream` |
| `string` | *absent* | `text/plain` |
| `number`, `integer`, or `boolean` | *n/a* | `text/plain` |
| `object` | *n/a* | `application/json` |
| `array` | *n/a* | `application/json` |

Determining how to handle a `type` value of `null` depends on how `null` values are being serialized. If `null` values are entirely omitted, then the `contentType` is irrelevant. See [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion) for a discussion of data type conversion options.

##### 4.15.1.2 Fixed Fields for RFC6570-style Serialization

[](https://spec.openapis.org/oas/latest.html#fixed-fields-for-rfc6570-style-serialization)

| Field Name | Type | Description |
| --- | --- | --- |
| style | `string` | Describes how a specific property value will be serialized depending on its type. See [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) for details on the [`style`](https://spec.openapis.org/oas/latest.html#parameter-style) field. The behavior follows the same values as `query` parameters, including the default value of `"form"` which applies only when `contentType` is *not* being used due to one or both of `explode` or `allowReserved` being explicitly specified. Note that the initial `?` used in query strings is not used in `application/x-www-form-urlencoded` message bodies, and *MUST* be removed (if using an RFC6570 implementation) or simply not added (if constructing the string manually). This field *SHALL* be ignored if the media type is not `application/x-www-form-urlencoded` or `multipart/form-data`. If a value is explicitly defined, then the value of [`contentType`](https://spec.openapis.org/oas/latest.html#encoding-content-type) (implicit or explicit) *SHALL* be ignored. |
| explode | `boolean` | When this is true, property values of type `array` or `object` generate separate parameters for each value of the array, or key-value-pair of the map. For other types of properties, or when [`style`](https://spec.openapis.org/oas/latest.html#encoding-style) is `"deepObject"`, this field has no effect. When `style` is `"form"`, the default value is `true`. For all other styles, the default value is `false`. This field *SHALL* be ignored if the media type is not `application/x-www-form-urlencoded` or `multipart/form-data`. If a value is explicitly defined, then the value of [`contentType`](https://spec.openapis.org/oas/latest.html#encoding-content-type) (implicit or explicit) *SHALL* be ignored. |
| allowReserved | `boolean` | When this is true, parameter values are serialized using reserved expansion, as defined by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 3.2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3), which allows [RFC3986’s reserved character set](https://tools.ietf.org/html/rfc3986#section-2.2), as well as percent-encoded triples, to pass through unchanged, while still percent-encoding all other disallowed characters (including `%` outside of percent-encoded triples). Applications are still responsible for percent-encoding reserved characters that are not allowed in the target media type; see [URL Percent-Encoding](https://spec.openapis.org/oas/latest.html#url-percent-encoding) for details. The default value is `false`. This field *SHALL* be ignored if the media type is not `application/x-www-form-urlencoded` or `multipart/form-data`. If a value is explicitly defined, then the value of [`contentType`](https://spec.openapis.org/oas/latest.html#encoding-content-type) (implicit or explicit) *SHALL* be ignored. |

When using RFC6570-style serialization for `multipart/form-data`, URI percent-encoding *MUST NOT* be applied, and the value of `allowReserved` has no effect. See also [Appendix C: Using RFC6570 Implementations](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

Note that the presence of at least one of `style`, `explode`, or `allowReserved` with an explicit value is equivalent to using `schema` with `in: "query"` Parameter Objects. The absence of all three of those fields is the equivalent of using `content`, but with the media type specified in `contentType` rather than through a Media Type Object.

#### 4.15.2 Nested Encoding

[](https://spec.openapis.org/oas/latest.html#nested-encoding)

Nested formats requiring encoding, most notably nested `multipart/mixed`, can be supported with this Object’s `encoding`, `prefixEncoding`, and / or `itemEncoding` fields. Implementations *MUST* support one level of nesting, and *MAY* support additional levels.

#### 4.15.3 Encoding the `x-www-form-urlencoded` Media Type

[](https://spec.openapis.org/oas/latest.html#encoding-the-x-www-form-urlencoded-media-type)

To work with content using form url encoding via \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\], use the `application/x-www-form-urlencoded` media type in the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object). This configuration means that the content *MUST* be percent-encoded per \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\]'s rules for that media type, after any complex objects have been serialized to a string representation.

See [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns for form media types.

##### 4.15.3.1 Example: URL Encoded Form with JSON Values

[](https://spec.openapis.org/oas/latest.html#example-url-encoded-form-with-json-values)

When there is no [`encoding`](https://spec.openapis.org/oas/latest.html#media-type-encoding) field, the serialization strategy is based on the Encoding Object’s default values:

```
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        type: object
        properties:
          id:
            type: string
            format: uuid
          address:
            type: object
            properties: {}
```

With this example, consider an `id` of `f81d4fae-7dec-11d0-a765-00a0c91e6bf6` and a US-style address (with ZIP+4) as follows:

```
{
  "streetAddress": "123 Example Dr.",
  "city": "Somewhere",
  "state": "CA",
  "zip": "99999+1234"
}
```

Assuming the most compact representation of the JSON value (with unnecessary whitespace removed), we would expect to see the following request body, where space characters have been replaced with `+` and `+`, `"`, `:`, `,`, `{`, and `}` have been percent-encoded to `%2B`, `%22`, `%3A`, `%2C`, `%7B`, and `%7D`, respectively:

```
id=f81d4fae-7dec-11d0-a765-00a0c91e6bf6&address=%7B%22streetAddress%22%3A%22123+Example+Dr.%22%2C%22city%22%3A%22Somewhere%22%2C%22state%22%3A%22CA%22%2C%22zip%22%3A%2299999%2B1234%22%7D
```

Note that the `id` keyword is treated as `text/plain` per the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)’s default behavior, and is serialized as-is. If it were treated as `application/json`, then the serialized value would be a JSON string including quotation marks, which would be percent-encoded as `%22`.

Here is the `id` parameter (without `address`) serialized as `application/json` instead of `text/plain`, and then encoded per \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\]'s `form-urlencoded` rules:

```
id=%22f81d4fae-7dec-11d0-a765-00a0c91e6bf6%22
```

##### 4.15.3.2 Example: URL Encoded Form with Binary Values

[](https://spec.openapis.org/oas/latest.html#example-url-encoded-form-with-binary-values)

Note that `application/x-www-form-urlencoded` is a text format, which requires base64-encoding any binary data:

```
requestBody:
  content:
    application/x-www-form-urlencoded:
      schema:
        type: object
        properties:
          name:
            type: string
          icon:
            # The default content type with `contentEncoding` present
            # is `application/octet-stream`, so we need to set the correct
            # image media type(s) in the Encoding Object.
            type: string
            contentEncoding: base64url
  encoding:
    icon:
      contentType: image/png, image/jpeg
```

Given a name of `example` and a solid red 2x2-pixel PNG for `icon`, this would produce a request body of:

```
name=example&icon=iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAABGdBTUEAALGPC_xhBQAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAAqADAAQAAAABAAAAAgAAAADO0J6QAAAAEElEQVQIHWP8zwACTGCSAQANHQEDqtPptQAAAABJRU5ErkJggg%3D%3D
```

Note that the `=` padding characters at the end need to be percent-encoded, even with the “URL safe” `contentEncoding: base64url`. Some base64-decoding implementations may be able to use the string without the padding per \[[RFC4648](https://spec.openapis.org/oas/latest.html#bib-rfc4648 "The Base16, Base32, and Base64 Data Encodings")\] [Section 3.2](https://datatracker.ietf.org/doc/html/rfc4648#section-3.2). However, this is not guaranteed, so it may be more interoperable to keep the padding and rely on percent-decoding.

#### 4.15.4 Encoding `multipart` Media Types

[](https://spec.openapis.org/oas/latest.html#encoding-multipart-media-types)

See [Encoding Usage and Restrictions](https://spec.openapis.org/oas/latest.html#encoding-usage-and-restrictions) for guidance on correlating schema properties with parts.

Note that there are significant restrictions on what headers can be used with `multipart` media types in general (\[[RFC2046](https://spec.openapis.org/oas/latest.html#bib-rfc2046 "Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types")\] [Section 5.1](https://datatracker.ietf.org/doc/html/rfc2046#section-5.1)) and `multi-part/form-data` in particular (\[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.8](https://datatracker.ietf.org/doc/html/rfc7578#section-4.8)).

##### 4.15.4.1 Handling Multiple `contentType` Values

[](https://spec.openapis.org/oas/latest.html#handling-multiple-contenttype-values)

When multiple values are provided for `contentType`, parsing remains straightforward as the part’s actual `Content-Type` is included in the document.

For encoding and serialization, implementations *MUST* provide a mechanism for applications to indicate which media type is intended. Implementations *MAY* choose to offer media type sniffing (\[[SNIFF](https://spec.openapis.org/oas/latest.html#bib-sniff "MIME Sniffing Standard")\]) as an alternative, but this *MUST NOT* be the default behavior due to the security risks inherent in the process.

##### 4.15.4.2 `Content-Transfer-Encoding` and `contentEncoding`

[](https://spec.openapis.org/oas/latest.html#content-transfer-encoding-and-contentencoding)

Using `contentEncoding` for a multipart field is equivalent to specifying an [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) with a `headers` field containing `Content-Transfer-Encoding` with a schema that requires the value used in `contentEncoding`. If `contentEncoding` is used for a multipart field that has an Encoding Object with a `headers` field containing `Content-Transfer-Encoding` with a schema that disallows the value from `contentEncoding`, the result is undefined for serialization and parsing.

Note that as stated in [Working with Binary Data](https://spec.openapis.org/oas/latest.html#working-with-binary-data), if the Encoding Object’s `contentType`, whether set explicitly or implicitly through its default value rules, disagrees with the `contentMediaType` in a Schema Object, the `contentMediaType` *SHALL* be ignored. Because of this, and because the Encoding Object’s `contentType` defaulting rules do not take the Schema Object’s`contentMediaType` into account, the use of `contentMediaType` with an Encoding Object is *NOT RECOMMENDED*.

Note also that `Content-Transfer-Encoding` is deprecated for `multipart/form-data` (\[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.7](https://datatracker.ietf.org/doc/html/rfc7578#section-4.7)) where binary data is supported, as it is in HTTP.

See [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns for form media types.

##### 4.15.4.3 Example: Basic Multipart Form

[](https://spec.openapis.org/oas/latest.html#example-basic-multipart-form)

When the `encoding` field is *not* used, the encoding is determined by the Encoding Object’s defaults:

```
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          # default content type for a string without `contentEncoding`
          # is `text/plain`
          id:
            type: string
            format: uuid

          # default content type for a schema without `type`
          # is `application/octet-stream`
          profileImage: {}

          # for arrays, the `encoding` field applies the Encoding Object
          # to each item individually and determines the default content type
          # based on the type in the `items` subschema, which in this example
          # is an object, so the default content type for each item is
          # `application/json`
          addresses:
            type: array
            items:
              $ref: '#/components/schemas/Address'
```

##### 4.15.4.4 Example: Multipart Form with Encoding Objects

[](https://spec.openapis.org/oas/latest.html#example-multipart-form-with-encoding-objects)

Using `encoding`, we can set more specific types for binary data, or non-JSON formats for complex values. We can also describe headers for each part:

```
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          # No Encoding Object, so use default `text/plain`
          id:
            type: string
            format: uuid

          # Encoding Object overrides the default `application/json` content type
          # for each item in the array with `application/xml; charset=utf-8`
          addresses:
            description: addresses in XML format
            type: array
            items:
              $ref: '#/components/schemas/Address'

          # Encoding Object accepts only PNG or JPEG, and also describes
          # a custom header for just this part in the multipart format
          profileImage: {}

      encoding:
        addresses:
          contentType: application/xml; charset=utf-8
        profileImage:
          contentType: image/png, image/jpeg
          headers:
            X-Rate-Limit-Limit:
              description: The number of allowed requests in the current period
              schema:
                type: integer
```

##### 4.15.4.5 Example: Multipart Form with Multiple Files

[](https://spec.openapis.org/oas/latest.html#example-multipart-form-with-multiple-files)

In accordance with \[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.3](https://datatracker.ietf.org/doc/html/rfc7578#section-4.3), multiple files for a single form field are uploaded using the same name (`file` in this example) for each file’s part:

```
requestBody:
  content:
    multipart/form-data:
      schema:
        properties:
          # The property name `file` will be used for all files.
          file:
            type: array
            items: {}
```

As seen in the [Encoding Object’s `contentType` field documentation](https://spec.openapis.org/oas/latest.html#encoding-content-type), the empty schema for `items` indicates a media type of `application/octet-stream`.

##### 4.15.4.6 Example: Ordered, Unnamed Multipart

[](https://spec.openapis.org/oas/latest.html#example-ordered-unnamed-multipart)

A `multipart/mixed` payload consisting of a JSON metadata document followed by an image which the metadata describes:

```
multipart/mixed:
  schema:
    type: array
    prefixItems:
    - # default content type for objects
      # is `application/json`
      type: object
      properties:
        author:
          type: string
        created:
          type: string
          format: datetime
        copyright:
          type: string
        license:
          type: string
    - # default content type for a schema without `type`
      # is `application/octet-stream`, which we need
      # to override.
      {}
  prefixEncoding:
  - # Encoding Object defaults are correct for JSON
    {}
  - contentType: image/*
```

##### 4.15.4.7 Example: Ordered Multipart With Required Header

[](https://spec.openapis.org/oas/latest.html#example-ordered-multipart-with-required-header)

As described in \[[RFC2557](https://spec.openapis.org/oas/latest.html#bib-rfc2557 "MIME Encapsulation of Aggregate Documents, such as HTML (MHTML)")\], a set of resources making up a web page can be sent in a `multipart/related` payload, preserving links from the `text/html` document to subsidiary resources such as scripts, style sheets, and images by defining a `Content-Location` header for each page. The first part is used as the root resource (unless using `Content-ID`, which RFC2557 advises against and is forbidden in this example), so we use `prefixItems` and `prefixEncoding` to define that it must be an HTML resource, and then allow any of several different types of resources in any order to follow.

The `Content-Location` header is defined using `content: {text/plain: {...}}` to avoid percent-encoding its URI value; see [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for further details.

```
components:
  headers:
    RFC2557NoContentId:
      description: Use Content-Location instead of Content-ID
      schema: false
    RFC2557ContentLocation:
      required: true
      content:
        text/plain:
          schema:
            $comment: Use a full URI (not a relative reference)
            type: string
            format: uri
  requestBodies:
    RFC2557:
      content:
        multipart/related; type=text/html:
          schema:
            prefixItems:
            - type: string
            items:
              anyOf:
              - type: string
              - $comment: To allow binary, this must always pass
          prefixEncoding:
          - contentType: text/html
            headers:
              Content-ID:
                $ref: '#/components/headers/RFC2557NoContentId'
              Content-Location:
                $ref: '#/components/headers/RFC2557ContentLocation'
          itemEncoding:
            contentType: text/css,text/javascript,image/*
            headers:
              Content-ID:
                $ref: '#/components/headers/RFC2557NoContentId'
              Content-Location:
                $ref: '#/components/headers/RFC2557ContentLocation'
```

##### 4.15.4.8 Example: Streaming Multipart

[](https://spec.openapis.org/oas/latest.html#example-streaming-multipart)

This example assumes a device that takes large sets of pictures and streams them to the caller. Unlike the previous example, we use `itemSchema` here because the expectation is that each image is processed as it arrives (or in small batches), since we know that buffering the entire stream will take too much memory.

```
multipart/mixed:
  itemSchema:
    $comment: A single data image from the device
  itemEncoding:
    contentType: image/jpg
```

##### 4.15.4.9 Example: Streaming Byte Ranges

[](https://spec.openapis.org/oas/latest.html#example-streaming-byte-ranges)

For `multipart/byteranges` \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 14.6](https://tools.ietf.org/html/rfc9110#section-14.6), a `Content-Range` header is required:

See [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for an explanation of why `content: {text/plain: {...}}` is used to describe the header value.

```
multipart/byteranges:
  itemSchema:
    $comment: A single range of bytes from a video
  itemEncoding:
    contentType: video/mp4
    headers:
      Content-Range:
        required: true
        content:
          text/plain:
            schema:
              # The `pattern` regular expression that would
              # be included in practice is omitted for simplicity
              type: string
```

##### 4.15.4.10 Example: Nested `multipart/mixed`

[](https://spec.openapis.org/oas/latest.html#example-nested-multipart-mixed)

This defines a two-part `multipart/mixed` where the first part is a JSON array and the second part is a nested `multipart/mixed` document. The nested parts are XML, plain text, and a PNG image.

```
multipart/mixed:
  schema:
    type: array
    prefixItems:
    - type: array
    - type: array
      prefixItems:
      - type: object
      - type: string
      - {}
  prefixEncoding:
    - {} # Accept the default application/json
    - contentType: multipart/mixed
      prefixEncoding:
      - contentType: application/xml
      - {} # Accept the default text/plain
      - contentType: image/png
```

### 4.16 Responses Object

[](https://spec.openapis.org/oas/latest.html#responses-object)

A container for the expected responses of an operation. The container maps a HTTP response code to the expected response.

The documentation is not necessarily expected to cover all possible HTTP response codes because they may not be known in advance. However, documentation is expected to cover a successful operation response and any known errors.

The `default` *MAY* be used as a default Response Object for all HTTP codes that are not covered individually by the Responses Object.

The Responses Object *MUST* contain at least one response code, and if only one response code is provided it *SHOULD* be the response for a successful operation call.

#### 4.16.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-13)

| Field Name | Type | Description |
| --- | --- | --- |
| default | [Response Object](https://spec.openapis.org/oas/latest.html#response-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object) | The documentation of responses other than the ones declared for specific HTTP response codes. Use this field to cover undeclared responses. |

#### 4.16.2 Patterned Fields

[](https://spec.openapis.org/oas/latest.html#patterned-fields-0)

| Field Pattern | Type | Description |
| --- | --- | --- |
| [HTTP Status Code](https://spec.openapis.org/oas/latest.html#http-status-codes) | [Response Object](https://spec.openapis.org/oas/latest.html#response-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object) | Any [HTTP status code](https://spec.openapis.org/oas/latest.html#http-status-codes) can be used as the property name, but only one property per code, to describe the expected response for that HTTP status code. This field *MUST* be enclosed in quotation marks (for example, “200”) for compatibility between JSON and YAML. To define a range of response codes, this field *MAY* contain the uppercase wildcard character `X`. For example, `2XX` represents all response codes between `200` and `299`. Only the following range definitions are allowed: `1XX`, `2XX`, `3XX`, `4XX`, and `5XX`. If a response is defined using an explicit code, the explicit code definition takes precedence over the range definition for that code. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.16.3 HTTP Status Codes

[](https://spec.openapis.org/oas/latest.html#http-status-codes)

The HTTP Status Codes are used to indicate the status of the executed operation. Status codes *SHOULD* be selected from the available status codes registered in the [IANA Status Code Registry](https://spec.openapis.org/oas/latest.html#bib-iana-http-status-codes "Hypertext Transfer Protocol (HTTP) Status Code Registry").

#### 4.16.4 Responses Object Example

[](https://spec.openapis.org/oas/latest.html#responses-object-example)

A 200 response for a successful operation and a default response for others (implying an error):

```
'200':
  description: a pet to be returned
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/Pet'
default:
  description: Unexpected error
  content:
    application/json:
      schema:
        $ref: '#/components/schemas/ErrorModel'
```

### 4.17 Response Object

[](https://spec.openapis.org/oas/latest.html#response-object)

Describes a single response from an API operation, including design-time, static `links` to operations based on the response.

#### 4.17.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-14)

| Field Name | Type | Description |
| --- | --- | --- |
| summary | `string` | A short summary of the meaning of the response. |
| description | `string` | A description of the response. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| headers | Map\[`string`, [Header Object](https://spec.openapis.org/oas/latest.html#header-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | Maps a header name to its definition. \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 5.1](https://datatracker.ietf.org/doc/html/rfc9110#section-5.1) states header names are case-insensitive. If a response header is defined with the name `"Content-Type"`, it *SHALL* be ignored. |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A map containing descriptions of potential response payloads. The key is a media type or [media type range](https://tools.ietf.org/html/rfc9110#appendix-A) and the value describes it. For responses that match multiple keys, only the most specific key is applicable. e.g. `"text/plain"` overrides `"text/*"` |
| links | Map\[`string`, [Link Object](https://spec.openapis.org/oas/latest.html#link-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A map of operations links that can be followed from the response. The key of the map is a short name for the link, following the naming constraints of the names for [Component Objects](https://spec.openapis.org/oas/latest.html#components-object). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.17.2 Response Object Examples

[](https://spec.openapis.org/oas/latest.html#response-object-examples)

Response of an array of a complex type:

```
description: A complex object array response
content:
  application/json:
    schema:
      type: array
      items:
        $ref: '#/components/schemas/VeryComplexType'
```

Response with a string type:

```
description: A simple string response
content:
  text/plain:
    schema:
      type: string
```

Plain text response with headers:

```
description: A simple string response
content:
  text/plain:
    schema:
      type: string
    example: 'whoa!'
headers:
  X-Rate-Limit-Limit:
    description: The number of allowed requests in the current period
    schema:
      type: integer
  X-Rate-Limit-Remaining:
    description: The number of remaining requests in the current period
    schema:
      type: integer
  X-Rate-Limit-Reset:
    description: The number of seconds left in the current period
    schema:
      type: integer
```

Response with no return value:

```
description: object created
```

### 4.18 Callback Object

[](https://spec.openapis.org/oas/latest.html#callback-object)

A map of possible out-of band callbacks related to the parent operation. Each value in the map is a [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object) that describes a set of requests that may be initiated by the API provider and the expected responses. The key value used to identify the Path Item Object is an expression, evaluated at runtime, that identifies a URL to use for the callback operation.

To describe incoming requests from the API provider independent from another API call, use the [`webhooks`](https://spec.openapis.org/oas/latest.html#oas-webhooks) field.

#### 4.18.1 Patterned Fields

[](https://spec.openapis.org/oas/latest.html#patterned-fields-1)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {expression} | [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object) | A Path Item Object used to define a callback request and expected responses. A [complete example](https://learn.openapis.org/examples/v3.0/callback-example.html) is available. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.18.2 Key Expression

[](https://spec.openapis.org/oas/latest.html#key-expression)

The key that identifies the [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object) is a [runtime expression](https://spec.openapis.org/oas/latest.html#runtime-expressions) that can be evaluated in the context of a runtime HTTP request/response to identify the URL to be used for the callback request. A simple example might be `$request.body#/url`. However, using a [runtime expression](https://spec.openapis.org/oas/latest.html#runtime-expressions) the complete HTTP message can be accessed. This includes accessing any part of a body that a JSON Pointer \[[RFC6901](https://spec.openapis.org/oas/latest.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\] can reference.

For example, given the following HTTP request:

```
POST /subscribe/myevent?queryUrl=https://clientdomain.com/stillrunning HTTP/1.1
Host: example.org
Content-Type: application/json
Content-Length: 188

{
  "failedUrl": "https://clientdomain.com/failed",
  "successUrls": [
    "https://clientdomain.com/fast",
    "https://clientdomain.com/medium",
    "https://clientdomain.com/slow"
  ]
}
```

resulting in:

```
201 Created
Location: https://example.org/subscription/1
```

The following examples show how the various expressions evaluate, assuming the callback operation has a path parameter named `eventType` and a query parameter named `queryUrl`.

| Expression | Value |
| --- | --- |
| $url | [https://example.org/subscribe/myevent?queryUrl=https://clientdomain.com/stillrunning](https://example.org/subscribe/myevent?queryUrl=https://clientdomain.com/stillrunning) |
| $method | POST |
| $request.path.eventType | myevent |
| $request.query.queryUrl | [https://clientdomain.com/stillrunning](https://clientdomain.com/stillrunning) |
| $request.header.content-type | application/json |
| $request.body#/failedUrl | [https://clientdomain.com/failed](https://clientdomain.com/failed) |
| $request.body#/successUrls/1 | [https://clientdomain.com/medium](https://clientdomain.com/medium) |
| $response.header.Location | [https://example.org/subscription/1](https://example.org/subscription/1) |

#### 4.18.3 Callback Object Examples

[](https://spec.openapis.org/oas/latest.html#callback-object-examples)

The following example uses the user provided `queryUrl` query string parameter to define the callback URL. This is similar to a [webhook](https://spec.openapis.org/oas/latest.html#oas-webhooks), but differs in that the callback only occurs because of the initial request that sent the `queryUrl`.

```
myCallback:
  '{$request.query.queryUrl}':
    post:
      requestBody:
        description: Callback payload
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SomePayload'
      responses:
        '200':
          description: callback successfully processed
```

The following example shows a callback where the server is hard-coded, but the query string parameters are populated from the `id` and `email` property in the request body.

```
transactionCallback:
  'http://notificationServer.com?transactionId={$request.body#/id}&email={$request.body#/email}':
    post:
      requestBody:
        description: Callback payload
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SomePayload'
      responses:
        '200':
          description: callback successfully processed
```

### 4.19 Example Object

[](https://spec.openapis.org/oas/latest.html#example-object)

An object grouping an internal or external example value with basic `summary` and `description` metadata. The examples can show either data suitable for schema validation, or serialized data as required by the containing [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object), [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object), or [Header Object](https://spec.openapis.org/oas/latest.html#header-object). This object is typically used in fields named `examples` (plural), and is a [referenceable](https://spec.openapis.org/oas/latest.html#reference-object) alternative to older `example` (singular) fields that do not support referencing or metadata. The various fields and types of examples are explained in more detail under [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples).

#### 4.19.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-15)

| Field Name | Type | Description |
| --- | --- | --- |
| summary | `string` | Short description for the example. |
| description | `string` | Long description for the example. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| dataValue | Any | An example of the data structure that *MUST* be valid according to the relevant [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object). If this field is present, `value` *MUST* be absent. |
| serializedValue | `string` | An example of the serialized form of the value, including encoding and escaping as described under [Validating Examples](https://spec.openapis.org/oas/latest.html#validating-examples). If `dataValue` is present, then this field *SHOULD* contain the serialization of the given data. Otherwise, it *SHOULD* be the valid serialization of a data value that itself *MUST* be valid as described for `dataValue`. This field *SHOULD NOT* be used if the serialization format is JSON, as the data form is easier to work with. If this field is present, `value`, and `externalValue` *MUST* be absent. |
| externalValue | `string` | A URI that identifies the serialized example in a separate document, allowing for values not easily or readably expressed as a Unicode string. If `dataValue` is present, then this field *SHOULD* identify a serialization of the given data. Otherwise, the value *SHOULD* be the valid serialization of a data value that itself *MUST* be valid as described for `dataValue`. If this field is present, `serializedValue` and `value` *MUST* be absent. See also the rules for resolving [Relative References](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris). |
| value | Any | Embedded literal example. The `value` field and `externalValue` field are mutually exclusive. To represent examples of media types that cannot naturally be represented in JSON or YAML, use a string value to contain the example, escaping where necessary.

**Deprecated for non-JSON serialization targets:** Use `dataValue` and/or `serializedValue`, which both have unambiguous syntax and semantics, instead. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

In all cases, the example value *SHOULD* be compatible with the schema of its associated value. Tooling implementations *MAY* choose to validate compatibility automatically, and reject the example value(s) if incompatible. See [Validating Examples](https://spec.openapis.org/oas/latest.html#validating-examples) for the exact meaning of “compatible” for each field in this Object.

#### 4.19.2 Working with Examples

[](https://spec.openapis.org/oas/latest.html#working-with-examples)

Example Objects can be used in [Parameter Objects](https://spec.openapis.org/oas/latest.html#parameter-object), [Header Objects](https://spec.openapis.org/oas/latest.html#header-object), and [Media Type Objects](https://spec.openapis.org/oas/latest.html#media-type-object). In all three Objects, this is done through the `examples` (plural) field. However, there are several other ways to provide examples: The `example` (singular) field that is mutually exclusive with `examples` in all three Objects, and two keywords (the deprecated singular `example` and the current plural `examples`, which takes an array of examples) in the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) that appears in the `schema` field of all three Objects. We will refer to the singular `example` field in the Parameter, Header, or Media Type Object, which has the same behavior as a single Example Object with only the `value` field, as the “shorthand `example`” field. Each of these fields has slightly different considerations.

##### 4.19.2.1 JSON-Compatible and `value`\-Safe Examples

[](https://spec.openapis.org/oas/latest.html#json-compatible-and-value-safe-examples)

The `value` and the shorthand `example` field are intended to have the same *semantics* as `serializedValue` (or `externalValue`), while allowing a more convenient *syntax* when there is no difference between a JSON (or [JSON-compatible YAML](https://spec.openapis.org/oas/latest.html#format)) representation and the final serialized form. When using this syntax for `application/json` or any `+json` media type, these fields effectively behave like `dataValue`, as the serialization is trivial, and they are safe to use.

For data that consists of a single string, and a serialization target such as `text/plain` where the string is guaranteed to be serialized without any further escaping, these fields are also safe to use.

For other serialization targets, the ambiguity of the phrase “naturally be represented in JSON or YAML,” as well as past errors in the parameter style examples table, have resulted in inconsistencies in the support and usage of these fields. In practice, this has resulted in the `value` and shorthand `example` fields having implementation-defined behavior for non-JSON targets; OAD authors *SHOULD* use other fields to ensure interoperability.

##### 4.19.2.2 Choosing Which Field(s) to Use

[](https://spec.openapis.org/oas/latest.html#choosing-which-field-s-to-use)

Keeping in mind the caveats from the previous section, and that the shorthand `example` can be used in place of `value` if there is only one Example Object involved, use the following guidelines to determine which field to use.

To show an example as it would be validated by a Schema Object:

-   Use the Schema Object’s `examples` array (from JSON Schema draft 2020-12) if the intent is to keep the example with the validating schema.
    -   Use the Schema Object’s `example` (singular) only if compatibility with OAS v3.0 or earlier is required.
-   Use the Example Object’s `dataValue` field if the intent is to associate the example with an example of its serialization, or if it is desirable to maintain it separately from the schema.
    -   Use the Example Object’s `value` field only if compatibility with OAS v3.1 or earlier is needed and the value can be “naturally represented in JSON or YAML” without any changes (such as percent-encoding) between the validation-ready value and the serialized representation.

To show an example as it would be serialized in order to construct an HTTP/1.1 message:

-   Use the Example Object’s `serializedValue` if the serialization can be represented as a valid Unicode string, and there is no need to demonstrate the exact character encoding to be used.
    -   Use the string form of `value` only if compatibility with OAS v3.1 or earlier is needed.
-   Use the Example Object’s `externalValue` for all other values, or if it is desirable to maintain the example separately from the OpenAPI document.

The `serializedValue` and `externalValue` fields both *MUST* show the serialized form of the data. For Media Type Objects, this is a document of the appropriate media type, with any Encoding Object effects applied. For Parameter and Header Objects using `schema` and `style` rather than a Media Type Object, see [Style Examples](https://spec.openapis.org/oas/latest.html#style-examples) for what constitutes a serialized value.

##### 4.19.2.3 Criteria for `serializedExample`

[](https://spec.openapis.org/oas/latest.html#criteria-for-serializedexample)

A serialization can be represented as a valid Unicode string in `serializedValue` if any of the following are true of the serialization:

-   It is for a media type that supports a `charset` parameter that indicates any Unicode encoding (UTF-8, UTF-16, etc.), or any valid subset of such an encoding, such as US-ASCII.
-   It is for a format (such as URIs or HTTP fields) or character-based media type that requires or defaults to a Unicode encoding, or any valid subset of such an encoding, such as US-ASCII, and this is not overridden by `charset`.
-   It is for a compound format where all parts meet at least one of the above criteria, e.g. a `multipart/mixed` media type with parts that are `application/json` (a media type that defaults to UTF-8) and `application/xml; charset=utf-8` (a media type with an explicit `charset` parameter).

In all of these cases, the conversion from the character set of the OAD (presumed to be UTF-8 as the only interoperable character set for JSON, and therefore also for JSON-compatible YAML as noted in \[[RFC9512](https://spec.openapis.org/oas/latest.html#bib-rfc9512 "YAML Media Type")\] [Section 3.4](https://tools.ietf.org/html/rfc9512#section-3.4)) first to Unicode code points and then to the actual serialization character set is well-defined.

For `externalValue`, if the character set is neither explicitly stated nor determined by the format or media type specification, implementations *SHOULD* assume UTF-8.

##### 4.19.2.4 Validating Examples

[](https://spec.openapis.org/oas/latest.html#validating-examples)

Tooling implementations *MAY* choose to validate compatibility automatically, and reject the example value(s) if incompatible. For examples that are in schema-ready data form, this is straightforward.

With serialized examples, some formats allow multiple possible valid representations of the same data, including in scenarios noted in [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion). In some cases, parsing the serialized example and validating the resulting data can eliminate the ambiguity, but in a few cases parsing is also ambiguous. Therefore, OAD authors are cautioned that validation of certain serialized examples is by necessity a best-effort feature.

#### 4.19.3 Example Object Examples

[](https://spec.openapis.org/oas/latest.html#example-object-examples)

##### 4.19.3.1 JSON Examples

[](https://spec.openapis.org/oas/latest.html#json-examples)

When writing in YAML, JSON syntax can be used for `dataValue` (as shown in the `noRating` example) but is not required. While this example shows the behavior of both `dataValue` and `serializedValue` for JSON (in the 'withRating\` example), in most cases only the data form is needed.

```
content:
  application/json:
    schema:
      type: object
      required:
      - author
      - title
      properties:
        author:
          type: string
        title:
          type: string
        rating:
          type: number
          minimum: 1
          maximum: 5
          multipleOf: 0.5
    examples:
      noRating:
        summary: A not-yet-rated work
        dataValue:
          author: A. Writer
          title: The Newest Book
      withRating:
        summary: A work with an average rating of 4.5 stars
        dataValue:
          author: A. Writer
          title: An Older Book
          rating: 4.5
        serializedValue: |
          {
            "author": "A. Writer",
            "title": "An Older Book",
            "rating": 4.5
          }
```

##### 4.19.3.2 Binary Examples

[](https://spec.openapis.org/oas/latest.html#binary-examples)

Fully binary data is shown using `externalValue`:

```
content:
  image/png:
    schema: {}
    examples:
      Red:
        externalValue: ./examples/2-by-2-red-pixels.png
```

##### 4.19.3.3 Boolean Query Parameter Examples

[](https://spec.openapis.org/oas/latest.html#boolean-query-parameter-examples)

Since there is no standard for serializing boolean values (as discussed in [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion)), this example uses `dataValue` and `serializedValue` to show how booleans are serialized for this particular parameter:

```
name: flag
in: query
required: true
schema:
  type: boolean
examples:
  "true":
    dataValue: true
    serializedValue: flag=true
  "false":
    dataValue: false
    serializedValue: flag=false
```

### 4.20 Link Object

[](https://spec.openapis.org/oas/latest.html#link-object)

The Link Object represents a possible design-time link for a response. The presence of a link does not guarantee the caller’s ability to successfully invoke it, rather it provides a known relationship and traversal mechanism between responses and other operations.

Unlike *dynamic* links (i.e. links provided **in** the response payload), the OAS linking mechanism does not require link information in the runtime response.

For computing links and providing instructions to execute them, a [runtime expression](https://spec.openapis.org/oas/latest.html#runtime-expressions) is used for accessing values in an operation and using them as parameters while invoking the linked operation.

#### 4.20.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-16)

| Field Name | Type | Description |
| --- | --- | --- |
| operationRef | `string` | A URI reference to an OAS operation. This field is mutually exclusive of the `operationId` field, and *MUST* point to an [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object). Relative `operationRef` values *MAY* be used to locate an existing [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) in the OpenAPI Description. |
| operationId | `string` | The name of an *existing*, resolvable OAS operation, as defined with a unique `operationId`. This field is mutually exclusive of the `operationRef` field. |
| parameters | Map\[`string`, Any | [{expression}](https://spec.openapis.org/oas/latest.html#runtime-expressions)\] | A map representing parameters to pass to an operation as specified with `operationId` or identified via `operationRef`. The key is the parameter name to be used (optionally qualified with the parameter location, e.g. `path.id` for an `id` parameter in the path), whereas the value can be a constant or an expression to be evaluated and passed to the linked operation. |
| requestBody | Any | [{expression}](https://spec.openapis.org/oas/latest.html#runtime-expressions) | A literal value or [{expression}](https://spec.openapis.org/oas/latest.html#runtime-expressions) to use as a request body when calling the target operation. |
| description | `string` | A description of the link. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| server | [Server Object](https://spec.openapis.org/oas/latest.html#server-object) | A server object to be used by the target operation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

A linked operation *MUST* be identified using either an `operationRef` or `operationId`. The identified or referenced operation *MUST* be unique, and in the case of an `operationId`, it *MUST* be resolved within the scope of the OpenAPI Description (OAD). Because of the potential for name clashes, the `operationRef` syntax is preferred for multi-document OADs. However, because use of an operation depends on its URL path template in the [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object), operations from any [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object) that is referenced multiple times within the OAD cannot be resolved unambiguously. In such ambiguous cases, the resulting behavior is implementation-defined and *MAY* result in an error.

Note that it is not possible to provide a constant value to `parameters` that matches the syntax of a runtime expression. It is possible to have ambiguous parameter names, e.g. `name: "id", in: "path"` and `name: "path.id", in: "query"`; this is *NOT RECOMMENDED* and the behavior is implementation-defined, however implementations *SHOULD* prefer the qualified interpretation (`path.id` as a path parameter), as the names can always be qualified to disambiguate them (e.g. using `query.path.id` for the query parameter).

#### 4.20.2 Examples

[](https://spec.openapis.org/oas/latest.html#examples)

Computing a link from a request operation where the `$request.path.id` is used to pass a request parameter to the linked operation.

```
paths:
  /users/{id}:
    parameters:
      - name: id
        in: path
        required: true
        description: the user identifier, as userId
        schema:
          type: string
    get:
      responses:
        '200':
          description: the user being returned
          content:
            application/json:
              schema:
                type: object
                properties:
                  uuid: # the unique user id
                    type: string
                    format: uuid
          links:
            address:
              # the target link operationId
              operationId: getUserAddress
              parameters:
                # get the `id` field from the request path parameter named "id"
                userid: $request.path.id
  # the path item of the linked operation
  /users/{userid}/address:
    parameters:
      - name: userid
        in: path
        required: true
        description: the user identifier, as userId
        schema:
          type: string
    # linked operation
    get:
      operationId: getUserAddress
      responses:
        '200':
          description: the user's address
```

When a runtime expression fails to evaluate, no parameter value is passed to the target operation.

Values from the response body can be used to drive a linked operation.

```
links:
  address:
    operationId: getUserAddressByUUID
    parameters:
      # get the `uuid` field from the `uuid` field in the response body
      userUuid: $response.body#/uuid
```

Clients follow all links at their discretion. Neither permissions nor the capability to make a successful call to that link is guaranteed solely by the existence of a relationship.

##### 4.20.2.1 `operationRef` Examples

[](https://spec.openapis.org/oas/latest.html#operationref-examples)

As the `operationId` is an optional field in an [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object), references *MAY* instead be made through a URI reference with `operationRef`. Note that both of these examples reference operations that can be identified via the [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object) to ensure that the operation’s path template is unambiguous.

A relative URI reference `operationRef`:

```
links:
  UserRepositories:
    # returns array of '#/components/schemas/repository'
    operationRef: '#/paths/~12.0~1repositories~1%7Busername%7D/get'
    parameters:
      username: $response.body#/username
```

A non-relative URI `operationRef`:

```
links:
  UserRepositories:
    # returns array of '#/components/schemas/repository'
    operationRef: https://na2.gigantic-server.com/#/paths/~12.0~1repositories~1%7Busername%7D/get
    parameters:
      username: $response.body#/username
```

Note that in the use of `operationRef` the *escaped forward-slash* (`~1`) is necessary when using JSON Pointer in URI fragments, and it is necessary to URL-encode `{` and `}` as `%7B` and `%7D`, respectively. The unescaped, percent-decoded path template in the above examples would be `/2.0/repositories/{username}`.

#### 4.20.3 Runtime Expressions

[](https://spec.openapis.org/oas/latest.html#runtime-expressions)

Runtime expressions allow defining values based on information that will only be available within the HTTP message in an actual API call. This mechanism is used by [Link Objects](https://spec.openapis.org/oas/latest.html#link-object) and [Callback Objects](https://spec.openapis.org/oas/latest.html#callback-object).

The runtime expression is defined by the following \[[ABNF](https://spec.openapis.org/oas/latest.html#bib-abnf "Augmented BNF for Syntax Specifications: ABNF")\] syntax

```
    expression = "$url" / "$method" / "$statusCode" / "$request." source / "$response." source
    source     = header-reference / query-reference / path-reference / body-reference
    header-reference = "header." token
    query-reference  = "query." name
    path-reference   = "path." name
    body-reference   = "body" ["#" json-pointer ]
    json-pointer    = *( "/" reference-token )
    reference-token = *( unescaped / escaped )
    unescaped       = %x00-2E / %x30-7D / %x7F-10FFFF
                    ; %x2F ('/') and %x7E ('~') are excluded from 'unescaped'
    escaped         = "~" ( "0" / "1" )
                    ; representing '~' and '/', respectively
    name = *char
    token = 1*tchar
    tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*" / "+" / "-" / "."
          / "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA
```

Here, `json-pointer` is taken from \[[RFC6901](https://spec.openapis.org/oas/latest.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\], `char` from \[[RFC8259](https://spec.openapis.org/oas/latest.html#bib-rfc8259 "The JavaScript Object Notation (JSON) Data Interchange Format")\] [Section 7](https://datatracker.ietf.org/doc/html/rfc8259#section-7) and `token` from \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 5.6.2](https://datatracker.ietf.org/doc/html/rfc9110#section-5.6.2).

The `name` identifier is case-sensitive, whereas `token` is not.

The table below provides examples of runtime expressions and examples of their use in a value:

##### 4.20.3.1 Example Expressions

[](https://spec.openapis.org/oas/latest.html#example-expressions)

| Source Location | example expression | notes |
| --- | --- | --- |
| HTTP Method | `$method` | The allowable values for the `$method` will be those for the HTTP operation. |
| Requested media type | `$request.header.accept` |  |
| Request parameter | `$request.path.id` | Request parameters *MUST* be declared in the `parameters` section of the parent operation or they cannot be evaluated. This includes request headers. |
| Request body property | `$request.body#/user/uuid` | In operations which accept payloads, references may be made to portions of the `requestBody` or the entire body. |
| Request URL | `$url` |  |
| Response value | `$response.body#/status` | In operations which return payloads, references may be made to portions of the response body or the entire body. |
| Response header | `$response.header.Server` | Single header values only are available |

Runtime expressions preserve the type of the referenced value. Expressions can be embedded into string values by surrounding the expression with `{}` curly braces.

### 4.21 Header Object

[](https://spec.openapis.org/oas/latest.html#header-object)

Describes a single header for [HTTP responses](https://spec.openapis.org/oas/latest.html#response-headers) and for [individual parts in `multipart` representations](https://spec.openapis.org/oas/latest.html#encoding-headers); see the relevant [Response Object](https://spec.openapis.org/oas/latest.html#response-object) and [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) documentation for restrictions on which headers can be described.

The Header Object follows the structure of the [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object), including determining its serialization strategy based on whether `schema` or `content` is present, with the following changes:

1.  `name` *MUST NOT* be specified, it is given in the corresponding `headers` map.
2.  `in` *MUST NOT* be specified, it is implicitly in `header`.
3.  All traits that are affected by the location *MUST* be applicable to a location of `header` (for example, [`style`](https://spec.openapis.org/oas/latest.html#parameter-style)). This means that `allowEmptyValue` *MUST NOT* be used, and `style`, if used, *MUST* be limited to `"simple"`.

#### 4.21.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-17)

##### 4.21.1.1 Common Fixed Fields

[](https://spec.openapis.org/oas/latest.html#common-fixed-fields-1)

These fields *MAY* be used with either `content` or `schema`.

The `example` and `examples` fields are mutually exclusive; see [Working with Examples](https://spec.openapis.org/oas/latest.html#working-with-examples) for guidance on validation requirements.

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A brief description of the header. This could contain examples of use. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| required | `boolean` | Determines whether this header is mandatory. The default value is `false`. |
| deprecated | `boolean` | Specifies that the header is deprecated and *SHOULD* be transitioned out of usage. Default value is `false`. |
| example | Any | Example of the header’s potential value; see [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples). |
| examples | Map\[ `string`, [Example Object](https://spec.openapis.org/oas/latest.html#example-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | Examples of the header’s potential value; see [Working With Examples](https://spec.openapis.org/oas/latest.html#working-with-examples). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

##### 4.21.1.2 Fixed Fields for use with `schema`

[](https://spec.openapis.org/oas/latest.html#fixed-fields-for-use-with-schema-0)

For simpler scenarios, a [`schema`](https://spec.openapis.org/oas/latest.html#header-schema) and [`style`](https://spec.openapis.org/oas/latest.html#header-style) can describe the structure and syntax of the header.

When serializing headers with `schema`, URI percent-encoding *MUST NOT* be applied; if using an RFC6570 implementation that automatically applies it, it *MUST* be removed before use. Implementations *MUST* pass header values through unchanged rather than attempting to automatically quote header values, as the quoting rules vary too widely among different headers; see [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for guidance on quoting and escaping.

| Field Name | Type | Description |
| --- | --- | --- |
| style | `string` | Describes how the header value will be serialized. The default (and only legal value for headers) is `"simple"`. |
| explode | `boolean` | When this is true, header values of type `array` or `object` generate a single header whose value is a comma-separated list of the array items or key-value pairs of the map, see [Style Examples](https://spec.openapis.org/oas/latest.html#style-examples). For other data types this field has no effect. The default value is `false`. |
| schema | [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) | The schema defining the type used for the header. |

See also [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

##### 4.21.1.3 Fixed Fields for use with `content`

[](https://spec.openapis.org/oas/latest.html#fixed-fields-for-use-with-content-0)

For more complex scenarios, the [`content`](https://spec.openapis.org/oas/latest.html#header-content) field can define the media type and schema of the header, as well as give examples of its use.

| Field Name | Type | Description |
| --- | --- | --- |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) | [Reference Object](https://spec.openapis.org/oas/latest.html#reference-object)\] | A map containing the representations for the header. The key is the media type and the value describes it. The map *MUST* only contain one entry. |

#### 4.21.2 Modeling Link Headers

[](https://spec.openapis.org/oas/latest.html#modeling-link-headers)

\[[RFC9264](https://spec.openapis.org/oas/latest.html#bib-rfc9264 "Linkset: Media Types and a Link Relation Type for Link Sets")\] defines the `application/linkset` and `application/linkset+json` media types. The former is exactly the format of HTTP link header values except allowing additional whitespace for readability, while the latter is an equivalent JSON representation of such headers.

To use either of these media types, the `schema` in the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) *MUST* describe the links as they would be structured in the `application/linkset+json` format. If the Media Type Object’s parent key is `application/linkset+json`, then the serialization is trivial, however this format cannot be used in the HTTP `Link` header. If the Media Type Object’s parent key is `application/linkset`, then the serialization *MUST* be the equivalent representation of the `schema`\-modeled links in the `application/linkset` format. If the `application/linkset` Media Type Object is used in the `content` field of a Header Object (or a Parameter Object with `in: "header"`), the serialization *MUST* be made compatible with the HTTP field syntax as described by \[[RFC9264](https://spec.openapis.org/oas/latest.html#bib-rfc9264 "Linkset: Media Types and a Link Relation Type for Link Sets")\] [Section 4.1](https://tools.ietf.org/html/rfc9264#name-http-link-document-format-a).

The following example shows how the same data model can be used for a collection pagination linkset either in JSON format as message content, or in the HTTP `Link` header:

```
components:
  schemas:
    SimpleLinkContext:
      type: array
      items:
        type: object
        required:
        - href
        properties:
          href:
            type: string
            format: uri-reference
    CollectionLinks:
      type: object
      required:
      - linkset
      properties:
        linkset:
          type: array
          items:
            type: object
            required: [first, prev, next, last]
            properties:
              anchor:
                type: string
                format: uri
            additionalProperties:
              $ref: '#/components/schemas/SimpleLinkContext'
  responses:
    CollectionWithLinks:
      content:
        application/json:
          schema:
            type: array
      headers:
        Link:
          required: true
          content:
            application/linkset:
              schema:
                $ref: '#/components/schemas/CollectionLinks'
    StandaloneJsonLinkset:
      content:
        application/linkset+json:
          schema:
            $ref: '#/components/mediaTypes/CollectionLinks'
```

#### 4.21.3 Representing the `Set-Cookie` Header

[](https://spec.openapis.org/oas/latest.html#representing-the-set-cookie-header)

The `Set-Cookie` header is noted in \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 5.3](https://tools.ietf.org/html/rfc9110#section-5.3) as an exception to the normal rules of headers with multiple values.

For most headers using the general syntax defined in RFC9110, the multiple-line and comma-separated single-line forms are interchangeable, meaning that this:

```
Accept-Encoding: compress;q=0.5
Accept-Encoding: gzip;q=1.0
```

is interchangeable with the one-line form that works well with the OAS’s `style: "simple"` option:

```
Accept-Encoding: compress;q=0.5,gzip;q=1.0
```

The OAS models such multi-value headers using the one-line form as it matches the behavior of `style: "simple"`, and works well when using `content` as the values are completely separate from the header name, but it does not matter which form is used in an actual HTTP message.

As also noted in the RFC, `Set-Cookie` is an exception as it allows unquoted, non-escaped commas in its values, and can only use the one-value-per-line form. For HTTP messages, this is purely a serialization concern, and no more of a problem than a message that uses the multi-line form of any other header.

However, because examples and values modeled with `content` do not incorporate the header name, for these fields `Set-Cookie` *MUST* be handled by placing each value on a separate line, without the header name or the `:` delimiter.

Note also that any URI percent-encoding, base64 encoding, or other escaping *MUST* be performed prior to supplying the data to OAS tooling; see [Appendix D](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies) for details.

The following example shows two different ways to describe `Set-Cookie` headers that require cookies named `"lang"` and `"foo"`, as well as a `"urlSafeData"` cookie that is expected to be percent-encoded. The first uses `content` in order to show exactly how such examples are formatted, but also notes the limitations of schema constraints with multi-line text. The second shows the use of `style: "simple"`, which produces the same serialized example text (with each line corresponding to one `Set-Cookie:` line in the HTTP response), but allows schema constraints on each cookie; note that the percent-encoding is already applied in the `dataValue` field of the example:

```
components:
  headers:
    SetCookieWithContent:
      content:
        text/plain:
          schema:
            # Due to lack of support for multiline regular expressions
            # in the `pattern` keyword, not much validation can be done.
            type: string
      examples:
        WithExpires:
          # This demonstrates that the text is required to be provided
          # in the final format, and is not changed by serialization.
          # In practice, it is not necessary to show both value fields.
          # Note that only the comma (%2C) would need to be percent-encoded
          # if percent-encoding were only being done to make the value
          # a valid cookie, as space (%20) and the exclamation point (%21)
          # are allowed in cookies, but not in URLs.  See the cookie
          # input parameter examples for an example of encoding only
          # what is needed for the cookie syntax.
          dataValue: |
            lang=en-US; Expires=Wed, 09 Jun 2021 10:18:14 GMT
            foo=bar; Expires=Wed, 09 Jun 2021 10:18:14 GMT
            urlSafeData: Hello%2C%20world%21
          serializedValue: |
            lang=en-US; Expires=Wed, 09 Jun 2021 10:18:14 GMT
            foo=bar; Expires=Wed, 09 Jun 2021 10:18:14 GMT
            urlSafeData: Hello%2C%20world%21
    SetCookieWithSchemaAndStyle:
      schema:
        type: object
        required:
        - lang
        - foo
        - urlSafeData
        properties:
          urlSafeData:
            type: string
            pattern: ^[-_.%a-zA-Z0-9]+(;|$)
        additionalProperties:
          $comment: Require an Expires parameter
          pattern: "; *Expires="
      style: simple
      explode: true
      examples:
        SetCookies:
          dataValue: {
            "lang": "en-US; Expires=Wed, 09 Jun 2021 10:18:14 GMT"
            "foo": "bar; Expires=Wed, 09 Jun 2021 10:18:14 GMT"
            "urlSafeData": "Hello%2C%20world%21"
          }
          serializedValue: |
            lang=en-US; Expires=Wed, 09 Jun 2021 10:18:14 GMT
            foo=bar; Expires=Wed, 09 Jun 2021 10:18:14 GMT
            urlSafeData: Hello%2C%20world%21
```

In an HTTP message, the serialized example would look like:

```
Set-Cookie: lang=en-US; Expires=Wed, 09 Jun 2021 10:18:14 GM
Set-Cookie: foo=bar; Expires=Wed, 09 Jun 2021 10:18:14 GMT
Set-Cookie: urlSafeData=Hello%2C%20world%21
```

#### 4.21.4 Header Object Example

[](https://spec.openapis.org/oas/latest.html#header-object-example)

A simple header of type `integer`:

```
X-Rate-Limit-Limit:
  description: The number of allowed requests in the current period
  schema:
    type: integer
```

Requiring that a strong `ETag` header (with a value starting with `"` rather than `W/`) is present.

```
ETag:
  required: true
  schema:
    type: string
    # Note that quotation marks are part of the
    # ETag value, unlike many other headers that
    # use a quoted string purely for managing
    # reserved characters.
    pattern: ^"
  example: '"xyzzy"'
```

### 4.22 Tag Object

[](https://spec.openapis.org/oas/latest.html#tag-object)

Adds metadata to a single tag that is used by the [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object). It is not mandatory to have a Tag Object per tag defined in the Operation Object instances.

#### 4.22.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-18)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the tag. Use this value in the `tags` array of an Operation. |
| summary | `string` | A short summary of the tag, used for display purposes. |
| description | `string` | A description for the tag. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/latest.html#external-documentation-object) | Additional external documentation for this tag. |
| parent | `string` | The `name` of a tag that this tag is nested under. The named tag *MUST* exist in the API description, and circular references between parent and child tags *MUST NOT* be used. |
| kind | `string` | A machine-readable string to categorize what sort of tag it is. Any string value can be used; common uses are `nav` for Navigation, `badge` for visible badges, `audience` for APIs used by different groups. A [registry of the most commonly used values](https://spec.openapis.org/registry/tag-kind/) is available. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.22.2 Tag Object Example

[](https://spec.openapis.org/oas/latest.html#tag-object-example)

```
tags:
  - name: account-updates
    summary: Account Updates
    description: Account update operations
    kind: nav

  - name: partner
    summary: Partner
    description: Operations available to the partners network
    parent: external
    kind: audience

  - name: external
    summary: External
    description: Operations available to external consumers
    kind: audience
```

### 4.23 Reference Object

[](https://spec.openapis.org/oas/latest.html#reference-object)

A simple object to allow referencing other components in the OpenAPI Description, internally and externally.

The `$ref` string value contains a URI \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\], which identifies the value being referenced.

See the rules for resolving [Relative References](https://spec.openapis.org/oas/latest.html#relative-references-in-api-description-uris).

#### 4.23.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-19)

| Field Name | Type | Description |
| --- | --- | --- |
| $ref | `string` | ***REQUIRED***. The reference identifier. This *MUST* be in the form of a URI. |
| summary | `string` | A short summary which by default *SHOULD* override that of the referenced component. If the referenced object-type does not allow a `summary` field, then this field has no effect. |
| description | `string` | A description which by default *SHOULD* override that of the referenced component. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. If the referenced object-type does not allow a `description` field, then this field has no effect. |

This object cannot be extended with additional properties, and any properties added *SHALL* be ignored.

Note that this restriction on additional properties is a difference between Reference Objects and [Schema Objects](https://spec.openapis.org/oas/latest.html#schema-object) that contain a `$ref` keyword.

#### 4.23.2 Reference Object Example

[](https://spec.openapis.org/oas/latest.html#reference-object-example)

```
$ref: '#/components/schemas/Pet'
```

#### 4.23.3 Relative Schema Document Example

[](https://spec.openapis.org/oas/latest.html#relative-schema-document-example)

```
$ref: Pet.yaml
```

#### 4.23.4 Relative Documents with Embedded Schema Example

[](https://spec.openapis.org/oas/latest.html#relative-documents-with-embedded-schema-example)

```
$ref: definitions.yaml#/Pet
```

### 4.24 Schema Object

[](https://spec.openapis.org/oas/latest.html#schema-object)

The Schema Object allows the definition of input and output data types. These types can be objects, but also primitives and arrays. This object is a superset of the [JSON Schema Specification Draft 2020-12](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html). The empty schema (which allows any instance to validate) *MAY* be represented by the boolean value `true` and a schema which allows no instance to validate *MAY* be represented by the boolean value `false`.

For more information about the keywords, see [JSON Schema Core](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html) and [JSON Schema Validation](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html).

Unless stated otherwise, the keyword definitions follow those of JSON Schema and do not add any additional semantics; this includes keywords such as `$schema`, `$id`, `$ref`, and `$dynamicRef` being URIs rather than URLs. Where JSON Schema indicates that behavior is defined by the application (e.g. for annotations), OAS also defers the definition of semantics to the application consuming the OpenAPI document.

#### 4.24.1 JSON Schema Keywords

[](https://spec.openapis.org/oas/latest.html#json-schema-keywords)

The OpenAPI Schema Object [dialect](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.3.3) is defined as requiring the [OAS base vocabulary](https://spec.openapis.org/oas/latest.html#base-vocabulary), in addition to the vocabularies as specified in the JSON Schema Specification Draft 2020-12 [general purpose meta-schema](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-8).

The OpenAPI Schema Object dialect for this version of the specification is identified by the URI `https://spec.openapis.org/oas/3.1/dialect/base` (the “OAS dialect schema id”).

The following keywords are taken from the JSON Schema specification but their definitions have been extended by the OAS:

-   description - \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation.
-   format - See [Data Type Formats](https://spec.openapis.org/oas/latest.html#data-type-format) for further details. While relying on JSON Schema’s defined formats, the OAS offers a few additional predefined formats.

In addition to the JSON Schema keywords comprising the OAS dialect, the Schema Object supports keywords from any other vocabularies, or entirely arbitrary properties.

JSON Schema implementations *MAY* choose to treat keywords defined by the OpenAPI Specification’s base vocabulary as [unknown keywords](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.3.1), due to its inclusion in the OAS dialect with a [`$vocabulary`](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-8.1.2) value of `false`. The OAS base vocabulary is comprised of the following keywords:

#### 4.24.2 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-20)

| Field Name | Type | Description |
| --- | --- | --- |
| discriminator | [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) | The discriminator provides a “hint” for which of a set of schemas a payload is expected to satisfy. See [Composition and Inheritance](https://spec.openapis.org/oas/latest.html#composition-and-inheritance-polymorphism) for more details. |
| xml | [XML Object](https://spec.openapis.org/oas/latest.html#xml-object) | Adds additional metadata to describe the XML representation of this schema. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/latest.html#external-documentation-object) | Additional external documentation for this schema. |
| example | Any | A free-form field to include an example of an instance for this schema. To represent examples that cannot be naturally represented in JSON or YAML, a string value can be used to contain the example with escaping where necessary.

**Deprecated:** The `example` field has been deprecated in favor of the JSON Schema `examples` keyword. Use of `example` is discouraged, and later versions of this specification may remove it. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions), though as noted, additional properties *MAY* omit the `x-` prefix within this object.

#### 4.24.3 Data Types

[](https://spec.openapis.org/oas/latest.html#data-types)

Data types in the OAS are based on the types defined by the [JSON Schema Validation Specification Draft 2020-12](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-6.1.1): “null”, “boolean”, “object”, “array”, “number”, “string”, or “integer”. Models are defined using the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object), which is a superset of the JSON Schema Specification Draft 2020-12.

JSON Schema keywords and `format` values operate on JSON “instances” which may be one of the six JSON data types, “null”, “boolean”, “object”, “array”, “number”, or “string”, with certain keywords and formats only applying to a specific type. For example, the `pattern` keyword and the `date-time` format only apply to strings, and treat any instance of the other five types as *automatically valid.* This means JSON Schema keywords and formats do **NOT** implicitly require the expected type. Use the `type` keyword to explicitly constrain the type.

Note that the `type` keyword allows `"integer"` as a value for convenience, but keyword and format applicability does not recognize integers as being of a distinct JSON type from other numbers because [JSON](https://spec.openapis.org/oas/latest.html#bib-rfc8259 "The JavaScript Object Notation (JSON) Data Interchange Format") itself does not make that distinction. Since there is no distinct JSON integer type, JSON Schema defines integers mathematically. This means that both `1` and `1.0` are [equivalent](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.2.2), and are both considered to be integers.

##### 4.24.3.1 Data Type Format

[](https://spec.openapis.org/oas/latest.html#data-type-format)

As defined by the [JSON Schema Validation specification](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-7.3), data types can have an optional modifier keyword: `format`. As described in that specification, `format` is treated as a non-validating annotation by default; the ability to validate `format` varies across implementations.

The OpenAPI Initiative also hosts a [Format Registry](https://spec.openapis.org/registry/format/) for formats defined by OAS users and other specifications. Support for any registered format is strictly *OPTIONAL*, and support for one registered format does not imply support for any others.

Types that are not accompanied by a `format` keyword follow the type definition in the JSON Schema. Tools that do not recognize a specific `format` *MAY* default back to the `type` alone, as if the `format` is not specified. For the purpose of [JSON Schema validation](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-7.1), each format should specify the set of JSON data types for which it applies. In this registry, these types are shown in the “JSON Data Type” column.

The formats defined by the OAS are:

| `format` | JSON Data Type | Comments |
| --- | --- | --- |
| `int32` | number | signed 32 bits |
| `int64` | number | signed 64 bits (a.k.a long) |
| `float` | number |  |
| `double` | number |  |
| `password` | string | A hint to obscure the value. |

As noted under [Data Type](https://spec.openapis.org/oas/latest.html#data-types), both `type: number` and `type: integer` are considered to be numbers in the data model.

#### 4.24.4 Parsing and Serializing

[](https://spec.openapis.org/oas/latest.html#parsing-and-serializing)

API data has several forms:

1.  The serialized form, which is either a document of a particular media type, an HTTP header value, or part of a URI.
2.  The data form, intended for use with a [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object).
3.  The application form, which incorporates any additional information conveyed by JSON Schema keywords such as `format` and `contentType`, and possibly additional information such as class hierarchies that are beyond the scope of this specification, although they *MAY* be based on specification elements such as the [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) or guidance regarding [Data Modeling Techniques](https://spec.openapis.org/oas/latest.html#data-modeling-techniques).

##### 4.24.4.1 JSON Data

[](https://spec.openapis.org/oas/latest.html#json-data)

JSON-serialized data is nearly equivalent to the data form because the [JSON Schema data model](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.2.1) is nearly equivalent to the JSON representation. The serialized UTF-8 JSON string `{"when": "1985-04-12T23:20:50.52"}` represents an object with one data field, named `when`, with a string value, `1985-04-12T23:20:50.52`.

The exact application form is beyond the scope of this specification, as can be shown with the following schema for our JSON instance:

```
type: object
properties:
  when:
    type: string
    format: date-time
```

Some applications might leave the string as a string regardless of programming language, while others might notice the `format` and use it as a `datetime.datetime` instance in Python, or a `java.time.ZonedDateTime` in Java. This specification only requires that the data is valid according to the schema, and that [annotations](https://spec.openapis.org/oas/latest.html#extended-validation-with-annotations) such as `format` are available in accordance with the JSON Schema specification.

##### 4.24.4.2 Non-JSON Data

[](https://spec.openapis.org/oas/latest.html#non-json-data)

Non-JSON serializations can be substantially different from their corresponding data form, and might require several steps to parse.

To continue our “when” example, if we serialized the object as `application/x-www-form-urlencoded`, it would appear as the ASCII string `when=1985-04-12T23%3A20%3A50.52`. This example is still straightforward to use as it is all string data, and the only differences from JSON are the URI percent-encoding and the delimiter syntax (`=` instead of JSON punctuation and quoting).

However, many non-JSON text-based formats can be complex, requiring examination of the appropriate schema(s) in order to correctly parse the text into a schema-ready data structure. Serializing data into such formats requires either examining the schema-validated data or performing the same schema inspections.

When inspecting schemas, given a starting point schema, implementations *MUST* examine that schema and all schemas that can be reached from it by following only `$ref` and `allOf` keywords. These schemas are guaranteed to apply to any instance. When searching schemas for `type`, if the `type` keyword’s value is a list of types and the serialized value can be successfully parsed as more than one of the types in the list, and no other findable `type` keyword disambiguates the actual required type, the behavior is implementation-defined. Schema Objects that do not contain `type` *MUST* be considered to allow all types, regardless of which other keywords are present (e.g. `maximum` applies to numbers, but *does not* require the instance to be a number).

Implementations *MAY* inspect subschemas or possible reference targets of other keywords such as `oneOf` or `$dynamicRef`, but *MUST NOT* attempt to resolve ambiguities. For example, if an implementation opts to inspect `anyOf`, the schema:

```
anyOf:
- type: number
  minimum: 0
- type: number
  maximum: 100
```

unambiguously indicates a numeric type, but the schema:

```
anyOf:
- type: number
- maximum: 100
```

does not, because the second subschema allows all types.

Due to these limited requirements for searching schemas, serializers that have access to validated data *MUST* inspect the data if possible; implementations that either do not work with runtime data (such as code generators) or cannot access validated data for some reason *MUST* fall back to schema inspection.

Recall also that in JSON Schema, keywords that apply to a specific type (e.g. `pattern` applies to strings, `minimum` applies to numbers) *do not* require or imply that the data will actually be of that type.

As an example of these processes, given these OpenAPI components:

```
components:
  requestBodies:
    Form:
      content:
        application/x-www-form-urlencoded:
          schema:
            $ref: "#/components/schemas/FormData"
          encoding:
            extra:
              contentType: application/xml
  schemas:
    FormData:
      type: object
      properties:
        code:
          allOf:
          - type: [string, number]
            pattern: "1"
            minimum: 0
          - type: string
            pattern: "2"
        count:
          type: integer
        extra:
          type: object
```

And this request body to parse into its data form:

```
code=1234&count=42&extra=%3Cinfo%3Eabc%3C/info%3E
```

We must first search the schema for `properties` or other property-defining keywords, and then use each property schema as a starting point for a search for that property’s `type` keyword, as follows (the exact order is implementation-defined):

-   `#/components/requestBodies/Form/content/application~1x-www-form-urlencoded/schema` (initial starting point schema, only `$ref`)
-   `#/components/schemas/FormData` (follow `$ref`, found `properties`)
-   `#/components/schemas/FormData/properties/code` (starting point schema for `code` property)
-   `#/components/schemas/FormData/properties/code/allOf/0` (follow `allOf`, found `type: [string, number]`)
-   `#/components/schemas/FormData/properties/code/allOf/1` (follow `allOf`, found `type: string`)
-   `#/components/schemas/FormData/properties/count` (starting point schema for `count` property, found `type: integer`)
-   `#/components/schemas/FormData/properties/extra` (starting point schema for `extra` property, found `type: object`)

Note that for `code` we first found an ambiguous `type`, but then found another `type` keyword that ensures only one of the two possibilities is valid.

From this inspection, we determine that `code` is a string that happens to look like a number, while `count` needs to be parsed into a number *prior* to schema validation. Furthermore, the `extra` string is in fact an XML serialization of an object containing an `info` property. This means that the data form of this serialization is equivalent to the following JSON object:

```
{
  "code": "1234",
  "count": 42
  "extra": {
    "info": "abc"
  }
}
```

Serializing this object also requires correlating properties with [Encoding Objects](https://spec.openapis.org/oas/latest.html#encoding-object), and may require inspection to determine a default value of the `contentType` field. If validated data is not available, the schema inspection process is identical to that shown for parsing.

In this example, both `code` and `count` are of primitive type and do not appear in the `encoding` field, and are therefore serialized as plain text. However, the `extra` field is an object, which would by default be serialized as JSON, but the `extra` entry in the `encoding` field tells use to serialize it as XML instead.

##### 4.24.4.3 Working with Binary Data

[](https://spec.openapis.org/oas/latest.html#working-with-binary-data)

The OAS can describe either *raw* or *encoded* binary data.

-   **raw binary** is used where unencoded binary data is allowed, such as when sending a binary payload as the entire HTTP message body, or as part of a `multipart/*` payload that allows binary parts
-   **encoded binary** is used where binary data is embedded in a text-only format such as `application/json` or `application/x-www-form-urlencoded` (either as a message body or in the URL query string).

In the following table showing how to use Schema Object keywords for binary data, we use `image/png` as an example binary media type. Any binary media type, including `application/octet-stream`, is sufficient to indicate binary content.

| Keyword | Raw | Encoded | Comments |
| --- | --- | --- | --- |
| `type` | *omit* | `string` | raw binary is [outside of `type`](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.2.3) |
| `contentMediaType` | `image/png` | `image/png` | can sometimes be omitted if redundant (see below) |
| `contentEncoding` | *omit* | `base64` or `base64url` | other encodings are [allowed](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-8.3) |

Note that the encoding indicated by `contentEncoding`, which inflates the size of data in order to represent it as 7-bit ASCII text, is unrelated to HTTP’s `Content-Encoding` header, which indicates whether and how a message body has been compressed and is applied after all content serialization described in this section has occurred. Since HTTP allows unencoded binary message bodies, there is no standardized HTTP header for indicating base64 or similar encoding of an entire message body.

Using a `contentEncoding` of `base64url` ensures that URL encoding (as required in the query string and in message bodies of type `application/x-www-form-urlencoded`) does not need to further encode any part of the already-encoded binary data.

The `contentMediaType` keyword is redundant if the media type is already set:

-   as the key for a [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object)
-   in the `contentType` field of an [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object)

If the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) will be processed by a non-OAS-aware JSON Schema implementation, it may be useful to include `contentMediaType` even if it is redundant. However, if `contentMediaType` contradicts a relevant Media Type Object or Encoding Object, then `contentMediaType` *SHALL* be ignored.

See [Complete vs Streaming Content](https://spec.openapis.org/oas/latest.html#complete-vs-streaming-content) for guidance on streaming binary payloads.

###### 4.24.4.3.1 Schema Evaluation and Binary Data

[](https://spec.openapis.org/oas/latest.html#schema-evaluation-and-binary-data)

Few JSON Schema implementations directly support working with binary data, as doing so is not a mandatory part of that specification.

OAS Implementations that do not have access to a binary-instance-supporting JSON Schema implementation *MUST* examine schemas and apply them in accordance with [Working with Binary Data](https://spec.openapis.org/oas/latest.html#working-with-binary-data). When the entire instance is binary, this is straightforward as few keywords are relevant.

However, `multipart` media types can mix binary and text-based data, leaving implementations with two options for schema evaluations:

1.  Use a placeholder value, on the assumption that no assertions will apply to the binary data and no conditional schema keywords will cause the schema to treat the placeholder value differently (e.g. a part that could be either plain text or binary might behave unexpectedly if a string is used as a binary placeholder, as it would likely be treated as plain text and subject to different subschemas and keywords).
2.  Inspect the schema(s) to find the appropriate keywords (`properties`, `prefixItems`, etc.) in order to break up the subschemas and apply them separately to binary and JSON-compatible data.

###### 4.24.4.3.2 Migrating Binary Descriptions from OAS 3.0

[](https://spec.openapis.org/oas/latest.html#migrating-binary-descriptions-from-oas-3-0)

The following table shows how to migrate from OAS 3.0 binary data descriptions, continuing to use `image/png` as the example binary media type:

| OAS < 3.1 | OAS >= 3.1 | Comments |
| --- | --- | --- |
| `type: string`
`format: binary` | `contentMediaType: image/png` | if redundant, can be omitted, often resulting in an empty [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) |
| `type: string`
`format: byte` | `type: string`
`contentMediaType: image/png`
`contentEncoding: base64` | note that `base64url` can be used to avoid re-encoding the base64 string to be URL-safe |

#### 4.24.5 Extended Validation with Annotations

[](https://spec.openapis.org/oas/latest.html#extended-validation-with-annotations)

JSON Schema Draft 2020-12 supports [collecting annotations](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-7.7.1), including [treating unrecognized keywords as annotations](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-6.5). OAS implementations *MAY* use such annotations, including [extensions](https://spec.openapis.org/registry/extension/) not recognized as part of a declared JSON Schema vocabulary, as the basis for further validation. Note that JSON Schema Draft 2020-12 does not require an `x-` prefix for extensions.

##### 4.24.5.1 Non-Validating Constraint Keywords

[](https://spec.openapis.org/oas/latest.html#non-validating-constraint-keywords)

The [`format` keyword (when using default format-annotation vocabulary)](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-7.2.1) and the [`contentMediaType`, `contentEncoding`, and `contentSchema` keywords](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-8.2) define constraints on the data, but are treated as annotations instead of being validated directly. Extended validation is one way that these constraints *MAY* be enforced.

##### 4.24.5.2 Validating `readOnly` and `writeOnly`

[](https://spec.openapis.org/oas/latest.html#validating-readonly-and-writeonly)

The `readOnly` and `writeOnly` keywords are annotations, as JSON Schema is not aware of how the data it is validating is being used. Validation of these keywords *MAY* be done by checking the annotation, the read or write direction, and (if relevant) the current value of the field. [JSON Schema Validation Draft 2020-12 Section 9.4](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-9.4) defines the expectations of these keywords, including that a resource (described as the “owning authority”) *MAY* either ignore a `readOnly` field or treat it as an error.

Fields that are both required and read-only are an example of when it is beneficial to ignore a `readOnly: true` constraint in a PUT, particularly if the value has not been changed. This allows correctly requiring the field on a GET and still using the same representation and schema with PUT. Even when read-only fields are not required, stripping them is burdensome for clients, particularly when the JSON data is complex or deeply nested.

Note that the behavior of `readOnly` in particular differs from that specified by version 3.0 of this specification.

#### 4.24.6 Data Modeling Techniques

[](https://spec.openapis.org/oas/latest.html#data-modeling-techniques)

##### 4.24.6.1 Composition and Inheritance (Polymorphism)

[](https://spec.openapis.org/oas/latest.html#composition-and-inheritance-polymorphism)

The OpenAPI Specification allows combining and extending model definitions using the `allOf` keyword of JSON Schema, in effect offering model composition. `allOf` takes an array of object definitions that are validated *independently* but together compose a single object.

While composition offers model extensibility, it does not imply a hierarchy between the models.

JSON Schema also provides the `anyOf` and `oneOf` keywords, which allow defining multiple schemas where at least one or exactly one of them must be valid, respectively. As is the case with `allOf`, the schemas are validated *independently*. These keywords can be used to describe polymorphism, where a single field can accept multiple types of values.

The OpenAPI specification extends the JSON Schema support for polymorphism by adding the [`discriminator`](https://spec.openapis.org/oas/latest.html#schema-discriminator) field whose value is a [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object). When used, the Discriminator Object indicates the name of the property that hints which schema of an `anyOf` or `oneOf` is expected to validate the structure of the model. The discriminating property *MAY* be defined as required or optional, but when defined as an optional property the Discriminator Object *MUST* include a `defaultMapping` field that specifies which schema of the `anyOf` or `oneOf`, or which schema that references the current schema in an `allOf`, is expected to validate the structure of the model when the discriminating property is not present.

There are two ways to define the value of a discriminating property for an inheriting instance.

-   Use the schema name.
-   [Override the schema name](https://spec.openapis.org/oas/latest.html#discriminator-mapping) by overriding the property with a new value. If a new value exists, this takes precedence over the schema name.

##### 4.24.6.2 Generic (Template) Data Structures

[](https://spec.openapis.org/oas/latest.html#generic-template-data-structures)

Implementations *SHOULD* support defining generic or template data structures using JSON Schema’s dynamic referencing feature:

-   `$dynamicAnchor` identifies a set of possible schemas (including a default placeholder schema) to which a `$dynamicRef` can resolve
-   `$dynamicRef` resolves to the first matching `$dynamicAnchor` encountered on its path from the schema entry point to the reference, as described in the JSON Schema specification

An example is included in the [Schema Object Examples](https://spec.openapis.org/oas/latest.html#schema-object-examples) section below, and further information can be found on the Learn OpenAPI site’s [“Dynamic References”](https://learn.openapis.org/referencing/dynamic.html) page.

##### 4.24.6.3 Annotated Enumerations

[](https://spec.openapis.org/oas/latest.html#annotated-enumerations)

The Schema Object’s `enum` keyword does not allow associating descriptions or other information with individual values.

Implementations *MAY* support recognizing a `oneOf` or `anyOf` where each subschema in the keyword’s array consists of a `const` keyword and annotations such as `title` or `description` as an enumerated type with additional information. The exact behavior of this pattern beyond what is required by JSON Schema is implementation-defined.

##### 4.24.6.4 XML Modeling

[](https://spec.openapis.org/oas/latest.html#xml-modeling)

The [xml](https://spec.openapis.org/oas/latest.html#schema-xml) field allows extra definitions when translating the JSON definition to XML. The [XML Object](https://spec.openapis.org/oas/latest.html#xml-object) contains additional information about the available options.

#### 4.24.7 Specifying Schema Dialects

[](https://spec.openapis.org/oas/latest.html#specifying-schema-dialects)

It is important for tooling to be able to determine which dialect or meta-schema any given resource wishes to be processed with: JSON Schema Core, JSON Schema Validation, OpenAPI Schema dialect, or some custom meta-schema.

The `$schema` keyword *MAY* be present in any Schema Object that is a [schema resource root](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.3.5), and if present *MUST* be used to determine which dialect should be used when processing the schema. This allows use of Schema Objects which comply with other drafts of JSON Schema than the default Draft 2020-12 support. Tooling *MUST* support the [OAS dialect schema id](https://spec.openapis.org/oas/latest.html#dialect-schema-id), and *MAY* support additional values of `$schema`.

To allow use of a different default `$schema` value for all Schema Objects contained within an OAS document, a `jsonSchemaDialect` value may be set within the [OpenAPI Object](https://spec.openapis.org/oas/latest.html#openapi-object). If this default is not set, then the OAS dialect schema id *MUST* be used for these Schema Objects. The value of `$schema` within a resource root Schema Object always overrides any default.

For standalone JSON Schema documents that do not set `$schema`, or for Schema Objects in OpenAPI description documents that are *not* [complete documents](https://spec.openapis.org/oas/latest.html#openapi-description-structure), the dialect *SHOULD* be assumed to be the OAS dialect. However, for maximum interoperability, it is *RECOMMENDED* that OpenAPI description authors explicitly set the dialect through `$schema` in such documents.

#### 4.24.8 Schema Object Examples

[](https://spec.openapis.org/oas/latest.html#schema-object-examples)

##### 4.24.8.1 Primitive Example

[](https://spec.openapis.org/oas/latest.html#primitive-example)

```
type: string
format: email
```

##### 4.24.8.2 Simple Model

[](https://spec.openapis.org/oas/latest.html#simple-model)

```
type: object
required:
  - name
properties:
  name:
    type: string
  address:
    $ref: '#/components/schemas/Address'
  age:
    type: integer
    format: int32
    minimum: 0
```

##### 4.24.8.3 Model with Map/Dictionary Properties

[](https://spec.openapis.org/oas/latest.html#model-with-map-dictionary-properties)

For a simple string to string mapping:

```
type: object
additionalProperties:
  type: string
```

For a string to model mapping:

```
type: object
additionalProperties:
  $ref: '#/components/schemas/ComplexModel'
```

##### 4.24.8.4 Model with Annotated Enumeration

[](https://spec.openapis.org/oas/latest.html#model-with-annotated-enumeration)

```
oneOf:
  - const: RGB
    title: Red, Green, Blue
    description: Specify colors with the red, green, and blue additive color model
  - const: CMYK
    title: Cyan, Magenta, Yellow, Black
    description: Specify colors with the cyan, magenta, yellow, and black subtractive color model
```

##### 4.24.8.5 Model with Example

[](https://spec.openapis.org/oas/latest.html#model-with-example)

```
type: object
properties:
  id:
    type: integer
    format: int64
  name:
    type: string
required:
  - name
examples:
  - name: Puma
    id: 1
```

##### 4.24.8.6 Models with Composition

[](https://spec.openapis.org/oas/latest.html#models-with-composition)

```
components:
  schemas:
    ErrorModel:
      type: object
      required:
        - message
        - code
      properties:
        message:
          type: string
        code:
          type: integer
          minimum: 100
          maximum: 600
    ExtendedErrorModel:
      allOf:
        - $ref: '#/components/schemas/ErrorModel'
        - type: object
          required:
            - rootCause
          properties:
            rootCause:
              type: string
```

##### 4.24.8.7 Models with Polymorphism Support

[](https://spec.openapis.org/oas/latest.html#models-with-polymorphism-support)

The following example describes a `Pet` model that can represent either a cat or a dog, as distinguished by the `petType` property. Each type of pet has other properties beyond those of the base `Pet` model. An instance without a `petType` property, or with a `petType` property that does not match either `cat` or `dog`, is invalid.

```
components:
  schemas:
    Pet:
      type: object
      properties:
        name:
          type: string
      required:
        - name
        - petType
      oneOf:
        - $ref: '#/components/schemas/Cat'
        - $ref: '#/components/schemas/Dog'
    Cat:
      description: A pet cat
      type: object
      properties:
        petType:
          const: 'cat'
        huntingSkill:
          type: string
          description: The measured skill for hunting
          enum:
            - clueless
            - lazy
            - adventurous
            - aggressive
      required:
        - huntingSkill
    Dog:
      description: A pet dog
      type: object
      properties:
        petType:
          const: 'dog'
        packSize:
          type: integer
          format: int32
          description: the size of the pack the dog is from
          default: 0
          minimum: 0
      required:
        - packSize
```

##### 4.24.8.8 Models with Polymorphism Support and a Discriminator Object

[](https://spec.openapis.org/oas/latest.html#models-with-polymorphism-support-and-a-discriminator-object)

The following example extends the example of the previous section by adding a [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) to the `Pet` schema. Note that the Discriminator Object is only a hint to the consumer of the API and does not change the validation outcome of the schema.

```
components:
  schemas:
    Pet:
      type: object
      discriminator:
        propertyName: petType
        mapping:
          cat: '#/components/schemas/Cat'
          dog: '#/components/schemas/Dog'
      properties:
        name:
          type: string
      required:
        - name
        - petType
      oneOf:
        - $ref: '#/components/schemas/Cat'
        - $ref: '#/components/schemas/Dog'
    Cat:
      description: A pet cat
      type: object
      properties:
        petType:
          const: 'cat'
        huntingSkill:
          type: string
          description: The measured skill for hunting
          enum:
            - clueless
            - lazy
            - adventurous
            - aggressive
      required:
        - huntingSkill
    Dog:
      description: A pet dog
      type: object
      properties:
        petType:
          const: 'dog'
        packSize:
          type: integer
          format: int32
          description: the size of the pack the dog is from
          default: 0
          minimum: 0
      required:
        - petType
        - packSize
```

##### 4.24.8.9 Models with Polymorphism Support using `allOf` and a Discriminator Object

[](https://spec.openapis.org/oas/latest.html#models-with-polymorphism-support-using-allof-and-a-discriminator-object)

It is also possible to describe polymorphic models using `allOf`. The following example uses `allOf` with a [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) to describe a polymorphic `Pet` model.

```
components:
  schemas:
    Pet:
      type: object
      discriminator:
        propertyName: petType
      properties:
        name:
          type: string
        petType:
          type: string
      required:
        - name
        - petType
    Cat: # "Cat" will be used as the discriminating value
      description: A representation of a cat
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          properties:
            huntingSkill:
              type: string
              description: The measured skill for hunting
              enum:
                - clueless
                - lazy
                - adventurous
                - aggressive
          required:
            - huntingSkill
    Dog: # "Dog" will be used as the discriminating value
      description: A representation of a dog
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          properties:
            packSize:
              type: integer
              format: int32
              description: the size of the pack the dog is from
              default: 0
              minimum: 0
          required:
            - packSize
```

##### 4.24.8.10 Generic Data Structure Model

[](https://spec.openapis.org/oas/latest.html#generic-data-structure-model)

```
components:
  schemas:
    genericArrayComponent:
      $id: fully_generic_array
      type: array
      items:
        $dynamicRef: '#generic-array'
      $defs:
        allowAll:
          $dynamicAnchor: generic-array
    numberArray:
      $id: array_of_numbers
      $ref: fully_generic_array
      $defs:
        numbersOnly:
          $dynamicAnchor: generic-array
          type: number
    stringArray:
      $id: array_of_strings
      $ref: fully_generic_array
      $defs:
        stringsOnly:
          $dynamicAnchor: generic-array
          type: string
    objWithTypedArray:
      $id: obj_with_typed_array
      type: object
      required:
      - dataType
      - data
      properties:
        dataType:
          enum:
          - string
          - number
      oneOf:
      - properties:
          dataType:
            const: string
          data:
            $ref: array_of_strings
      - properties:
          dataType:
            const: number
          data:
            $ref: array_of_numbers
```

### 4.25 Discriminator Object

[](https://spec.openapis.org/oas/latest.html#discriminator-object)

When request bodies or response payloads may be one of a number of different schemas, these should use the JSON Schema `anyOf` or `oneOf` keywords to describe the possible schemas (see [Composition and Inheritance](https://spec.openapis.org/oas/latest.html#composition-and-inheritance-polymorphism)).

A polymorphic schema *MAY* include a Discriminator Object, which defines the name of the property that may be used as a hint for which schema of the `anyOf` or `oneOf`, or which schema that references the current schema in an `allOf`, is expected to validate the structure of the model. This hint can be used to aid in serialization, deserialization, and validation. The Discriminator Object does this by implicitly or explicitly associating the possible values of a named property with alternative schemas.

Note that `discriminator` *MUST NOT* change the validation outcome of the schema.

#### 4.25.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-21)

| Field Name | Type | Description |
| --- | --- | --- |
| propertyName | `string` | ***REQUIRED***. The name of the discriminating property in the payload that will hold the discriminating value. The discriminating property *MAY* be defined as required or optional, but when defined as optional the Discriminator Object *MUST* include a `defaultMapping` field that specifies which schema is expected to validate the structure of the model when the discriminating property is not present. |
| mapping | Map\[`string`, `string`\] | An object to hold mappings between payload values and schema names or URI references. |
| defaultMapping | `string` | The schema name or URI reference to a schema that is expected to validate the structure of the model when the discriminating property is not present in the payload or contains a value for which there is no explicit or implicit mapping. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.25.2 Conditions for Using the Discriminator Object

[](https://spec.openapis.org/oas/latest.html#conditions-for-using-the-discriminator-object)

The Discriminator Object is legal only when using one of the composite keywords `oneOf`, `anyOf`, `allOf`.

In both the `oneOf` and `anyOf` use cases, where those keywords are adjacent to `discriminator`, all possible schemas *MUST* be listed explicitly.

To avoid redundancy, the discriminator *MAY* be added to a parent schema definition, and all schemas building on the parent schema via an `allOf` construct may be used as an alternate schema.

The `allOf` form of `discriminator` is *only* useful for non-validation use cases; validation with the parent schema with this form of `discriminator` *does not* perform a search for child schemas or use them in validation in any way. This is because `discriminator` cannot change the validation outcome, and no standard JSON Schema keyword connects the parent schema to the child schemas.

The behavior of any configuration of `oneOf`, `anyOf`, `allOf` and `discriminator` that is not described above is undefined.

#### 4.25.3 Options for Mapping Values to Schemas

[](https://spec.openapis.org/oas/latest.html#options-for-mapping-values-to-schemas)

The value of the property named in `propertyName` is used as the name of the associated schema under the [Components Object](https://spec.openapis.org/oas/latest.html#components-object), *unless* a `mapping` is present for that value. The `mapping` entry maps a specific property value to either a different schema component name, or to a schema identified by a URI. When using implicit or explicit schema component names, inline `oneOf` or `anyOf` subschemas are not considered. The behavior of a `mapping` value or `defaultMapping` value that is both a valid schema name and a valid relative URI reference is implementation-defined, but it is *RECOMMENDED* that it be treated as a schema name. To ensure that an ambiguous value (e.g. `"foo"`) is treated as a relative URI reference by all implementations, authors *MUST* prefix it with the `"."` path segment (e.g. `"./foo"`).

Mapping keys *MUST* be string values, but tooling *MAY* convert response values to strings for comparison. However, the exact nature of such conversions are implementation-defined.

#### 4.25.4 Optional Discriminating Property

[](https://spec.openapis.org/oas/latest.html#optional-discriminating-property)

When the discriminating property is defined as optional, the [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) *MUST* include a `defaultMapping` field that specifies a schema that is expected to validate the structure of the model when the discriminating property is not present in the payload or contains a value for which there is no explicit or implicit mapping. This allows the schema to still be validated correctly even if the discriminating property is missing.

The primary use case for an optional discriminating property is to allow a schema to be extended with a discriminator without breaking existing clients that do not provide the discriminating property.

When the discriminating property is defined as optional, it is important that each subschema that defines a value for the discriminating property also define the property as required, since this is no longer enforced by the parent schema.

The `defaultMapping` schema is also expected to validate the structure of the model when the discriminating property is present but contains a value for which there is no explicit or implicit mapping. This is typically expressed in the `defaultMapping` schema by excluding any instances with mapped values of the discriminating property, e.g.

```
OtherPet:
  type: object
  properties:
    petType:
      not:
        enum: ['cat', 'dog']
```

This prevents the `defaultMapping` schema from validating a payload that includes the discriminating property with a mapped discriminating value, which would cause a validation to fail when polymorphism is described using the `oneOf` JSON schema keyword.

#### 4.25.5 Examples

[](https://spec.openapis.org/oas/latest.html#examples-0)

For these examples, assume all schemas are in the [entry document](https://spec.openapis.org/oas/latest.html#openapi-description-structure) of the OAD; for handling of `discriminator` in referenced documents see [Resolving Implicit Connections](https://spec.openapis.org/oas/latest.html#resolving-implicit-connections).

In OAS 3.x, a response payload *MAY* be described to be exactly one of any number of types:

```
MyResponseType:
  oneOf:
    - $ref: '#/components/schemas/Cat'
    - $ref: '#/components/schemas/Dog'
    - $ref: '#/components/schemas/Lizard'
```

which means a valid payload has to match exactly one of the schemas described by `Cat`, `Dog`, or `Lizard`. Deserialization of a `oneOf` can be a costly operation, as it requires determining which schema matches the payload and thus should be used in deserialization. This problem also exists for `anyOf` schemas. A `discriminator` can be used as a “hint” to improve the efficiency of selection of the matching schema. The [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) cannot change the validation result of the `oneOf`, it can only help make the deserialization more efficient and provide better error messaging. We can specify the exact field that tells us which schema is expected to match the instance:

```
MyResponseType:
  oneOf:
    - $ref: '#/components/schemas/Cat'
    - $ref: '#/components/schemas/Dog'
    - $ref: '#/components/schemas/Lizard'
  discriminator:
    propertyName: petType
```

The expectation now is that a property with name `petType` **MUST** be present in the response payload, and the value will correspond to the name of a schema defined in the OpenAPI Description. Thus the response payload:

```
{
  "id": 12345,
  "petType": "Cat"
}
```

will indicate that the `Cat` schema is expected to match this payload.

In scenarios where the value of the discriminating property does not match the schema name or implicit mapping is not possible, an optional `mapping` definition can be used:

```
MyResponseType:
  oneOf:
    - $ref: '#/components/schemas/Cat'
    - $ref: '#/components/schemas/Dog'
    - $ref: '#/components/schemas/Lizard'
    - $ref: https://gigantic-server.com/schemas/Monster/schema.json
  discriminator:
    propertyName: petType
    mapping:
      dog: '#/components/schemas/Dog'
      monster: https://gigantic-server.com/schemas/Monster/schema.json
```

Here the discriminating value of `dog` will map to the schema `#/components/schemas/Dog`, rather than the default (implicit) value of `#/components/schemas/dog`. If the discriminating value does not match an implicit or explicit mapping, no schema can be determined and validation *SHOULD* fail.

When used in conjunction with the `anyOf` construct, the use of the discriminator can avoid ambiguity for serializers/deserializers where multiple schemas may satisfy a single payload.

When the discriminating property is defined as optional, the Discriminator Object has to include a `defaultMapping` field that specifies a schema of the `anyOf` or `oneOf` is expected to validate the structure of the model when the discriminating property is not present in the payload. This allows the schema to still be validated correctly even if the discriminator property is missing.

For example:

```
MyResponseType:
  oneOf:
    - $ref: '#/components/schemas/Cat'
    - $ref: '#/components/schemas/Dog'
    - $ref: '#/components/schemas/Lizard'
    - $ref: '#/components/schemas/OtherPet'
  discriminator:
    propertyName: petType
    defaultMapping: OtherPet
OtherPet:
  type: object
  properties:
    petType:
      not:
        enum: ['Cat', 'Dog', 'Lizard']
```

In this example, if the `petType` property is not present in the payload, or if the value of `petType` is not “Cat”, “Dog”, or “Lizard”, then the payload should validate against the `OtherPet` schema.

This example shows the `allOf` usage, which avoids needing to reference all child schemas in the parent:

```
components:
  schemas:
    Pet:
      type: object
      required:
        - petType
      properties:
        petType:
          type: string
      discriminator:
        propertyName: petType
        mapping:
          dog: Dog
    Cat:
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          # all other properties specific to a `Cat`
          properties:
            name:
              type: string
    Dog:
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          # all other properties specific to a `Dog`
          properties:
            bark:
              type: string
    Lizard:
      allOf:
        - $ref: '#/components/schemas/Pet'
        - type: object
          # all other properties specific to a `Lizard`
          properties:
            lovesRocks:
              type: boolean
```

Validated against the `Pet` schema, a payload like this:

```
{
  "petType": "Cat",
  "name": "Misty"
}
```

will indicate that the `#/components/schemas/Cat` schema is expected to match. Likewise this payload:

```
{
  "petType": "dog",
  "bark": "soft"
}
```

will map to `#/components/schemas/Dog` because the `dog` entry in the `mapping` element maps to `Dog` which is the schema name for `#/components/schemas/Dog`.

### 4.26 XML Object

[](https://spec.openapis.org/oas/latest.html#xml-object)

A metadata object that allows for more fine-tuned XML model definitions. When using a Schema Object with XML, if no XML Object is present, the behavior is determined by the XML Object’s default field values.

#### 4.26.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-22)

| Field Name | Type | Description |
| --- | --- | --- |
| nodeType | `string` | One of `element`, `attribute`, `text`, `cdata`, or `none`, as explained under [XML Node Types](https://spec.openapis.org/oas/latest.html#xml-node-types). The default value is `none` if `$ref`, `$dynamicRef`, or `type: "array"` is present in the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) containing the XML Object, and `element` otherwise. |
| name | `string` | Sets the name of the element/attribute corresponding to the schema, replacing the name that was inferred as described under [XML Node Names](https://spec.openapis.org/oas/latest.html#xml-node-names). This field *SHALL* be ignored if the `nodeType` is `text`, `cdata`, or `none`. |
| namespace | `string` | The IRI (\[[RFC3987](https://spec.openapis.org/oas/latest.html#bib-rfc3987 "Internationalized Resource Identifiers (IRIs)")\]) of the namespace definition. Value *MUST* be in the form of a non-relative IRI. |
| prefix | `string` | The prefix to be used for the [name](https://spec.openapis.org/oas/latest.html#xml-name). |
| attribute | `boolean` | Declares whether the property definition translates to an attribute instead of an element. Default value is `false`. If `nodeType` is present, this field *MUST NOT* be present.

**Deprecated:** Use `nodeType: "attribute"` instead of `attribute: true` |
| wrapped | `boolean` | *MAY* be used only for an array definition. Signifies whether the array is wrapped (for example, `<books><book/><book/></books>`) or unwrapped (`<book/><book/>`). Default value is `false`. The definition takes effect only when defined alongside `type` being `"array"` (outside the `items`). If `nodeType` is present, this field *MUST NOT* be present.

**Deprecated:** Use `nodeType: "element"` instead of `wrapped: true` |

Note that when generating an XML document from object data, the order of the nodes is undefined. Use `prefixItems` to control node ordering as shown under [Ordered Elements and Text](https://spec.openapis.org/oas/latest.html#ordered-elements-and-text).

See [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion) for a discussion of converting values of various types to string representations.

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.26.2 XML Node Types

[](https://spec.openapis.org/oas/latest.html#xml-node-types)

Each Schema Object describes a particular type of XML \[[DOM](https://spec.openapis.org/oas/latest.html#bib-dom "DOM Standard")\] [node](https://dom.spec.whatwg.org/#interface-node) which is specified by the `nodeType` field, which has the following possible values. Except for the special value `none`, these values have numeric equivalents in the DOM specification which are given in parentheses after the name:

-   `element` (1): The schema represents an element and describes its contents
-   `attribute` (2): The schema represents an attribute and describes its value
-   `text` (3): The schema represents a text node (parsed character data)
-   `cdata` (4): The schema represents a CDATA section
-   `none`: The schema does not correspond to any node in the XML document, and the nodes corresponding to its subschema(s) are included directly under its parent schema’s node

The `none` type is useful for JSON Schema constructs that require more Schema Objects than XML nodes, such as a schema containing only `$ref` that exists to facilitate re-use rather than imply any structure.

##### 4.26.2.1 Modeling Element Lists

[](https://spec.openapis.org/oas/latest.html#modeling-element-lists)

For historical compatibility, schemas of `type: "array"` default to `nodeType: "none"`, placing the nodes for each array item directly under the parent node. This also aligns with the inferred naming behavior defined under [XML Node Names](https://spec.openapis.org/oas/latest.html#xml-node-names).

To produce an element wrapping the list, set an explicit `nodeType: "element"` on the `type: "array"` schema. When doing so, it is advisable to set an explicit name on either the wrapping element or the item elements to avoid them having the same inferred name. See examples for expected behavior.

##### 4.26.2.2 Implicit and Explicit `text` Nodes

[](https://spec.openapis.org/oas/latest.html#implicit-and-explicit-text-nodes)

If an `element` node has a primitive type, then the schema also produces an implicit `text` node described by the schema for the contents of the `element` node named by the property name (or `name` field).

Explicit `text` nodes are necessary if an element has both attributes and content.

Note that placing two `text` nodes adjacent to each other is ambiguous for parsing, and the resulting behavior is implementation-defined.

#### 4.26.3 XML Node Names

[](https://spec.openapis.org/oas/latest.html#xml-node-names)

The `element` and `attribute` node types require a name, which *MUST* be inferred from the schema as follows, unless overridden by the `name` field:

-   For schemas directly under the [Components Object’s](https://spec.openapis.org/oas/latest.html#components-object) `schemas` field, the component name is the inferred name.
-   For property schemas, and for array item schemas under a property schema, the property name is the inferred name.
-   In all other cases, such as an inline schema under a [Media Type Object’s](https://spec.openapis.org/oas/latest.html#media-type-object) `schema` field, no name can be inferred and an XML Object with a `name` field *MUST* be present.

Note that when using arrays, singular vs plural forms are *not* inferred, and must be set explicitly.

#### 4.26.4 Namespace Limitations

[](https://spec.openapis.org/oas/latest.html#namespace-limitations)

The `namespace` field is intended to match the syntax of [XML namespaces](https://spec.openapis.org/oas/latest.html#bib-xml-names11 "Namespaces in XML 1.1 (Second Edition)"), although there are a few caveats:

-   Versions 3.1.0, 3.0.3, and earlier of this specification erroneously used the term “absolute URI” instead of “non-relative URI” (“non-relative IRI” as of OAS v3.2.0), so authors using namespaces that include a fragment should check tooling support carefully.
-   XML allows but discourages relative IRI-references, while this specification outright forbids them.

#### 4.26.5 Handling `null` Values

[](https://spec.openapis.org/oas/latest.html#handling-null-values)

XML does not, by default, have a concept equivalent to `null`, and to preserve compatibility with version 3.1.1 and earlier of this specification, the behavior of serializing `null` values is implementation-defined.

However, implementations *SHOULD* handle `null` values as follows:

-   For elements, produce an empty element with an `xsi:nil="true"` attribute.
-   For attributes, omit the attribute.
-   For text and CDATA sections, see [Appendix B](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion) for a discussion of serializing non-text values to text.

Note that for attributes, this makes either a `null` value or a missing property serialize to an omitted attribute. As the Schema Object validates the in-memory representation, this allows handling the combination of `null` and a required property. However, because there is no distinct way to represent `null` as an attribute, it is *RECOMMENDED* to make attribute properties optional rather than use `null`.

To ensure correct round-trip behavior, when parsing an element that omits an attribute, implementations *SHOULD* set the corresponding property to `null` if the schema allows for that value (e.g. `type: ["number", "null"]`), and omit the property otherwise (e.g.`type: "number"`).

#### 4.26.6 XML Object Examples

[](https://spec.openapis.org/oas/latest.html#xml-object-examples)

The Schema Objects are followed by an example XML representation produced for the schema shown. For examples using `attribute` or `wrapped`, please see version 3.1 of the OpenAPI Specification.

##### 4.26.6.1 No XML Object

[](https://spec.openapis.org/oas/latest.html#no-xml-object)

Basic string property without an XML Object, using `serializedValue` (the remaining examples will use `externalValue` so that the XML form can be shown with syntax highlighting):

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: string
  examples:
    pets:
      dataValue:
        animals: dog, cat, hamster
      serializedValue: |
        <document>
          <animals>dog, cat, hamster</animals>
        </document>
```

Basic string array property (`nodeType` is `none` by default):

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        items:
          type: string
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <animals>dog</animals>
  <animals>cat</animals>
  <animals>hamster</animals>
</document>
```

##### 4.26.6.2 XML Name Replacement

[](https://spec.openapis.org/oas/latest.html#xml-name-replacement)

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: string
        xml:
          name: animal
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <animal>dog</animal>
  <animal>cat</animal>
  <animal>hamster</animal>
</document>
```

##### 4.26.6.3 XML Attribute, Prefix and Namespace

[](https://spec.openapis.org/oas/latest.html#xml-attribute-prefix-and-namespace)

Note that the name of the root XML element comes from the component name.

```
components:
  schemas:
    Person:
      type: object
      properties:
        id:
          type: integer
          format: int32
          xml:
            nodeType: attribute
        name:
          type: string
          xml:
            namespace: https://example.com/schema/sample
            prefix: sample
  requestBodies:
    Person:
      content:
        application/xml:
          schema:
            $ref: "#/components/schemas/Person"
          examples:
            Person:
              dataValue:
                id: 123
                name: example
              externalValue: ./examples/Person.xml
```

Where `./examples/Person.xml` would be:

```
<Person id="123">
  <sample:name xmlns:sample="https://example.com/schema/sample">example</sample:name>
</Person>
```

##### 4.26.6.4 XML Arrays

[](https://spec.openapis.org/oas/latest.html#xml-arrays)

Changing the element names:

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        items:
          type: string
          xml:
            name: animal
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <animal>dog</animal>
  <animal>cat</animal>
  <animal>hamster</animal>
</document>
```

The `name` field for the `type: "array"` schema has no effect because the default `nodeType` for that object is `none`:

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        xml:
          name: aliens
        items:
          type: string
          xml:
            name: animal
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <animal>dog</animal>
  <animal>cat</animal>
  <animal>hamster</animal>
</document>
```

Even when a wrapping element is explicitly created by setting `nodeType` to `element`, if a name is not explicitly defined, the same name will be used for both the wrapping element and the list item elements:

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        xml:
          nodeType: element
        items:
          type: string
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <animals>
    <animals>dog</animals>
    <animals>cat</animals>
    <animals>hamster</animals>
  </animals>
</document>
```

To overcome the naming problem in the example above, the following definition can be used:

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        xml:
          nodeType: element
        items:
          type: string
          xml:
            name: animal
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <animals>
    <animal>dog</animal>
    <animal>cat</animal>
    <animal>hamster</animal>
  </animals>
</document>
```

Affecting both wrapping element and item element names:

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        xml:
          name: aliens
          nodeType: element
        items:
          type: string
          xml:
            name: animal
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <aliens>
    <animal>dog</animal>
    <animal>cat</animal>
    <animal>hamster</animal>
  </aliens>
</document>
```

If we change the wrapping element name but not the item element names:

```
application/xml:
  schema:
    type: object
    xml:
      name: document
    properties:
      animals:
        type: array
        xml:
          name: aliens
          nodeType: element
        items:
          type: string
  examples:
    pets:
      dataValue:
        animals:
          - dog
          - cat
          - hamster
      externalValue: ./examples/pets.xml
```

Where `./examples/pets.xml` would be:

```
<document>
  <aliens>
    <aliens>dog</aliens>
    <aliens>cat</aliens>
    <aliens>hamster</aliens>
  </aliens>
</document>
```

##### 4.26.6.5 Elements With Attributes And Text

[](https://spec.openapis.org/oas/latest.html#elements-with-attributes-and-text)

```
application/xml:
  schema:
    type: array
    xml:
      nodeType: element
      name: animals
    items:
      xml:
        name: animal
      properties:
        kind:
          type: string
          xml:
            nodeType: attribute
        name:
          type: string
          xml:
            nodeType: text
  examples:
    pets:
      dataValue:
      - kind: Cat
        name: Fluffy
      - kind: Dog
        name: Fido
```

Where `./examples/pets.xml` would be:

```
<animals>
  <animal kind="Cat">Fluffy</animals>
  <animal kind="Dog">Fido</animals>
<animals>
```

##### 4.26.6.6 Referenced Element With CDATA

[](https://spec.openapis.org/oas/latest.html#referenced-element-with-cdata)

In this example, no element is created for the Schema Object that contains only the `$ref`, as its `nodeType` defaults to `none`. It is necessary to create a subschema for the CDATA section as otherwise the content would be treated as an implicit node of type `text`.

```
components:
  schemas:
    Documentation:
      type: object
      properties:
        content:
          type: string
          contentMediaType: text/html
          xml:
            nodeType: cdata
  responses:
    content:
      application/xml:
        schema:
          $ref: "#/components/schemas/Documentation"
        examples:
          docs:
            dataValue:
              content: <html><head><title>Awesome Docs</title></head><body></body><html>
            externalValue: ./examples/docs.xml
```

Where `./examples/docs.xml` would be:

```
<Documentation>
  <![CDATA[<html><head><title>Awesome Docs</title></head><body></body><html>]]>
</Documentation>
```

Alternatively, the named root element could be set at the point of use and the root element disabled on the component (note that in this example, the same `dataValue` is used in two places with different serializations shown with `externalValue`):

```
paths:
  /docs:
    get:
      responses:
        "200":
          content:
            application/xml:
              schema:
                xml:
                  nodeType: element
                  name: StoredDocument
                $ref: "#/components/schemas/Documentation"
              examples:
                stored:
                  dataValue:
                    content: <html><head><title>Awesome Docs</title></head><body></body><html>
                  externalValue: ./examples/stored.xml
    put:
      requestBody:
        required: true
        content:
          application/xml:
            schema:
              xml:
                nodeType: element
                name: UpdatedDocument
              $ref: "#/components/schemas/Documentation"
            examples:
              updated:
                dataValue:
                  content: <html><head><title>Awesome Docs</title></head><body></body><html>
                externalValue: ./examples/updated.xml
      responses:
        "201": {}
components:
  schemas:
    Documentation:
      xml:
        nodeType: none
      type: object
      properties:
        content:
          type: string
          contentMediaType: text/html
          xml:
            nodeType: cdata
```

where `./examples/stored.xml` would be:

```
<StoredDocument>
  <![CDATA[<html><head><title>Awesome Docs</title></head><body></body><html>]]>
</StoredDocument>
```

and `./examples/updated.xml` would be:

```
<UpdatedDocument>
  <![CDATA[<html><head><title>Awesome Docs</title></head><body></body><html>]]>
</UpdatedDocument>
```

##### 4.26.6.7 Ordered Elements and Text

[](https://spec.openapis.org/oas/latest.html#ordered-elements-and-text)

To control the exact order of elements, use the `prefixItems` keyword. With this approach, it is necessary to set the element names using the XML Object as they would otherwise all inherit the parent’s name despite being different elements in a specific order. It is also necessary to set `nodeType: "element"` explicitly on the array in order to get an element containing the sequence.

This first ordered example shows a sequence of elements, as well as the recommended serialization of `null` for elements:

```
application/xml:
  schema:
    xml:
      nodeType: element
      name: OneTwoThree
    type: array
    minLength: 3
    maxLength: 3
    prefixItems:
    - xml:
        name: One
      type: string
    - xml:
        name: Two
      type: object
      required:
      - unit
      - value
      properties:
        unit:
          type: string
          xml:
            nodeType: attribute
        value:
          type: number
          xml:
            nodeType: text
    - xml:
        name: Three
      type:
      - boolean
      - "null"
  examples:
    OneTwoThree:
      dataValue:
        - Some text
        - unit: cubits
          value: 42
        null
      ]
      externalValue: ./examples/OneTwoThree.xml
```

Where `./examples/OneTwoThree.xml` would be:

```
<OneTwoThree>
  <One>Some text</One>
  <Two unit="cubits">42</Two>
  <Three xsi:nil="true" />
</OneTwoThree>
```

In this next example, the `name` needs to be set for the element, while the `nodeType` needs to be set for the text nodes.

```
application/xml:
  schema:
    xml:
      nodeType: element
      name: Report
    type: array
    prefixItems:
    - xml:
        nodeType: text
      type: string
    - xml:
        name: data
      type: number
    - xml:
        nodeType: text
      type: string
  examples:
    Report:
      dataValue:
        - Some preamble text.
        - 42
        - Some postamble text.
      externalValue: ./examples/Report.xml
```

Where `./examples/Report.xml` would be:

```
<Report>Some preamble text.<data>42</data>Some postamble text.</Report>
```

##### 4.26.6.8 XML With `null` Values

[](https://spec.openapis.org/oas/latest.html#xml-with-null-values)

Recall that the schema validates the in-memory data, not the XML document itself. This example does not define properties for `"related"` as it is showing how empty objects and `null` are handled.

```
application/xml:
  schema:
    xml:
      name: product
    type: object
    required:
    - count
    - description
    - related
    properties:
      count:
        type:
        - number
        - "null"
        xml:
          nodeType: attribute
      rating:
        type: string
        xml:
          nodeType: attribute
      description:
        type: string
      related:
        type:
        - object
        - "null"
  examples:
    productWithNulls:
      dataValue:
        count: null
        description: Thing
        related: null
      externalValue: ./examples/productWithNulls.xml
    productNoNulls:
      dataValue:
        count: 42
        description: Thing
        related: {}
      externalValue: ./examples/productNoNulls.xml
```

Where `./examples/productWithNulls.xml` would be:

```
<product>
  <description>Thing</description>
  <related xsi:nil="true" />
</product>
```

and `./examples/productNoNulls.xml` would be:

```
<product count="42">
  <description>Thing</description>
  <related></related>
</product>
```

### 4.27 Security Scheme Object

[](https://spec.openapis.org/oas/latest.html#security-scheme-object)

Defines a security scheme that can be used by the operations.

Supported schemes are HTTP authentication, an API key (either as a header, a cookie parameter or as a query parameter), mutual TLS (use of a client certificate), OAuth2’s common flows (implicit, password, client credentials and authorization code) as defined in \[[RFC6749](https://spec.openapis.org/oas/latest.html#bib-rfc6749 "The OAuth 2.0 Authorization Framework")\], OAuth2 device authorization flow as defined in \[[RFC8628](https://spec.openapis.org/oas/latest.html#bib-rfc8628 "OAuth 2.0 Device Authorization Grant")\], and \[[OpenID-Connect-Core](https://spec.openapis.org/oas/latest.html#bib-openid-connect-core "OpenID Connect Core 1.0 incorporating errata set 2")\]. Please note that as of 2020, the implicit flow is about to be deprecated by [OAuth 2.0 Security Best Current Practice](https://tools.ietf.org/html/draft-ietf-oauth-security-topics). Recommended for most use cases is Authorization Code Grant flow with PKCE.

#### 4.27.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-23)

| Field Name | Type | Applies To | Description |
| --- | --- | --- | --- |
| type | `string` | Any | ***REQUIRED***. The type of the security scheme. Valid values are `"apiKey"`, `"http"`, `"mutualTLS"`, `"oauth2"`, `"openIdConnect"`. |
| description | `string` | Any | A description for security scheme. \[[CommonMark](https://spec.openapis.org/oas/latest.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| name | `string` | `apiKey` | ***REQUIRED***. The name of the header, query or cookie parameter to be used. |
| in | `string` | `apiKey` | ***REQUIRED***. The location of the API key. Valid values are `"query"`, `"header"`, or `"cookie"`. |
| scheme | `string` | `http` | ***REQUIRED***. The name of the HTTP Authentication scheme to be used in the Authorization header as defined in \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 16.4.1](https://datatracker.ietf.org/doc/html/rfc9110#section-16.4.1). The values used *SHOULD* be registered in the [IANA Authentication Scheme registry](https://spec.openapis.org/oas/latest.html#bib-iana-http-authschemes "Hypertext Transfer Protocol (HTTP) Authentication Scheme Registry"). The value is case-insensitive, as defined in \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 11.1](https://datatracker.ietf.org/doc/html/rfc9110#section-11.1). |
| bearerFormat | `string` | `http` (`"bearer"`) | A hint to the client to identify how the bearer token is formatted. Bearer tokens are usually generated by an authorization server, so this information is primarily for documentation purposes. |
| flows | [OAuth Flows Object](https://spec.openapis.org/oas/latest.html#oauth-flows-object) | `oauth2` | ***REQUIRED***. An object containing configuration information for the flow types supported. |
| openIdConnectUrl | `string` | `openIdConnect` | ***REQUIRED***. [Well-known URL](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig) to discover the \[[OpenID-Connect-Discovery](https://spec.openapis.org/oas/latest.html#bib-openid-connect-discovery "OpenID Connect Discovery 1.0 incorporating errata set 2")\] [provider metadata](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata). |
| oauth2MetadataUrl | `string` | `oauth2` | URL to the OAuth2 authorization server metadata \[[RFC8414](https://spec.openapis.org/oas/latest.html#bib-rfc8414 "OAuth 2.0 Authorization Server Metadata")\]. TLS is required. |
| deprecated | `boolean` | Any | Declares this security scheme to be deprecated. Consumers *SHOULD* refrain from usage of the declared scheme. Default value is `false`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.27.2 Security Scheme Object Examples

[](https://spec.openapis.org/oas/latest.html#security-scheme-object-examples)

##### 4.27.2.1 Basic Authentication Example

[](https://spec.openapis.org/oas/latest.html#basic-authentication-example)

```
type: http
scheme: basic
```

##### 4.27.2.2 API Key Example

[](https://spec.openapis.org/oas/latest.html#api-key-example)

```
type: apiKey
name: api-key
in: header
```

##### 4.27.2.3 JWT Bearer Example

[](https://spec.openapis.org/oas/latest.html#jwt-bearer-example)

```
type: http
scheme: bearer
bearerFormat: JWT
```

##### 4.27.2.4 MutualTLS Example

[](https://spec.openapis.org/oas/latest.html#mutualtls-example)

```
type: mutualTLS
description: Cert must be signed by example.com CA
```

##### 4.27.2.5 Implicit OAuth2 Example

[](https://spec.openapis.org/oas/latest.html#implicit-oauth2-example)

```
type: oauth2
flows:
  implicit:
    authorizationUrl: https://example.com/api/oauth/dialog
    scopes:
      write:pets: modify pets in your account
      read:pets: read your pets
```

### 4.28 OAuth Flows Object

[](https://spec.openapis.org/oas/latest.html#oauth-flows-object)

Allows configuration of the supported OAuth Flows.

#### 4.28.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-24)

| Field Name | Type | Description |
| --- | --- | --- |
| implicit | [OAuth Flow Object](https://spec.openapis.org/oas/latest.html#oauth-flow-object) | Configuration for the OAuth Implicit flow |
| password | [OAuth Flow Object](https://spec.openapis.org/oas/latest.html#oauth-flow-object) | Configuration for the OAuth Resource Owner Password flow |
| clientCredentials | [OAuth Flow Object](https://spec.openapis.org/oas/latest.html#oauth-flow-object) | Configuration for the OAuth Client Credentials flow. Previously called `application` in OpenAPI 2.0. |
| authorizationCode | [OAuth Flow Object](https://spec.openapis.org/oas/latest.html#oauth-flow-object) | Configuration for the OAuth Authorization Code flow. Previously called `accessCode` in OpenAPI 2.0. |
| deviceAuthorization | [OAuth Flow Object](https://spec.openapis.org/oas/latest.html#oauth-flow-object) | Configuration for the OAuth Device Authorization flow. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

### 4.29 OAuth Flow Object

[](https://spec.openapis.org/oas/latest.html#oauth-flow-object)

Configuration details for a supported OAuth Flow

#### 4.29.1 Fixed Fields

[](https://spec.openapis.org/oas/latest.html#fixed-fields-25)

| Field Name | Type | Applies To | Description |
| --- | --- | --- | --- |
| authorizationUrl | `string` | `oauth2` (`"implicit"`, `"authorizationCode"`) | ***REQUIRED***. The authorization URL to be used for this flow. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| deviceAuthorizationUrl | `string` | `oauth2` (`"deviceAuthorization"`) | ***REQUIRED***. The device authorization URL to be used for this flow. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| tokenUrl | `string` | `oauth2` (`"password"`, `"clientCredentials"`, `"authorizationCode"`, `"deviceAuthorization"`) | ***REQUIRED***. The token URL to be used for this flow. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| refreshUrl | `string` | `oauth2` | The URL to be used for obtaining refresh tokens. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| scopes | Map\[`string`, `string`\] | `oauth2` | ***REQUIRED***. The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map *MAY* be empty. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/latest.html#specification-extensions).

#### 4.29.2 OAuth Flow Object Example

[](https://spec.openapis.org/oas/latest.html#oauth-flow-object-example)

```
type: oauth2
flows:
  implicit:
    authorizationUrl: https://example.com/api/oauth/dialog
    scopes:
      write:pets: modify pets in your account
      read:pets: read your pets
  authorizationCode:
    authorizationUrl: https://example.com/api/oauth/dialog
    tokenUrl: https://example.com/api/oauth/token
    scopes:
      write:pets: modify pets in your account
      read:pets: read your pets
```

### 4.30 Security Requirement Object

[](https://spec.openapis.org/oas/latest.html#security-requirement-object)

Lists the required security schemes to execute this operation.

The name used for each property *MUST* either correspond to a security scheme declared in the [Security Schemes](https://spec.openapis.org/oas/latest.html#components-security-schemes) under the [Components Object](https://spec.openapis.org/oas/latest.html#components-object), or be the URI of a Security Scheme Object. Property names that are identical to a component name under the Components Object *MUST* be treated as a component name. To reference a Security Scheme with a single-segment relative URI reference (e.g. `foo`) that collides with a component name (e.g. `#/components/securitySchemes/foo`), use the `.` path segment (e.g. `./foo`).

Using a Security Scheme component name that appears to be a URI is *NOT RECOMMENDED*, as the precedence of component-name-matching over URI resolution, which is necessary to maintain compatibility with prior OAS versions, is counter-intuitive. See also [Security Considerations](https://spec.openapis.org/oas/latest.html#security-considerations).

A Security Requirement Object *MAY* refer to multiple security schemes in which case all schemes *MUST* be satisfied for a request to be authorized. This enables support for scenarios where multiple query parameters or HTTP headers are required to convey security information.

When the `security` field is defined on the [OpenAPI Object](https://spec.openapis.org/oas/latest.html#openapi-object) or [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) and contains multiple Security Requirement Objects, only one of the entries in the list needs to be satisfied to authorize the request. This enables support for scenarios where the API allows multiple, independent security schemes.

An empty Security Requirement Object (`{}`) indicates anonymous access is supported.

#### 4.30.1 Patterned Fields

[](https://spec.openapis.org/oas/latest.html#patterned-fields-2)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | \[`string`\] | Each name or URI *MUST* correspond to a security scheme as described above. If the security scheme is of type `"oauth2"` or `"openIdConnect"`, then the value is a list of scope names required for the execution, and the list *MAY* be empty if authorization does not require a specified scope. For other security scheme types, the array *MAY* contain a list of role names which are required for the execution, but are not otherwise defined or exchanged in-band. |

#### 4.30.2 Security Requirement Object Examples

[](https://spec.openapis.org/oas/latest.html#security-requirement-object-examples)

See also [Implicit Connection Resolution Examples](https://spec.openapis.org/oas/latest.html#implicit-connection-resolution-examples) in [Appendix G: Parsing and Resolution Guidance](https://spec.openapis.org/oas/latest.html#appendix-g-parsing-and-resolution-guidance) for an example using Security Requirement Objects in multi-document OpenAPI Descriptions.

##### 4.30.2.1 Non-OAuth2 Security Requirement

[](https://spec.openapis.org/oas/latest.html#non-oauth2-security-requirement)

```
api_key: []
```

##### 4.30.2.2 OAuth2 Security Requirement

[](https://spec.openapis.org/oas/latest.html#oauth2-security-requirement)

This example uses a component name for the Security Scheme.

```
petstore_auth:
  - write:pets
  - read:pets
```

##### 4.30.2.3 Optional OAuth2 Security

[](https://spec.openapis.org/oas/latest.html#optional-oauth2-security)

This example uses a relative URI reference for the Security Scheme.

Optional OAuth2 security as would be defined in an [OpenAPI Object](https://spec.openapis.org/oas/latest.html#openapi-object) or an [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object):

```
security:
  - {}
  - petstore_auth:
      - write:pets
      - read:pets
```

## 5\. Specification Extensions

[](https://spec.openapis.org/oas/latest.html#specification-extensions)

While the OpenAPI Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points.

The extensions properties are implemented as patterned fields that are always prefixed by `x-`.

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the OpenAPI Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. Field names beginning `x-oai-` and `x-oas-` are reserved for uses defined by the [OpenAPI Initiative](https://www.openapis.org/). The value can be any valid JSON value (`null`, a primitive, an array, or an object.) |

The OpenAPI Initiative maintains several [extension registries](https://spec.openapis.org/oas/latest.html#bib-openapi-registry "OpenAPI Initiative Registry"), including registries for [individual extension keywords](https://spec.openapis.org/registry/extension/) and [extension keyword namespaces](https://spec.openapis.org/registry/namespace/).

Extensions are one of the best ways to prove the viability of proposed additions to the specification. It is therefore *RECOMMENDED* that implementations be designed for extensibility to support community experimentation.

Support for any one extension is *OPTIONAL*, and support for one extension does not imply support for others.

## 6\. Security Considerations

[](https://spec.openapis.org/oas/latest.html#security-considerations)

### 6.1 OpenAPI Description Formats

[](https://spec.openapis.org/oas/latest.html#openapi-description-formats)

OpenAPI Descriptions use a combination of JSON, YAML, and JSON Schema, and therefore share their security considerations:

-   [JSON](https://www.iana.org/assignments/media-types/application/json)
-   [YAML](https://www.iana.org/assignments/media-types/application/yaml)
-   [JSON Schema Core](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-13)
-   [JSON Schema Validation](https://www.ietf.org/archive/id/draft-bhutton-json-schema-validation-01.html#section-10)

### 6.2 Tooling and Usage Scenarios

[](https://spec.openapis.org/oas/latest.html#tooling-and-usage-scenarios)

In addition, OpenAPI Descriptions are processed by a wide variety of tooling for numerous different purposes, such as client code generation, documentation generation, server side routing, and API testing. OpenAPI Description authors must consider the risks of the scenarios where the OpenAPI Description may be used.

### 6.3 Security Schemes

[](https://spec.openapis.org/oas/latest.html#security-schemes)

An OpenAPI Description describes the security schemes used to protect the resources it defines. The security schemes available offer varying degrees of protection. Factors such as the sensitivity of the data and the potential impact of a security breach should guide the selection of security schemes for the API resources. Some security schemes, such as basic auth and OAuth Implicit flow, are supported for compatibility with existing APIs. However, their inclusion in OpenAPI does not constitute an endorsement of their use, particularly for highly sensitive data or operations.

The rules for connecting a [Security Requirement Object](https://spec.openapis.org/oas/latest.html#security-requirement-object) to a [Security Scheme Object](https://spec.openapis.org/oas/latest.html#security-scheme-object) under a [Components Object](https://spec.openapis.org/oas/latest.html#components-object) are ambiguous in a way that could be exploited. Specifically:

-   It is implementation-defined whether a component name used by a Security Requirement Object in a referenced document is resolved from the entry document (*RECOMMENDED*) or the referenced document.
-   A Security Requirement Object that uses a URI to identify a Security Scheme Object can have the URI resolution hijacked by providing a Security Scheme component name identical to the URI, as the name lookup behavior takes precedence over URI resolution for compatibility with previous versions of the OAS.

### 6.4 Security Filtering

[](https://spec.openapis.org/oas/latest.html#security-filtering)

Some objects in the OpenAPI Specification *MAY* be declared and remain empty, or be completely removed, even though they are inherently the core of the API documentation.

The reasoning is to allow an additional layer of access control over the documentation. While not part of the specification itself, certain libraries *MAY* choose to allow access to parts of the documentation based on some form of authentication/authorization.

Two examples of this:

1.  The [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object) *MAY* be present but empty. It may be counterintuitive, but this may tell the viewer that they got to the right place, but can’t access any documentation. They would still have access to at least the [Info Object](https://spec.openapis.org/oas/latest.html#info-object) which may contain additional information regarding authentication.
2.  The [Path Item Object](https://spec.openapis.org/oas/latest.html#path-item-object) *MAY* be empty. In this case, the viewer will be aware that the path exists, but will not be able to see any of its operations or parameters. This is different from hiding the path itself from the [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object), because the user will be aware of its existence. This allows the documentation provider to finely control what the viewer can see.

### 6.5 Handling External Resources

[](https://spec.openapis.org/oas/latest.html#handling-external-resources)

OpenAPI Descriptions may contain references to external resources that may be dereferenced automatically by consuming tools. External resources may be hosted on different domains that may be untrusted.

### 6.6 Handling Reference Cycles

[](https://spec.openapis.org/oas/latest.html#handling-reference-cycles)

References in an OpenAPI Description may cause a cycle. Tooling must detect and handle cycles to prevent resource exhaustion.

### 6.7 Markdown and HTML Sanitization

[](https://spec.openapis.org/oas/latest.html#markdown-and-html-sanitization)

Certain fields allow the use of Markdown which can contain HTML including script. It is the responsibility of tooling to appropriately sanitize the Markdown.

## A. Appendix A: Revision History

[](https://spec.openapis.org/oas/latest.html#appendix-a-revision-history)

| Version | Date | Notes |
| --- | --- | --- |
| 3.2.0 | 2025-09-19 | Release of the OpenAPI Specification 3.2.0 |
| 3.1.2 | 2025-09-19 | Patch release of the OpenAPI Specification 3.1.2 |
| 3.1.1 | 2024-10-24 | Patch release of the OpenAPI Specification 3.1.1 |
| 3.1.0 | 2021-02-15 | Release of the OpenAPI Specification 3.1.0 |
| 3.1.0-rc1 | 2020-10-08 | rc1 of the 3.1 specification |
| 3.1.0-rc0 | 2020-06-18 | rc0 of the 3.1 specification |
| 3.0.4 | 2024-10-24 | Patch release of the OpenAPI Specification 3.0.4 |
| 3.0.3 | 2020-02-20 | Patch release of the OpenAPI Specification 3.0.3 |
| 3.0.2 | 2018-10-08 | Patch release of the OpenAPI Specification 3.0.2 |
| 3.0.1 | 2017-12-06 | Patch release of the OpenAPI Specification 3.0.1 |
| 3.0.0 | 2017-07-26 | Release of the OpenAPI Specification 3.0.0 |
| 3.0.0-rc2 | 2017-06-16 | rc2 of the 3.0 specification |
| 3.0.0-rc1 | 2017-04-27 | rc1 of the 3.0 specification |
| 3.0.0-rc0 | 2017-02-28 | Implementer’s Draft of the 3.0 specification |
| 2.0 | 2015-12-31 | Donation of Swagger 2.0 to the OpenAPI Initiative |
| 2.0 | 2014-09-08 | Release of Swagger 2.0 |
| 1.2 | 2014-03-14 | Initial release of the formal document. |
| 1.1 | 2012-08-22 | Release of Swagger 1.1 |
| 1.0 | 2011-08-10 | First release of the Swagger Specification |

## B. Appendix B: Data Type Conversion

[](https://spec.openapis.org/oas/latest.html#appendix-b-data-type-conversion)

Serializing typed data to plain text, which can occur in `text/plain` message bodies or `multipart` parts, as well as in the `application/x-www-form-urlencoded` format in either URL query strings or message bodies, involves significant implementation- or application-defined behavior.

[Schema Objects](https://spec.openapis.org/oas/latest.html#schema-object) validate data based on the [JSON Schema data model](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-4.2.1), which only recognizes four primitive data types: strings (which are [only broadly interoperable as UTF-8](https://tools.ietf.org/html/rfc7159#section-8.1)), numbers, booleans, and `null`. Notably, integers are not a distinct type from other numbers, with `type: "integer"` being a convenience defined mathematically, rather than based on the presence or absence of a decimal point in any string representation.

The [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object), [Header Object](https://spec.openapis.org/oas/latest.html#header-object), and [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) offer features to control how to arrange values from array or object types. They can also be used to control how strings are further encoded to avoid reserved or illegal characters. However, there is no general-purpose specification for converting schema-validated non-UTF-8 primitive data types (or entire arrays or objects) to strings.

Two cases do offer standards-based guidance:

-   \[[RFC3987](https://spec.openapis.org/oas/latest.html#bib-rfc3987 "Internationalized Resource Identifiers (IRIs)")\] [Section 3.1](https://datatracker.ietf.org/doc/html/rfc3987#section-3.1) provides guidance for converting non-Unicode strings to UTF-8, particularly in the context of URIs (and by extension, the form media types which use the same encoding rules)
-   \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] [Section 2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-2.3) specifies which values, including but not limited to `null`, are considered *undefined* and therefore treated specially in the expansion process when serializing based on that specification

Implementations of RFC6570 often have their own conventions for converting non-string values, but these are implementation-specific and not defined by the RFC itself. This is one reason for the OpenAPI Specification to leave these conversions as implementation-defined: It allows using RFC6570 implementations regardless of how they choose to perform the conversions.

To control the serialization of numbers, booleans, and `null` (or other values RFC6570 deems to be undefined) more precisely, schemas can be defined as `type: "string"` and constrained using `pattern`, `enum`, `format`, and other keywords to communicate how applications must pre-convert their data prior to schema validation. The resulting strings would not require any further type conversion.

The `format` keyword can assist in serialization. Some formats (such as `date-time`) are unambiguous, while others (such as [`decimal`](https://spec.openapis.org/registry/format/decimal.html) in the [Format Registry](https://spec.openapis.org/registry/format/)) are less clear. However, care must be taken with `format` to ensure that the specific formats are supported by all relevant tools as unrecognized formats are ignored.

Requiring input as pre-formatted, schema-validated strings also improves round-trip interoperability as not all programming languages and environments support the same data types.

## C. Appendix C: Using RFC6570-Based Serialization

[](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization)

Serialization is defined in terms of \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] URI Templates in three scenarios:

| Object | Condition |
| --- | --- |
| [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) | When `schema` is present |
| [Header Object](https://spec.openapis.org/oas/latest.html#header-object) | When `schema` is present |
| [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) | When encoding for `application/x-www-form-urlencoded` and any of `style`, `explode`, or `allowReserved` are used |

Implementations of this specification *MAY* use an implementation of RFC6570 to perform variable expansion, however, some caveats apply.

Note that when using `style: "form"` RFC6570 expansion to produce an `application/x-www-form-urlencoded` HTTP message body, it is necessary to remove the `?` prefix that is produced to satisfy the URI query string syntax.

When using `style` and similar keywords to produce a `multipart/form-data` body, the query string names are placed in the `name` parameter of the `Content-Disposition` part header, and the values are placed in the corresponding part body; the `?`, `=`, and `&` characters are not used, and URI percent encoding is not applied, regardless of the value of `allowReserved`. Note that while \[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] allows using \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] percent-encoding in “file names”, it does not otherwise address the use of percent-encoding within the format. Users are expected to provide names and data with any escaping necessary for conformance with RFC7578 already applied.

Note also that not all RFC6570 implementations support all four levels of operators, all of which are needed to fully support the OpenAPI Specification’s usage. Using an implementation with a lower level of support will require additional manual construction of URI Templates to work around the limitations.

### C.1 Equivalences Between Fields and RFC6570 Operators

[](https://spec.openapis.org/oas/latest.html#equivalences-between-fields-and-rfc6570-operators)

Certain field values translate to RFC6570 [operators](https://tools.ietf.org/html/rfc6570#section-2.2) (or lack thereof):

| field | value | equivalent |
| --- | --- | --- |
| style | `"simple"` | *n/a* |
| style | `"matrix"` | `;` prefix operator |
| style | `"label"` | `.` prefix operator |
| style | `"form"` | `?` prefix operator |
| allowReserved | `false` | *n/a* |
| allowReserved | `true` | `+` prefix operator |
| explode | `false` | *n/a* |
| explode | `true` | `*` modifier suffix |

Multiple `style: "form"` parameters are equivalent to a single RFC6570 [variable list](https://tools.ietf.org/html/rfc6570#section-2.2) using the `?` prefix operator:

```
parameters:
- name: foo
  in: query
  schema:
    type: object
  explode: true
- name: bar
  in: query
  schema:
    type: string
```

This example is equivalent to RFC6570’s `{?foo*,bar}`, and **NOT** `{?foo*}{&bar}`. The latter is problematic because if `foo` is not defined, the result will be an invalid URI. The `&` prefix operator has no equivalent in the Parameter Object.

Note that RFC6570 does not specify behavior for compound values beyond the single level addressed by `explode`. The result of using objects or arrays where no behavior is clearly specified for them is implementation-defined.

### C.2 Delimiters in Parameter Values

[](https://spec.openapis.org/oas/latest.html#delimiters-in-parameter-values)

Delimiters used by RFC6570 expansion, such as the `,` used to join arrays or object values with `style: "simple"`, are all automatically percent-encoded as long as `allowReserved` is `false`. Note that since RFC6570 does not define a way to parse variables based on a URI Template, users must take care to first split values by delimiter before percent-decoding values that might contain the delimiter character.

When `allowReserved` is `true`, both percent-encoding (prior to joining values with a delimiter) and percent-decoding (after splitting on the delimiter) must be done manually at the correct time.

See [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for additional guidance on handling delimiters for `style` values with no RFC6570 equivalent that already need to be percent-encoded when used as delimiters.

### C.3 Non-RFC6570 Field Values and Combinations

[](https://spec.openapis.org/oas/latest.html#non-rfc6570-field-values-and-combinations)

Configurations with no direct \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] equivalent *SHOULD* also be handled according to RFC6570. Implementations *MAY* create a properly delimited URI Template with variables for individual names and values using RFC6570 regular or reserved expansion (based on `allowReserved`).

This includes:

-   the styles `pipeDelimited`, `spaceDelimited`, and `deepObject`, which have no equivalents at all
-   the combination of the style `form` with `allowReserved: true`, which is not allowed because only one prefix operator can be used at a time
-   any parameter name that is not a legal RFC6570 variable name

The Parameter Object’s `name` field has a much more permissive syntax than RFC6570 [variable name syntax](https://tools.ietf.org/html/rfc6570#section-2.3). A parameter name that includes characters outside of the allowed RFC6570 variable character set *MUST* be percent-encoded before it can be used in a URI Template.

### C.4 Examples

[](https://spec.openapis.org/oas/latest.html#examples-1)

Let’s say we want to use the following data in a form query string, where `formulas` is exploded, and `words` is not:

```
formulas:
  a: x+y
  b: x/y
  c: x^y
words:
- math
- is
- fun
```

#### C.4.1 RFC6570-Equivalent Expansion

[](https://spec.openapis.org/oas/latest.html#rfc6570-equivalent-expansion)

This array of Parameter Objects uses regular `style: "form"` expansion, fully supported by \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\]:

```
parameters:
- name: formulas
  in: query
  schema:
    type: object
    additionalProperties:
      type: string
  explode: true
- name: words
  in: query
  schema:
    type: array
    items:
      type: string
```

This translates to the following URI Template:

```
{?formulas*,words}
```

when expanded with the data given earlier, we get:

```
?a=x%2By&b=x%2Fy&c=x%5Ey&words=math,is,fun
```

#### C.4.2 Expansion with Non-RFC6570-Supported Options

[](https://spec.openapis.org/oas/latest.html#expansion-with-non-rfc6570-supported-options)

But now let’s say that (for some reason), we really want that `/` in the `b` formula to show up as-is in the query string, and we want our words to be space-separated like in a written phrase. To do that, we’ll add `allowReserved: true` to `formulas`, and change to `style: "spaceDelimited"` for `words`:

```
parameters:
- name: formulas
  in: query
  schema:
    type: object
    additionalProperties:
      type: string
  explode: true
  allowReserved: true
- name: words
  in: query
  style: spaceDelimited
  explode: false
  schema:
    type: array
    items:
      type: string
```

We can’t combine the `?` and `+` RFC6570 [prefixes](https://tools.ietf.org/html/rfc6570#section-2.4.1), and there’s no way with RFC6570 to replace the `,` separator with a space character. So we need to restructure the data to fit a manually constructed URI Template that passes all of the pieces through the right sort of expansion.

Here is one such template, using a made-up convention of `words.0` for the first entry in the words value, `words.1` for the second, and `words.2` for the third:

```
?a={+a}&b={+b}&c={+c}&words={words.0} {words.1} {words.2}
```

RFC6570 [mentions](https://tools.ietf.org/html/rfc6570#section-2.4.2) the use of `.` “to indicate name hierarchy in substructures,” but does not define any specific naming convention or behavior for it. Since the `.` usage is not automatic, we’ll need to construct an appropriate input structure for this new template.

We’ll also need to pre-process the values for `formulas` because while `/` and most other reserved characters are allowed in the query string by RFC3986, `[`, `]`, and `#` [are not](https://tools.ietf.org/html/rfc3986#appendix-A), and `&`, `=`, and `+` all have [special behavior](https://url.spec.whatwg.org/#application/x-www-form-urlencoded) in the `application/x-www-form-urlencoded` format, which is what we are using in the query string.

Setting `allowReserved: true` does *not* make reserved characters that are not allowed in URIs allowed, it just allows them to be *passed through expansion unchanged*, for example because some other specification has defined a particular meaning for them.

Therefore, users still need to percent-encode any reserved characters that are *not* being passed through due to a special meaning because reserved expansion does not know which reserved characters are being used, and which should still be percent-encoded. However, reserved expansion, unlike regular expansion, *will* leave the pre-percent-encoded triples unchanged. See also [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types) for further guidance on percent-encoding and form media types, including guidance on handling the delimiter characters for `spaceDelimited`, `pipeDelimited`, and `deepObject` in parameter names and values.

So here is our data structure that arranges the names and values to suit the template above, where values for `formulas` have `[]#&=+` pre-percent encoded (although only `+` appears in this example):

```
a: x%2By
b: x/y
c: x^y
words.0: math
words.1: is
words.2: fun
```

Expanding our manually assembled template with our restructured data yields the following query string:

```
?a=x%2By&b=x/y&c=x%5Ey&words=math%20is%20fun
```

The `/` and the pre-percent-encoded `%2B` have been left alone, but the disallowed `^` character (inside a value) and space characters (in the template but outside of the expanded variables) were percent-encoded.

#### C.4.3 Undefined Values and Manual URI Template Construction

[](https://spec.openapis.org/oas/latest.html#undefined-values-and-manual-uri-template-construction)

Care must be taken when manually constructing templates to handle the values that RFC6570 [considers to be *undefined*](https://tools.ietf.org/html/rfc6570#section-2.3) correctly:

```
formulas: {}
words:
- hello
- world
```

Using this data with our original RFC6570-friendly URI Template, `{?formulas*,words}`, produces the following:

```
?words=hello,world
```

This means that the manually constructed URI Template and restructured data need to leave out the `formulas` object entirely so that the `words` parameter is the first and only parameter in the query string.

Restructured data:

```
words.0: hello
words.1: world
```

Manually constructed URI Template:

```
?words={words.0} {words.1}
```

Result:

```
?words=hello%20world
```

#### C.4.4 Illegal Variable Names as Parameter Names

[](https://spec.openapis.org/oas/latest.html#illegal-variable-names-as-parameter-names)

In this example, the heart emoji is not legal in URI Template names (or URIs):

```
parameters:
- name: ❤️
  in: query
  schema:
    type: string
```

We can’t just pass `❤️: "love!"` to an RFC6570 implementation. Instead, we have to pre-percent-encode the name (which is a six-octet UTF-8 sequence) in both the data and the URI Template:

```
"%E2%9D%A4%EF%B8%8F": love!
```

```
{?%E2%9D%A4%EF%B8%8F}
```

This will expand to the result:

```
?%E2%9D%A4%EF%B8%8F=love%21
```

## D. Appendix D: Serializing Headers and Cookies

[](https://spec.openapis.org/oas/latest.html#appendix-d-serializing-headers-and-cookies)

HTTP headers have inconsistent rules regarding what characters are allowed, and how some or all disallowed characters can be escaped and included. While the `quoted-string` ABNF rule given in \[[RFC9110](https://spec.openapis.org/oas/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 5.4.6](https://tools.ietf.org/html/rfc9110#section-5.6.4) is the most common escaping solution, it is not sufficiently universal to apply automatically. For example, a strong `ETag` looks like `"foo"` (with quotes, regardless of the contents), and a weak `ETag` looks like `W/"foo"` (note that only part of the value is quoted); the contents of the quotes for this header are also not escaped in the way `quoted-string` contents are.

For this reason, any data being passed to a header by way of a [Parameter](https://spec.openapis.org/oas/latest.html#parameter-object) or [Header](https://spec.openapis.org/oas/latest.html#header-object) Object needs to be quoted and escaped prior to passing it to the OAS implementation, and the parsed header values are expected to contain the quotes and escapes.

### D.1 Percent-Encoding and Cookies

[](https://spec.openapis.org/oas/latest.html#percent-encoding-and-cookies)

\[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\]'s percent-encoding behavior is not always appropriate for `in: "cookie"` parameters. While percent-encoding seems more common as an escaping mechanism than the base64 encoding (`contentEncoding`: “base64”) recommended by \[[RFC6265](https://spec.openapis.org/oas/latest.html#bib-rfc6265 "HTTP State Management Mechanism")\], [section 5.6 of draft-ietf-httpbis-rfc6265bis-20](https://www.ietf.org/archive/id/draft-ietf-httpbis-rfc6265bis-20.html#section-5.6), the proposed update to that RFC notes that cookies sent in the `Set-Cookie` response header that appear to be percent-encoded *MUST NOT* be decoded when stored by the client, which would mean that they are already encoded when retrieved from that storage for use in the `Cookie` request header. The behavior of `style: "cookie"` assumes this usage, and *does not* apply or remove percent-encoding.

If automatic percent-encoding is desired, `style: "form"` with a primitive value or with the non-default `explode` value of `false` provides this behavior. However, note that the default value of `explode: true` for `style: "form"` with non-primitive values uses the wrong delimiter for cookies (`&` instead of `;` followed by a single space) to set multiple cookie values. Using `style: "form"` with `in: "cookie"` via an RFC6570 implementation requires stripping the `?` prefix, as when producing `application/x-www-form-urlencoded` message bodies. To allow the full use of `style: "form"` with `in: "cookie"`, use the `allowReserved` field.

## E. Appendix E: Percent-Encoding and Form Media Types

[](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types)

***NOTE:** In this section, the `application/x-www-form-urlencoded` and `multipart/form-data` media types are abbreviated as `form-urlencoded` and `form-data`, respectively, for readability.*

Percent-encoding is used in URIs and media types that derive their syntax from URIs. The fundamental rules of percent-encoding are:

-   The set of characters that *MUST* be encoded varies depending on which version of which specification you use, and (for URIs) in which part of the URI the character appears.
-   The way an unencoded `+` character is decoded depends on whether you are using `application/x-www-form-urlencoded` rules or more general URI rules; this is the only time where choice of decoding algorithm can change the outcome.
-   Encoding more characters than necessary is always safe in terms of the decoding process, but may produce non-normalized URIs.
-   In practice, some systems tolerate or even expect unencoded characters that some or all percent-encoding specifications require to be encoded; this can cause interoperability issues with more strictly compliant implementations.

The rest of this appendix provides more detailed guidance based on the above rules.

### E.1 Percent-Encoding Character Classes

[](https://spec.openapis.org/oas/latest.html#percent-encoding-character-classes)

This process is concerned with three classes of characters, the names of which vary among specifications but are defined as follows for the purposes of this section:

-   *unreserved* characters do not need to be percent-encoded; while it is safe to percent-encode them, doing so produces a URI that is [not normalized](https://tools.ietf.org/html/rfc3986#section-6.2.2.2)
-   *reserved* characters either have special behavior in the URI syntax (such as delimiting components) or are reserved for other specifications that need to define special behavior (e.g. `form-urlencoded` defines special behavior for `=`, `&`, and `+`)
-   *unsafe* characters are known to cause problems when parsing URIs in certain environments

Unless otherwise specified, this section uses RFC3986’s definition of [reserved](https://tools.ietf.org/html/rfc3986#section-2.2) and [unreserved](https://tools.ietf.org/html/rfc3986#section-2.3), and defines the unsafe set as all characters not included in either of those sets.

### E.2 Percent-Encoding and `form-urlencoded`

[](https://spec.openapis.org/oas/latest.html#percent-encoding-and-form-urlencoded)

Each URI component (such as the query string) considers some of the reserved characters to be unsafe, either because they serve as delimiters between the components (e.g. `#`), or (in the case of `[` and `]`) were historically considered globally unsafe but were later given reserved status for limited purposes.

Reserved characters with no special meaning defined within a component can be left un-percent encoded. However, other specifications can define special meanings, requiring percent-encoding for those characters outside of the additional special meanings.

The `form-urlencoded` media type defines special meanings for `=` and `&` as delimiters, and `+` as the replacement for the space character (instead of its percent-encoded form of `%20`). This means that while these three characters are reserved-but-allowed in query strings by RFC3986, they must be percent-encoded in `form-urlencoded` query strings except when used for their `form-urlencoded` purposes; see [Appendix C](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for an example of handling `+` in form values.

### E.3 Percent-Encoding and `form-data`

[](https://spec.openapis.org/oas/latest.html#percent-encoding-and-form-data)

\[[RFC7578](https://spec.openapis.org/oas/latest.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 2](https://datatracker.ietf.org/doc/html/rfc7578#section-2) suggests RFC3986-based percent-encoding as a mechanism to keep text-based per-part header data such as file names within the ASCII character set. This suggestion was not part of older (pre-2015) specifications for `form-data`, so care must be taken to ensure interoperability. Users wishing to use percent-encoding in this way *MUST* provide the data in percent-encoded form, as percent-encoding is not automatically applied for this media type regardless of which Encoding Object fields are used.

The `form-data` media type allows arbitrary text or binary data in its parts, so percent-encoding or similar escaping is not needed in general.

### E.4 Generating and Validating URIs and `form-urlencoded` Strings

[](https://spec.openapis.org/oas/latest.html#generating-and-validating-uris-and-form-urlencoded-strings)

URI percent encoding and the `form-urlencoded` media type have complex specification histories spanning multiple revisions and, in some cases, conflicting claims of ownership by different standards bodies. Unfortunately, these specifications each define slightly different percent-encoding rules, which need to be taken into account if the URIs or `form-urlencoded` message bodies will be subject to strict validation. (Note that many URI parsers do not perform validation by default, if at all.)

This specification normatively cites the following relevant standards:

| Specification | Date | OAS Usage | Percent-Encoding | Notes |
| --- | --- | --- | --- | --- |
| \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] | 01/2005 | URI/URL syntax, including non-`form-urlencoded` content-based serialization | \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] | obsoletes \[[RFC1738](https://spec.openapis.org/oas/latest.html#bib-rfc1738 "Uniform Resource Locators (URL)")\], \[[RFC2396](https://spec.openapis.org/oas/latest.html#bib-rfc2396 "Uniform Resource Identifiers (URI): Generic Syntax")\] |
| \[[RFC6570](https://spec.openapis.org/oas/latest.html#bib-rfc6570 "URI Template")\] | 03/2012 | style-based serialization | \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] | does not use `+` for query strings |
| [WHATWG-URL Section 5](https://url.spec.whatwg.org/#application/x-www-form-urlencoded) | “living” standard | content-based `form/url-encoded` serialization, including HTTP message contents | [WHATWG-URL Section 1.3](https://url.spec.whatwg.org/#application-x-www-form-urlencoded-percent-encode-set) | obsoletes \[[RFC1866](https://spec.openapis.org/oas/latest.html#bib-rfc1866 "Hypertext Markup Language - 2.0")\], \[[HTML401](https://spec.openapis.org/oas/latest.html#bib-html401 "HTML 4.01 Specification")\] |

Style-based serialization with percent-encoding is used in the [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) when `schema` is present, and in the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) when at least one of `style`, `explode`, or `allowReserved` is present. See [Appendix C](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization) for more details of RFC6570’s two different approaches to percent-encoding, including an example involving `+`.

Content-based serialization is defined by the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object), and used with the [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object) and [Header Object](https://spec.openapis.org/oas/latest.html#header-object) when the `content` field is present, and with the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) based on the `contentType` field when the fields `style`, `explode`, and `allowReserved` are absent. For use in URIs, each part is encoded based on the media type (e.g. `text/plain` or `application/json`), and must then be percent-encoded for use in a `form-urlencoded` string (in form-style query strings), or for general URI use in other URL components, unless the media type already incorporates URI percent-encoding.

#### E.4.1 Interoperability with Historical Specifications

[](https://spec.openapis.org/oas/latest.html#interoperability-with-historical-specifications)

Prior versions of this specification required \[[RFC1866](https://spec.openapis.org/oas/latest.html#bib-rfc1866 "Hypertext Markup Language - 2.0")\] and its use of \[[RFC1738](https://spec.openapis.org/oas/latest.html#bib-rfc1738 "Uniform Resource Locators (URL)")\] percent-encoding rules in place of \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\]. The \[[WHATWG-URL](https://spec.openapis.org/oas/latest.html#bib-whatwg-url "URL Standard")\] `form-urlencoded` rules represent the current browser consensus on that media type, and avoid the ambiguity introduced by unclear paraphrasing of RFC1738 in RFC1866.

Users needing conformance with RFC1866/RFC1738 are advised to check their tooling and library behavior carefully.

#### E.4.2 Interoperability with Web Browser Environments

[](https://spec.openapis.org/oas/latest.html#interoperability-with-web-browser-environments)

WHATWG is a [web browser-oriented](https://whatwg.org/faq#what-is-the-whatwg-working-on) standards group that has defined a “URL Living Standard” for parsing and serializing URLs in a browser context, including parsing and serializing `form-urlencoded` data. WHATWG’s percent-encoding rules for query strings are different depending on whether the query string is [being treated as `form-urlencoded`](https://url.spec.whatwg.org/#application-x-www-form-urlencoded-percent-encode-set) (where it requires more percent-encoding than \[[RFC1738](https://spec.openapis.org/oas/latest.html#bib-rfc1738 "Uniform Resource Locators (URL)")\]) or [as part of the generic syntax](https://url.spec.whatwg.org/#query-percent-encode-set), where its requirements differ from \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\].

This specification only depends on WHATWG for its `form-urlencoded` specification. Implementations using the query string in other ways are advised that, the distinctions between WHATWG’s non-`form-urlencoded` query string rules and RFC3986 require careful consideration, incorporating both WHATWG’s percent-encoding sets and their set of valid Unicode code points for URLs; see [Percent-Encoding and Illegal or Reserved Delimiters](https://spec.openapis.org/oas/latest.html#percent-encoding-and-illegal-or-reserved-delimiters) for more information.

### E.5 Decoding URIs and `form-urlencoded` Strings

[](https://spec.openapis.org/oas/latest.html#decoding-uris-and-form-urlencoded-strings)

The percent-decoding algorithm does not care which characters were or were not percent-decoded, which means that URIs percent-encoded according to any specification will be decoded correctly.

Similarly, all `form-urlencoded` decoding algorithms simply add `+`\-for-space handling to the percent-decoding algorithm, and will work regardless of the encoding specification used.

However, care must be taken to use `form-urlencoded` decoding if `+` represents a space, and to use regular percent-decoding if `+` represents itself as a literal value.

### E.6 Percent-Encoding and Illegal or Reserved Delimiters

[](https://spec.openapis.org/oas/latest.html#percent-encoding-and-illegal-or-reserved-delimiters)

The `[`, `]`, `|`, and space characters, which are used as delimiters for the `deepObject`, `pipeDelimited`, and `spaceDelimited` styles, respectively, all *MUST* be percent-encoded to comply with \[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\]. This requires users to pre-encode the character(s) in some other way in parameter names and values to distinguish them from the delimiter usage when using one of these styles.

The space character is always illegal and encoded in some way by all implementations of all versions of the relevant standards. While one could use the `form-urlencoded` convention of `+` to distinguish spaces in parameter names and values from `spaceDelimited` delimiters encoded as `%20`, the specifications define the decoding as a single pass, making it impossible to distinguish the different usages in the decoded result unless a non-standard parsing algorithm is used that separates based on one delimiter before decoding the other. Any such non-standard parsing approach will not be interoperable across all tools.

Some environments use `[`, `]`, and possibly `|` unencoded in query strings without apparent difficulties. WHATWG’s generic query string rules do not require percent-encoding them in non-`form-urlencoded` query strings, although it also excludes them from the set of valid URL Unicode code points. Code that relies on leaving these delimiters unencoded, while using regular percent-encoding for them within names and values, is not guaranteed to be interoperable across all implementations.

For maximum interoperability, it is *RECOMMENDED* to either define and document an additional escape convention while percent-encoding the delimiters for these styles, or to avoid these styles entirely. The exact method of additional encoding/escaping is left to the API designer, and is expected to be performed before serialization and encoding described in this specification, and reversed after this specification’s encoding and serialization steps are reversed. This keeps it outside of the processes governed by this specification.

## F. Appendix F: Examples of Base URI Determination and Reference Resolution

[](https://spec.openapis.org/oas/latest.html#appendix-f-examples-of-base-uri-determination-and-reference-resolution)

This section shows each of the four possible sources of base URIs, followed by an example with a relative `$self` and `$id`.

### F.1 Base URI Within Content

[](https://spec.openapis.org/oas/latest.html#base-uri-within-content)

A base URI within the resource’s content (\[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.1](https://datatracker.ietf.org/doc/html/rfc3986#section-5.1.1)) is the highest-precedence source of a base URI. For OpenAPI documents, this source is the OpenAPI Object’s `$self` field, while for Schema Objects that contain a `$id`, or are a subschema of a Schema Object containing a `$id`, the source is the `$id` field:

Assume the retrieval URI of the following document is `file://home/someone/src/api/openapi.yaml`:

```
openapi: 3.2.0
$self: https://example.com/api/openapi
info:
  title: Example API
  version: 1.0
paths:
  /foo:
    get:
      requestBody:
        $ref: "shared/foo#/components/requestBodies/Foo"
```

Assume the retrieval URI for the following document is `https://git.example.com/shared/blob/main/shared/foo.yaml`:

```
openapi: 3.2.0
$self: https://example.com/api/shared/foo
info:
  title: Shared components for all APIs
  version: 1.0
components:
  requestBodies:
    Foo:
      content:
        application/json:
          schema:
            $ref: ../schemas/foo
  schemas:
    Foo:
      $id: https://example.com/api/schemas/foo
      properties:
        bar:
          $ref: bar
    Bar:
      $id: https://example.com/api/schemas/bar
      type: string
```

In this example, the retrieval URIs are irrelevant because both documents define `$self`.

The relative `$ref` in the first document is resolved against `$self` to produce `https://example.com/api/shared/foo#/components/requestBodies/Foo`. The portion of that URI before the `#` matches the `$self` of the second document, so the reference target is resolved to `#/components/requestBodies/Foo` in that second document.

In that document, the `$ref` in the Request Body Object is resolved using that document’s `$self` as the base URI, producing `https://example.com/api/schemas/foo`. This matches the `$id` at `#/components/schemas/Foo/$id` so it points to that Schema Object. That Schema Object has a subschema with `$ref: bar`, which is resolved against the `$id` to produce `https://example.com/api/schemas/bar`, which matches the `$id` at `#/components/schemas/Bar/$id`.

To guarantee interoperability, Schema Objects containing an `$id`, or that are under a schema containing an `$id`, *MUST* be referenced by the nearest such `$id` for the non-fragment part of the reference. As the JSON Schema specification notes, using a base URI other than the nearest `$id` and crossing that `$id` with a JSON Pointer fragment [is not interoperable](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#name-json-pointer-fragments-and-).

Note also that it is impossible for the reference at `#/components/schemas/Foo/properties/bar/$ref` to reference the schema at `#/components/schemas/Bar` using *only* a JSON Pointer fragment, as the JSON Pointer would be resolved relative to `https://example.com/api/schemas/foo`, not to the OpenAPI document’s base URI from `$self`.

### F.2 Base URI From Encapsulating Entity

[](https://spec.openapis.org/oas/latest.html#base-uri-from-encapsulating-entity)

If no base URI can be determined within the content, the next location to search is any encapsulating entity (\[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.2](https://datatracker.ietf.org/doc/html/rfc3986#section-5.1.2)).

This is common for Schema Objects encapsulated within an OpenAPI document. An example of an OpenAPI Object itself being encapsulated in another entity would be a `multipart/related` archive (\[[RFC2557](https://spec.openapis.org/oas/latest.html#bib-rfc2557 "MIME Encapsulation of Aggregate Documents, such as HTML (MHTML)")\]), such as the following `multipart/related; boundary="boundary-example"; type="application/openapi+yaml"` document. Note that this is purely an example, and support for such multipart documents or any other format that could encapsulate an OpenAPI Object is not a requirement of this specification.

RFC2557 was written to allow sending hyperlinked sets of documents as email attachments, in which case there would not be a retrieval URI for the multipart attachment (although the format could also be used in HTTP as well).

```
--boundary-example
Content-Type: application/openapi+yaml
Content-Location: https://example.com/api/openapi.yaml

openapi: 3.2.0
info:
  title: Example API
  version: 1.0
  externalDocs:
    url: docs.html
components:
  requestBodies:
    Foo:
      content:
        application/json:
          schema:
            $ref: "#/components/api/schemas/Foo"
  schemas:
    Foo:
      properties:
        bar:
          $ref: schemas/bar
--boundary-example
Content-Type: application/schema+json
Content-Location: https://example.com/api/schemas/bar

{
  "type": "string"
}
--boundary-example
Content-Type: text/html
Content-Location: https://example.com/api/docs.html

<html>
  <head>
    <title>API Documentation</title>
  </head>
  <body>
    <p>Awesome documentation goes here</p>
  </body>
</html>
--boundary-example
```

In this example, the URI for each part, which also serves as its base URI, comes from the part’s `Content-Location` header as specified by RFC2557. Since the Schema Object at `#/components/schemas/Foo` does not contain an `$id`, the reference in its subschema uses the OpenAPI document’s base URI, which is taken from the `Content-Location` header of its part within the `multipart/related` format. The resulting reference to `https://example.com/schemas/bar` matches the `Content-Location` header of the second part, which according to RFC2557 allows the reference target to be located within the multipart archive.

Similarly, the `url` field of the [External Documentation Object](https://spec.openapis.org/oas/latest.html#external-documentation-object) is resolved against the base URI from `Content-Location`, producing `https://example.com/api/docs.html` which matches the `Content-Location` of the third part.

### F.3 Base URI From the Retrieval URI

[](https://spec.openapis.org/oas/latest.html#base-uri-from-the-retrieval-uri)

If no base URI is provided from either of the previous sources, the next source is the retrieval URI (\[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.3](https://datatracker.ietf.org/doc/html/rfc3986#section-5.1.3)).

Assume this document was retrieved from `https://example.com/api/openapis.yaml`:

```
openapi: 3.2.0
info:
  title: Example API
  version: 1.0
components:
  requestBodies:
    Foo:
      content:
        application/json:
          schema:
            $ref: schemas/foo
```

Assume this document was retrieved from `https://example.com/api/schemas/foo`:

```
{
  "type": "object",
  "properties": {
    "bar": {
      "type": "string"
    }
  }
}
```

Resolving the `$ref: schemas/foo` against the retrieval URI of the OpenAPI document produces `https://example.com/api/schemas/foo`, the retrieval URI of the JSON Schema document.

### F.4 Application-Specific Default Base URI

[](https://spec.openapis.org/oas/latest.html#application-specific-default-base-uri)

When constructing an OpenAPI document in memory that does not have a `$self`, or an encapsulating entity, or a retrieval URI, applications can resolve internal (fragment-only) references by assuming a default base URI (\[[RFC3986](https://spec.openapis.org/oas/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 5.1.4](https://datatracker.ietf.org/doc/html/rfc3986#section-5.1.4)). While this sort of internal resolution can be performed in practice without choosing a base URI, choosing one, such as a URN with a randomly generated UUID (e.g. `urn:uuid:f26cdaad-3193-4398-a838-4ecb7326c4c5`) avoids the need to implement it as a special case.

### F.5 Resolving Relative `$self` and `$id`

[](https://spec.openapis.org/oas/latest.html#resolving-relative-self-and-id)

Let’s re-consider the first example in this appendix, but with relative URI references for `$self` and `$id`, and retrieval URIs that support that relative usage:

Assume that the following is retrieved from `https://staging.example.com/api/openapi`:

```
openapi: 3.2.0
$self: /api/openapi
info:
  title: Example API
  version: 1.0
paths:
  /foo:
    get:
      requestBody:
        $ref: "shared/foo#/components/requestBodies/Foo"
```

Assume the retrieval URI for the following document is `https://staging.example.com/api/shared/foo`:

```
openapi: 3.2.0
$self: /api/shared/foo
info:
  title: Shared components for all APIs
  version: 1.0
components:
  requestBodies:
    Foo:
      content:
        application/json:
          schema:
            $ref: ../schemas/foo
  schemas:
    Foo:
      $id: /api/schemas/foo
      properties:
        bar:
          $ref: bar
    Bar:
      $id: /api/schemas/bar
      type: string
```

In this example, all of the `$self` and `$id` values are relative URI references consisting of an absolute path. This allows the retrieval URI to set the host (and scheme), in this case `https://staging.example.com`, resulting in the first document’s `$self` being `https://staging.example.com/openapi`, and the second document’s `$self` being `https://staging.example.com/api/shared/foo`, with `$id` values of `https://staging.example.com/api/schemas/foo` and `https://staging.example.com/api/schemas/bar`. Relative `$self` and `$id` values of this sort allow the same set of documents to work when deployed to other hosts, e.g. `https://example.com` (production) or `https://localhost:8080` (local development).

## G. Appendix G: Parsing and Resolution Guidance

[](https://spec.openapis.org/oas/latest.html#appendix-g-parsing-and-resolution-guidance)

Implementations *MAY* support complete-document parsing in any of the following ways:

-   Detecting OpenAPI or JSON Schema documents using media types
-   Detecting OpenAPI documents through the root `openapi` field
-   Detecting JSON Schema documents through detecting keywords or otherwise successfully parsing the document in accordance with the JSON Schema specification

Additional mechanisms can be used to support documents with Objects other than an OpenAPI Object or a Schema Object at the root, but note that the resulting behavior is implementation-defined:

-   Detecting a document containing a referenceable Object at its root based on the expected type of the reference
-   Allowing users to configure the type of documents that might be loaded due to a reference to a non-root Object

### G.1 Warnings Regarding Fragmentary Parsing

[](https://spec.openapis.org/oas/latest.html#warnings-regarding-fragmentary-parsing)

Implementations that parse referenced fragments of OpenAPI content without regard for the content of the rest of the containing document will miss keywords that change the meaning and behavior of the reference target. In particular, failing to take into account keywords that change the base URI introduces security risks by causing references to resolve to unintended URIs, with unpredictable results. While some implementations support this sort of parsing due to the requirements of past versions of this specification, in version 3.1 and later, the result of parsing fragments in isolation is *undefined* and likely to contradict the requirements of this specification.

While it is possible to structure certain OpenAPI Descriptions to ensure that they will behave correctly when references are parsed as isolated fragments, depending on this is *NOT RECOMMENDED*. This specification does not explicitly enumerate the conditions under which such behavior is safe and provides no guarantee for continued safety in any future versions of the OAS.

### G.2 Conflicts Between Field Types and Reference Contexts

[](https://spec.openapis.org/oas/latest.html#conflicts-between-field-types-and-reference-contexts)

JSON or YAML objects within an OAD are interpreted as specific Objects (such as [Operation Objects](https://spec.openapis.org/oas/latest.html#operation-object), [Response Objects](https://spec.openapis.org/oas/latest.html#response-object), [Reference Objects](https://spec.openapis.org/oas/latest.html#reference-object), etc.) based on their context. Depending on how references are arranged, a given JSON or YAML object can be interpreted in multiple different contexts:

-   As the root object of the [entry document](https://spec.openapis.org/oas/latest.html#openapi-description-structure), which is always interpreted as an OpenAPI Object
-   As the Object type implied by its parent Object’s field within the document
-   As a reference target, with the Object type matching the reference source’s context

If the same JSON/YAML object is parsed multiple times and the respective contexts require it to be parsed as *different* Object types, the resulting behavior is *implementation defined*, and *MAY* be treated as an error if detected. An example would be referencing an empty Schema Object under `#/components/schemas` where a Path Item Object is expected, as an empty object is valid for both types. For maximum interoperability, it is *RECOMMENDED* that OpenAPI Description authors avoid such scenarios.

### G.3 Guidance Regarding Implicit Connections

[](https://spec.openapis.org/oas/latest.html#guidance-regarding-implicit-connections)

The following Objects and Fields involve the use of implicit connections:

| Source | Target | Alternative |
| --- | --- | --- |
| [Security Requirement Object](https://spec.openapis.org/oas/latest.html#security-requirement-object) `{name}` | [Security Scheme Object](https://spec.openapis.org/oas/latest.html#security-scheme-object) name under the [Components Object](https://spec.openapis.org/oas/latest.html#components-object) | *n/a* |
| [Discriminator Object](https://spec.openapis.org/oas/latest.html#discriminator-object) `mapping` *(implicit, or explicit name syntax)* | [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) name under the Components Object | `mapping` *(explicit URI syntax)* |
| [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) `tags` | [Tag Object](https://spec.openapis.org/oas/latest.html#tag-object) `name` (in the [OpenAPI Object](https://spec.openapis.org/oas/latest.html#openapi-object)’s `tags` array) | *n/a* |
| [Link Object](https://spec.openapis.org/oas/latest.html#link-object) `operationId` | [Operation Object](https://spec.openapis.org/oas/latest.html#operation-object) `operationId` | `operationRef` |

An additional implicit connection involves appending the templated URL paths of the [Paths Object](https://spec.openapis.org/oas/latest.html#paths-object) to the appropriate [Server Object](https://spec.openapis.org/oas/latest.html#server-object)’s `url` field. This connection is unambiguous because only the entry document’s Paths Object contributes URLs to the described API.

The implicit connections in the Security Requirement Object and Discriminator Object rely on the *component name*, which is the name of the property holding the component in the appropriately typed sub-object of the Components Object. For example, the component name of the Schema Object at `#/components/schemas/Foo` is `Foo`. The implicit connection of `tags` in the Operation Object uses the `name` field of Tag Objects, which (like the Components Object) are found under the root OpenAPI Object. This means resolving component names and tag names both depend on starting from the correct OpenAPI Object.

For resolving component and tag name connections from a referenced (non-entry) document, it is *RECOMMENDED* that tools resolve from the entry document, rather than the current document. Resolving component and tag name connections from a referenced (non-entry) document to the entry document as recommended under [Resolving Implicit Connections](https://spec.openapis.org/oas/latest.html#resolving-implicit-connections) allows components and Tag Objects to be defined next to the API’s deployment information in the top-level array of Server Objects and treated as an interface for referenced documents to access.

For Security Requirement Objects and Discriminator Objects, it is also possible to keep the resolution within the referenced document by using the URI-reference form that these Objects offer.

There are no URI-based alternatives for the Operation Object’s `tags` field. OAD authors are advised to use external solutions such as the OpenAPI Initiative’s Overlay Specification to simulate sharing [Tag Objects](https://spec.openapis.org/oas/latest.html#tag-object) across multiple documents.

#### G.3.1 Implicit Connection Resolution Examples

[](https://spec.openapis.org/oas/latest.html#implicit-connection-resolution-examples)

This section shows how to retrieve an HTTP-accessible multi-document OpenAPI Description (OAD) and resolve a [Security Requirement Object](https://spec.openapis.org/oas/latest.html#security-requirement-object) in the referenced (non-entry) document. The behavior for Discriminator Object non-URI mappings and for the Operation Object’s `tags` field operate on the same principles.

First, the [entry document](https://spec.openapis.org/oas/latest.html#openapi-description-structure) is where parsing begins. It defines the `MySecurity` security scheme to be JWT-based, and it defines a Path Item as a reference to a component in another document:

```
GET /api/description/openapi HTTP/1.1
Host: www.example.com
Accept: application/openapi+json
```

```
"components": {
  "securitySchemes": {
    "MySecurity": {
      "type": "http",
      "scheme": "bearer",
      "bearerFormat": "JWT"
    }
  }
},
"paths": {
  "/foo": {
    "$ref": "other#/components/pathItems/Foo"
  }
}
```

```
GET /api/description/openapi HTTP/1.1
Host: www.example.com
Accept: application/openapi+yaml
```

```
components:
  securitySchemes:
    MySecurity:
      type: http
      scheme: bearer
      bearerFormat: JWT
paths:
  /foo:
    $ref: 'other#/components/pathItems/Foo'
```

This entry document references another document, `other`, without using a file extension. This gives the client the flexibility to choose an acceptable format on a resource-by-resource basis, assuming both representations are available:

```
GET /api/description/other HTTP/1.1
Host: www.example.com
Accept: application/openapi+json
```

```
"components": {
  "securitySchemes": {
    "MySecurity": {
      "type": "http",
      "scheme": "basic"
    }
  },
  "pathItems": {
    "Foo": {
      "get": {
        "security": [
          "MySecurity": []
        ]
      }
    }
  }
}
```

```
GET /api/description/other HTTP/1.1
Host: www.example.com
Accept: application/openapi+yaml
```

```
components:
  securitySchemes:
    MySecurity:
      type: http
      scheme: basic
  pathItems:
    Foo:
      get:
        security:
          - MySecurity: []
```

In the `other` document, the referenced path item has a Security Requirement for a Security Scheme, `MySecurity`. The same Security Scheme exists in the original entry document. As outlined in [Resolving Implicit Connections](https://spec.openapis.org/oas/latest.html#resolving-implicit-connections), `MySecurity` is resolved with an [implementation-defined behavior](https://spec.openapis.org/oas/latest.html#undefined-and-implementation-defined-behavior), but the section formally recommends that tools resolve component names from the [entry document](https://spec.openapis.org/oas/latest.html#openapi-description-structure). As with all implementation-defined behavior, it is important to check tool documentation to determine which behavior is supported.

## H. References

[](https://spec.openapis.org/oas/latest.html#references)

### H.1 Normative references

[](https://spec.openapis.org/oas/latest.html#normative-references)

\[ABNF\]

[Augmented BNF for Syntax Specifications: ABNF](https://www.rfc-editor.org/rfc/rfc5234). D. Crocker, Ed.; P. Overell. IETF. January 2008. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc5234](https://www.rfc-editor.org/rfc/rfc5234)

\[CommonMark\]

[CommonMark Spec](https://spec.commonmark.org/). URL: [https://spec.commonmark.org/](https://spec.commonmark.org/)

\[CommonMark-0.27\]

[CommonMark Spec, Version 0.27](https://spec.commonmark.org/0.27/). John MacFarlane. 18 November 2016. URL: [https://spec.commonmark.org/0.27/](https://spec.commonmark.org/0.27/)

\[DOM\]

[DOM Standard](https://dom.spec.whatwg.org/). Anne van Kesteren. WHATWG. Living Standard. URL: [https://dom.spec.whatwg.org/](https://dom.spec.whatwg.org/)

\[IANA-HTTP-AUTHSCHEMES\]

[Hypertext Transfer Protocol (HTTP) Authentication Scheme Registry](https://www.iana.org/assignments/http-authschemes/). IANA. URL: [https://www.iana.org/assignments/http-authschemes/](https://www.iana.org/assignments/http-authschemes/)

\[IANA-HTTP-STATUS-CODES\]

[Hypertext Transfer Protocol (HTTP) Status Code Registry](https://www.iana.org/assignments/http-status-codes/). IANA. URL: [https://www.iana.org/assignments/http-status-codes/](https://www.iana.org/assignments/http-status-codes/)

\[OpenAPI-Registry\]

[OpenAPI Initiative Registry](https://spec.openapis.org/registry/index.html). OpenAPI Initiative. URL: [https://spec.openapis.org/registry/index.html](https://spec.openapis.org/registry/index.html)

\[OpenID-Connect-Core\]

[OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html). N. Sakimura; J. Bradley; M. Jones; B. de Medeiros; C. Mortimore. OpenID Foundation. 15 December 2023. Final. URL: [https://openid.net/specs/openid-connect-core-1\_0.html](https://openid.net/specs/openid-connect-core-1_0.html)

\[OpenID-Connect-Discovery\]

[OpenID Connect Discovery 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-discovery-1_0.html). N. Sakimura; J. Bradley; M. Jones; E. Jay. OpenID Foundation. 15 December 2023. Final. URL: [https://openid.net/specs/openid-connect-discovery-1\_0.html](https://openid.net/specs/openid-connect-discovery-1_0.html)

\[RFC2046\]

[Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types](https://www.rfc-editor.org/rfc/rfc2046). N. Freed; N. Borenstein. IETF. November 1996. Draft Standard. URL: [https://www.rfc-editor.org/rfc/rfc2046](https://www.rfc-editor.org/rfc/rfc2046)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC3986\]

[Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986). T. Berners-Lee; R. Fielding; L. Masinter. IETF. January 2005. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc3986](https://www.rfc-editor.org/rfc/rfc3986)

\[RFC3987\]

[Internationalized Resource Identifiers (IRIs)](https://www.rfc-editor.org/rfc/rfc3987). M. Duerst; M. Suignard. IETF. January 2005. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc3987](https://www.rfc-editor.org/rfc/rfc3987)

\[RFC4648\]

[The Base16, Base32, and Base64 Data Encodings](https://www.rfc-editor.org/rfc/rfc4648). S. Josefsson. IETF. October 2006. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc4648](https://www.rfc-editor.org/rfc/rfc4648)

\[RFC6265\]

[HTTP State Management Mechanism](https://httpwg.org/specs/rfc6265.html). A. Barth. IETF. April 2011. Proposed Standard. URL: [https://httpwg.org/specs/rfc6265.html](https://httpwg.org/specs/rfc6265.html)

\[RFC6570\]

[URI Template](https://www.rfc-editor.org/rfc/rfc6570). J. Gregorio; R. Fielding; M. Hadley; M. Nottingham; D. Orchard. IETF. March 2012. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc6570](https://www.rfc-editor.org/rfc/rfc6570)

\[RFC6749\]

[The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749). D. Hardt, Ed. IETF. October 2012. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc6749](https://www.rfc-editor.org/rfc/rfc6749)

\[RFC6901\]

[JavaScript Object Notation (JSON) Pointer](https://www.rfc-editor.org/rfc/rfc6901). P. Bryan, Ed.; K. Zyp; M. Nottingham, Ed. IETF. April 2013. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc6901](https://www.rfc-editor.org/rfc/rfc6901)

\[RFC7578\]

[Returning Values from Forms: multipart/form-data](https://www.rfc-editor.org/rfc/rfc7578). L. Masinter. IETF. July 2015. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7578](https://www.rfc-editor.org/rfc/rfc7578)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[RFC8259\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259). T. Bray, Ed. IETF. December 2017. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc8259](https://www.rfc-editor.org/rfc/rfc8259)

\[RFC8414\]

[OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414). M. Jones; N. Sakimura; J. Bradley. IETF. June 2018. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc8414](https://www.rfc-editor.org/rfc/rfc8414)

\[RFC8628\]

[OAuth 2.0 Device Authorization Grant](https://www.rfc-editor.org/rfc/rfc8628). W. Denniss; J. Bradley; M. Jones; H. Tschofenig. IETF. August 2019. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc8628](https://www.rfc-editor.org/rfc/rfc8628)

\[RFC9110\]

[HTTP Semantics](https://httpwg.org/specs/rfc9110.html). R. Fielding, Ed.; M. Nottingham, Ed.; J. Reschke, Ed. IETF. June 2022. Internet Standard. URL: [https://httpwg.org/specs/rfc9110.html](https://httpwg.org/specs/rfc9110.html)

\[RFC9264\]

[Linkset: Media Types and a Link Relation Type for Link Sets](https://www.rfc-editor.org/rfc/rfc9264). E. Wilde; H. Van de Sompel. IETF. July 2022. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc9264](https://www.rfc-editor.org/rfc/rfc9264)

\[RFC9512\]

[YAML Media Type](https://www.rfc-editor.org/rfc/rfc9512). R. Polli; E. Wilde; E. Aro. IETF. February 2024. Informational. URL: [https://www.rfc-editor.org/rfc/rfc9512](https://www.rfc-editor.org/rfc/rfc9512)

\[SNIFF\]

[MIME Sniffing Standard](https://mimesniff.spec.whatwg.org/). Gordon P. Hemsley. WHATWG. Living Standard. URL: [https://mimesniff.spec.whatwg.org/](https://mimesniff.spec.whatwg.org/)

\[SPDX-Licenses\]

[SPDX License List](https://spdx.org/licenses/). Linux Foundation. URL: [https://spdx.org/licenses/](https://spdx.org/licenses/)

\[WHATWG-URL\]

[URL Standard](https://url.spec.whatwg.org/). Anne van Kesteren. WHATWG. Living Standard. URL: [https://url.spec.whatwg.org/](https://url.spec.whatwg.org/)

\[xml-names11\]

[Namespaces in XML 1.1 (Second Edition)](https://www.w3.org/TR/xml-names11/). Tim Bray; Dave Hollander; Andrew Layman; Richard Tobin et al. W3C. 16 August 2006. W3C Recommendation. URL: [https://www.w3.org/TR/xml-names11/](https://www.w3.org/TR/xml-names11/)

\[YAML\]

[YAML Ain’t Markup Language (YAML™) Version 1.2](http://yaml.org/spec/1.2/spec.html). Oren Ben-Kiki; Clark Evans; Ingy döt Net. 1 October 2009. URL: [http://yaml.org/spec/1.2/spec.html](http://yaml.org/spec/1.2/spec.html)

### H.2 Informative references

[](https://spec.openapis.org/oas/latest.html#informative-references)

\[HTML\]

[HTML Standard](https://html.spec.whatwg.org/multipage/). Anne van Kesteren; Domenic Denicola; Dominic Farolino; Ian Hickson; Philip Jägenstedt; Simon Pieters. WHATWG. Living Standard. URL: [https://html.spec.whatwg.org/multipage/](https://html.spec.whatwg.org/multipage/)

\[HTML401\]

[HTML 4.01 Specification](https://www.w3.org/TR/html401/). Dave Raggett; Arnaud Le Hors; Ian Jacobs. W3C. 27 March 2018. W3C Recommendation. URL: [https://www.w3.org/TR/html401/](https://www.w3.org/TR/html401/)

\[OpenAPI-Learn\]

[OpenAPI - Getting started, and the specification explained](https://learn.openapis.org/). OpenAPI Initiative. URL: [https://learn.openapis.org/](https://learn.openapis.org/)

\[RFC1738\]

[Uniform Resource Locators (URL)](https://www.rfc-editor.org/rfc/rfc1738). T. Berners-Lee; L. Masinter; M. McCahill. IETF. December 1994. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc1738](https://www.rfc-editor.org/rfc/rfc1738)

\[RFC1866\]

[Hypertext Markup Language - 2.0](https://www.rfc-editor.org/rfc/rfc1866). T. Berners-Lee; D. Connolly. IETF. November 1995. Historic. URL: [https://www.rfc-editor.org/rfc/rfc1866](https://www.rfc-editor.org/rfc/rfc1866)

\[RFC2396\]

[Uniform Resource Identifiers (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc2396). T. Berners-Lee; R. Fielding; L. Masinter. IETF. August 1998. Draft Standard. URL: [https://www.rfc-editor.org/rfc/rfc2396](https://www.rfc-editor.org/rfc/rfc2396)

\[RFC2557\]

[MIME Encapsulation of Aggregate Documents, such as HTML (MHTML)](https://www.rfc-editor.org/rfc/rfc2557). J. Palme; A. Hopmann; N. Shelness. IETF. March 1999. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc2557](https://www.rfc-editor.org/rfc/rfc2557)

\[RFC6838\]

[Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838). N. Freed; J. Klensin; T. Hansen. IETF. January 2013. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc6838](https://www.rfc-editor.org/rfc/rfc6838)

\[RFC7464\]

[JavaScript Object Notation (JSON) Text Sequences](https://www.rfc-editor.org/rfc/rfc7464). N. Williams. IETF. February 2015. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7464](https://www.rfc-editor.org/rfc/rfc7464)

\[RFC8091\]

[A Media Type Structured Syntax Suffix for JSON Text Sequences](https://www.rfc-editor.org/rfc/rfc8091). E. Wilde. IETF. February 2017. Informational. URL: [https://www.rfc-editor.org/rfc/rfc8091](https://www.rfc-editor.org/rfc/rfc8091)

\[RFC9535\]

[JSONPath: Query Expressions for JSON](https://www.rfc-editor.org/rfc/rfc9535). S. Gössner, Ed.; G. Normington, Ed.; C. Bormann, Ed. IETF. February 2024. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc9535](https://www.rfc-editor.org/rfc/rfc9535)

[↑](https://spec.openapis.org/oas/latest.html#title)
