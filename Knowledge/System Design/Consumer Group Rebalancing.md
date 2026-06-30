---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: ["Kafka Architecture Overview"]
tags: [kafka, operations]
---

# Consumer Group Rebalancing

## Intuition
When a consumer joins or leaves a group (due to a deploy, crash, or scale-up), Kafka must reassign partitions among the remaining/new consumers. This is a rebalance.

## Eager Rebalancing (Legacy Default)
*All* consumers in the group stop consuming, every partition is revoked, and then partitions are reassigned from scratch. This creates a "stop-the-world" pause for the entire group, even for consumers whose assignments won't change.

## Cooperative Rebalancing
Supported in modern Kafka (2.4+). Only the partitions that actually *need* to move are revoked and reassigned. Consumers keep processing their unaffected partitions throughout the rebalance. This dramatically reduces disruption during routine scaling and deploys.
