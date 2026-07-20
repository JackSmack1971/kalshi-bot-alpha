---
title: "Format Registry"
source_url: "https://spec.openapis.org/registry/format/double-int.html"
host: "spec.openapis.org"
depth: 2
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:37:08.346Z"
---
# [](https://spec.openapis.org/registry/format/double-int.html#format-registry)[Format Registry](https://spec.openapis.org/registry/format/)

## [](https://spec.openapis.org/registry/format/double-int.html#double-int---an-integer-that-can-be-stored-in-an-ieee-754-double-precision-number-without-loss-of-precision)double-int - an integer that can be stored in an IEEE 754 double-precision number without loss of precision

JSON Data Type: `number`.

The `double-int` format represents an integer that can be stored in an IEEE 754 double-precision number without loss of precision. The range of values is -(253)+1 to (253)-1.

This format is useful for systems that need to support languages (such as JavaScript) that store all numeric values as IEEE 754 double-precision numbers.
