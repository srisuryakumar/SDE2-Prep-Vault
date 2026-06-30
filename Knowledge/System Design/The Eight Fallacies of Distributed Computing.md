---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 1 — The machine you already understand"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [distributed-systems, fallacies]
---

# The Eight Fallacies of Distributed Computing

## Intuition
Catalogued by Sun Microsystems engineers in the 1990s, these are the false assumptions newcomers make about distributed systems. Designing a system believing any of these are true will lead to failure.

## The Fallacies
1. **The network is reliable:** It isn't. Packets drop, switches fail.
2. **Latency is zero:** It isn't. Network round-trips take milliseconds and are highly variable.
3. **Bandwidth is infinite:** It isn't. Large payloads congest the network.
4. **The network is secure:** It isn't. You must encrypt and authenticate.
5. **Topology doesn't change:** It does. Nodes are added, removed, and IPs change constantly.
6. **There is one administrator:** There isn't. You depend on DNS, ISPs, and cloud providers you don't control.
7. **Transport cost is zero:** It isn't. Serialization and connection setup cost CPU and time.
8. **The network is homogeneous:** It isn't. Different links and hardware behave differently under load.
