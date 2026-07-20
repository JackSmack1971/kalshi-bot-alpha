---
title: "JSON Schema for OpenAPI 3.2 - with schema validation"
source_url: "https://spec.openapis.org/oas/3.2/schema-base/2025-11-23.html"
host: "spec.openapis.org"
depth: 1
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:36:59.446Z"
---
```
{
  "$id": "https://spec.openapis.org/oas/3.2/schema-base/2025-11-23",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "description": "The description of OpenAPI v3.2.x Documents using the OpenAPI JSON Schema dialect",
  "$ref": "https://spec.openapis.org/oas/3.2/schema/2025-11-23",
  "properties": {
    "jsonSchemaDialect": {
      "$ref": "#/$defs/dialect"
    }
  },
  "$defs": {
    "dialect": {
      "const": "https://spec.openapis.org/oas/3.2/dialect/2025-09-17"
    },
    "schema": {
      "$dynamicAnchor": "meta",
      "$ref": "https://spec.openapis.org/oas/3.2/dialect/2025-09-17",
      "properties": {
        "$schema": {
          "$ref": "#/$defs/dialect"
        }
      }
    }
  }
}

```
