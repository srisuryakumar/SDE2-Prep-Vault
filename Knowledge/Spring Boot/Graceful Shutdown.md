---
type: concept
subject: Spring Boot and Backend Engineering
source_book: "Book 4 — Spring Boot and Backend Engineering"
source_chapter: "Chapter 7 — Documentation & Production"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [architecture, kubernetes, operations]
---

# Graceful Shutdown

## Intuition
When Kubernetes scales down or restarts a pod, it sends a `SIGTERM` signal. 
If the JVM shuts down immediately, any in-flight HTTP requests (and database transactions) are abruptly killed mid-response. 

## How to configure it
In `application.yml`:
```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

## The Sequence
When a `SIGTERM` arrives:
1. The web server (Tomcat) stops accepting *new* requests.
2. It waits for any currently executing requests to finish, up to the 30s timeout.
3. Once finished (or timed out), it closes the database connection pool, runs `@PreDestroy` methods, and exits cleanly.

## Integration with Kubernetes Probes
Spring Boot 2.3+ splits health into `/liveness` and `/readiness`.
When graceful shutdown begins, the readiness probe immediately returns `DOWN`. This tells the Kubernetes load balancer to stop routing new traffic to this pod, while the existing requests gracefully complete.
