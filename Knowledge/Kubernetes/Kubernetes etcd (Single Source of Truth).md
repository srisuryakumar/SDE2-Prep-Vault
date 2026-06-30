---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kubernetes API Server"]
tags: [kubernetes, architecture, state, etcd]
---

# Kubernetes etcd (Single Source of Truth)

## Intuition
`etcd` is a distributed key-value store. It is the **single source of truth** for the entire cluster's state (Deployments, Pods, Services, Secrets). The API Server is its only client.

## Raft Consensus
`etcd` uses the Raft consensus algorithm to keep multiple nodes in agreement. It requires a strict **majority (quorum)** to commit writes.
- You must run `etcd` in clusters of **3 or 5 nodes**, never an even number. A 4-node cluster still only tolerates 1 failure (needs 3 for quorum), providing no extra reliability over a 3-node cluster while adding overhead.

## Backups are Critical
Losing `etcd` without a backup means losing the entire cluster's state. Running containers might survive temporarily, but nothing can be updated, healed, or rescheduled.
