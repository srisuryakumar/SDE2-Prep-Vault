---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 7 — Distributed Transactions"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Two-Phase Commit (2PC)", "The Saga Pattern"]
tags: [distributed-systems, transactions, architecture]
---

# Distributed Transactions Overview

## Intuition
On a single machine, a database transaction ensures that multiple writes either all commit together, or none do (Atomicity). 
In a microservices architecture, a single business action (e.g., placing an order) might span three different services (Order, Payment, Inventory) with three different databases. There is no single database to wrap a transaction around. If Payment succeeds but Inventory fails, you are left with an inconsistent system (customer charged, but no item reserved).

## Solutions
To keep data consistent across multiple services without a shared database, you must use a distributed transaction protocol. The two main approaches are:
1. **Two-Phase Commit (2PC):** The classical, strict, but blocking approach.
2. **The Saga Pattern:** The modern, eventually consistent approach based on compensating transactions.
