---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 5 — How Different Types of Software Work"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations, daemons, background]
---

# Background Services and Daemons

A daemon is a background process that starts automatically, runs continuously, has no UI, and provides services (e.g., `sshd`, `nginx`, `postgresql`). 

## systemd
`systemd` is the init system on modern Linux. It starts and monitors all daemons. You interact with it using `systemctl` to start, stop, and enable services to run at boot. (In Kubernetes, the kubelet serves a similar role for pods).

## Scheduled Jobs
- **Cron:** A Unix daemon that runs commands on a schedule (e.g., `30 2 * * * backup.sh`).
- **Spring `@Scheduled`:** Runs a method on a schedule within the JVM. *Crucial limitation:* If you deploy 3 instances of your Spring Boot app, the scheduled task will fire 3 times simultaneously. Use distributed locks (like ShedLock) or a dedicated scheduler (Quartz) for clustered environments.

## Kafka Consumers as Daemons
A Kafka consumer is a long-running daemon thread. It enters an infinite `while(running)` loop, polling the broker for new messages, processing them, and committing offsets, until the application receives a shutdown signal (SIGTERM).
