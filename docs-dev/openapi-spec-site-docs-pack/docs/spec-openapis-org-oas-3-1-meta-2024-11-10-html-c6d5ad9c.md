---
title: "JSON Schema Vocabulary used in OpenAPI 3.1"
source_url: "https://spec.openapis.org/oas/3.1/meta/2024-11-10.html"
host: "spec.openapis.org"
depth: 1
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:01.315Z"
---
```
{
  "$id": "https://spec.openapis.org/oas/3.1/meta/2024-11-10",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "OAS Base Vocabulary",
  "description": "A JSON Schema Vocabulary used in the OpenAPI Schema Dialect",
  "$dynamicAnchor": "meta",
  "$vocabulary": {
    "https://spec.openapis.org/oas/3.1/vocab/base": true
  },
  "type": [
    "object",
    "boolean"
  ],
  "properties": {
    "discriminator": {
      "$ref": "#/$defs/discriminator"
    },
    "example": true,
    "externalDocs": {
      "$ref": "#/$defs/external-docs"
    },
    "xml": {
      "$ref": "#/$defs/xml"
    }
  },
  "$defs": {
    "discriminator": {
      "$ref": "#/$defs/extensible",
      "properties": {
        "mapping": {
          "additionalProperties": {
            "type": "string"
          },
          "type": "object"
        },
        "propertyName": {
          "type": "string"
        }
      },
      "required": [
        "propertyName"
      ],
      "type": "object",
      "unevaluatedProperties": false
    },
    "extensible": {
      "patternProperties": {
        "^x-": true
      }
    },
    "external-docs": {
      "$ref": "#/$defs/extensible",
      "properties": {
        "description": {
          "type": "string"
        },
        "url": {
          "format": "uri-reference",
          "type": "string"
        }
      },
      "required": [
        "url"
      ],
      "type": "object",
      "unevaluatedProperties": false
    },
    "xml": {
      "$ref": "#/$defs/extensible",
      "properties": {
        "attribute": {
          "type": "boolean"
        },
        "name": {
          "type": "string"
        },
        "namespace": {
          "format": "uri",
          "type": "string"
        },
        "prefix": {
          "type": "string"
        },
        "wrapped": {
          "type": "boolean"
        }
      },
      "type": "object",
      "unevaluatedProperties": false
    }
  }
}

```
