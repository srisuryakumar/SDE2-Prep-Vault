---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 7 — Distributed Transactions"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Idempotent Producers (Kafka)"]
tags: [distributed-systems, idempotency, database]
---

# Idempotency in Distributed Systems

## Intuition
Distributed systems rely heavily on **retries** to recover from ambiguous network failures. Retries are only safe if the operation is **idempotent** (calling it twice has the same effect as calling it once).

## Idempotency Keys
The client generates a unique ID for the specific *logical operation* (not per HTTP request, but per intent) and sends it along. The server checks if it has already processed that key.

## Enforcing it at the Database Level
Checking `if (exists(key))` in application logic is not enough, because a check-then-act sequence is not atomic; two concurrent retries can race past the check.
To make it truly safe, you must enforce a **unique constraint** on the idempotency key column in the database. If two retries race, the database rejects the second `INSERT` with a constraint violation, which the application catches and treats as "already processed" instead of an error.
