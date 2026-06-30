---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 7 — Distributed Transactions"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Saga Choreography vs Orchestration"]
tags: [distributed-systems, transactions, microservices]
---

# The Saga Pattern

## Intuition
A saga replaces a single distributed transaction with a **sequence of local transactions**. Each step occurs in a single service's own database and commits independently and immediately. There is no global lock.

## Compensating Transactions
Because steps commit immediately, you cannot simply "roll back" if a later step fails. Instead, every step must have a **compensating transaction** that semantically undoes its effect.
- **Example:** If Step 1 creates an order and Step 2 charges the payment, but Step 3 (reserve inventory) fails, you must run compensating transactions in reverse: Step 2' (issue a refund) and Step 1' (mark order as cancelled).

A compensating transaction is a *new, forward-moving transaction* that cancels the effect of a previous action, not a database rollback.
