---
title: "v3.0"
source_url: "https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0"
host: "github.com"
depth: 3
selector: "article,main"
fetched_at: "2026-07-17T17:43:39.328Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


 ## Files

 main

# v3.0

## Directory actions

## More options

## Directory actions

## More options

## Latest commit

## History

[History](https://github.com/OAI/OpenAPI-Specification/commits/main/_archive_/schemas/v3.0)

[](https://github.com/OAI/OpenAPI-Specification/commits/main/_archive_/schemas/v3.0)

 main

# v3.0

Top

## Folders and files

| Name | Name |
Last commit message

 |

Last commit date

 |
| --- | --- | --- | --- |
|

### parent directory

[

..

](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas) |
|

[pass](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0/pass "pass")


 |

[pass](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0/pass "pass")


 |

 |

 |
|

[README.md](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/schemas/v3.0/README.md "README.md")


 |

[README.md](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/schemas/v3.0/README.md "README.md")


 |

 |

 |
|

[schema.test.mjs](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/schemas/v3.0/schema.test.mjs "schema.test.mjs")


 |

[schema.test.mjs](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/schemas/v3.0/schema.test.mjs "schema.test.mjs")


 |

 |

 |
|

[schema.yaml](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/schemas/v3.0/schema.yaml "schema.yaml")


 |

[schema.yaml](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/schemas/v3.0/schema.yaml "schema.yaml")


 |

 |

 |
|

View all files

 |

## [README.md](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0#readme)

# OpenAPI 3.0.X JSON Schema

[](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0#openapi-30x-json-schema)

This directory contains the YAML source for generating the JSON Schema for validating OpenAPI definitions of versions 3.0.X, which is published on [https://spec.openapis.org](https://spec.openapis.org/).

Due to limitations of GitHub pages, the schemas on the spec site are served with `Content-Type: application/octet-stream`, but should be interpreted as `application/schema+json`.

The source in this directory, which has `WORK-IN-PROGRESS` in its `id`, is *not intended for direct use*.

## Schema `id` dates

[](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0#schema-id-dates)

The published schemas on the spec site have an *iteration date* in their `id`s. This allows the schemas for a release line (in this case 3.0) to be updated independent of the spec patch release cycle.

The iteration version of the JSON Schema can be found in the `id` field. For example, the value of `id: https://spec.openapis.org/oas/3.0/schema/2019-04-02` means this iteration was created on April 2nd, 2019.

We are [working on](https://github.com/OAI/OpenAPI-Specification/issues/4152) how to best provide programmatic access for determining the latest date for each schema.

## Improving the schema

[](https://github.com/OAI/OpenAPI-Specification/tree/main/_archive_/schemas/v3.0#improving-the-schema)

As a reminder, the JSON Schema is not the source of truth for the Specification. In cases of conflicts between the Specification itself and the JSON Schema, the Specification wins. Also, some Specification constraints cannot be represented with the JSON Schema so it's highly recommended to employ other methods to ensure compliance.

The schema only validates the mandatory aspects of the OAS. Validating requirements that are optional, or field usage that has undefined or ignored behavior are not within the scope of this schema. Schemas to perform additional optional validation are [under consideration](https://github.com/OAI/OpenAPI-Specification/issues/4141).

Improvements can be submitted by opening a PR against the `main` branch.

Modify the `schema.yaml` file and add test cases for your changes.

The TSC will then:

-   Run tests on the updated schema
-   Update the iteration version
-   Publish the new version

The [test suite](https://github.com/OAI/OpenAPI-Specification/blob/main/_archive_/tests/v3.0) is part of this package.

```shell
npm install
npm test
```
