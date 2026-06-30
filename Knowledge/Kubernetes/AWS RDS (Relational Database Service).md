---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 8 — AWS Fundamentals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [aws, databases, high-availability]
---

# AWS RDS (Relational Database Service)

## Intuition
RDS provides managed databases (PostgreSQL, MySQL, etc.) where AWS handles patching, backups, and failover.

## Multi-AZ vs Read Replicas
These two features solve entirely different problems and are often used together:
- **Multi-AZ:** Solves **availability**. A synchronously-replicated standby is maintained in a *different* Availability Zone. If the primary fails, RDS automatically fails over and repoints the DNS. The standby is *not directly queryable*; it exists solely for failover.
- **Read Replicas:** Solves **read scaling**. Separate, asynchronously-replicated instances that *are* directly queryable. You use them to offload read-heavy traffic (analytics, reporting) from the primary. Because replication is async, they can lag slightly behind the primary.
