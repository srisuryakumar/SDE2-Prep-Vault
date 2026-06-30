---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Strong Consistency (Linearizability)", "Eventual Consistency", "Read-Your-Writes Consistency"]
tags: [distributed-systems, consistency]
---

# Consistency Models Overview

## Intuition
A consistency model dictates what you can expect when reading data that was recently written in a distributed system. 
If a user updates their profile and reloads the page, do they see the new data immediately, or might they see the old data? The consistency model determines whether seeing the old data is a "bug" or expected behavior.

## The Spectrum
Models exist on a spectrum from strong to weak:
- **Stronger models:** Easier to reason about (behaves like a single machine), but expensive to provide, higher latency, and less available during partitions.
- **Weaker models:** Cheaper, faster, and scale well horizontally, but push complexity into the application code to handle stale or conflicting data.
