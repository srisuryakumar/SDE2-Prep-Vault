---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 7 — Distributed Transactions"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["The Saga Pattern"]
tags: [distributed-systems, transactions]
---

# Two-Phase Commit (2PC)

## Intuition
2PC coordinates a true atomic commit across multiple participants (services/databases) using a central **coordinator**.

## How it works
- **Phase 1 (Prepare):** The coordinator asks all participants, "Can you commit?". Each participant locks its resources, writes the change to a durable log (but doesn't make it visible), and replies YES or NO.
- **Phase 2 (Commit/Abort):** If ALL replied YES, the coordinator broadcasts "COMMIT". If ANY replied NO, the coordinator broadcasts "ABORT".

## The Fatal Weakness: Blocking
If the coordinator crashes *after* collecting all YES votes but *before* sending the final COMMIT, every participant is stuck. They hold locks on their resources but cannot unilaterally commit or abort. This freezes the entire transaction indefinitely until the coordinator recovers. 

Because it ties the availability of all services together at the moment of commit, 2PC is rarely used across modern microservices.
