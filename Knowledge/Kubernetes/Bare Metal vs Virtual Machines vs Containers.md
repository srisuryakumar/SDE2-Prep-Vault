---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 1 — The History That Explains Everything"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Namespaces and cgroups", "Container Orchestration Overview"]
tags: [infrastructure, docker, kubernetes, history]
---

# Bare Metal vs Virtual Machines vs Containers

## Intuition
To understand why containers and Kubernetes exist, you must understand the problems they solved.

## Era 1: Bare Metal (1990s - 2005)
- **Model:** One application per physical server. 
- **Problem:** Applications fought over ports and dependencies, so they had to be isolated physically. This led to terrible utilization (5-15%) and slow provisioning (weeks to order and rack a server).

## Era 2: Virtual Machines (2005 - 2013)
- **Model:** A hypervisor carves one physical server into many VMs, each with its own full Operating System (Guest OS) and kernel.
- **Problem Solved:** Better isolation on shared hardware. Utilization rose to 40-70%, and provisioning dropped to minutes.
- **New Problem:** You pay the overhead of a full OS for every single app (GBs of disk, hundreds of MBs of RAM, slow boot times). Config drift was also common.

## Era 3: Containers (2013 - present)
- **Model:** Multiple isolated user-spaces (containers) sharing a single host OS kernel.
- **Problem Solved:** Fast boot times (milliseconds) and low overhead (MBs instead of GBs) because there is no Guest OS to boot. Provides high density and eliminates config drift via immutable images.
