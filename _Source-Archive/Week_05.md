# Week 5: Advanced Java, Spring Boot Resiliency, and Graphs Start

## Day 29 — Spring AOP, Trees Continued, and Project Initialization

### DSA Block (2.5 hrs)
- Problem 1: Construct Binary Tree from Inorder and Postorder Traversal — LeetCode #106 — Pattern: Divide and Conquer
  - Hint: The last element in postorder is the root. Find it in inorder to split into left and right subtrees.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Flatten Binary Tree to Linked List — LeetCode #114 — Pattern: DFS/Preorder
  - Hint: Recursively flatten left and right. Attach the flattened left subtree to `root.right`, then attach the flattened right subtree to the end of the new right branch.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Advanced Java & Spring AOP
- Subtopics covered today: Aspect-Oriented Programming concepts (Aspect, Advice, Pointcut). Uses in Spring (Logging, Security, `@Transactional`). Java Reflection API basics.
- Coding exercise: Create a custom `@LogExecutionTime` annotation. Write an Aspect that measures and logs the execution time of any method annotated with it.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Initialize the new repository. Set up a Spring Boot project with Web, JPA, Validation, and PostgreSQL. Apply your `@LogExecutionTime` aspect to a dummy controller endpoint.
- Definition of done: The app starts, and curling the endpoint prints the execution time in the console via the AOP interceptor.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Begin daily checking of your application tracker. Apply to 2 more Tier C companies.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 4: Primitive Types).
- [ ] Complete the AOP Custom Annotation exercise.
- [ ] Initialize `order-management-api` and commit.
- [ ] Complete LeetCode #106 and #114.

---

## Day 30 — JVM Internals, Graph Fundamentals, and Controller Testing

### DSA Block (2.5 hrs)
- Problem 1: Number of Islands — LeetCode #200 — Pattern: Matrix DFS/BFS
  - Hint: Iterate through the grid. When you hit a '1', increment the island count and start a DFS/BFS to mark all connected '1's as '0' (visited).
  - Complexity: Time O(m×n) | Space O(m×n)
- Problem 2: Max Area of Island — LeetCode #695 — Pattern: Matrix DFS
  - Hint: Similar to #200, but the DFS function should return the count of nodes visited in the current island. Keep track of the max count.
  - Complexity: Time O(m×n) | Space O(m×n)

### Theory Block (2 hrs)
- Topic: JVM Internals & API Testing
- Subtopics covered today: Classloaders. Garbage Collection algorithms (G1GC vs ZGC). `@WebMvcTest` and `MockMvc` for testing Spring Controllers without starting the full server.
- Coding exercise: Write a script to launch a simple Java program with `-XX:+PrintGCDetails` to observe GC logs.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Create an `OrderController` with a POST endpoint. Write a test using `@WebMvcTest` and `MockMvc` to assert that it returns HTTP 201 Created for a valid payload, mocking the `OrderService`.
- Definition of done: Controller unit test runs instantly and passes without needing a database connection.

### Career Block (1 hr)
- LinkedIn: Post 9 — Order Management API Architecture (publish at 8 AM IST).
- Networking: First Tier C application practice starts today. Apply to 3 more target roles.
- **Day 30 Open Source Action:**
  Go to github.com/TheAlgorithms/Java. Search for issues labelled
  "good first issue". Pick one DSA algorithm you've already implemented
  (e.g., a Linked List operation, a sorting algorithm). Fork the repo,
  add your implementation following their contribution guidelines, and
  open a pull request. Even if it takes an extra 30 minutes, do it today.
  A merged PR on a 57K-star repository appears on your GitHub profile.
  This is the single highest-visibility action you can take with 30 minutes.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 5: Arrays).
- [ ] Complete the GC logging observation exercise.
- [ ] Complete Controller testing.
- [ ] Complete LeetCode #200 and #695.

---

## Day 31 — DP Start, Kubernetes Architecture, and Repository Testing

### DSA Block (2.5 hrs)
- Problem 1: Climbing Stairs — LeetCode #70 — Pattern: 1D Dynamic Programming
  - Hint: `dp[i] = dp[i-1] + dp[i-2]`. Note how this maps directly to the Fibonacci sequence. Optimize space to O(1) by only keeping the last two values.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Min Cost Climbing Stairs — LeetCode #746 — Pattern: 1D Dynamic Programming
  - Hint: `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`. You can start from index 0 or 1.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Kubernetes Architecture & Spring Data Testing
- Subtopics covered today: Control Plane (API Server, etcd, Scheduler, Controller Manager) vs Worker Nodes (Kubelet, Kube-proxy, Container Runtime). Intro to `@DataJpaTest`.
- Coding exercise: Sketch the Kubernetes architecture showing how a `kubectl run` command flows from the API Server to scheduling a pod on a worker node.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Define an `Order` entity and `OrderRepository`. Write tests using `@DataJpaTest` that use the embedded H2 database to verify custom query methods.
- Definition of done: The repository tests pass, verifying JPA mapping and queries without needing a real PostgreSQL instance.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Follow up on any recruiter responses from Week 3.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 6: Strings).
- [ ] Complete the K8s architecture sketch.
- [ ] Complete the `@DataJpaTest` implementation.
- [ ] Complete LeetCode #70 and #746.

---

## Day 32 — DP Grids, Resilience4j, and Spring Cloud Config

### DSA Block (2.5 hrs)
- Problem 1: Unique Paths — LeetCode #62 — Pattern: 2D Dynamic Programming
  - Hint: Create a 2D array. `dp[i][j] = dp[i-1][j] + dp[i][j-1]`. The first row and first column are all 1s.
  - Complexity: Time O(m×n) | Space O(m×n)
- Problem 2: Minimum Path Sum — LeetCode #64 — Pattern: 2D Dynamic Programming
  - Hint: `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`.
  - Complexity: Time O(m×n) | Space O(m×n)

### Theory Block (2 hrs)
- Topic: Microservices Resiliency
- Subtopics covered today: Cascading failures. Circuit Breaker Pattern. Rate Limiting. Spring Cloud Config basics for externalized configuration.
- Coding exercise: Create a standalone Spring Boot app that mimics a slow third-party API (Thread.sleep).

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Integrate `Resilience4j`. Add a `@CircuitBreaker` annotation to a service method that calls the dummy slow API from the coding exercise. Configure it to open after 3 failures.
- Definition of done: When the external API times out 3 times, the circuit breaker opens and immediately returns a fallback response for subsequent calls.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Apply to 2 more Tier C companies. 

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 7: Linked Lists).
- [ ] Complete the slow API coding exercise.
- [ ] Implement Circuit Breaker in `order-management-api`.
- [ ] Complete LeetCode #62 and #64.

---

## Day 33 — Advanced Graphs, Batch Processing, and Resilience Testing

### DSA Block (2.5 hrs)
- Problem 1: Clone Graph — LeetCode #133 — Pattern: Graph DFS + HashMap
  - Hint: Use a `HashMap<Node, Node>` to map original nodes to cloned nodes. If a node is already in the map, return the clone to handle cycles.
  - Complexity: Time O(V+E) | Space O(V)
- Problem 2: Course Schedule — LeetCode #207 — Pattern: Topological Sort / Graph Cycle Detection
  - Hint: Represent prerequisites as a directed graph. Use Kahn's Algorithm (in-degree array) or DFS with states (unvisited, visiting, visited) to detect cycles.
  - Complexity: Time O(V+E) | Space O(V+E)

### Theory Block (2 hrs)
- Topic: Spring Batch Basics + OAuth 2.0 Awareness
- Subtopics covered today:
  1. Spring Batch: ItemReader, ItemProcessor, ItemWriter. Chunk-oriented processing.
     Transaction management in batches. Write a simple Spring Batch job configuration
     that reads dummy strings, converts them to uppercase, and prints them.
  2. OAuth 2.0 Awareness (30 min — concept, not implementation):
     - OAuth 2.0 is an AUTHORIZATION FRAMEWORK, not an authentication protocol
     - JWT is a TOKEN FORMAT. OAuth 2.0 often uses JWTs as its tokens.
     - These are complementary, not competing.
     - Authorization Code Flow: user → your app → auth server (Google) → code → token exchange
     - Client Credentials Flow: service-to-service (no user), machine-to-machine auth
     - In your Order Management API: users authenticate with email/password → server
       issues a JWT. This is NOT OAuth 2.0. It's custom JWT issuance.
     - Adding "Login with Google": THAT requires OAuth 2.0. Spring Boot handles it
       with spring-boot-starter-oauth2-resource-server.
     - For the Scalable E-Commerce Platform: the API Gateway validates JWTs issued
       by an external OAuth 2.0 provider. Add to your architecture mental model.
     - Interview answer: "What's the difference between OAuth 2.0 and JWT?"
       → "OAuth 2.0 is a framework defining how apps request access to resources.
       JWT is a token format. OAuth 2.0 can issue JWTs. They're orthogonal."

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Write integration tests for your Resilience4j implementation. Assert that the `payFallback` method is invoked when the primary external call throws an exception.
- Definition of done: Tests prove the circuit breaker transitions correctly from CLOSED to OPEN states under failure conditions.
- Also: In your Resilience4j integration tests, add a comment explaining
  where OAuth 2.0 token validation would sit in the request pipeline
  (before the circuit breaker, at the Gateway filter level). This prepares
  you for the full implementation in Week 9.

### Career Block (1 hr)
- LinkedIn: Post 10 — @Transactional Deep Dive (publish at 6 PM IST).
- Networking: Update your networking CRM with response statuses.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 8: Stacks and Queues).
- [ ] Complete the Spring Batch exercise.
- [ ] Complete LeetCode #133 and #207.
- [ ] Committed to GitHub.

---

## Day 34 (Weekend) — Graph Traversals and Spring Core Review

### DSA Block (3.5 hrs)
- Problem 1: Word Ladder — LeetCode #127 — Pattern: BFS for Shortest Path
  - Hint: Shortest path in an unweighted graph is BFS. Generate all possible 1-letter mutations and check if they exist in the word set.
  - Complexity: Time O(m²×n) | Space O(m²×n)
- Problem 2: Pacific Atlantic Water Flow — LeetCode #417 — Pattern: Multi-source BFS/DFS
  - Hint: Instead of starting from every cell, start from the ocean borders and see which cells water can reach by traveling *uphill*.
  - Complexity: Time O(m×n) | Space O(m×n)

### Theory Block (1.5 hrs)
- Topic: Spring Core Deep Dive Review
- Subtopics covered today: Bean lifecycle. `@PostConstruct` and `@PreDestroy`. Scopes (Singleton vs Prototype). Proxies and the self-invocation issue.
- Coding exercise: Create a bean with prototype scope. Inject it into a singleton bean. Prove that the singleton always gets the same instance unless you use `ObjectFactory` or scoped proxies.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Refactor any self-invoking `@Transactional` methods (like the trap described in Post 10). Ensure transactional boundaries are correctly maintained via separate service beans.
- Definition of done: Architecture is clean; no internal method calls bypass Spring's CGLIB proxies.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Reach out to your Accountability Partner for a mock interview scheduling next week.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 9: Binary Trees).
- [ ] Complete the Spring Bean Scope exercise.
- [ ] Complete LeetCode #127 and #417.
- [ ] Committed to GitHub.

---

## Day 35 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode. 

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate DP and Graph algorithms.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post on Circuit Breakers.
  - Scan Hacker News.
  - Log findings in the study journal.
- **Weekly Scorecard:** Fill out the scorecard for Week 5. How did DP feel? 

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
