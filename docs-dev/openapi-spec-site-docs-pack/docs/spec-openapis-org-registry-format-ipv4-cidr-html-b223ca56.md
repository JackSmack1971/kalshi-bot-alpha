---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/ipv4-cidr.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:09.180Z"
---
# [](https://spec.openapis.org/registry/format/ipv4-cidr.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/ipv4-cidr.html#ipv4-cidr---an-ipv4-address-in-cidr-notation)ipv4-cidr - An IPv4 address in CIDR notation

JSON Data Type: `string`.

The `ipv4-cidr` format represents an IPv4 address in CIDR notation, with the address and prefix-length syntax described in [RFC4632](https://www.rfc-editor.org/rfc/rfc4632#section-3.1).

The address MUST be a valid `ipv4` address, and the prefix length MUST be a decimal integer from `0` to `32`, inclusive. A plain IPv4 address without a prefix length is not accepted.

Examples of valid values include `10.0.0.0/8` and `192.168.1.0/24`.
