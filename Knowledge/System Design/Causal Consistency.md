---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Consistency Models Overview"]
tags: [distributed-systems, consistency]
---

# Causal Consistency

## Intuition
**Guarantee:** Operations that are **causally related** must be seen in the same order by everyone. Operations that are **independent** can be seen in different orders by different observers.

## Example
If User B replies to User A's post, the reply causally depends on the post. Causal consistency guarantees no user will ever see B's reply *before* seeing A's original post. 
Independent posts by different users, however, can arrive in any order.

## Why use it?
It gives you the ordering guarantees that users actually notice (no out-of-order replies) at a fraction of the coordination cost of strong consistency.
