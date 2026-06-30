---
type: linkedin-post
post_number: 28
scheduled_week: 14
scheduled_day: Friday
status: drafted
---
The flagship project is complete.

scalable-ecommerce-platform: [GitHub link]

Architecture:
→ 4 microservices: Product, Order, Payment, Notification
→ Spring Cloud Gateway as API Gateway with JWT validation
→ Kafka with Schema Registry (Avro) for all inter-service events
→ Resilience4j circuit breakers on every external call
→ PostgreSQL (separate database per service) + Flyway migrations
→ Redis for distributed caching and rate limiting
→ Kubernetes: HPA, PodDisruptionBudget, NetworkPolicies, RBAC
→ Prometheus + Grafana dashboards for all 4 services
→ GitHub Actions: test → build → push → Helm upgrade on every merge

Load test results (k6, 1000 concurrent users):
→ P99 latency: 287ms
→ Error rate: 0.02%
→ Throughput: 4,200 requests/second

This is the project I'll walk through in every system design interview.
120 days of preparation visible in 6 repositories.

#BackendEngineering #Kubernetes #DistributedSystems
