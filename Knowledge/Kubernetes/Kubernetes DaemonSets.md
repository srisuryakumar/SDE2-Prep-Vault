---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 4 — Kubernetes Objects"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Kubernetes Deployments and ReplicaSets", "Kubernetes StatefulSets"]
tags: [kubernetes, architecture, nodes]
---

# Kubernetes DaemonSets

## Intuition
A **DaemonSet** guarantees that exactly *one* copy of a pod runs on every node in the cluster (or every node matching a selector). 

## Behavior
If a new node joins the cluster, the DaemonSet automatically spins up a pod on it. If a node is removed, the pod is garbage collected.

## Use Cases
It is used when "one per node" is the strict requirement:
- Log collection agents (Fluentd, Filebeat) tailing logs from the node's filesystem.
- Monitoring agents (node-exporter, Datadog agent) collecting hardware metrics.
- CNI network plugins, which must run on every node to provide networking.
