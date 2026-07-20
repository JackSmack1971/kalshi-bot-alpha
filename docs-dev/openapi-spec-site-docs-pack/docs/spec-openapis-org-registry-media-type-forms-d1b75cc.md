---
title: "Media Type Registry"
source_url: "https://spec.openapis.org/registry/media-type/forms"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:10.998Z"
---
# [](https://spec.openapis.org/registry/media-type/forms#media-type-registry)[Media Type Registry](https://spec.openapis.org/registry/media-type/)

## [](https://spec.openapis.org/registry/media-type/forms#forms-ordered-name-value-pairs)Forms: Ordered name-value pairs

**Media Type(s):**

• application/x-www-form-urlencoded ([IANA](https://www.iana.org/assignments/media-types/application/x-www-form-urlencoded)) – [WHATWG URL](https://url.spec.whatwg.org/#application/x-www-form-urlencoded), [HTTP 4.01 §17.13.4.1](https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.1) (historical), [RFC1866 §8.2.1](https://datatracker.ietf.org/doc/html/rfc1866#section-8.2.1) (historical but cited by later RFCs and the OAS)
• multipart/form-data ([IANA](https://www.iana.org/assignments/media-types/multipart/form-data)) – [RFC7578](https://www.rfc-editor.org/rfc/rfc7578.html)

**OAS References:**

• [Encoding By Name](https://spec.openapis.org/oas/latest.html#encoding-by-name)
• [Encoding By Position](https://spec.openapis.org/oas/latest.html#encoding-by-position)
• [Encoding the `x-www-form-urlencoded` Media Type](https://spec.openapis.org/oas/latest.html#encoding-the-x-www-form-urlencoded-media-type)
• [Encoding multipart Media Types](https://spec.openapis.org/oas/latest.html#encoding-multipart-media-types)
• [Appendix C: Using RFC6570-Based Serialization](https://spec.openapis.org/oas/latest.html#appendix-c-using-rfc6570-based-serialization)
• [Appendix E: Percent-Encoding and Form Media Types](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types)
• [Non-JSON Data](https://spec.openapis.org/oas/latest.html#non-json-data)

## [](https://spec.openapis.org/registry/media-type/forms#summary)Summary

Web-style form data consists of name-value pairs, with duplicate names allowed, and are structured either in a way compatible with URI form query strings or as a `multipart` document.

## [](https://spec.openapis.org/registry/media-type/forms#remarks)Remarks

Both form media types use the [Encoding Object](https://spec.openapis.org/oas/latest.html#encoding-object) to map object properties from schema-ready data structures to name-value pairs, with special rules for arrays causing each array value to be treated as a separate pair with the same name.

As of OAS v3.2, endpoint URL query strings can be modeled as a media type using `in: querystring` in the [Parameter Object](https://spec.openapis.org/oas/latest.html#parameter-object). The query string can also be modeled using multiple `in: query` Parameter Objects through mechanisms similar to the Encoding Object.

Note that URL-encoded forms have been defined by different standards organizations at different times, leading to inconsistencies regarding percent-encoding in later standards and implementations; this is addressed in detail in [Appendix E](https://spec.openapis.org/oas/latest.html#appendix-e-percent-encoding-and-form-media-types).

Since v3.3, the OAS provides for a way to preserve ordering, by treating the deserialized content as an array, rather than an object.

## [](https://spec.openapis.org/registry/media-type/forms#examples)Examples

Treating the data as an object, this data:

```
{
  "alpha": 1,
  "beta": 2,
  "gamma": [ 3, 4 ]
}
```

… serializes as `application/x-www-form-urlencoded` to: `alpha=1&beta=2&gamma=3&gamma=4`

and serializes as `multipart/form-data; boundary="4aKOX"` to:

```
--4aKOX
Content-Disposition: form-data; name="alpha"

1
--4aKOX
Content-Disposition: form-data; name="beta"

2
--4aKOX
Content-Disposition: form-data; name="gamma"

3
--4aKOX
Content-Disposition: form-data; name="gamma"

4
--4aKOX--
```

If preservation of value/part order is important, treat the data as an array, where each array item is an object consisting of the key/value pair:

```
[
  { "alpha": 1 },
  { "beta": 2 },
  { "gamma": 3 }
  { "gamma": 4 }
}
```

This distinction can be made clear to a deserializer by using `type: array` in the schema, using the process as described in [Non-JSON Data](https://spec.openapis.org/oas/latest#non-json-data).
