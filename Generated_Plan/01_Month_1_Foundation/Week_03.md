# Week 3: Spring Boot Foundations, Concurrency, and Trees

## Day 15 — Stacks, Generics, and API Initialization

### DSA Block (2.5 hrs)
- Problem 1: Valid Parentheses — LeetCode #20 — Pattern: Stack
  - Hint: Use a Stack to keep track of opening brackets. When encountering a closing bracket, check if it matches the top of the stack.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Min Stack — LeetCode #155 — Pattern: Two Stacks
  - Hint: Maintain a primary stack for values and a secondary stack that strictly tracks the minimum value seen so far.
  - Complexity: Time O(1) all ops | Space O(n)

### Theory Block (2 hrs)
- Topic: Java Generics & Spring Boot Basics
- Subtopics covered today: Generics (`<T>`, wildcards `? extends`, type erasure). HTTP Protocol (GET, POST, PUT, DELETE, Status Codes). REST API Design principles.
- Coding exercise: Write a generic `ResponseWrapper<T>` class that wraps any API payload along with a success flag and timestamp.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Initialize the Spring Boot project using Spring Initializr. Include Web, JPA, PostgreSQL, and Validation dependencies. Create a basic `/health` REST endpoint returning your generic `ResponseWrapper<String>`.
- Definition of done: Project compiles, server starts on port 8080, and `curl localhost:8080/health` returns a 200 OK JSON response.

### Additional Day 15 Task: Add Swagger/OpenAPI Documentation
- Add springdoc-openapi-starter-webmvc-ui to pom.xml:
  `org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0`
- Add @Tag(name = "Health") to the health controller class
- Add @Operation(summary = "Health check endpoint") to the health method
- Verify Swagger UI is accessible at http://localhost:8080/swagger-ui.html
- Definition of done: Opening the Swagger URL shows your health endpoint
  listed and callable from the browser. This will be the live URL you put
  in your README.

### Career Block (1 hr)
- LinkedIn: Post 5 — To-Do API Launch (publish at 8 AM IST).
- Networking: Comment on 3 posts from engineers at your target Tier B companies.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 26: Don't use raw types).
- [ ] Initialize `todo-api` and push the first commit.
- [ ] Complete LeetCode #20 and #155.

---

## Day 16 — HashMaps, Streams, and DTOs

### DSA Block (2.5 hrs)
- Problem 1: Contiguous Array — LeetCode #525 — Pattern: Prefix Sum with HashMap
  - Hint: Replace 0s with -1s. Keep a running sum. If the same running sum
  - Complexity: Time O(n) | Space O(n)
    appears twice, the subarray between those indices has equal 0s and 1s.
    This extends the prefix sum + HashMap pattern from a different angle than Day 5.
- Problem 2: Group Anagrams — LeetCode #49 — Pattern: HashMap Grouping
  - Hint: Sort the string characters to use as a canonical key in a
  - Complexity: Time O(n×k log k) | Space O(n×k)
    HashMap<String, List<String>>. All anagrams share the same sorted form.

### Theory Block (2 hrs)
- Topic: Functional Programming in Java
- Subtopics covered today: Lambdas, Functional Interfaces (`Predicate`, `Function`, `Consumer`), and the Stream API (`map`, `filter`, `collect`).
- Coding exercise: Given a list of integers, write a single Stream pipeline that filters out odd numbers, squares the remaining, and collects them into an unmodifiable list.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Create a `TaskController` and a `TaskDTO`. Implement dummy GET and POST endpoints (using an in-memory `ConcurrentHashMap` for now) that use Java Streams to map entities to DTOs.
- Definition of done: API accepts POST requests to create tasks and GET requests to list them, returning valid JSON mapped from DTOs.

### Career Block (1 hr)
- Networking: Send connection requests to 5 Senior Engineers at your target Tier A companies (e.g., Atlassian, Amazon).

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 42: Prefer lambdas to anonymous classes).
- [ ] Complete the Stream API coding exercise.
- [ ] Complete LeetCode #1 and #49.
- [ ] Committed to GitHub.

---

## Day 17 — Trees Start, Concurrency 101, and SQL Fundamentals

### DSA Block (2.5 hrs)
- Problem 1: Maximum Depth of Binary Tree — LeetCode #104 — Pattern: DFS
  - Hint: Base case: if node is null, return 0. Recursive case: `1 + Math.max(leftDepth, rightDepth)`.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Invert Binary Tree — LeetCode #226 — Pattern: Tree Traversal
  - Hint: Swap the left and right children, then recursively call invert on the left and right subtrees.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: Concurrency Start & SQL
- Subtopics covered today: Creating Threads (extending `Thread` vs implementing `Runnable`). Thread lifecycle. Relational DB concepts (Primary Keys, Foreign Keys, Normalization).
- Coding exercise: Write a simple program that spawns two threads, each printing numbers 1 to 5 with a 100ms sleep, to observe interleaved output.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Add Spring Data JPA. Define the `Task` entity with proper `@Entity`, `@Id`, and `@Column` annotations. Configure PostgreSQL connection properties in `application.yml`.
- Definition of done: Application connects to a local PostgreSQL instance and Hibernate auto-generates the `tasks` table (using `ddl-auto: update` for now).

### Additional Day 17 Task: Add Flyway Database Migrations to todo-api
- Add Flyway dependency to pom.xml: `org.flywaydb:flyway-core`
- Change spring.jpa.hibernate.ddl-auto from 'update' to 'validate'
  (Flyway now owns the schema, not Hibernate)
- Create src/main/resources/db/migration/V1__create_tasks_table.sql:
  ```sql
  CREATE TABLE tasks (
      id          BIGSERIAL PRIMARY KEY,
      title       VARCHAR(255) NOT NULL,
      description TEXT,
      status      VARCHAR(20)  DEFAULT 'PENDING',
      priority    VARCHAR(10)  DEFAULT 'MEDIUM',
      due_date    DATE,
      created_at  TIMESTAMP    DEFAULT NOW(),
      updated_at  TIMESTAMP    DEFAULT NOW()
  );
  ```
- Definition of done: Application starts without errors. Flyway creates the
  schema automatically. Check the flyway_schema_history table in PostgreSQL
  to confirm V1 ran successfully.
- Interview answer to prepare: "How do you handle schema changes without
  downtime?" → "We use Flyway. Every schema change is a versioned SQL script
  committed to Git alongside the application code. For zero-downtime: we add
  new columns as nullable first, deploy, backfill data, then add NOT NULL
  in a separate migration after the code handles both states."

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Review profiles of 3 engineering managers to personalize outreach tomorrow.

### Daily Deliverable
- [ ] Read *Java Concurrency in Practice* (Chapter 1: Introduction).
- [ ] Complete the thread interleaving exercise.
- [ ] Complete LeetCode #104 and #226.
- [ ] Committed to GitHub.

---

## Day 18 — Tree BFS, Synchronization, and Unit Testing

### DSA Block (2.5 hrs)
- Problem 1: Binary Tree Level Order Traversal — LeetCode #102 — Pattern: BFS
  - Hint: Use a Queue. Process nodes level by level by taking the `queue.size()` before starting the inner loop.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Binary Tree Right Side View — LeetCode #199 — Pattern: BFS
  - Hint: Similar to level order, but only add the last node of each level to the result array.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: Concurrency & Testing
- Subtopics covered today: Race conditions. The `synchronized` keyword (method vs block). The `volatile` keyword (visibility guarantee). Intro to JUnit 5 and AssertJ.
- Coding exercise: Write a counter class without synchronization. Write a test that increments it from 100 threads and fails. Then fix the class using `synchronized`.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Write JUnit 5 tests for your Spring components. Use `@DataJpaTest` to verify database operations and AssertJ for fluent assertions (e.g., `assertThat(task.getId()).isNotNull()`).
- Definition of done: Maven build passes with your new tests executing successfully against the embedded H2 test database.

### Career Block (1 hr)
- LinkedIn: Post 6 — DSA Pattern Visual (publish at 6 PM IST).
- Networking: Send connection requests to the 3 managers identified yesterday.

### Daily Deliverable
- [ ] Read *Java Concurrency in Practice* (Chapter 2: Thread Safety).
- [ ] Complete the synchronization coding exercise.
- [ ] Complete LeetCode #102 and #199.
- [ ] Committed to GitHub.

---

## Day 19 — Monotonic Stacks, SQL Joins, and Exception Handling

### DSA Block (2.5 hrs)
- Problem 1: Daily Temperatures — LeetCode #739 — Pattern: Monotonic Decreasing Stack
  - Hint: Store indices in the stack. If the current temperature is greater than the temperature at the index on top of the stack, pop and calculate the difference.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Next Greater Element I — LeetCode #496 — Pattern: Monotonic Stack + HashMap
  - Hint: Use a stack to find the next greater element for the base array, map it in a HashMap, then build the result for the query array.
  - Complexity: Time O(n+m) | Space O(n)

### Theory Block (2 hrs)
- Topic: Advanced SQL & API Exception Handling
- Subtopics covered today: INNER, LEFT, RIGHT, and FULL OUTER joins. Database Indexes (B-tree). `@RestControllerAdvice` and `@ExceptionHandler` in Spring.
- Coding exercise: Write an SQL query joining a `users` and `orders` table to find users who have never placed an order.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Implement a `@RestControllerAdvice` class. Map specific exceptions (e.g., `EntityNotFoundException`) to a structured JSON error response with HTTP 404.
- Definition of done: Querying a non-existent task ID returns a clean, standardized JSON error instead of a stack trace.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Follow up on unanswered messages from Week 2.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 73: Throw exceptions appropriate to the abstraction).
- [ ] Complete the SQL Join coding exercise.
- [ ] Complete LeetCode #739 and #496.
- [ ] Committed to GitHub.

---

## Day 20 (Weekend) — Validating BSTs and Redis Basics

### DSA Block (3.5 hrs)
- Problem 1: Validate Binary Search Tree — LeetCode #98 — Pattern: DFS with boundaries
  - Hint: Pass `min` and `max` limits down the recursive calls. The left child must be `< root.val`, right child `> root.val`.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Lowest Common Ancestor of a BST — LeetCode #235 — Pattern: BST Traversal
  - Hint: If both `p` and `q` are less than root, LCA is in the left subtree. If both are greater, it's in the right. Otherwise, root is the LCA.
  - Complexity: Time O(n) | Space O(n)
- Problem 3: Construct Binary Tree from Preorder and Inorder Traversal — LeetCode #105 — Pattern: Divide and Conquer
  - Hint: The first element in preorder is the root. Find it in inorder to split the left and right subtrees.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (1.5 hrs)
- Topic: Distributed Caching with Redis
- Subtopics covered today: In-memory datastores vs RDBMS. Redis data structures (Strings, Hashes). The Cache-Aside pattern.
- Coding exercise: Connect to a local Redis instance via CLI. Set a key, read it, and set an expiration (TTL).

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Integrate Spring Boot Data Redis. Add `@Cacheable` to your Task retrieval endpoint and `@CacheEvict` on task updates to implement the Cache-Aside pattern.
- Definition of done: Fetching a task twice logs a DB query the first time, but not the second time, proving Redis is serving the cached response.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Reach out to a peer for a casual virtual coffee chat.

### Daily Deliverable
- [ ] Read *Java Concurrency in Practice* (Chapter 3: Sharing Objects).
- [ ] Complete the Redis CLI exercise.
- [ ] Complete LeetCode #98, #235, and #105.
- [ ] Committed to GitHub.

---

## Day 21 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Brain recovery day.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an architecture post (e.g., Discord's migration from Cassandra to ScyllaDB).
  - Scan Hacker News.
  - Log findings in the study journal.
- **Weekly Scorecard:** Fill out the scorecard for Week 3. Reflect on your test coverage and database understanding.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
