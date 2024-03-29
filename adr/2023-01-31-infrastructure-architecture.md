# API infrastructure architecture

Date: `2023-01-31`

## Status

`APPROVED`

## Context

With the decision to host the URL Shortener as a production service, we need to decide on the API's infrastructure architecture.  The goal of this ADR is to document the architectural decisions and the reasoning behind them.

## Options

We have the following options for the API's infrastructure architecture:

1. [AWS Lambda with CloudFront](#option-1-aws-lambda-with-cloudfront)
1. [AWS Lambda with API Gateway](#option-2-aws-lambda-with-api-gateway)
1. [Persistent service using AWS Elastic Container Service (ECS)](#option-3-persistent-service-using-aws-elastic-container-service-ecs)

### Option 1: AWS Lambda with CloudFront
Use a Docker image based AWS Lambda function to run the API, accessed using a Lambda Function URL.  A CloudFront distribution will then provide a custom URL and caching for the API.  Data storage will be provided by AWS DynamoDB.

### Option 2: AWS Lambda with API Gateway
Similar to option 1, but using API Gateway to provide a custom URL and caching for the API.  Data storage will be provided by AWS DynamoDB.

### Option 3: Persistent service using AWS Elastic Container Service (ECS)
Use ECS to host a persistent service that runs the API.  A load balancer will provide access to the ECS service and a CloudFront distribution could be added to provide caching.  As with option 1, DynamoDB will be used for data storage.

## Additional considerations

We have chosen to only use highly managed AWS services.  This will reduce the amount of maintenance and operations work required to support the product.

## Decision

We will be using `Option 1: AWS Lambda with CloudFront` for the URL Shortener's infrastructure.  This will provide the following benefits:  

1. The API will be highly available and scalable as it is using AWS Lambda, which scales much faster than ECS services.
1. CloudFront will further improve the availability and performance of the API by caching redirect responses and serving responses geographically close to the user.
1. The use of Lambda Function URLs entirely removes the need to manage an API Gateway instance.
1. DynamoDB will provide a highly available and scalable data store for the API.
1. There is not currently a need for a persistent service, so the value of ECS in that regard is negated.
1. By avoiding the use of ECS, we also do not need to include a load balancer in our architecture.  This further reduces the request bottlenecks and improves the scalability of the API.

![URL Shortener API infrastructure diagram](attachments/2023-01-31-infrastructure-architecture.png)
__Figure 1:__ URL Shortener API infrastructure diagram ([source](attachments/2023-01-31-infrastructure-architecture.drawio))

## Consequences

### DynamoDB data model

We will need to be careful in how we design our DynamoDB item data model.  It is imperative that we do not create a situation where data cannot be directly retrieved and must instead by scanned for.  The reason being that DynamoDB scan operations are expensive and inefficient.

### Persistent service limitation

If we discover a future requirement that needs a persistent service, we will need to add additional infrastructure to support it.  As persistent services are generally only needed to run scheduled or long-running jobs, this should not impact us:

- Scheduled jobs can be handled with AWS CloudWatch Events and AWS Lambda.
- Long-running jobs would have to exceed 15 minutes before they became problematic for the Lambda.  If they did, we could then look at using a Step Function or introducting a dedicated ECS task that is triggered via a CloudWatch Event.

### Lambda cold-start time

A limitation of Lambda is that on a function's first invocation, it will take longer to execute and return a response than on subsequent invocations.  If we discover that the API's Lambda function cold-start time is impacting user experience, we can mitigate with a few different startup strategies:

- Use a health check to keep Lambda function's warm.
- Use Lambda provisioned concurrency to always have a configurable nubmer of Lambda functions warm and ready to serve requests.

### Preventing malicious network egress

There is a requirement for the API to check shortened URLs are still valid.  This will be accomplished by making a HEAD request to the full URL and considering it invalid if the response is in the 4xx HTTP status code range.  

This will require the API to perform DNS looksup and make network requests to external URLs.  To mitigate the risk of malicious network egress, Route53's DNS Resolver Firewall will be used to only allow the API to perform DNS lookups for domains that are part of the service's allow list (e.g. `*.canada.ca` and `*.gc.ca`).

In addition to the above, we will limit egress to TCP on port 443 using Lambda security groups.  

### Preventing malicious requests

AWS Web Application Firewall (WAF) and Shield Advnaced will be used to protect the API from malicious requests and DDoS attacks.  The WAF will be configured to:

- Block requests that do not match an safelist of request URL patterns.
- Block requests that contain malicious payloads (e.g. SQL injection, XSS, directory traversal, etc.).
- Rate limit `POST` and `PUT` requests to the API by IP address.

### Protecting data in-transit

In addition to using data encryption in-transit and at rest, we'll also setup AWS private endpoints for DynamoDB, S3 and CloudWatch.  This will prevent the API from routing any data to those services through the public internet.  It will travel directly from the API's Virtual Private Cloud (VPC) to the AWS service.

### Intrusion detection

We will be using AWS GuardDuty to detect anomalous activity in the API's AWS account.  In addition to this, the API's CloudWatch logs will be sent to Azure Sentinel where we will be able to monitor for suspicious activity.

### Direct access to Lambda function via its Function URL

The API will need to have a mechanism that prevents direct access to it using the raw Lambda Function URL.  The reason for this is that it would bypass the CloudFront distribution and WAF.  This could be accomplished by either:

- having CloudFront add a secret header value and then ensuring it's present in the API's handler; or
- by redirecting all raw Function URL requests to the main API URL. 



## Other architectual decisions

### Nightly DynamoDB backup
In order to satify [CP-9 (Contigency Planning - information systems backup)](https://github.com/cds-snc/url-shortener-documentation/issues/171), we needed to setup an AWS Backup for our DynamoDB tables. Currently, the backup executes via AWS Backup at 12:00am every day and is stored in AWS Vault. In order to allow persistency and to create/run the backup, we wrote a [backup plan](https://github.com/cds-snc/url-shortener/tree/main/terragrunt/aws/backup_plan) using terraform that executes the backup actions.
