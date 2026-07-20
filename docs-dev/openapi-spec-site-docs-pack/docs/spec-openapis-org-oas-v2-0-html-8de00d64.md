---
title: "OpenAPI Specification v2.0"
source_url: "https://spec.openapis.org/oas/v2.0.html"
host: "spec.openapis.org"
depth: 1
selector: "body"
fetched_at: "2026-07-17T17:36:58.844Z"
---
[![OpenAPI Initiative](https://raw.githubusercontent.com/OAI/OpenAPI-Style-Guide/master/graphics/bitmap/OpenAPI_Logo_Pantone.png)](https://openapis.org/)

# OpenAPI Specification v2.0

## Version 2.0

08 September 2014

More details about this document

This version:

[https://spec.openapis.org/oas/v2.0.html](https://spec.openapis.org/oas/v2.0.html)

Latest published version:

[https://spec.openapis.org/oas/latest.html](https://spec.openapis.org/oas/latest.html)

Latest editor's draft:

[https://github.com/OAI/OpenAPI-Specification/](https://github.com/OAI/OpenAPI-Specification/)

Editors:

Jeremy Whitlock

Marsh Gardiner

Ron Ratovsky

Tony Tam

Other versions:

[https://spec.openapis.org/oas/v3.2.0.html](https://spec.openapis.org/oas/v3.2.0.html)

[https://spec.openapis.org/oas/v3.1.2.html](https://spec.openapis.org/oas/v3.1.2.html)

[https://spec.openapis.org/oas/v3.1.1.html](https://spec.openapis.org/oas/v3.1.1.html)

[https://spec.openapis.org/oas/v3.1.0.html](https://spec.openapis.org/oas/v3.1.0.html)

[https://spec.openapis.org/oas/v3.0.4.html](https://spec.openapis.org/oas/v3.0.4.html)

[https://spec.openapis.org/oas/v3.0.3.html](https://spec.openapis.org/oas/v3.0.3.html)

[https://spec.openapis.org/oas/v3.0.2.html](https://spec.openapis.org/oas/v3.0.2.html)

[https://spec.openapis.org/oas/v3.0.1.html](https://spec.openapis.org/oas/v3.0.1.html)

[https://spec.openapis.org/oas/v3.0.0.html](https://spec.openapis.org/oas/v3.0.0.html)

Participate

[GitHub OAI/OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification/)

[File a bug](https://github.com/OAI/OpenAPI-Specification/issues)

[Commit history](https://github.com/OAI/OpenAPI-Specification/commits/main/versions/2.0.md)

[Pull requests](https://github.com/OAI/OpenAPI-Specification/pulls)

Copyright © 2014 the Linux Foundation

* * *

## What is the OpenAPI Specification?

The OpenAPI Specification (OAS) defines a standard, programming language-agnostic interface description for HTTP APIs, which allows both humans and computers to discover and understand the capabilities of a service without requiring access to source code, additional documentation, or inspection of network traffic. When properly defined via OpenAPI, a consumer can understand and interact with the remote service with a minimal amount of implementation logic. Similar to what interface descriptions have done for lower-level programming, the OpenAPI Specification removes guesswork in calling a service.

## Status of This Document

The source-of-truth for this specification is the HTML file referenced above as *This version*.

## 1\. OpenAPI Specification

[](https://spec.openapis.org/oas/v2.0.html#openapi-specification)

## 2\. (fka Swagger RESTful API Documentation Specification)

[](https://spec.openapis.org/oas/v2.0.html#fka-swagger-restful-api-documentation-specification)

### 2.1 Version 2.0

[](https://spec.openapis.org/oas/v2.0.html#conformance)

The key words “*MUST*”, “*MUST NOT*”, “*REQUIRED*”, “*SHALL*”, “*SHALL NOT*”, “*SHOULD*”, “*SHOULD NOT*”, “*RECOMMENDED*”, “*MAY*”, and “*OPTIONAL*” in this document are to be interpreted as described in \[[RFC2119](https://spec.openapis.org/oas/v2.0.html#bib-rfc2119 "Key words for use in RFCs to Indicate Requirement Levels")\].

The Swagger specification is licensed under [The Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

## 3\. Introductions

[](https://spec.openapis.org/oas/v2.0.html#introductions)

Swagger™ is a project used to describe and document RESTful APIs.

The Swagger specification defines a set of files required to describe such an API. These files can then be used by the Swagger-UI project to display the API and Swagger-Codegen to generate clients in various languages. Additional utilities can also take advantage of the resulting files, such as testing tools.

## 4\. Revision History

[](https://spec.openapis.org/oas/v2.0.html#revision-history)

| Version | Date | Notes |
| --- | --- | --- |
| 2.0 | 2014-09-08 | Release of Swagger 2.0 |
| 1.2 | 2014-03-14 | Initial release of the formal document. |
| 1.1 | 2012-08-22 | Release of Swagger 1.1 |
| 1.0 | 2011-08-10 | First release of the Swagger Specification |

## 5\. Definitions

[](https://spec.openapis.org/oas/v2.0.html#definitions)

### 5.1 Path Templating

[](https://spec.openapis.org/oas/v2.0.html#path-templating)

Path templating refers to the usage of curly braces ({}) to mark a section of a URL path as replaceable using path parameters.

### 5.2 Mime Types

[](https://spec.openapis.org/oas/v2.0.html#mime-types)

Mime type definitions are spread across several resources. The mime type definitions should be in compliance with \[[RFC6838](https://spec.openapis.org/oas/v2.0.html#bib-rfc6838 "Media Type Specifications and Registration Procedures")\].

Some examples of possible mime type definitions:

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

### 5.3 HTTP Status Codes

[](https://spec.openapis.org/oas/v2.0.html#http-status-codes)

The HTTP Status Codes are used to indicate the status of the executed operation. The available status codes are described by \[[RFC7231](https://spec.openapis.org/oas/v2.0.html#bib-rfc7231 "Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content")\] [Section 6](https://datatracker.ietf.org/doc/html/rfc7231#section-6) and in the [IANA Status Code Registry](https://spec.openapis.org/oas/v2.0.html#bib-iana-http-status-codes "Hypertext Transfer Protocol (HTTP) Status Code Registry").

## 6\. Specification

[](https://spec.openapis.org/oas/v2.0.html#specification)

### 6.1 Format

[](https://spec.openapis.org/oas/v2.0.html#format)

The files describing the RESTful API in accordance with the Swagger specification are represented as JSON objects and conform to the [JSON](https://spec.openapis.org/oas/v2.0.html#bib-rfc7159 "The JavaScript Object Notation (JSON) Data Interchange Format") standards. [YAML](https://spec.openapis.org/oas/v2.0.html#bib-yaml "YAML Ain’t Markup Language (YAML™) Version 1.2"), being a superset of JSON, can be used as well to represent a Swagger specification file.

For example, if a field is said to have an array value, the JSON array representation will be used:

```
{
   "field" : [...]
}
```

While the API is described using JSON it does not impose a JSON input/output to the API itself.

All field names in the specification are **case sensitive**.

The schema exposes two types of fields. Fixed fields, which have a declared name, and Patterned fields, which declare a regex pattern for the field name. Patterned fields can have multiple occurrences as long as each has a unique name.

### 6.2 File Structure

[](https://spec.openapis.org/oas/v2.0.html#file-structure)

The Swagger representation of the API is made of a single file. However, parts of the definitions can be split into separate files, at the discretion of the user. This is applicable for `$ref` fields in the specification as follows from the [JSON Schema](https://json-schema.org/) definitions.

By convention, the Swagger specification file is named `swagger.json`.

### 6.3 Data Types

[](https://spec.openapis.org/oas/v2.0.html#data-types)

Primitive data types in the Swagger Specification are based on the types supported by the [JSON-Schema Draft 4](https://tools.ietf.org/html/draft-zyp-json-schema-04#section-3.5). Models are described using the [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object) which is a subset of JSON Schema Draft 4.

An additional primitive data type `"file"` is used by the [Parameter Object](https://spec.openapis.org/oas/v2.0.html#parameter-object) and the [Response Object](https://spec.openapis.org/oas/v2.0.html#response-object) to set the parameter type or the response as being a file.

Primitives have an optional modifier property `format`. Swagger uses several known formats to more finely define the data type being used. However, the `format` property is an open `string`\-valued property, and can have any value to support documentation needs. Formats such as `"email"`, `"uuid"`, etc., can be used even though they are not defined by this specification. Types that are not accompanied by a `format` property follow their definition from the JSON Schema (except for `file` type which is defined above). The formats defined by the Swagger Specification are:

| Common Name | [`type`](https://spec.openapis.org/oas/v2.0.html#dataTypeType) | [`format`](https://spec.openapis.org/oas/v2.0.html#dataTypeFormat) | Comments |
| --- | --- | --- | --- |
| integer | `integer` | `int32` | signed 32 bits |
| long | `integer` | `int64` | signed 64 bits |
| float | `number` | `float` |  |
| double | `number` | `double` |  |
| string | `string` |  |  |
| byte | `string` | `byte` | base64 encoded characters |
| binary | `string` | `binary` | any sequence of octets |
| boolean | `boolean` |  |  |
| date | `string` | `date` | As defined by `full-date` - \[[RFC3339](https://spec.openapis.org/oas/v2.0.html#bib-rfc3339 "Date and Time on the Internet: Timestamps")\] [Section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) |
| dateTime | `string` | `date-time` | As defined by `date-time` - \[[RFC3339](https://spec.openapis.org/oas/v2.0.html#bib-rfc3339 "Date and Time on the Internet: Timestamps")\] [Section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6) |
| password | `string` | `password` | Used to hint UIs the input needs to be obscured. |

### 6.4 Schema

[](https://spec.openapis.org/oas/v2.0.html#schema)

#### 6.4.1 Swagger Object

[](https://spec.openapis.org/oas/v2.0.html#swagger-object)

This is the root document object for the API specification. It combines what previously was the Resource Listing and API Declaration (version 1.2 and earlier) together into one document.

##### 6.4.1.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields)

| Field Name | Type | Description |
| --- | --- | --- |
| swagger | `string` | **Required.** Specifies the Swagger Specification version being used. It can be used by the Swagger UI and other clients to interpret the API listing. The value *MUST* be `"2.0"`. |
| info | [Info Object](https://spec.openapis.org/oas/v2.0.html#info-object) | **Required.** Provides metadata about the API. The metadata can be used by the clients if needed. |
| host | `string` | The host (name or ip) serving the API. This *MUST* be the host only and does not include the scheme nor sub-paths. It *MAY* include a port. If the `host` is not included, the host serving the documentation is to be used (including the port). The `host` does not support [path templating](https://spec.openapis.org/oas/v2.0.html#path-templating). |
| basePath | `string` | The base path on which the API is served, which is relative to the [`host`](https://spec.openapis.org/oas/v2.0.html#swaggerHost). If it is not included, the API is served directly under the `host`. The value *MUST* start with a leading slash (`/`). The `basePath` does not support [path templating](https://spec.openapis.org/oas/v2.0.html#path-templating). |
| schemes | \[`string`\] | The transfer protocol of the API. Values *MUST* be from the list: `"http"`, `"https"`, `"ws"`, `"wss"`. If the `schemes` is not included, the default scheme to be used is the one used to access the Swagger definition itself. |
| consumes | \[`string`\] | A list of MIME types the APIs can consume. This is global to all APIs but can be overridden on specific API calls. Value *MUST* be as described under [Mime Types](https://spec.openapis.org/oas/v2.0.html#mime-types). |
| produces | \[`string`\] | A list of MIME types the APIs can produce. This is global to all APIs but can be overridden on specific API calls. Value *MUST* be as described under [Mime Types](https://spec.openapis.org/oas/v2.0.html#mime-types). |
| paths | [Paths Object](https://spec.openapis.org/oas/v2.0.html#paths-object) | **Required.** The available paths and operations for the API. |
| definitions | [Definitions Object](https://spec.openapis.org/oas/v2.0.html#definitions-object) | An object to hold data types produced and consumed by operations. |
| parameters | [Parameters Definitions Object](https://spec.openapis.org/oas/v2.0.html#parameters-definitions-object) | An object to hold parameters that can be used across operations. This property *does not* define global parameters for all operations. |
| responses | [Responses Definitions Object](https://spec.openapis.org/oas/v2.0.html#responses-definitions-object) | An object to hold responses that can be used across operations. This property *does not* define global responses for all operations. |
| securityDefinitions | [Security Definitions Object](https://spec.openapis.org/oas/v2.0.html#security-definitions-object) | Security scheme definitions that can be used across the specification. |
| security | \[[Security Requirement Object](https://spec.openapis.org/oas/v2.0.html#security-requirement-object)\] | A declaration of which security schemes are applied for the API as a whole. The list of values describes alternative security schemes that can be used (that is, there is a logical OR between the security requirements). Individual operations can override this definition. |
| tags | \[[Tag Object](https://spec.openapis.org/oas/v2.0.html#tag-object)\] | A list of tags used by the specification with additional metadata. The order of the tags can be used to reflect on their order by the parsing tools. Not all tags that are used by the [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) must be declared. The tags that are not declared may be organized randomly or based on the tools’ logic. Each tag name in the list *MUST* be unique. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v2.0.html#external-documentation-object) | Additional external documentation. |

##### 6.4.1.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

#### 6.4.2 Info Object

[](https://spec.openapis.org/oas/v2.0.html#info-object)

The object provides metadata about the API. The metadata can be used by the clients if needed, and can be presented in the Swagger-UI for convenience.

##### 6.4.2.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-0)

| Field Name | Type | Description |
| --- | --- | --- |
| title | `string` | **Required.** The title of the application. |
| description | `string` | A short description of the application. [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation. |
| termsOfService | `string` | The Terms of Service for the API. |
| contact | [Contact Object](https://spec.openapis.org/oas/v2.0.html#contact-object) | The contact information for the exposed API. |
| license | [License Object](https://spec.openapis.org/oas/v2.0.html#license-object) | The license information for the exposed API. |
| version | `string` | **Required** Provides the version of the application API (not to be confused with the specification version). |

##### 6.4.2.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-0)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.2.3 Info Object Example:

[](https://spec.openapis.org/oas/v2.0.html#info-object-example)

```
{
  "title": "Swagger Sample App",
  "description": "This is a sample server Petstore server.",
  "termsOfService": "http://swagger.io/terms/",
  "contact": {
    "name": "API Support",
    "url": "http://www.swagger.io/support",
    "email": "support@swagger.io"
  },
  "license": {
    "name": "Apache 2.0",
    "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
  },
  "version": "1.0.1"
}
```

```
title: Swagger Sample App
description: This is a sample server Petstore server.
termsOfService: http://swagger.io/terms/
contact:
  name: API Support
  url: http://www.swagger.io/support
  email: support@swagger.io
license:
  name: Apache 2.0
  url: http://www.apache.org/licenses/LICENSE-2.0.html
version: 1.0.1
```

#### 6.4.3 Contact Object

[](https://spec.openapis.org/oas/v2.0.html#contact-object)

Contact information for the exposed API.

##### 6.4.3.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-1)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | The identifying name of the contact person/organization. |
| url | `string` | The URL pointing to the contact information. *MUST* be in the format of a URL. |
| email | `string` | The email address of the contact person/organization. *MUST* be in the format of an email address. |

##### 6.4.3.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-1)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.3.3 Contact Object Example:

[](https://spec.openapis.org/oas/v2.0.html#contact-object-example)

```
{
  "name": "API Support",
  "url": "http://www.swagger.io/support",
  "email": "support@swagger.io"
}
```

```
name: API Support
url: http://www.swagger.io/support
email: support@swagger.io
```

#### 6.4.4 License Object

[](https://spec.openapis.org/oas/v2.0.html#license-object)

License information for the exposed API.

##### 6.4.4.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-2)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | **Required.** The license name used for the API. |
| url | `string` | A URL to the license used for the API. *MUST* be in the format of a URL. |

##### 6.4.4.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-2)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.4.3 License Object Example:

[](https://spec.openapis.org/oas/v2.0.html#license-object-example)

```
{
  "name": "Apache 2.0",
  "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
}
```

```
name: Apache 2.0
url: http://www.apache.org/licenses/LICENSE-2.0.html
```

#### 6.4.5 Paths Object

[](https://spec.openapis.org/oas/v2.0.html#paths-object)

Holds the relative paths to the individual endpoints. The path is appended to the [`basePath`](https://spec.openapis.org/oas/v2.0.html#swaggerBasePath) in order to construct the full URL. The Paths may be empty, due to [ACL constraints](https://spec.openapis.org/oas/v2.0.html#security-filtering).

##### 6.4.5.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields)

| Field Pattern | Type | Description |
| --- | --- | --- |
| /{path} | [Path Item Object](https://spec.openapis.org/oas/v2.0.html#path-item-object) | A relative path to an individual endpoint. The field name *MUST* begin with a slash. The path is appended to the [`basePath`](https://spec.openapis.org/oas/v2.0.html#swaggerBasePath) in order to construct the full URL. [Path templating](https://spec.openapis.org/oas/v2.0.html#path-templating) is allowed. |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.5.2 Paths Object Example

[](https://spec.openapis.org/oas/v2.0.html#paths-object-example)

```
{
  "/pets": {
    "get": {
      "description": "Returns all pets from the system that the user has access to",
      "produces": [
        "application/json"
      ],
      "responses": {
        "200": {
          "description": "A list of pets.",
          "schema": {
            "type": "array",
            "items": {
              "$ref": "#/definitions/pet"
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
    produces:
    - application/json
    responses:
      '200':
        description: A list of pets.
        schema:
          type: array
          items:
            $ref: '#/definitions/pet'
```

#### 6.4.6 Path Item Object

[](https://spec.openapis.org/oas/v2.0.html#path-item-object)

Describes the operations available on a single path. A Path Item may be empty, due to [ACL constraints](https://spec.openapis.org/oas/v2.0.html#security-filtering). The path itself is still exposed to the documentation viewer but they will not know which operations and parameters are available.

##### 6.4.6.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-3)

| Field Name | Type | Description |
| --- | --- | --- |
| $ref | `string` | Allows for an external definition of this path item. The referenced structure *MUST* be in the format of a [Path Item Object](https://spec.openapis.org/oas/v2.0.html#path-item-object). If there are conflicts between the referenced definition and this Path Item’s definition, the behavior is *undefined*. |
| get | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a GET operation on this path. |
| put | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a PUT operation on this path. |
| post | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a POST operation on this path. |
| delete | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a DELETE operation on this path. |
| options | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a OPTIONS operation on this path. |
| head | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a HEAD operation on this path. |
| patch | [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object) | A definition of a PATCH operation on this path. |
| parameters | \[[Parameter Object](https://spec.openapis.org/oas/v2.0.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object)\] | A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the operation level, but cannot be removed there. The list *MUST NOT* include duplicated parameters. A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/v2.0.html#parameterName) and [location](https://spec.openapis.org/oas/v2.0.html#parameterIn). The list can use the [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object) to link to parameters that are defined at the [Swagger Object’s parameters](https://spec.openapis.org/oas/v2.0.html#swaggerParameters). There can be one “body” parameter at most. |

##### 6.4.6.2 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-0)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.6.3 Path Item Object Example

[](https://spec.openapis.org/oas/v2.0.html#path-item-object-example)

```
{
  "get": {
    "description": "Returns pets based on ID",
    "summary": "Find pets by ID",
    "operationId": "getPetsById",
    "produces": [
      "application/json",
      "text/html"
    ],
    "responses": {
      "200": {
        "description": "pet response",
        "schema": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Pet"
          }
        }
      },
      "default": {
        "description": "error payload",
        "schema": {
          "$ref": "#/definitions/ErrorModel"
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
      "type": "array",
      "items": {
        "type": "string"
      },
      "collectionFormat": "csv"
    }
  ]
}
```

```
get:
  description: Returns pets based on ID
  summary: Find pets by ID
  operationId: getPetsById
  produces:
  - application/json
  - text/html
  responses:
    '200':
      description: pet response
      schema:
        type: array
        items:
          $ref: '#/definitions/Pet'
    default:
      description: error payload
      schema:
        $ref: '#/definitions/ErrorModel'
parameters:
- name: id
  in: path
  description: ID of pet to use
  required: true
  type: array
  items:
    type: string
  collectionFormat: csv
```

#### 6.4.7 Operation Object

[](https://spec.openapis.org/oas/v2.0.html#operation-object)

Describes a single API operation on a path.

##### 6.4.7.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-4)

| Field Name | Type | Description |
| --- | --- | --- |
| tags | \[`string`\] | A list of tags for API documentation control. Tags can be used for logical grouping of operations by resources or any other qualifier. |
| summary | `string` | A short summary of what the operation does. For maximum readability in the swagger-ui, this field *SHOULD* be less than 120 characters. |
| description | `string` | A verbose explanation of the operation behavior. [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v2.0.html#external-documentation-object) | Additional external documentation for this operation. |
| operationId | `string` | Unique string used to identify the operation. The id *MUST* be unique among all operations described in the API. Tools and libraries *MAY* use the operationId to uniquely identify an operation, therefore, it is recommended to follow common programming naming conventions. |
| consumes | \[`string`\] | A list of MIME types the operation can consume. This overrides the [`consumes`](https://spec.openapis.org/oas/v2.0.html#swaggerConsumes) definition at the Swagger Object. An empty value *MAY* be used to clear the global definition. Value *MUST* be as described under [Mime Types](https://spec.openapis.org/oas/v2.0.html#mime-types). |
| produces | \[`string`\] | A list of MIME types the operation can produce. This overrides the [`produces`](https://spec.openapis.org/oas/v2.0.html#swaggerProduces) definition at the Swagger Object. An empty value *MAY* be used to clear the global definition. Value *MUST* be as described under [Mime Types](https://spec.openapis.org/oas/v2.0.html#mime-types). |
| parameters | \[[Parameter Object](https://spec.openapis.org/oas/v2.0.html#parameter-object) | [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object)\] | A list of parameters that are applicable for this operation. If a parameter is already defined at the [Path Item](https://spec.openapis.org/oas/v2.0.html#pathItemParameters), the new definition will override it, but can never remove it. The list *MUST NOT* include duplicated parameters. A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/v2.0.html#parameterName) and [location](https://spec.openapis.org/oas/v2.0.html#parameterIn). The list can use the [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object) to link to parameters that are defined at the [Swagger Object’s parameters](https://spec.openapis.org/oas/v2.0.html#swaggerParameters). There can be one “body” parameter at most. |
| responses | [Responses Object](https://spec.openapis.org/oas/v2.0.html#responses-object) | **Required.** The list of possible responses as they are returned from executing this operation. |
| schemes | \[`string`\] | The transfer protocol for the operation. Values *MUST* be from the list: `"http"`, `"https"`, `"ws"`, `"wss"`. The value overrides the Swagger Object [`schemes`](https://spec.openapis.org/oas/v2.0.html#swaggerSchemes) definition. |
| deprecated | `boolean` | Declares this operation to be deprecated. Usage of the declared operation should be refrained. Default value is `false`. |
| security | \[[Security Requirement Object](https://spec.openapis.org/oas/v2.0.html#security-requirement-object)\] | A declaration of which security schemes are applied for this operation. The list of values describes alternative security schemes that can be used (that is, there is a logical OR between the security requirements). This definition overrides any declared top-level [`security`](https://spec.openapis.org/oas/v2.0.html#swaggerSecurity). To remove a top-level security declaration, an empty array can be used. |

##### 6.4.7.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-3)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.7.3 Operation Object Example

[](https://spec.openapis.org/oas/v2.0.html#operation-object-example)

```
{
  "tags": [
    "pet"
  ],
  "summary": "Updates a pet in the store with form data",
  "description": "",
  "operationId": "updatePetWithForm",
  "consumes": [
    "application/x-www-form-urlencoded"
  ],
  "produces": [
    "application/json",
    "application/xml"
  ],
  "parameters": [
    {
      "name": "petId",
      "in": "path",
      "description": "ID of pet that needs to be updated",
      "required": true,
      "type": "string"
    },
    {
      "name": "name",
      "in": "formData",
      "description": "Updated name of the pet",
      "required": false,
      "type": "string"
    },
    {
      "name": "status",
      "in": "formData",
      "description": "Updated status of the pet",
      "required": false,
      "type": "string"
    }
  ],
  "responses": {
    "200": {
      "description": "Pet updated."
    },
    "405": {
      "description": "Invalid input"
    }
  },
  "security": [
    {
      "petstore_auth": [
        "write:pets",
        "read:pets"
      ]
    }
  ]
}
```

```
tags:
- pet
summary: Updates a pet in the store with form data
description: ""
operationId: updatePetWithForm
consumes:
- application/x-www-form-urlencoded
produces:
- application/json
- application/xml
parameters:
- name: petId
  in: path
  description: ID of pet that needs to be updated
  required: true
  type: string
- name: name
  in: formData
  description: Updated name of the pet
  required: false
  type: string
- name: status
  in: formData
  description: Updated status of the pet
  required: false
  type: string
responses:
  '200':
    description: Pet updated.
  '405':
    description: Invalid input
security:
- petstore_auth:
  - write:pets
  - read:pets
```

#### 6.4.8 External Documentation Object

[](https://spec.openapis.org/oas/v2.0.html#external-documentation-object)

Allows referencing an external resource for extended documentation.

##### 6.4.8.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-5)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A short description of the target documentation. [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation. |
| url | `string` | **Required.** The URL for the target documentation. Value *MUST* be in the format of a URL. |

##### 6.4.8.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-4)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.8.3 External Documentation Object Example

[](https://spec.openapis.org/oas/v2.0.html#external-documentation-object-example)

```
{
  "description": "Find more info here",
  "url": "https://swagger.io"
}
```

```
description: Find more info here
url: https://swagger.io
```

#### 6.4.9 Parameter Object

[](https://spec.openapis.org/oas/v2.0.html#parameter-object)

Describes a single operation parameter.

A unique parameter is defined by a combination of a [name](https://spec.openapis.org/oas/v2.0.html#parameterName) and [location](https://spec.openapis.org/oas/v2.0.html#parameterIn).

There are five possible parameter types.

-   Path - Used together with [Path Templating](https://spec.openapis.org/oas/v2.0.html#path-templating), where the parameter value is actually part of the operation’s URL. This does not include the host or base path of the API. For example, in `/items/{itemId}`, the path parameter is `itemId`.
-   Query - Parameters that are appended to the URL. For example, in `/items?id=###`, the query parameter is `id`.
-   Header - Custom headers that are expected as part of the request.
-   Body - The payload that’s appended to the HTTP request. Since there can only be one payload, there can only be *one* body parameter. The name of the body parameter has no effect on the parameter itself and is used for documentation purposes only. Since Form parameters are also in the payload, body and form parameters cannot exist together for the same operation.
-   Form - Used to describe the payload of an HTTP request when either `application/x-www-form-urlencoded`, `multipart/form-data` or both are used as the content type of the request (in Swagger’s definition, the [`consumes`](https://spec.openapis.org/oas/v2.0.html#operationConsumes) property of an operation). This is the only parameter type that can be used to send files, thus supporting the `file` type. Since form parameters are sent in the payload, they cannot be declared together with a body parameter for the same operation. Form parameters have a different format based on the content-type used (for further details, consult \[[HTML401](https://spec.openapis.org/oas/v2.0.html#bib-html401 "HTML 4.01 Specification")\] [Section 17.13.4](http://www.w3.org/TR/html401/interact/forms.html#h-17.13.4):
    -   `application/x-www-form-urlencoded` - Similar to the format of Query parameters but as a payload. For example, `foo=1&bar=swagger` - both `foo` and `bar` are form parameters. This is normally used for simple parameters that are being transferred.
    -   `multipart/form-data` - each parameter takes a section in the payload with an internal header. For example, for the header `Content-Disposition: form-data; name="submit-name"` the name of the parameter is `submit-name`. This type of form parameters is more commonly used for file transfers.

##### 6.4.9.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-6)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | **Required.** The name of the parameter. Parameter names are *case sensitive*.
-   If [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) is `"path"`, the `name` field *MUST* correspond to the associated path segment from the [path](https://spec.openapis.org/oas/v2.0.html#pathsPath) field in the [Paths Object](https://spec.openapis.org/oas/v2.0.html#paths-object). See [Path Templating](https://spec.openapis.org/oas/v2.0.html#path-templating) for further information.
-   For all other cases, the `name` corresponds to the parameter name used based on the [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) property.

 |
| in | `string` | **Required.** The location of the parameter. Possible values are “query”, “header”, “path”, “formData” or “body”. |
| description | `string` | A brief description of the parameter. This could contain examples of use. [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation. |
| required | `boolean` | Determines whether this parameter is mandatory. If the parameter is [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) “path”, this property is **required** and its value *MUST* be `true`. Otherwise, the property *MAY* be included and its default value is `false`. |

If [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) is `"body"`:

| Field Name | Type | Description |
| --- | --- | --- |
| schema | [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object) | **Required.** The schema defining the type used for the body parameter. |

If [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) is any value other than `"body"`:

| Field Name | Type | Description |
| --- | --- | --- |
| type | `string` | **Required.** The type of the parameter. Since the parameter is not located at the request body, it is limited to simple types (that is, not an object). The value *MUST* be one of `"string"`, `"number"`, `"integer"`, `"boolean"`, `"array"` or `"file"`. If `type` is `"file"`, the [`consumes`](https://spec.openapis.org/oas/v2.0.html#operationConsumes) *MUST* be either `"multipart/form-data"`, `" application/x-www-form-urlencoded"` or both and the parameter *MUST* be [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) `"formData"`. |
| format | `string` | The extending format for the previously mentioned [`type`](https://spec.openapis.org/oas/v2.0.html#parameterType). See [Data Type Formats](https://spec.openapis.org/oas/v2.0.html#dataTypeFormat) for further details. |
| allowEmptyValue | `boolean` | Sets the ability to pass empty-valued parameters. This is valid only for either `query` or `formData` parameters and allows you to send a parameter with a name only or an empty value. Default value is `false`. |
| items | [Items Object](https://spec.openapis.org/oas/v2.0.html#items-object) | **Required if [`type`](https://spec.openapis.org/oas/v2.0.html#parameterType) is “array”.** Describes the type of items in the array. |
| collectionFormat | `string` | Determines the format of the array if type array is used. Possible values are:
-   `csv` - comma separated values `foo,bar`.
-   `ssv` - space separated values `foo bar`.
-   `tsv` - tab separated values `foo\tbar`.
-   `pipes` - pipe separated values `foo|bar`.
-   `multi` - corresponds to multiple parameter instances instead of multiple values for a single instance `foo=bar&foo=baz`. This is valid only for parameters [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) “query” or “formData”.

Default value is `csv`. |
| default | \* | Declares the value of the parameter that the server will use if none is provided, for example a “count” to control the number of results per page might default to 100 if not supplied by the client in the request. (Note: “default” has no meaning for required parameters.) See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6.2). Unlike JSON Schema this value *MUST* conform to the defined [`type`](https://spec.openapis.org/oas/v2.0.html#parameterType) for this parameter. |
| maximum | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2). |
| exclusiveMaximum | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2). |
| minimum | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3). |
| exclusiveMinimum | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3). |
| maxLength | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.1). |
| minLength | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.2). |
| pattern | `string` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.3). |
| maxItems | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.2). |
| minItems | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.3). |
| uniqueItems | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.4](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.4). |
| enum | \[\*\] | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.1). |
| multipleOf | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.1). |

##### 6.4.9.2 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-1)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.9.3 Parameter Object Examples

[](https://spec.openapis.org/oas/v2.0.html#parameter-object-examples)

###### 6.4.9.3.1 Body Parameters

[](https://spec.openapis.org/oas/v2.0.html#body-parameters)

A body parameter with a referenced schema definition (normally for a model definition):

```
{
  "name": "user",
  "in": "body",
  "description": "user to add to the system",
  "required": true,
  "schema": {
    "$ref": "#/definitions/User"
  }
}
```

```
name: user
in: body
description: user to add to the system
required: true
schema:
  $ref: '#/definitions/User'
```

A body parameter that is an array of string values:

```
{
  "name": "user",
  "in": "body",
  "description": "user to add to the system",
  "required": true,
  "schema": {
    "type": "array",
    "items": {
      "type": "string"
    }
  }
}
```

```
name: user
in: body
description: user to add to the system
required: true
schema:
  type: array
  items:
    type: string
```

###### 6.4.9.3.2 Other Parameters

[](https://spec.openapis.org/oas/v2.0.html#other-parameters)

A header parameter with an array of 64 bit integer numbers:

```
{
  "name": "token",
  "in": "header",
  "description": "token to be passed as a header",
  "required": true,
  "type": "array",
  "items": {
    "type": "integer",
    "format": "int64"
  },
  "collectionFormat": "csv"
}
```

```
name: token
in: header
description: token to be passed as a header
required: true
type: array
items:
  type: integer
  format: int64
collectionFormat: csv
```

A path parameter of a string value:

```
{
  "name": "username",
  "in": "path",
  "description": "username to fetch",
  "required": true,
  "type": "string"
}
```

```
name: username
in: path
description: username to fetch
required: true
type: string
```

An optional query parameter of a string value, allowing multiple values by repeating the query parameter:

```
{
  "name": "id",
  "in": "query",
  "description": "ID of the object to fetch",
  "required": false,
  "type": "array",
  "items": {
    "type": "string"
  },
  "collectionFormat": "multi"
}
```

```
name: id
in: query
description: ID of the object to fetch
required: false
type: array
items:
  type: string
collectionFormat: multi
```

A form data with file type for a file upload:

```
{
  "name": "avatar",
  "in": "formData",
  "description": "The avatar of the user",
  "required": true,
  "type": "file"
}
```

```
name: avatar
in: formData
description: The avatar of the user
required: true
type: file
```

#### 6.4.10 Items Object

[](https://spec.openapis.org/oas/v2.0.html#items-object)

A limited subset of JSON-Schema’s items object. It is used by parameter definitions that are not located [`in`](https://spec.openapis.org/oas/v2.0.html#parameterIn) `"body"`.

##### 6.4.10.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-7)

| Field Name | Type | Description |
| --- | --- | --- |
| type | `string` | **Required.** The internal type of the array. The value *MUST* be one of `"string"`, `"number"`, `"integer"`, `"boolean"`, or `"array"`. Files and models are not allowed. |
| format | `string` | The extending format for the previously mentioned [`type`](https://spec.openapis.org/oas/v2.0.html#parameterType). See [Data Type Formats](https://spec.openapis.org/oas/v2.0.html#dataTypeFormat) for further details. |
| items | [Items Object](https://spec.openapis.org/oas/v2.0.html#items-object) | **Required if [`type`](https://spec.openapis.org/oas/v2.0.html#itemsType) is “array”.** Describes the type of items in the array. |
| collectionFormat | `string` | Determines the format of the array if type array is used. Possible values are:
-   `csv` - comma separated values `foo,bar`.
-   `ssv` - space separated values `foo bar`.
-   `tsv` - tab separated values `foo\tbar`.
-   `pipes` - pipe separated values `foo|bar`.

Default value is `csv`. |
| default | \* | Declares the value of the item that the server will use if none is provided. (Note: “default” has no meaning for required items.) See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6.2). Unlike JSON Schema this value *MUST* conform to the defined [`type`](https://spec.openapis.org/oas/v2.0.html#itemsType) for the data type. |
| maximum | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2). |
| exclusiveMaximum | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2). |
| minimum | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3). |
| exclusiveMinimum | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3). |
| maxLength | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.1). |
| minLength | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.2). |
| pattern | `string` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.3). |
| maxItems | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.2). |
| minItems | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.3). |
| uniqueItems | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.4](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.4). |
| enum | \[\*\] | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.1). |
| multipleOf | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.1). |

##### 6.4.10.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-5)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.10.3 Items Object Examples

[](https://spec.openapis.org/oas/v2.0.html#items-object-examples)

Items must be of type string and have the minimum length of 2 characters:

```
{
    "type": "string",
    "minLength": 2
}
```

```
type: string
minLength: 2
```

An array of arrays, the internal array being of type integer, numbers must be between 0 and 63 (inclusive):

```
{
    "type": "array",
    "items": {
        "type": "integer",
        "minimum": 0,
        "maximum": 63
    }
}
```

```
type: array
items:
  type: integer
  minimum: 0
  maximum: 63
```

#### 6.4.11 Responses Object

[](https://spec.openapis.org/oas/v2.0.html#responses-object)

A container for the expected responses of an operation. The container maps a HTTP response code to the expected response. It is not expected from the documentation to necessarily cover all possible HTTP response codes, since they may not be known in advance. However, it is expected from the documentation to cover a successful operation response and any known errors.

The `default` can be used as the default response object for all HTTP codes that are not covered individually by the specification.

The `Responses Object` *MUST* contain at least one response code, and it *SHOULD* be the response for a successful operation call.

##### 6.4.11.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-8)

| Field Name | Type | Description |
| --- | --- | --- |
| default | [Response Object](https://spec.openapis.org/oas/v2.0.html#response-object) | [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object) | The documentation of responses other than the ones declared for specific HTTP response codes. It can be used to cover undeclared responses. [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object) can be used to link to a response that is defined at the [Swagger Object’s responses](https://spec.openapis.org/oas/v2.0.html#swaggerResponses) section. |

##### 6.4.11.2 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-2)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {[HTTP Status Code](https://spec.openapis.org/oas/v2.0.html#http-status-codes)} | [Response Object](https://spec.openapis.org/oas/v2.0.html#response-object) | [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object) | Any [HTTP status code](https://spec.openapis.org/oas/v2.0.html#http-status-codes) can be used as the property name (one property per HTTP status code). Describes the expected response for that HTTP status code. [Reference Object](https://spec.openapis.org/oas/v2.0.html#reference-object) can be used to link to a response that is defined at the [Swagger Object’s responses](https://spec.openapis.org/oas/v2.0.html#swaggerResponses) section. |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.11.3 Responses Object Example

[](https://spec.openapis.org/oas/v2.0.html#responses-object-example)

A 200 response for successful operation and a default response for others (implying an error):

```
{
  "200": {
    "description": "a pet to be returned",
    "schema": {
      "$ref": "#/definitions/Pet"
    }
  },
  "default": {
    "description": "Unexpected error",
    "schema": {
      "$ref": "#/definitions/ErrorModel"
    }
  }
}
```

```
'200':
  description: a pet to be returned
  schema:
    $ref: '#/definitions/Pet'
default:
  description: Unexpected error
  schema:
    $ref: '#/definitions/ErrorModel'
```

#### 6.4.12 Response Object

[](https://spec.openapis.org/oas/v2.0.html#response-object)

Describes a single response from an API Operation.

##### 6.4.12.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-9)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | **Required.** A short description of the response. [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation. |
| schema | [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object) | A definition of the response structure. It can be a primitive, an array or an object. If this field does not exist, it means no content is returned as part of the response. As an extension to the [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object), its root `type` value may also be `"file"`. This *SHOULD* be accompanied by a relevant `produces` mime-type. |
| headers | [Headers Object](https://spec.openapis.org/oas/v2.0.html#headers-object) | A list of headers that are sent with the response. |
| examples | [Example Object](https://spec.openapis.org/oas/v2.0.html#example-object) | An example of the response message. |

##### 6.4.12.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-6)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.12.3 Response Object Examples

[](https://spec.openapis.org/oas/v2.0.html#response-object-examples)

Response of an array of a complex type:

```
{
  "description": "A complex object array response",
  "schema": {
    "type": "array",
    "items": {
      "$ref": "#/definitions/VeryComplexType"
    }
  }
}
```

```
description: A complex object array response
schema:
  type: array
  items:
    $ref: '#/definitions/VeryComplexType'
```

Response with a string type:

```
{
  "description": "A simple string response",
  "schema": {
    "type": "string"
  }
}
```

```
description: A simple string response
schema:
  type: string
```

Response with headers:

```
{
  "description": "A simple string response",
  "schema": {
    "type": "string"
  },
  "headers": {
    "X-Rate-Limit-Limit": {
      "description": "The number of allowed requests in the current period",
      "type": "integer"
    },
    "X-Rate-Limit-Remaining": {
      "description": "The number of remaining requests in the current period",
      "type": "integer"
    },
    "X-Rate-Limit-Reset": {
      "description": "The number of seconds left in the current period",
      "type": "integer"
    }
  }
}
```

```
description: A simple string response
schema:
  type: string
headers:
  X-Rate-Limit-Limit:
    description: The number of allowed requests in the current period
    type: integer
  X-Rate-Limit-Remaining:
    description: The number of remaining requests in the current period
    type: integer
  X-Rate-Limit-Reset:
    description: The number of seconds left in the current period
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

#### 6.4.13 Headers Object

[](https://spec.openapis.org/oas/v2.0.html#headers-object)

Lists the headers that can be sent as part of a response.

##### 6.4.13.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-3)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | [Header Object](https://spec.openapis.org/oas/v2.0.html#header-object) | The name of the property corresponds to the name of the header. The value describes the type of the header. |

##### 6.4.13.2 Headers Object Example

[](https://spec.openapis.org/oas/v2.0.html#headers-object-example)

Rate-limit headers:

```
{
    "X-Rate-Limit-Limit": {
        "description": "The number of allowed requests in the current period",
        "type": "integer"
    },
    "X-Rate-Limit-Remaining": {
        "description": "The number of remaining requests in the current period",
        "type": "integer"
    },
    "X-Rate-Limit-Reset": {
        "description": "The number of seconds left in the current period",
        "type": "integer"
    }
}
```

```
X-Rate-Limit-Limit:
  description: The number of allowed requests in the current period
  type: integer
X-Rate-Limit-Remaining:
  description: The number of remaining requests in the current period
  type: integer
X-Rate-Limit-Reset:
  description: The number of seconds left in the current period
  type: integer
```

#### 6.4.14 Example Object

[](https://spec.openapis.org/oas/v2.0.html#example-object)

Allows sharing examples for operation responses.

##### 6.4.14.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-4)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {[mime type](https://spec.openapis.org/oas/v2.0.html#mime-types)} | Any | The name of the property *MUST* be one of the Operation `produces` values (either implicit or inherited). The value *SHOULD* be an example of what such a response would look like. |

##### 6.4.14.2 Example Object Example

[](https://spec.openapis.org/oas/v2.0.html#example-object-example)

Example response for application/json mimetype of a Pet data type:

```
{
  "application/json": {
    "name": "Puma",
    "type": "Dog",
    "color": "Black",
    "gender": "Female",
    "breed": "Mixed"
  }
}
```

```
application/json:
  name: Puma
  type: Dog
  color: Black
  gender: Female
  breed: Mixed
```

#### 6.4.15 Header Object

[](https://spec.openapis.org/oas/v2.0.html#header-object)

| Field Name | Type | Description |
| --- | --- | --- |
| description | `string` | A short description of the header. |
| type | `string` | **Required.** The type of the object. The value *MUST* be one of `"string"`, `"number"`, `"integer"`, `"boolean"`, or `"array"`. |
| format | `string` | The extending format for the previously mentioned [`type`](https://spec.openapis.org/oas/v2.0.html#stType). See [Data Type Formats](https://spec.openapis.org/oas/v2.0.html#dataTypeFormat) for further details. |
| items | [Items Object](https://spec.openapis.org/oas/v2.0.html#items-object) | **Required if [`type`](https://spec.openapis.org/oas/v2.0.html#stType) is “array”.** Describes the type of items in the array. |
| collectionFormat | `string` | Determines the format of the array if type array is used. Possible values are:
-   `csv` - comma separated values `foo,bar`.
-   `ssv` - space separated values `foo bar`.
-   `tsv` - tab separated values `foo\tbar`.
-   `pipes` - pipe separated values `foo|bar`.

Default value is `csv`. |
| default | \* | Declares the value of the header that the server will use if none is provided. (Note: “default” has no meaning for required headers.) See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6.2). Unlike JSON Schema this value *MUST* conform to the defined [`type`](https://spec.openapis.org/oas/v2.0.html#headerDefault) for the header. |
| maximum | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2). |
| exclusiveMaximum | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.2). |
| minimum | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3). |
| exclusiveMinimum | `boolean` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.3). |
| maxLength | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.1). |
| minLength | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.2). |
| pattern | `string` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2.3). |
| maxItems | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.2](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.2). |
| minItems | `integer` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.3](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.3). |
| uniqueItems | `boolean` | [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.4](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3.4). |
| enum | \[\*\] | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5.1). |
| multipleOf | `number` | See [https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.1](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.1.1). |

##### 6.4.15.1 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-7)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.15.2 Header Object Example

[](https://spec.openapis.org/oas/v2.0.html#header-object-example)

A simple header with of an integer type:

```
{
  "description": "The number of allowed requests in the current period",
  "type": "integer"
}
```

```
description: The number of allowed requests in the current period
type: integer
```

#### 6.4.16 Tag Object

[](https://spec.openapis.org/oas/v2.0.html#tag-object)

Allows adding meta data to a single tag that is used by the [Operation Object](https://spec.openapis.org/oas/v2.0.html#operation-object). It is not mandatory to have a Tag Object per tag used there.

##### 6.4.16.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-10)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | **Required.** The name of the tag. |
| description | `string` | A short description for the tag. [GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v2.0.html#external-documentation-object) | Additional external documentation for this tag. |

##### 6.4.16.2 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-5)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.16.3 Tag Object Example

[](https://spec.openapis.org/oas/v2.0.html#tag-object-example)

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

#### 6.4.17 Reference Object

[](https://spec.openapis.org/oas/v2.0.html#reference-object)

A simple object to allow referencing other definitions in the specification. It can be used to reference parameters and responses that are defined at the top level for reuse.

The Reference Object is a [JSON Reference](https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-02) that uses a JSON Pointer \[[RFC6901](https://spec.openapis.org/oas/v2.0.html#bib-rfc6901 "JavaScript Object Notation (JSON) Pointer")\] as its value. For this specification, only [canonical dereferencing](https://tools.ietf.org/html/draft-zyp-json-schema-04#section-7.2.3) is supported.

##### 6.4.17.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-11)

| Field Name | Type | Description |
| --- | --- | --- |
| $ref | `string` | **Required.** The reference string. |

##### 6.4.17.2 Reference Object Example

[](https://spec.openapis.org/oas/v2.0.html#reference-object-example)

```
{
	"$ref": "#/definitions/Pet"
}
```

```
$ref: '#/definitions/Pet'
```

##### 6.4.17.3 Relative Schema File Example

[](https://spec.openapis.org/oas/v2.0.html#relative-schema-file-example)

```
{
  "$ref": "Pet.json"
}
```

```
$ref: 'Pet.yaml'
```

##### 6.4.17.4 Relative Files With Embedded Schema Example

[](https://spec.openapis.org/oas/v2.0.html#relative-files-with-embedded-schema-example)

```
{
  "$ref": "definitions.json#/Pet"
}
```

```
$ref: 'definitions.yaml#/Pet'
```

#### 6.4.18 Schema Object

[](https://spec.openapis.org/oas/v2.0.html#schema-object)

The Schema Object allows the definition of input and output data types. These types can be objects, but also primitives and arrays. This object is based on the [JSON Schema Specification Draft 4](https://spec.openapis.org/oas/v2.0.html#bib-json-schema-04 "JSON Schema: core definitions and terminology. Draft 4") and uses a predefined subset of it. On top of this subset, there are extensions provided by this specification to allow for more complete documentation.

Further information about the properties can be found in [JSON Schema Core](https://spec.openapis.org/oas/v2.0.html#bib-json-schema-04 "JSON Schema: core definitions and terminology. Draft 4") and [JSON Schema Validation](https://spec.openapis.org/oas/v2.0.html#bib-json-schema-validation-04 "JSON Schema: interactive and non interactive validation. Draft 4"). Unless stated otherwise, the property definitions follow the JSON Schema specification as referenced here.

The following properties are taken directly from the JSON Schema definition and follow the same specifications:

-   $ref - As a [JSON Reference](https://spec.openapis.org/oas/v2.0.html#bib-json-reference "JSON Reference")
-   format (See [Data Type Formats](https://spec.openapis.org/oas/v2.0.html#dataTypeFormat) for further details)
-   title
-   description ([GFM syntax](https://guides.github.com/features/mastering-markdown/#GitHub-flavored-markdown) can be used for rich text representation)
-   default (Unlike JSON Schema, the value *MUST* conform to the defined type for the Schema Object)
-   multipleOf
-   maximum
-   exclusiveMaximum
-   minimum
-   exclusiveMinimum
-   maxLength
-   minLength
-   pattern
-   maxItems
-   minItems
-   uniqueItems
-   maxProperties
-   minProperties
-   required
-   enum
-   type

The following properties are taken from the JSON Schema definition but their definitions were adjusted to the Swagger Specification. Their definition is the same as the one from JSON Schema, only where the original definition references the JSON Schema definition, the [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object) definition is used instead.

-   items
-   allOf
-   properties
-   additionalProperties

Other than the JSON Schema subset fields, the following fields may be used for further schema documentation.

##### 6.4.18.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-12)

| Field Name | Type | Description |
| --- | --- | --- |
| discriminator | `string` | Adds support for polymorphism. The discriminator is the schema property name that is used to differentiate between other schema that inherit this schema. The property name used *MUST* be defined at this schema and it *MUST* be in the `required` property list. When used, the value *MUST* be the name of this schema or any schema that inherits it. |
| readOnly | `boolean` | Relevant only for Schema `"properties"` definitions. Declares the property as “read only”. This means that it *MAY* be sent as part of a response but *MUST NOT* be sent as part of the request. Properties marked as `readOnly` being `true` *SHOULD NOT* be in the `required` list of the defined schema. Default value is `false`. |
| xml | [XML Object](https://spec.openapis.org/oas/v2.0.html#xml-object) | This *MAY* be used only on properties schemas. It has no effect on root schemas. Adds Additional metadata to describe the XML representation format of this property. |
| externalDocs | [External Documentation Object](https://spec.openapis.org/oas/v2.0.html#external-documentation-object) | Additional external documentation for this schema. |
| example | Any | A free-form property to include an example of an instance for this schema. |

##### 6.4.18.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-8)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

###### 6.4.18.2.1 Composition and Inheritance (Polymorphism)

[](https://spec.openapis.org/oas/v2.0.html#composition-and-inheritance-polymorphism)

Swagger allows combining and extending model definitions using the `allOf` property of JSON Schema, in effect offering model composition. `allOf` takes in an array of object definitions that are validated *independently* but together compose a single object.

While composition offers model extensibility, it does not imply a hierarchy between the models. To support polymorphism, Swagger adds the support of the `discriminator` field. When used, the `discriminator` will be the name of the property used to decide which schema definition is used to validate the structure of the model. As such, the `discriminator` field *MUST* be a required field. The value of the chosen property has to be the friendly name given to the model under the `definitions` property. As such, inline schema definitions, which do not have a given id, *cannot* be used in polymorphism.

###### 6.4.18.2.2 XML Modeling

[](https://spec.openapis.org/oas/v2.0.html#xml-modeling)

The [xml](https://spec.openapis.org/oas/v2.0.html#schemaXml) property allows extra definitions when translating the JSON definition to XML. The [XML Object](https://spec.openapis.org/oas/v2.0.html#xml-object) contains additional information about the available options.

##### 6.4.18.3 Schema Object Examples

[](https://spec.openapis.org/oas/v2.0.html#schema-object-examples)

###### 6.4.18.3.1 Primitive Sample

[](https://spec.openapis.org/oas/v2.0.html#primitive-sample)

Unlike previous versions of Swagger, Schema definitions can be used to describe primitive and arrays as well.

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

###### 6.4.18.3.2 Simple Model

[](https://spec.openapis.org/oas/v2.0.html#simple-model)

```
{
  "type": "object",
  "required": [
    "name"
  ],
  "properties": {
    "name": {
      "type": "string"
    },
    "address": {
      "$ref": "#/definitions/Address"
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
    $ref: '#/definitions/Address'
  age:
    type: integer
    format: int32
    minimum: 0
```

###### 6.4.18.3.3 Model with Map/Dictionary Properties

[](https://spec.openapis.org/oas/v2.0.html#model-with-map-dictionary-properties)

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
    "$ref": "#/definitions/ComplexModel"
  }
}
```

```
type: object
additionalProperties:
  $ref: '#/definitions/ComplexModel'
```

###### 6.4.18.3.4 Model with Example

[](https://spec.openapis.org/oas/v2.0.html#model-with-example)

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
  "required": [
    "name"
  ],
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

###### 6.4.18.3.5 Models with Composition

[](https://spec.openapis.org/oas/v2.0.html#models-with-composition)

```
{
  "definitions": {
    "ErrorModel": {
      "type": "object",
      "required": [
        "message",
        "code"
      ],
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
          "$ref": "#/definitions/ErrorModel"
        },
        {
          "type": "object",
          "required": [
            "rootCause"
          ],
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
```

```
definitions:
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
    - $ref: '#/definitions/ErrorModel'
    - type: object
      required:
      - rootCause
      properties:
        rootCause:
          type: string
```

###### 6.4.18.3.6 Models with Polymorphism Support

[](https://spec.openapis.org/oas/v2.0.html#models-with-polymorphism-support)

```
{
  "definitions": {
    "Pet": {
      "type": "object",
      "discriminator": "petType",
      "properties": {
        "name": {
          "type": "string"
        },
        "petType": {
          "type": "string"
        }
      },
      "required": [
        "name",
        "petType"
      ]
    },
    "Cat": {
      "description": "A representation of a cat",
      "allOf": [
        {
          "$ref": "#/definitions/Pet"
        },
        {
          "type": "object",
          "properties": {
            "huntingSkill": {
              "type": "string",
              "description": "The measured skill for hunting",
              "default": "lazy",
              "enum": [
                "clueless",
                "lazy",
                "adventurous",
                "aggressive"
              ]
            }
          },
          "required": [
            "huntingSkill"
          ]
        }
      ]
    },
    "Dog": {
      "description": "A representation of a dog",
      "allOf": [
        {
          "$ref": "#/definitions/Pet"
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
          "required": [
            "packSize"
          ]
        }
      ]
    }
  }
}
```

```
definitions:
  Pet:
    type: object
    discriminator: petType
    properties:
      name:
        type: string
      petType:
        type: string
    required:
    - name
    - petType
  Cat:
    description: A representation of a cat
    allOf:
    - $ref: '#/definitions/Pet'
    - type: object
      properties:
        huntingSkill:
          type: string
          description: The measured skill for hunting
          default: lazy
          enum:
          - clueless
          - lazy
          - adventurous
          - aggressive
      required:
      - huntingSkill
  Dog:
    description: A representation of a dog
    allOf:
    - $ref: '#/definitions/Pet'
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

#### 6.4.19 XML Object

[](https://spec.openapis.org/oas/v2.0.html#xml-object)

A metadata object that allows for more fine-tuned XML model definitions.

When using arrays, XML element names are *not* inferred (for singular/plural forms) and the `name` property should be used to add that information. See examples for expected behavior.

##### 6.4.19.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-13)

| Field Name | Type | Description |
| --- | --- | --- |
| name | `string` | Replaces the name of the element/attribute used for the described schema property. When defined within the Items Object (`items`), it will affect the name of the individual XML elements within the list. When defined alongside `type` being `array` (outside the `items`), it will affect the wrapping element and only if `wrapped` is `true`. If `wrapped` is `false`, it will be ignored. |
| namespace | `string` | The URL of the namespace definition. Value *SHOULD* be in the form of a URL. |
| prefix | `string` | The prefix to be used for the [name](https://spec.openapis.org/oas/v2.0.html#xmlName). |
| attribute | `boolean` | Declares whether the property definition translates to an attribute instead of an element. Default value is `false`. |
| wrapped | `boolean` | *MAY* be used only for an array definition. Signifies whether the array is wrapped (for example, `<books><book/><book/></books>`) or unwrapped (`<book/><book/>`). Default value is `false`. The definition takes effect only when defined alongside `type` being `array` (outside the `items`). |

##### 6.4.19.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-9)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.19.3 XML Object Examples

[](https://spec.openapis.org/oas/v2.0.html#xml-object-examples)

The examples of the XML object definitions are included inside a property definition of a [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object) with a sample of the XML representation of it.

###### 6.4.19.3.1 No XML Element

[](https://spec.openapis.org/oas/v2.0.html#no-xml-element)

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

Basic string array property ([`wrapped`](https://spec.openapis.org/oas/v2.0.html#xmlWrapped) is `false` by default):

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

###### 6.4.19.3.2 XML Name Replacement

[](https://spec.openapis.org/oas/v2.0.html#xml-name-replacement)

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

###### 6.4.19.3.3 XML Attribute, Prefix and Namespace

[](https://spec.openapis.org/oas/v2.0.html#xml-attribute-prefix-and-namespace)

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
          "namespace": "http://swagger.io/schema/sample",
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
        namespace: http://swagger.io/schema/sample
        prefix: sample
```

```
<Person id="123">
    <sample:name xmlns:sample="http://swagger.io/schema/sample">example</sample:name>
</Person>
```

###### 6.4.19.3.4 XML Arrays

[](https://spec.openapis.org/oas/v2.0.html#xml-arrays)

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

The external `name` property has no effect on the XML:

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

Even when the array is wrapped, if no name is explicitly defined, the same name will be used both internally and externally:

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

To overcome the above example, the following definition can be used:

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

#### 6.4.20 Definitions Object

[](https://spec.openapis.org/oas/v2.0.html#definitions-object)

An object to hold data types that can be consumed and produced by operations. These data types can be primitives, arrays or models.

##### 6.4.20.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-6)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | [Schema Object](https://spec.openapis.org/oas/v2.0.html#schema-object) | A single definition, mapping a “name” to the schema it defines. |

##### 6.4.20.2 Definitions Object Example

[](https://spec.openapis.org/oas/v2.0.html#definitions-object-example)

```
{
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
}
```

```
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
```

#### 6.4.21 Parameters Definitions Object

[](https://spec.openapis.org/oas/v2.0.html#parameters-definitions-object)

An object to hold parameters to be reused across operations. Parameter definitions can be referenced to the ones defined here.

This does *not* define global operation parameters.

##### 6.4.21.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-7)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | [Parameter Object](https://spec.openapis.org/oas/v2.0.html#parameter-object) | A single parameter definition, mapping a “name” to the parameter it defines. |

##### 6.4.21.2 Parameters Definition Object Example

[](https://spec.openapis.org/oas/v2.0.html#parameters-definition-object-example)

```
{
  "skipParam": {
    "name": "skip",
    "in": "query",
    "description": "number of items to skip",
    "required": true,
    "type": "integer",
    "format": "int32"
  },
  "limitParam": {
    "name": "limit",
    "in": "query",
    "description": "max records to return",
    "required": true,
    "type": "integer",
    "format": "int32"
  }
}
```

```
skipParam:
  name: skip
  in: query
  description: number of items to skip
  required: true
  type: integer
  format: int32
limitParam:
  name: limit
  in: query
  description: max records to return
  required: true
  type: integer
  format: int32
```

#### 6.4.22 Responses Definitions Object

[](https://spec.openapis.org/oas/v2.0.html#responses-definitions-object)

An object to hold responses to be reused across operations. Response definitions can be referenced to the ones defined here.

This does *not* define global operation responses.

##### 6.4.22.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-8)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | [Response Object](https://spec.openapis.org/oas/v2.0.html#response-object) | A single response definition, mapping a “name” to the response it defines. |

##### 6.4.22.2 Responses Definitions Object Example

[](https://spec.openapis.org/oas/v2.0.html#responses-definitions-object-example)

```
{
  "NotFound": {
    "description": "Entity not found."
  },
  "IllegalInput": {
  	"description": "Illegal input for operation."
  },
  "GeneralError": {
  	"description": "General Error",
  	"schema": {
  		"$ref": "#/definitions/GeneralError"
  	}
  }
}
```

```
NotFound:
  description: Entity not found.
IllegalInput:
  description: Illegal input for operation.
GeneralError:
  description: General Error
  schema:
    $ref: '#/definitions/GeneralError'
```

#### 6.4.23 Security Definitions Object

[](https://spec.openapis.org/oas/v2.0.html#security-definitions-object)

A declaration of the security schemes available to be used in the specification. This does not enforce the security schemes on the operations and only serves to provide the relevant details for each scheme.

##### 6.4.23.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-9)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | [Security Scheme Object](https://spec.openapis.org/oas/v2.0.html#security-scheme-object) | A single security scheme definition, mapping a “name” to the scheme it defines. |

##### 6.4.23.2 Security Definitions Object Example

[](https://spec.openapis.org/oas/v2.0.html#security-definitions-object-example)

```
{
  "api_key": {
    "type": "apiKey",
    "name": "api_key",
    "in": "header"
  },
  "petstore_auth": {
    "type": "oauth2",
    "authorizationUrl": "http://swagger.io/api/oauth/dialog",
    "flow": "implicit",
    "scopes": {
      "write:pets": "modify pets in your account",
      "read:pets": "read your pets"
    }
  }
}
```

```
api_key:
  type: apiKey
  name: api_key
  in: header
petstore_auth:
  type: oauth2
  authorizationUrl: http://swagger.io/api/oauth/dialog
  flow: implicit
  scopes:
    write:pets: modify pets in your account
    read:pets: read your pets
```

#### 6.4.24 Security Scheme Object

[](https://spec.openapis.org/oas/v2.0.html#security-scheme-object)

Allows the definition of a security scheme that can be used by the operations. Supported schemes are basic authentication, an API key (either as a header or as a query parameter) and OAuth2’s common flows (implicit, password, application and access code).

##### 6.4.24.1 Fixed Fields

[](https://spec.openapis.org/oas/v2.0.html#fixed-fields-14)

| Field Name | Type | Validity | Description |
| --- | --- | --- | --- |
| type | `string` | Any | **Required.** The type of the security scheme. Valid values are `"basic"`, `"apiKey"` or `"oauth2"`. |
| description | `string` | Any | A short description for security scheme. |
| name | `string` | `apiKey` | **Required.** The name of the header or query parameter to be used. |
| in | `string` | `apiKey` | **Required** The location of the API key. Valid values are `"query"` or `"header"`. |
| flow | `string` | `oauth2` | **Required.** The flow used by the OAuth2 security scheme. Valid values are `"implicit"`, `"password"`, `"application"` or `"accessCode"`. |
| authorizationUrl | `string` | `oauth2` (`"implicit"`, `"accessCode"`) | **Required.** The authorization URL to be used for this flow. This *SHOULD* be in the form of a URL. |
| tokenUrl | `string` | `oauth2` (`"password"`, `"application"`, `"accessCode"`) | **Required.** The token URL to be used for this flow. This *SHOULD* be in the form of a URL. |
| scopes | [Scopes Object](https://spec.openapis.org/oas/v2.0.html#scopes-object) | `oauth2` | **Required.** The available scopes for the OAuth2 security scheme. |

##### 6.4.24.2 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-10)

| Field Name | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.24.3 Security Scheme Object Example

[](https://spec.openapis.org/oas/v2.0.html#security-scheme-object-example)

###### 6.4.24.3.1 Basic Authentication Sample

[](https://spec.openapis.org/oas/v2.0.html#basic-authentication-sample)

```
{
  "type": "basic"
}
```

```
type: basic
```

###### 6.4.24.3.2 API Key Sample

[](https://spec.openapis.org/oas/v2.0.html#api-key-sample)

```
{
  "type": "apiKey",
  "name": "api_key",
  "in": "header"
}
```

```
type: apiKey
name: api_key
in: header
```

###### 6.4.24.3.3 Implicit OAuth2 Sample

[](https://spec.openapis.org/oas/v2.0.html#implicit-oauth2-sample)

```
{
  "type": "oauth2",
  "authorizationUrl": "http://swagger.io/api/oauth/dialog",
  "flow": "implicit",
  "scopes": {
    "write:pets": "modify pets in your account",
    "read:pets": "read your pets"
  }
}
```

```
type: oauth2
authorizationUrl: http://swagger.io/api/oauth/dialog
flow: implicit
scopes:
  write:pets: modify pets in your account
  read:pets: read your pets
```

#### 6.4.25 Scopes Object

[](https://spec.openapis.org/oas/v2.0.html#scopes-object)

Lists the available scopes for an OAuth2 security scheme.

##### 6.4.25.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-11)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | `string` | Maps between a name of a scope to a short description of it (as the value of the property). |

##### 6.4.25.2 Patterned Objects

[](https://spec.openapis.org/oas/v2.0.html#patterned-objects-10)

| Field Pattern | Type | Description |
| --- | --- | --- |
| ^x- | Any | Allows extensions to the Swagger Schema. The field name *MUST* begin with `x-`, for example, `x-internal-id`. The value can be `null`, a primitive, an array or an object. See [Vendor Extensions](https://spec.openapis.org/oas/v2.0.html#specification-extensions) for further details. |

##### 6.4.25.3 Scopes Object Example

[](https://spec.openapis.org/oas/v2.0.html#scopes-object-example)

```
{
  "write:pets": "modify pets in your account",
  "read:pets": "read your pets"
}
```

```
write:pets: modify pets in your account
read:pets: read your pets
```

#### 6.4.26 Security Requirement Object

[](https://spec.openapis.org/oas/v2.0.html#security-requirement-object)

Lists the required security schemes to execute this operation. The object can have multiple security schemes declared in it which are all required (that is, there is a logical AND between the schemes).

The name used for each property *MUST* correspond to a security scheme declared in the [Security Definitions](https://spec.openapis.org/oas/v2.0.html#security-definitions-object).

##### 6.4.26.1 Patterned Fields

[](https://spec.openapis.org/oas/v2.0.html#patterned-fields-12)

| Field Pattern | Type | Description |
| --- | --- | --- |
| {name} | \[`string`\] | Each name must correspond to a security scheme which is declared in the [Security Definitions](https://spec.openapis.org/oas/v2.0.html#securityDefinitions). If the security scheme is of type `"oauth2"`, then the value is a list of scope names required for the execution. For other security scheme types, the array *MUST* be empty. |

##### 6.4.26.2 Security Requirement Object Examples

[](https://spec.openapis.org/oas/v2.0.html#security-requirement-object-examples)

###### 6.4.26.2.1 Non-OAuth2 Security Requirement

[](https://spec.openapis.org/oas/v2.0.html#non-oauth2-security-requirement)

```
{
  "api_key": []
}
```

```
api_key: []
```

###### 6.4.26.2.2 OAuth2 Security Requirement

[](https://spec.openapis.org/oas/v2.0.html#oauth2-security-requirement)

```
{
  "petstore_auth": [
    "write:pets",
    "read:pets"
  ]
}
```

```
petstore_auth:
- write:pets
- read:pets
```

### 6.5 Specification Extensions

[](https://spec.openapis.org/oas/v2.0.html#specification-extensions)

While the Swagger Specification tries to accommodate most use cases, additional data can be added to extend the specification at certain points.

The extensions properties are always prefixed by `"x-"` and can have any valid JSON format value.

The extensions may or may not be supported by the available tooling, but those may be extended as well to add requested support (if tools are internal or open-sourced).

### 6.6 Security Filtering

[](https://spec.openapis.org/oas/v2.0.html#security-filtering)

Some objects in the Swagger specification may be declared and remain empty, or completely be removed, even though they are inherently the core of the API documentation.

The reasoning behind it is to allow an additional layer of access control over the documentation itself. While not part of the specification itself, certain libraries may choose to allow access to parts of the documentation based on some form of authentication/authorization.

Two examples for this:

1.  The [Paths Object](https://spec.openapis.org/oas/v2.0.html#paths-object) may be empty. It may be counterintuitive, but this may tell the viewer that they got to the right place, but can’t access any documentation. They’d still have access to the [Info Object](https://spec.openapis.org/oas/v2.0.html#info-object) which may contain additional information regarding authentication.
2.  The [Path Item Object](https://spec.openapis.org/oas/v2.0.html#path-item-object) may be empty. In this case, the viewer will be aware that the path exists, but will not be able to see any of its operations or parameters. This is different than hiding the path itself from the [Paths Object](https://spec.openapis.org/oas/v2.0.html#paths-object) so the user will not be aware of its existence. This allows the documentation provider a finer control over what the viewer can see.

## A. References

[](https://spec.openapis.org/oas/v2.0.html#references)

### A.1 Normative references

[](https://spec.openapis.org/oas/v2.0.html#normative-references)

\[HTML401\]

[HTML 4.01 Specification](https://www.w3.org/TR/html401/). Dave Raggett; Arnaud Le Hors; Ian Jacobs. W3C. 27 March 2018. W3C Recommendation. URL: [https://www.w3.org/TR/html401/](https://www.w3.org/TR/html401/)

\[IANA-HTTP-STATUS-CODES\]

[Hypertext Transfer Protocol (HTTP) Status Code Registry](https://www.iana.org/assignments/http-status-codes/). IANA. URL: [https://www.iana.org/assignments/http-status-codes/](https://www.iana.org/assignments/http-status-codes/)

\[JSON-Reference\]

[JSON Reference](https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03). Paul Bryan; Kris Zyp. Internet Engineering Task Force (IETF). 16 September 2012. Internet-Draft. URL: [https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03](https://datatracker.ietf.org/doc/html/draft-pbryan-zyp-json-ref-03)

\[JSON-Schema-04\]

[JSON Schema: core definitions and terminology. Draft 4](https://datatracker.ietf.org/doc/html/draft-zyp-json-schema-04). Kris Zyp; Francis Galiegue; Gary Court. Internet Engineering Task Force (IETF). 31 January 2013. Internet-Draft. URL: [https://datatracker.ietf.org/doc/html/draft-zyp-json-schema-04](https://datatracker.ietf.org/doc/html/draft-zyp-json-schema-04)

\[JSON-Schema-Validation-04\]

[JSON Schema: interactive and non interactive validation. Draft 4](https://datatracker.ietf.org/doc/html/draft-fge-json-schema-validation-00). Kris Zyp; Francis Galiegue; Gary Court. Internet Engineering Task Force (IETF). 1 February 2013. Internet-Draft. URL: [https://datatracker.ietf.org/doc/html/draft-fge-json-schema-validation-00](https://datatracker.ietf.org/doc/html/draft-fge-json-schema-validation-00)

\[RFC2119\]

[Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119). S. Bradner. IETF. March 1997. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119)

\[RFC3339\]

[Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339). G. Klyne; C. Newman. IETF. July 2002. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc3339](https://www.rfc-editor.org/rfc/rfc3339)

\[RFC6838\]

[Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838). N. Freed; J. Klensin; T. Hansen. IETF. January 2013. Best Current Practice. URL: [https://www.rfc-editor.org/rfc/rfc6838](https://www.rfc-editor.org/rfc/rfc6838)

\[RFC6901\]

[JavaScript Object Notation (JSON) Pointer](https://www.rfc-editor.org/rfc/rfc6901). P. Bryan, Ed.; K. Zyp; M. Nottingham, Ed. IETF. April 2013. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc6901](https://www.rfc-editor.org/rfc/rfc6901)

\[RFC7159\]

[The JavaScript Object Notation (JSON) Data Interchange Format](https://www.rfc-editor.org/rfc/rfc7159). T. Bray, Ed. IETF. March 2014. Proposed Standard. URL: [https://www.rfc-editor.org/rfc/rfc7159](https://www.rfc-editor.org/rfc/rfc7159)

\[RFC7231\]

[Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content](https://httpwg.org/specs/rfc7231.html). R. Fielding, Ed.; J. Reschke, Ed. IETF. June 2014. Proposed Standard. URL: [https://httpwg.org/specs/rfc7231.html](https://httpwg.org/specs/rfc7231.html)

\[YAML\]

[YAML Ain’t Markup Language (YAML™) Version 1.2](http://yaml.org/spec/1.2/spec.html). Oren Ben-Kiki; Clark Evans; Ingy döt Net. 1 October 2009. URL: [http://yaml.org/spec/1.2/spec.html](http://yaml.org/spec/1.2/spec.html)

[↑](https://spec.openapis.org/oas/v2.0.html#title)
