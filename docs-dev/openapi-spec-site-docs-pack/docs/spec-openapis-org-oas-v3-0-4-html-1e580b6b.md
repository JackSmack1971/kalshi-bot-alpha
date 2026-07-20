---
title: "OpenAPI Specification v3.0.4"
source_url: "https://spec.openapis.org/oas/v3.0.4.html"
host: "spec.openapis.org"
depth: 1
selector: "body"
fetched_at: "2026-07-17T17:36:57.450Z"
---
[![OpenAPI Initiative](https://raw.githubusercontent.com/OAI/OpenAPI-Style-Guide/master/graphics/bitmap/OpenAPI_Logo_Pantone.png)](https://openapis.org/)

# OpenAPI Specification v3.0.4

## Version 3.0.4

24 October 2024

More details about this document

This version:

[https://spec.openapis.org/oas/v3.0.4.html](https://spec.openapis.org/oas/v3.0.4.html)

Latest published version:

[https://spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)

Latest editor's draft:

[https://github.com/OAI/OpenAPI-Specification/](https://github.com/OAI/OpenAPI-Specification/)

Editors:

Darrel Miller

Henry Andrews

Jeremy Whitlock

Lorna Mitchell

Marsh Gardiner

Miguel Quintero

Mike Kistler

Ralf Handl

Ron Ratovsky

Former editors:

Mike Ralphson

Uri Sarid

Jason Harmon

Tony Tam

Other versions:

[https://spec.openapis.org/oas/v3.2.0.html](https://spec.openapis.org/oas/v3.2.0.html)

[https://spec.openapis.org/oas/v3.1.2.html](https://spec.openapis.org/oas/v3.1.2.html)

[https://spec.openapis.org/oas/v3.1.1.html](https://spec.openapis.org/oas/v3.1.1.html)

[https://spec.openapis.org/oas/v3.1.0.html](https://spec.openapis.org/oas/v3.1.0.html)

[https://spec.openapis.org/oas/v3.0.3.html](https://spec.openapis.org/oas/v3.0.3.html)

[https://spec.openapis.org/oas/v3.0.2.html](https://spec.openapis.org/oas/v3.0.2.html)

[https://spec.openapis.org/oas/v3.0.1.html](https://spec.openapis.org/oas/v3.0.1.html)

[https://spec.openapis.org/oas/v3.0.0.html](https://spec.openapis.org/oas/v3.0.0.html)

[https://spec.openapis.org/oas/v2.0.html](https://spec.openapis.org/oas/v2.0.html)

Participate

[GitHub OAI/OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/)

[File a bug](https://github.com/OAI/OpenAPI-Specification/issues)

[Commit history](https://github.com/OAI/OpenAPI-Specification/commits/main/versions/3.0.4.md)

[Pull requests](https://github.com/OAI/OpenAPI-Specification/pulls)

Copyright © 2024 the Linux Foundation

* * *

## What is the OpenAPI Specification?

The OpenAPI Specification (OAS) defines a standard, programming language-agnostic interface description for HTTP APIs, which allows both humans and computers to discover and understand the capabilities of a service without requiring access to source code, additional documentation, or inspection of network traffic. When properly defined via OpenAPI, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. Similar to what interface descriptions have done for lower-level programming, the OpenAPI Specification removes guesswork in calling a service.

## Status of This Document

The source-of-truth for this specification is the HTML file referenced above as *This version*.

## 1\. OpenAPI Specification

[](https://spec.openapis.org/oas/v3.0.4.html#openapi-specification)

### 1.1 Version 3.0.4

[](https://spec.openapis.org/oas/v3.0.4.html#conformance)

The key words “*MUST*”, “*MUST NOT*”, “*REQUIRED*”, “*SHALL*”, “*SHALL NOT*”, “*SHOULD*”, “*SHOULD NOT*”, “*RECOMMENDED*”, “*NOT RECOMMENDED*”, “*MAY*”, and “*OPTIONAL*” in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14) \[[RFC2119](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

This document is licensed under [The Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

## 2\. Introduction

[](https://spec.openapis.org/oas/v3.0.4.html#introduction)

The OpenAPI Specification (OAS) defines a standard, language-agnostic interface to HTTP APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. When properly defined, a consumer can understand and interact with the remote service with a minimal amount of implementation logic.

An OpenAPI Description can then be used by documentation generation tools to display the API, code generation tools to generate servers and clients in various programming languages, testing tools, and many other use cases.

For examples of OpenAPI usage and additional documentation, please visit \[[OpenAPI-Learn](https://spec.openapis.org/oas/v3.0.4.html#bib-openapi-learn "OpenAPI - Getting started, and the specification explained")\].

For extension registries and other specifications published by the OpenAPI Initiative, as well as the authoritative rendering of this specification, please visit [spec.openapis.org](https://spec.openapis.org/).

## 3\. Definitions

[](https://spec.openapis.org/oas/v3.0.4.html#definitions)

### 3.1 OpenAPI Description

[](https://spec.openapis.org/oas/v3.0.4.html#openapi-description)

An OpenAPI Description (OAD) formally describes the surface of an API and its semantics. It is composed of an [entry document](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-structure), which must be an OpenAPI Document, and any/all of its referenced documents. An OAD uses and conforms to the OpenAPI Specification.

### 3.2 OpenAPI Document

[](https://spec.openapis.org/oas/v3.0.4.html#openapi-document)

An OpenAPI Document is a single JSON or YAML document that conforms to the OpenAPI Specification. An OpenAPI Document compatible with OAS 3.\*.\* contains a required [`openapi`](https://spec.openapis.org/oas/v3.0.4.html#oas-version) field which designates the version of the OAS that it uses.

### 3.3 Schema

[](https://spec.openapis.org/oas/v3.0.4.html#schema)

A “schema” is a formal description of syntax and structure. This document serves as the [schema](https://spec.openapis.org/oas/v3.0.4.html#schema) for the OpenAPI Specification format; a non-authoritative JSON Schema based on this document is also provided on [spec.openapis.org](https://spec.openapis.org/) for informational purposes. This specification also *uses* schemas in the form of the [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object).

### 3.4 Object

[](https://spec.openapis.org/oas/v3.0.4.html#object)

When capitalized, the word “Object” refers to any of the Objects that are named by section headings in this document.

### 3.5 Path Templating

[](https://spec.openapis.org/oas/v3.0.4.html#path-templating)

Path templating refers to the usage of template expressions, delimited by curly braces (`{}`), to mark a section of a URL path as replaceable using path parameters.

Each template expression in the path *MUST* correspond to a path parameter that is included in the [Path Item](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) itself and/or in each of the Path Item’s [Operations](https://spec.openapis.org/oas/v3.0.4.html#operation-object).

### 3.6 Media Types

[](https://spec.openapis.org/oas/v3.0.4.html#media-types)

Media type definitions are spread across several resources. The media type definitions *SHOULD* be in compliance with \[[RFC6838](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6838 "Media Type Specifications and Registration Procedures")\].

Some examples of possible media type definitions:

```
  text/plain; charset=utf-8
  application/json
  application/vnd.github+json
  application/vnd.github.v3+json
  application/vnd.github.v3.raw+json
  application/vnd.github.v3.text+json
  application/vnd.github.v3.html+json
  application/vnd.github.v3.full+json
  application/vnd.github.v3.diff
  application/vnd.github.v3.patch
```

### 3.7 HTTP Status Codes

[](https://spec.openapis.org/oas/v3.0.4.html#http-status-codes)

The HTTP Status Codes are used to indicate the status of the executed operation. Status codes *SHOULD* be selected from the available status codes registered in the [IANA Status Code Registry](https://spec.openapis.org/oas/v3.0.4.html#bib-iana-http-status-codes "Hypertext Transfer Protocol (HTTP) Status Code Registry").

### 3.8 Case Sensitivity

[](https://spec.openapis.org/oas/v3.0.4.html#case-sensitivity)

As most field names and values in the OpenAPI Specification are case-sensitive, this document endeavors to call out any case-insensitive names and values. However, the case sensitivity of field names and values that map directly to HTTP concepts follow the case sensitivity rules of HTTP, even if this document does not make a note of every concept.

### 3.9 Undefined and Implementation-Defined Behavior

[](https://spec.openapis.org/oas/v3.0.4.html#undefined-and-implementation-defined-behavior)

This specification deems certain situations to have either *undefined* or *implementation-defined* behavior.

Behavior described as *undefined* is likely, at least in some circumstances, to result in outcomes that contradict the specification. This description is used when detecting the contradiction is impossible or impractical. Implementations *MAY* support undefined scenarios for historical reasons, including ambiguous text in prior versions of the specification. This support might produce correct outcomes in many cases, but relying on it is *NOT RECOMMENDED* as there is no guarantee that it will work across all tools or with future specification versions, even if those versions are otherwise strictly compatible with this one.

Behavior described as *implementation-defined* allows implementations to choose which of several different-but-compliant approaches to a requirement to implement. This documents ambiguous requirements that API description authors are *RECOMMENDED* to avoid in order to maximize interoperability. Unlike undefined behavior, it is safe to rely on implementation-defined behavior if *and only if* it can be guaranteed that all relevant tools support the same behavior.

## 4\. Specification

[](https://spec.openapis.org/oas/v3.0.4.html#specification)

### 4.1 Versions

[](https://spec.openapis.org/oas/v3.0.4.html#versions)

The OpenAPI Specification is versioned using a `major`.`minor`.`patch` versioning scheme. The `major`.`minor` portion of the version string (for example `3.1`) *SHALL* designate the OAS feature set. *`.patch`* versions address errors in, or provide clarifications to, this document, not the feature set. Tooling which supports OAS 3.1 *SHOULD* be compatible with all OAS 3.1.\* versions. The patch version *SHOULD NOT* be considered by tooling, making no distinction between `3.1.0` and `3.1.1` for example.

Occasionally, non-backwards compatible changes may be made in `minor` versions of the OAS where impact is believed to be low relative to the benefit provided.

### 4.2 Format

[](https://spec.openapis.org/oas/v3.0.4.html#format)

An OpenAPI Document that conforms to the OpenAPI Specification is itself a JSON object, which may be represented either in [JSON](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7159 "The JavaScript Object Notation (JSON) Data Interchange Format") or [YAML](https://spec.openapis.org/oas/v3.0.4.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2") format.

For example, if a field has an array value, the JSON array representation will be used:

```
{
  "field": [1, 2, 3]
}
```

All field names in the specification are **case sensitive**. This includes all fields that are used as keys in a map, except where explicitly noted that keys are **case insensitive**.

The [schema](https://spec.openapis.org/oas/v3.0.4.html#schema) exposes two types of fields: *fixed fields*, which have a declared name, and *patterned fields*, which have a declared pattern for the field name.

Patterned fields *MUST* have unique names within the containing object.

In order to preserve the ability to round-trip between YAML and JSON formats, [YAML version 1.2](https://spec.openapis.org/oas/v3.0.4.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2") is *RECOMMENDED* along with some additional constraints:

-   Tags *MUST* be limited to those allowed by [YAML’s JSON schema ruleset](https://yaml.org/spec/1.2/spec.html#id2803231), which defines a subset of the YAML syntax and is unrelated to [JSON Schema](https://spec.openapis.org/oas/v3.0.4.html#bib-json-schema-05 "JSON Schema: A Media Type for Describing JSON Documents. Draft 5").
-   Keys used in YAML maps *MUST* be limited to a scalar string, as defined by the [YAML Failsafe schema ruleset](https://yaml.org/spec/1.2/spec.html#id2802346).

**Note:** While APIs may be described by OpenAPI Descriptions in either YAML or JSON format, the API request and response bodies and other content are not required to be JSON or YAML.

### 4.3 OpenAPI Description Structure

[](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-structure)

An OpenAPI Description (OAD) *MAY* be made up of a single JSON or YAML document or be divided into multiple, connected parts at the discretion of the author. In the latter case, [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) and [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) `$ref` fields, as well as the [Link Object](https://spec.openapis.org/oas/v3.0.4.html#link-object) `operationRef` field, and the URI form of the [Discriminator Object](https://spec.openapis.org/oas/v3.0.4.html#discriminator-object) `mapping` field, are used to identify the referenced elements.

In a multi-document OAD, the document containing the OpenAPI Object where parsing begins is known as that OAD’s **entry document**.

It is *RECOMMENDED* that the entry document of an OAD be named: `openapi.json` or `openapi.yaml`.

#### 4.3.1 Structural Interoperability

[](https://spec.openapis.org/oas/v3.0.4.html#structural-interoperability)

JSON or YAML objects within an OAD are interpreted as specific Objects (such as [Operation Objects](https://spec.openapis.org/oas/v3.0.4.html#operation-object), [Response Objects](https://spec.openapis.org/oas/v3.0.4.html#response-object), [Reference Objects](https://spec.openapis.org/oas/v3.0.4.html#reference-object), etc.) based on their context. Depending on how references are arranged, a given JSON or YAML object can be interpreted in multiple different contexts:

-   As the root object of the [entry document](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-structure), which is always interpreted as an OpenAPI Object
-   As the Object type implied by its parent Object within the document
-   As a reference target, with the Object type matching the reference source’s context

If the same JSON/YAML object is parsed multiple times and the respective contexts require it to be parsed as *different* Object types, the resulting behavior is *implementation defined*, and *MAY* be treated as an error if detected. An example would be referencing an empty Schema Object under `#/components/schemas` where a Path Item Object is expected, as an empty object is valid for both types. For maximum interoperability, it is *RECOMMENDED* that OpenAPI Description authors avoid such scenarios.

#### 4.3.2 Resolving Implicit Connections

[](https://spec.openapis.org/oas/v3.0.4.html#resolving-implicit-connections)

Several features of this specification require resolution of non-URI-based connections to some other part of the OpenAPI Description (OAD).

These connections are unambiguously resolved in single-document OADs, but the resolution process in multi-document OADs is *implementation-defined*, within the constraints described in this section. In some cases, an unambiguous URI-based alternative is available, and OAD authors are *RECOMMENDED* to always use the alternative:

| Source | Target | Alternative |
| --- | --- | --- |
| [Security Requirement Object](https://spec.openapis.org/oas/v3.0.4.html#security-requirement-object) `{name}` | [Security Scheme Object](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object) name under the [Components Object](https://spec.openapis.org/oas/v3.0.4.html#components-object) | *n/a* |
| [Discriminator Object](https://spec.openapis.org/oas/v3.0.4.html#discriminator-object) `mapping` *(implicit, or explicit name syntax)* | [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) name under the Components Object | `mapping` *(explicit URI syntax)* |
| [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) `tags` | [Tag Object](https://spec.openapis.org/oas/v3.0.4.html#tag-object) `name` (in the [OpenAPI Object](https://spec.openapis.org/oas/v3.0.4.html#openapi-object)’s `tags` array) | *n/a* |
| [Link Object](https://spec.openapis.org/oas/v3.0.4.html#link-object) `operationId` | [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) `operationId` | `operationRef` |

A fifth implicit connection involves appending the templated URL paths of the [Paths Object](https://spec.openapis.org/oas/v3.0.4.html#paths-object) to the appropriate [Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object)’s `url` field. This is unambiguous because only the entry document’s Paths Object contributes URLs to the described API.

It is *RECOMMENDED* to consider all Operation Objects from all parsed documents when resolving any Link Object `operationId`. This requires parsing all referenced documents prior to determining an `operationId` to be unresolvable.

The implicit connections in the Security Requirement Object and Discriminator Object rely on the *component name*, which is the name of the property holding the component in the appropriately typed sub-object of the Components Object. For example, the component name of the Schema Object at `#/components/schemas/Foo` is `Foo`. The implicit connection of `tags` in the Operation Object uses the `name` field of Tag Objects, which (like the Components Object) are found under the root OpenAPI Object. This means resolving component names and tag names both depend on starting from the correct OpenAPI Object.

For resolving component and tag name connections from a referenced (non-entry) document, it is *RECOMMENDED* that tools resolve from the entry document, rather than the current document. This allows Security Scheme Objects and Tag Objects to be defined next to the API’s deployment information (the top-level array of Server Objects), and treated as an interface for referenced documents to access.

The interface approach can also work for Discriminator Objects and Schema Objects, but it is also possible to keep the Discriminator Object’s behavior within a single document using the relative URI-reference syntax of `mapping`.

There are no URI-based alternatives for the Security Requirement Object or for the Operation Object’s `tags` field. These limitations are expected to be addressed in a future release.

See [Appendix F: Resolving Security Requirements in a Referenced Document](https://spec.openapis.org/oas/v3.0.4.html#appendix-f-resolving-security-requirements-in-a-referenced-document) for an example of the possible resolutions, including which one is recommended by this section. The behavior for Discrimator Object non-URI mappings and for the Operation Object’s `tags` field operate on the same principles.

Note that no aspect of implicit connection resolution changes how [URLs are resolved](https://spec.openapis.org/oas/v3.0.4.html#relative-references-in-urls) or restricts their possible targets.

### 4.4 Data Types

[](https://spec.openapis.org/oas/v3.0.4.html#data-types)

Data types in the OAS are based on the non-`null` types supported by the [JSON Schema Validation Specification Draft Wright-00](https://tools.ietf.org/html/draft-wright-json-schema-validation-00#autoid-32): “boolean”, “object”, “array”, “number”, “string”, or “integer”. See [`nullable`](https://spec.openapis.org/oas/v3.0.4.html#schema-nullable) for an alternative solution to “null” as a type. Models are defined using the [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object), which is an extended subset of JSON Schema Specification Draft Wright-00.

JSON Schema keywords and `format` values operate on JSON “instances” which may be one of the six JSON data types, “null”, “boolean”, “object”, “array”, “number”, or “string”, with certain keywords and formats [only applying to a specific type](https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-4.1). For example, the `pattern` keyword and the `date-time` format only apply to strings, and treat any instance of the other five types as *automatically valid.* This means JSON Schema keywords and formats do **NOT** implicitly require the expected type. Use the `type` keyword to explicitly constrain the type.

Note that the `type` keyword allows `"integer"` as a value for convenience, but keyword and format applicability does not recognize integers as being of a distinct JSON type from other numbers because [JSON](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7159 "The JavaScript Object Notation (JSON) Data Interchange Format") itself does not make that distinction. Since there is no distinct JSON integer type, JSON Schema defines integers mathematically. This means that both `1` and `1.0` are [equivalent](https://tools.ietf.org/html/draft-bhutton-json-schema-00#section-4.2.2), and are both considered to be integers.

#### 4.4.1 Data Type Format

[](https://spec.openapis.org/oas/v3.0.4.html#data-type-format)

As defined by the [JSON Schema Validation specification](https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-7.3), data types can have an optional modifier keyword: `format`. As described in that specification, `format` is treated as a non-validating annotation by default; the ability to validate `format` varies across implementations.

The OpenAPI Initiative also hosts a [Format Registry](https://spec.openapis.org/registry/format/) for formats defined by OAS users and other specifications. Support for any registered format is strictly *OPTIONAL*, and support for one registered format does not imply support for any others.

Types that are not accompanied by a `format` keyword follow the type definition in the JSON Schema. Tools that do not recognize a specific `format` *MAY* default back to the `type` alone, as if the `format` is not specified. For the purpose of [JSON Schema validation](https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-7.1), each format should specify the set of JSON data types for which it applies. In this registry, these types are shown in the “JSON Data Type” column.

The formats defined by the OAS are:

| `format` | JSON Data Type | Comments |
| --- | --- | --- |
| `int32` | number | signed 32 bits |
| `int64` | number | signed 64 bits (a.k.a long) |
| `float` | number |  |
| `double` | number |  |
| `byte` | string | base64 encoded characters - \[[RFC4648](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc4648 "The Base16, Base32, and Base64 Data Encodings")\] [Section 4](https://datatracker.ietf.org/doc/html/rfc4648#section-4) |
| `binary` | string | any sequence of octets |
| `date` | string | As defined by `full-date` - \[[RFC3339](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3339 "Date and Time on the Internet: Timestamps")\] [Section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) |
| `date-time` | string | As defined by `date-time` - \[[RFC3339](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3339 "Date and Time on the Internet: Timestamps")\] [Section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) |
| `password` | string | A hint to obscure the value. |

#### 4.4.2 Working with Binary Data

[](https://spec.openapis.org/oas/v3.0.4.html#working-with-binary-data)

Two formats, `binary` and `byte`, describe different ways to work with binary data:

-   `binary` is used where unencoded binary data is allowed, such as when sending a binary payload as an HTTP message body, or as part of a `multipart/*` payload that allows binary parts
-   `byte` is used where binary data is embedded in a text-only format such as `application/json` or `application/x-www-form-urlencoded`

The `maxLength` keyword *MAY* be used to set an expected upper bound on the length of a streaming payload. The keyword can be applied to either string data, including encoded binary data, or to unencoded binary data. For unencoded binary, the length is the number of octets.

Note that the encoding indicated by `byte`, which inflates the size of data in order to represent it as 7-bit ASCII text, is unrelated to HTTP’s `Content-Encoding` header, which indicates whether and how a message body has been compressed.

### 4.5 Rich Text Formatting

[](https://spec.openapis.org/oas/v3.0.4.html#rich-text-formatting)

Throughout the specification `description` fields are noted as supporting \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] markdown formatting. Where OpenAPI tooling renders rich text it *MUST* support, at a minimum, markdown syntax as described by \[[CommonMark-0.27](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark-0.27 "CommonMark Spec, Version 0.27")\]. Tooling *MAY* choose to ignore some CommonMark or extension features to address security concerns.

While the framing of CommonMark 0.27 as a minimum requirement means that tooling *MAY* choose to implement extensions on top of it, note that any such extensions are by definition implementation-defined and will not be interoperable. OpenAPI Description authors *SHOULD* consider how text using such extensions will be rendered by tools that offer only the minimum support.

### 4.6 Relative References in URLs

[](https://spec.openapis.org/oas/v3.0.4.html#relative-references-in-urls)

Unless specified otherwise, all fields that are URLs *MAY* be relative references as defined by \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://datatracker.ietf.org/doc/html/rfc3986#section-4.2).

Relative references are resolved using the URLs defined in the [Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object) as a Base URI.

Relative references used in `$ref` are processed as per [JSON Reference](https://spec.openapis.org/oas/v3.0.4.html#bib-json-reference "JSON Reference"), using the URL of the current document as the base URI. See also the [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object).

It is *implementation\_defined* whether the resolution of relative references in each of the `operationRef` field of the [Link Object](https://spec.openapis.org/oas/v3.0.4.html#link-object), the URI form of the `mapping` field of the [Discriminator Object](https://spec.openapis.org/oas/v3.0.4.html#discriminator-object), the `externalValue` field of the [Example Object](https://spec.openapis.org/oas/v3.0.4.html#example-object), and the `url` fields of the [External Documentation](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object), [Contact](https://spec.openapis.org/oas/v3.0.4.html#contact-object), and [License](https://spec.openapis.org/oas/v3.0.4.html#license-object) Objects resolve by using the same process as `$ref` or by using the Server Object. For compatibility with future versions of this specification, the `$ref` process is *RECOMMENDED* for all of these fields.

Relative references in CommonMark hyperlinks are resolved in their rendered context, which might differ from the context of the API description.

### 4.7 Schema

[](https://spec.openapis.org/oas/v3.0.4.html#schema-0)

This section describes the structure of the OpenAPI Description format. This text is the only normative description of the format. A JSON Schema is hosted on [spec.openapis.org](https://spec.openapis.org/) for informational purposes. If the JSON Schema differs from this section, then this section *MUST* be considered authoritative.

In the following description, if a field is not explicitly ***REQUIRED*** or described with a *MUST* or *SHALL*, it can be considered *OPTIONAL*.

#### 4.7.1 OpenAPI Object

[](https://spec.openapis.org/oas/v3.0.4.html#openapi-object)

This is the root object of the [OpenAPI Description](https://spec.openapis.org/oas/v3.0.4.html#openapi-description).

##### 4.7.1.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields)

| Field Name | Type | Description |
| --- | --- | --- |
| openapi | `string` | ***REQUIRED***. This string *MUST* be the [version number](https://spec.openapis.org/oas/v3.0.4.html#versions) of the OpenAPI Specification that the OpenAPI Document uses. The `openapi` field *SHOULD* be used by tooling to interpret the OpenAPI Document. This is *not* related to the API [`info.version`](https://spec.openapis.org/oas/v3.0.4.html#info-version) string. |
| info | [Info Object](https://spec.openapis.org/oas/v3.0.4.html#info-object) | ***REQUIRED***. Provides metadata about the API. The metadata *MAY* be used by tooling as required. |
| servers | \[[Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object)\] | An array of Server Objects, which provide connectivity information to a target server. If the `servers` field is not provided, or is an empty array, the default value would be a [Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object) with a [url](https://spec.openapis.org/oas/v3.0.4.html#server-url) value of `/`. |
| paths | [Paths Object](https://spec.openapis.org/oas/v3.0.4.html#paths-object) | ***REQUIRED***. The available paths and operations for the API. |
| components | [Components Object](https://spec.openapis.org/oas/v3.0.4.html#components-object) | An element to hold various Objects for the OpenAPI Description. |
| security | \[[Security Requirement Object](https://spec.openapis.org/oas/v3.0.4.html#security-requirement-object)\] | A declaration of which security mechanisms can be used across the API. The list of values includes alternative Security Requirement Objects that can be used. Only one of the Security Requirement Objects need to be satisfied to authorize a request. Individual operations can override this definition. The list can be incomplete, up to being empty or absent. To make security explicitly optional, an empty security requirement (`{}`) can be included in the array. |
| tags | \[[Tag Object](https://spec.openapis.org/oas/v3.0.4.html#tag-object)\] | A list of tags used by the OpenAPI Description with additional metadata. The order of the tags can be used to reflect on their order by the parsing tools. Not all tags that are used by the [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) must be declared. The tags that are not declared *MAY* be organized randomly or based on the tools’ logic. Each tag name in the list *MUST* be unique. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object) | Additional external documentation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

#### 4.7.2 Info Object

[](https://spec.openapis.org/oas/v3.0.4.html#info-object)

The object provides metadata about the API. The metadata *MAY* be used by the clients if needed, and *MAY* be presented in editing or documentation generation tools for convenience.

##### 4.7.2.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-0)

| Field Name | Type | Description |
| --- | --- | --- |
| title | `string` | ***REQUIRED***. The title of the API. |
| description | `string` | A description of the API. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| termsOfService | `string` | A URL for the Terms of Service for the API. This *MUST* be in the form of a URL. |
| contact | [Contact Object](https://spec.openapis.org/oas/v3.0.4.html#contact-object) | The contact information for the exposed API. |
| license | [License Object](https://spec.openapis.org/oas/v3.0.4.html#license-object) | The license information for the exposed API. |
| version | `string` | ***REQUIRED***. The version of the OpenAPI Document (which is distinct from the [OpenAPI Specification version](https://spec.openapis.org/oas/v3.0.4.html#oas-version) or the version of the API being described or the version of the OpenAPI Description). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.2.2 Info Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#info-object-example)

```
{
  "title": "Example Pet Store App",
  "description": "This is an example server for a pet store.",
  "termsOfService": "https://example.com/terms/",
  "contact": {
    "name": "API Support",
    "url": "https://www.example.com/support",
    "email": "support@example.com"
  },
  "license": {
    "name": "Apache 2.0",
    "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
  },
  "version": "1.0.1"
}
```

```
title: Example Pet Store App
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

#### 4.7.3 Contact Object

[](https://spec.openapis.org/oas/v3.0.4.html#contact-object)

Contact information for the exposed API.

##### 4.7.3.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-1)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | The identifying name of the contact person/organization. |
| url | `string` | The URL for the contact information. This *MUST* be in the form of a URL. |
| email | `string` | The email address of the contact person/organization. This *MUST* be in the form of an email address. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.3.2 Contact Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#contact-object-example)

```
{
  "name": "API Support",
  "url": "https://www.example.com/support",
  "email": "support@example.com"
}
```

```
name: API Support
url: https://www.example.com/support
email: support@example.com
```

#### 4.7.4 License Object

[](https://spec.openapis.org/oas/v3.0.4.html#license-object)

License information for the exposed API.

##### 4.7.4.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-2)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The license name used for the API. |
| url | `string` | A URL for the license used for the API. This *MUST* be in the form of a URL. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.4.2 License Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#license-object-example)

```
{
  "name": "Apache 2.0",
  "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
}
```

```
name: Apache 2.0
url: https://www.apache.org/licenses/LICENSE-2.0.html
```

#### 4.7.5 Server Object

[](https://spec.openapis.org/oas/v3.0.4.html#server-object)

An object representing a Server.

##### 4.7.5.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-3)

| Field Name | Type | Description |
| --- | --- | --- |
| url | `string` | ***REQUIRED***. A URL to the target host. This URL supports Server Variables and *MAY* be relative, to indicate that the host location is relative to the location where the document containing the Server Object is being served. Variable substitutions will be made when a variable is named in `{`braces`}`. |
| description | `string` | An optional string describing the host designated by the URL. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| variables | Map\[`string`, [Server Variable Object](https://spec.openapis.org/oas/v3.0.4.html#server-variable-object)\] | A map between a variable name and its value. The value is used for substitution in the server’s URL template. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.5.2 Server Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#server-object-example)

A single server would be described as:

```
{
  "url": "https://development.gigantic-server.com/v1",
  "description": "Development server"
}
```

```
url: https://development.gigantic-server.com/v1
description: Development server
```

The following shows how multiple servers can be described, for example, at the OpenAPI Object’s [`servers`](https://spec.openapis.org/oas/v3.0.4.html#oas-servers):

```
{
  "servers": [
    {
      "url": "https://development.gigantic-server.com/v1",
      "description": "Development server"
    },
    {
      "url": "https://staging.gigantic-server.com/v1",
      "description": "Staging server"
    },
    {
      "url": "https://api.gigantic-server.com/v1",
      "description": "Production server"
    }
  ]
}
```

```
servers:
  - url: https://development.gigantic-server.com/v1
    description: Development server
  - url: https://staging.gigantic-server.com/v1
    description: Staging server
  - url: https://api.gigantic-server.com/v1
    description: Production server
```

The following shows how variables can be used for a server configuration:

```
{
  "servers": [
    {
      "url": "https://{username}.gigantic-server.com:{port}/{basePath}",
      "description": "The production API server",
      "variables": {
        "username": {
          "default": "demo",
          "description": "A user-specific subdomain. Use `demo` for a free sandbox environment."
        },
        "port": {
          "enum": ["8443", "443"],
          "default": "8443"
        },
        "basePath": {
          "default": "v2"
        }
      }
    }
  ]
}
```

```
servers:
  - url: https://{username}.gigantic-server.com:{port}/{basePath}
    description: The production API server
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
        # open meaning there is the opportunity to use special base paths as assigned by the provider, default is `v2`
        default: v2
```

#### 4.7.6 Server Variable Object

[](https://spec.openapis.org/oas/v3.0.4.html#server-variable-object)

An object representing a Server Variable for server URL template substitution.

##### 4.7.6.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-4)

| Field Name | Type | Description |
| --- | --- | --- |
| enum | \[`string`\] | An enumeration of string values to be used if the substitution options are from a limited set. The array *SHOULD NOT* be empty. |
| default | `string` | ***REQUIRED***. The default value to use for substitution, which *SHALL* be sent if an alternate value is *not* supplied. If the [`enum`](https://spec.openapis.org/oas/v3.0.4.html#server-variable-enum) is defined, the value *SHOULD* exist in the enum’s values. Note that this behavior is different from the [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object)’s `default` keyword, which documents the receiver’s behavior rather than inserting the value into the data. |
| description | `string` | An optional description for the server variable. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

#### 4.7.7 Components Object

[](https://spec.openapis.org/oas/v3.0.4.html#components-object)

Holds a set of reusable objects for different aspects of the OAS. All objects defined within the Components Object will have no effect on the API unless they are explicitly referenced from outside the Components Object.

##### 4.7.7.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-5)

| Field Name | Type | Description |
| --- | --- | --- |
| schemas | Map\[`string`, [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Schema Objects](https://spec.openapis.org/oas/v3.0.4.html#schema-object). |
| responses | Map\[`string`, [Response Object](https://spec.openapis.org/oas/v3.0.4.html#response-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Response Objects](https://spec.openapis.org/oas/v3.0.4.html#response-object). |
| parameters | Map\[`string`, [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Parameter Objects](https://spec.openapis.org/oas/v3.0.4.html#parameter-object). |
| examples | Map\[`string`, [Example Object](https://spec.openapis.org/oas/v3.0.4.html#example-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Example Objects](https://spec.openapis.org/oas/v3.0.4.html#example-object). |
| requestBodies | Map\[`string`, [Request Body Object](https://spec.openapis.org/oas/v3.0.4.html#request-body-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Request Body Objects](https://spec.openapis.org/oas/v3.0.4.html#request-body-object). |
| headers | Map\[`string`, [Header Object](https://spec.openapis.org/oas/v3.0.4.html#header-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Header Objects](https://spec.openapis.org/oas/v3.0.4.html#header-object). |
| securitySchemes | Map\[`string`, [Security Scheme Object](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Security Scheme Objects](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object). |
| links | Map\[`string`, [Link Object](https://spec.openapis.org/oas/v3.0.4.html#link-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Link Objects](https://spec.openapis.org/oas/v3.0.4.html#link-object). |
| callbacks | Map\[`string`, [Callback Object](https://spec.openapis.org/oas/v3.0.4.html#callback-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | An object to hold reusable [Callback Objects](https://spec.openapis.org/oas/v3.0.4.html#callback-object). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

All the fixed fields declared above are objects that *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`.

Field Name Examples:

```
User
User_1
User_Name
user-name
my.org.User
```

##### 4.7.7.2 Components Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#components-object-example)

```
"components": {
  "schemas": {
    "GeneralError": {
      "type": "object",
      "properties": {
        "code": {
          "type": "integer",
          "format": "int32"
        },
        "message": {
          "type": "string"
        }
      }
    },
    "Category": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "name": {
          "type": "string"
        }
      }
    },
    "Tag": {
      "type": "object",
      "properties": {
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "name": {
          "type": "string"
        }
      }
    }
  },
  "parameters": {
    "skipParam": {
      "name": "skip",
      "in": "query",
      "description": "number of items to skip",
      "required": true,
      "schema": {
        "type": "integer",
        "format": "int32"
      }
    },
    "limitParam": {
      "name": "limit",
      "in": "query",
      "description": "max records to return",
      "required": true,
      "schema" : {
        "type": "integer",
        "format": "int32"
      }
    }
  },
  "responses": {
    "NotFound": {
      "description": "Entity not found."
    },
    "IllegalInput": {
      "description": "Illegal input for operation."
    },
    "GeneralError": {
      "description": "General Error",
      "content": {
        "application/json": {
          "schema": {
            "$ref": "#/components/schemas/GeneralError"
          }
        }
      }
    }
  },
  "securitySchemes": {
    "api_key": {
      "type": "apiKey",
      "name": "api-key",
      "in": "header"
    },
    "petstore_auth": {
      "type": "oauth2",
      "flows": {
        "implicit": {
          "authorizationUrl": "https://example.org/api/oauth/dialog",
          "scopes": {
            "write:pets": "modify pets in your account",
            "read:pets": "read your pets"
          }
        }
      }
    }
  }
}
```

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

#### 4.7.8 Paths Object

[](https://spec.openapis.org/oas/v3.0.4.html#paths-object)

Holds the relative paths to the individual endpoints and their operations. The path is appended to the URL from the [Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object) in order to construct the full URL. The Paths Object *MAY* be empty, due to [Access Control List (ACL) constraints](https://spec.openapis.org/oas/v3.0.4.html#security-filtering).

##### 4.7.8.1 Patterned Fields

[](https://spec.openapis.org/oas/v3.0.4.html#patterned-fields)

| Field Pattern | Type | Description |
| --- | --- | --- |
| /{path} | [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) | A relative path to an individual endpoint. The field name *MUST* begin with a forward slash (`/`). The path is **appended** (no relative URL resolution) to the expanded URL from the [Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object)’s `url` field in order to construct the full URL. [Path templating](https://spec.openapis.org/oas/v3.0.4.html#path-templating) is allowed. When matching URLs, concrete (non-templated) paths would be matched before their templated counterparts. Templated paths with the same hierarchy but different templated names *MUST NOT* exist as they are identical. In case of ambiguous matching, it’s up to the tooling to decide which one to use. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.8.2 Path Templating Matching

[](https://spec.openapis.org/oas/v3.0.4.html#path-templating-matching)

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

##### 4.7.8.3 Paths Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#paths-object-example)

```
{
  "/pets": {
    "get": {
      "description": "Returns all pets from the system that the user has access to",
      "responses": {
        "200": {
          "description": "A list of pets.",
          "content": {
            "application/json": {
              "schema": {
                "type": "array",
                "items": {
                  "$ref": "#/components/schemas/pet"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

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

#### 4.7.9 Path Item Object

[](https://spec.openapis.org/oas/v3.0.4.html#path-item-object)

Describes the operations available on a single path. A Path Item *MAY* be empty, due to [ACL constraints](https://spec.openapis.org/oas/v3.0.4.html#security-filtering). The path itself is still exposed to the documentation viewer but they will not know which operations and parameters are available.

##### 4.7.9.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-6)

| Field Name | Type | Description |
| --- | --- | --- |
| $ref | `string` | Allows for a referenced definition of this path item. The value *MUST* be in the form of a URL, and the referenced structure *MUST* be in the form of a [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object). In case a Path Item Object field appears both in the defined object and the referenced object, the behavior is undefined. See the rules for resolving [Relative References](https://spec.openapis.org/oas/v3.0.4.html#relative-references-in-urls). |
| summary | `string` | An optional string summary, intended to apply to all operations in this path. |
| description | `string` | An optional string description, intended to apply to all operations in this path. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| get | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a GET operation on this path. |
| put | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a PUT operation on this path. |
| post | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a POST operation on this path. |
| delete | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a DELETE operation on this path. |
| options | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a OPTIONS operation on this path. |
| head | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a HEAD operation on this path. |
| patch | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a PATCH operation on this path. |
| trace | [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) | A definition of a TRACE operation on this path. |
| servers | \[[Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object)\] | An alternative `servers` array to service all operations in this path. If a `servers` array is specified at the [OpenAPI Object](https://spec.openapis.org/oas/v3.0.4.html#oas-servers) level, it will be overridden by this value. |
| parameters | \[[Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the operation level, but cannot be removed there. The list *MUST NOT* include duplicated parameters. A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/v3.0.4.html#parameter-name) and [location](https://spec.openapis.org/oas/v3.0.4.html#parameter-in). The list can use the [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) to link to parameters that are defined in the [OpenAPI Object’s `components.parameters`](https://spec.openapis.org/oas/v3.0.4.html#components-parameters). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.9.2 Path Item Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#path-item-object-example)

```
{
  "get": {
    "description": "Returns pets based on ID",
    "summary": "Find pets by ID",
    "operationId": "getPetsById",
    "responses": {
      "200": {
        "description": "pet response",
        "content": {
          "*/*": {
            "schema": {
              "type": "array",
              "items": {
                "$ref": "#/components/schemas/Pet"
              }
            }
          }
        }
      },
      "default": {
        "description": "error payload",
        "content": {
          "text/html": {
            "schema": {
              "$ref": "#/components/schemas/ErrorModel"
            }
          }
        }
      }
    }
  },
  "parameters": [
    {
      "name": "id",
      "in": "path",
      "description": "ID of pet to use",
      "required": true,
      "schema": {
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "style": "simple"
    }
  ]
}
```

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
```

#### 4.7.10 Operation Object

[](https://spec.openapis.org/oas/v3.0.4.html#operation-object)

Describes a single API operation on a path.

##### 4.7.10.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-7)

| Field Name | Type | Description |
| --- | --- | --- |
| tags | \[`string`\] | A list of tags for API documentation control. Tags can be used for logical grouping of operations by resources or any other qualifier. |
| summary | `string` | A short summary of what the operation does. |
| description | `string` | A verbose explanation of the operation behavior. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object) | Additional external documentation for this operation. |
| operationId | `string` | Unique string used to identify the operation. The id *MUST* be unique among all operations described in the API. The operationId value is **case-sensitive**. Tools and libraries *MAY* use the operationId to uniquely identify an operation, therefore, it is *RECOMMENDED* to follow common programming naming conventions. |
| parameters | \[[Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | A list of parameters that are applicable for this operation. If a parameter is already defined in the [Path Item](https://spec.openapis.org/oas/v3.0.4.html#path-item-parameters), the new definition will override it but can never remove it. The list *MUST NOT* include duplicated parameters. A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/v3.0.4.html#parameter-name) and [location](https://spec.openapis.org/oas/v3.0.4.html#parameter-in). The list can use the [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) to link to parameters that are defined in the [OpenAPI Object’s `components.parameters`](https://spec.openapis.org/oas/v3.0.4.html#components-parameters). |
| requestBody | [Request Body Object](https://spec.openapis.org/oas/v3.0.4.html#request-body-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) | The request body applicable for this operation. The `requestBody` is only supported in HTTP methods where the HTTP 1.1 specification \[[RFC7231](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content")\] [Section 4.3.1](https://datatracker.ietf.org/doc/html/rfc7231#section-4.3.1) has explicitly defined semantics for request bodies. In other cases where the HTTP spec is vague (such as [GET](https://tools.ietf.org/html/rfc7231#section-4.3.1), [HEAD](https://tools.ietf.org/html/rfc7231#section-4.3.2) and [DELETE](https://tools.ietf.org/html/rfc7231#section-4.3.5)), `requestBody` *SHALL* be ignored by consumers. |
| responses | [Responses Object](https://spec.openapis.org/oas/v3.0.4.html#responses-object) | ***REQUIRED***. The list of possible responses as they are returned from executing this operation. |
| callbacks | Map\[`string`, [Callback Object](https://spec.openapis.org/oas/v3.0.4.html#callback-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | A map of possible out-of band callbacks related to the parent operation. The key is a unique identifier for the Callback Object. Each value in the map is a [Callback Object](https://spec.openapis.org/oas/v3.0.4.html#callback-object) that describes a request that may be initiated by the API provider and the expected responses. |
| deprecated | `boolean` | Declares this operation to be deprecated. Consumers *SHOULD* refrain from usage of the declared operation. Default value is `false`. |
| security | \[[Security Requirement Object](https://spec.openapis.org/oas/v3.0.4.html#security-requirement-object)\] | A declaration of which security mechanisms can be used for this operation. The list of values includes alternative Security Requirement Objects that can be used. Only one of the Security Requirement Objects need to be satisfied to authorize a request. To make security optional, an empty security requirement (`{}`) can be included in the array. This definition overrides any declared top-level [`security`](https://spec.openapis.org/oas/v3.0.4.html#oas-security). To remove a top-level security declaration, an empty array can be used. |
| servers | \[[Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object)\] | An alternative `servers` array to service this operation. If a `servers` array is specified at the [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-servers) or [OpenAPI Object](https://spec.openapis.org/oas/v3.0.4.html#oas-servers) level, it will be overridden by this value. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.10.2 Operation Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#operation-object-example)

```
{
  "tags": ["pet"],
  "summary": "Updates a pet in the store with form data",
  "operationId": "updatePetWithForm",
  "parameters": [
    {
      "name": "petId",
      "in": "path",
      "description": "ID of pet that needs to be updated",
      "required": true,
      "schema": {
        "type": "string"
      }
    }
  ],
  "requestBody": {
    "content": {
      "application/x-www-form-urlencoded": {
        "schema": {
          "type": "object",
          "properties": {
            "name": {
              "description": "Updated name of the pet",
              "type": "string"
            },
            "status": {
              "description": "Updated status of the pet",
              "type": "string"
            }
          },
          "required": ["status"]
        }
      }
    }
  },
  "responses": {
    "200": {
      "description": "Pet updated.",
      "content": {
        "application/json": {},
        "application/xml": {}
      }
    },
    "405": {
      "description": "Method Not Allowed",
      "content": {
        "application/json": {},
        "application/xml": {}
      }
    }
  },
  "security": [
    {
      "petstore_auth": ["write:pets", "read:pets"]
    }
  ]
}
```

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

#### 4.7.11 External Documentation Object

[](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object)

Allows referencing an external resource for extended documentation.

##### 4.7.11.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-8)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A description of the target documentation. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| url | `string` | ***REQUIRED***. The URL for the target documentation. This *MUST* be in the form of a URL. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.11.2 External Documentation Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object-example)

```
{
  "description": "Find more info here",
  "url": "https://example.com"
}
```

```
description: Find more info here
url: https://example.com
```

#### 4.7.12 Parameter Object

[](https://spec.openapis.org/oas/v3.0.4.html#parameter-object)

Describes a single operation parameter.

A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/v3.0.4.html#parameter-name) and [location](https://spec.openapis.org/oas/v3.0.4.html#parameter-in).

See [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns, including interactions with the `application/x-www-form-urlencoded` query string format.

##### 4.7.12.1 Parameter Locations

[](https://spec.openapis.org/oas/v3.0.4.html#parameter-locations)

There are four possible parameter locations specified by the `in` field:

-   path - Used together with [Path Templating](https://spec.openapis.org/oas/v3.0.4.html#path-templating), where the parameter value is actually part of the operation’s URL. This does not include the host or base path of the API. For example, in `/items/{itemId}`, the path parameter is `itemId`.
-   query - Parameters that are appended to the URL. For example, in `/items?id=###`, the query parameter is `id`.
-   header - Custom headers that are expected as part of the request. Note that \[[RFC7230](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7230 "Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing")\] [Section 3.2](https://datatracker.ietf.org/doc/html/rfc7230#section-3.2) states header names are case insensitive.
-   cookie - Used to pass a specific cookie value to the API.

##### 4.7.12.2 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-9)

The rules for serialization of the parameter are specified in one of two ways. Parameter Objects *MUST* include either a `content` field or a `schema` field, but not both. See [Appendix B](https://spec.openapis.org/oas/v3.0.4.html#appendix-b-data-type-conversion) for a discussion of converting values of various types to string representations.

###### 4.7.12.2.1 Common Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#common-fixed-fields)

These fields *MAY* be used with either `content` or `schema`.

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the parameter. Parameter names are *case sensitive*.
-   If [`in`](https://spec.openapis.org/oas/v3.0.4.html#parameter-in) is `"path"`, the `name` field *MUST* correspond to a template expression occurring within the [path](https://spec.openapis.org/oas/v3.0.4.html#paths-path) field in the [Paths Object](https://spec.openapis.org/oas/v3.0.4.html#paths-object). See [Path Templating](https://spec.openapis.org/oas/v3.0.4.html#path-templating) for further information.
-   If [`in`](https://spec.openapis.org/oas/v3.0.4.html#parameter-in) is `"header"` and the `name` field is `"Accept"`, `"Content-Type"` or `"Authorization"`, the parameter definition *SHALL* be ignored.
-   For all other cases, the `name` corresponds to the parameter name used by the [`in`](https://spec.openapis.org/oas/v3.0.4.html#parameter-in) field.

 |
| in | `string` | ***REQUIRED***. The location of the parameter. Possible values are `"query"`, `"header"`, `"path"` or `"cookie"`. |
| description | `string` | A brief description of the parameter. This could contain examples of use. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| required | `boolean` | Determines whether this parameter is mandatory. If the [parameter location](https://spec.openapis.org/oas/v3.0.4.html#parameter-in) is `"path"`, this field is ***REQUIRED*** and its value *MUST* be `true`. Otherwise, the field *MAY* be included and its default value is `false`. |
| deprecated | `boolean` | Specifies that a parameter is deprecated and *SHOULD* be transitioned out of usage. Default value is `false`. |
| allowEmptyValue | `boolean` | If `true`, clients *MAY* pass a zero-length string value in place of parameters that would otherwise be omitted entirely, which the server *SHOULD* interpret as the parameter being unused. Default value is `false`. If [`style`](https://spec.openapis.org/oas/v3.0.4.html#parameter-style) is used, and if [behavior is *n/a* (cannot be serialized)](https://spec.openapis.org/oas/v3.0.4.html#style-examples), the value of `allowEmptyValue` *SHALL* be ignored. Interactions between this field and the parameter’s [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) are implementation-defined. This field is valid only for `query` parameters. Use of this field is *NOT RECOMMENDED*, and it is likely to be removed in a later revision. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

Note that while `"Cookie"` as a `name` is not forbidden if `in` is `"header"`, the effect of defining a cookie parameter that way is undefined; use `in: "cookie"` instead.

###### 4.7.12.2.2 Fixed Fields for use with `schema`

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-for-use-with-schema)

For simpler scenarios, a [`schema`](https://spec.openapis.org/oas/v3.0.4.html#parameter-schema) and [`style`](https://spec.openapis.org/oas/v3.0.4.html#parameter-style) can describe the structure and syntax of the parameter. When `example` or `examples` are provided in conjunction with the `schema` field, the example *SHOULD* match the specified schema and follow the prescribed serialization strategy for the parameter. The `example` and `examples` fields are mutually exclusive, and if either is present it *SHALL* *override* any `example` in the schema.

Serializing with `schema` is *NOT RECOMMENDED* for `in: "cookie"` parameters, `in: "header"` parameters that use HTTP header parameters (name=value pairs following a `;`) in their values, or `in: "header"` parameters where values might have non-URL-safe characters; see [Appendix D](https://spec.openapis.org/oas/v3.0.4.html#appendix-d-serializing-headers-and-cookies) for details.

| Field Name | Type | Description |
| --- | --- | --- |
| style | `string` | Describes how the parameter value will be serialized depending on the type of the parameter value. Default values (based on value of `in`): for `"query"` - `"form"`; for `"path"` - `"simple"`; for `"header"` - `"simple"`; for `"cookie"` - `"form"`. |
| explode | `boolean` | When this is true, parameter values of type `array` or `object` generate separate parameters for each value of the array or key-value pair of the map. For other types of parameters this field has no effect. When [`style`](https://spec.openapis.org/oas/v3.0.4.html#parameter-style) is `"form"`, the default value is `true`. For all other styles, the default value is `false`. Note that despite `false` being the default for `deepObject`, the combination of `false` with `deepObject` is undefined. |
| allowReserved | `boolean` | When this is true, parameter values are serialized using reserved expansion, as defined by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 3.2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3), which allows [RFC3986’s reserved character set](https://tools.ietf.org/html/rfc3986#section-2.2), as well as percent-encoded triples, to pass through unchanged, while still percent-encoding all other disallowed characters (including `%` outside of percent-encoded triples). Applications are still responsible for percent-encoding reserved characters that are [not allowed in the query string](https://tools.ietf.org/html/rfc3986#section-3.4) (`[`, `]`, `#`), or have a special meaning in `application/x-www-form-urlencoded` (`-`, `&`, `+`); see Appendices [C](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) and [E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for details. This field only applies to parameters with an `in` value of `query`. The default value is `false`. |
| schema | [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) | The schema defining the type used for the parameter. |
| example | Any | Example of the parameter’s potential value; see [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples). |
| examples | Map\[ `string`, [Example Object](https://spec.openapis.org/oas/v3.0.4.html#example-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | Examples of the parameter’s potential value; see [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples). |

See also [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

###### 4.7.12.2.3 Fixed Fields for use with `content`

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-for-use-with-content)

For more complex scenarios, the [`content`](https://spec.openapis.org/oas/v3.0.4.html#parameter-content) field can define the media type and schema of the parameter, as well as give examples of its use. Using `content` with a `text/plain` media type is *RECOMMENDED* for `in: "header"` and `in: "cookie"` parameters where the `schema` strategy is not appropriate.

| Field Name | Type | Description |
| --- | --- | --- |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/v3.0.4.html#media-type-object)\] | A map containing the representations for the parameter. The key is the media type and the value describes it. The map *MUST* only contain one entry. |

##### 4.7.12.3 Style Values

[](https://spec.openapis.org/oas/v3.0.4.html#style-values)

In order to support common ways of serializing simple parameters, a set of `style` values are defined.

| `style` | [`type`](https://spec.openapis.org/oas/v3.0.4.html#data-types) | `in` | Comments |
| --- | --- | --- | --- |
| matrix | `primitive`, `array`, `object` | `path` | Path-style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 3.2.7](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.7) |
| label | `primitive`, `array`, `object` | `path` | Label style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 3.2.5](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.5) |
| simple | `primitive`, `array`, `object` | `path`, `header` | Simple style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 3.2.2](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.2). This option replaces `collectionFormat` with a `csv` value from OpenAPI 2.0. |
| form | `primitive`, `array`, `object` | `query`, `cookie` | Form style parameters defined by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 3.2.8](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.8). This option replaces `collectionFormat` with a `csv` (when `explode` is false) or `multi` (when `explode` is true) value from OpenAPI 2.0. |
| spaceDelimited | `array`, `object` | `query` | Space separated array values or object properties and values. This option replaces `collectionFormat` equal to `ssv` from OpenAPI 2.0. |
| pipeDelimited | `array`, `object` | `query` | Pipe separated array values or object properties and values. This option replaces `collectionFormat` equal to `pipes` from OpenAPI 2.0. |
| deepObject | `object` | `query` | Allows objects with scalar properties to be represented using form parameters. The representation of array or object properties is not defined. |

See [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for a discussion of percent-encoding, including when delimiters need to be percent-encoded and options for handling collisions with percent-encoded data.

##### 4.7.12.4 Style Examples

[](https://spec.openapis.org/oas/v3.0.4.html#style-examples)

Assume a parameter named `color` has one of the following values:

```
   string -> "blue"
   array -> ["blue", "black", "brown"]
   object -> { "R": 100, "G": 200, "B": 150 }
```

The following table shows examples, as would be shown with the `example` or `examples` keywords, of the different serializations for each value.

-   The value *empty* denotes the empty string, and is unrelated to the `allowEmptyValue` field
-   The behavior of combinations marked *n/a* is undefined
-   The `undefined` column replaces the `empty` column in previous versions of this specification in order to better align with \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-2.3) terminology, which describes certain values including but not limited to `null` as “undefined” values with special handling; notably, the empty string is *not* undefined
-   For `form` and the non-RFC6570 query string styles `spaceDelimited`, `pipeDelimited`, and `deepObject`, each example is shown prefixed with `?` as if it were the only query parameter; see [Appendix C](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for more information on constructing query strings from multiple parameters, and [Appendix D](https://spec.openapis.org/oas/v3.0.4.html#appendix-d-serializing-headers-and-cookies) for warnings regarding `form` and cookie parameters
-   Note that the `?` prefix is not appropriate for serializing `application/x-www-form-urlencoded` HTTP message bodies, and *MUST* be stripped or (if constructing the string manually) not added when used in that context; see the [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) for more information
-   The examples are percent-encoded as required by RFC6570 and RFC3986; see [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for a thorough discussion of percent-encoding concerns, including why unencoded `|` (`%7C`), `[` (`%5B`), and `]` (`%5D`) seem to work in some environments despite not being compliant.

| [`style`](https://spec.openapis.org/oas/v3.0.4.html#style-values) | `explode` | `undefined` | `string` | `array` | `object` |
| --- | --- | --- | --- | --- | --- |
| matrix | false | ;color | ;color=blue | ;color=blue,black,brown | ;color=R,100,G,200,B,150 |
| matrix | true | ;color | ;color=blue | ;color=blue;color=black;color=brown | ;R=100;G=200;B=150 |
| label | false | . | .blue | .blue,black,brown | .R,100,G,200,B,150 |
| label | true | . | .blue | .blue.black.brown | .R=100.G=200.B=150 |
| simple | false | *empty* | blue | blue,black,brown | R,100,G,200,B,150 |
| simple | true | *empty* | blue | blue,black,brown | R=100,G=200,B=150 |
| form | false | ?color= | ?color=blue | ?color=blue,black,brown | ?color=R,100,G,200,B,150 |
| form | true | ?color= | ?color=blue | ?color=blue&color=black&color=brown | ?R=100&G=200&B=150 |
| spaceDelimited | false | *n/a* | *n/a* | ?color=blue%20black%20brown | ?color=R%20100%20G%20200%20B%20150 |
| spaceDelimited | true | *n/a* | *n/a* | *n/a* | *n/a* |
| pipeDelimited | false | *n/a* | *n/a* | ?color=blue%7Cblack%7Cbrown | ?color=R%7C100%7CG%7C200%7CB%7C150 |
| pipeDelimited | true | *n/a* | *n/a* | *n/a* | *n/a* |
| deepObject | false | *n/a* | *n/a* | *n/a* | *n/a* |
| deepObject | true | *n/a* | *n/a* | *n/a* | ?color%5BR%5D=100&color%5BG%5D=200&color%5BB%5D=150 |

##### 4.7.12.5 Parameter Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#parameter-object-examples)

A header parameter with an array of 64-bit integer numbers:

```
{
  "name": "token",
  "in": "header",
  "description": "token to be passed as a header",
  "required": true,
  "schema": {
    "type": "array",
    "items": {
      "type": "integer",
      "format": "int64"
    }
  },
  "style": "simple"
}
```

```
name: token
in: header
description: token to be passed as a header
required: true
schema:
  type: array
  items:
    type: integer
    format: int64
style: simple
```

A path parameter of a string value:

```
{
  "name": "username",
  "in": "path",
  "description": "username to fetch",
  "required": true,
  "schema": {
    "type": "string"
  }
}
```

```
name: username
in: path
description: username to fetch
required: true
schema:
  type: string
```

An optional query parameter of a string value, allowing multiple values by repeating the query parameter:

```
{
  "name": "id",
  "in": "query",
  "description": "ID of the object to fetch",
  "required": false,
  "schema": {
    "type": "array",
    "items": {
      "type": "string"
    }
  },
  "style": "form",
  "explode": true
}
```

```
name: id
in: query
description: ID of the object to fetch
required: false
schema:
  type: array
  items:
    type: string
style: form
explode: true
```

A free-form query parameter, allowing undefined parameters of a specific type:

```
{
  "in": "query",
  "name": "freeForm",
  "schema": {
    "type": "object",
    "additionalProperties": {
      "type": "integer"
    }
  },
  "style": "form"
}
```

```
in: query
name: freeForm
schema:
  type: object
  additionalProperties:
    type: integer
style: form
```

A complex parameter using `content` to define serialization:

```
{
  "in": "query",
  "name": "coordinates",
  "content": {
    "application/json": {
      "schema": {
        "type": "object",
        "required": ["lat", "long"],
        "properties": {
          "lat": {
            "type": "number"
          },
          "long": {
            "type": "number"
          }
        }
      }
    }
  }
}
```

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
```

#### 4.7.13 Request Body Object

[](https://spec.openapis.org/oas/v3.0.4.html#request-body-object)

Describes a single request body.

##### 4.7.13.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-10)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A brief description of the request body. This could contain examples of use. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/v3.0.4.html#media-type-object)\] | ***REQUIRED***. The content of the request body. The key is a media type or media type range, see \[[RFC7231](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content")\] [Appendix D](https://datatracker.ietf.org/doc/html/rfc7231#appendix-D), and the value describes it. For requests that match multiple keys, only the most specific key is applicable. e.g. `"text/plain"` overrides `"text/*"` |
| required | `boolean` | Determines if the request body is required in the request. Defaults to `false`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.13.2 Request Body Examples

[](https://spec.openapis.org/oas/v3.0.4.html#request-body-examples)

A request body with a referenced schema definition.

```
{
  "description": "user to add to the system",
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/User"
      },
      "examples": {
        "user": {
          "summary": "User Example",
          "externalValue": "https://foo.bar/examples/user-example.json"
        }
      }
    },
    "application/xml": {
      "schema": {
        "$ref": "#/components/schemas/User"
      },
      "examples": {
        "user": {
          "summary": "User example in XML",
          "externalValue": "https://foo.bar/examples/user-example.xml"
        }
      }
    },
    "text/plain": {
      "examples": {
        "user": {
          "summary": "User example in Plain text",
          "externalValue": "https://foo.bar/examples/user-example.txt"
        }
      }
    },
    "*/*": {
      "examples": {
        "user": {
          "summary": "User example in other format",
          "externalValue": "https://foo.bar/examples/user-example.whatever"
        }
      }
    }
  }
}
```

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

#### 4.7.14 Media Type Object

[](https://spec.openapis.org/oas/v3.0.4.html#media-type-object)

Each Media Type Object provides schema and examples for the media type identified by its key.

When `example` or `examples` are provided, the example *SHOULD* match the specified schema and be in the correct format as specified by the media type and its encoding. The `example` and `examples` fields are mutually exclusive, and if either is present it *SHALL* *override* any `example` in the schema. See [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples) for further guidance regarding the different ways of specifying examples, including non-JSON/YAML values.

##### 4.7.14.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-11)

| Field Name | Type | Description |
| --- | --- | --- |
| schema | [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) | The schema defining the content of the request, response, parameter, or header. |
| example | Any | Example of the media type; see [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples). |
| examples | Map\[ `string`, [Example Object](https://spec.openapis.org/oas/v3.0.4.html#example-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | Examples of the media type; see [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples). |
| encoding | Map\[`string`, [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object)\] | A map between a property name and its encoding information. The key, being the property name, *MUST* exist in the schema as a property. The `encoding` field *SHALL* only apply to [Request Body Objects](https://spec.openapis.org/oas/v3.0.4.html#request-body-object), and only when the media type is `multipart` or `application/x-www-form-urlencoded`. If no Encoding Object is provided for a property, the behavior is determined by the default values documented for the Encoding Object. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.14.2 Media Type Examples

[](https://spec.openapis.org/oas/v3.0.4.html#media-type-examples-0)

```
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/Pet"
    },
    "examples": {
      "cat": {
        "summary": "An example of a cat",
        "value": {
          "name": "Fluffy",
          "petType": "Cat",
          "color": "White",
          "gender": "male",
          "breed": "Persian"
        }
      },
      "dog": {
        "summary": "An example of a dog with a cat's name",
        "value": {
          "name": "Puma",
          "petType": "Dog",
          "color": "Black",
          "gender": "Female",
          "breed": "Mixed"
        }
      },
      "frog": {
        "$ref": "#/components/examples/frog-example"
      }
    }
  }
}
```

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

##### 4.7.14.3 Considerations for File Uploads

[](https://spec.openapis.org/oas/v3.0.4.html#considerations-for-file-uploads)

In contrast to OpenAPI 2.0, `file` input/output content in OpenAPI 3 is described with the same semantics as any other schema type. Specifically:

```
# content transferred in binary (octet-stream):
schema:
  type: string
  format: binary
```

These examples apply to either input payloads of file uploads or response payloads.

A `requestBody` for submitting a file in a `POST` operation may look like the following example:

```
requestBody:
  content:
    application/octet-stream:
      schema:
        # a binary file of any type
        type: string
        format: binary
```

In addition, specific media types *MAY* be specified:

```
# multiple, specific media types may be specified:
requestBody:
  content:
    # a binary file of type png or jpeg
    'image/jpeg':
      schema:
        type: string
        format: binary
    'image/png':
      schema:
        type: string
        format: binary
```

To upload multiple files, a `multipart` media type *MUST* be used as shown under [Example: Multipart Form with Multiple Files](https://spec.openapis.org/oas/v3.0.4.html#example-multipart-form-with-multiple-files).

##### 4.7.14.4 Support for x-www-form-urlencoded Request Bodies

[](https://spec.openapis.org/oas/v3.0.4.html#support-for-x-www-form-urlencoded-request-bodies)

See [Encoding the `x-www-form-urlencoded` Media Type](https://spec.openapis.org/oas/v3.0.4.html#encoding-the-x-www-form-urlencoded-media-type) for guidance and examples, both with and without the `encoding` field.

##### 4.7.14.5 Special Considerations for `multipart` Content

[](https://spec.openapis.org/oas/v3.0.4.html#special-considerations-for-multipart-content)

See [Encoding `multipart` Media Types](https://spec.openapis.org/oas/v3.0.4.html#encoding-multipart-media-types) for further guidance and examples, both with and without the `encoding` field.

#### 4.7.15 Encoding Object

[](https://spec.openapis.org/oas/v3.0.4.html#encoding-object)

A single encoding definition applied to a single schema property. See [Appendix B](https://spec.openapis.org/oas/v3.0.4.html#appendix-b-data-type-conversion) for a discussion of converting values of various types to string representations.

Properties are correlated with `multipart` parts using the [`name` parameter](https://tools.ietf.org/html/rfc7578#section-4.2) of `Content-Disposition: form-data`, and with `application/x-www-form-urlencoded` using the query string parameter names. In both cases, their order is implementation-defined.

See [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns for form media types.

##### 4.7.15.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-12)

###### 4.7.15.1.1 Common Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#common-fixed-fields-0)

These fields *MAY* be used either with or without the RFC6570-style serialization fields defined in the next section below.

| Field Name | Type | Description |
| --- | --- | --- |
| contentType | `string` | The `Content-Type` for encoding a specific property. The value is a comma-separated list, each element of which is either a specific media type (e.g. `image/png`) or a wildcard media type (e.g. `image/*`). Default value depends on the property type as shown in the table below. |
| headers | Map\[`string`, [Header Object](https://spec.openapis.org/oas/v3.0.4.html#header-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | A map allowing additional information to be provided as headers. `Content-Type` is described separately and *SHALL* be ignored in this section. This field *SHALL* be ignored if the request body media type is not a `multipart`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

The default values for `contentType` are as follows, where an *n/a* in the `format` column means that the presence or value of `format` is irrelevant:

| `type` | `format` | Default `contentType` |
| --- | --- | --- |
| `string` | `binary` *or* `byte` | `application/octet-stream` |
| `string` | *none, or any except `binary` or `byte`* | `text/plain` |
| `number`, `integer`, or `boolean` | *n/a* | `text/plain` |
| `object` | *n/a* | `application/json` |
| `array` | *n/a* | according to the `type` and `format` of the `items` schema |

Determining how to handle `null` values if `nullable: true` is present depends on how `null` values are being serialized. If `null` values are entirely omitted, then the `contentType` is irrelevant. See [Appendix B](https://spec.openapis.org/oas/v3.0.4.html#appendix-b-data-type-conversion) for a discussion of data type conversion options.

###### 4.7.15.1.2 Fixed Fields for RFC6570-style Serialization

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-for-rfc6570-style-serialization)

| Field Name | Type | Description |
| --- | --- | --- |
| style | `string` | Describes how a specific property value will be serialized depending on its type. See [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) for details on the [`style`](https://spec.openapis.org/oas/v3.0.4.html#parameter-style) field. The behavior follows the same values as `query` parameters, including default values. Note that the initial `?` used in query strings is not used in `application/x-www-form-urlencoded` message bodies, and *MUST* be removed (if using an RFC6570 implementation) or simply not added (if constructing the string manually). This field *SHALL* be ignored if the request body media type is not `application/x-www-form-urlencoded`. |
| explode | `boolean` | When this is true, property values of type `array` or `object` generate separate parameters for each value of the array, or key-value-pair of the map. For other types of properties this field has no effect. When [`style`](https://spec.openapis.org/oas/v3.0.4.html#encoding-style) is `"form"`, the default value is `true`. For all other styles, the default value is `false`. Note that despite `false` being the default for `deepObject`, the combination of `false` with `deepObject` is undefined. This field *SHALL* be ignored if the request body media type is not `application/x-www-form-urlencoded`. |
| allowReserved | `boolean` | When this is true, parameter values are serialized using reserved expansion, as defined by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 3.2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-3.2.3), which allows [RFC3986’s reserved character set](https://tools.ietf.org/html/rfc3986#section-2.2), as well as percent-encoded triples, to pass through unchanged, while still percent-encoding all other disallowed characters (including `%` outside of percent-encoded triples). Applications are still responsible for percent-encoding reserved characters that are [not allowed in the query string](https://tools.ietf.org/html/rfc3986#section-3.4) (`[`, `]`, `#`), or have a special meaning in `application/x-www-form-urlencoded` (`-`, `&`, `+`); see Appendices [C](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) and [E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for details. The default value is `false`. This field *SHALL* be ignored if the request body media type is not `application/x-www-form-urlencoded`. |

See also [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

The role of `contentType` with `application/x-www-form-urlencoded` request bodies was not described in detail in version 3.0.3 and earlier of this specification. To match the intent of these fields and be compatible with version 3.1 of this specification, it is *RECOMMENDED* that whenever any of `style`, `explode`, or `allowReserved` are present with an explicit value:

-   The value of `contentType`, whether it is explicitly defined or has the default value, is to be ignored
-   If any of `style`, `explode`, or `allowReserved` are *not* present with explicit values, then they are to be treated as if they were present with their default values

However, if all three of `style`, `explode`, and `allowReserved` fields are absent, it is *RECOMMENDED* that:

-   All three keywords are to be entirely ignored, rather than treated as having their default values
-   Encoding is to be based on `contentType` alone, whether it is present with an explicit value or absent and treated as having its default value

Note that the presence of at least one of `style`, `explode`, or `allowReserved` with an explicit value is equivalent to using `schema` with `in: "query"` Parameter Objects. The absence of all three of those fields is the equivalent of using `content`, but with the media type specified in `contentType` rather than through a Media Type Object.

##### 4.7.15.2 Encoding the `x-www-form-urlencoded` Media Type

[](https://spec.openapis.org/oas/v3.0.4.html#encoding-the-x-www-form-urlencoded-media-type)

To submit content using form url encoding via \[[RFC1866](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1866 "Hypertext Markup Language - 2.0")\], use the `application/x-www-form-urlencoded` media type in the [Media Type Object](https://spec.openapis.org/oas/v3.0.4.html#media-type-object) under the [Request Body Object](https://spec.openapis.org/oas/v3.0.4.html#request-body-object). This configuration means that the request body *MUST* be encoded per \[[RFC1866](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1866 "Hypertext Markup Language - 2.0")\] when passed to the server, after any complex objects have been serialized to a string representation.

See [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns for form media types.

###### 4.7.15.2.1 Example: URL Encoded Form with JSON Values

[](https://spec.openapis.org/oas/v3.0.4.html#example-url-encoded-form-with-json-values)

When there is no [`encoding`](https://spec.openapis.org/oas/v3.0.4.html#media-type-encoding) field, the serialization strategy is based on the Encoding Object’s default values:

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
            # complex types are stringified to support RFC 1866
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

Assuming the most compact representation of the JSON value (with unnecessary whitespace removed), we would expect to see the following request body, where space characters have been replaced with `+` and `+`, `"`, `{`, and `}` have been percent-encoded to `%2B`, `%22`, `%7B`, and `%7D`, respectively:

```
id=f81d4fae-7dec-11d0-a765-00a0c91e6bf6&address=%7B%22streetAddress%22:%22123+Example+Dr.%22,%22city%22:%22Somewhere%22,%22state%22:%22CA%22,%22zip%22:%2299999%2B1234%22%7D
```

Note that the `id` keyword is treated as `text/plain` per the [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object)’s default behavior, and is serialized as-is. If it were treated as `application/json`, then the serialized value would be a JSON string including quotation marks, which would be percent-encoded as `%22`.

Here is the `id` parameter (without `address`) serialized as `application/json` instead of `text/plain`, and then encoded per RFC1866:

```
id=%22f81d4fae-7dec-11d0-a765-00a0c91e6bf6%22
```

###### 4.7.15.2.2 Example: URL Encoded Form with Binary Values

[](https://spec.openapis.org/oas/v3.0.4.html#example-url-encoded-form-with-binary-values)

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
            # The default with "format: byte" is application/octet-stream,
            # so we need to set image media type(s) in the Encoding Object.
            type: string
            format: byte
  encoding:
    icon:
      contentType: image/png, image/jpeg
```

Given a name of `example` and a solid red 2x2-pixel PNG for `icon`, this would produce a request body of:

```
name=example&icon=iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAABGdBTUEAALGPC%2FxhBQAAADhlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAAqACAAQAAAABAAAAAqADAAQAAAABAAAAAgAAAADO0J6QAAAAEElEQVQIHWP8zwACTGCSAQANHQEDqtPptQAAAABJRU5ErkJggg%3D%3D
```

Note that this base64-encoded value had to be futher percent-encoded, replacing `/` with `%2F` and each of two final `=` padding characters with `%3D`. Some base64-decoding implementations may be able to use the string without the padding per \[[RFC4648](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc4648 "The Base16, Base32, and Base64 Data Encodings")\] [Section 3.2](https://datatracker.ietf.org/doc/html/rfc4648#section-3.2). However, this is not guaranteed and the value would still need to be percent-decoded due to the `%2F`.

##### 4.7.15.3 Encoding `multipart` Media Types

[](https://spec.openapis.org/oas/v3.0.4.html#encoding-multipart-media-types)

It is common to use `multipart/form-data` as a `Content-Type` when transferring forms as request bodies. In contrast to OpenAPI 2.0, a `schema` is *REQUIRED* to define the input parameters to the operation when using `multipart` content. This supports complex structures as well as supporting mechanisms for multiple file uploads.

The `form-data` disposition and its `name` parameter are mandatory for `multipart/form-data` (\[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.2](https://datatracker.ietf.org/doc/html/rfc7578#section-4.2)). Array properties are handled by applying the same `name` to multiple parts, as is recommended by \[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.3](https://datatracker.ietf.org/doc/html/rfc7578#section-4.3) for supplying multiple values per form field. See \[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 5](https://datatracker.ietf.org/doc/html/rfc7578#section-5) for guidance regarding non-ASCII part names.

Various other `multipart` types, most notable `multipart/mixed` (\[[RFC2046](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc2046 "Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types")\] [Section 5.1.3](https://datatracker.ietf.org/doc/html/rfc2046#section-5.1.3)) neither require nor forbid specific `Content-Disposition` values, which means care must be taken to ensure that any values used are supported by all relevant software. It is not currently possible to correlate schema properties with unnamed, ordered parts in media types such as `multipart/mixed`, but implementations *MAY* choose to support such types when `Content-Disposition: form-data` is used with a `name` parameter.

Note that there are significant restrictions on what headers can be used with `multipart` media types in general (\[[RFC2046](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc2046 "Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types")\] [Section 5.1](https://datatracker.ietf.org/doc/html/rfc2046#section-5.1)) and `multi-part/form-data` in particular (\[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.8](https://datatracker.ietf.org/doc/html/rfc7578#section-4.8)).

Note also that `Content-Transfer-Encoding` is deprecated for `multipart/form-data` (\[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.7](https://datatracker.ietf.org/doc/html/rfc7578#section-4.7)) where binary data is supported, as it is in HTTP.

Using `format: "byte"` for a multipart field is equivalent to specifying an [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) with a `headers` field containing `Content-Transfer-Encoding` with a schema that requires the value `base64`. If `format: "byte"` is used for a multipart field that has an Encoding Object with a `headers` field containing `Content-Transfer-Encoding` with a schema that disallows `base64`, the result is undefined for serialization and parsing.

Per the JSON Schema specification, `contentMediaType` without `contentEncoding` present is treated as if `contentEncoding: "identity"` were present. While useful for embedding text documents such as `text/html` into JSON strings, it is not useful for a `multipart/form-data` part, as it just causes the document to be treated as `text/plain` instead of its actual media type. Use the Encoding Object without `contentMediaType` if no `contentEncoding` is required.

See [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for a detailed examination of percent-encoding concerns for form media types.

###### 4.7.15.3.1 Example: Basic Multipart Form

[](https://spec.openapis.org/oas/v3.0.4.html#example-basic-multipart-form)

When the `encoding` field is *not* used, the encoding is determined by the Encoding Object’s defaults:

```
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          id:
            # default for primitives without a special format is text/plain
            type: string
            format: uuid
          profileImage:
            # default for string with binary format is `application/octet-stream`
            type: string
            format: binary
          addresses:
            # default for arrays is based on the type in the `items`
            # subschema, which is an object, so `application/json`
            type: array
            items:
              $ref: '#/components/schemas/Address'
```

###### 4.7.15.3.2 Example: Multipart Form with Encoding Objects

[](https://spec.openapis.org/oas/v3.0.4.html#example-multipart-form-with-encoding-objects)

Using `encoding`, we can set more specific types for binary data, or non-JSON formats for complex values. We can also describe headers for each part:

```
requestBody:
  content:
    multipart/form-data:
      schema:
        type: object
        properties:
          id:
            # default is `text/plain`
            type: string
            format: uuid
          addresses:
            # default based on the `items` subschema would be
            # `application/json`, but we want these address objects
            # serialized as `application/xml` instead
            description: addresses in XML format
            type: array
            items:
              $ref: '#/components/schemas/Address'
          profileImage:
            # default is application/octet-stream, but we can declare
            # a more specific image type or types
            type: string
            format: binary
      encoding:
        addresses:
          # require XML Content-Type in utf-8 encoding
          # This is applied to each address part corresponding
          # to each address in he array
          contentType: application/xml; charset=utf-8
        profileImage:
          # only accept png or jpeg
          contentType: image/png, image/jpeg
          headers:
            X-Rate-Limit-Limit:
              description: The number of allowed requests in the current period
              schema:
                type: integer
```

###### 4.7.15.3.3 Example: Multipart Form with Multiple Files

[](https://spec.openapis.org/oas/v3.0.4.html#example-multipart-form-with-multiple-files)

In accordance with \[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 4.3](https://datatracker.ietf.org/doc/html/rfc7578#section-4.3), multiple files for a single form field are uploaded using the same name (`file` in this example) for each file’s part:

```
requestBody:
  content:
    multipart/form-data:
      schema:
        properties:
          # The property name 'file' will be used for all files.
          file:
            type: array
            items:
              type: string
              format: binary
```

#### 4.7.16 Responses Object

[](https://spec.openapis.org/oas/v3.0.4.html#responses-object)

A container for the expected responses of an operation. The container maps a HTTP response code to the expected response.

The documentation is not necessarily expected to cover all possible HTTP response codes because they may not be known in advance. However, documentation is expected to cover a successful operation response and any known errors.

The `default` *MAY* be used as a default Response Object for all HTTP codes that are not covered individually by the Responses Object.

The Responses Object *MUST* contain at least one response code, and if only one response code is provided it *SHOULD* be the response for a successful operation call.

##### 4.7.16.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-13)

| Field Name | Type | Description |
| --- | --- | --- |
| default | [Response Object](https://spec.openapis.org/oas/v3.0.4.html#response-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) | The documentation of responses other than the ones declared for specific HTTP response codes. Use this field to cover undeclared responses. A [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) can link to a response that the [OpenAPI Object’s `components.responses`](https://spec.openapis.org/oas/v3.0.4.html#components-responses) section defines. |

##### 4.7.16.2 Patterned Fields

[](https://spec.openapis.org/oas/v3.0.4.html#patterned-fields-0)

| Field Pattern | Type | Description |
| --- | --- | --- |
| [HTTP Status Code](https://spec.openapis.org/oas/v3.0.4.html#http-status-codes) | [Response Object](https://spec.openapis.org/oas/v3.0.4.html#response-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) | Any [HTTP status code](https://spec.openapis.org/oas/v3.0.4.html#http-status-codes) can be used as the property name, but only one property per code, to describe the expected response for that HTTP status code. A [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) can link to a response that is defined in the [OpenAPI Object’s `components.responses`](https://spec.openapis.org/oas/v3.0.4.html#components-responses) section. This field *MUST* be enclosed in quotation marks (for example, “200”) for compatibility between JSON and YAML. To define a range of response codes, this field *MAY* contain the uppercase wildcard character `X`. For example, `2XX` represents all response codes between `200` and `299`. Only the following range definitions are allowed: `1XX`, `2XX`, `3XX`, `4XX`, and `5XX`. If a response is defined using an explicit code, the explicit code definition takes precedence over the range definition for that code. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.16.3 Responses Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#responses-object-example)

A 200 response for a successful operation and a default response for others (implying an error):

```
{
  "200": {
    "description": "a pet to be returned",
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/Pet"
        }
      }
    }
  },
  "default": {
    "description": "Unexpected error",
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/ErrorModel"
        }
      }
    }
  }
}
```

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

#### 4.7.17 Response Object

[](https://spec.openapis.org/oas/v3.0.4.html#response-object)

Describes a single response from an API operation, including design-time, static `links` to operations based on the response.

##### 4.7.17.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-14)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | ***REQUIRED***. A description of the response. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| headers | Map\[`string`, [Header Object](https://spec.openapis.org/oas/v3.0.4.html#header-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | Maps a header name to its definition. \[[RFC7230](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7230 "Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing")\] [Section 3.2](https://datatracker.ietf.org/doc/html/rfc7230#section-3.2) states header names are case insensitive. If a response header is defined with the name `"Content-Type"`, it *SHALL* be ignored. |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/v3.0.4.html#media-type-object)\] | A map containing descriptions of potential response payloads. The key is a media type or media type range, see \[[RFC7231](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content")\] [Appendix D](https://datatracker.ietf.org/doc/html/rfc7231#appendix-D), and the value describes it. For responses that match multiple keys, only the most specific key is applicable. e.g. `"text/plain"` overrides `"text/*"` |
| links | Map\[`string`, [Link Object](https://spec.openapis.org/oas/v3.0.4.html#link-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | A map of operations links that can be followed from the response. The key of the map is a short name for the link, following the naming constraints of the names for [Component Objects](https://spec.openapis.org/oas/v3.0.4.html#components-object). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.17.2 Response Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#response-object-examples)

Response of an array of a complex type:

```
{
  "description": "A complex object array response",
  "content": {
    "application/json": {
      "schema": {
        "type": "array",
        "items": {
          "$ref": "#/components/schemas/VeryComplexType"
        }
      }
    }
  }
}
```

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
{
  "description": "A simple string response",
  "content": {
    "text/plain": {
      "schema": {
        "type": "string"
      }
    }
  }
}
```

```
description: A simple string response
content:
  text/plain:
    schema:
      type: string
```

Plain text response with headers:

```
{
  "description": "A simple string response",
  "content": {
    "text/plain": {
      "schema": {
        "type": "string"
      },
      "example": "whoa!"
    }
  },
  "headers": {
    "X-Rate-Limit-Limit": {
      "description": "The number of allowed requests in the current period",
      "schema": {
        "type": "integer"
      }
    },
    "X-Rate-Limit-Remaining": {
      "description": "The number of remaining requests in the current period",
      "schema": {
        "type": "integer"
      }
    },
    "X-Rate-Limit-Reset": {
      "description": "The number of seconds left in the current period",
      "schema": {
        "type": "integer"
      }
    }
  }
}
```

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
{
  "description": "object created"
}
```

```
description: object created
```

#### 4.7.18 Callback Object

[](https://spec.openapis.org/oas/v3.0.4.html#callback-object)

A map of possible out-of band callbacks related to the parent operation. Each value in the map is a [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) that describes a set of requests that may be initiated by the API provider and the expected responses. The key value used to identify the Path Item Object is an expression, evaluated at runtime, that identifies a URL to use for the callback operation.

##### 4.7.18.1 Patterned Fields

[](https://spec.openapis.org/oas/v3.0.4.html#patterned-fields-1)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {expression} | [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) | A Path Item Object used to define a callback request and expected responses. A [complete example](https://learn.openapis.org/examples/v3.0/callback-example.html) is available. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.18.2 Key Expression

[](https://spec.openapis.org/oas/v3.0.4.html#key-expression)

The key that identifies the [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) is a [runtime expression](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions) that can be evaluated in the context of a runtime HTTP request/response to identify the URL to be used for the callback request. A simple example might be `$request.body#/url`. However, using a [runtime expression](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions) the complete HTTP message can be accessed. This includes accessing any part of a body that a JSON Pointer \[[RFC6901](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\] can reference.

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

##### 4.7.18.3 Callback Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#callback-object-examples)

The following example uses the user provided `queryUrl` query string parameter to define the callback URL. This is an example of how to use a Callback Object to describe a WebHook callback that goes with the subscription operation to enable registering for the WebHook.

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

#### 4.7.19 Example Object

[](https://spec.openapis.org/oas/v3.0.4.html#example-object)

An object grouping an internal or external example value with basic `summary` and `description` metadata. This object is typically used in fields named `examples` (plural), and is a [referenceable](https://spec.openapis.org/oas/v3.0.4.html#reference-object) alternative to older `example` (singular) fields that do not support referencing or metadata.

Examples allow demonstration of the usage of properties, parameters and objects within OpenAPI.

##### 4.7.19.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-15)

| Field Name | Type | Description |
| --- | --- | --- |
| summary | `string` | Short description for the example. |
| description | `string` | Long description for the example. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| value | Any | Embedded literal example. The `value` field and `externalValue` field are mutually exclusive. To represent examples of media types that cannot naturally represented in JSON or YAML, use a string value to contain the example, escaping where necessary. |
| externalValue | `string` | A URL that points to the literal example. This provides the capability to reference examples that cannot easily be included in JSON or YAML documents. The `value` field and `externalValue` field are mutually exclusive. See the rules for resolving [Relative References](https://spec.openapis.org/oas/v3.0.4.html#relative-references-in-urls). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

In all cases, the example value *SHOULD* be compatible with the schema of its associated value. Tooling implementations *MAY* choose to validate compatibility automatically, and reject the example value(s) if incompatible.

##### 4.7.19.2 Working with Examples

[](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples)

Example Objects can be used in both [Parameter Objects](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) and [Media Type Objects](https://spec.openapis.org/oas/v3.0.4.html#media-type-object). In both objects, this is done through the `examples` (plural) field. However, there are two other ways to provide examples: The `example` (singular) field that is mutually exclusive with `examples` in both objects, and the `example` (singular) field in the [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) that appears in the `schema` field of both objects. Each of these fields has slightly different considerations.

The Schema Object’s `example` field is used to show example values without regard to how they might be formatted as parameters or within media type representations.

The mutually exclusive fields in the Parameter or Media Type Objects are used to show example values which *SHOULD* both match the schema and be formatted as they would appear as a serialized parameter or within a media type representation. The exact serialization and encoding is determined by various fields in the Parameter Object, or in the Media Type Object’s [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object). Because examples using these fields represent the final serialized form of the data, they *SHALL* *override* any `example` in the corresponding Schema Object.

The singular `example` field in the Parameter or Media Type Object is concise and convenient for simple examples, but does not offer any other advantages over using Example Objects under `examples`.

Some examples cannot be represented directly in JSON or YAML. For all three ways of providing examples, these can be shown as string values with any escaping necessary to make the string valid in the JSON or YAML format of documents that comprise the OpenAPI Description. With the Example Object, such values can alternatively be handled through the `externalValue` field.

##### 4.7.19.3 Example Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#example-object-examples)

In a request body:

```
requestBody:
  content:
    'application/json':
      schema:
        $ref: '#/components/schemas/Address'
      examples:
        foo:
          summary: A foo example
          value:
            foo: bar
        bar:
          summary: A bar example
          value:
            bar: baz
    application/xml:
      examples:
        xmlExample:
          summary: This is an example in XML
          externalValue: https://example.org/examples/address-example.xml
    text/plain:
      examples:
        textExample:
          summary: This is a text example
          externalValue: https://foo.bar/examples/address-example.txt
```

In a parameter:

```
parameters:
  - name: zipCode
    in: query
    schema:
      type: string
      format: zip-code
    examples:
      zip-example:
        $ref: '#/components/examples/zip-example'
```

In a response:

```
responses:
  '200':
    description: your car appointment has been booked
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/SuccessResponse'
        examples:
          confirmation-success:
            $ref: '#/components/examples/confirmation-success'
```

Two different uses of JSON strings:

First, a request or response body that is just a JSON string (not an object containing a string):

```
"application/json": {
  "schema": {
    "type": "string"
  },
  "examples": {
    "jsonBody": {
      "description": "A body of just the JSON string \"json\"",
      "value": "json"
    }
  }
}
```

```
application/json:
  schema:
    type: string
  examples:
    jsonBody:
      description: 'A body of just the JSON string "json"'
      value: json
```

In the above example, we can just show the JSON string (or any JSON value) as-is, rather than stuffing a serialized JSON value into a JSON string, which would have looked like `"\"json\""`.

In contrast, a JSON string encoded inside of a URL-style form body:

```
"application/x-www-form-urlencoded": {
  "schema": {
    "type": "object",
    "properties": {
      "jsonValue": {
        "type": "string"
      }
    }
  },
  "encoding": {
    "jsonValue": {
      "contentType": "application/json"
    }
  },
  "examples": {
    "jsonFormValue": {
      "description": "The JSON string \"json\" as a form value",
      "value": "jsonValue=%22json%22"
    }
  }
}
```

```
application/x-www-form-urlencoded:
  schema:
    type: object
    properties:
      jsonValue:
        type: string
  encoding:
    jsonValue:
      contentType: application/json
  examples:
    jsonFormValue:
      description: 'The JSON string "json" as a form value'
      value: jsonValue=%22json%22
```

In this example, the JSON string had to be serialized before encoding it into the URL form value, so the example includes the quotation marks that are part of the JSON serialization, which are then URL percent-encoded.

#### 4.7.20 Link Object

[](https://spec.openapis.org/oas/v3.0.4.html#link-object)

The Link Object represents a possible design-time link for a response. The presence of a link does not guarantee the caller’s ability to successfully invoke it, rather it provides a known relationship and traversal mechanism between responses and other operations.

Unlike *dynamic* links (i.e. links provided **in** the response payload), the OAS linking mechanism does not require link information in the runtime response.

For computing links and providing instructions to execute them, a [runtime expression](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions) is used for accessing values in an operation and using them as parameters while invoking the linked operation.

##### 4.7.20.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-16)

| Field Name | Type | Description |
| --- | --- | --- |
| operationRef | `string` | A URI reference to an OAS operation. This field is mutually exclusive of the `operationId` field, and *MUST* point to an [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object). |
| operationId | `string` | The name of an *existing*, resolvable OAS operation, as defined with a unique `operationId`. This field is mutually exclusive of the `operationRef` field. |
| parameters | Map\[`string`, Any | [{expression}](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions)\] | A map representing parameters to pass to an operation as specified with `operationId` or identified via `operationRef`. The key is the parameter name to be used (optionally qualified with the parameter location, e.g. `path.id` for an `id` parameter in the path), whereas the value can be a constant or an expression to be evaluated and passed to the linked operation. |
| requestBody | Any | [{expression}](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions) | A literal value or [{expression}](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions) to use as a request body when calling the target operation. |
| description | `string` | A description of the link. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| server | [Server Object](https://spec.openapis.org/oas/v3.0.4.html#server-object) | A server object to be used by the target operation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

A linked operation *MUST* be identified using either an `operationRef` or `operationId`. The identified or reference operation *MUST* be unique, and in the case of an `operationId`, it *MUST* be resolved within the scope of the OpenAPI Description (OAD). Because of the potential for name clashes, the `operationRef` syntax is preferred for multi-document OADs. However, because use of an operation depends on its URL path template in the [Paths Object](https://spec.openapis.org/oas/v3.0.4.html#paths-object), operations from any [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) that is referenced multiple times within the OAD cannot be resolved unambiguously. In such ambiguous cases, the resulting behavior is implementation-defined and *MAY* result in an error.

Note that it is not possible to provide a constant value to `parameters` that matches the syntax of a runtime expression. It is possible to have ambiguous parameter names, e.g. `name: "id", in: "path"` and `name: "path.id", in: "query"`; this is *NOT RECOMMENDED* and the behavior is implementation-defined, however implementations *SHOULD* prefer the qualified interpretation (`path.id` as a path parameter), as the names can always be qualified to disambiguate them (e.g. using `query.path.id` for the query parameter).

##### 4.7.20.2 Examples

[](https://spec.openapis.org/oas/v3.0.4.html#examples)

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
                # get the `id` field from the request path parameter named `id`
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

##### 4.7.20.3 `operationRef` Examples

[](https://spec.openapis.org/oas/v3.0.4.html#operationref-examples)

As references to `operationId` *MAY* NOT be possible (the `operationId` is an optional field in an [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object)), references *MAY* also be made through a relative `operationRef`:

```
links:
  UserRepositories:
    # returns array of '#/components/schemas/repository'
    operationRef: '#/paths/~12.0~1repositories~1%7Busername%7D/get'
    parameters:
      username: $response.body#/username
```

or a URI `operationRef`:

```
links:
  UserRepositories:
    # returns array of '#/components/schemas/repository'
    operationRef: https://na2.gigantic-server.com/#/paths/~12.0~1repositories~1%7Busername%7D/get
    parameters:
      username: $response.body#/username
```

Note that in the use of `operationRef` the *escaped forward-slash* is necessary when using JSON Pointer, and it is necessary to URL-encode `{` and `}` as `%7B` and `%7D`, respectively, when using JSON Pointer as URI fragments.

##### 4.7.20.4 Runtime Expressions

[](https://spec.openapis.org/oas/v3.0.4.html#runtime-expressions)

Runtime expressions allow defining values based on information that will only be available within the HTTP message in an actual API call. This mechanism is used by [Link Objects](https://spec.openapis.org/oas/v3.0.4.html#link-object) and [Callback Objects](https://spec.openapis.org/oas/v3.0.4.html#callback-object).

The runtime expression is defined by the following \[[ABNF](https://spec.openapis.org/oas/v3.0.4.html#bib-abnf "Augmented BNF for Syntax Specifications: ABNF")\] syntax

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
    name = *( CHAR )
    token = 1*tchar
    tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*" / "+" / "-" / "."
          / "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA
```

Here, `json-pointer` is taken from \[[RFC6901](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\], `char` from \[[RFC7159](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7159 "The JavaScript Object Notation (JSON) Data Interchange Format")\] [Section 7](https://datatracker.ietf.org/doc/html/rfc7159#section-7) and `token` from \[[RFC7230](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7230 "Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing")\] [Section 3.2.6](https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.6).

The `name` identifier is case-sensitive, whereas `token` is not.

The table below provides examples of runtime expressions and examples of their use in a value:

##### 4.7.20.5 Examples

[](https://spec.openapis.org/oas/v3.0.4.html#examples-0)

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

#### 4.7.21 Header Object

[](https://spec.openapis.org/oas/v3.0.4.html#header-object)

Describes a single header for [HTTP responses](https://spec.openapis.org/oas/v3.0.4.html#response-headers) and for [individual parts in `multipart` representations](https://spec.openapis.org/oas/v3.0.4.html#encoding-headers); see the relevant [Response Object](https://spec.openapis.org/oas/v3.0.4.html#response-object) and [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) documentation for restrictions on which headers can be described.

The Header Object follows the structure of the [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object), including determining its serialization strategy based on whether `schema` or `content` is present, with the following changes:

1.  `name` *MUST NOT* be specified, it is given in the corresponding `headers` map.
2.  `in` *MUST NOT* be specified, it is implicitly in `header`.
3.  All traits that are affected by the location *MUST* be applicable to a location of `header` (for example, [`style`](https://spec.openapis.org/oas/v3.0.4.html#parameter-style)). This means that `allowEmptyValue` and `allowReserved` *MUST NOT* be used, and `style`, if used, *MUST* be limited to `"simple"`.

##### 4.7.21.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-17)

###### 4.7.21.1.1 Common Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#common-fixed-fields-1)

These fields *MAY* be used with either `content` or `schema`.

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A brief description of the header. This could contain examples of use. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| required | `boolean` | Determines whether this header is mandatory. The default value is `false`. |
| deprecated | `boolean` | Specifies that the header is deprecated and *SHOULD* be transitioned out of usage. Default value is `false`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

###### 4.7.21.1.2 Fixed Fields for use with `schema`

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-for-use-with-schema-0)

For simpler scenarios, a [`schema`](https://spec.openapis.org/oas/v3.0.4.html#header-schema) and [`style`](https://spec.openapis.org/oas/v3.0.4.html#header-style) can describe the structure and syntax of the header. When `example` or `examples` are provided in conjunction with the `schema` field, the example *MUST* follow the prescribed serialization strategy for the header.

Serializing with `schema` is *NOT RECOMMENDED* for headers with parameters (name=value pairs following a `;`) in their values, or where values might have non-URL-safe characters; see [Appendix D](https://spec.openapis.org/oas/v3.0.4.html#appendix-d-serializing-headers-and-cookies) for details.

When `example` or `examples` are provided in conjunction with the `schema` field, the example *SHOULD* match the specified schema and follow the prescribed serialization strategy for the header. The `example` and `examples` fields are mutually exclusive, and if either is present it *SHALL* *override* any `example` in the schema.

| Field Name | Type | Description |
| --- | --- | --- |
| style | `string` | Describes how the header value will be serialized. The default (and only legal value for headers) is `"simple"`. |
| explode | `boolean` | When this is true, header values of type `array` or `object` generate a single header whose value is a comma-separated list of the array items or key-value pairs of the map, see [Style Examples](https://spec.openapis.org/oas/v3.0.4.html#style-examples). For other data types this field has no effect. The default value is `false`. |
| schema | [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) | The schema defining the type used for the header. |
| example | Any | Example of the header’s potential value; see [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples). |
| examples | Map\[ `string`, [Example Object](https://spec.openapis.org/oas/v3.0.4.html#example-object) | [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object)\] | Examples of the header’s potential value; see [Working With Examples](https://spec.openapis.org/oas/v3.0.4.html#working-with-examples). |

See also [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for additional guidance.

###### 4.7.21.1.3 Fixed Fields for use with `content`

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-for-use-with-content-0)

For more complex scenarios, the [`content`](https://spec.openapis.org/oas/v3.0.4.html#header-content) field can define the media type and schema of the header, as well as give examples of its use. Using `content` with a `text/plain` media type is *RECOMMENDED* for headers where the `schema` strategy is not appropriate.

| Field Name | Type | Description |
| --- | --- | --- |
| content | Map\[`string`, [Media Type Object](https://spec.openapis.org/oas/v3.0.4.html#media-type-object)\] | A map containing the representations for the header. The key is the media type and the value describes it. The map *MUST* only contain one entry. |

##### 4.7.21.2 Header Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#header-object-example)

A simple header of type `integer`:

```
"X-Rate-Limit-Limit": {
  "description": "The number of allowed requests in the current period",
  "schema": {
    "type": "integer"
  }
}
```

```
X-Rate-Limit-Limit:
  description: The number of allowed requests in the current period
  schema:
    type: integer
```

Requiring that a strong `ETag` header (with a value starting with `"` rather than `W/`) is present. Note the use of `content`, because using `schema` and `style` would require the `"` to be percent-encoded as `%22`:

```
"ETag": {
  "required": true,
  "content": {
    "text/plain": {
      "schema": {
        "type": "string",
        "pattern": "^\""
      }
    }
  }
}
```

```
ETag:
  required: true
  content:
    text/plain:
      schema:
        type: string
        pattern: ^"
```

#### 4.7.22 Tag Object

[](https://spec.openapis.org/oas/v3.0.4.html#tag-object)

Adds metadata to a single tag that is used by the [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object). It is not mandatory to have a Tag Object per tag defined in the Operation Object instances.

##### 4.7.22.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-18)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the tag. |
| description | `string` | A description for the tag. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object) | Additional external documentation for this tag. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.22.2 Tag Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#tag-object-example)

```
{
  "name": "pet",
  "description": "Pets operations"
}
```

```
name: pet
description: Pets operations
```

#### 4.7.23 Reference Object

[](https://spec.openapis.org/oas/v3.0.4.html#reference-object)

A simple object to allow referencing other components in the OpenAPI Description, internally and externally.

The Reference Object is defined by [JSON Reference](https://spec.openapis.org/oas/v3.0.4.html#bib-json-reference "JSON Reference") and follows the same structure, behavior and rules.

For this specification, reference resolution is accomplished as defined by the JSON Reference specification and not by the JSON Schema specification.

##### 4.7.23.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-19)

| Field Name | Type | Description |
| --- | --- | --- |
| $ref | `string` | ***REQUIRED***. The reference string. |

This object cannot be extended with additional properties, and any properties added *SHALL* be ignored.

##### 4.7.23.2 Reference Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#reference-object-example)

```
{
  "$ref": "#/components/schemas/Pet"
}
```

```
$ref: '#/components/schemas/Pet'
```

##### 4.7.23.3 Relative Schema Document Example

[](https://spec.openapis.org/oas/v3.0.4.html#relative-schema-document-example)

```
{
  "$ref": "Pet.json"
}
```

```
$ref: Pet.yaml
```

##### 4.7.23.4 Relative Documents with Embedded Schema Example

[](https://spec.openapis.org/oas/v3.0.4.html#relative-documents-with-embedded-schema-example)

```
{
  "$ref": "definitions.json#/Pet"
}
```

```
$ref: definitions.yaml#/Pet
```

#### 4.7.24 Schema Object

[](https://spec.openapis.org/oas/v3.0.4.html#schema-object)

The Schema Object allows the definition of input and output data types. These types can be objects, but also primitives and arrays. This object is an extended subset of the [JSON Schema Specification Draft Wright-00](https://spec.openapis.org/oas/v3.0.4.html#bib-json-schema-05 "JSON Schema: A Media Type for Describing JSON Documents. Draft 5").

For more information about the keywords, see [JSON Schema Core](https://spec.openapis.org/oas/v3.0.4.html#bib-json-schema-05 "JSON Schema: A Media Type for Describing JSON Documents. Draft 5") and [JSON Schema Validation](https://spec.openapis.org/oas/v3.0.4.html#bib-json-schema-validation-05 "JSON Schema Validation: A Vocabulary for Structural Validation of JSON. Draft 5"). Unless stated otherwise, the keyword definitions follow those of JSON Schema and do not add any additional semantics.

##### 4.7.24.1 JSON Schema Keywords

[](https://spec.openapis.org/oas/v3.0.4.html#json-schema-keywords)

The following keywords are taken directly from the JSON Schema definition and follow the same specifications:

-   title
-   multipleOf
-   maximum
-   exclusiveMaximum
-   minimum
-   exclusiveMinimum
-   maxLength
-   minLength
-   pattern (This string *SHOULD* be a valid regular expression, according to the [Ecma-262 Edition 5.1 regular expression](https://www.ecma-international.org/ecma-262/5.1/#sec-15.10.1) dialect)
-   maxItems
-   minItems
-   uniqueItems
-   maxProperties
-   minProperties
-   required
-   enum

The following keywords are taken from the JSON Schema definition but their definitions were adjusted to the OpenAPI Specification.

-   type - Value *MUST* be a string. Multiple types via an array are not supported.
-   allOf - Inline or referenced schema *MUST* be of a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema.
-   oneOf - Inline or referenced schema *MUST* be of a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema.
-   anyOf - Inline or referenced schema *MUST* be of a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema.
-   not - Inline or referenced schema *MUST* be of a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema.
-   items - Value *MUST* be an object and not an array. Inline or referenced schema *MUST* be of a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema. `items` *MUST* be present if `type` is `"array"`.
-   properties - Property definitions *MUST* be a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema (inline or referenced).
-   additionalProperties - Value can be boolean or object. Inline or referenced schema *MUST* be of a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) and not a standard JSON Schema. Consistent with JSON Schema, `additionalProperties` defaults to `true`.
-   description - \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation.
-   format - See [Data Type Formats](https://spec.openapis.org/oas/v3.0.4.html#data-type-format) for further details. While relying on JSON Schema’s defined formats, the OAS offers a few additional predefined formats.
-   default - The default value represents what would be assumed by the consumer of the input as the value of the schema if one is not provided. Unlike JSON Schema, the value *MUST* conform to the defined `type` for the Schema Object defined at the same level. For example, if `type` is `"string"`, then `default` can be `"foo"` but cannot be `1`.

Alternatively, any time a Schema Object can be used, a [Reference Object](https://spec.openapis.org/oas/v3.0.4.html#reference-object) can be used in its place. This allows referencing definitions instead of defining them inline.

Additional keywords defined by the JSON Schema specification that are not mentioned here are strictly unsupported.

Other than the JSON Schema subset fields, the following fields *MAY* be used for further schema documentation:

##### 4.7.24.2 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-20)

| Field Name | Type | Description |
| --- | --- | --- |
| nullable | `boolean` | This keyword only takes effect if `type` is explicitly defined within the same Schema Object. A `true` value indicates that both `null` values and values of the type specified by `type` are allowed. Other Schema Object constraints retain their defined behavior, and therefore may disallow the use of `null` as a value. A `false` value leaves the specified or default `type` unmodified. The default value is `false`. |
| discriminator | [Discriminator Object](https://spec.openapis.org/oas/v3.0.4.html#discriminator-object) | Adds support for polymorphism. The discriminator is used to determine which of a set of schemas a payload is expected to satisfy. See [Composition and Inheritance](https://spec.openapis.org/oas/v3.0.4.html#composition-and-inheritance-polymorphism) for more details. |
| readOnly | `boolean` | Relevant only for Schema Object `properties` definitions. Declares the property as “read only”. This means that it *MAY* be sent as part of a response but *SHOULD NOT* be sent as part of the request. If the property is marked as `readOnly` being `true` and is in the `required` list, the `required` will take effect on the response only. A property *MUST NOT* be marked as both `readOnly` and `writeOnly` being `true`. Default value is `false`. |
| writeOnly | `boolean` | Relevant only for Schema Object `properties` definitions. Declares the property as “write only”. Therefore, it *MAY* be sent as part of a request but *SHOULD NOT* be sent as part of the response. If the property is marked as `writeOnly` being `true` and is in the `required` list, the `required` will take effect on the request only. A property *MUST NOT* be marked as both `readOnly` and `writeOnly` being `true`. Default value is `false`. |
| xml | [XML Object](https://spec.openapis.org/oas/v3.0.4.html#xml-object) | This *MAY* be used only on property schemas. It has no effect on root schemas. Adds additional metadata to describe the XML representation of this property. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v3.0.4.html#external-documentation-object) | Additional external documentation for this schema. |
| example | Any | A free-form field to include an example of an instance for this schema. To represent examples that cannot be naturally represented in JSON or YAML, a string value can be used to contain the example with escaping where necessary. |
| deprecated | `boolean` | Specifies that a schema is deprecated and *SHOULD* be transitioned out of usage. Default value is `false`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

###### 4.7.24.2.1 Composition and Inheritance (Polymorphism)

[](https://spec.openapis.org/oas/v3.0.4.html#composition-and-inheritance-polymorphism)

The OpenAPI Specification allows combining and extending model definitions using the `allOf` keyword of JSON Schema, in effect offering model composition. `allOf` takes an array of object definitions that are validated *independently* but together compose a single object.

While composition offers model extensibility, it does not imply a hierarchy between the models. To support polymorphism, the OpenAPI Specification adds the [`discriminator`](https://spec.openapis.org/oas/v3.0.4.html#schema-discriminator) field. When used, the `discriminator` indicates the name of the property that hints which schema definition is expected to validate the structure of the model. As such, the `discriminator` field *MUST* be a required field. There are two ways to define the value of a discriminator for an inheriting instance.

-   Use the schema name.
-   [Override the schema name](https://spec.openapis.org/oas/v3.0.4.html#discriminator-mapping) by overriding the property with a new value. If a new value exists, this takes precedence over the schema name.

###### 4.7.24.2.2 XML Modeling

[](https://spec.openapis.org/oas/v3.0.4.html#xml-modeling)

The [xml](https://spec.openapis.org/oas/v3.0.4.html#schema-xml) field allows extra definitions when translating the JSON definition to XML. The [XML Object](https://spec.openapis.org/oas/v3.0.4.html#xml-object) contains additional information about the available options.

##### 4.7.24.3 Schema Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#schema-object-examples)

###### 4.7.24.3.1 Primitive Example

[](https://spec.openapis.org/oas/v3.0.4.html#primitive-example)

```
{
  "type": "string",
  "format": "email"
}
```

```
type: string
format: email
```

###### 4.7.24.3.2 Simple Model

[](https://spec.openapis.org/oas/v3.0.4.html#simple-model)

```
{
  "type": "object",
  "required": ["name"],
  "properties": {
    "name": {
      "type": "string"
    },
    "address": {
      "$ref": "#/components/schemas/Address"
    },
    "age": {
      "type": "integer",
      "format": "int32",
      "minimum": 0
    }
  }
}
```

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

###### 4.7.24.3.3 Model with Map/Dictionary Properties

[](https://spec.openapis.org/oas/v3.0.4.html#model-with-map-dictionary-properties)

For a simple string to string mapping:

```
{
  "type": "object",
  "additionalProperties": {
    "type": "string"
  }
}
```

```
type: object
additionalProperties:
  type: string
```

For a string to model mapping:

```
{
  "type": "object",
  "additionalProperties": {
    "$ref": "#/components/schemas/ComplexModel"
  }
}
```

```
type: object
additionalProperties:
  $ref: '#/components/schemas/ComplexModel'
```

###### 4.7.24.3.4 Model with Example

[](https://spec.openapis.org/oas/v3.0.4.html#model-with-example)

```
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "format": "int64"
    },
    "name": {
      "type": "string"
    }
  },
  "required": ["name"],
  "example": {
    "name": "Puma",
    "id": 1
  }
}
```

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
example:
  name: Puma
  id: 1
```

###### 4.7.24.3.5 Models with Composition

[](https://spec.openapis.org/oas/v3.0.4.html#models-with-composition)

```
{
  "components": {
    "schemas": {
      "ErrorModel": {
        "type": "object",
        "required": ["message", "code"],
        "properties": {
          "message": {
            "type": "string"
          },
          "code": {
            "type": "integer",
            "minimum": 100,
            "maximum": 600
          }
        }
      },
      "ExtendedErrorModel": {
        "allOf": [
          {
            "$ref": "#/components/schemas/ErrorModel"
          },
          {
            "type": "object",
            "required": ["rootCause"],
            "properties": {
              "rootCause": {
                "type": "string"
              }
            }
          }
        ]
      }
    }
  }
}
```

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

###### 4.7.24.3.6 Models with Polymorphism Support

[](https://spec.openapis.org/oas/v3.0.4.html#models-with-polymorphism-support)

```
{
  "components": {
    "schemas": {
      "Pet": {
        "type": "object",
        "discriminator": {
          "propertyName": "petType"
        },
        "properties": {
          "name": {
            "type": "string"
          },
          "petType": {
            "type": "string"
          }
        },
        "required": ["name", "petType"]
      },
      "Cat": {
        "description": "A representation of a cat. Note that `Cat` will be used as the discriminating value.",
        "allOf": [
          {
            "$ref": "#/components/schemas/Pet"
          },
          {
            "type": "object",
            "properties": {
              "huntingSkill": {
                "type": "string",
                "description": "The measured skill for hunting",
                "default": "lazy",
                "enum": ["clueless", "lazy", "adventurous", "aggressive"]
              }
            },
            "required": ["huntingSkill"]
          }
        ]
      },
      "Dog": {
        "description": "A representation of a dog. Note that `Dog` will be used as the discriminating value.",
        "allOf": [
          {
            "$ref": "#/components/schemas/Pet"
          },
          {
            "type": "object",
            "properties": {
              "packSize": {
                "type": "integer",
                "format": "int32",
                "description": "the size of the pack the dog is from",
                "default": 0,
                "minimum": 0
              }
            },
            "required": ["packSize"]
          }
        ]
      }
    }
  }
}
```

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

#### 4.7.25 Discriminator Object

[](https://spec.openapis.org/oas/v3.0.4.html#discriminator-object)

When request bodies or response payloads may be one of a number of different schemas, a Discriminator Object gives a hint about the expected schema of the document. This hint can be used to aid in serialization, deserialization, and validation. The Discriminator Object does this by implicitly or explicitly associating the possible values of a named property with alternative schemas.

Note that `discriminator` *MUST NOT* change the validation outcome of the schema.

##### 4.7.25.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-21)

| Field Name | Type | Description |
| --- | --- | --- |
| propertyName | `string` | ***REQUIRED***. The name of the property in the payload that will hold the discriminating value. This property *SHOULD* be required in the payload schema, as the behavior when the property is absent is undefined. |
| mapping | Map\[`string`, `string`\] | An object to hold mappings between payload values and schema names or URI references. |

##### 4.7.25.2 Conditions for Using the Discriminator Object

[](https://spec.openapis.org/oas/v3.0.4.html#conditions-for-using-the-discriminator-object)

The Discriminator Object is legal only when using one of the composite keywords `oneOf`, `anyOf`, `allOf`.

In both the `oneOf` and `anyOf` use cases, where those keywords are adjacent to `discriminator`, all possible schemas *MUST* be listed explicitly.

To avoid redundancy, the discriminator *MAY* be added to a parent schema definition, and all schemas building on the parent schema via an `allOf` construct may be used as an alternate schema. It is implementation-defined as to whether all named [Schema Objects](https://spec.openapis.org/oas/v3.0.4.html#schema-object) under the [Components Object](https://spec.openapis.org/oas/v3.0.4.html#components-object), or only those that are otherwise directly referenced are searched for `allOf` references to the parent schema. However, it is *RECOMMENDED* to search all named schemas in the Components Object because it is common with the `allOf` usage for other parts of the API to only directly reference the parent schema.

The `allOf` form of `discriminator` is *only* useful for non-validation use cases; validation with the parent schema with this form of `discriminator` *does not* perform a search for child schemas or use them in validation in any way. This is because `discriminator` cannot change the validation outcome, and no standard JSON Schema keyword connects the parent schema to the child schemas.

The behavior of any configuration of `oneOf`, `anyOf`, `allOf` and `discriminator` that is not described above is undefined.

##### 4.7.25.3 Options for Mapping Values to Schemas

[](https://spec.openapis.org/oas/v3.0.4.html#options-for-mapping-values-to-schemas)

The value of the property named in `propertyName` is used as the name of the associated schema under the [Components Object](https://spec.openapis.org/oas/v3.0.4.html#components-object), *unless* a `mapping` is present for that value. The `mapping` entry maps a specific property value to either a different schema component name, or to a schema identified by a URI. When using implicit or explicit schema component names, inline `oneOf` or `anyOf` subschemas are not considered. The behavior of a `mapping` value that is both a valid schema name and a valid relative URI reference is implementation-defined, but it is *RECOMMENDED* that it be treated as a schema name. To ensure that an ambiguous value (e.g. `"foo"`) is treated as a relative URI reference by all implementations, authors *MUST* prefix it with the `"."` path segment (e.g. `"./foo"`).

Mapping keys *MUST* be string values, but tooling *MAY* convert response values to strings for comparison. However, the exact nature of such conversions are implementation-defined.

##### 4.7.25.4 Examples

[](https://spec.openapis.org/oas/v3.0.4.html#examples-1)

For these examples, assume all schemas are in the [entry document](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-structure) of the OAD; for handling of `discriminator` in referenced documents see [Resolving Implicit Connections](https://spec.openapis.org/oas/v3.0.4.html#resolving-implicit-connections).

In OAS 3.0, a response payload *MAY* be described to be exactly one of any number of types:

```
MyResponseType:
  oneOf:
    - $ref: '#/components/schemas/Cat'
    - $ref: '#/components/schemas/Dog'
    - $ref: '#/components/schemas/Lizard'
```

which means the payload **MUST**, by validation, match exactly one of the schemas described by `Cat`, `Dog`, or `Lizard`. Deserialization of a `oneOf` can be a costly operation, as it requires determining which schema matches the payload and thus should be used in deserialization. This problem also exists for `anyOf` schemas. A `discriminator` *MAY* be used as a “hint” to improve the efficiency of selection of the matching schema. The `discriminator` field cannot change the validation result of the `oneOf`, it can only help make the deserialization more efficient and provide better error messaging. We can specify the exact field that tells us which schema is expected to match the instance:

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

In scenarios where the value of the `discriminator` field does not match the schema name or implicit mapping is not possible, an optional `mapping` definition *MAY* be used:

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

#### 4.7.26 XML Object

[](https://spec.openapis.org/oas/v3.0.4.html#xml-object)

A metadata object that allows for more fine-tuned XML model definitions.

When using arrays, XML element names are *not* inferred (for singular/plural forms) and the `name` field *SHOULD* be used to add that information. See examples for expected behavior.

##### 4.7.26.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-22)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | Replaces the name of the element/attribute used for the described schema property. When defined within `items`, it will affect the name of the individual XML elements within the list. When defined alongside `type` being `"array"` (outside the `items`), it will affect the wrapping element if and only if `wrapped` is `true`. If `wrapped` is `false`, it will be ignored. |
| namespace | `string` | The URI of the namespace definition. Value *MUST* be in the form of a non-relative URI. |
| prefix | `string` | The prefix to be used for the [name](https://spec.openapis.org/oas/v3.0.4.html#xml-name). |
| attribute | `boolean` | Declares whether the property definition translates to an attribute instead of an element. Default value is `false`. |
| wrapped | `boolean` | *MAY* be used only for an array definition. Signifies whether the array is wrapped (for example, `<books><book/><book/></books>`) or unwrapped (`<book/><book/>`). Default value is `false`. The definition takes effect only when defined alongside `type` being `"array"` (outside the `items`). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

The `namespace` field is intended to match the syntax of [XML namespaces](https://spec.openapis.org/oas/v3.0.4.html#bib-xml-names11 "Namespaces in XML 1.1 (Second Edition)"), although there are a few caveats:

-   Version 3.0.3 and earlier of this specification erroneously used the term “absolute URI” instead of “non-relative URI”, so authors using namespaces that include a fragment should check tooling support carefully.
-   XML allows but discourages relative URI-references, while this specification outright forbids them.
-   XML 1.1 allows IRIs (\[[RFC3987](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3987 "Internationalized Resource Identifiers (IRIs)")\]) as namespaces, and specifies that namespaces are compared without any encoding or decoding, which means that IRIs encoded to meet this specification’s URI syntax requirement cannot be compared to IRIs as-is.

##### 4.7.26.2 XML Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#xml-object-examples)

Each of the following examples represent the value of the `properties` keyword in a [Schema Object](https://spec.openapis.org/oas/v3.0.4.html#schema-object) that is omitted for brevity. The JSON and YAML representations of the `properties` value are followed by an example XML representation produced for the single property shown.

###### 4.7.26.2.1 No XML Element

[](https://spec.openapis.org/oas/v3.0.4.html#no-xml-element)

Basic string property:

```
{
  "animals": {
    "type": "string"
  }
}
```

```
animals:
  type: string
```

```
<animals>...</animals>
```

Basic string array property ([`wrapped`](https://spec.openapis.org/oas/v3.0.4.html#xml-wrapped) is `false` by default):

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string"
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
```

```
<animals>...</animals>
<animals>...</animals>
<animals>...</animals>
```

###### 4.7.26.2.2 XML Name Replacement

[](https://spec.openapis.org/oas/v3.0.4.html#xml-name-replacement)

```
{
  "animals": {
    "type": "string",
    "xml": {
      "name": "animal"
    }
  }
}
```

```
animals:
  type: string
  xml:
    name: animal
```

```
<animal>...</animal>
```

###### 4.7.26.2.3 XML Attribute, Prefix and Namespace

[](https://spec.openapis.org/oas/v3.0.4.html#xml-attribute-prefix-and-namespace)

In this example, a full model definition is shown.

```
{
  "Person": {
    "type": "object",
    "properties": {
      "id": {
        "type": "integer",
        "format": "int32",
        "xml": {
          "attribute": true
        }
      },
      "name": {
        "type": "string",
        "xml": {
          "namespace": "https://example.com/schema/sample",
          "prefix": "sample"
        }
      }
    }
  }
}
```

```
Person:
  type: object
  properties:
    id:
      type: integer
      format: int32
      xml:
        attribute: true
    name:
      type: string
      xml:
        namespace: https://example.com/schema/sample
        prefix: sample
```

```
<Person id="123">
    <sample:name xmlns:sample="https://example.com/schema/sample">example</sample:name>
</Person>
```

###### 4.7.26.2.4 XML Arrays

[](https://spec.openapis.org/oas/v3.0.4.html#xml-arrays)

Changing the element names:

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string",
      "xml": {
        "name": "animal"
      }
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
    xml:
      name: animal
```

```
<animal>value</animal>
<animal>value</animal>
```

The external `name` field has no effect on the XML:

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string",
      "xml": {
        "name": "animal"
      }
    },
    "xml": {
      "name": "aliens"
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
    xml:
      name: animal
  xml:
    name: aliens
```

```
<animal>value</animal>
<animal>value</animal>
```

Even when the array is wrapped, if a name is not explicitly defined, the same name will be used both internally and externally:

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string"
    },
    "xml": {
      "wrapped": true
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
  xml:
    wrapped: true
```

```
<animals>
  <animals>value</animals>
  <animals>value</animals>
</animals>
```

To overcome the naming problem in the example above, the following definition can be used:

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string",
      "xml": {
        "name": "animal"
      }
    },
    "xml": {
      "wrapped": true
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
    xml:
      name: animal
  xml:
    wrapped: true
```

```
<animals>
  <animal>value</animal>
  <animal>value</animal>
</animals>
```

Affecting both internal and external names:

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string",
      "xml": {
        "name": "animal"
      }
    },
    "xml": {
      "name": "aliens",
      "wrapped": true
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
    xml:
      name: animal
  xml:
    name: aliens
    wrapped: true
```

```
<aliens>
  <animal>value</animal>
  <animal>value</animal>
</aliens>
```

If we change the external element but not the internal ones:

```
{
  "animals": {
    "type": "array",
    "items": {
      "type": "string"
    },
    "xml": {
      "name": "aliens",
      "wrapped": true
    }
  }
}
```

```
animals:
  type: array
  items:
    type: string
  xml:
    name: aliens
    wrapped: true
```

```
<aliens>
  <aliens>value</aliens>
  <aliens>value</aliens>
</aliens>
```

#### 4.7.27 Security Scheme Object

[](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object-0)

Defines a security scheme that can be used by the operations.

Supported schemes are HTTP authentication, an API key (either as a header, a cookie parameter, or as a query parameter), OAuth2’s common flows (implicit, password, client credentials, and authorization code) as defined in \[[RFC6749](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6749 "The OAuth 2.0 Authorization Framework")\], and \[[OpenID-Connect-Core](https://spec.openapis.org/oas/v3.0.4.html#bib-openid-connect-core "OpenID Connect Core 1.0 incorporating errata set 2")\]. Please note that as of 2020, the implicit flow is about to be deprecated by [OAuth 2.0 Security Best Current Practice](https://tools.ietf.org/html/draft-ietf-oauth-security-topics). Recommended for most use cases is Authorization Code Grant flow with PKCE.

##### 4.7.27.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-23)

| Field Name | Type | Applies To | Description |
| --- | --- | --- | --- |
| type | `string` | Any | ***REQUIRED***. The type of the security scheme. Valid values are `"apiKey"`, `"http"`, `"oauth2"`, `"openIdConnect"`. |
| description | `string` | Any | A description for security scheme. \[[CommonMark](https://spec.openapis.org/oas/v3.0.4.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| name | `string` | `apiKey` | ***REQUIRED***. The name of the header, query or cookie parameter to be used. |
| in | `string` | `apiKey` | ***REQUIRED***. The location of the API key. Valid values are `"query"`, `"header"`, or `"cookie"`. |
| scheme | `string` | `http` | ***REQUIRED***. The name of the HTTP Authentication scheme to be used in the Authorization header as defined in \[[RFC7235](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7235 "Hypertext Transfer Protocol (HTTP/1.1): Authentication")\] [Section 5.1](https://datatracker.ietf.org/doc/html/rfc7235#section-5.1). The values used *SHOULD* be registered in the [IANA Authentication Scheme registry](https://spec.openapis.org/oas/v3.0.4.html#bib-iana-http-authschemes "Hypertext Transfer Protocol (HTTP) Authentication Scheme Registry"). The value is case-insensitive, as defined in \[[RFC7235](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7235 "Hypertext Transfer Protocol (HTTP/1.1): Authentication")\] [Section 2.1](https://datatracker.ietf.org/doc/html/rfc7235#section-2.1). |
| bearerFormat | `string` | `http` (`"bearer"`) | A hint to the client to identify how the bearer token is formatted. Bearer tokens are usually generated by an authorization server, so this information is primarily for documentation purposes. |
| flows | [OAuth Flows Object](https://spec.openapis.org/oas/v3.0.4.html#oauth-flows-object) | `oauth2` | ***REQUIRED***. An object containing configuration information for the flow types supported. |
| openIdConnectUrl | `string` | `openIdConnect` | ***REQUIRED***. [Well-known URL](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig) to discover the \[[OpenID-Connect-Discovery](https://spec.openapis.org/oas/v3.0.4.html#bib-openid-connect-discovery "OpenID Connect Discovery 1.0 incorporating errata set 2")\] [provider metadata](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.27.2 Security Scheme Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object-examples)

###### 4.7.27.2.1 Basic Authentication Example

[](https://spec.openapis.org/oas/v3.0.4.html#basic-authentication-example)

```
{
  "type": "http",
  "scheme": "basic"
}
```

```
type: http
scheme: basic
```

###### 4.7.27.2.2 API Key Example

[](https://spec.openapis.org/oas/v3.0.4.html#api-key-example)

```
{
  "type": "apiKey",
  "name": "api-key",
  "in": "header"
}
```

```
type: apiKey
name: api-key
in: header
```

###### 4.7.27.2.3 JWT Bearer Example

[](https://spec.openapis.org/oas/v3.0.4.html#jwt-bearer-example)

```
{
  "type": "http",
  "scheme": "bearer",
  "bearerFormat": "JWT"
}
```

```
type: http
scheme: bearer
bearerFormat: JWT
```

###### 4.7.27.2.4 Implicit OAuth2 Example

[](https://spec.openapis.org/oas/v3.0.4.html#implicit-oauth2-example)

```
{
  "type": "oauth2",
  "flows": {
    "implicit": {
      "authorizationUrl": "https://example.com/api/oauth/dialog",
      "scopes": {
        "write:pets": "modify pets in your account",
        "read:pets": "read your pets"
      }
    }
  }
}
```

```
type: oauth2
flows:
  implicit:
    authorizationUrl: https://example.com/api/oauth/dialog
    scopes:
      write:pets: modify pets in your account
      read:pets: read your pets
```

#### 4.7.28 OAuth Flows Object

[](https://spec.openapis.org/oas/v3.0.4.html#oauth-flows-object)

Allows configuration of the supported OAuth Flows.

##### 4.7.28.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-24)

| Field Name | Type | Description |
| --- | --- | --- |
| implicit | [OAuth Flow Object](https://spec.openapis.org/oas/v3.0.4.html#oauth-flow-object) | Configuration for the OAuth Implicit flow |
| password | [OAuth Flow Object](https://spec.openapis.org/oas/v3.0.4.html#oauth-flow-object) | Configuration for the OAuth Resource Owner Password flow |
| clientCredentials | [OAuth Flow Object](https://spec.openapis.org/oas/v3.0.4.html#oauth-flow-object) | Configuration for the OAuth Client Credentials flow. Previously called `application` in OpenAPI 2.0. |
| authorizationCode | [OAuth Flow Object](https://spec.openapis.org/oas/v3.0.4.html#oauth-flow-object) | Configuration for the OAuth Authorization Code flow. Previously called `accessCode` in OpenAPI 2.0. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

#### 4.7.29 OAuth Flow Object

[](https://spec.openapis.org/oas/v3.0.4.html#oauth-flow-object)

Configuration details for a supported OAuth Flow

##### 4.7.29.1 Fixed Fields

[](https://spec.openapis.org/oas/v3.0.4.html#fixed-fields-25)

| Field Name | Type | Applies To | Description |
| --- | --- | --- | --- |
| authorizationUrl | `string` | `oauth2` (`"implicit"`, `"authorizationCode"`) | ***REQUIRED***. The authorization URL to be used for this flow. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| tokenUrl | `string` | `oauth2` (`"password"`, `"clientCredentials"`, `"authorizationCode"`) | ***REQUIRED***. The token URL to be used for this flow. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| refreshUrl | `string` | `oauth2` | The URL to be used for obtaining refresh tokens. This *MUST* be in the form of a URL. The OAuth2 standard requires the use of TLS. |
| scopes | Map\[`string`, `string`\] | `oauth2` | ***REQUIRED***. The available scopes for the OAuth2 security scheme. A map between the scope name and a short description for it. The map *MAY* be empty. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions).

##### 4.7.29.2 OAuth Flow Object Example

[](https://spec.openapis.org/oas/v3.0.4.html#oauth-flow-object-example)

```
{
  "type": "oauth2",
  "flows": {
    "implicit": {
      "authorizationUrl": "https://example.com/api/oauth/dialog",
      "scopes": {
        "write:pets": "modify pets in your account",
        "read:pets": "read your pets"
      }
    },
    "authorizationCode": {
      "authorizationUrl": "https://example.com/api/oauth/dialog",
      "tokenUrl": "https://example.com/api/oauth/token",
      "scopes": {
        "write:pets": "modify pets in your account",
        "read:pets": "read your pets"
      }
    }
  }
}
```

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

#### 4.7.30 Security Requirement Object

[](https://spec.openapis.org/oas/v3.0.4.html#security-requirement-object)

Lists the required security schemes to execute this operation. The name used for each property *MUST* correspond to a security scheme declared in the [Security Schemes](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object) under the [Components Object](https://spec.openapis.org/oas/v3.0.4.html#components-object).

A Security Requirement Object *MAY* refer to multiple security schemes in which case all schemes *MUST* be satisfied for a request to be authorized. This enables support for scenarios where multiple query parameters or HTTP headers are required to convey security information.

When the `security` field is defined on the [OpenAPI Object](https://spec.openapis.org/oas/v3.0.4.html#openapi-object) or [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object) and contains multiple Security Requirement Objects, only one of the entries in the list needs to be satisfied to authorize the request. This enables support for scenarios where the API allows multiple, independent security schemes.

An empty Security Requirement Object (`{}`) indicates anonymous access is supported.

##### 4.7.30.1 Patterned Fields

[](https://spec.openapis.org/oas/v3.0.4.html#patterned-fields-2)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | \[`string`\] | Each name *MUST* correspond to a security scheme which is declared in the [Security Schemes](https://spec.openapis.org/oas/v3.0.4.html#security-scheme-object) under the [Components Object](https://spec.openapis.org/oas/v3.0.4.html#components-object). If the security scheme is of type `"oauth2"` or `"openIdConnect"`, then the value is a list of scope names required for the execution, and the list *MAY* be empty if authorization does not require a specified scope. For other security scheme types, the array *MUST* be empty. |

##### 4.7.30.2 Security Requirement Object Examples

[](https://spec.openapis.org/oas/v3.0.4.html#security-requirement-object-examples)

See also [Appendix F: Resolving Security Requirements in a Referenced Document](https://spec.openapis.org/oas/v3.0.4.html#appendix-f-resolving-security-requirements-in-a-referenced-document) for an example using Security Requirement Objects in multi-document OpenAPI Descriptions.

###### 4.7.30.2.1 Non-OAuth2 Security Requirement

[](https://spec.openapis.org/oas/v3.0.4.html#non-oauth2-security-requirement)

```
{
  "api_key": []
}
```

```
api_key: []
```

###### 4.7.30.2.2 OAuth2 Security Requirement

[](https://spec.openapis.org/oas/v3.0.4.html#oauth2-security-requirement)

```
{
  "petstore_auth": ["write:pets", "read:pets"]
}
```

```
petstore_auth:
  - write:pets
  - read:pets
```

###### 4.7.30.2.3 Optional OAuth2 Security

[](https://spec.openapis.org/oas/v3.0.4.html#optional-oauth2-security)

Optional OAuth2 security as would be defined in an [OpenAPI Object](https://spec.openapis.org/oas/v3.0.4.html#openapi-object) or an [Operation Object](https://spec.openapis.org/oas/v3.0.4.html#operation-object):

```
{
  "security": [
    {},
    {
      "petstore_auth": ["write:pets", "read:pets"]
    }
  ]
}
```

```
security:
  - {}
  - petstore_auth:
      - write:pets
      - read:pets
```

### 4.8 Specification Extensions

[](https://spec.openapis.org/oas/v3.0.4.html#specification-extensions)

While the OpenAPI Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points.

The extensions properties are implemented as patterned fields that are always prefixed by `x-`.

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the OpenAPI Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be any valid JSON value (`null`, a primitive, an array, or an object.) |

The OpenAPI Initiative maintains several [extension registries](https://spec.openapis.org/oas/v3.0.4.html#bib-openapi-registry "OpenAPI Initiative Registry"), including registries for [individual extension keywords](https://spec.openapis.org/registry/extension/) and [extension keyword namespaces](https://spec.openapis.org/registry/namespace/).

Extensions are one of the best ways to prove the viability of proposed additions to the specification. It is therefore *RECOMMENDED* that implementations be designed for extensibility to support community experimentation.

Support for any one extension is *OPTIONAL*, and support for one extension does not imply support for others.

### 4.9 Security Filtering

[](https://spec.openapis.org/oas/v3.0.4.html#security-filtering)

Some objects in the OpenAPI Specification *MAY* be declared and remain empty, or be completely removed, even though they are inherently the core of the API documentation.

The reasoning is to allow an additional layer of access control over the documentation. While not part of the specification itself, certain libraries *MAY* choose to allow access to parts of the documentation based on some form of authentication/authorization.

Two examples of this:

1.  The [Paths Object](https://spec.openapis.org/oas/v3.0.4.html#paths-object) *MAY* be present but empty. It may be counterintuitive, but this may tell the viewer that they got to the right place, but can’t access any documentation. They would still have access to at least the [Info Object](https://spec.openapis.org/oas/v3.0.4.html#info-object) which may contain additional information regarding authentication.
2.  The [Path Item Object](https://spec.openapis.org/oas/v3.0.4.html#path-item-object) *MAY* be empty. In this case, the viewer will be aware that the path exists, but will not be able to see any of its operations or parameters. This is different from hiding the path itself from the [Paths Object](https://spec.openapis.org/oas/v3.0.4.html#paths-object), because the user will be aware of its existence. This allows the documentation provider to finely control what the viewer can see.

## 5\. Security Considerations

[](https://spec.openapis.org/oas/v3.0.4.html#security-considerations)

### 5.1 OpenAPI Description Formats

[](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-formats)

OpenAPI Descriptions use a combination of JSON, YAML, and JSON Schema, and therefore share their security considerations:

-   [JSON](https://www.iana.org/assignments/media-types/application/json)
-   [YAML](https://www.iana.org/assignments/media-types/application/yaml)
-   [JSON Schema Core](https://tools.ietf.org/html/draft-wright-json-schema-00#section-10)
-   [JSON Schema Validation](https://tools.ietf.org/html/draft-wright-json-schema-validation-00#section-8)

### 5.2 Tooling and Usage Scenarios

[](https://spec.openapis.org/oas/v3.0.4.html#tooling-and-usage-scenarios)

In addition, OpenAPI Descriptions are processed by a wide variety of tooling for numerous different purposes, such as client code generation, documentation generation, server side routing, and API testing. OpenAPI Description authors must consider the risks of the scenarios where the OpenAPI Description may be used.

### 5.3 Security Schemes

[](https://spec.openapis.org/oas/v3.0.4.html#security-schemes)

An OpenAPI Description describes the security schemes used to protect the resources it defines. The security schemes available offer varying degrees of protection. Factors such as the sensitivity of the data and the potential impact of a security breach should guide the selection of security schemes for the API resources. Some security schemes, such as basic auth and OAuth Implicit flow, are supported for compatibility with existing APIs. However, their inclusion in OpenAPI does not constitute an endorsement of their use, particularly for highly sensitive data or operations.

### 5.4 Handling External Resources

[](https://spec.openapis.org/oas/v3.0.4.html#handling-external-resources)

OpenAPI Descriptions may contain references to external resources that may be dereferenced automatically by consuming tools. External resources may be hosted on different domains that may be untrusted.

### 5.5 Handling Reference Cycles

[](https://spec.openapis.org/oas/v3.0.4.html#handling-reference-cycles)

References in an OpenAPI Description may cause a cycle. Tooling must detect and handle cycles to prevent resource exhaustion.

### 5.6 Markdown and HTML Sanitization

[](https://spec.openapis.org/oas/v3.0.4.html#markdown-and-html-sanitization)

Certain fields allow the use of Markdown which can contain HTML including script. It is the responsibility of tooling to appropriately sanitize the Markdown.

## A. Appendix A: Revision History

[](https://spec.openapis.org/oas/v3.0.4.html#appendix-a-revision-history)

| Version | Date | Notes |
| --- | --- | --- |
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

[](https://spec.openapis.org/oas/v3.0.4.html#appendix-b-data-type-conversion)

Serializing typed data to plain text, which can occur in `text/plain` message bodies or `multipart` parts, as well as in the `application/x-www-form-urlencoded` format in either URL query strings or message bodies, involves significant implementation- or application-defined behavior.

[Schema Objects](https://spec.openapis.org/oas/v3.0.4.html#schema-object) validate data based on the [JSON Schema data model](https://tools.ietf.org/html/draft-wright-json-schema-00#section-4.2), which only recognizes four primitive data types: strings (which are [only broadly interoperable as UTF-8](https://tools.ietf.org/html/rfc7159#section-8.1)), numbers, booleans, and `null`. Notably, integers are not a distinct type from other numbers, with `type: "integer"` being a convenience defined mathematically, rather than based on the presence or absence of a decimal point in any string representation.

The [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object), [Header Object](https://spec.openapis.org/oas/v3.0.4.html#header-object), and [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) offer features to control how to arrange values from array or object types. They can also be used to control how strings are further encoded to avoid reserved or illegal characters. However, there is no general-purpose specification for converting schema-validated non-UTF-8 primitive data types (or entire arrays or objects) to strings.

Two cases do offer standards-based guidance:

-   \[[RFC3987](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3987 "Internationalized Resource Identifiers (IRIs)")\] [Section 3.1](https://datatracker.ietf.org/doc/html/rfc3987#section-3.1) provides guidance for converting non-Unicode strings to UTF-8, particularly in the context of URIs (and by extension, the form media types which use the same encoding rules)
-   \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] [Section 2.3](https://datatracker.ietf.org/doc/html/rfc6570#section-2.3) specifies which values, including but not limited to `null`, are considered *undefined* and therefore treated specially in the expansion process when serializing based on that specification

Implementations of RFC6570 often have their own conventions for converting non-string values, but these are implementation-specific and not defined by the RFC itself. This is one reason for the OpenAPI Specification to leave these conversions as implementation-defined: It allows using RFC6570 implementations regardless of how they choose to perform the conversions.

To control the serialization of numbers, booleans, and `null` (or other values RFC6570 deems to be undefined) more precisely, schemas can be defined as `type: "string"` and constrained using `pattern`, `enum`, `format`, and other keywords to communicate how applications must pre-convert their data prior to schema validation. The resulting strings would not require any further type conversion.

The `format` keyword can assist in serialization. Some formats (such as `date-time`) are unambiguous, while others (such as [`decimal`](https://spec.openapis.org/registry/format/decimal.html) in the [Format Registry](https://spec.openapis.org/registry/format/)) are less clear. However, care must be taken with `format` to ensure that the specific formats are supported by all relevant tools as unrecognized formats are ignored.

Requiring input as pre-formatted, schema-validated strings also improves round-trip interoperability as not all programming languages and environments support the same data types.

## C. Appendix C: Using RFC6570-Based Serialization

[](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization)

Serialization is defined in terms of \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] URI Templates in three scenarios:

| Object | Condition |
| --- | --- |
| [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) | When `schema` is present |
| [Header Object](https://spec.openapis.org/oas/v3.0.4.html#header-object) | When `schema` is present |
| [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) | When encoding for `application/x-www-form-urlencoded` and any of `style`, `explode`, or `allowReserved` are used |

Implementations of this specification *MAY* use an implementation of RFC6570 to perform variable expansion, however, some caveats apply.

Note that when using `style: "form"` RFC6570 expansion to produce an `application/x-www-form-urlencoded` HTTP message body, it is necessary to remove the `?` prefix that is produced to satisfy the URI query string syntax.

Note also that not all RFC6570 implementations support all four levels of operators, all of which are needed to fully support the OpenAPI Specification’s usage. Using an implementation with a lower level of support will require additional manual construction of URI Templates to work around the limitations.

### C.1 Equivalences Between Fields and RFC6570 Operators

[](https://spec.openapis.org/oas/v3.0.4.html#equivalences-between-fields-and-rfc6570-operators)

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

[](https://spec.openapis.org/oas/v3.0.4.html#delimiters-in-parameter-values)

Delimiters used by RFC6570 expansion, such as the `,` used to join arrays or object values with `style: "simple"`, are all automatically percent-encoded as long as `allowReserved` is `false`. Note that since RFC6570 does not define a way to parse variables based on a URI Template, users must take care to first split values by delimiter before percent-decoding values that might contain the delimiter character.

When `allowReserved` is `true`, both percent-encoding (prior to joining values with a delimiter) and percent-decoding (after splitting on the delimiter) must be done manually at the correct time.

See [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for additional guidance on handling delimiters for `style` values with no RFC6570 equivalent that already need to be percent-encoded when used as delimiters.

### C.3 Non-RFC6570 Field Values and Combinations

[](https://spec.openapis.org/oas/v3.0.4.html#non-rfc6570-field-values-and-combinations)

Configurations with no direct \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] equivalent *SHOULD* also be handled according to RFC6570. Implementations *MAY* create a properly delimited URI Template with variables for individual names and values using RFC6570 regular or reserved expansion (based on `allowReserved`).

This includes:

-   the styles `pipeDelimited`, `spaceDelimited`, and `deepObject`, which have no equivalents at all
-   the combination of the style `form` with `allowReserved: true`, which is not allowed because only one prefix operator can be used at a time
-   any parameter name that is not a legal RFC6570 variable name

The Parameter Object’s `name` field has a much more permissive syntax than RFC6570 [variable name syntax](https://tools.ietf.org/html/rfc6570#section-2.3). A parameter name that includes characters outside of the allowed RFC6570 variable character set *MUST* be percent-encoded before it can be used in a URI Template.

### C.4 Examples

[](https://spec.openapis.org/oas/v3.0.4.html#examples-2)

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

[](https://spec.openapis.org/oas/v3.0.4.html#rfc6570-equivalent-expansion)

This array of Parameter Objects uses regular `style: "form"` expansion, fully supported by \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\]:

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

[](https://spec.openapis.org/oas/v3.0.4.html#expansion-with-non-rfc6570-supported-options)

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

We’ll also need to pre-process the values for `formulas` because while `/` and most other reserved characters are allowed in the query string by RFC3986, `[`, `]`, and `#` [are not](https://tools.ietf.org/html/rfc3986#appendix-A), and `&`, `=`, and `+` all have [special behavior](https://tools.ietf.org/html/rfc1866#section-8.2.1) in the `application/x-www-form-urlencoded` format, which is what we are using in the query string.

Setting `allowReserved: true` does *not* make reserved characters that are not allowed in URIs allowed, it just allows them to be *passed through expansion unchanged.* Therefore, any tooling still needs to percent-encode those characters because reserved expansion will not do it, but it *will* leave the percent-encoded triples unchanged. See also [Appendix E](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types) for further guidance on percent-encoding and form media types, including guidance on handling the delimiter characters for `spaceDelimited`, `pipeDelimited`, and `deepObject` in parameter names and values.

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

[](https://spec.openapis.org/oas/v3.0.4.html#undefined-values-and-manual-uri-template-construction)

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

[](https://spec.openapis.org/oas/v3.0.4.html#illegal-variable-names-as-parameter-names)

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

[](https://spec.openapis.org/oas/v3.0.4.html#appendix-d-serializing-headers-and-cookies)

\[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\]'s percent-encoding behavior is not always appropriate for `in: "header"` and `in: "cookie"` parameters. In many cases, it is more appropriate to use `content` with a media type such as `text/plain` and require the application to assemble the correct string.

For both \[[RFC6265](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6265 "HTTP State Management Mechanism")\] cookies and HTTP headers using the \[[RFC8941](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc8941 "Structured Field Values for HTTP")\] structured fields syntax, non-ASCII content is handled using base64 encoding (`format: "byte"`). Note that the standard base64-encoding alphabet includes non-URL-safe characters that are percent-encoded by RFC6570 expansion; serializing values through both encodings is *NOT RECOMMENDED*.

Most HTTP headers predate the structured field syntax, and a comprehensive assessment of their syntax and encoding rules is well beyond the scope of this specification. While \[[RFC8187](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc8187 "Indicating Character Encoding and Language for HTTP Header Field Parameters")\] recommends percent-encoding HTTP (header or trailer) field parameters, these parameters appear after a `;` character. With `style: "simple"`, that delimiter would itself be percent-encoded, violating the general HTTP field syntax.

Using `style: "form"` with `in: "cookie"` is ambiguous for a single value, and incorrect for multiple values. This is true whether the multiple values are the result of using `explode: true` or not.

This style is specified to be equivalent to RFC6570 form expansion which includes the `?` character (see [Appendix C](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for more details), which is not part of the cookie syntax. However, examples of this style in past versions of this specification have not included the `?` prefix, suggesting that the comparison is not exact. Because implementations that rely on an RFC6570 implementation and those that perform custom serialization based on the style example will produce different results, it is implementation-defined as to which of the two results is correct.

For multiple values, `style: "form"` is always incorrect as name=value pairs in cookies are delimited by `;` (a semicolon followed by a space character) rather than `&`.

## E. Appendix E: Percent-Encoding and Form Media Types

[](https://spec.openapis.org/oas/v3.0.4.html#appendix-e-percent-encoding-and-form-media-types)

***NOTE:** In this section, the `application/x-www-form-urlencoded` and `multipart/form-data` media types are abbreviated as `form-urlencoded` and `form-data`, respectively, for readability.*

Percent-encoding is used in URIs and media types that derive their syntax from URIs. This process is concerned with three sets of characters, the names of which vary among specifications but are defined as follows for the purposes of this section:

-   *unreserved* characters do not need to be percent-encoded; while it is safe to percent-encode them, doing so produces a URI that is [not normalized](https://tools.ietf.org/html/rfc3986#section-6.2.2.2)
-   *reserved* characters either have special behavior in the URI syntax (such as delimiting components) or are reserved for other specifications that need to define special behavior (e.g. `form-urlencoded` defines special behavior for `=`, `&`, and `+`)
-   *unsafe* characters are known to cause problems when parsing URIs in certain environments

Unless otherwise specified, this section uses RFC3986’s definition of [reserved](https://tools.ietf.org/html/rfc3986#section-2.2) and [unreserved](https://tools.ietf.org/html/rfc3986#section-2.3), and defines the unsafe set as all characters not included in either of those sets.

### E.1 Percent-Encoding and `form-urlencoded`

[](https://spec.openapis.org/oas/v3.0.4.html#percent-encoding-and-form-urlencoded)

Each URI component (such as the query string) considers some of the reserved characters to be unsafe, either because they serve as delimiters between the components (e.g. `#`), or (in the case of `[` and `]`) were historically considered globally unsafe but were later given reserved status for limited purposes.

Reserved characters with no special meaning defined within a component can be left un-percent encoded. However, other specifications can define special meanings, requiring percent-encoding for those characters outside of the additional special meanings.

The `form-urlencoded` media type defines special meanings for `=` and `&` as delimiters, and `+` as the replacement for the space character (instead of its percent-encoded form of `%20`). This means that while these three characters are reserved-but-allowed in query strings by RFC3986, they must be percent-encoded in `form-urlencoded` query strings except when used for their `form-urlencoded` purposes; see [Appendix C](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for an example of handling `+` in form values.

### E.2 Percent-Encoding and `form-data`

[](https://spec.openapis.org/oas/v3.0.4.html#percent-encoding-and-form-data)

\[[RFC7578](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc7578 "Returning Values from Forms: multipart/form-data")\] [Section 2](https://datatracker.ietf.org/doc/html/rfc7578#section-2) suggests RFC3986-based percent-encoding as a mechanism to keep text-based per-part header data such as file names within the ASCII character set. This suggestion was not part of older (pre-2015) specifications for `form-data`, so care must be taken to ensure interoperability.

The `form-data` media type allows arbitrary text or binary data in its parts, so percent-encoding is not needed and is likely to cause interoperability problems unless the `Content-Type` of the part is defined to require it.

### E.3 Generating and Validating URIs and `form-urlencoded` Strings

[](https://spec.openapis.org/oas/v3.0.4.html#generating-and-validating-uris-and-form-urlencoded-strings)

URI percent encoding and the `form-urlencoded` media type have complex specification histories spanning multiple revisions and, in some cases, conflicting claims of ownership by different standards bodies. Unfortunately, these specifications each define slightly different percent-encoding rules, which need to be taken into account if the URIs or `form-urlencoded` message bodies will be subject to strict validation. (Note that many URI parsers do not perform validation by default.)

This specification normatively cites the following relevant standards:

| Specification | Date | OAS Usage | Percent-Encoding | Notes |
| --- | --- | --- | --- | --- |
| \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] | 01/2005 | URI/URL syntax | \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] | obsoletes \[[RFC1738](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1738 "Uniform Resource Locators (URL)")\], \[[RFC2396](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc2396 "Uniform Resource Identifiers (URI): Generic Syntax")\] |
| \[[RFC6570](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc6570 "URI Template")\] | 03/2012 | style-based serialization | \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] | does not use `+` for `form‑urlencoded` |
| \[[RFC1866](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1866 "Hypertext Markup Language - 2.0")\] [Section 8.2.1](https://datatracker.ietf.org/doc/html/rfc1866#section-8.2.1) | 11/1995 | content-based serialization | \[[RFC1738](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1738 "Uniform Resource Locators (URL)")\] | obsoleted by \[[HTML401](https://spec.openapis.org/oas/v3.0.4.html#bib-html401 "HTML 4.01 Specification")\] [Section 17.13.4.1](https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.1), \[[URL](https://spec.openapis.org/oas/v3.0.4.html#bib-url "URL Standard")\] [Section 5](https://url.spec.whatwg.org/#urlencoded-serializing) |

Style-based serialization is used in the [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) when `schema` is present, and in the [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) when at least one of `style`, `explode`, or `allowReserved` is present. See [Appendix C](https://spec.openapis.org/oas/v3.0.4.html#appendix-c-using-rfc6570-based-serialization) for more details of RFC6570’s two different approaches to percent-encoding, including an example involving `+`.

Content-based serialization is defined by the [Media Type Object](https://spec.openapis.org/oas/v3.0.4.html#media-type-object), and used with the [Parameter Object](https://spec.openapis.org/oas/v3.0.4.html#parameter-object) when the `content` field is present, and with the [Encoding Object](https://spec.openapis.org/oas/v3.0.4.html#encoding-object) based on the `contentType` field when the fields `style`, `explode`, and `allowReserved` are absent. Each part is encoded based on the media type (e.g. `text/plain` or `application/json`), and must then be percent-encoded for use in a `form-urlencoded` string.

Note that content-based serialization for `form-data` does not expect or require percent-encoding in the data, only in per-part header values.

#### E.3.1 Interoperability with Historical Specifications

[](https://spec.openapis.org/oas/v3.0.4.html#interoperability-with-historical-specifications)

In most cases, generating query strings in strict compliance with \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] is sufficient to pass validation (including JSON Schema’s `format: "uri"` and `format: "uri-reference"`), but some `form-urlencoded` implementations still expect the slightly more restrictive \[[RFC1738](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1738 "Uniform Resource Locators (URL)")\] rules to be used.

Since all RFC1738-compliant URIs are compliant with RFC3986, applications needing to ensure historical interoperability *SHOULD* use RFC1738’s rules.

#### E.3.2 Interoperability with Web Browser Environments

[](https://spec.openapis.org/oas/v3.0.4.html#interoperability-with-web-browser-environments)

WHATWG is a [web browser-oriented](https://whatwg.org/faq#what-is-the-whatwg-working-on) standards group that has defined a “URL Living Standard” for parsing and serializing URLs in a browser context, including parsing and serializing `form-urlencoded` data. WHATWG’s percent-encoding rules for query strings are different depending on whether the query string is [being treated as `form-urlencoded`](https://url.spec.whatwg.org/#application-x-www-form-urlencoded-percent-encode-set) (where it requires more percent-encoding than \[[RFC1738](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc1738 "Uniform Resource Locators (URL)")\]) or [as part of the generic syntax](https://url.spec.whatwg.org/#query-percent-encode-set), where it allows characters that \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] forbids.

Implementations needing maximum compatibility with web browsers *SHOULD* use WHATWG’s `form-urlencoded` percent-encoding rules. However, they *SHOULD NOT* rely on WHATWG’s less stringent generic query string rules, as the resulting URLs would fail RFC3986 validation, including JSON Schema’s `format: uri` and `format: uri-reference`.

### E.4 Decoding URIs and `form-urlencoded` Strings

[](https://spec.openapis.org/oas/v3.0.4.html#decoding-uris-and-form-urlencoded-strings)

The percent-decoding algorithm does not care which characters were or were not percent-decoded, which means that URIs percent-encoded according to any specification will be decoded correctly.

Similarly, all `form-urlencoded` decoding algorithms simply add `+`\-for-space handling to the percent-decoding algorithm, and will work regardless of the encoding specification used.

However, care must be taken to use `form-urlencoded` decoding if `+` represents a space, and to use regular percent-decoding if `+` represents itself as a literal value.

### E.5 Percent-Encoding and Illegal or Reserved Delimiters

[](https://spec.openapis.org/oas/v3.0.4.html#percent-encoding-and-illegal-or-reserved-delimiters)

The `[`, `]`, `|`, and space characters, which are used as delimiters for the `deepObject`, `pipeDelimited`, and `spaceDelimited` styles, respectively, all *MUST* be percent-encoded to comply with \[[RFC3986](https://spec.openapis.org/oas/v3.0.4.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\]. This requires users to pre-encode the character(s) in some other way in parameter names and values to distinguish them from the delimiter usage when using one of these styles.

The space character is always illegal and encoded in some way by all implementations of all versions of the relevant standards. While one could use the `form-urlencoded` convention of `+` to distinguish spaces in parameter names and values from `spaceDelimited` delimiters encoded as `%20`, the specifications define the decoding as a single pass, making it impossible to distinguish the different usages in the decoded result.

Some environments use `[`, `]`, and possibly `|` unencoded in query strings without apparent difficulties, and WHATWG’s generic query string rules do not require percent-encoding them. Code that relies on leaving these delimiters unencoded, while using regular percent-encoding for them within names and values, is not guaranteed to be interoperable across all implementations.

For maximum interoperability, it is *RECOMMENDED* to either define and document an additional escape convention while percent-encoding the delimiters for these styles, or to avoid these styles entirely. The exact method of additional encoding/escaping is left to the API designer, and is expected to be performed before serialization and encoding described in this specification, and reversed after this specification’s encoding and serialization steps are reversed. This keeps it outside of the processes governed by this specification.

## F. Appendix F: Resolving Security Requirements in a Referenced Document

[](https://spec.openapis.org/oas/v3.0.4.html#appendix-f-resolving-security-requirements-in-a-referenced-document)

This appendix shows how to retrieve an HTTP-accessible multi-document OpenAPI Description (OAD) and resolve a [Security Requirement Object](https://spec.openapis.org/oas/v3.0.4.html#security-requirement-object) in the referenced (non-entry) document. See [Resolving Implicit Connections](https://spec.openapis.org/oas/v3.0.4.html#resolving-implicit-connections) for more information.

First, the [entry document](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-structure) is where parsing begins. It defines the `MySecurity` security scheme to be JWT-based, and it defines a Path Item as a reference to a component in another document:

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

In the `other` document, the referenced path item has a Security Requirement for a Security Scheme, `MySecurity`. The same Security Scheme exists in the original entry document. As outlined in [Resolving Implicit Connections](https://spec.openapis.org/oas/v3.0.4.html#resolving-implicit-connections), `MySecurity` is resolved with an [implementation-defined behavior](https://spec.openapis.org/oas/v3.0.4.html#undefined-and-implementation-defined-behavior). However, documented in that section, it is *RECOMMENDED* that tools resolve component names from the [entry document](https://spec.openapis.org/oas/v3.0.4.html#openapi-description-structure). As with all implementation-defined behavior, it is important to check tool documentation to determine which behavior is supported.

## G. References

[](https://spec.openapis.org/oas/v3.0.4.html#references)

### G.1 Normative references

[](https://spec.openapis.org/oas/v3.0.4.html#normative-references)

\[ABNF\]

[Augmented BNF for Syntax Specifications: ABNF](https://www.rfc-editor.org/rfc/rfc5234). D. Crocker, Ed.; P. Overell. IETF. January 2008. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc5234](https://www.rfc-editor.org/rfc/rfc5234)

\[CommonMark\]

[CommonMark Spec](https://spec.commonmark.org/). URL: [https://spec.commonmark.org/](https://spec.commonmark.org/)

\[CommonMark-0.27\]

[CommonMark Spec, Version 0.27](https://spec.commonmark.org/0.27/). John MacFarlane. 18 November 2016. URL: [https://spec.commonmark.org/0.27/](https://spec.commonmark.org/0.27/)

\[HTML401\]

[HTML 4.01 Specification](https://www.w3.org/TR/html401/). Dave Raggett; Arnaud Le Hors; Ian Jacobs. W3C. 27 March 2018. W3C Recommendation. URL: [https://www.w3.org/TR/html401/](https://www.w3.org/TR/html401/)

\[IANA-HTTP-AUTHSCHEMES\]

[Hypertext Transfer Protocol (HTTP) Authentication Scheme Registry](https://www.iana.org/assignments/http-authschemes/). IANA. URL: [https://www.iana.org/assignments/http-authschemes/](https://www.iana.org/assignments/http-authschemes/)

\[IANA-HTTP-STATUS-CODES\]

[Hypertext Transfer Protocol (HTTP) Status Code Registry](https://www.iana.org/assignments/http-status-codes/). IANA. URL: [https://www.iana.org/assignments/http-status-codes/](https://www.iana.org/assignments/http-status-codes/)

\[JSON-Reference\]

[JSON Reference](https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03). Paul Bryan; Kris Zyp. Internet Engineering Task Force (IETF). 16 September 2012. Internet-Draft. URL: [https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03](https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03)

\[JSON-Schema-05\]

[JSON Schema: A Media Type for Describing JSON Documents. Draft 5](https://datatracker.ietf.org/doc/html/draft-wright-json-schema-00). Austin Wright. Internet Engineering Task Force (IETF). 13 October 2016. Internet-Draft. URL: [https://datatracker.ietf.org/doc/html/draft-wright-json-schema-00](https://datatracker.ietf.org/doc/html/draft-wright-json-schema-00)

\[JSON-Schema-Validation-05\]

[JSON Schema Validation: A Vocabulary for Structural Validation of JSON. Draft 5](https://datatracker.ietf.org/doc/html/draft-wright-json-schema-validation-00). Austin Wright; G. Luff. Internet Engineering Task Force (IETF). 13 October 2016. Internet-Draft. URL: [https://datatracker.ietf.org/doc/html/draft-wright-json-schema-validation-00](https://datatracker.ietf.org/doc/html/draft-wright-json-schema-validation-00)

\[OpenAPI-Registry\]

[OpenAPI Initiative Registry](https://spec.openapis.org/registry/index.html). OpenAPI Initiative. URL: [https://spec.openapis.org/registry/index.html](https://spec.openapis.org/registry/index.html)

\[OpenID-Connect-Core\]

[OpenID Connect Core 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-core-1_0.html). N. Sakimura; J. Bradley; M. Jones; B. de Medeiros; C. Mortimore. OpenID Foundation. 15 December 2023. Final. URL: [https://openid.net/specs/openid-connect-core-1\_0.html](https://openid.net/specs/openid-connect-core-1_0.html)

\[OpenID-Connect-Discovery\]

[OpenID Connect Discovery 1.0 incorporating errata set 2](https://openid.net/specs/openid-connect-discovery-1_0.html). N. Sakimura; J. Bradley; M. Jones; E. Jay. OpenID Foundation. 15 December 2023. Final. URL: [https://openid.net/specs/openid-connect-discovery-1\_0.html](https://openid.net/specs/openid-connect-discovery-1_0.html)

\[RFC1738\]

[Uniform Resource Locators (URL)](https://www.rfc-editor.org/rfc/rfc1738). T. Berners-Lee; L. Masinter; M. McCahill. IETF. December 1994. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc1738](https://www.rfc-editor.org/rfc/rfc1738)

\[RFC1866\]

[Hypertext Markup Language - 2.0](https://www.rfc-editor.org/rfc/rfc1866). T. Berners-Lee; D. Connolly. IETF. November 1995. Historic. URL: [https://www.rfc-editor.org/rfc/rfc1866](https://www.rfc-editor.org/rfc/rfc1866)

\[RFC2046\]

[Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types](https://www.rfc-editor.org/rfc/rfc2046). N. Freed; N. Borenstein. IETF. November 1996. Draft Standard. URL: [https://www.rfc-editor.org/rfc/rfc2046](https://www.rfc-editor.org/rfc/rfc2046)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC2396\]

[Uniform Resource Identifiers (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc2396). T. Berners-Lee; R. Fielding; L. Masinter. IETF. August 1998. Draft Standard. URL: [https://www.rfc-editor.org/rfc/rfc2396](https://www.rfc-editor.org/rfc/rfc2396)

\[RFC3339\]

[Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339). G. Klyne; C. Newman. IETF. July 2002. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc3339](https://www.rfc-editor.org/rfc/rfc3339)

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

\[RFC6838\]

[Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838). N. Freed; J. Klensin; T. Hansen. IETF. January 2013. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc6838](https://www.rfc-editor.org/rfc/rfc6838)

\[RFC6901\]

[JavaScript Object Notation (JSON) Pointer](https://www.rfc-editor.org/rfc/rfc6901). P. Bryan, Ed.; K. Zyp; M. Nottingham, Ed. IETF. April 2013. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc6901](https://www.rfc-editor.org/rfc/rfc6901)

\[RFC7159\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc7159). T. Bray, Ed. IETF. March 2014. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7159](https://www.rfc-editor.org/rfc/rfc7159)

\[RFC7230\]

[Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing](https://httpwg.org/specs/rfc7230.html). R. Fielding, Ed.; J. Reschke, Ed. IETF. June 2014. Proposed Standard. URL: [https://httpwg.org/specs/rfc7230.html](https://httpwg.org/specs/rfc7230.html)

\[RFC7231\]

[Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content](https://httpwg.org/specs/rfc7231.html). R. Fielding, Ed.; J. Reschke, Ed. IETF. June 2014. Proposed Standard. URL: [https://httpwg.org/specs/rfc7231.html](https://httpwg.org/specs/rfc7231.html)

\[RFC7235\]

[Hypertext Transfer Protocol (HTTP/1.1): Authentication](https://httpwg.org/specs/rfc7235.html). R. Fielding, Ed.; J. Reschke, Ed. IETF. June 2014. Proposed Standard. URL: [https://httpwg.org/specs/rfc7235.html](https://httpwg.org/specs/rfc7235.html)

\[RFC7578\]

[Returning Values from Forms: multipart/form-data](https://www.rfc-editor.org/rfc/rfc7578). L. Masinter. IETF. July 2015. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7578](https://www.rfc-editor.org/rfc/rfc7578)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[RFC8187\]

[Indicating Character Encoding and Language for HTTP Header Field Parameters](https://www.rfc-editor.org/rfc/rfc8187). J. Reschke. IETF. September 2017. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc8187](https://www.rfc-editor.org/rfc/rfc8187)

\[RFC8941\]

[Structured Field Values for HTTP](https://httpwg.org/specs/rfc8941.html). M. Nottingham; P-H. Kamp. IETF. February 2021. Proposed Standard. URL: [https://httpwg.org/specs/rfc8941.html](https://httpwg.org/specs/rfc8941.html)

\[URL\]

[URL Standard](https://url.spec.whatwg.org/). Anne van Kesteren. WHATWG. Living Standard. URL: [https://url.spec.whatwg.org/](https://url.spec.whatwg.org/)

\[xml-names11\]

[Namespaces in XML 1.1 (Second Edition)](https://www.w3.org/TR/xml-names11/). Tim Bray; Dave Hollander; Andrew Layman; Richard Tobin et al. W3C. 16 August 2006. W3C Recommendation. URL: [https://www.w3.org/TR/xml-names11/](https://www.w3.org/TR/xml-names11/)

\[YAML\]

[YAML Ain’t Markup Language (YAML™) Version 1.2](http://yaml.org/spec/1.2/spec.html). Oren Ben-Kiki; Clark Evans; Ingy döt Net. 1 October 2009. URL: [http://yaml.org/spec/1.2/spec.html](http://yaml.org/spec/1.2/spec.html)

### G.2 Informative references

[](https://spec.openapis.org/oas/v3.0.4.html#informative-references)

\[OpenAPI-Learn\]

[OpenAPI - Getting started, and the specification explained](https://learn.openapis.org/). OpenAPI Initiative. URL: [https://learn.openapis.org/](https://learn.openapis.org/)

[↑](https://spec.openapis.org/oas/v3.0.4.html#title)
