---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 5 — NoSQL Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["[[MongoDB (Document Store)]]", "[[Cassandra (Wide-Column Store)]]", ]
tags: [database, distributed-systems, cap-theorem]
---

# CAP Theorem

## Intuition
Eric Brewer's CAP theorem states: In the presence of a **network partition** (P - nodes cannot communicate), a distributed system must choose between **Consistency** (C) and **Availability** (A). It cannot have both.

Because networks ALWAYS fail, you must always have Partition Tolerance (P). So the real choice is between CP and AP when a partition occurs.

## The Choices
- **Consistency (C):** Every read gets the most recent write or an error.
- **Availability (A):** Every request receives a non-error response, but without the guarantee that it contains the most recent write.

## Examples
| Database | CAP Position | Behavior During Partition |
| :--- | :--- | :--- |
| **PostgreSQL (Primary)** | **CP** | Refuses writes to non-primary; may be unavailable, but data is never stale. |
| **Cassandra** | **AP** | Serves reads and writes from both sides; eventual consistency. |
| **Redis Cluster** | **AP** (reads) / **CP** (writes) | Reads from a replica may be stale; writes to primary. |
| **DynamoDB** | **AP** (by default) | Serves eventually-consistent reads. |

## Interview Example
> "You're designing an order history service that must handle 500,000 writes/second globally. Which database and why?"

**Answer:** Cassandra. Order history is append-heavy (new orders only). Queries are always by user_id (the natural partition key). We can tolerate eventual consistency (AP) — a user seeing their order appear 200ms after placing it is perfectly fine. Cassandra's AP model gives us availability during network partitions and linear write scalability. PostgreSQL could not absorb 500K writes/sec on a single primary.

## Related Concepts
- See also [[MongoDB (Document Store)]] for the canonical CP example.
- See also [[Cassandra (Wide-Column Store)]] for the canonical AP example.
