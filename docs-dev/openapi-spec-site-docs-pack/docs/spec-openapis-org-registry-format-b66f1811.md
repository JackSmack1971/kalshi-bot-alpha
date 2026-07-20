---
title: "Formats Registry"
source_url: "https://spec.openapis.org/registry/format/"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:12.147Z"
---
# [](https://spec.openapis.org/registry/format/#formats-registry)Formats Registry

## [](https://spec.openapis.org/registry/format/#considerations)Considerations

The existence of a format in this registry DOES NOT require tools to implement it.

If tools choose to implement any format present in this registry, they SHOULD implement the format following the provided behavior.

The registry SHOULD NOT contain two entries that have the same meaning, unless all but one have been deprecated.

## [](https://spec.openapis.org/registry/format/#contributing)Contributing

Please raise a [Pull-Request](https://github.com/OAI/spec.openapis.org/pulls) against the `main` branch and add a new Markdown file to the folder `registries/_format`. The name of the file is considered the registration entry, ignoring the file extension. Alternatively you can open an [Issue](https://github.com/OAI/OpenAPI-Specification/issues) to discuss a registry value.

## [](https://spec.openapis.org/registry/format/#values)Values

For the purpose of [JSON Schema validation](https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-validation-00#section-7.1), each format should specify the set of JSON data types for which it applies. In this registry, these types are shown in the “JSON data type” column.

| Value | Description | JSON Data Type | Source | Deprecated |
| --- | --- | --- | --- | --- |
| [base64url](https://spec.openapis.org/registry/format/base64url.html) | Binary data encoded as a url-safe string as defined in [RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-5) | string |   | Yes |
| [binary](https://spec.openapis.org/registry/format/binary.html) | any sequence of octets | string | [OAS](https://spec.openapis.org/oas/v3.0.3.html#data-types) | Yes |
| [byte](https://spec.openapis.org/registry/format/byte.html) | base64 encoded data as defined in [RFC4648](https://www.rfc-editor.org/rfc/rfc4648#section-4) | string | [OAS](https://spec.openapis.org/oas/v3.0.3.html#data-types) | Yes |
| [char](https://spec.openapis.org/registry/format/char.html) | A single character | string |   | No |
| [commonmark](https://spec.openapis.org/registry/format/commonmark.html) | commonmark-formatted text | string | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [date-time-local](https://spec.openapis.org/registry/format/date-time-local.html) | RFC3339 date-time without the timezone component | string | [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) | No |
| [date-time](https://spec.openapis.org/registry/format/date-time.html) | date and time as defined by date-time - [RFC3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration) | No |
| [date](https://spec.openapis.org/registry/format/date.html) | date as defined by full-date - [RFC3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration) | No |
| [decimal](https://spec.openapis.org/registry/format/decimal.html) | A fixed point decimal number of unspecified precision and range | string, number |   | No |
| [decimal128](https://spec.openapis.org/registry/format/decimal128.html) | A decimal floating-point number with 34 significant decimal digits | string, number |   | No |
| [double-int](https://spec.openapis.org/registry/format/double-int.html) | an integer that can be stored in an IEEE 754 double-precision number without loss of precision | number |   | No |
| [double](https://spec.openapis.org/registry/format/double.html) | double precision floating point number | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [duration](https://spec.openapis.org/registry/format/duration.html) | duration as defined by duration - RFC3339 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration) | No |
| [email](https://spec.openapis.org/registry/format/email.html) | An email address as defined as Mailbox in RFC5321 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-email-addresses) | No |
| [float](https://spec.openapis.org/registry/format/float.html) | single precision floating point number | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [hostname](https://spec.openapis.org/registry/format/hostname.html) | A host name as defined by RFC1123 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-hostnames) | No |
| [html](https://spec.openapis.org/registry/format/html.html) | HTML-formatted text | string | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [http-date](https://spec.openapis.org/registry/format/http-date.html) | date and time as defined by HTTP-date - [RFC7231](https://datatracker.ietf.org/doc/html/rfc7231#section-7.1.1.1) | string |   | No |
| [idn-email](https://spec.openapis.org/registry/format/idn-email.html) | An email address as defined as Mailbox in RFC6531 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-email-addresses) | No |
| [idn-hostname](https://spec.openapis.org/registry/format/idn-hostname.html) | An internationalized host name as defined by RFC5890 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-hostnames) | No |
| [int16](https://spec.openapis.org/registry/format/int16.html) | signed 16-bit integer | number |   | No |
| [int32](https://spec.openapis.org/registry/format/int32.html) | signed 32-bit integer | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [int64](https://spec.openapis.org/registry/format/int64.html) | signed 64-bit integer | number, string | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [int8](https://spec.openapis.org/registry/format/int8.html) | signed 8-bit integer | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [ipv4-cidr](https://spec.openapis.org/registry/format/ipv4-cidr.html) | An IPv4 address in CIDR notation | string | [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632#section-3.1) | No |
| [ipv4](https://spec.openapis.org/registry/format/ipv4.html) | An IPv4 address as defined as dotted-quad by RFC2673 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-ip-addresses) | No |
| [ipv6-cidr](https://spec.openapis.org/registry/format/ipv6-cidr.html) | An IPv6 address in CIDR-style notation | string | [RFC 4291](https://www.rfc-editor.org/rfc/rfc4291#section-2.3) | No |
| [ipv6](https://spec.openapis.org/registry/format/ipv6.html) | An IPv6 address as defined by RFC4673 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-ip-addresses) | No |
| [iri-reference](https://spec.openapis.org/registry/format/iri-reference.html) | A Internationalized Resource Identifier as defined in RFC3987 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-resource-identifiers) | No |
| [iri](https://spec.openapis.org/registry/format/iri.html) | A Internationalized Resource Identifier as defined in RFC3987 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-resource-identifiers) | No |
| [json-pointer](https://spec.openapis.org/registry/format/json-pointer.html) | A JSON string representation of a JSON Pointer as defined in RFC6901 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-json-pointers) | No |
| [language](https://spec.openapis.org/registry/format/language.html) | language tag as defined in [RFC5646](https://www.rfc-editor.org/info/rfc5646/#section-2.1) | string | [RFC5646](https://www.rfc-editor.org/info/rfc5646/#section-2.1) | No |
| [media-range](https://spec.openapis.org/registry/format/media-range.html) | A media type as defined by the `media-range` ABNF production in RFC9110. | string | [OpenAPI](https://www.rfc-editor.org/rfc/rfc9110#field.accept) | No |
| [password](https://spec.openapis.org/registry/format/password.html) | a string that hints to obscure the value. | string | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [regex](https://spec.openapis.org/registry/format/regex.html) | A regular expression as defined in ECMA-262 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-regex) | No |
| [relative-json-pointer](https://spec.openapis.org/registry/format/relative-json-pointer.html) | A JSON string representation of a relative JSON Pointer as defined in draft RFC 01 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-json-pointers) | No |
| [sf-binary](https://spec.openapis.org/registry/format/sf-binary.html) | structured fields byte sequence as defined in \[RFC8941\] | string | [RFC 8941](https://www.rfc-editor.org/rfc/rfc8941#name-byte-sequences) | No |
| [sf-boolean](https://spec.openapis.org/registry/format/sf-boolean.html) | structured fields boolean as defined in \[RFC8941\] | string | [RFC 8941](https://www.rfc-editor.org/rfc/rfc8941#name-booleans) | No |
| [sf-decimal](https://spec.openapis.org/registry/format/sf-decimal.html) | structured fields decimal as defined in \[RFC8941\] | number | [RFC 8941](https://www.rfc-editor.org/rfc/rfc8941#name-decimals) | No |
| [sf-integer](https://spec.openapis.org/registry/format/sf-integer.html) | structured fields integer as defined in \[RFC8941\] | number | [RFC 8941](https://www.rfc-editor.org/rfc/rfc8941#name-integers) | No |
| [sf-string](https://spec.openapis.org/registry/format/sf-string.html) | structured fields string as defined in \[RFC8941\] | string | [RFC 8941](https://www.rfc-editor.org/rfc/rfc8941#name-strings) | No |
| [sf-token](https://spec.openapis.org/registry/format/sf-token.html) | structured fields token as defined in \[RFC8941\] | string | [RFC 8941](https://www.rfc-editor.org/rfc/rfc8941#name-tokens) | No |
| [time-local](https://spec.openapis.org/registry/format/time-local.html) | RFC3339 time without the timezone component | string | [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) | No |
| [time](https://spec.openapis.org/registry/format/time.html) | time as defined by full-time - RFC3339 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-dates-times-and-duration) | No |
| [uint16](https://spec.openapis.org/registry/format/uint16.html) | unsigned 16-bit integer | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [uint32](https://spec.openapis.org/registry/format/uint32.html) | unsigned 32-bit integer | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [uint64](https://spec.openapis.org/registry/format/uint64.html) | unsigned 64-bit integer | number, string | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [uint8](https://spec.openapis.org/registry/format/uint8.html) | unsigned 8-bit integer | number | [OAS](https://spec.openapis.org/oas/latest.html#data-types) | No |
| [unixtime](https://spec.openapis.org/registry/format/unixtime.html) | seconds since Jan 1st 1970 - [IEEE1003.1-2024/POSIX.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | number, string | [IEEE1003.1-2024](https://pubs.opengroup.org/onlinepubs/9799919799/) | No |
| [uri-reference](https://spec.openapis.org/registry/format/uri-reference.html) | A URI reference as defined in [RFC3986](https://www.rfc-editor.org/info/rfc3986) | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-resource-identifiers) | No |
| [uri-template](https://spec.openapis.org/registry/format/uri-template.html) | A URI Template as defined in RFC6570 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-uri-template) | No |
| [uri](https://spec.openapis.org/registry/format/uri.html) | A Uniform Resource Identifier as defined in RFC3986 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-resource-identifiers) | No |
| [uuid](https://spec.openapis.org/registry/format/uuid.html) | A Universally Unique IDentifier as defined in RFC4122 | string | [JSON Schema](https://json-schema.org/draft/2020-12/json-schema-validation.html#name-resource-identifiers) | No |
