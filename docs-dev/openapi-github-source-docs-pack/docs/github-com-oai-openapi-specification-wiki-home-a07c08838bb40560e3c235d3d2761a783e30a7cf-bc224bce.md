---
title: "Home"
source_url: "https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf"
host: "github.com"
depth: 3
selector: "article,main"
fetched_at: "2026-07-17T17:43:28.938Z"
---
[OAI](https://github.com/OAI) / **[OpenAPI-Specification](https://github.com/OAI/OpenAPI-Specification)** Public

-   [Notifications](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification) You must be signed in to change notification settings
-   [Fork 9.2k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)
-   [Star 31.1k](https://github.com/login?return_to=%2FOAI%2FOpenAPI-Specification)


# Home

[Jump to bottom](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#wiki-pages-box)

Erik van Wingerden edited this page Jan 13, 2016 · [9 revisions](https://github.com/OAI/OpenAPI-Specification/wiki/Home/_history)

# What is Swagger?

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#what-is-swagger)

Swagger™ is a specification and complete framework implementation for describing, producing, consuming, and visualizing RESTful web services. The overarching goal of Swagger is to enable client and documentation systems to update at the same pace as the server.
The documentation of methods, parameters and models can be tightly integrated into the server code, allowing APIs to always stay in sync.

## Who is Responsible for Swagger?

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#who-is-responsible-for-swagger)

Both the specification and framework implementation are initiatives from Wordnik. Swagger was developed for Wordnik's own use during the development of [http://developer.wordnik.com/docs](http://developer.wordnik.com/docs) and the underlying [http://api.wordnik.com/v4](http://api.wordnik.com/v4/resources.json). Swagger development began in early 2010—the framework being released is currently used by Wordnik’s APIs, which power both internal and external API clients.

## Why is Swagger Useful?

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#why-is-swagger-useful)

The Swagger framework simultaneously addresses server, client, and documentation/sandbox needs for REST APIs. As a specification, it is language-agnostic. It also provides a long runway into new technologies and protocols beyond HTTP.

With Swagger's declarative resource specification, clients can understand and consume services without knowledge of server implementation or access to the server code. The Swagger UI framework allows both developers and non-developers to interact with the API in a sandbox UI that gives clear insight into how the API responds to parameters and options. Swagger happily speaks both JSON and XML, with additional formats in the works.

## Quick Introduction

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#quick-introduction)

Swagger is made up of three components:

-   Server: hosts the REST APIs description that you want to use.
-   Client: uses the REST APIs description from the server.
-   UI: Reads a description of the APIs from the server and renders it as a web-page and an interactive sandbox to play with the APIs.

### Server

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#server)

The typical place to start with a Swagger implementation is with the server. A server will have some number of APIs as well as a api-docs url (something like [http://yourhost.com/api-docs](http://yourhost.com/api-docs)). The api-docs URL is the starting point for Swagger. It contains a JSON description of the resources that are available.

### Client

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#client)

The client is any application that wants to use the APIs on the server. The client is given a URL that points to the api-docs and converts the JSON into an object that can used to call the REST APIs. Clients are available in any number of languages, making it very easy to quickly implement REST APIs that have been documented with Swagger without requiring much new code.

### UI

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#ui)

Finally, the Swagger UI serves a double-purpose as documentation and a way to enable developers to play around with the REST APIs without actually having to write any code. The default Swagger UI can be seen at the [pet store demo](http://petstore.swagger.io/). The default Swagger UI includes a box at the top of the screen for typing in the URL for any api-docs. Since the Swagger UI is completely dynamic, it will read in the api-docs from any site and render the API documentation and enable the calling of the REST APIs. The default Swagger UI can be installed through `npm install swagger-ui`, and the HTML templates can be modified to your liking.

## Creating Your Swagger Specification

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#creating-your-swagger-specification)

The api-docs URL that typically lives on the server and is used by both the client and the Swagger UI is referred to as a Swagger Specification. The Swagger Specification is made up of two files:

-   **Resource Listing:** Lists the APIs that are available and gives a brief description of them.
-   **API Description:** Detailed description of each API in the Resource Listing, including both the functional description (parameters, function names, return values) and human-readable description of how to use the API.

The actual api-docs URL is a Resource Listing JSON that describes the Swagger resources that are available, where they live, and how to use them. If you type the api-docs URL into your browser, you will see the resource listing.

There are three ways to create a Swagger Specification, depending on which server you are using:

-   **Codegen:** This is the traditional way of creating a Swagger Specification. The [swagger codegen](https://github.com/wordnik/swagger-codegen) converts annotations in your code into the Swagger Specification. For an example of the annotations see [this code](https://github.com/swagger-api/swagger-samples/blob/master/java/java-jaxrs/src/main/java/io/swagger/sample/resource/PetStoreResource.java).
-   **Automatically:** Some servers, such as [swagger-node-express](https://npmjs.org/package/swagger-node-express) and [swagger-play](https://github.com/wordnik/swagger-core/tree/master/modules/swagger-play2), will create both your REST APIs and your Swagger Specification for you at the same time.
-   **Manually:** And finally, you can always create your Swagger specification by writing the JSON by hand. After you write your Swagger specification (or if you get a Swagger specification from a different server) you can use one of the Server generators to create your code, such as the [node.js server generator](https://github.com/wordnik/swagger-codegen/tree/master/samples/server-generator/node)

## Navigation

[](https://github.com/OAI/OpenAPI-Specification/wiki/Home/a07c08838bb40560e3c235d3d2761a783e30a7cf#navigation)

-   [Home](https://github.com/OAI/OpenAPI-Specification/wiki/Home)
-   [OAS Maintainers](https://github.com/orgs/OAI/teams/tsc/members)
-   [TSC Minutes](https://github.com/OAI/OpenAPI-Specification/wiki/TSC-Minutes)

### Clone this wiki locally
