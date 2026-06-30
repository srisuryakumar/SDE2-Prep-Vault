---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 8 — AWS Fundamentals"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [aws, compute, security]
---

# AWS EC2 and Security Groups

## Intuition
EC2 provides on-demand Virtual Machines (instances) with various families (compute-optimized, memory-optimized, etc.) tailored to workload needs.

## Security Groups
A Security Group acts as a **stateful, instance-level virtual firewall**.
- It uses allow rules only (anything not explicitly allowed is denied).
- "Stateful" means that if an inbound request is allowed, the response is automatically allowed back out, without requiring a matching outbound rule.
