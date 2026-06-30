---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Eventual Consistency", "Monotonic Reads"]
tags: [distributed-systems, consistency]
---

# Read-Your-Writes Consistency

## Intuition
**Guarantee:** A specific guarantee on top of eventual consistency. After a client writes a value, *that same client* will always see their own write on subsequent reads, even if other clients might still see stale data.

## Why it matters
Without it, a user updates their shipping address, hits "save", and is immediately redirected to "review order". If that read hits a lagging replica, they see the *old* address and assume the save failed.

## Common Fixes
- Route a user's reads to the leader (or the replica that handled their write) for a short window after they write.
- Pass a "write version" token from the client; the server refuses to answer until the replica catches up to that version.
