---
type: concept
subject: System Design
source_book: "Book 5 — Distributed Systems and Messaging"
source_chapter: "Chapter 1 — The machine you already understand"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["The Eight Fallacies of Distributed Computing"]
tags: [distributed-systems, scaling]
---

# Why a single machine isn't enough

## Intuition
A single machine has a simple mental model: **everything either happens or it doesn't, and you always know which**. A method call either returns or throws. 

However, you must eventually scale horizontally (adding more machines) instead of vertically (buying a bigger machine) because:
1. **Hardware ceiling:** CPU and memory have physical limits and exponential costs at the high end.
2. **Single point of failure:** If the machine dies, the entire system is down.
3. **Geographic latency:** Users far from the data center experience high latency due to the speed of light.

## The Cost of Horizontal Scaling
By scaling horizontally, you fix those problems but introduce a new category of problems: **Partial Failure** and **Ambiguity**.
If Service A calls Service B over a network and doesn't get a response, Service A cannot tell if:
- Service B never received the request.
- Service B processed the request but the response was lost in the network.
- Service B is just slow.

This ambiguity requires idempotency, retries, and consensus protocols.
