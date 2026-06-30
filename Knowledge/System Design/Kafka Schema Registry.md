---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 6 — Apache Kafka"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [kafka, architecture, data-contracts]
---

# Kafka Schema Registry

## Intuition
Without a schema registry, if a producer adds a new field or renames a field in a JSON message, all downstream consumers might silently break or throw deserialization exceptions in production. 

## How it works
The Schema Registry (typically using Avro or Protobuf) stores a versioned schema for each topic and enforces a **compatibility mode** on every new schema version a producer tries to register.

## Compatibility Modes
- **Backward:** A new schema can read data written with the *previous* schema. Use when consumers upgrade before producers. (e.g. Reject a field rename).
- **Forward:** An old schema can read data written with the *new* schema. Use when producers upgrade before consumers.
- **Full:** Both backward and forward compatible.

By enforcing this at registration (build/deploy time), bad schema changes are caught before they ever hit production.
