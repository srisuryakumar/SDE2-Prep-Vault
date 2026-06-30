---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 2 — CAP Theorem"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["PACELC Theorem", "CP vs AP Systems"]
tags: [distributed-systems, cap, architecture]
---

# CAP Theorem

## Intuition
The CAP Theorem states that in a distributed data store, you can only guarantee two out of the following three properties during a network partition:
- **Consistency (C):** Every read receives the most recent write, or an error. All nodes see the same data at the same time.
- **Availability (A):** Every request to a non-failing node receives a non-error response, though it might not contain the most recent write (stale data).
- **Partition Tolerance (P):** The system continues to operate despite an arbitrary number of messages being dropped or delayed between nodes (a network partition).

## P Isn't Optional
Beginners read CAP as "pick any 2 of 3." In practice, **you cannot opt out of Partition Tolerance**. Networks *will* partition eventually.
The real choice is: **When a partition happens, do you sacrifice Consistency (by staying Available) or sacrifice Availability (by refusing to respond to maintain Consistency)?**
