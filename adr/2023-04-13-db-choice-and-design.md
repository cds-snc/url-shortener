# DB choice and design

Date: 2023-04-13

## Status

**DRAFT**.

## Context

We needed to make a decision on how to store data for the URL shortener, primarily a quick an easy way to translate a shortened URL back into the original URL. Additionally, we were unsure what other data elements we may want to store based on the evolution of the product.

## Options

We have adopted the following database design patterns at CDS:

1. Using Aurora PostgreSQL as a relational database
2. DynamoDB using a single NoSQL table design
3. Transitory key-based caching using Redis

### Option 1 (Aurora PostgreSQL)

Based on the simplicity of the data model (one to two tables at most), the overhead of creating an Aurora PostgreSQL cluster with migrations (ex. SQLAlchemy ), we deemed both the time and cost to be egregious compared to the alternatives. The advantage is that we use a simple relational schema.

### Option 2 (DynamoDB)

DynamoDB promises single-digit millisecond performance, easy scalability, and is fully managed, making it the most attractive option in terms of performance and maintenance requirements. It also allows simple point in time recovery, backups, and IAM based access management, which can be more difficult to set up with the other options. The only drawback is that a single table design can become complex to understand, especially when used with secondary indexes.

### Option 3 (Redis)

Redis offers the same index based lookup that makes DynamoDB so performant, however, it would require us to set up the ElastiCache cluster and also manage backups, which again is more overhead that we get from DynamoDB with the same NoSQL overhead.

## Additional considerations

DynamoDB is a technology that can be tricky once you go beyond a simple use case. It is easy to fall into traps with multiple tables as well as running `scan` operations that operate on your entire data set and can cause latency. However, we are confident that with the simple feature set, we can avoid these traps.

## Decision

Based on the low complexity of the data model and the low overhead for getting started with DynamoDB, we will use DynamoDB for now until it no longer matches our use case.

## Consequences

If we find out that we do need a more complex data model, moving from DynamoDB to a relational database design will require more work than if we had gone down the relational path from the beginning. Also continuing to use a single table design may add unwanted complexities and inefficiencies.
