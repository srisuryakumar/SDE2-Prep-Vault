---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kafka Architecture Overview"]
tags: [kafka, messaging, architecture, distributed-systems]
---

# Why Kafka Exists (Decoupling)

## Intuition
If Service A tells Service B to do something via a direct HTTP call, they are **tightly coupled**. If Service B is down, slow, or unreachable, Service A's operation fails. 

With Kafka between them, Service A publishes an event to a Kafka topic and moves on. It never blocks on Service B being available. If Service B is down for a deployment, the message simply sits in Kafka until B comes back online and consumes it. Service A never even knows there was an outage.

## Beyond Simple Decoupling
Kafka adds two more properties:
1. **Persistence:** Messages are written to disk, so a consumer down for hours can catch up later.
2. **Replay:** A new consumer can re-read the *entire* history of a topic from the beginning, not just see what happens from "now" forward.
