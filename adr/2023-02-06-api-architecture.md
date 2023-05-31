# API Decisions

Date: `2023-02-06`

## Status

`APPROVED`

## Framework Context

As a minimum viable product it has been decided to take an API first approach for the development of the url-shortener. This ADR documents the decision to use [FastAPI](https://fastapi.tiangolo.com) as a basis for the API.

## Framework Requirements

Whilst the full requirements are not known at this time; some key features/requirements are universally required

- Familiarity to CDS-SNC staff

- Ease of use

- Ease of deployment

- Active development ecosystem

## Framework Decision

Based on the above requirements and the following observations the decision was made to develop the initial MVP with [FastAPI](https://fastapi.tiangolo.com)

- FastAPI is used by a number of CDS-SNC projects such as
  
  - [GitHub - cds-snc/scan-websites: On-demand scanning of websites for accessibility and security vulnerabilities/compliance / Analyse à la demande des sites Web pour les vulnérabilités/conformité en matière d&#39;accessibilité et de sécurité](https://github.com/cds-snc/scan-websites)
  
  - [GitHub - cds-snc/scan-files: File scanning for CDS Platform products](https://github.com/cds-snc/scan-files)
  
  - [GitHub - cds-snc/sre-bot: Slack bot for site reliability engineering](https://github.com/cds-snc/sre-bot)
  
  - [GitHub - cds-snc/github-secret-scanning: GitHub secret scanning alert service](https://github.com/cds-snc/github-secret-scanning)
  
  - [GitHub - cds-snc/list-manager: CDS list manager](https://github.com/cds-snc/list-manager)

- The second [commit](https://github.com/cds-snc/url-shortener/commit/ad07b0e556725da102665361fc90f90503bc783a) introduced FastAPI very early into the development

## Framework Consequences

The initial development versions of the url-shortener were a side project/learning opportunity. As a broader cds-snc/government need has been identified the decision has been made to add a dedicated team to the development of the url-shortener.

During dicussions that team decided to move to using highly managed infrastructure as detailed in [url-shortener/2023-01-31-infrastructure-architecture.md at main · cds-snc/url-shortener · GitHub](https://github.com/cds-snc/url-shortener/blob/main/adr/2023-01-31-infrastructure-architecture.md) which includes the deployment of the API via AWS Lambda and the utilization of DynamoDB

## General Development approach

The API will generally be a RESTful/RESTISH/CRUD API making use of HTTP verbs but not neccesarily following the full REST approach - that is to say it will send/recieve JSON payloads and make use of appropriate HTTP response codes.

The initial version of the API will serve regular HTTP responses consisting of HTML as an initial interface for use/testing - though it is likely that the frontend will be moved to a separate repository/out of the API folder at a future date.

## Versioning

Apart from the ops related endpoints the API shall be versioned using the url .e.g. /v1

## Configuration

The API shall be configured using environment variables.

## Authentication & Authorization

There will be no authentication or authorization required to retrieve a shorturl.

Only autenticated and authroized users shall be able to create a shorturl to an approved domain - at this stage an authentication/authorization strategy has not been determined.

## Allowed/Blocked Domains

The URL shortener shall only be allowed to create URLs for predefined target URLs. That is to say, each target domain shall be explicity allowed. The allowlist of domains should consist of FQDNs separated by commas provided via environment variables. Wildcard domains are allowed. The order of the allowed domains is not significant. Multiple entries for the same fully qualified domain should not be present.

# Endpoints

## Ops Endpoints

To aid in automated ops workflows the API shall expose the following 'GET' endpoints

* /version - Which shall return the GIT_SHA of the currently deployed code

## / - POST

## /v1/shorten - POST

The API accepts either a JSON payload or a URL-form encoded payload constisting of `original_url.`



The API will return either a JSON response in the following form

```json
{
    "short_url": <the shortened url>,
    "original_url": <the original url>,
    "status": "OK" or "ERROR"
}
```

or redirect to the / GET action which renders the index page with appropriate error messaging to the user. If there is an error there will be an additional 'error' with a message in the response payload.



## /{short-url} -GET

If the requested short-url cannot be found the system will return a 404 response

If the short url is found - the system will return a HTTP 200 response consisting of a HTML redirect notice. The current redirect does not make use of a '<meta http-equiv="refresh" content="10; url='https://canada.ca'" />' tag
