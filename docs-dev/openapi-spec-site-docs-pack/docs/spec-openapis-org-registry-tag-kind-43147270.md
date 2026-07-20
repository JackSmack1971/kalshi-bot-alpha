---
title: "Tag Kinds Registry"
source_url: "https://spec.openapis.org/registry/tag-kind/index.html"
host: "spec.openapis.org"
depth: 1
selector: "article,main,[role=main]"
fetched_at: "2026-07-17T17:36:54.516Z"
---
# [](https://spec.openapis.org/registry/tag-kind/index.html#tag-kinds-registry)Tag Kinds Registry

## [](https://spec.openapis.org/registry/tag-kind/index.html#supporting-versions)Supporting Versions

OpenAPI 3.2 added more structure to tags, including by adding a `kind` property to a [Tag Object](https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.2.0.md#tag-object). Support for the values in this registry should not be expected until tools add support for the 3.2 version.

## [](https://spec.openapis.org/registry/tag-kind/index.html#contributing)Contributing

Please raise a [Pull-Request](https://github.com/OAI/spec.openapis.org/pulls) against the `main` branch and add a new Markdown file to the folder `registries/_tag-kind`. The name of the file is considered the registration entry, ignoring the file extension. Alternatively you can open an [Issue](https://github.com/OAI/OpenAPI-Specification/issues) to discuss a registry value.

## [](https://spec.openapis.org/registry/tag-kind/index.html#values)Values

| Value | Description |
| --- | --- |
| [audience](https://spec.openapis.org/registry/tag-kind/audience.html) | Tags with `kind: audience` indicate the intended audience for an operation. |
| [badge](https://spec.openapis.org/registry/tag-kind/badge.html) | Tags with `kind: badge` are applied as visible badges in documentation. |
| [nav](https://spec.openapis.org/registry/tag-kind/nav.html) | Tags with `kind: nav` are used in documentation to group operations into sections |
