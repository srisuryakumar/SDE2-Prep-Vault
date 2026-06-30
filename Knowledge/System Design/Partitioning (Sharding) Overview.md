---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 5 — Partitioning and Sharding"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Hash Partitioning vs Range Partitioning", "Database Replication (Why replicate)"]
tags: [database, distributed-systems, sharding]
---

# Partitioning (Sharding) Overview

## Intuition
Replication copies the *entire* dataset to every node, solving fault tolerance and read scaling. But what if the dataset is bigger than any single node's disk? 
**Partitioning (sharding)** solves this by breaking the dataset into smaller subsets. Each node only holds a subset of the data. 

## Combining Partitioning and Replication
In practice, you use both. The data is partitioned across multiple nodes (to handle total data size and write scaling), and each partition is replicated (for fault tolerance and read scaling).
