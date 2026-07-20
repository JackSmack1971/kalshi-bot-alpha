---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/linksets"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:11.068Z"
---
# [](https://spec.openapis.org/registry/media-type/linksets#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/linksets#link-sets-sets-of-rfc8288-web-links)Link Sets: Sets of RFC8288 Web Links

**Media Type(s):**

• application/linkset ([IANA](https://www.iana.org/assignments/media-types/application/linkset)) – [RFC9264](https://www.rfc-editor.org/rfc/rfc9264), [RFC8288](https://www.rfc-editor.org/rfc/rfc8288)
• application/linkset+json ([IANA](https://www.iana.org/assignments/media-types/application/linkset+json)) – [RFC9264](https://www.rfc-editor.org/rfc/rfc9264)

**OAS References:**

• [Modeling Link Headers](https://spec.openapis.org/oas/latest.html#modeling-link-headers) ([Header Object](https://spec.openapis.org/oas/latest.html#header-object))

## [](https://spec.openapis.org/registry/media-type/linksets#summary)Summary

The JSON form for linksets is used to define the schema-ready data form for both of these media types, with `application/linkset` being usable for HTTP `Link` header values using the conversion defined in the RFC.

## [](https://spec.openapis.org/registry/media-type/linksets#remarks)Remarks

The `application/linkset+json` data model is used with the [Schema Object](https://spec.openapis.org/oas/latest.html#schema-object) for both media types, with the choice of the parent key for the [Media Type Object](https://spec.openapis.org/oas/latest.html#media-type-object) (with or without `+json`) determining only the serialization format.
