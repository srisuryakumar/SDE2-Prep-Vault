---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 5 — NoSQL Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [database, nosql, cassandra]
---

# Cassandra (Wide-Column Store)

## Intuition
Cassandra is designed for massive write throughput and horizontal scale. It natively replicates across data centers (multi-region active-active).
Its fundamental design constraint: **every query MUST include the partition key**.

## Data Modeling Rule
**Schema is driven by your query access patterns, NOT entity relationships.** Ask "What queries will I run?" *then* design the table. You will often create multiple denormalized tables for the same data just to support different query patterns.

## Keys
- **Partition Key:** Determines which node stores these rows. Must be provided in every query.
- **Clustering Key:** Sort order for rows within a single partition.
```sql
CREATE TABLE orders_by_user (
    user_id    UUID,
    order_date TIMESTAMP,
    order_id   UUID,
    status     TEXT,
    PRIMARY KEY (user_id, order_date, order_id)
);
-- user_id is the partition key
-- order_date and order_id are clustering keys
```

## Consistency Levels
Assuming Replication Factor (RF) = 3 (each row stored on 3 nodes):
- **ONE:** Reads from 1 replica. Fastest; may read stale data.
- **QUORUM:** Reads from 2 replicas (RF/2 + 1). Balanced, tolerates 1 node down.
- **ALL:** Reads from 3 replicas. Slowest, most consistent, fails if any node is down.

**Strong Consistency Trick:** Write at QUORUM + Read at QUORUM. There is guaranteed overlap, meaning at least one node in the read quorum has the latest write.
