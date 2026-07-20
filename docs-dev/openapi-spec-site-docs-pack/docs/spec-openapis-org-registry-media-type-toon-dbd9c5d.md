---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/toon"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:11.386Z"
---
# [](https://spec.openapis.org/registry/media-type/toon#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/toon#token-oriented-object-notation-toon-compact-encoding-of-the-json-data-model-for-llm-prompts)Token-Oriented Object Notation (TOON): Compact encoding of the JSON data model for LLM prompts

**Media Type(s):**

• text/toon (not IANA-registered) – [TOON Specification](https://github.com/toon-format/spec/blob/main/SPEC.md)

## [](https://spec.openapis.org/registry/media-type/toon#summary)Summary

Since TOON is simply an alternate serialization of the JSON data model, and serialization is not a concern of the OAS, `text/toon` can be treated the same as `application/json` for the purposes of the Schema Object.

## [](https://spec.openapis.org/registry/media-type/toon#remarks)Remarks

Note, however, that TOON specifies object property order preservation in terms of encounter order, which is not necessarily the same as the order of properties in a Schema Object. JSON Schema is not able to specify object property order.

Similarly, TOON encoding options such as keyfolding are outside of the scope of the Schema Object and the OAS, as they are not specified as media type parameters.

Finally, the `text/toon` media type is provisional; if it is changed, it is expected that the new media type will work the same as the current one.
