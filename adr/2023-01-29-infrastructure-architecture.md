# API infrastructure architecture

Date: `2023-01-31`

## Status

`DRAFT`

## Context

With the decision to host the URL Shortener as a production service, we need to decide on the API's infrastructure architecture.  The goal of this ADR is to document the architectural decisions and the reasoning behind them.

## Options

We have the following options for the API's infrastructure architecture:

1. AWS Lambda with CloudFront
1. AWS Lambda with API Gateway
1. Persistent service using AWS Elastic Container Service (ECS)

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

# Note: Add attachments/diagrams etc to attachments folder 
