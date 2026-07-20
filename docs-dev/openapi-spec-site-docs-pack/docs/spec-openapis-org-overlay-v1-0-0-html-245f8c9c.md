---
title: "Overlay Specification v1.0.0"
source_url: "https://spec.openapis.org/overlay/v1.0.0.html"
host: "spec.openapis.org"
depth: 2
selector: "body"
fetched_at: "2026-07-17T17:37:05.302Z"
---
[![OpenAPI Initiative](https://raw.githubusercontent.com/OAI/OpenAPI-Style-Guide/master/graphics/bitmap/OpenAPI_Logo_Pantone.png)](https://openapis.org/)

# Overlay Specification v1.0.0

## Version 1.0.0

17 October 2024

More details about this document

This version:

[https://spec.openapis.org/overlay/v1.0.0.html](https://spec.openapis.org/overlay/v1.0.0.html)

Latest published version:

[https://spec.openapis.org/overlay/latest.html](https://spec.openapis.org/overlay/latest.html)

Latest editor's draft:

[https://github.com/OAI/Overlay-Specification/](https://github.com/OAI/Overlay-Specification/)

Editors:

Darrel Miller

Greg Dennis

Kevin Swiber

Lorna Mitchell

Mike Kistler

Mike Ralphson

Ron Ratovsky

Participate

[GitHub OAI/Overlay-Specification](https://github.com/OAI/Overlay-Specification/)

[File a bug](https://github.com/OAI/Overlay-Specification/issues)

[Commit history](https://github.com/OAI/Overlay-Specification/commits/main/versions/1.0.0.md)

[Pull requests](https://github.com/OAI/Overlay-Specification/pulls)

Copyright © 2024 the Linux Foundation

* * *

## What is the Overlay Specification?

The Overlay Specification defines a document format for information that augments an existing \[[OpenAPI](https://spec.openapis.org/overlay/v1.0.0.html#bib-openapi "OpenAPI Specification")\] description yet remains separate from the OpenAPI description’s source document(s).

## Status of This Document

The source-of-truth for this specification is the HTML file referenced above as *This version*.

## 1\. Overlay Specification

[](https://spec.openapis.org/overlay/v1.0.0.html#overlay-specification)

### 1.1 Version 1.0.0

[](https://spec.openapis.org/overlay/v1.0.0.html#conformance)

The key words “*MUST*”, “*MUST NOT*”, “*REQUIRED*”, “*SHALL*”, “*SHALL NOT*”, “*SHOULD*”, “*SHOULD NOT*”, “*RECOMMENDED*”, “*NOT RECOMMENDED*”, “*MAY*”, and “*OPTIONAL*” in this document are to be interpreted as described in [BCP 14](https://tools.ietf.org/html/bcp14) \[[RFC2119](https://spec.openapis.org/overlay/v1.0.0.html#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\] \[[RFC8174](https://spec.openapis.org/overlay/v1.0.0.html#bib-rfc8174 "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words")\] when, and only when, they appear in all capitals, as shown here.

This document is licensed under [The Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

## 2\. Introduction

[](https://spec.openapis.org/overlay/v1.0.0.html#introduction)

The Overlay Specification is a companion to the \[[OpenAPI](https://spec.openapis.org/overlay/v1.0.0.html#bib-openapi "OpenAPI Specification")\] Specification. An Overlay describes a set of changes to be applied or “overlaid” onto an existing OpenAPI description.

The main purpose of the Overlay Specification is to provide a way to repeatably apply transformations to one or many OpenAPI descriptions. Use cases include updating descriptions, adding metadata to be consumed by another tool, or removing certain elements from an API description before sharing it with partners. An Overlay may be specific to a single OpenAPI description or be designed to apply the same transform to any OpenAPI description.

## 3\. Definitions

[](https://spec.openapis.org/overlay/v1.0.0.html#definitions)

### 3.1 Overlay

[](https://spec.openapis.org/overlay/v1.0.0.html#overlay)

An Overlay is a JSON or YAML structure containing an ordered list of [Action Objects](https://spec.openapis.org/overlay/v1.0.0.html#overlay-actions) that are to be applied to the target document. Each [Action Object](https://spec.openapis.org/overlay/v1.0.0.html#action-object) has a `target` property and a modifier type (`update` or `remove`). The `target` property is a [JSONPath](https://spec.openapis.org/overlay/v1.0.0.html#bib-rfc9535 "JSONPath: Query Expressions for JSON") query expression that identifies the elements of the target document to be updated and the modifier determines the change.

## 4\. Specification

[](https://spec.openapis.org/overlay/v1.0.0.html#specification)

### 4.1 Versions

[](https://spec.openapis.org/overlay/v1.0.0.html#versions)

The Overlay Specification is versioned using a `major`.`minor`.`patch` versioning scheme. The `major`.`minor` portion of the version string (for example 1.0) *SHALL* designate the Overlay feature set. `patch` versions address errors in, or provide clarifications to, this document, not the feature set. The patch version *SHOULD NOT* be considered by tooling, making no distinction between 1.0.0 and 1.0.1 for example.

**Note:** Version 1.0.0 of the Overlay Specification was released after spending some time in draft and being implemented by a few early-adopting tool providers. Check with your tool provider for the details of what is supported in each tool.

### 4.2 Format

[](https://spec.openapis.org/overlay/v1.0.0.html#format)

An Overlay document that conforms to the Overlay Specification is itself a JSON object, which may be represented either in [JSON](https://spec.openapis.org/overlay/v1.0.0.html#bib-rfc7159 "The JavaScript Object Notation (JSON) Data Interchange Format") or [YAML](https://spec.openapis.org/overlay/v1.0.0.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2") format.

All field names in the specification are **case sensitive**. This includes all fields that are used as keys in a map, except where explicitly noted that keys are **case insensitive**.

In order to preserve the ability to round-trip between YAML and JSON formats, [YAML version 1.2](https://spec.openapis.org/overlay/v1.0.0.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2") is *RECOMMENDED* along with some additional constraints:

-   Tags *MUST* be limited to those allowed by the [JSON Schema ruleset](https://yaml.org/spec/1.2/spec.html#id2803231).
-   Keys used in YAML maps *MUST* be limited to a scalar string, as defined by the [YAML Failsafe schema ruleset](https://yaml.org/spec/1.2/spec.html#id2802346).

### 4.3 Relative References in URIs

[](https://spec.openapis.org/overlay/v1.0.0.html#relative-references-in-uris)

Unless specified otherwise, all fields that are URI references *MAY* be relative references as defined by \[[RFC3986](https://spec.openapis.org/overlay/v1.0.0.html#bib-rfc3986 "Uniform Resource Identifier (URI): Generic Syntax")\] [Section 4.2](https://datatracker.ietf.org/doc/html/rfc3986#section-4.2).

### 4.4 Schema

[](https://spec.openapis.org/overlay/v1.0.0.html#schema)

In the following description, if a field is not explicitly ***REQUIRED*** or described with a *MUST* or *SHALL*, it can be considered *OPTIONAL*.

#### 4.4.1 Overlay Object

[](https://spec.openapis.org/overlay/v1.0.0.html#overlay-object)

This is the root object of the [Overlay](https://spec.openapis.org/overlay/v1.0.0.html#overlay).

##### 4.4.1.1 Fixed Fields

[](https://spec.openapis.org/overlay/v1.0.0.html#fixed-fields)

| Field Name | Type | Description |
| --- | --- | --- |
| overlay | `string` | ***REQUIRED***. This string *MUST* be the [version number](https://spec.openapis.org/overlay/v1.0.0.html#versions) of the Overlay Specification that the Overlay document uses. The `overlay` field *SHOULD* be used by tooling to interpret the Overlay document. |
| info | [Info Object](https://spec.openapis.org/overlay/v1.0.0.html#info-object) | ***REQUIRED***. Provides metadata about the Overlay. The metadata *MAY* be used by tooling as required. |
| extends | `string` | URI reference that identifies the target document (such as an \[[OpenAPI](https://spec.openapis.org/overlay/v1.0.0.html#bib-openapi "OpenAPI Specification")\] document) this overlay applies to. |
| actions | \[[Action Object](https://spec.openapis.org/overlay/v1.0.0.html#action-object)\] | ***REQUIRED*** An ordered list of actions to be applied to the target document. The array *MUST* contain at least one value. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/overlay/v1.0.0.html#specification-extensions).

The list of actions *MUST* be applied in sequential order to ensure a consistent outcome. Actions are applied to the result of the previous action. This enables objects to be deleted in one action and then re-created in a subsequent action, for example.

The `extends` property can be used to indicate that the Overlay was designed to update a specific \[[OpenAPI](https://spec.openapis.org/overlay/v1.0.0.html#bib-openapi "OpenAPI Specification")\] document. Where no `extends` is provided it is the responsibility of tooling to apply the Overlay document to the appropriate OpenAPI document(s).

In the following example the `extends` property specifies that the overlay is designed to update the OpenAPI Tic Tac Toe example document, identified by an absolute URI.

```
overlay: 1.0.0
info:
  title: Overlay for the Tic Tac Toe API document
  version: 1.0.0
extends: 'https://raw.githubusercontent.com/OAI/learn.openapis.org/refs/heads/main/examples/v3.1/tictactoe.yaml'
...
```

The `extends` property can also specify a relative URI reference.

```
overlay: 1.0.0
info:
  title: Overlay for the Tic Tac Toe API document
  version: 1.0.0
extends: './tictactoe.yaml'
```

#### 4.4.2 Info Object

[](https://spec.openapis.org/overlay/v1.0.0.html#info-object)

The object provides metadata about the Overlay. The metadata *MAY* be used by the clients if needed.

##### 4.4.2.1 Fixed Fields

[](https://spec.openapis.org/overlay/v1.0.0.html#fixed-fields-0)

| Field Name | Type | Description |
| --- | --- | --- |
| title | `string` | ***REQUIRED***. A human readable description of the purpose of the overlay. |
| version | `string` | ***REQUIRED***. A version identifer for indicating changes to the Overlay document. |

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/overlay/v1.0.0.html#specification-extensions).

#### 4.4.3 Action Object

[](https://spec.openapis.org/overlay/v1.0.0.html#action-object)

This object represents one or more changes to be applied to the target document at the location defined by the target JSONPath expression.

##### 4.4.3.1 Fixed Fields

[](https://spec.openapis.org/overlay/v1.0.0.html#fixed-fields-1)

| Field Name | Type | Description |
| --- | --- | --- |
| target | `string` | ***REQUIRED*** A JSONPath expression selecting nodes in the target document. |
| description | `string` | A description of the action. \[[CommonMark](https://spec.openapis.org/overlay/v1.0.0.html#bib-commonmark "CommonMark Spec")\] syntax *MAY* be used for rich text representation. |
| update | Any | If the `target` selects an object node, the value of this field *MUST* be an object with the properties and values to merge with the selected node. If the `target` selects an array, the value of this field *MUST* be an entry to append to the array. This field has no impact if the `remove` field of this action object is `true`. |
| remove | `boolean` | A boolean value that indicates that the target object or array *MUST* be removed from the the map or array it is contained in. The default value is `false`. |

The result of the `target` JSONPath expression *MUST* be zero or more objects or arrays (not primitive types or `null` values).

To update a primitive property value such as a string, the `target` expression should select the *containing* object in the target document and `update` should contain an object with the property and its new primitive value.

Primitive-valued items of an array cannot be replaced or removed individually, only the complete array can be replaced.

The properties of the `update` object *MUST* be compatible with the target object referenced by the JSONPath key. When the Overlay document is applied, the properties in the `update` object are recursively merged with the properties in the target object with the same names; new properties are added to the target object.

This object *MAY* be extended with [Specification Extensions](https://spec.openapis.org/overlay/v1.0.0.html#specification-extensions).

### 4.5 Examples

[](https://spec.openapis.org/overlay/v1.0.0.html#examples)

#### 4.5.1 Structured Overlay Example

[](https://spec.openapis.org/overlay/v1.0.0.html#structured-overlay-example)

When updating properties throughout the target document it may be more efficient to create a single `Action Object` that mirrors the structure of the target document. e.g.

```
overlay: 1.0.0
info:
  title: Structured Overlay
  version: 1.0.0
actions:
  - target: '$' # Root of document
    update:
      info:
        x-overlay-applied: structured-overlay
      paths:
        '/':
          summary: 'The root resource'
          get:
            summary: 'Retrieve the root resource'
            x-rate-limit: 100
        '/pets':
          get:
            summary: 'Retrieve a list of pets'
            x-rate-limit: 100
      components:
      tags:
```

#### 4.5.2 Targeted Overlay Example

[](https://spec.openapis.org/overlay/v1.0.0.html#targeted-overlay-example)

Alternatively, where only a small number of updates need to be applied to a large document, each [Action Object](https://spec.openapis.org/overlay/v1.0.0.html#action-object) *MAY* be more targeted.

```
overlay: 1.0.0
info:
  title: Targeted Overlay
  version: 1.0.0
actions:
  - target: $.paths['/foo'].get
    update:
      description: This is the new description
  - target: $.paths['/bar'].get
    update:
      description: This is the updated description
  - target: $.paths['/bar']
    update:
      post:
        description: This is an updated description of a child object
        x-safe: false
```

#### 4.5.3 Wildcard Overlay Example

[](https://spec.openapis.org/overlay/v1.0.0.html#wildcard-overlay-example)

One significant advantage of using the JSONPath syntax is that it allows referencing multiple nodes in the target document. This would allow a single update object to be applied to multiple target objects using wildcards and other multi-value selectors.

```
overlay: 1.0.0
info:
  title: Update many objects at once
  version: 1.0.0
actions:
  - target: $.paths.*.get
    update:
      x-safe: true
  - target: $.paths.*.get.parameters[?@.name=='filter' && @.in=='query']
    update:
      schema:
        $ref: '/components/schemas/filterSchema'
```

#### 4.5.4 Array Modification Example

[](https://spec.openapis.org/overlay/v1.0.0.html#array-modification-example)

Array elements *MAY* be deleted using the `remove` property. Use of array indexes to remove array items should be avoided where possible as indexes will change when items are removed.

```
overlay: 1.0.0
info:
  title: Add an array element
  version: 1.0.0
actions:
  - target: $.paths.*.get.parameters
    update:
      name: newParam
      in: query
```

```
overlay: 1.0.0
info:
  title: Remove a array element
  version: 1.0.0
actions:
  - target: $.paths.*.get.parameters[?@.name == 'dummy']
    remove: true
```

#### 4.5.5 Traits Example

[](https://spec.openapis.org/overlay/v1.0.0.html#traits-example)

By annotating a target document (such as an \[[OpenAPI](https://spec.openapis.org/overlay/v1.0.0.html#bib-openapi "OpenAPI Specification")\] document) using [Specification Extensions](https://spec.openapis.org/overlay/v1.0.0.html#specification-extensions) such as `x-oai-traits`, the author of the target document *MAY* identify where overlay updates should be applied.

```
openapi: 3.1.0
info:
  title: API with a paged collection
  version: 1.0.0
paths:
  /items:
    get:
      x-oai-traits: ['paged']
      responses:
        200:
          description: OK
```

With the above OpenAPI document, the following Overlay document will apply the necessary updates to describe how paging is implemented, where that trait has been applied.

```
overlay: 1.0.0
info:
  title: Apply Traits
  version: 1.0.0
actions:
  - target: $.paths.*.get[?@.x-oai-traits.paged]
    update:
      parameters:
        - name: top
          in: query
          # ...
        - name: skip
          in: query
          # ...
```

This approach allows inversion of control as to where the Overlay updates apply to the target document itself.

### 4.6 Specification Extensions

[](https://spec.openapis.org/overlay/v1.0.0.html#specification-extensions)

While the Overlay Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points.

The extension properties are implemented as patterned fields that are always prefixed by `"x-"`.

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Overlay Specification. The field name *MUST* begin with `x-`, for example, `x-internal-id`. Field names beginning `x-oai-` and `x-oas-` are reserved for uses defined by the [OpenAPI Initiative](https://www.openapis.org/). The value *MAY* be `null`, a primitive, an array or an object. |

The extensions may or may not be supported by the available tooling, but those may be extended as well to add requested support (if tools are internal or open-sourced).

## A. Appendix A: Revision History

[](https://spec.openapis.org/overlay/v1.0.0.html#appendix-a-revision-history)

| Version | Date | Notes |
| --- | --- | --- |
| 1.0.0 | 2024-10-17 | First release of the Overlay Specification |

## B. References

[](https://spec.openapis.org/overlay/v1.0.0.html#references)

### B.1 Normative references

[](https://spec.openapis.org/overlay/v1.0.0.html#normative-references)

\[CommonMark\]

[CommonMark Spec](https://spec.commonmark.org/). URL: [https://spec.commonmark.org/](https://spec.commonmark.org/)

\[OpenAPI\]

[OpenAPI Specification](https://www.openapis.org/). Darrell Miller; Jason Harmon; Jeremy Whitlock; Marsh Gardiner; Mike Ralphson; Ron Ratovsky; Tony Tam; Uri Sarid. OpenAPI Initiative. URL: [https://www.openapis.org/](https://www.openapis.org/)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC3986\]

[Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986). T. Berners-Lee; R. Fielding; L. Masinter. IETF. January 2005. Internet Standard. URL: [https://www.rfc-editor.org/rfc/rfc3986](https://www.rfc-editor.org/rfc/rfc3986)

\[RFC7159\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc7159). T. Bray, Ed. IETF. March 2014. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7159](https://www.rfc-editor.org/rfc/rfc7159)

\[RFC8174\]

[Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words](https://www.rfc-editor.org/rfc/rfc8174). B. Leiba. IETF. May 2017. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc8174](https://www.rfc-editor.org/rfc/rfc8174)

\[RFC9535\]

[JSONPath: Query Expressions for JSON](https://www.rfc-editor.org/rfc/rfc9535). S. Gössner, Ed.; G. Normington, Ed.; C. Bormann, Ed. IETF. February 2024. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc9535](https://www.rfc-editor.org/rfc/rfc9535)

\[YAML\]

[YAML Ain’t Markup Language (YAML™) Version 1.2](http://yaml.org/spec/1.2/spec.html). Oren Ben-Kiki; Clark Evans; Ingy döt Net. 1 October 2009. URL: [http://yaml.org/spec/1.2/spec.html](http://yaml.org/spec/1.2/spec.html)

[↑](https://spec.openapis.org/overlay/v1.0.0.html#title)
