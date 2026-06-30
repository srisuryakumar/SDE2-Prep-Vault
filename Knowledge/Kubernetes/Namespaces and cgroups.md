---
type: concept
subject: Kubernetes
source_book: "Book 6 — Docker Kubernetes and Cloud Infrastructure"
source_chapter: "Chapter 1 — The History That Explains Everything"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Bare Metal vs Virtual Machines vs Containers"]
tags: [docker, linux, containers]
---

# Namespaces and cgroups

## Intuition
A container is not a virtual machine. It does not virtualize hardware and does not boot its own kernel. Instead, a container is just a normal Linux process that has been isolated using two core kernel features:

## 1. Namespaces (What a process can see)
Namespaces isolate the environment the process perceives.
- **PID:** It thinks it's PID 1, completely isolated from other processes on the host.
- **NET:** It gets its own network stack and IP address.
- **MNT:** It gets its own filesystem mount points.
- **UTS:** It gets its own hostname.

## 2. cgroups / Control Groups (What a process can use)
cgroups place hard limits on resource consumption (CPU, memory, disk I/O, network bandwidth) so that a runaway process inside one container cannot starve its neighbors on the same host.
