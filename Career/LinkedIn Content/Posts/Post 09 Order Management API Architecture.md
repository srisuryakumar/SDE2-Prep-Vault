---
type: linkedin-post
post_number: 9
scheduled_week: 5
scheduled_day: Tuesday
status: drafted
---
Just pushed the Order Management API to GitHub.

GitHub: [link] | Swagger: [link]

Architecture in one diagram: [ATTACH]

What's inside:
→ JWT authentication via Spring Security filter chain
→ Redis cache (Cache-Aside pattern, 15-min TTL)
→ Kafka events (OrderCreated, OrderUpdated) with Dead Letter Queue
→ Resilience4j circuit breaker on every external service call
→ TestContainers: tests run against real PostgreSQL, Redis, and Kafka
→ Flyway migrations versioning every schema change
→ GitHub Actions CI/CD pipeline: test → Docker build → GHCR push

The biggest learning: testing with TestContainers caught 3 bugs
that H2 never would have. Real PostgreSQL, real constraints.

#SpringBoot #Java #BackendEngineering #DistributedSystems
