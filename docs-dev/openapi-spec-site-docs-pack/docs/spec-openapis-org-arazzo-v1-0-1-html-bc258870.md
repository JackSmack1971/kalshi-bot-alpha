---
title: "The Arazzo Specification v1.0.1"
source_url: "https://spec.openapis.org/arazzo/v1.0.1.html"
host: "spec.openapis.org"
depth: 2
selector: "body"
fetched_at: "2026-07-17T17:37:04.244Z"
---
[![OpenAPI Initiative](https://raw.githubusercontent.com/OAI/OpenAPI-Style-Guide/master/graphics/bitmap/OpenAPI_Logo_Pantone.png)](https://openapis.org/)

# The Arazzo Specification v1.0.1

## Version 1.0.1

16 January 2025

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

[Commit history](https://github.com/OAI/Arazzo-Specification/commits/main/versions/1.0.1.md)

[Pull requests](https://github.com/OAI/Arazzo-Specification/pulls)

Copyright © 2025 the Linux Foundation

* * *

## What is the Arazzo Specification?

The Arazzo Specification provides a mechanism that can define sequences of calls and their dependencies to be woven together and expressed in the context of delivering a particular outcome or set of outcomes when dealing with API descriptions (such as OpenAPI descriptions).

## Status of This Document

The source-of-truth for the specification is the GitHub markdown file referenced above.

## 1\. Arazzo Specification

[](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-specification)

### 1.1 Version 1.0.1

[](https://spec.openapis.org/arazzo/v1.0.1.html#version-1-0-1)

The key words “*MUST*”, “*MUST NOT*”, “*REQUIRED*”, “*SHALL*”, “*SHALL NOT*”, “*SHOULD*”, “*SHOULD NOT*”, “*RECOMMENDED*”, “*NOT RECOMMENDED*”, “*MAY*”, and “*OPTIONAL*” in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14) \[[RFC2119](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

This document is licensed under [The Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

## 2\. Introduction

[](https://spec.openapis.org/arazzo/v1.0.1.html#introduction)

Being able to express specific sequences of calls and articulate the dependencies between them to achieve a particular goal is desirable in the context of API descriptions. The aim of the Arazzo Specification is to provide a mechanism that can define sequences of calls and their dependencies to be woven together and expressed in the context of delivering a particular outcome or set of outcomes when dealing with API descriptions (such as OpenAPI descriptions).

The Arazzo Specification can articulate these workflows in a human-readable and machine-readable manner, thus improving the capability of API specifications to tell the story of the API in a manner that can improve the consuming developer experience.

## 3\. Definitions

[](https://spec.openapis.org/arazzo/v1.0.1.html#definitions)

### 3.1 Arazzo Description

[](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-description)

A self-contained document (or set of documents) which defines or describes API workflows (specific sequence of calls to achieve a particular goal in the context of an API definition). An Arazzo Description uses and conforms to the Arazzo Specification, and `*MUST*` contain a valid Arazzo Specification version field (`arazzo`), an [info](https://spec.openapis.org/arazzo/v1.0.1.html#info-object) field, a `sourceDescriptions` field with at least one defined [Source Description](https://spec.openapis.org/arazzo/v1.0.1.html#source-description-object), and there `*MUST*` be at least one [Workflow](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object) defined in the `workflows` fixed field.

## 4\. Specification

[](https://spec.openapis.org/arazzo/v1.0.1.html#specification)

### 4.1 Versions

[](https://spec.openapis.org/arazzo/v1.0.1.html#versions)

The Arazzo Specification is versioned using a `major`.`minor`.`patch` versioning scheme. The `major`.`minor` portion of the version string (for example 1.0) *SHALL* designate the Arazzo feature set. `.patch` versions address errors in, or provide clarifications to, this document, not the feature set. The patch version *SHOULD NOT* be considered by tooling, making no distinction between 1.0.0 and 1.0.1 for example.

### 4.2 Format

[](https://spec.openapis.org/arazzo/v1.0.1.html#format)

An Arazzo Description that conforms to the Arazzo Specification is itself a JSON object, which may be represented either in JSON or YAML format.

All field names in the specification are **case sensitive**. This includes all fields that are used as keys in a map, except where explicitly noted that keys are **case insensitive**.

In order to preserve the ability to round-trip between YAML and JSON formats, YAML version [1.2](https://yaml.org/spec/1.2/spec.html) is *RECOMMENDED* along with some additional constraints:

-   Tags *MUST* be limited to those allowed by the [JSON Schema ruleset](https://yaml.org/spec/1.2/spec.html#id2803231).
-   Keys used in YAML maps *MUST* be limited to a scalar string, as defined by the [YAML Failsafe schema ruleset](https://yaml.org/spec/1.2/spec.html#id2802346).

### 4.3 Arazzo Description Structure

[](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-description-structure)

It is *RECOMMENDED* that the entry Arazzo document be named: `arazzo.json` or `arazzo.yaml`.

An Arazzo Description *MAY* be made up of a single document or be divided into multiple, connected parts at the discretion of the author. If workflows from other documents are being referenced, they *MUST* be included as a [Source Description Object](https://spec.openapis.org/arazzo/v1.0.1.html#source-description-object). In a multi-document description, the document containing the [Arazzo Specification Object](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-specification-object) is known as the **entry Arazzo document**.

### 4.4 Data Types

[](https://spec.openapis.org/arazzo/v1.0.1.html#data-types)

Data types in the Arazzo Specification are based on the types supported by the [JSON Schema Specification Draft 2020-12](https://tools.ietf.org/html/draft-bhutton-json-schema-00#section-4.2.1). Note that integer as a type is also supported and is defined as a JSON number without a fraction or exponent part.

As defined by the [JSON Schema Validation vocabulary](https://tools.ietf.org/html/draft-bhutton-json-schema-validation-00#section-7), data types can have an optional modifier property: `format`. Arazzo additionally supports the formats (similar to the OpenAPI specification) to provide fine detail for primitive data types.

The formats defined are:

| [`type`](https://spec.openapis.org/arazzo/v1.0.1.html#data-types) | `format` | Comments |
| --- | --- | --- |
| `integer` | `int32` | signed 32 bits |
| `integer` | `int64` | signed 64 bits (a.k.a long) |
| `number` | `float` |  |
| `number` | `double` |  |
| `string` | `password` | A hint to UIs to obscure input. |

### 4.5 Relative References in URLs

[](https://spec.openapis.org/arazzo/v1.0.1.html#relative-references-in-urls)

Unless specified otherwise, all properties that are URLs *MAY* be relative references as defined by \[[RFC3986](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://tools.ietf.org/html/rfc3986#section-4.2). Unless specified otherwise, relative references are resolved using the URL of the referring document.

### 4.6 Schema

[](https://spec.openapis.org/arazzo/v1.0.1.html#schema)

In the following description, if a field is not explicitly ***REQUIRED*** or described with a *MUST* or *SHALL*, it can be considered *OPTIONAL*.

#### 4.6.1 Arazzo Specification Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-specification-object)

This is the root object of the [Arazzo Description](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-description).

##### 4.6.1.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields)

| Field Name | Type | Description |
| --- | --- | --- |
| arazzo | `string` | ***REQUIRED***. This string *MUST* be the [version number](https://spec.openapis.org/arazzo/v1.0.1.html#versions) of the Arazzo Specification that the Arazzo Description uses. The `arazzo` field *MUST* be used by tooling to interpret the Arazzo Description. |
| info | [Info Object](https://spec.openapis.org/arazzo/v1.0.1.html#info-object) | ***REQUIRED***. Provides metadata about the workflows contain within the Arazzo Description. The metadata *MAY* be used by tooling as required. |
| sourceDescriptions | \[[Source Description Object](https://spec.openapis.org/arazzo/v1.0.1.html#source-description-object)\] | ***REQUIRED***. A list of source descriptions (such as an OpenAPI description) this Arazzo Description *SHALL* apply to. The list *MUST* have at least one entry. |
| workflows | \[[Workflow Object](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object)\] | ***REQUIRED***. A list of workflows. The list *MUST* have at least one entry. |
| components | [Components Object](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) | An element to hold various schemas for the Arazzo Description. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.1.2 Arazzo Specification Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#arazzo-specification-object-example)

```

arazzo: 1.0.1
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
    operationPath: '{$sourceDescriptions.petstoreDescription.url}#/paths/~1pet~1findByStatus/get'
    parameters:
      - name: status
        in: query
        value: 'available'
      - name: Authorization
        in: header
        value: $steps.loginUser.outputs.sessionToken
    successCriteria:
      - condition: $statusCode == 200
    outputs:
      # outputs from this step
      availablePets: $response.body
  outputs:
      available: $steps.getPetStep.outputs.availablePets
```

#### 4.6.2 Info Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#info-object)

The object provides metadata about API workflows defined in this Arazzo document. The metadata *MAY* be used by the clients if needed.

##### 4.6.2.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-0)

| Field Name | Type | Description |
| --- | --- | --- |
| title | `string` | ***REQUIRED***. A human readable title of the Arazzo Description. |
| summary | `string` | A short summary of the Arazzo Description. |
| description | `string` | A description of the purpose of the workflows defined. [CommonMark syntax](https://spec.commonmark.org/) *MAY* be used for rich text representation. |
| version | `string` | ***REQUIRED***. The version identifier of the Arazzo document (which is distinct from the [Arazzo Specification version](https://spec.openapis.org/arazzo/v1.0.1.html#versions)). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.2.2 Info Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#info-object-example)

```

title: A pet purchasing workflow
summary: This workflow showcases how to purchase a pet through a sequence of API calls
description: |
    This workflow walks you through the steps of searching for, selecting, and purchasing an available pet.
version: 1.0.1
```

#### 4.6.3 Source Description Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#source-description-object)

Describes a source description (such as an OpenAPI description) that will be referenced by one or more workflows described within an Arazzo Description.

An object storing a map between named description keys and location URLs to the source descriptions (such as an OpenAPI description) this Arazzo Description *SHALL* apply to. Each source location `string` *MUST* be in the form of a URI-reference as defined by \[[RFC3986](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.1](https://tools.ietf.org/html/rfc3986#section-4.1).

##### 4.6.3.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-1)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. A unique name for the source description. Tools and libraries *MAY* use the `name` to uniquely identify a source description, therefore, it is *RECOMMENDED* to follow common programming naming conventions. *SHOULD* conform to the regular expression `[A-Za-z0-9_\-]+`. |
| url | `string` | ***REQUIRED***. A URL to a source description to be used by a workflow. If a relative reference is used, it *MUST* be in the form of a URI-reference as defined by \[[RFC3986](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://tools.ietf.org/html/rfc3986#section-4.2). |
| type | `string` | The type of source description. Possible values are `"openapi"` or `"arazzo"`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.3.2 Source Description Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#source-description-object-example)

```

name: petStoreDescription
url: https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml
type: openapi
```

#### 4.6.4 Workflow Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object)

Describes the steps to be taken across one or more APIs to achieve an objective. The workflow object *MAY* define inputs needed in order to execute workflow steps, where the defined steps represent a call to an API operation or another workflow, and a set of outputs.

##### 4.6.4.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-2)

| Field Name | Type | Description |
| --- | --- | --- |
| workflowId | `string` | ***REQUIRED***. Unique string to represent the workflow. The id *MUST* be unique amongst all workflows described in the Arazzo Description. The `workflowId` value is **case-sensitive**. Tools and libraries *MAY* use the `workflowId` to uniquely identify a workflow, therefore, it is *RECOMMENDED* to follow common programming naming conventions. *SHOULD* conform to the regular expression `[A-Za-z0-9_\-]+`. |
| summary | `string` | A summary of the purpose or objective of the workflow. |
| description | `string` | A description of the workflow. [CommonMark syntax](https://spec.commonmark.org/) *MAY* be used for rich text representation. |
| inputs | `JSON Schema` | A JSON Schema 2020-12 object representing the input parameters used by this workflow. |
| dependsOn | \[`string`\] | A list of workflows that *MUST* be completed before this workflow can be processed. Each value provided *MUST* be a `workflowId`. If the workflow depended on is defined within the current Workflow Document, then specify the `workflowId` of the relevant local workflow. If the workflow is defined in a separate Arazzo Document then the workflow *MUST* be defined in the `sourceDescriptions` and the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. |
| steps | \[[Step Object](https://spec.openapis.org/arazzo/v1.0.1.html#step-object)\] | ***REQUIRED***. An ordered list of steps where each step represents a call to an API operation or to another workflow. |
| successActions | \[[Success Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#success-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)\] | A list of success actions that are applicable for all steps described under this workflow. These success actions can be overridden at the step level but cannot be removed there. If a Reusable Object is provided, it *MUST* link to success actions defined in the [components/successActions](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate success actions. |
| failureActions | \[[Failure Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#failure-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)\] | A list of failure actions that are applicable for all steps described under this workflow. These failure actions can be overridden at the step level but cannot be removed there. If a Reusable Object is provided, it *MUST* link to failure actions defined in the [components/failureActions](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate failure actions. |
| outputs | Map\[`string`, {expression}\] | A map between a friendly name and a dynamic output value. The name *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`. |
| parameters | \[[Parameter Object](https://spec.openapis.org/arazzo/v1.0.1.html#parameter-object) | [Reusable Object](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)\] | A list of parameters that are applicable for all steps described under this workflow. These parameters can be overridden at the step level but cannot be removed there. Each parameter *MUST* be passed to an operation or workflow as referenced by `operationId`, `operationPath`, or `workflowId` as specified within each step. If a Reusable Object is provided, it *MUST* link to a parameter defined in the [components/parameters](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate parameters. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.4.2 Workflow Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object-example)

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

#### 4.6.5 Step Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#step-object)

Describes a single workflow step which *MAY* be a call to an API operation ([OpenAPI Operation Object](https://spec.openapis.org/oas/latest.html#operation-object)) or another [Workflow Object](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object).

##### 4.6.5.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-3)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A description of the step. [CommonMark syntax](https://spec.commonmark.org/) *MAY* be used for rich text representation. |
| stepId | `string` | ***REQUIRED***. Unique string to represent the step. The `stepId` *MUST* be unique amongst all steps described in the workflow. The `stepId` value is **case-sensitive**. Tools and libraries *MAY* use the `stepId` to uniquely identify a workflow step, therefore, it is *RECOMMENDED* to follow common programming naming conventions. *SHOULD* conform to the regular expression `[A-Za-z0-9_\-]+`. |
| operationId | `string` | The name of an existing, resolvable operation, as defined with a unique `operationId` and existing within one of the `sourceDescriptions`. The referenced operation will be invoked by this workflow step. If multiple (non `arazzo` type) `sourceDescriptions` are defined, then the `operationId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<operationId>`) to avoid ambiguity or potential clashes. This field is mutually exclusive of the `operationPath` and `workflowId` fields respectively. |
| operationPath | `string` | A reference to a [Source Description Object](https://spec.openapis.org/arazzo/v1.0.1.html#source-description-object) combined with a [JSON Pointer](https://tools.ietf.org/html/rfc6901) to reference an operation. This field is mutually exclusive of the `operationId` and `workflowId` fields respectively. The operation being referenced *MUST* be described within one of the `sourceDescriptions` descriptions. A [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) syntax *MUST* be used to identify the source description document. If the referenced operation has an `operationId` defined then the `operationId` *SHOULD* be preferred over the `operationPath`. |
| workflowId | `string` | The [workflowId](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-2) referencing an existing workflow within the Arazzo Description. If the referenced workflow is contained within an `arazzo` type `sourceDescription`, then the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. The field is mutually exclusive of the `operationId` and `operationPath` fields respectively. |
| parameters | \[[Parameter Object](https://spec.openapis.org/arazzo/v1.0.1.html#parameter-object) | [Reusable Object](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)\] | A list of parameters that *MUST* be passed to an operation or workflow as referenced by `operationId`, `operationPath`, or `workflowId`. If a parameter is already defined at the [Workflow](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object), the new definition will override it but can never remove it. If a Reusable Object is provided, it *MUST* link to a parameter defined in the [components/parameters](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate parameters. |
| requestBody | [Request Body Object](https://spec.openapis.org/arazzo/v1.0.1.html#request-body-object) | The request body to pass to an operation as referenced by `operationId` or `operationPath`. The `requestBody` is fully supported in HTTP methods where the HTTP 1.1 specification \[[RFC9110](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc9110 "HTTP Semantics")\] [Section 9.3](https://tools.ietf.org/html/rfc9110#section-9.3) explicitly defines semantics for “content” like request bodies, such as within POST, PUT, and PATCH methods. For methods where the HTTP specification provides less clarity—such as GET, HEAD, and DELETE—the use of `requestBody` is permitted but does not have well-defined semantics. In these cases, its use *SHOULD* be avoided if possible. |
| successCriteria | \[[Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object)\] | A list of assertions to determine the success of the step. Each assertion is described using a [Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object). All assertions `*MUST*` be satisfied for the step to be deemed successful. |
| onSuccess | \[[Success Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#success-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)\] | An array of success action objects that specify what to do upon step success. If omitted, the next sequential step shall be executed as the default behavior. If multiple success actions have similar `criteria`, the first sequential action matching the criteria *SHALL* be the action executed. If a success action is already defined at the [Workflow](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object), the new definition will override it but can never remove it. If a Reusable Object is provided, it *MUST* link to a success action defined in the [components](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate success actions. |
| onFailure | \[[Failure Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#failure-action-object) | [Reusable Object](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)\] | An array of failure action objects that specify what to do upon step failure. If omitted, the default behavior is to break and return. If multiple failure actions have similar `criteria`, the first sequential action matching the criteria *SHALL* be the action executed. If a failure action is already defined at the [Workflow](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object), the new definition will override it but can never remove it. If a Reusable Object is provided, it *MUST* link to a failure action defined in the [components](https://spec.openapis.org/arazzo/v1.0.1.html#components-object) of the current Arazzo document. The list *MUST NOT* include duplicate failure actions. |
| outputs | Map\[`string`, {expression}\] | A map between a friendly name and a dynamic output value defined using a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions). The name *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.5.2 Step Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#step-object-example)

**Single step**

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

**Multiple steps**

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
        value: $steps.loginUser.outputs.sessionToken
    successCriteria:
      - condition: $statusCode == 200
    outputs:
        # outputs from this step
        availablePets: $response.body
```

#### 4.6.6 Parameter Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#parameter-object)

Describes a single step parameter. A unique parameter is defined by the combination of a `name` and `in` fields. There are four possible locations specified by the `in` field:

-   path - Used together with OpenAPI style [Path Templating](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#path-templating), where the parameter value is actually part of the operation’s URL. This does not include the host or base path of the API. For example, in `/items/{itemId}`, the path parameter is `itemId`.
-   query - Parameters that are appended to the URL. For example, in `/items?id=###`, the query parameter is `id`.
-   header - Custom headers that are expected as part of the request. Note that \[[RFC9110](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc9110 "HTTP Semantics")\] [Name field names](https://tools.ietf.org/html/rfc9110#name-field-names) states field names (which includes header) are case-insensitive.
-   cookie - Used to pass a specific cookie value to the source API.

##### 4.6.6.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-4)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the parameter. Parameter names are *case sensitive*. |
| in | `string` | The location of the parameter. Possible values are `"path"`, `"query"`, `"header"`, or `"cookie"`. When the step in context specifies a `workflowId`, then all parameters map to workflow inputs. In all other scenarios (e.g., a step specifies an `operationId`), the `in` field *MUST* be specified. |
| value | Any | {expression} | ***REQUIRED***. The value to pass in the parameter. The value can be a constant or a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) to be evaluated and passed to the referenced operation or workflow. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.6.2 Parameter Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#parameter-object-example)

**Query Example**

```

- name: username
  in: query
  value: $inputs.username
```

**Header Example**

```

- name: X-Api-Key
  in: header
  value: $inputs.x-api-key
```

#### 4.6.7 Success Action Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#success-action-object)

A single success action which describes an action to take upon success of a workflow step. There are two possible values for the `type` field.

-   end - The workflow ends, and context returns to the caller with applicable outputs
-   goto - A one-way transfer of workflow control to the specified label (either a `workflowId` or `stepId`)

##### 4.6.7.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-5)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the success action. Names are *case sensitive*. |
| type | `string` | ***REQUIRED***. The type of action to take. Possible values are `"end"` or `"goto"`. |
| workflowId | `string` | The [workflowId](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-2) referencing an existing workflow within the Arazzo Description to transfer to upon success of the step. This field is only relevant when the `type` field value is `"goto"`. If the referenced workflow is contained within an `arazzo` type `sourceDescription`, then the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. This field is mutually exclusive to `stepId`. |
| stepId | `string` | The `stepId` to transfer to upon success of the step. This field is only relevant when the `type` field value is `"goto"`. The referenced `stepId` *MUST* be within the current workflow. This field is mutually exclusive to `workflowId`. |
| criteria | \[[Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object)\] | A list of assertions to determine if this action *SHALL* be executed. Each assertion is described using a [Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object). All criteria assertions `*MUST*` be satisfied for the action to be executed. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.7.2 Success Action Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#success-action-object-example)

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

#### 4.6.8 Failure Action Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#failure-action-object)

A single failure action which describes an action to take upon failure of a workflow step. There are three possible values for the `type` field.

-   end - The workflow ends, and context returns to the caller with applicable outputs
-   retry - The current step will be retried. The retry will be constrained by the `retryAfter` and `retryLimit` fields. If a `stepId` or `workflowId` are specified, then the reference is executed and the context is returned, after which the current step is retried.
-   goto - A one-way transfer of workflow control to the specified label (either a `workflowId` or `stepId`)

##### 4.6.8.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-6)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | ***REQUIRED***. The name of the failure action. Names are *case sensitive*. |
| type | `string` | ***REQUIRED***. The type of action to take. Possible values are `"end"`, `"retry"`, or `"goto"`. |
| workflowId | `string` | The [workflowId](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-2) referencing an existing workflow within the Arazzo Description to transfer to upon failure of the step. This field is only relevant when the `type` field value is `"goto"` or `"retry"`. If the referenced workflow is contained within an `arazzo` type `sourceDescription`, then the `workflowId` *MUST* be specified using a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) (e.g., `$sourceDescriptions.<name>.<workflowId>`) to avoid ambiguity or potential clashes. This field is mutually exclusive to `stepId`. When used with `"retry"`, context transfers back upon completion of the specified workflow. |
| stepId | `string` | The `stepId` to transfer to upon failure of the step. This field is only relevant when the `type` field value is `"goto"` or `"retry"`. The referenced `stepId` *MUST* be within the current workflow. This field is mutually exclusive to `workflowId`. When used with `"retry"`, context transfers back upon completion of the specified step. |
| retryAfter | `number` | A non-negative decimal indicating the seconds to delay after the step failure before another attempt *SHALL* be made. **Note:** if an HTTP [Retry-After](https://tools.ietf.org/html/rfc9110.html#name-retry-after) response header was returned to a step from a targeted operation, then it *SHOULD* overrule this particular field value. This field only applies when the `type` field value is `"retry"`. |
| retryLimit | `integer` | A non-negative integer indicating how many attempts to retry the step *MAY* be attempted before failing the overall step. If not specified then a single retry *SHALL* be attempted. This field only applies when the `type` field value is `"retry"`. The `retryLimit` *MUST* be exhausted prior to executing subsequent failure actions. |
| criteria | \[[Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object)\] | A list of assertions to determine if this action *SHALL* be executed. Each assertion is described using a [Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object). |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.8.2 Failure Action Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#failure-action-object-example)

```

name: retryStep
type: retry
retryAfter: 1
retryLimit: 5
criteria:
    # assertions to determine if this action should be executed
    - condition: $statusCode == 503
```

#### 4.6.9 Components Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#components-object)

Holds a set of reusable objects for different aspects of the Arazzo Specification. All objects defined within the components object will have no effect on the Arazzo Description unless they are explicitly referenced from properties outside the components object.

Components are scoped to the Arazzo document they are defined in. For example, if a step defined in Arazzo document “A” references a workflow defined in Arazzo document “B”, the components in “A” are not considered when evaluating the workflow referenced in “B”.

##### 4.6.9.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-7)

| Field Name | Type | Description |
| --- | --- | --- |
| inputs | Map\[`string`, `JSON Schema`\] | An object to hold reusable JSON Schema objects to be referenced from workflow inputs. |
| parameters | Map\[`string`, [Parameter Object](https://spec.openapis.org/arazzo/v1.0.1.html#parameter-object)\] | An object to hold reusable Parameter Objects |
| successActions | Map\[`string`, [Success Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#success-action-object)\] | An object to hold reusable Success Actions Objects. |
| failureActions | Map\[`string`, [Failure Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#failure-action-object)\] | An object to hold reusable Failure Actions Objects. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

All the fixed fields declared above are objects that *MUST* use keys that match the regular expression: `^[a-zA-Z0-9\.\-_]+$`. The key is used to refer to the input or parameter in other parts of the Workflow Description.

Field Name Examples:

```

User
User_1
User_Name
user-name
my.org.User
```

##### 4.6.9.2 Components Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#components-object-example)

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
          "condition": "{$statusCode == 401}"
        }
      ]
    }
  }
}
```

#### 4.6.10 Reusable Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object)

A simple object to allow referencing of objects contained within the [Components Object](https://spec.openapis.org/arazzo/v1.0.1.html#components-object). It can be used from locations within steps or workflows in the Arazzo Description. **Note** - Input Objects *MUST* use standard JSON Schema referencing via the `$ref` keyword while all non JSON Schema objects use this object and its expression based referencing mechanism.

##### 4.6.10.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-8)

| Field Name | Type | Description |
| --- | --- | --- |
| reference | `{expression}` | ***REQUIRED***. A [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) used to reference the desired object. |
| value | `string` | Sets a value of the referenced parameter. This is only applicable for parameter object references. |

This object cannot be extended with additional properties and any properties added *MUST* be ignored.

##### 4.6.10.2 Reusable Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#reusable-object-example)

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

#### 4.6.11 Criterion Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object)

An object used to specify the context, conditions, and condition types that can be used to prove or satisfy assertions specified in [Step Object](https://spec.openapis.org/arazzo/v1.0.1.html#step-object) `successCriteria`, [Success Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#success-action-object) `criteria`, and [Failure Action Object](https://spec.openapis.org/arazzo/v1.0.1.html#failure-action-object) `criteria`.

There are four flavors of conditions supported:

-   simple - where basic literals, operators, and loose comparisons are used in combination with [Runtime Expressions](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions).
-   regex - where a regex pattern is applied on the supplied context. The context is defined by a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions).
-   jsonpath - where a JSONPath expression is applied. The root node context is defined by a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions).
-   xpath - where an XPath expression is applied. The root node context is defined by a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions).

##### 4.6.11.1 Literals

[](https://spec.openapis.org/arazzo/v1.0.1.html#literals)

As part of a condition expression, you can use `boolean`, `null`, `number`, or `string` data types.

| Type | Literal value |
| --- | --- |
| `boolean` | `true` or `false` |
| `null` | `null` |
| `number` | Any number format supported in [Data Types](https://spec.openapis.org/arazzo/v1.0.1.html#data-types) |
| `string` | Strings *MUST* use single quotes (‘) around the string. To use a literal single quote, escape the literal single quote using an additional single quote (’'). |

##### 4.6.11.2 Operators

[](https://spec.openapis.org/arazzo/v1.0.1.html#operators)

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

##### 4.6.11.3 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-9)

| Field Name | Type | Description |
| --- | --- | --- |
| context | `{expression}` | A [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) used to set the context for the condition to be applied on. If `type` is specified, then the `context` *MUST* be provided (e.g. `$response.body` would set the context that a JSONPath query expression could be applied to). |
| condition | `string` | ***REQUIRED***. The condition to apply. Conditions can be simple (e.g. `$statusCode == 200` which applies an operator on a value obtained from a runtime expression), or a regex, or a JSONPath expression. For regex or JSONPath, the `type` and `context` *MUST* be specified. |
| type | `string` | [Criterion Expression Type Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-expression-type-object) | The type of condition to be applied. If specified, the options allowed are `simple`, `regex`, `jsonpath` or `xpath`. If omitted, then the condition is assumed to be `simple`, which at most combines literals, operators and [Runtime Expressions](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions). If `jsonpath`, then the expression *MUST* conform to [JSONPath](https://tools.ietf.org/html/rfc9535). If `xpath` the expression *MUST* conform to [XML Path Language 3.1](https://www.w3.org/TR/xpath-31/#d2e24229). Should other variants of JSONPath or XPath be required, then a [Criterion Expression Type Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-expression-type-object) *MUST* be specified. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.11.4 Criterion Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object-example)

**Simple Condition Example**

```

- condition: $statusCode == 200
```

**Regex Condition Example**

```

- context: $statusCode
  condition: '^200$'
  type: regex
```

**JSONPath Condition Example**

```

- context: $response.body
  condition: $[?count(@.pets) > 0]
  type: jsonpath
```

#### 4.6.12 Criterion Expression Type Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-expression-type-object)

An object used to describe the type and version of an expression used within a [Criterion Object](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-object). If this object is not defined, then the following defaults apply:

-   JSONPath as described by \[[RFC9535](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc9535 "JSONPath: Query Expressions for JSON")\]
-   XPath as described by [XML Path Language 3.1](https://www.w3.org/TR/xpath-31)

Defining this object gives the ability to utilize tooling compatible with older versions of either JSONPath or XPath.

##### 4.6.12.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-10)

| Field Name | Type | Description |
| --- | --- | --- |
| type | `string` | ***REQUIRED***. The type of condition to be applied. The options allowed are `jsonpath` or `xpath`. |
| version | `string` | ***REQUIRED***. A short hand string representing the version of the expression type being used. The allowed values for JSONPath are `draft-goessner-dispatch-jsonpath-00`. The allowed values for XPath are `xpath-30`, `xpath-20`, or `xpath-10`. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.12.2 Criterion Expression Type Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#criterion-expression-type-example)

**JSONPath Example**

```

  type: jsonpath
  version: draft-goessner-dispatch-jsonpath-00
```

**XPath Example**

```

  type: xpath
  version: xpath-30
```

#### 4.6.13 Request Body Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#request-body-object)

A single request body describing the `Content-Type` and request body content to be passed by a step to an operation.

##### 4.6.13.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-11)

| Field Name | Type | Description |
| --- | --- | --- |
| contentType | `string` | The Content-Type for the request content. If omitted then refer to Content-Type specified at the targeted operation to understand serialization requirements. |
| payload | Any | A value representing the request body payload. The value can be a literal value or can contain [Runtime Expressions](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) which *MUST* be evaluated prior to calling the referenced operation. To represent examples of media types that cannot be naturally represented in JSON or YAML, use a string value to contain the example, escaping where necessary. |
| replacements | \[[Payload Replacement Object](https://spec.openapis.org/arazzo/v1.0.1.html#payload-replacement-object)\] | A list of locations and values to set within a payload. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.13.2 RequestBody Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#requestbody-object-example)

**JSON Templated Example**

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

**JSON Object Example**

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

**Complete Runtime Expression**

```

  contentType: application/json
  payload: $inputs.petOrderRequest
```

**XML Templated Example**

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

**Form Data Example**

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

**Form Data String Example**

```

  contentType: application/x-www-form-urlencoded
  payload: "client_id={$inputs.clientId}&grant_type={$inputs.grantType}&redirect_uri={$inputs.redirectUri}&client_secret={$inputs.clientSecret}&code{$steps.browser-authorize.outputs.code}&scope=$inputs.scope}"
```

#### 4.6.14 Payload Replacement Object

[](https://spec.openapis.org/arazzo/v1.0.1.html#payload-replacement-object)

Describes a location within a payload (e.g., a request body) and a value to set within the location.

##### 4.6.14.1 Fixed Fields

[](https://spec.openapis.org/arazzo/v1.0.1.html#fixed-fields-12)

| Field Name | Type | Description |
| --- | --- | --- |
| target | `string` | ***REQUIRED***. A [JSON Pointer](https://tools.ietf.org/html/rfc6901) or [XPath Expression](https://www.w3.org/TR/xpath-31/#id-expressions) which *MUST* be resolved against the request body. Used to identify the location to inject the `value`. |
| value | Any | {expression} | ***REQUIRED***. The value set within the target location. The value can be a constant or a [Runtime Expression](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions) to be evaluated and passed to the referenced operation or workflow. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions).

##### 4.6.14.2 Payload Replacement Object Example

[](https://spec.openapis.org/arazzo/v1.0.1.html#payload-replacement-object-example)

**Runtime Expression Example**

```

  target: /petId
  value: $inputs.pet_id
```

**Literal Example**

```

  target: /quantity
  value: 10
```

### 4.7 Runtime Expressions

[](https://spec.openapis.org/arazzo/v1.0.1.html#runtime-expressions)

A runtime expression allows values to be defined based on information that will be available within the HTTP message in an actual API call, or within objects serialized from the Arazzo document such as [workflows](https://spec.openapis.org/arazzo/v1.0.1.html#workflow-object) or [steps](https://spec.openapis.org/arazzo/v1.0.1.html#step-object).

The runtime expression is defined by the following [ABNF](https://tools.ietf.org/html/rfc5234) syntax:

```

      expression = ( "$url" / "$method" / "$statusCode" / "$request." source / "$response." source / "$inputs." name / "$outputs." name / "$steps." name / "$workflows." name / "$sourceDescriptions." name / "$components." name / "$components.parameters." parameter-name)
      parameter-name = name ; Reuses 'name' rule for parameter names
      source = ( header-reference / query-reference / path-reference / body-reference )
      header-reference = "header." token
      query-reference = "query." name
      path-reference = "path." name
      body-reference = "body" ["#" json-pointer ]
      json-pointer    = *( "/" reference-token )
      reference-token = *( unescaped / escaped )
      unescaped       = %x00-2E / %x30-7D / %x7F-10FFFF
         ; %x2F ('/') and %x7E ('~') are excluded from 'unescaped'
      escaped         = "~" ( "0" / "1" )
        ; representing '~' and '/', respectively
      name = *( CHAR )
      token = 1*tchar
      tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*" / "+" / "-" / "." /
        "^" / "_" / "`" / "|" / "~" / DIGIT / ALPHA
```

#### 4.7.1 Examples

[](https://spec.openapis.org/arazzo/v1.0.1.html#examples)

| Source Location | example expression | notes |
| --- | --- | --- |
| HTTP Method | `$method` | The allowable values for the `$method` will be those for the HTTP operation. |
| Requested media type | `$request.header.accept` |  |
| Request parameter | `$request.path.id` | Request parameters *MUST* be declared in the `parameters` section of the parent operation or they cannot be evaluated. This includes request headers. |
| Request body property | `$request.body#/user/uuid` | In operations which accept payloads, references may be made to portions of the `requestBody` or the entire body. |
| Request URL | `$url` |  |
| Response value | `$response.body#/status` | In operations which return payloads, references may be made to portions of the response body or the entire body. |
| Response header | `$response.header.Server` | Single header values only are available |
| workflow input | `$inputs.username` or `$workflows.foo.inputs.username` | Single input values only are available |
| Step output value | `$steps.someStepId.outputs.pets` | In situations where the output named property return payloads, references may be made to portions of the response body (e.g., `$steps.someStepId.outputs.pets#/0/id`) or the entire body. |
| Workflow output value | `$outputs.bar` or `$workflows.foo.outputs.bar` | In situations where the output named property return payloads, references may be made to portions of the response body (e.g., `$workflows.foo.outputs.mappedResponse#/name`) or the entire body. |
| Components parameter | `$components.parameters.foo` | Accesses a foo parameter defined within the Components Object. |

Runtime expressions preserve the type of the referenced value. Expressions can be embedded into string values by surrounding the expression with `{}` curly braces.

### 4.8 Specification Extensions

[](https://spec.openapis.org/arazzo/v1.0.1.html#specification-extensions)

While the Arazzo Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points.

The extension properties are implemented as patterned fields that are always prefixed by `"x-"`.

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Arazzo Specification. The field name *MUST* begin with `x-`, for example, `x-internal-id`. Field names beginning `x-oai-`, `x-oas-`, and `x-arazzo` are reserved for uses defined by the [OpenAPI Initiative](https://www.openapis.org/). The value *MAY* be `null`, a primitive, an array or an object. |

The extensions may or may not be supported by the available tooling, but those may be extended as well to add requested support (if tools are internal or open-sourced).

## 5\. Security Considerations

[](https://spec.openapis.org/arazzo/v1.0.1.html#security-considerations)

The Arazzo Specification does not enforce a security mechanism. Security is left to the implementer, though TLS, specifically HTTPS may be recommended for exchanging sensitive workflows.

Arazzo Descriptions can be JSON or YAML values. As such, all security considerations defined in \[[RFC8259](https://spec.openapis.org/arazzo/v1.0.1.html#bib-rfc8259 "The JavaScript Object Notation (JSON) Data Interchange Format")\] and within YAML version [1.2](https://yaml.org/spec/1.2/spec.html) apply.

Arazzo Descriptions are frequently written by untrusted third parties, to be deployed on public Internet servers. Processing an Arazzo Description can cause both safe and unsafe operations to be performed on arbitrary network resources. It is the responsibility of the description consumer to ensure that the operations performed are not harmful.

## 6\. IANA Considerations

[](https://spec.openapis.org/arazzo/v1.0.1.html#iana-considerations)

The proposed MIME media types for the Arazzo Specification are described below.

### 6.1 application/vnd.oai.workflows

[](https://spec.openapis.org/arazzo/v1.0.1.html#application-vnd-oai-workflows)

The default (or general) MIME type for Arazzo documents (e.g. workflows) is defined as follows:

  Media type name: application

  Media subtype name: vnd.oai.workflows

  Required parameters: N/A

  Optional parameters: version (e.g. version=1.0.0 to indicate that the type of workflow conforms to version 1.0.0 of the Arazzo Specification).

  Encoding considerations: Encoding considerations are identical to those specified for the `application/json` and `application/yaml` media types, respectively.

  Security considerations: See [security considerations](https://spec.openapis.org/arazzo/v1.0.1.html#security-considerations) above.

  Interoperability considerations: N/A

**Note:** When using the `application/vnd.oai.workflows` media type the consumer should be prepared to receive YAML formatted content

### 6.2 application/vnd.oai.workflows+json

[](https://spec.openapis.org/arazzo/v1.0.1.html#application-vnd-oai-workflows-json)

The proposed MIME media type for Arazzo documents (e.g. workflows) that require a JSON-specific media type is defined as follows:

  Media type name: application

  Media subtype name: vnd.oai.workflows+json

  Required parameters: N/A

  Optional parameters: version (e.g. version=1.0.0 to indicate that the type of Arazzo document conforms to version 1.0.0 of the Arazzo Specification).

  Encoding considerations: Encoding considerations are identical to those specified for the `application/json` media type.

  Security considerations: See [security considerations](https://spec.openapis.org/arazzo/v1.0.1.html#security-considerations) above.

  Interoperability considerations: N/A

### 6.3 application/vnd.oai.workflows+yaml

[](https://spec.openapis.org/arazzo/v1.0.1.html#application-vnd-oai-workflows-yaml)

The proposed MIME media type for Arazzo documents (e.g. workflows) that require a YAML-specific media type is defined as follows:

  Media type name: application

  Media subtype name: vnd.oai.workflows+yaml

  Required parameters: N/A

  Optional parameters: version (e.g. version=1.0.0 to indicate that the type of Arazzo document conforms to version 1.0.0 of the Arazzo Specification).

  Encoding considerations: Encoding considerations are identical to those specified for the `application/yaml` media type.

  Security considerations: See [security considerations](https://spec.openapis.org/arazzo/v1.0.1.html#security-considerations) above.

  Interoperability considerations: N/A

## 7\. Appendix A: Revision History

[](https://spec.openapis.org/arazzo/v1.0.1.html#appendix-a-revision-history)

| Version | Date | Notes |
| --- | --- | --- |
| 1.0.1 | 2025-01-16 | Patch release of the Arazzo Specification 1.0.1 |
| 1.0.0 | 2024-05-29 | First release of the Arazzo Specification |

## A. References

[](https://spec.openapis.org/arazzo/v1.0.1.html#references)

### A.1 Informative references

[](https://spec.openapis.org/arazzo/v1.0.1.html#informative-references)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC3986\]

[Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986). T. Berners-Lee; R. Fielding; L. Masinter. IETF. January 2005. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc3986](https://www.rfc-editor.org/rfc/rfc3986)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[RFC8259\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc8259). T. Bray, Ed. IETF. December 2017. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc8259](https://www.rfc-editor.org/rfc/rfc8259)

\[RFC9110\]

[HTTP Semantics](https://httpwg.org/specs/rfc9110.html). R. Fielding, Ed.; M. Nottingham, Ed.; J. Reschke, Ed. IETF. June 2022. Internet Standard. URL: [https://httpwg.org/specs/rfc9110.html](https://httpwg.org/specs/rfc9110.html)

\[RFC9535\]

[JSONPath: Query Expressions for JSON](https://www.rfc-editor.org/rfc/rfc9535). S. Gössner, Ed.; G. Normington, Ed.; C. Bormann, Ed. IETF. February 2024. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc9535](https://www.rfc-editor.org/rfc/rfc9535)

[↑](https://spec.openapis.org/arazzo/v1.0.1.html#title)
