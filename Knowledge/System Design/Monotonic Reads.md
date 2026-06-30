---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 3 — Consistency Models"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Read-Your-Writes Consistency"]
tags: [distributed-systems, consistency]
---

# Monotonic Reads

## Intuition
**Guarantee:** Once a client has seen a particular value, it will never subsequently see an *older* value on a later read. Time only moves forward for that client.

## Why it matters
Without it, a user refreshes a page and sees a new comment. They refresh again (hitting a more lagging replica) and the comment disappears. It looks like the system "forgot" data, but it's just replica lag.

## Common Fixes
- Sticky sessions: Consistently route a single client's reads to the same replica.
- Session tokens tracking the highest read version the client has seen.
