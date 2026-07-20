---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/ipv6-cidr.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:09.292Z"
---
# [](https://spec.openapis.org/registry/format/ipv6-cidr.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/ipv6-cidr.html#ipv6-cidr---an-ipv6-address-in-cidr-style-notation)ipv6-cidr - An IPv6 address in CIDR-style notation

JSON Data Type: `string`.

The `ipv6-cidr` format represents an IPv6 address in CIDR notation, with the syntax described in [RFC4291](https://www.rfc-editor.org/rfc/rfc4291#section-2.3).

The address MUST be a valid `ipv6` address, and the prefix length MUST be a decimal integer from `0` to `128`, inclusive. A plain IPv6 address without a prefix length is not accepted.

Examples of valid values include `2001:db8::/32` and `::1/128`.
