---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Consistency Models Overview"]
tags: [distributed-systems, consistency]
---

# Strong Consistency (Linearizability)

## Intuition
**Guarantee:** Every read reflects the most recent completed write, system-wide. Every operation appears to take effect instantaneously. The system behaves exactly as if there were only one copy of the data.

## The Trade-off
To guarantee this, every operation typically needs to coordinate with a quorum or a single leader before responding. This adds latency and reduces availability during partitions (the 'C' side of CAP).

## Use Cases
- Bank balances
- Inventory counts where overselling is unacceptable
- Distributed locks
- Leader election
