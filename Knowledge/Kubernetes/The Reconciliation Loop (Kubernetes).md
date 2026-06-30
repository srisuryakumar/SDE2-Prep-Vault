---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Kubernetes Controller Manager"]
tags: [kubernetes, architecture, distributed-systems]
---

# The Reconciliation Loop (Kubernetes)

## Intuition
The single most important mental model in Kubernetes is the **reconciliation loop**. Every controller in the system follows this exact pattern continuously and indefinitely.

## The Pattern
1. **Desired State:** You declare what you want (e.g., "3 replicas of this image") via the API Server.
2. **Actual State:** The controller observes the real world (e.g., "2 replicas are currently running").
3. **Reconcile:** The controller compares desired vs actual. If they differ, it takes the smallest action needed to converge them (e.g., "create 1 pod").

A Deployment does not "deploy your app" once. It *continuously enforces* that the desired state exists, actively healing any deviation (crashes, node failures, or manual deletions) forever.
