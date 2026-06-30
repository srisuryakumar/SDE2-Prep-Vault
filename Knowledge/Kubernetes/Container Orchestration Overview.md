---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 1 — The History That Explains Everything"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Bare Metal vs Virtual Machines vs Containers"]
tags: [kubernetes, orchestration, architecture]
---

# Container Orchestration Overview

## Intuition
Docker solves density, startup speed, and config drift for a *single* container on a *single* host. But production systems often involve hundreds of containers spread across dozens of servers. Managing this manually is impossible.

## The 5 Problems Orchestration Solves
A container orchestrator (like Kubernetes) exists to answer these questions automatically at fleet-scale:
1. **Scheduling:** When a new container needs to start, which of the 50 servers has enough CPU/RAM to run it?
2. **Self-healing:** If a container crashes, or a whole server dies at 3 AM, who notices and restarts replacements elsewhere?
3. **Scaling:** How do we automatically add instances when traffic triples, and remove them when it drops?
4. **Service Discovery:** How does Container A find Container B when B's IP address changes every time it restarts?
5. **Rolling Updates:** How do we deploy a new version to 30 instances without taking the API down, and safely rollback if needed?
