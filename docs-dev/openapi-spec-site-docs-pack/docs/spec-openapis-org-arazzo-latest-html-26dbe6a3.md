---
title: "The Arazzo Specification v1.1.0"
source_url: "https://spec.openapis.org/arazzo/latest.html"
host: "spec.openapis.org"
depth: 1
selector: "body"
fetched_at: "2026-07-17T17:36:55.398Z"
---
[![OpenAPI Initiative](https://raw.githubusercontent.com/OAI/OpenAPI-Style-Guide/master/graphics/bitmap/OpenAPI_Logo_Pantone.png)](https://openapis.org/)

# The Arazzo Specification v1.1.0

## Version 1.1.0

17 May 2026

More details about this document

Latest published version:

[https://spec.openapis.org/arazzo/latest.html](https://spec.openapis.org/arazzo/latest.html)

Latest editor's draft:

[https://github.com/OAI/Arazzo-Specification/](https://github.com/OAI/Arazzo-Specification/)

Editors:

Frank Kilcommins

Nick Denny

Kevin Duffey

Participate

[GitHub OAI/Arazzo-Specification](https://github.com/OAI/Arazzo-Specification/)

[File a bug](https://github.com/OAI/Arazzo-Specification/issues)

[Commit history](https://github.com/OAI/Arazzo-Specification/commits/main/versions/1.1.0.md)

[Pull requests](https://github.com/OAI/Arazzo-Specification/pulls)

Copyright © 2026 the Linux Foundation

* * *

## What is the Arazzo Specification?

The Arazzo Specification provides a mechanism that can define sequences of calls and their dependencies to be woven together and expressed in the context of delivering a particular outcome or set of outcomes when dealing with API descriptions (such as OpenAPI descriptions).

## Status of This Document

The source-of-truth for the specification is the GitHub markdown file referenced above.

## 1\. Arazzo Specification

[](https://spec.openapis.org/arazzo/latest.html#arazzo-specification)

## 2\. Version 1.1.0

[](https://spec.openapis.org/arazzo/latest.html#version-1-1-0)

The key words “*MUST*”, “*MUST NOT*”, “*REQUIRED*”, “*SHALL*”, “*SHALL NOT*”, “*SHOULD*”, “*SHOULD NOT*”, “*RECOMMENDED*”, “*NOT RECOMMENDED*”, “*MAY*”, and “*OPTIONAL*” in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14) \[[RFC2119](https://spec.openapis.org/arazzo/latest.html#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://spec.openapis.org/arazzo/latest.html#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

This document is licensed under [The Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

## 3\. Introduction

[](https://spec.openapis.org/arazzo/latest.html#introduction)

Being able to express specific sequences of calls and articulate the dependencies between them to achieve a particular goal is desirable in the context of API descriptions. The aim of the Arazzo Specification is to provide a mechanism that can define sequences of calls and their dependencies to be woven together and expressed in the context of delivering a particular outcome or set of outcomes when dealing with API descriptions (such as OpenAPI descriptions).

The Arazzo Specification can articulate these workflows in a human-readable and machine-readable manner, thus improving the capability of API specifications to tell the story of the API in a manner that can improve the consuming developer experience.

## 4\. Definitions

[](https://spec.openapis.org/arazzo/latest.html#definitions)

### 4.1 Arazzo Description

[](https://spec.openapis.org/arazzo/latest.html#arazzo-description)

A self-contained document (or set of documents) which defines or describes API workflows (specific sequence of calls to achieve a particular goal in the context of an API definition). An Arazzo Description uses and conforms to the Arazzo Specification, and `*MUST*` contain a valid Arazzo Specification version field (`arazzo`), an [info](https://spec.openapis.org/arazzo/latest.html#info-object) field, a `sourceDescriptions` field with at least one defined [Source Description](https://spec.openapis.org/arazzo/latest.html#source-description-object), and there `*MUST*` be at least one [Workflow](https://spec.openapis.org/arazzo/latest.html#workflow-object) defined in the `workflows` fixed field.

## 5\. Specification

[](https://spec.openapis.org/arazzo/latest.html#specification)

### 5.1 Versions

[](https://spec.openapis.org/arazzo/latest.html#versions)

The Arazzo Specification is versioned using a `major`.`minor`.`patch` versioning scheme. The `major`.`minor` portion of the version string (for example 1.0) *SHALL* designate the Arazzo feature set. `.patch` versions address errors in, or provide clarifications to, this document, not the feature set. The patch version *SHOULD NOT* be considered by tooling, making no distinction between 1.0.0 and 1.0.1 for example.

### 5.2 Format

[](https://spec.openapis.org/arazzo/latest.html#format)

An Arazzo Description that conforms to the Arazzo Specification is itself a JSON object, which may be represented either in JSON or YAML format.

All field names in the specification are **case sensitive**. This includes all fields that are used as keys in a map, except where explicitly noted that keys are **case insensitive**.

In order to preserve the ability to round-trip between YAML and JSON formats, YAML version [1.2](https://yaml.org/spec/1.2/spec.html) is *RECOMMENDED* along with some additional constraints:

-   Tags *MUST* be limited to those allowed by the [JSON Schema ruleset](https://yaml.org/spec/1.2/spec.html#id2803231).
-   Keys used in YAML maps *MUST* be limited to a scalar string, as defined by the [YAML Failsafe schema ruleset](https://yaml.org/spec/1.2/spec.html#id2802346).

### 5.3 Arazzo Description Structure

[](https://spec.openapis.org/arazzo/latest.html#arazzo-description-structure)

It is *RECOMMENDED* that the entry Arazzo document be named: `arazzo.json` or `arazzo.yaml`.

An Arazzo Description *MAY* be made up of a single document or be divided into multiple, connected parts at the discretion of the author. If workflows from other documents are being referenced, they *MUST* be included as a [Source Description Object](https://spec.openapis.org/arazzo/latest.html#source-description-object). In a multi-document description, the document containing the [Arazzo Specification Object](https://spec.openapis.org/arazzo/latest.html#arazzo-specification-object) is known as the **entry Arazzo document**.

### 5.4 Data Types

[](https://spec.openapis.org/arazzo/latest.html#data-types)

Data types in the Arazzo Specification are based on the types supported by the [JSON Schema Specification Draft 2020-12](https://tools.ietf.org/html/draft-bhutton-json-schema-00#section-4.2.1). Note that integer as a type is also supported and is defined as a JSON number without a fraction or exponent part.

As defined by the [JSON Schema Validation vocabulary](https://tools.ietf.org/html/draft-bhutton-json-schema-validation-00#section-7), data types can have an optional modifier property: `format`. Arazzo additionally supports the formats (similar to the OpenAPI specification) to provide fine detail for primitive data types.

The formats defined are:

| `format` | JSON Data Type | Comments |
| --- | --- | --- |
| `int32` | number | signed 32 bits |
| `int64` | number | signed 64 bits (a.k.a long) |
| `float` | number |  |
| `double` | number |  |
| `password` | string | A hint to obscure the value. |

### 5.5 Parsing Documents

[](https://spec.openapis.org/arazzo/latest.html#parsing-documents)

Each document in an Arazzo Description *MUST* be fully parsed in order to locate possible reference targets before attempting to resolve references. This includes the parsing requirements of [JSON Schema Specification Draft 2020-12](https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html#section-9), with appropriate modifications regarding base URIs as specified in [Relative References in Arazzo Description URIs](https://spec.openapis.org/arazzo/latest.html#relative-references-in-arazzo-description-uris). Reference targets include the Arazzo Object’s [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) field (when present) and Source Description `url` fields.

Implementations *MUST NOT* treat a reference as unresolvable before completely parsing all documents provided to the implementation as possible parts of the Arazzo Description.

#### 5.5.1 Fragmentary Parsing

[](https://spec.openapis.org/arazzo/latest.html#fragmentary-parsing)

**Fragmentary parsing** occurs when an implementation parses only the specific part of a document being referenced, rather than parsing the complete document first. This practice is **strongly discouraged** and produces undefined behavior.

If only the referenced part of a document is parsed when resolving a reference, implementations may miss critical fields such as:

-   The [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) field, causing identity-based references to fail
-   Source Description `url` fields, preventing proper resolution of referenced API descriptions
-   Other workflow or step definitions needed to validate cross-references

When fragmentary parsing causes references to resolve to unintended locations or fail to resolve entirely, the resulting behavior is *undefined* and *implementation-defined*. Different implementations may handle such cases inconsistently, breaking interoperability.

Implementations *MUST* parse entire documents before resolving references to ensure consistent, predictable behavior across different tools and environments.

#### 5.5.2 Identity-Based Referencing

[](https://spec.openapis.org/arazzo/latest.html#identity-based-referencing)

To ensure interoperability, when referencing an Arazzo Description by URI, references *MUST* use the target document’s [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) URI if the `$self` field is present in that document.

This means implementations *MUST* examine potential target Arazzo Descriptions (including those referenced via Source Description `url` fields or Workflow `workflowId` references) to check for matching `$self` values. When a Source Description Object’s `url` field is an absolute URI, the implementation *MUST* resolve it to an Arazzo Description by identity (matching the `$self` value) rather than by location alone.

Implementations *MAY* support referencing by other identifiers (such as retrieval URIs), but this behavior is not interoperable and relying on it is *NOT RECOMMENDED*.

### 5.6 Relative References in Arazzo Description URIs

[](https://spec.openapis.org/arazzo/latest.html#relative-references-in-arazzo-description-uris)

URIs used as references within an Arazzo Description, including Source Description `url`, are resolved as *identifiers*, and described by this specification as **URIs**.

Unless specified otherwise, all fields that are URIs *MAY* be relative references as defined by [RFC3986 Section 4.2](https://tools.ietf.org/html/rfc3986#section-4.2).

#### 5.6.1 Establishing the Base URI

[](https://spec.openapis.org/arazzo/latest.html#establishing-the-base-uri)

Relative URI references are resolved using the appropriate base URI, which *MUST* be determined in accordance with [RFC3986 Section 5.1.1 – 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.1).

The base URI for resolving relative references within an Arazzo Description is determined as follows:

-   If the [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) field is present and is an absolute URI, the base URI is the `$self` URI (per [RFC3986 Section 5.1.1](https://tools.ietf.org/html/rfc3986#section-5.1.1): Base URI Embedded in Content).
-   If the [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) field is present and is a relative URI-reference, it *MUST* first be resolved against the next possible base URI source per [RFC3986 Section 5.1.2 – 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.2) before being used as the base URI for resolving other relative references.
-   If the [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) field is not present, the base URI *MUST* be determined from the next possible base URI source per [RFC3986 Section 5.1.2 – 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.2). The most common base URI source in this case is the retrieval URI of the Arazzo Description document (per [RFC3986 Section 5.1.3](https://tools.ietf.org/html/rfc3986#section-5.1.3)), though other sources such as encapsulating entities ([RFC3986 Section 5.1.2](https://tools.ietf.org/html/rfc3986#section-5.1.2)) or application-specific defaults ([RFC3986 Section 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.4)) *MAY* apply.

For examples demonstrating base URI determination and reference resolution, see [Appendix B: Examples of Base URI Determination and Reference Resolution](https://spec.openapis.org/arazzo/latest.html#appendix-b-examples-of-base-uri-determination-and-reference-resolution).

#### 5.6.2 Resolving URI Fragments

[](https://spec.openapis.org/arazzo/latest.html#resolving-uri-fragments)

If a URI contains a fragment identifier, then the fragment *MUST* be resolved per the fragment resolution mechanism of the referenced document.

For JSON or YAML documents, the fragment identifier *SHOULD* be interpreted as a JSON Pointer as per \[[RFC6901](https://spec.openapis.org/arazzo/latest.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\].

For JSON Schema objects used in workflow `inputs` and `components.inputs`, references via `$ref` *MUST* support both JSON Pointer fragments and plain-name fragments (defined by `$anchor`) as specified by [JSON Schema Specification Draft 2020-12](https://tools.ietf.org/html/draft-bhutton-json-schema-01.html).

When an Arazzo Description references an OpenAPI or AsyncAPI description via a Source Description `url` field, any fragments in runtime expressions (such as in `operationPath`) use JSON Pointer syntax to identify specific operations or components within that description. The resolution of further references within the referenced OpenAPI or AsyncAPI description (including Schema Object `$ref` and `$anchor` keywords) *MUST* follow the rules and guidance laid out by the OpenAPI Specification and AsyncAPI Specification respectively.

**Example:**

```

sourceDescriptions:
  - name: petstore
    url: https://api.example.com/petstore.yaml
    type: openapi

workflows:
  - workflowId: example
    steps:
      - stepId: getPet
        # Fragment '#/paths/~1pets/get' resolves via JSON Pointer
        operationPath: '{$sourceDescriptions.petstore.url}#/paths/~1pets/get'
```

#### 5.6.3 Relative URI References in CommonMark Fields

[](https://spec.openapis.org/arazzo/latest.html#relative-uri-references-in-commonmark-fields)

Relative references in CommonMark hyperlinks (such as those in `description` or `summary` fields) are resolved in their rendered context, which might differ from the context of the Arazzo Description.

### 5.7 Relative References in API URLs

[](https://spec.openapis.org/arazzo/latest.html#relative-references-in-api-urls)

API endpoints accessed during workflow execution are described by this specification as **URLs** (locations, not identifiers).

When [Step Objects](https://spec.openapis.org/arazzo/latest.html#step-object) reference API operations via `operationId` or `operationPath`, the actual API endpoint URL is determined by the OpenAPI description’s Server Object, not by the Arazzo Description’s base URI.

Runtime expressions may reference API URLs via `$url` during workflow execution, but these are evaluated at execution time, not during document parsing.

### 5.8 Schema

[](https://spec.openapis.org/arazzo/latest.html#schema)

In the following description, if a field is not explicitly ***REQUIRED*** or described with a *MUST* or *SHALL*, it can be considered *OPTIONAL*.

#### 5.8.1 Arazzo Specification Object

[](https://spec.openapis.org/arazzo/latest.html#arazzo-specification-object)

This is the root object of the [Arazzo Description](https://spec.openapis.org/arazzo/latest.html#arazzo-description).

##### 5.8.1.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields)

| Field Name | Type | Description |
| --- | --- | --- |
| arazzo | `string` | ***REQUIRED***. This string *MUST* be the [version number](https://spec.openapis.org/arazzo/latest.html#versions) of the Arazzo Specification that the Arazzo Description uses. The `arazzo` field *MUST* be used by tooling to interpret the Arazzo Description. |
| $self | `string` | A URI-reference for the Arazzo Description. This string *MUST* be in the form of a URI-reference as defined by [RFC3986 Section 4.1](https://tools.ietf.org/html/rfc3986#section-4.1). When present, this field provides the self-assigned URI of this Arazzo Description, which also serves as its base URI in accordance with [RFC3986 Section 5.1.1](https://tools.ietf.org/html/rfc3986#section-5.1.1) for resolving relative references within this document. The `$self` URI *MUST NOT* contain a fragment identifier. Arazzo Description documents can include a `$self` field to ensure portable, unambiguous reference resolution. |
| info | [Info Object](https://spec.openapis.org/arazzo/latest.html#info-object) | ***REQUIRED***. Provides metadata about the workflows contain within the Arazzo Description. The metadata *MAY* be used by tooling as required. |
| sourceDescriptions | \[[Source Description Object](https://spec.openapis.org/arazzo/latest.html#source-description-object)\] | ***REQUIRED***. A list of source descriptions (such as an OpenAPI description) this Arazzo Description *SHALL* apply to. The list *MUST* have at least one entry. |
| workflows | \[[Workflow Object](https://spec.openapis.org/arazzo/latest.html#workflow-object)\] | ***REQUIRED***. A list of workflows. The list *MUST* have at least one entry. |
| components | [Components Object](https://spec.openapis.org/arazzo/latest.html#components-object) | An element to hold various schemas for the Arazzo Description. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.1.2 Arazzo Specification Object Example

[](https://spec.openapis.org/arazzo/latest.html#arazzo-specification-object-example)

```

arazzo: 1.1.0
$self: https://api.example.com/workflows/pet-purchase.arazzo.yaml
info:
  title: A pet purchasing workflow
  summary: This Arazzo Description showcases the workflow for how to purchase a pet through a sequence of API calls
  description: |
      This Arazzo Description walks you through the workflow and steps of `searching` for, `selecting`, and `purchasing` an available pet.
  version: 1.0.1
sourceDescriptions:
- name: petStoreDescription
  url: https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml
  type: openapi
- name: asyncOrderApiDescription
  url: https://raw.githubusercontent.com/OAI/Arazzo-Specification/main/examples/1.1.0/pet-asyncapi.yaml
  type: asyncapi

workflows:
- workflowId: loginUserAndRetrievePet
  summary: Login User and then retrieve pets
  description: This workflow lays out the steps to login a user and then retrieve pets
  inputs:
      type: object
      properties:
          username:
              type: string
          password:
              type: string
          orderCorrelationId:
              type: string
  steps:
  - stepId: loginStep
    description: This step demonstrates the user login step
    operationId: $sourceDescriptions.petstoreDescription.loginUser
    parameters:
      # parameters to inject into the loginUser operation (parameter name must be resolvable at the referenced operation and the value is determined using {expression} syntax)
      - name: username
        in: query
        value: $inputs.username
      - name: password
        in: query
        value: $inputs.password
    successCriteria:
      # assertions to determine step was successful
      - condition: $statusCode == 200
    outputs:
      # outputs from this step
      tokenExpires: $response.header.X-Expires-After
      rateLimit: $response.header.X-Rate-Limit
      sessionToken: $response.body
  - stepId: getPetStep
    description: retrieve a pet by status from the GET pets endpoint
    operationPath: '{$sourceDescriptions.petstoreDescription.url}#/paths/~1pet~1findByStatus/get'
    parameters:
      - name: status
        in: query
        value: 'available'
      - name: Authorization
        in: header
        value: $steps.loginStep.outputs.sessionToken
    successCriteria:
      - condition: $statusCode == 200
    onSuccess:
      - name: 'noPetsAvailable'
        type: "end"
        criteria:
          - condition: $response.body#/0 == null
    outputs:
      petId: $response.body#/0/id
  - stepId: purchasePetStep
    description: purchase a pet by posting an message on place-order channel
    operationPath: $sourceDescriptions.asyncOrderApiDescription.placeOrder
    action: send
    parameters:
    - name: orderCorrelationId
      in: header
      value: $inputs.orderCorrelationId
    requestBody:
      contentType: application/json
      payload:
        petId: $steps.getPetStep.outputs.petId
  - stepId: confirmPetPurchaseStep
    description: confirm the purchase of a pet
    operationPath: $sourceDescriptions.asyncOrderApiDescription.confirmOrder
    correlationId: $inputs.orderCorrelationId
    timeout: 6000
    action: receive
    outputs:
      orderId: $message.payload.orderId
  outputs:
      orderId: $steps.confirmPetPurchaseStep.outputs.orderId
```

#### 5.8.2 Info Object

[](https://spec.openapis.org/arazzo/latest.html#info-object)

The object provides metadata about API workflows defined in this Arazzo document. The metadata *MAY* be used by the clients if needed.

##### 5.8.2.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-0)

| Field Name | Type | Description |
| --- | --- | --- |
| title | `string` | ***REQUIRED***. A human readable title of the Arazzo Description. |
| summary | `string` | A short summary of the Arazzo Description. |
| description | `string` | A description of the purpose of the workflows defined. [CommonMark syntax](https://spec.commonmark.org/) *MAY* be used for rich text representation. |
| version | `string` | ***REQUIRED***. The version identifier of the Arazzo document (which is distinct from the [Arazzo Specification version](https://spec.openapis.org/arazzo/latest.html#versions)). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.2.2 Info Object Example

[](https://spec.openapis.org/arazzo/latest.html#info-object-example)

```

title: A pet purchasing workflow
summary: This workflow showcases how to purchase a pet through a sequence of API calls
description: |
    This workflow walks you through the steps of searching for, selecting, and purchasing an available pet.
version: 1.0.1
```

#### 5.8.3 Source Description Object

[](https://spec.openapis.org/arazzo/latest.html#source-description-object)

Describes a source description (such as an OpenAPI description) that will be referenced by one or more workflows described within an Arazzo Description.

An object storing a map between named description keys and location URLs to the source descriptions (such as an OpenAPI description) this Arazzo Description *SHALL* apply to. Each source location `string` *MUST* be in the form of a URI-reference as defined by \[[RFC3986](https://spec.openapis.org/arazzo/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.1](https://tools.ietf.org/html/rfc3986#section-4.1).

##### 5.8.3.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-1)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. A unique name for the source description. Tools and libraries *MAY* use the `name` to uniquely identify a source description, therefore, it is *RECOMMENDED* to follow common programming naming conventions. *SHOULD* conform to the regular expression `[A-Za-z0-9_\-]+`. |
| url | `string` | ***REQUIRED***. A URL to a source description to be used by a workflow. If a relative reference is used, it *MUST* be in the form of a URI-reference as defined by \[[RFC3986](https://spec.openapis.org/arazzo/latest.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://tools.ietf.org/html/rfc3986#section-4.2). |
| type | `string` | The type of source description. Possible values are `"openapi"` or `"asyncapi"` or `"arazzo"`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.3.2 Source Description Object Example

[](https://spec.openapis.org/arazzo/latest.html#source-description-object-example)

```

name: petStoreDescription
url: https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml
type: openapi
```

#### 5.8.4 Workflow Object

[](https://spec.openapis.org/arazzo/latest.html#workflow-object)

Describes the steps to be taken across one or more APIs to achieve an objective. The workflow object *MAY* define inputs needed in order to execute workflow steps, where the defined steps represent a call to an API operation or another workflow, and a set of outputs.

##### 5.8.4.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-2)

| Field Name | Type | Description |
| --- | --- | --- |
| workflowId | `string` | ***REQUIRED***. Unique string to represent the workflow. The id *MUST* be unique amongst all workflows described in the Arazzo Description. The `workflowId` value is **case-sensitive**. Tools and libraries *MAY* use the `workflowId` to uniquely identify a workflow, therefore, it is *RECOMMENDED* to follow common programming naming conventions. *SHOULD* conform to the regular expression `[A-Za-z0-9_\-]+`. |
| summary | `string` | A summary of the purpose or objective of the workflow. |
| description | `string` | A description of the workflow. [CommonMark syntax](https://spec.commonmark.org/) *MAY* be used for rich text representation. |
| inputs | `JSON Schema` | A JSON Schema 2020-12 object representing the input parameters used by this workflow. |
| dependsOn | \[`string`\] | A list of workflows that *MUST* be completed before this workflow can be processed. Each value provided *MUST* be a `workflowId`. If the workflow depended on is defined within the current Workflow Document, then specify the `workflowId` of the relevant local workflow. If the workflow is defined in a separate Arazzo Document then the workflow *MUST* be defined in the `sourceDescriptions` and the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. |
| steps | \[[Step Object](https://spec.openapis.org/arazzo/latest.html#step-object)\] | ***REQUIRED***. An ordered list of steps where each step represents a call to an API operation or to another workflow. |
| successActions | \[[Success Action Object](https://spec.openapis.org/arazzo/latest.html#success-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | A list of success actions that are applicable for all steps described under this workflow. These success actions can be overridden at the step level but cannot be removed there. If a Reusable Object is provided, it *MUST* link to success actions defined in the [components/successActions](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate success actions. |
| failureActions | \[[Failure Action Object](https://spec.openapis.org/arazzo/latest.html#failure-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | A list of failure actions that are applicable for all steps described under this workflow. These failure actions can be overridden at the step level but cannot be removed there. If a Reusable Object is provided, it *MUST* link to failure actions defined in the [components/failureActions](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate failure actions. |
| outputs | Map\[`string`, {expression} | [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object) \] | A map between a friendly name and a dynamic output value defined using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) or [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object). The name *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`. |
| parameters | \[[Parameter Object](https://spec.openapis.org/arazzo/latest.html#parameter-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | A list of parameters that are applicable for all steps described under this workflow. These parameters can be overridden at the step level but cannot be removed there. Each parameter *MUST* be passed to an operation or workflow as referenced by `operationId`, `operationPath`, or `workflowId` as specified within each step. If a Reusable Object is provided, it *MUST* link to a parameter defined in the [components/parameters](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate parameters. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.4.2 Workflow Object Example

[](https://spec.openapis.org/arazzo/latest.html#workflow-object-example)

```

workflowId: loginUser
summary: Login User
description: This workflow lays out the steps to login a user
inputs:
    type: object
    properties:
        username:
            type: string
        password:
            type: string
steps:
  - stepId: loginStep
    description: This step demonstrates the user login step
    operationId: loginUser
    parameters:
      # parameters to inject into the loginUser operation (parameter name must be resolvable at the referenced operation and the value is determined using {expression} syntax)
      - name: username
        in: query
        value: $inputs.username
      - name: password
        in: query
        value: $inputs.password
    successCriteria:
        # assertions to determine step was successful
        - condition: $statusCode == 200
    outputs:
        # outputs from this step
        tokenExpires: $response.header.X-Expires-After
        rateLimit: $response.header.X-Rate-Limit
outputs:
    tokenExpires: $steps.loginStep.outputs.tokenExpires
```

#### 5.8.5 Step Object

[](https://spec.openapis.org/arazzo/latest.html#step-object)

Describes a single workflow step which *MAY* be a call to an API operation ([OpenAPI Operation Object](https://spec.openapis.org/oas/latest.html#operation-object)), ([AysncAPI Operations Object](https://www.asyncapi.com/docs/reference/specification/latest#operationsObject)) or another [Workflow Object](https://spec.openapis.org/arazzo/latest.html#workflow-object).

##### 5.8.5.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-3)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A description of the step. [CommonMark syntax](https://spec.commonmark.org/) *MAY* be used for rich text representation. |
| stepId | `string` | ***REQUIRED***. Unique string to represent the step. The `stepId` *MUST* be unique amongst all steps described in the workflow. The `stepId` value is **case-sensitive**. Tools and libraries *MAY* use the `stepId` to uniquely identify a workflow step, therefore, it is *RECOMMENDED* to follow common programming naming conventions. *SHOULD* conform to the regular expression `[A-Za-z0-9_\-]+`. |
| operationId | `string` | The name of an existing, resolvable operation, as defined with a unique `operationId` and existing within one of the `sourceDescriptions`. The referenced operation will be invoked by this workflow step. If multiple (non `arazzo` type) `sourceDescriptions` are defined, then the `operationId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<operationId>`) to avoid ambiguity or potential clashes. This field is mutually exclusive of the `operationPath` and `workflowId` fields respectively. |
| operationPath | `string` | A reference to a [Source Description Object](https://spec.openapis.org/arazzo/latest.html#source-description-object) combined with a [JSON Pointer](https://tools.ietf.org/html/rfc6901) to reference an operation. This field is mutually exclusive of the `operationId` and `workflowId` fields respectively. The operation being referenced *MUST* be described within one of the `sourceDescriptions` descriptions. A [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) syntax *MUST* be used to identify the source description document. If the referenced operation has an `operationId` defined then the `operationId` *SHOULD* be preferred over the `operationPath`. |
| channelPath | `string` | A reference to a [Source Description Object](https://spec.openapis.org/arazzo/latest.html#source-description-object) combined with a [JSON Pointer](https://tools.ietf.org/html/rfc6901) to reference an event channel. This field is mutually exclusive of the `operationId` and `workflowId` fields respectively. The operation being referenced *MUST* be described within one of the `sourceDescriptions` descriptions. A [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) syntax *MUST* be used to identify the source description document. If the referenced operation has an `operationId` defined then the `operationId` *SHOULD* be preferred over the `channelPath`. |
| workflowId | `string` | The [workflowId](https://spec.openapis.org/arazzo/latest.html#fixed-fields-2) referencing an existing workflow within the Arazzo Description. If the referenced workflow is contained within an `arazzo` type `sourceDescription`, then the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. The field is mutually exclusive of the `operationId` and `operationPath` fields respectively. |
| parameters | \[[Parameter Object](https://spec.openapis.org/arazzo/latest.html#parameter-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | A list of parameters that *MUST* be passed to an operation or workflow as referenced by `operationId`, `operationPath`, or `workflowId`. If a parameter is already defined at the [Workflow](https://spec.openapis.org/arazzo/latest.html#workflow-object), the new definition will override it but can never remove it. If a Reusable Object is provided, it *MUST* link to a parameter defined in the [components/parameters](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate parameters. |
| requestBody | [Request Body Object](https://spec.openapis.org/arazzo/latest.html#request-body-object) | The request body to pass to an operation as referenced by `operationId` or `operationPath`. The `requestBody` is fully supported in HTTP methods where the HTTP 1.1 specification \[[RFC9110](https://spec.openapis.org/arazzo/latest.html#bib-rfc9110 "HTTP Semantics")\] [Section 9.3](https://tools.ietf.org/html/rfc9110#section-9.3) explicitly defines semantics for “content” like request bodies, such as within POST, PUT, and PATCH methods. For methods where the HTTP specification provides less clarity—such as GET, HEAD, and DELETE—the use of `requestBody` is permitted but does not have well-defined semantics. In these cases, its use *SHOULD* be avoided if possible. |
| successCriteria | \[[Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object)\] | A list of assertions to determine the success of the step. Each assertion is described using a [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object). All assertions `*MUST*` be satisfied for the step to be deemed successful. If `successCriteria` is provided, it `*MUST*` contain at least one [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object). |
| onSuccess | \[[Success Action Object](https://spec.openapis.org/arazzo/latest.html#success-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | An array of success action objects that specify what to do upon step success. If omitted, the next sequential step shall be executed as the default behavior. If multiple success actions have similar `criteria`, the first sequential action matching the criteria *SHALL* be the action executed. If a success action is already defined at the [Workflow](https://spec.openapis.org/arazzo/latest.html#workflow-object), the new definition will override it but can never remove it. If a Reusable Object is provided, it *MUST* link to a success action defined in the [components](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate success actions. |
| onFailure | \[[Failure Action Object](https://spec.openapis.org/arazzo/latest.html#failure-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | An array of failure action objects that specify what to do upon step failure. If omitted, the default behavior is to break and return. If multiple failure actions have similar `criteria`, the first sequential action matching the criteria *SHALL* be the action executed. If a failure action is already defined at the [Workflow](https://spec.openapis.org/arazzo/latest.html#workflow-object), the new definition will override it but can never remove it. If a Reusable Object is provided, it *MUST* link to a failure action defined in the [components](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate failure actions. |
| outputs | Map\[`string`, {expression} | [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object)\] | A map between a friendly name and a dynamic output value defined using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) or [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object). The name *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`. |
| timeout | `integer` | The maximum number of milli-seconds to wait for the step to complete before aborting and failing the step. Consequently this will fail the workflow unless `onFailure` actions are defined. |
| correlationId | `string` | A correlationId in AsyncAPI links a request with its response (or more broadly, to trace a single logical transaction across multiple asynchronous messages). Only applicable to `asyncapi` steps with action `receive` and has to be in-sync with correlationId defined in the AsyncAPI document. |
| action | `string` | Describes the message flow intent. Indicates whether the step will *send (publish)* or *receive (subscribe)* to a channel in an AsyncAPI document. Only applicable for `asyncapi` steps. Possible values are `"send"` or `"receive"`. |
| dependsOn | List\[`string`\] | A list of steps that *MUST* be completed before this step can be executed. `dependsOn` only establishes a prerequisite relationship for the current step and does not trigger execution of the referenced steps. Each value provided *MUST* be a `stepId`. The `stepId` value is case-sensitive. If the step depended on is defined within the **current workflow**, specify the `stepId` directly (e.g., `authStep`). If the step is defined in a **different workflow within the current Arazzo Document**, reference it using `$workflows.<workflowId>.steps.<stepId>`. If the step is defined in a **separate Arazzo Document**, the workflow *MUST* be listed in `sourceDescriptions` and referenced using `$sourceDescriptions.<name>.<workflowId>.steps.<stepId>` to avoid ambiguity. If the step depends on the output of a non-blocking/asynchronous step, then it *SHOULD* use `dependsOn` and refer to the async step using one of these patterns. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.5.2 Step Dependencies and Execution Order

[](https://spec.openapis.org/arazzo/latest.html#step-dependencies-and-execution-order)

The `dependsOn` field at the step level is primarily intended to coordinate asynchronous operations.

###### 5.8.5.2.1 Recommended Approach for Synchronous Workflows

[](https://spec.openapis.org/arazzo/latest.html#recommended-approach-for-synchronous-workflows)

For workflows containing only synchronous steps, the *RECOMMENDED* approach is to order steps sequentially in the steps array without using `dependsOn`. This provides the simplest and clearest execution model. Step-level `dependsOn` is typically unnecessary when all operations complete synchronously and execution follows a linear path.

###### 5.8.5.2.2 Use Case: Async Coordination

[](https://spec.openapis.org/arazzo/latest.html#use-case-async-coordination)

When a step must wait for an asynchronous operation to complete before proceeding, `dependsOn` establishes a join point for in-flight async work. For example, a step that requests an order status *SHOULD* declare `dependsOn` on the step that receives order creation status from an async order placement, even if no explicit output reference exists. This ensures the async operation completes before the dependent step executes.

###### 5.8.5.2.3 Authoring Guidance

[](https://spec.openapis.org/arazzo/latest.html#authoring-guidance)

For async workflows, authors *SHOULD* use `dependsOn` to explicitly declare when a step must wait for async work to complete, regardless of output references. This is the intended use case for step-level dependencies.

###### 5.8.5.2.4 Tool Behavior

[](https://spec.openapis.org/arazzo/latest.html#tool-behavior)

Tools *MUST* respect all declared `dependsOn` relationships. Tools *MUST* also treat runtime expression output references (e.g., `$steps.stepId.outputs.field`) as implicit dependencies and ensure the referenced step completes before the referencing step executes.

Tools supporting only sequential execution *MUST* execute steps in an order that satisfies both explicit (`dependsOn`) and implicit (output reference) dependencies.

###### 5.8.5.2.5 Validation Recommendations

[](https://spec.openapis.org/arazzo/latest.html#validation-recommendations)

Implementations *SHOULD* validate the following scenario:

When no `dependsOn` is used in a workflow (sequential execution model), implementations *SHOULD* produce an error if a step references another step’s outputs where the referenced step appears later in the steps array. This indicates a forward reference that cannot be satisfied in sequential execution.

##### 5.8.5.3 Defining Success for Asynchronous Steps

[](https://spec.openapis.org/arazzo/latest.html#defining-success-for-asynchronous-steps)

For steps that reference AsyncAPI operations (via `operationId` or `channelPath`), tools will send or receive messages on the specified channel as defined by the referenced AsyncAPI description. For AsyncAPI send operations, the step completes immediately after the message is sent. Arazzo does not model broker acknowledgment or delivery confirmation. For AsyncAPI receive operations, step completion depends on message receipt as described below.

Because AsyncAPI channels *MAY* define multiple message types, and because message payloads *MAY* represent either success or failure conditions, authors *SHOULD* define `successCriteria` for AsyncAPI receive steps to explicitly evaluate the received message payload (for example, via `$message.payload`) and determine whether the step succeeded.

Authors *MAY* omit `successCriteria` only when both of the following conditions are met:

-   The channel defines a single message type that unambiguously represents successful completion
-   The message payload does not contain fields indicating error states (e.g., status codes or error flags)

When `successCriteria` is omitted, receiving any message matching the `correlationId` (if specified) within the `timeout` period is considered a successful step completion.

If `correlationId` is specified, only messages matching the correlation identifier are considered. If no matching message is received within the `timeout` period, the step fails and triggers any defined `onFailure` actions.

##### 5.8.5.4 Step Object Examples

[](https://spec.openapis.org/arazzo/latest.html#step-object-examples)

A single step example:

```

stepId: loginStep
description: This step demonstrates the user login step
operationId: loginUser
parameters:
    # parameters to inject into the loginUser operation (parameter name must be resolvable at the referenced operation and the value is determined using {expression} syntax)
    - name: username
      in: query
      value: $inputs.username
    - name: password
      in: query
      value: $inputs.password
successCriteria:
    # assertions to determine step was successful
    - condition: $statusCode == 200
outputs:
    # outputs from this step
    tokenExpires: $response.header.X-Expires-After
    rateLimit: $response.header.X-Rate-Limit
```

A multiple step example:

```

steps:
  - stepId: loginStep
    description: This step demonstrates the user login step
    operationId: loginUser
    parameters:
        # parameters to inject into the loginUser operation (parameter name must be resolvable at the referenced operation and the value is determined using {expression} syntax)
      - name: username
        in: query
        value: $inputs.username
      - name: password
        in: query
        value: $inputs.password
    successCriteria:
        # assertions to determine step was successful
      - condition: $statusCode == 200
    outputs:
        # outputs from this step
        tokenExpires: $response.header.X-Expires-After
        rateLimit: $response.header.X-Rate-Limit
        sessionToken: $response.body
  - stepId: getPetStep
    description: retrieve a pet by status from the GET pets endpoint
    operationPath: '{$sourceDescriptions.petStoreDescription.url}#/paths/~1pet~1findByStatus/get'
    parameters:
      - name: status
        in: query
        value: 'available'
      - name: Authorization
        in: header
        value: $steps.loginStep.outputs.sessionToken
    successCriteria:
      - condition: $statusCode == 200
    outputs:
        # outputs from this step
        availablePets: $response.body
```

An async step example:

```

- stepId: placeOrder
  description: This step demonstrates the action of sending a message payload to place an order
  operationId: $sourceDescriptions.asyncOrderApi.placeOrder
  action: send
  parameters:
      - name: requestId
        in: header
        value: $inputs.correlationId
  requestBody:
      payload:
          productId: $inputs.productDetails.productId
          quantity: $inputs.productDetails.quantity
- stepId: confirmOrder
  description: This step demonstrates the action of receiving a message payload to confirm an order
  operationId: $sourceDescriptions.asyncOrderApi.confirmOrder
  correlationId: $inputs.correlationId
  action: receive
  dependsOn:
    - placeOrder
  timeout: 6000
  outputs:
      orderId: $message.payload.orderId
```

#### 5.8.6 Parameter Object

[](https://spec.openapis.org/arazzo/latest.html#parameter-object)

Describes a single step parameter. A unique parameter is defined by the combination of a `name` and `in` fields. There are several possible locations specified by the `in` field:

-   path - Used together with OpenAPI style [Path Templating](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#path-templating), where the parameter value is actually part of the operation’s URL. This does not include the host or base path of the API. For example, in `/items/{itemId}`, the path parameter is `itemId`.
-   query - Parameters that are appended to the URL as individual key-value pairs. For example, in `/items?id=###`, the query parameter is `id`.
-   querystring - A parameter that treats the entire URL query string as a single value. This parameter location was introduced in [OpenAPI 3.2.0](https://spec.openapis.org/oas/v3.2.0.html) to support scenarios where the complete query string must be passed as a pre-formatted string rather than individual parameters. When a step references an operation that defines a querystring parameter, the value *MUST* match the media type format as expressed by the parameter’s `content` field (e.g., `application/x-www-form-urlencoded`). The `querystring` location cannot coexist with `query` parameters in the same operation per OpenAPI constraints.
-   header - Custom headers that are expected as part of the request. Note that \[[RFC9110](https://spec.openapis.org/arazzo/latest.html#bib-rfc9110 "HTTP Semantics")\] [Name field names](https://tools.ietf.org/html/rfc9110#name-field-names) states field names (which includes header) are case-insensitive.
-   cookie - Used to pass a specific cookie value to the source API.

##### 5.8.6.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-4)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the parameter. Parameter names are *case sensitive*. |
| in | `string` | The location of the parameter. Possible values are `"path"`, `"query"`, `"querystring"`, `"header"`, or `"cookie"`. When the step, success action, or failure action in context specifies a `workflowId`, then all parameters map to workflow inputs. In all other scenarios (e.g., a step specifies an `operationId`), the `in` field *MUST* be specified. |
| value | Any | {expression} | [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object) | ***REQUIRED***. The value to pass in the parameter. The value can be a constant, a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions), or a [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object) to be evaluated and passed to the referenced operation or workflow. For `querystring` parameters, the value *MUST* resolve to a string representing the complete query string (e.g., `"key1=value1&key2=value2"`). Runtime expressions can be embedded within the string value using `{}` notation. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.6.2 Parameter Object Examples

[](https://spec.openapis.org/arazzo/latest.html#parameter-object-examples)

```

# Query Example
- name: username
  in: query
  value: $inputs.username

# Querystring Example (application/x-www-form-urlencoded)
- name: searchParams
  in: querystring
  value: "filter=active&sort=desc&limit=50"

# Querystring with Runtime Expressions (application/x-www-form-urlencoded)
- name: fullQuery
  in: querystring
  value: "category={$inputs.category}&minPrice={$inputs.minPrice}&inStock=true"

# Querystring Example (application/json)
- name: filterParams
  in: querystring
  value: '{"filter":"active","sort":"desc","limit":50}'

# Header Example
- name: X-Api-Key
  in: header
  value: $inputs.x-api-key
```

#### 5.8.7 Success Action Object

[](https://spec.openapis.org/arazzo/latest.html#success-action-object)

A single success action which describes an action to take upon success of a workflow step. There are two possible values for the `type` field:

-   end - The workflow ends, and context returns to the caller with applicable outputs
-   goto - A one-way transfer of workflow control to the specified label (either a `workflowId` or `stepId`)

##### 5.8.7.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-5)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the success action. Names are *case sensitive*. |
| type | `string` | ***REQUIRED***. The type of action to take. Possible values are `"end"` or `"goto"`. |
| workflowId | `string` | The [workflowId](https://spec.openapis.org/arazzo/latest.html#fixed-fields-2) referencing an existing workflow within the Arazzo Description to transfer to upon success of the step. This field is only relevant when the `type` field value is `"goto"`. If the referenced workflow is contained within an `arazzo` type `sourceDescription`, then the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. This field is mutually exclusive to `stepId`. |
| stepId | `string` | The `stepId` to transfer to upon success of the step. This field is only relevant when the `type` field value is `"goto"`. The referenced `stepId` *MUST* be within the current workflow. This field is mutually exclusive to `workflowId`. |
| parameters | \[[Parameter Object](https://spec.openapis.org/arazzo/latest.html#parameter-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | A list of parameters that *MUST* be passed to a workflow as referenced by `workflowId`. If a Reusable Object is provided, it *MUST* link to a parameter defined in the [components/parameters](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate parameters. The `in` field *MUST NOT* be used. |
| criteria | \[[Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object)\] | A list of assertions to determine if this action *SHALL* be executed. Each assertion is described using a [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object). All criteria assertions `*MUST*` be satisfied for the action to be executed. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.7.2 Success Action Object Example

[](https://spec.openapis.org/arazzo/latest.html#success-action-object-example)

```

name: JoinWaitingList
type: goto
stepId: joinWaitingListStep
criteria:
    # assertions to determine if this success action should be executed
    - context: $response.body
      condition: $[?count(@.pets) > 0]
      type: jsonpath
```

#### 5.8.8 Failure Action Object

[](https://spec.openapis.org/arazzo/latest.html#failure-action-object)

A single failure action which describes an action to take upon failure of a workflow step. There are three possible values for the `type` field:

-   end - The workflow ends, and context returns to the caller with applicable outputs
-   retry - The current step will be retried. The retry will be constrained by the `retryAfter` and `retryLimit` fields. If a `stepId` or `workflowId` are specified, then the reference is executed and the context is returned, after which the current step is retried.
-   goto - A one-way transfer of workflow control to the specified label (either a `workflowId` or `stepId`)

##### 5.8.8.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-6)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the failure action. Names are *case sensitive*. |
| type | `string` | ***REQUIRED***. The type of action to take. Possible values are `"end"`, `"retry"`, or `"goto"`. |
| workflowId | `string` | The [workflowId](https://spec.openapis.org/arazzo/latest.html#fixed-fields-2) referencing an existing workflow within the Arazzo Description to transfer to upon failure of the step. This field is only relevant when the `type` field value is `"goto"` or `"retry"`. If the referenced workflow is contained within an `arazzo` type `sourceDescription`, then the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. This field is mutually exclusive to `stepId`. When used with `"retry"`, context transfers back upon completion of the specified workflow. |
| stepId | `string` | The `stepId` to transfer to upon failure of the step. This field is only relevant when the `type` field value is `"goto"` or `"retry"`. The referenced `stepId` *MUST* be within the current workflow. This field is mutually exclusive to `workflowId`. When used with `"retry"`, context transfers back upon completion of the specified step. |
| parameters | \[[Parameter Object](https://spec.openapis.org/arazzo/latest.html#parameter-object) | [Reusable Object](https://spec.openapis.org/arazzo/latest.html#reusable-object)\] | A list of parameters that *MUST* be passed to a workflow as referenced by `workflowId`. If a Reusable Object is provided, it *MUST* link to a parameter defined in the [components/parameters](https://spec.openapis.org/arazzo/latest.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate parameters. The `in` field *MUST NOT* be used. |
| retryAfter | `number` | A non-negative decimal indicating the seconds to delay after the step failure before another attempt *SHALL* be made. **Note:** if an HTTP [Retry-After](https://tools.ietf.org/html/rfc9110.html#name-retry-after) response header was returned to a step from a targeted operation, then it *SHOULD* overrule this particular field value. This field only applies when the `type` field value is `"retry"`. |
| retryLimit | `integer` | A non-negative integer indicating how many attempts to retry the step *MAY* be attempted before failing the overall step. If not specified then a single retry *SHALL* be attempted. This field only applies when the `type` field value is `"retry"`. The `retryLimit` *MUST* be exhausted prior to executing subsequent failure actions. |
| criteria | \[[Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object)\] | A list of assertions to determine if this action *SHALL* be executed. Each assertion is described using a [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.8.2 Failure Action Object Example

[](https://spec.openapis.org/arazzo/latest.html#failure-action-object-example)

```

name: retryStep
type: retry
retryAfter: 1
retryLimit: 5
criteria:
    # assertions to determine if this action should be executed
    - condition: $statusCode == 503
```

#### 5.8.9 Components Object

[](https://spec.openapis.org/arazzo/latest.html#components-object)

Holds a set of reusable objects for different aspects of the Arazzo Specification. All objects defined within the components object will have no effect on the Arazzo Description unless they are explicitly referenced from properties outside the components object.

Components are scoped to the Arazzo document they are defined in. For example, if a step defined in Arazzo document “A” references a workflow defined in Arazzo document “B”, the components in “A” are not considered when evaluating the workflow referenced in “B”.

##### 5.8.9.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-7)

| Field Name | Type | Description |
| --- | --- | --- |
| inputs | Map\[`string`, `JSON Schema`\] | An object to hold reusable JSON Schema objects to be referenced from workflow inputs. |
| parameters | Map\[`string`, [Parameter Object](https://spec.openapis.org/arazzo/latest.html#parameter-object)\] | An object to hold reusable Parameter Objects |
| successActions | Map\[`string`, [Success Action Object](https://spec.openapis.org/arazzo/latest.html#success-action-object)\] | An object to hold reusable Success Actions Objects. |
| failureActions | Map\[`string`, [Failure Action Object](https://spec.openapis.org/arazzo/latest.html#failure-action-object)\] | An object to hold reusable Failure Actions Objects. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

All the fixed fields declared above are objects that *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`. The key is used to refer to the input or parameter in other parts of the Workflow Description.

Field Name Examples:

```

User
User_1
User_Name
user-name
my.org.User
```

##### 5.8.9.2 Components Object Example

[](https://spec.openapis.org/arazzo/latest.html#components-object-example)

```

components:
  parameters:
    storeId:
      name: storeId
      in: header
      value: $inputs.x-store-id
  inputs:
    pagination:
      type: object
      properties:
        page:
          type: integer
          format: int32
        pageSize:
          type: integer
          format: int32
  failureActions:
    refreshToken:
      name: refreshExpiredToken
      type: retry
      retryAfter: 1
      retryLimit: 5
      workflowId: refreshTokenWorkflowId
      criteria:
          # assertions to determine if this action should be executed
          - condition: $statusCode == 401
```

```

"components": {
  "parameters": {
    "storeId": {
      "name": "storeId",
      "in": "header",
      "value": "$inputs.x-store-id"
    }
  },
  "inputs": {
    "pagination": {
      "type": "object",
      "properties": {
        "page": {
          "type": "integer",
          "format": "int32"
        },
        "pageSize": {
          "type": "integer",
          "format": "int32"
        }
      }
    }
  },
  "failureActions": {
    "refreshToken": {
      "name": "refreshExpiredToken",
      "type": "retry",
      "retryAfter": 1,
      "retryLimit": 5,
      "workflowId": "refreshTokenWorkflowId",
      "criteria": [
        {
          "condition": "$statusCode == 401"
        }
      ]
    }
  }
}
```

#### 5.8.10 Reusable Object

[](https://spec.openapis.org/arazzo/latest.html#reusable-object)

A simple object to allow referencing of objects contained within the [Components Object](https://spec.openapis.org/arazzo/latest.html#components-object). It can be used from locations within steps or workflows in the Arazzo Description. **Note** - Input Objects *MUST* use standard JSON Schema referencing via the `$ref` keyword while all non JSON Schema objects use this object and its expression based referencing mechanism.

##### 5.8.10.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-8)

| Field Name | Type | Description |
| --- | --- | --- |
| reference | `{expression}` | ***REQUIRED***. A [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) used to reference the desired object. |
| value | `string` | Sets a value of the referenced parameter. This is only applicable for parameter object references. |

This object cannot be extended with additional properties and any properties added *MUST* be ignored.

##### 5.8.10.2 Reusable Object Example

[](https://spec.openapis.org/arazzo/latest.html#reusable-object-example)

```

  reference: $components.successActions.notify
```

```

  {
    "reference": "$components.successActions.notify"
  }
```

```

  reference: $components.parameters.page
  value: 1
```

```

  {
    "reference": "$components.parameters.page",
    "value": 1
  }
```

#### 5.8.11 Criterion Object

[](https://spec.openapis.org/arazzo/latest.html#criterion-object)

An object used to specify the context, conditions, and condition types that can be used to prove or satisfy assertions specified in [Step Object](https://spec.openapis.org/arazzo/latest.html#step-object) `successCriteria`, [Success Action Object](https://spec.openapis.org/arazzo/latest.html#success-action-object) `criteria`, and [Failure Action Object](https://spec.openapis.org/arazzo/latest.html#failure-action-object) `criteria`.

There are four flavors of conditions supported:

-   simple - where basic literals, operators, and loose comparisons are used in combination with [Runtime Expressions](https://spec.openapis.org/arazzo/latest.html#runtime-expressions).
-   regex - where a regex pattern is applied on the supplied context. The context is defined by a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions).
-   jsonpath - where a JSONPath expression is applied. The root node context is defined by a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions).
-   xpath - where an XPath expression is applied. The root node context is defined by a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions).

##### 5.8.11.1 Literals

[](https://spec.openapis.org/arazzo/latest.html#literals)

As part of a condition expression, you can use `boolean`, `null`, `number`, or `string` data types.

| Type | Literal value |
| --- | --- |
| `boolean` | `true` or `false` |
| `null` | `null` |
| `number` | Any number format supported in [Data Types](https://spec.openapis.org/arazzo/latest.html#data-types). |
| `string` | Strings *MUST* use single quotes (‘) around the string. To use a literal single quote, escape the literal single quote using an additional single quote (’'). |

##### 5.8.11.2 Operators

[](https://spec.openapis.org/arazzo/latest.html#operators)

| Operator | Description |
| --- | --- |
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `==` | Equal |
| `!=` | Not equal |
| `!` | Not |
| `&&` | And |
| `||` | Or |
| `()` | Logical Grouping |
| `[]` | Index (0-based) |
| `.` | Property de-reference |

String comparisons `*MUST*` be case insensitive.

##### 5.8.11.3 Runtime Expressions in Conditions

[](https://spec.openapis.org/arazzo/latest.html#runtime-expressions-in-conditions)

For `simple` conditions, [Runtime Expressions](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) can be used directly within the `condition` field:

```

# Direct usage in simple conditions
successCriteria:
  - condition: $statusCode == 200
  - condition: $response.body.count > $inputs.threshold
```

For `regex`, `jsonpath`, and `xpath` conditions, runtime expressions *MUST* be embedded within the `condition` string using `{}` curly braces. The runtime expressions are evaluated first, then substituted into the condition string before the expression is evaluated:

```

# Embedded expressions in JSONPath
successCriteria:
  - context: $response.body
    condition: '$[?(@.status == "{$inputs.expectedStatus}")]'
    type: jsonpath

# Embedded expressions in XPath
successCriteria:
  - context: $response.body
    condition: '/root/items[price > {$steps.getPricing.outputs.minPrice}]'
    type: xpath

# Embedded expressions in Regex
successCriteria:
  - context: $response.body.status
    condition: '^({$inputs.statusPattern})$'
    type: regex
```

The evaluation order is as follows:

-   Runtime expressions within `{}` are evaluated and converted to strings
-   The resulting string is the final condition expression
-   The condition expression is evaluated according to its `type` (regex, jsonpath, xpath)
-   The result is converted to pass/fail per [Condition Evaluation](https://spec.openapis.org/arazzo/latest.html#condition-evaluation)

The entire `condition` string *MUST* be quoted when it contains embedded expressions to ensure proper YAML parsing.

When runtime expressions are embedded in strings, type conversion follows the rules defined in [Runtime Expressions](https://spec.openapis.org/arazzo/latest.html#runtime-expressions).

##### 5.8.11.4 Condition Evaluation

[](https://spec.openapis.org/arazzo/latest.html#condition-evaluation)

A condition specified in a [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object) *MUST* evaluate to a pass (truthy) or fail (falsy) state. The evaluation semantics depend on the `type` of condition.

###### 5.8.11.4.1 Simple Conditions

[](https://spec.openapis.org/arazzo/latest.html#simple-conditions)

When `type` is `simple` or omitted, the `condition` *MUST* be an expression that combines [Runtime Expressions](https://spec.openapis.org/arazzo/latest.html#runtime-expressions), [literals](https://spec.openapis.org/arazzo/latest.html#literals), and [operators](https://spec.openapis.org/arazzo/latest.html#operators). The condition evaluates to:

A condition passes (truthy) when:

-   The expression evaluates to `true`.
-   A comparison operator (`==`, `!=`, `<`, `>`, `<=`, `>=`) evaluates to true.
-   A logical operator (`&&`, `||`) evaluates to true.

A condition fails (falsy) when:

-   The expression evaluates to `false`.
-   Any comparison or logical operator evaluates to false.
-   The expression evaluates to `null`.

The following type conversion applies:

-   String comparisons *MUST* be case-insensitive.
-   Numeric strings *SHOULD* be coerced to numbers when compared with numeric operators.
-   `null` only equals itself (`null == null` is `true`). Comparing `null` with any other value evaluates to `false`.

Example:

```

# Pass if status code is 200
- condition: $statusCode == 200

# Pass if status code is 200 AND body contains data
- condition: $statusCode == 200 && $response.body.data != null
```

###### 5.8.11.4.2 Regex Conditions

[](https://spec.openapis.org/arazzo/latest.html#regex-conditions)

When `type` is `regex`, the `condition` *MUST* be a valid regular expression pattern, and `context` *MUST* be provided. The condition evaluates to:

-   A condition passes (truthy) when the regex pattern matches the `context` value.
-   A condition fails (falsy) when the regex pattern does not match the `context` value.

If the `context` evaluates to `null` or `undefined`, the condition *MUST* evaluate to *fail*.

Example:

```

# Pass if status code starts with 2 (any 2xx code)
- context: $statusCode
  condition: '^2\d{2}$'
  type: regex
```

###### 5.8.11.4.3 JSONPath Conditions

[](https://spec.openapis.org/arazzo/latest.html#jsonpath-conditions)

When `type` is `jsonpath`, the `condition` *MUST* be a valid JSONPath expression conforming to \[[RFC9535](https://spec.openapis.org/arazzo/latest.html#bib-rfc9535 "JSONPath: Query Expressions for JSON")\], and `context` *MUST* be provided.

JSONPath expressions return a `NodesType` (a nodelist, which is a sequence of zero or more nodes). The condition evaluates to:

-   A condition passes (truthy) when the JSONPath expression returns a non-empty nodelist (one or more nodes).
-   A condition fails (falsy) when the JSONPath expression returns an empty nodelist (zero nodes).

If the `context` evaluates to `null` or `undefined`, or if the JSONPath expression is syntactically invalid, the condition *MUST* evaluate to *fail*.

JSONPath filter expressions (e.g., `$[?count(@.pets) > 0]`) that match nodes will return those nodes in the result nodelist. A filter with no matches returns an empty nodelist.

Example:

```

# Pass if response body contains at least one pet
- context: $response.body
  condition: $[?count(@.pets) > 0]
  type: jsonpath

# Pass if any pets array has elements
- context: $response.body
  condition: $.pets[*]
  type: jsonpath
```

###### 5.8.11.4.4 XPath Conditions

[](https://spec.openapis.org/arazzo/latest.html#xpath-conditions)

When `type` is `xpath`, the `condition` *MUST* be a valid XPath expression conforming to the version specified (default: [XML Path Language 3.1](https://www.w3.org/TR/xpath-31/) or as specified using an [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object)), and `context` *MUST* be provided.

XPath expressions can return different types: boolean, number, string, or node-set. The condition evaluates to:

-   A condition passes (truthy) when:

    -   The XPath expression returns `true` (boolean)
    -   The XPath expression returns a non-zero number
    -   The XPath expression returns a non-empty string
    -   The XPath expression returns a node-set with at least one node
-   A condition fails (falsy) when:

    -   The XPath expression returns `false` (boolean)
    -   The XPath expression returns zero (number)
    -   The XPath expression returns an empty string
    -   The XPath expression returns an empty node-set

If the `context` evaluates to `null` or `undefined`, or if the XPath expression is syntactically invalid, the condition *MUST* evaluate to *fail*.

Type conversion *MUST* follow the Effective Boolean Value (EBV) semantics defined by the XPath version being used. See [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) for version-specific semantics.

Example:

```

# Pass if count of pets is greater than 0 (returns boolean)
- context: $response.body
  condition: count(/root/pets/*) > 0
  type: xpath

# Pass if pets node exists (returns node-set)
- context: $response.body
  condition: /root/pets
  type: xpath
```

###### 5.8.11.4.5 Evaluation Errors

[](https://spec.openapis.org/arazzo/latest.html#evaluation-errors)

If a condition cannot be evaluated due to:

-   Syntax errors in the expression
-   Invalid context (e.g., applying JSONPath to non-JSON data)
-   Runtime evaluation errors (e.g., division by zero, invalid regex)

Then the condition *MUST* evaluate to *fail*, and implementations *SHOULD* log or report the error to aid debugging.

###### 5.8.11.4.6 Multiple Criteria

[](https://spec.openapis.org/arazzo/latest.html#multiple-criteria)

When multiple [Criterion Objects](https://spec.openapis.org/arazzo/latest.html#criterion-object) are specified in `successCriteria` or `criteria` arrays, all conditions *MUST* evaluate to pass (truthy) for the overall criteria to be satisfied. This is equivalent to a logical AND operation across all criteria.

Example:

```

successCriteria:
  # Both conditions must pass
  - condition: $statusCode == 200
  - context: $response.body
    condition: $.data[*]
    type: jsonpath
```

##### 5.8.11.5 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-9)

| Field Name | Type | Description |
| --- | --- | --- |
| context | `{expression}` | A [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) used to set the context for the condition to be applied on. If `type` is specified, then the `context` *MUST* be provided (e.g. `$response.body` would set the context that a JSONPath query expression could be applied to). |
| condition | `string` | ***REQUIRED***. The condition to apply. Conditions can be simple (e.g. `$statusCode == 200` which applies an operator on a value obtained from a runtime expression), or a regex, or a JSONPath expression. For regex or JSONPath, the `type` and `context` *MUST* be specified. |
| type | `string` | [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) | The type of condition to be applied. If specified, the options allowed are `simple`, `regex`, `jsonpath` or `xpath`. If omitted, then the condition is assumed to be `simple`, which at most combines literals, operators and [Runtime Expressions](https://spec.openapis.org/arazzo/latest.html#runtime-expressions). If `jsonpath`, then the expression *MUST* conform to [JSONPath](https://tools.ietf.org/html/rfc9535). If `xpath` the expression *MUST* conform to [XML Path Language 3.1](https://www.w3.org/TR/xpath-31/#d2e24229). Should other variants of JSONPath or XPath be required, then a [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) *MUST* be specified. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.11.6 Criterion Object Examples

[](https://spec.openapis.org/arazzo/latest.html#criterion-object-examples)

A simple Condition example:

```

- condition: $statusCode == 200
```

A regex Condition example:

```

- context: $statusCode
  condition: '^200$'
  type: regex
```

A JSONPath Condition example:

```

- context: $response.body
  condition: $[?count(@.pets) > 0]
  type: jsonpath
```

#### 5.8.12 Expression Type Object

[](https://spec.openapis.org/arazzo/latest.html#expression-type-object)

An object used to describe the type and version of an expression used within a [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object) or [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object).

Defining this object gives the ability to utilize tooling compatible with older versions of either JSONPath or XPath.

##### 5.8.12.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-10)

| Field Name | Type | Description |
| --- | --- | --- |
| type | `string` | ***REQUIRED***. The selector type. The options allowed are `jsonpath`, `xpath`, or `jsonpointer`. |
| version | `string` | ***REQUIRED***. A short hand string representing the version of the expression type being used. The allowed values for JSONPath are `rfc9535` or `draft-goessner-dispatch-jsonpath-00`. The allowed values for XPath are `xpath-30`, `xpath-20`, or `xpath-10`. The allowed value for JSON Pointer is `rfc6901`. |

The supported expression selector types and versions are as follows:

| Type | Allowed Versions | Default |
| --- | --- | --- |
| `jsonpath` | `rfc9535`, `draft-goessner-dispatch-jsonpath-00` | `rfc9535` |
| `xpath` | `xpath-31`, `xpath-30`, `xpath-20`, `xpath-10` | `xpath-31` |
| `jsonpointer` | `rfc6901` (added for completeness) | `rfc6901` |

When used to specify a particular version of JSONPath or XPath, implementations *MUST* apply the semantics defined in that version’s specification. This includes:

-   Query syntax, filter expressions, and function behavior for JSONPath as defined in the specified version.
-   Expression syntax, function library, and type conversion rules (including Effective Boolean Value) for XPath as defined in the specified version.

For [Criterion Object](https://spec.openapis.org/arazzo/latest.html#criterion-object) condition evaluation, the version-specific Effective Boolean Value (EBV) rules *MUST* be used when evaluating XPath expressions:

-   XPath 3.1 (default): [Section 19.1.2 - Effective Boolean Value](https://www.w3.org/TR/xpath-31/#id-ebv)
-   XPath 3.0: [Section 2.4.3 - Effective Boolean Value](https://www.w3.org/TR/xpath-30/#id-ebv)
-   XPath 2.0: [Section 2.4.3 - Effective Boolean Value](https://www.w3.org/TR/xpath20/#id-ebv)
-   XPath 1.0: [Section 4.2 - Boolean Conversions](https://www.w3.org/TR/xpath-10/#booleans)

If this object is not defined, the default version for the selector type *MUST* be used.

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.12.2 Expression Type Examples

[](https://spec.openapis.org/arazzo/latest.html#expression-type-examples)

A JSONPath example:

```

  type: jsonpath
  version: draft-goessner-dispatch-jsonpath-00
```

An XPath example:

```

  type: xpath
  version: xpath-30
```

#### 5.8.13 Selector Object

[](https://spec.openapis.org/arazzo/latest.html#selector-object)

An object which enables fine-grained traversal and precise data selection from structured data such as JSON or XML, using a defined selector syntax such as JSONPath or XPath.

##### 5.8.13.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-11)

| Field Name | Type | Description |
| --- | --- | --- |
| context | {expression} | ***REQUIRED***. A [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) which *MUST* evaluate to structured data (e.g., `$response.body`) and set the context for the selector to be applied on. |
| selector | `string` | ***REQUIRED***.A selector expression (e.g., `$.items[0].id`, `/Envelope/Item`) in the form of JSONPath expression, XPath expression, or JSON Pointer expression. |
| type | `string` | [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) | ***REQUIRED***. The selector expression type to use (e.g., `jsonpath`, `xpath`, or `jsonpointer`). If `jsonpath`, then the expression *MUST* conform to [JSONPath](https://tools.ietf.org/html/rfc9535). If `xpath` the expression *MUST* conform to [XML Path Language 3.1](https://www.w3.org/TR/xpath-31/#d2e24229). Should other variants of JSONPath or XPath be required, then a [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) *MUST* be specified. |

##### 5.8.13.2 Selector Object Examples

[](https://spec.openapis.org/arazzo/latest.html#selector-object-examples)

An output example:

```

  outputs:
    userEmail:
      context: $response.body
      selector: $.user.profile.email
      type: jsonpath
```

A Step RequestBody example:

```

  requestBody:
    contentType: application/json
    payload:
      invoiceId:
        context: $steps.fetchXml.outputs.invoiceXml
        selector: /Invoice/Header/InvoiceNumber
        type:
          type: xpath
          version: xpath-30
```

#### 5.8.14 Request Body Object

[](https://spec.openapis.org/arazzo/latest.html#request-body-object)

A single request body describing the `Content-Type` and request body content to be passed by a step to an operation.

##### 5.8.14.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-12)

| Field Name | Type | Description |
| --- | --- | --- |
| contentType | `string` | The Content-Type for the request content. If omitted then refer to Content-Type specified at the targeted operation to understand serialization requirements. |
| payload | Any | A value representing the request body payload. The value can be a literal value or can contain [Runtime Expressions](https://spec.openapis.org/arazzo/latest.html#runtime-expressions) or [Selector Objects](https://spec.openapis.org/arazzo/latest.html#selector-object) which *MUST* be evaluated prior to calling the referenced operation. To represent examples of media types that cannot be naturally represented in JSON or YAML, use a string value to contain the example, escaping where necessary. |
| replacements | \[[Payload Replacement Object](https://spec.openapis.org/arazzo/latest.html#payload-replacement-object)\] | A list of locations and values to set within a payload. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.14.2 RequestBody Object Examples

[](https://spec.openapis.org/arazzo/latest.html#requestbody-object-examples)

A JSON templated example:

```

  contentType: application/json
  payload: |
    {
      "petOrder": {
        "petId": "{$inputs.pet_id}",
        "couponCode": "{$inputs.coupon_code}",
        "quantity": "{$inputs.quantity}",
        "status": "placed",
        "complete": false
      }
    }
```

A JSON object example:

```

  contentType: application/json
  payload:
    petOrder:
      petId: $inputs.pet_id
      couponCode: $inputs.coupon_code
      quantity: $inputs.quantity
      status: placed
      complete: false
```

A complete Runtime Expression example:

```

  contentType: application/json
  payload: $inputs.petOrderRequest
```

An XML templated example:

```

  contentType: application/xml
  payload: |
    <petOrder>
      <petId>{$inputs.pet_id}</petId>
      <couponCode>{$inputs.coupon_code}</couponCode>
      <quantity>{$inputs.quantity}</quantity>
      <status>placed</status>
      <complete>false</complete>
    </petOrder>
```

A Form Data example:

```

  contentType: application/x-www-form-urlencoded
  payload:
    client_id: $inputs.clientId
    grant_type: $inputs.grantType
    redirect_uri: $inputs.redirectUri
    client_secret: $inputs.clientSecret
    code: $steps.browser-authorize.outputs.code
    scope: $inputs.scope
```

A Form Data String example:

```

  contentType: application/x-www-form-urlencoded
  payload: "client_id={$inputs.clientId}&grant_type={$inputs.grantType}&redirect_uri={$inputs.redirectUri}&client_secret={$inputs.clientSecret}&code{$steps.browser-authorize.outputs.code}&scope=$inputs.scope}"
```

#### 5.8.15 Payload Replacement Object

[](https://spec.openapis.org/arazzo/latest.html#payload-replacement-object)

Describes a location within a payload (e.g., a request body) and a value to set within the location.

##### 5.8.15.1 Fixed Fields

[](https://spec.openapis.org/arazzo/latest.html#fixed-fields-13)

| Field Name | Type | Description |
| --- | --- | --- |
| target | `string` | ***REQUIRED***. A [JSON Pointer](https://tools.ietf.org/html/rfc6901), or [XPath Expression](https://www.w3.org/TR/xpath-31/#id-expressions), or [JSONPath](https://tools.ietf.org/html/rfc9535) which *MUST* be resolved against the request body. Used to identify the location to inject the `value`. |
| targetSelectorType | `string` | [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) | The selector expression type to use (e.g., `jsonpath`, `xpath`, or `jsonpointer`). If `jsonpath`, then the `target` expression *MUST* conform to [JSONPath](https://tools.ietf.org/html/rfc9535). If `xpath` the expression *MUST* conform to [XML Path Language 3.1](https://www.w3.org/TR/xpath-31/#d2e24229). Should other variants of JSONPath or XPath be required, then a [Expression Type Object](https://spec.openapis.org/arazzo/latest.html#expression-type-object) *MUST* be specified. |
| value | Any | {expression} | [Selector Object](https://spec.openapis.org/arazzo/latest.html#selector-object) | ***REQUIRED***. The value set within the target location. The value can be a constant, a [Runtime Expression](https://spec.openapis.org/arazzo/latest.html#runtime-expressions), or [Selector Objects](https://spec.openapis.org/arazzo/latest.html#selector-object) to be evaluated and passed to the referenced operation or workflow. |

If `targetSelectorType` is omitted, then:

-   `target` *MUST* be interpreted as [JSON Pointer](https://tools.ietf.org/html/rfc6901)if the payload is `application/json`.
-   `target` *MUST* be interpreted as [XPath Expression](https://www.w3.org/TR/xpath-31/#id-expressions) if the payload is `application/xml` or another XML-based media type.

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/latest.html#specification-extensions).

##### 5.8.15.2 Payload Replacement Object Examples

[](https://spec.openapis.org/arazzo/latest.html#payload-replacement-object-examples)

A Runtime Expression example:

```

  target: /petId
  value: $inputs.pet_id
```

A literal example:

```

  target: /quantity
  value: 10
```

A JSONPath example using an Expression Type Object:

```

  target: $.items[?(@.sku=='ABC123')].quantity
  targetSelectorType: jsonpath
  value:
    context: $steps.getInventory.outputs.payload
    selector: $.newQuantity
    type: jsonpath
```

An XPath example using older XPATH 3.0:

```

  target: /Envelope/Header/CustomerId
  targetSelectorType:
    type: xpath
    version: xpath-30
  value:
    context: $steps.fetchCustomerData.outputs.xml
    selector: /CustomerInfo/Id
    type:
      type: xpath
      version: xpath-30
```

### 5.9 Runtime Expressions

[](https://spec.openapis.org/arazzo/latest.html#runtime-expressions)

A runtime expression allows values to be defined based on information that will be available within the HTTP message in an actual API call, or within objects serialized from the Arazzo document such as [workflows](https://spec.openapis.org/arazzo/latest.html#workflow-object) or [steps](https://spec.openapis.org/arazzo/latest.html#step-object).

The runtime expression is defined by the following [ABNF](https://tools.ietf.org/html/rfc5234) syntax:

```

  ; Top-level expression
  expression = (
      "$url" /
      "$method" /
      "$statusCode" /
      "$request." source /
      "$response." source /
      "$message." source /
      "$inputs." inputs-reference /
      "$outputs." outputs-reference /
      "$steps." steps-reference /
      "$workflows." workflows-reference /
      "$sourceDescriptions." source-reference /
      "$components." components-reference /
      "$self"
  )

  ; Request/Response sources
  source = ( header-reference / query-reference / path-reference / body-reference / payload-reference )
  header-reference = "header." token
  query-reference = "query." name
  path-reference = "path." name
  body-reference = "body" ["#" json-pointer ]
  payload-reference = "payload" ["#" json-pointer ]

  ; Input/Output references
  inputs-reference = input-name [ "#" json-pointer ]
  outputs-reference = output-name [ "#" json-pointer ]
  input-name = identifier
  output-name = identifier

  ; Steps expressions
  steps-reference = step-id ".outputs." output-name [ "#" json-pointer ]
  step-id = identifier-strict

  ; Workflows expressions
  workflows-reference = workflow-id "." workflow-field "." workflow-field-name [ "#" json-pointer ]
  workflow-id = identifier-strict
  workflow-field = "inputs" / "outputs"
  workflow-field-name = identifier

  ; Source descriptions expressions
  source-reference = source-name "." source-reference-id
  source-name = identifier-strict
  source-reference-id = 1*CHAR
      ; operationIds have no character restrictions in OpenAPI/AsyncAPI
      ; Resolution priority defined in spec text: (1) operationId/workflowId, (2) field names

  ; Components expressions
  components-reference = component-type "." component-name
  component-type = "parameters" / "successActions" / "failureActions"
  component-name = identifier

  ; Identifier rules
  identifier-strict = 1*( ALPHA / DIGIT / "-" / "_" )
      ; For step IDs, workflow IDs, and sourceDescription names (no dots)
      ; Matches [A-Za-z0-9_\-]+

  identifier = 1*( ALPHA / DIGIT / "." / "-" / "_" )
      ; For component keys (dots allowed)
      ; Matches [a-zA-Z0-9\.\-_]+

  name = *( CHAR )
      ; Allows unrestricted characters for query/path parameter names and field references

  ; JSON Pointer (RFC 6901)
  json-pointer = *( "/" reference-token )
  reference-token = *( unescaped / escaped )
  unescaped = %x00-2E / %x30-7A / %x7C / %x7F-10FFFF
      ; Excludes / (%x2F), { (%x7B), } (%x7D), and ~ (%x7E)
  escaped = "~" ( "0" / "1" )
      ; representing '~' and '/', respectively

  ; Token for header names (RFC 9110)
  token = 1*tchar
  tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*" / "+" / "-" / "." /
          "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA

  ; CHAR definition (RFC 7159, adapted to exclude { and })
  CHAR = unescape / escape (
      %x22 /          ; "    quotation mark  U+0022
      %x5C /          ; \    reverse solidus U+005C
      %x2F /          ; /    solidus         U+002F
      %x62 /          ; b    backspace       U+0008
      %x66 /          ; f    form feed       U+000C
      %x6E /          ; n    line feed       U+000A
      %x72 /          ; r    carriage return U+000D
      %x74 /          ; t    tab             U+0009
      %x75 4HEXDIG )  ; uXXXX                U+XXXX
  escape = %x5C       ; \
  unescape = %x20-21 / %x23-5B / %x5D-7A / %x7C / %x7E-10FFFF
      ; Excludes { (%x7B) and } (%x7D) for unambiguous embedded expression parsing

  ; Expression strings
  expression-string = *( literal-char / embedded-expression )
  embedded-expression = "{" expression "}"
  literal-char = %x00-7A / %x7C / %x7E-10FFFF
      ; Excludes { and } - simpler than CHAR for literal text

  ; Core ABNF rules (RFC 5234)
  ALPHA = %x41-5A / %x61-7A   ; A-Z / a-z
  DIGIT = %x30-39             ; 0-9
  HEXDIG = DIGIT / "A" / "B" / "C" / "D" / "E" / "F"
```

Here, `json-pointer` is taken from \[[RFC6901](https://spec.openapis.org/arazzo/latest.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\], `CHAR` from \[[RFC7159](https://spec.openapis.org/arazzo/latest.html#bib-rfc7159 "The JavaScript Object Notation (JSON) Data Interchange Format")\] [Section 7](https://tools.ietf.org/html/rfc7159#section-7) and `token` from \[[RFC7230](https://spec.openapis.org/arazzo/latest.html#bib-rfc7230 "Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing")\] [Section 3.2.6](https://tools.ietf.org/html/rfc7230#section-3.2.6).

The `name` identifier is case-sensitive, whereas `token` is not.

#### 5.9.1 Examples

[](https://spec.openapis.org/arazzo/latest.html#examples)

| Source Location | example expression | notes |
| --- | --- | --- |
| HTTP Method | `$method` | The allowable values for the `$method` will be those for the HTTP operation. |
| Requested media type | `$request.header.accept` |  |
| Request parameter | `$request.path.id` | Request parameters *MUST* be declared in the `parameters` section of the parent operation or they cannot be evaluated. This includes request headers. |
| Request body property | `$request.body#/user/uuid` | In operations which accept payloads, references may be made to portions of the `requestBody` or the entire body. |
| Request URL | `$url` |  |
| Response value | `$response.body#/status` | In operations which return payloads, references may be made to portions of the response body or the entire body. |
| Response array element | `$response.body#/items/0/id` | Array elements can be accessed using numeric indices in JSON Pointer syntax. |
| Response header | `$response.header.Server` | Single header values only are available. |
| Message header | `$message.header.Server` | Single header values only are available. |
| Payload value | `$message.payload#/status` | In operations which return payloads, references may be made to portions of the payload or the entire payload. |
| Self URI | `$self` | References the canonical URI of the current Arazzo Description as defined by the `$self` field. |
| Workflow input | `$inputs.username` or `$workflows.foo.inputs.username` | Single input values only are available. |
| Step output value | `$steps.someStepId.outputs.pets` | In situations where the output named property return payloads, references may be made to portions of the response body (e.g., `$steps.someStepId.outputs.pets#/0/id`) or the entire body. |
| Workflow output value | `$outputs.bar` or `$workflows.foo.outputs.bar` | In situations where the output named property return payloads, references may be made to portions of the response body (e.g., `$workflows.foo.outputs.mappedResponse#/name`) or the entire body. |
| Embedded expressions | `https://{$inputs.host}/api/{$steps.create.outputs.id}/status` | Multiple runtime expressions can be embedded within a single string value by wrapping each in curly braces. |
| Source description reference | `$sourceDescriptions.petstore.getPetById` | References an operationId or workflowId from the named source description. Resolution priority: (1) operationId/workflowId, (2) field names. |
| Source description field | `$sourceDescriptions.petstore.url` | References a field from the Source Description Object. Resolved when no matching operationId/workflowId is found. |
| Components parameter | `$components.parameters.foo` | Accesses a foo parameter defined within the Components Object. |
| Components action | `$components.successActions.bar` or `$components.failureActions.baz` | Accesses a success or failure action defined within the Components Object. |

Runtime expressions preserve the type of the referenced value. Expressions can be embedded into string values by surrounding the expression with `{}` curly braces. When a runtime expression is embedded in this manner, the following rules apply based on the value type:

-   Scalar values (string, number, boolean, null) are converted to their string representation.
-   Complex values (object, array) are handled based on their current representation:
    -   If the value is already a string (e.g., an XML or YAML response body stored without parsing), it is embedded as-is without modification.
    -   If the value is a parsed structure (e.g., a JSON object or array from a parsed response, or workflow input), it *MUST* be serialized as JSON per RFC 8259.

Whether a value is stored as a string or parsed structure depends on its content type. JSON responses and inputs are typically parsed into structures, while XML and plain text are typically stored as strings. When embedding a parsed structure into a non-JSON payload format, the resulting JSON serialization may not match the target format’s expected structure.

#### 5.9.2 Source Description Expression Resolution

[](https://spec.openapis.org/arazzo/latest.html#source-description-expression-resolution)

When using `$sourceDescriptions.<name>.<reference>`, the `<reference>` portion is resolved with the following priority:

-   **operationId or workflowId** - If the referenced source description is an OpenAPI description, `<reference>` is first matched against operationIds. If the source description is an Arazzo document, `<reference>` is matched against workflowIds.
-   **Source description field** - If no operationId/workflowId match is found, `<reference>` is matched against field names of the Source Description Object (e.g., `url`, `type`).

**Examples:**

Given this source description:

```

sourceDescriptions:
  - name: petstore
    url: https://api.example.com/petstore.yaml
    type: openapi
```

Given the above example source description and an OpenAPI description at that specified URL containing an operation with operationId: `getPetById`:

-   `$sourceDescriptions.petstore.getPetById` resolves to the operation with operationId `getPetById` (*priority 1*)
-   `$sourceDescriptions.petstore.url` resolves to `https://api.example.com/petstore.yaml` (*priority 2*)
-   `$sourceDescriptions.petstore.type` resolves to `openapi` (*priority 2*)

If an operationId happens to conflict with a field name (e.g., an operation with operationId: url), the operationId takes precedence.

### 5.10 Specification Extensions

[](https://spec.openapis.org/arazzo/latest.html#specification-extensions)

While the Arazzo Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points.

The extension properties are implemented as patterned fields that are always prefixed by `"x-"`.

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Arazzo Specification. The field name *MUST* begin with `x-`, for example, `x-internal-id`. Field names beginning `x-oai-`, `x-oas-`, and `x-arazzo` are reserved for uses defined by the [OpenAPI Initiative](https://www.openapis.org/). The value *MAY* be `null`, a primitive, an array or an object. |

The extensions may or may not be supported by the available tooling, but those may be extended as well to add requested support (if tools are internal or open-sourced).

## 6\. Security Considerations

[](https://spec.openapis.org/arazzo/latest.html#security-considerations)

The Arazzo Specification does not enforce a security mechanism. Security is left to the implementer, though TLS, specifically HTTPS may be recommended for exchanging sensitive workflows.

Arazzo Descriptions can be JSON or YAML values. As such, all security considerations defined in \[[RFC8259](https://spec.openapis.org/arazzo/latest.html#bib-rfc8259 "The JavaScript Object Notation (JSON) Data Interchange Format")\] and within YAML version [1.2](https://yaml.org/spec/1.2/spec.html) apply.

Arazzo Descriptions are frequently written by untrusted third parties, to be deployed on public Internet servers. Processing an Arazzo Description can cause both safe and unsafe operations to be performed on arbitrary network resources. It is the responsibility of the description consumer to ensure that the operations performed are not harmful.

## 7\. IANA Considerations

[](https://spec.openapis.org/arazzo/latest.html#iana-considerations)

The proposed MIME media types for the Arazzo Specification are described below.

### 7.1 application/vnd.oai.workflows

[](https://spec.openapis.org/arazzo/latest.html#application-vnd-oai-workflows)

The default (or general) MIME type for Arazzo documents (e.g. workflows) is defined as follows:

  Media type name: application

  Media subtype name: vnd.oai.workflows

  Required parameters: N/A

  Optional parameters: version (e.g. version=1.0.0 to indicate that the type of workflow conforms to version 1.0.0 of the Arazzo Specification).

  Encoding considerations: Encoding considerations are identical to those specified for the `application/json` and `application/yaml` media types, respectively.

  Security considerations: See [security considerations](https://spec.openapis.org/arazzo/latest.html#security-considerations) above.

  Interoperability considerations: N/A

**Note:** When using the `application/vnd.oai.workflows` media type the consumer should be prepared to receive YAML formatted content

### 7.2 application/vnd.oai.workflows+json

[](https://spec.openapis.org/arazzo/latest.html#application-vnd-oai-workflows-json)

The proposed MIME media type for Arazzo documents (e.g. workflows) that require a JSON-specific media type is defined as follows:

  Media type name: application

  Media subtype name: vnd.oai.workflows+json

  Required parameters: N/A

  Optional parameters: version (e.g. version=1.0.0 to indicate that the type of Arazzo document conforms to version 1.0.0 of the Arazzo Specification).

  Encoding considerations: Encoding considerations are identical to those specified for the `application/json` media type.

  Security considerations: See [security considerations](https://spec.openapis.org/arazzo/latest.html#security-considerations) above.

  Interoperability considerations: N/A

### 7.3 application/vnd.oai.workflows+yaml

[](https://spec.openapis.org/arazzo/latest.html#application-vnd-oai-workflows-yaml)

The proposed MIME media type for Arazzo documents (e.g. workflows) that require a YAML-specific media type is defined as follows:

  Media type name: application

  Media subtype name: vnd.oai.workflows+yaml

  Required parameters: N/A

  Optional parameters: version (e.g. version=1.0.0 to indicate that the type of Arazzo document conforms to version 1.0.0 of the Arazzo Specification).

  Encoding considerations: Encoding considerations are identical to those specified for the `application/yaml` media type.

  Security considerations: See [security considerations](https://spec.openapis.org/arazzo/latest.html#security-considerations) above.

  Interoperability considerations: N/A

## 8\. Appendix A: Revision History

[](https://spec.openapis.org/arazzo/latest.html#appendix-a-revision-history)

| Version | Date | Notes |
| --- | --- | --- |
| 1.1.0 | 2026-05-17 | Minor release of the Arazzo Specification 1.1.0 |
| 1.0.1 | 2025-01-16 | Patch release of the Arazzo Specification 1.0.1 |
| 1.0.0 | 2024-05-29 | First release of the Arazzo Specification |

## 9\. Appendix B: Examples of Base URI Determination and Reference Resolution

[](https://spec.openapis.org/arazzo/latest.html#appendix-b-examples-of-base-uri-determination-and-reference-resolution)

This appendix provides concrete examples demonstrating how the [`$self`](https://spec.openapis.org/arazzo/latest.html#arazzoSelf) field, Source Description URLs, and relative references work together across different deployment scenarios.

### 9.1 Base URI Within Content (Using `$self`)

[](https://spec.openapis.org/arazzo/latest.html#base-uri-within-content-using-self)

Assume the following Arazzo document is retrieved from `file:///Users/dev/projects/workflows/purchase.arazzo.yaml`:

```

arazzo: 1.1.0
$self: https://api.example.com/workflows/purchase.arazzo.yaml
info:
  title: Pet Purchase Workflow
  version: 1.0.0
sourceDescriptions:
  - name: petstore
    url: ../specs/petstore.yaml  # Resolves to https://api.example.com/specs/petstore.yaml
    type: openapi
```

The relative URL `../specs/petstore.yaml` resolves against the `$self` base URI `https://api.example.com/workflows/purchase.arazzo.yaml`. The resolution algorithm per [RFC3986 Section 5.2](https://tools.ietf.org/html/rfc3986#section-5.2) removes the final path segment during resolution, producing `https://api.example.com/specs/petstore.yaml`, regardless of the retrieval URI.

### 9.2 Base URI From the Retrieval URI (No `$self`)

[](https://spec.openapis.org/arazzo/latest.html#base-uri-from-the-retrieval-uri-no-self)

If the same document does not define `$self`:

```

arazzo: 1.1.0
# No $self field
info:
  title: Pet Purchase Workflow
  version: 1.0.0
sourceDescriptions:
  - name: petstore
    url: ../specs/petstore.yaml
    type: openapi
```

Retrieved from `file:///Users/dev/projects/workflows/purchase.arazzo.yaml`, the relative URL resolves to `file:///Users/dev/projects/specs/petstore.yaml`.

### 9.3 Base URI From Encapsulating Entity

[](https://spec.openapis.org/arazzo/latest.html#base-uri-from-encapsulating-entity)

Per [RFC3986 Section 5.1.2](https://tools.ietf.org/html/rfc3986#section-5.1.2), the base URI can be provided by an encapsulating entity. For example, in a `multipart/related` response where an Arazzo Description is embedded:

```

Content-Type: multipart/related; boundary=example; type=application/vnd.oai.arazzo+json

--example
Content-Type: application/vnd.oai.arazzo+json
Content-Location: https://api.example.com/workflows/purchase.arazzo.json

{
  "arazzo": "1.1.0",
  "info": {...},
  "sourceDescriptions": [
    {
      "name": "petstore",
      "url": "../specs/petstore.json"
    }
  ]
}
--example--
```

The `Content-Location` header provides the base URI (`https://api.example.com/workflows/purchase.arazzo.json`), so `../specs/petstore.json` resolves to `https://api.example.com/specs/petstore.json` even without a `$self` field.

### 9.4 Application-Specific Default Base URI

[](https://spec.openapis.org/arazzo/latest.html#application-specific-default-base-uri)

Per [RFC3986 Section 5.1.4](https://tools.ietf.org/html/rfc3986#section-5.1.4), applications may define default base URIs. For documents loaded without explicit retrieval URIs (e.g., from a database), implementations typically generate a unique base URI per document using a fixed prefix plus a unique identifier.

For example, a workflow orchestration platform might construct base URIs as `https://workflows.example.com/{uuid}` for each document:

```

arazzo: 1.1.0
# No $self field
# Loaded from database, assigned base URI: https://workflows.example.com/a7b3c4d5
info:
  title: Pet Purchase Workflow
  version: 1.0.0
sourceDescriptions:
  - name: petstore
    url: specs/petstore.yaml  # Resolves using application default
```

If the application assigns base URI `https://workflows.example.com/a7b3c4d5` to this document, then `specs/petstore.yaml` resolves to `https://workflows.example.com/specs/petstore.yaml`.

**Note:** While a base URI of `https://workflows.example.com/` (with trailing slash) is technically valid per RFC3986, the final path component is an empty string. In practice, implementations typically assign unique identifiers as the final component to distinguish documents.

### 9.5 Resolving Relative `$self`

[](https://spec.openapis.org/arazzo/latest.html#resolving-relative-self)

When `$self` is itself a relative URI-reference, it must be resolved before being used as a base URI:

```

arazzo: 1.1.0
$self: workflows/purchase.arazzo.yaml
info:
  title: Pet Purchase Workflow
  version: 1.0.0
sourceDescriptions:
  - name: petstore
    url: ../specs/petstore.yaml
```

Retrieved from `https://api.example.com/v2/api-description.yaml`:

1.  First, resolve the `$self` relative reference `workflows/purchase.arazzo.yaml` against the base URI `https://api.example.com/v2/api-description.yaml`, which resolves to `https://api.example.com/v2/workflows/purchase.arazzo.yaml` per [RFC3986 Section 5.2](https://tools.ietf.org/html/rfc3986#section-5.2).
2.  Then resolve the Source Description `url` relative reference `../specs/petstore.yaml` against the resolved `$self` base URI `https://api.example.com/v2/workflows/purchase.arazzo.yaml`, which resolves to `https://api.example.com/v2/specs/petstore.yaml`.

### 9.6 Identity vs Location: Why `$self` Matters

[](https://spec.openapis.org/arazzo/latest.html#identity-vs-location-why-self-matters)

An Arazzo Description may be retrieved from multiple locations but have a single canonical identity. Consider:

```

arazzo: 1.1.0
$self: https://workflows.example.com/canonical/purchase.arazzo.yaml
info:
  title: Pet Purchase Workflow
  version: 1.0.0
```

This document might be:

-   Retrieved from `https://cdn.example.com/cache/abc123.yaml`
-   Retrieved from `file:///local/dev/purchase.arazzo.yaml`
-   Embedded in a `multipart/related` response

In all cases, references to this Arazzo Description *MUST* use `https://workflows.example.com/canonical/purchase.arazzo.yaml` (the `$self` value), not the retrieval location. This ensures that references remain stable even when the document is mirrored, cached, or moved.

Identity-based referencing via `$self` is particularly valuable in security-restricted environments. When deploying document sets behind firewalls or on air-gapped networks, implementations can scan for `$self` values to locate documents from a provided collection without making network requests that security policies might prevent. This enables reference resolution in environments where external network access is restricted or prohibited.

## A. References

[](https://spec.openapis.org/arazzo/latest.html#references)

### A.1 Informative references

[](https://spec.openapis.org/arazzo/latest.html#informative-references)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC3986\]

[Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986). T. Berners-Lee; R. Fielding; L. Masinter. IETF. January 2005. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc3986](https://www.rfc-editor.org/rfc/rfc3986)

\[RFC6901\]

[JavaScript Object Notation (JSON) Pointer](https://www.rfc-editor.org/rfc/rfc6901). P. Bryan, Ed.; K. Zyp; M. Nottingham, Ed. IETF. April 2013. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc6901](https://www.rfc-editor.org/rfc/rfc6901)

\[RFC7159\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc7159). T. Bray, Ed. IETF. March 2014. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7159](https://www.rfc-editor.org/rfc/rfc7159)

\[RFC7230\]

[Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing](https://httpwg.org/specs/rfc7230.html). R. Fielding, Ed.; J. Reschke, Ed. IETF. June 2014. Proposed Standard. URL: [https://httpwg.org/specs/rfc7230.html](https://httpwg.org/specs/rfc7230.html)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[RFC8259\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259). T. Bray, Ed. IETF. December 2017. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc8259](https://www.rfc-editor.org/rfc/rfc8259)

\[RFC9110\]

[HTTP Semantics](https://httpwg.org/specs/rfc9110.html). R. Fielding, Ed.; M. Nottingham, Ed.; J. Reschke, Ed. IETF. June 2022. Internet Standard. URL: [https://httpwg.org/specs/rfc9110.html](https://httpwg.org/specs/rfc9110.html)

\[RFC9535\]

[JSONPath: Query Expressions for JSON](https://www.rfc-editor.org/rfc/rfc9535). S. Gössner, Ed.; G. Normington, Ed.; C. Bormann, Ed. IETF. February 2024. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc9535](https://www.rfc-editor.org/rfc/rfc9535)

[↑](https://spec.openapis.org/arazzo/latest.html#title)
