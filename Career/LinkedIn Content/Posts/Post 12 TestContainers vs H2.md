---
type: linkedin-post
post_number: 12
scheduled_week: 6
scheduled_day: Friday
status: drafted
---
I switched from H2 to TestContainers mid-project. Here's what changed.

With H2 (in-memory DB):
- Tests ran in 8 seconds
- Missed: PostgreSQL-specific syntax (array columns, JSONB queries)
- Missed: Flyway migration failures on real PostgreSQL types
- Missed: HikariCP connection pool exhaustion under load

With TestContainers (real PostgreSQL in Docker):
- Tests run in 23 seconds
- Caught: 3 bugs that H2 silently ignored
- Caught: a race condition in the seat booking endpoint
- Now: I can confidently say "tests pass against production database"

The 15-second trade-off is worth it every time.

Setup is surprisingly simple:
@Testcontainers
class OrderServiceTest {
    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:16-alpine");

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry r) {
        r.add("spring.datasource.url", postgres::getJdbcUrl);
    }
}

#SpringBoot #Testing #BackendEngineering
