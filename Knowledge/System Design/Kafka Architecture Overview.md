---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kafka Producers (Partition Selection)"]
tags: [kafka, messaging, architecture]
---

# Kafka Architecture Overview

## Intuition
Kafka is a distributed event streaming platform.

## Core Vocabulary
- **Broker:** A single Kafka server. A cluster is typically 3+ brokers.
- **Topic:** A named stream of messages (e.g., `order-events`). It is logically one stream, but physically split into partitions.
- **Partition:** An ordered, immutable, append-only log of messages. It is the unit of parallelism and ordering in Kafka. Each partition has a leader broker and replica brokers.
- **Offset:** A message's position within its partition (an ever-increasing integer). Offsets are only unique *within a partition*.
- **Consumer Group:** A set of consumers that share the work of reading a topic. Kafka guarantees each partition is read by **exactly one consumer within a given group** at a time.
- **ZooKeeper / KRaft:** The system that tracks cluster metadata and runs leader election. KRaft is Kafka's built-in consensus protocol that replaces ZooKeeper in modern deployments.

## The Partition Trade-off
Kafka only guarantees message order *within a single partition*, not across an entire topic. A totally ordered topic could only be processed by one consumer at a time (no parallelism). Partitions allow multiple consumers to work in parallel, at the cost of only guaranteeing order per-partition.
