---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 5 — NoSQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, nosql, postgresql]
---

# When to use NoSQL vs PostgreSQL

## Intuition
PostgreSQL handles the vast majority of workloads. Relational databases win when you need: ACID transactions, complex joins, ad-hoc queries, a stable schema, or referential integrity enforcement.
Consider NoSQL only when you hit specific bottlenecks or requirements.

## Signals to choose NoSQL
| Signal | Consider |
| :--- | :--- |
| >50,000 writes/sec, single-node PostgreSQL saturated | Cassandra, DynamoDB |
| Schema changes every sprint, migration overhead is a bottleneck | MongoDB |
| Data is naturally document-shaped (nested, variable per record) | MongoDB |
| Multi-region active-active writes required | Cassandra, DynamoDB |
| Time-series at scale (billions of sensor readings) | InfluxDB, TimescaleDB |
| Full-text search with relevance ranking | Elasticsearch |
