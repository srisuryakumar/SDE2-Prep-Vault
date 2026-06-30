---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 3 — Kubernetes Architecture"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["kubelet (Node Agent)"]
tags: [kubernetes, architecture, networking]
---

# kube-proxy

## Intuition
`kube-proxy` runs on every node and is responsible for making Kubernetes **Services** work at the network level. 

## How it works
A Service has a stable virtual IP, but that IP isn't attached to any real physical network interface. 
`kube-proxy` watches the API Server for Services and their backing Pod endpoints. It then programs `iptables` (or IPVS) rules on the node so that traffic destined for the Service's virtual IP gets transparently load-balanced across the actual, healthy Pod IP addresses.
