---
type: linkedin-post
post_number: 5
scheduled_week: 3
scheduled_day: Tuesday
status: drafted
---
My first Spring Boot API is live.

GitHub: [link] | Live Swagger UI: [link]

What it does:
- CRUD task management with JWT authentication
- PostgreSQL backend with Flyway migrations
- 80%+ test coverage with JUnit 5 and TestContainers

3 things I learned building it:

1. The N+1 problem — fetching 10 tasks ran 11 queries. Fixed with JOIN FETCH.
2. Flyway migrations — versioned SQL scripts mean no more "works on my machine"
3. TestContainers > H2 — tests now run against real PostgreSQL, catching real bugs

The live Swagger UI link means anyone can try the API without reading code.
That feels like the right way to build a portfolio.

Next: Order Management API with Kafka, Redis, and circuit breakers.

#SpringBoot #Java #BackendEngineering
