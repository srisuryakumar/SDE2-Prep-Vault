# Week 7: Advanced DP, NoSQL, and Kafka Streams

## Day 43 — DP Strings, NoSQL Data Modeling, and WireMock

### DSA Block (2.5 hrs)
- Problem 1: Longest Common Subsequence — LeetCode #1143 — Pattern: 2D String DP
  - Hint: `dp[i][j]` represents the LCS of `s1[0..i]` and `s2[0..j]`. If chars match: `1 + dp[i-1][j-1]`. If not: `max(dp[i-1][j], dp[i][j-1])`.
  - Complexity: Time O(m×n) | Space O(m×n)
- Problem 2: Edit Distance — LeetCode #72 — Pattern: 2D String DP
  - Hint: Similar grid to LCS. If chars match, `dp[i][j] = dp[i-1][j-1]`. If they don't match, take the minimum of insert, delete, or replace operations + 1.
  - Complexity: Time O(m×n) | Space O(m×n)

### Theory Block (2 hrs)
- Topic: NoSQL Data Modeling & API Mocking
- Subtopics covered today: Cassandra architecture (SSTables, LSM-Trees). Wide-column vs Document stores. Denormalization is mandatory in Cassandra. Intro to WireMock for testing.
- Coding exercise: Write a dummy test class using WireMock to stub an HTTP response for `http://localhost:8089/payment` returning a 200 OK with JSON data.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Integrate WireMock into your integration tests. Test the Resilience4j Circuit Breaker by configuring WireMock to return HTTP 500s or timeouts, proving the fallback logic is triggered.
- Definition of done: Integration tests pass cleanly, simulating external API failures realistically via WireMock.

### Career Block (1 hr)
- LinkedIn: Post 13 — Rate Limiter Algorithm Comparison (publish at 8 AM IST).
- Networking: Begin researching System Design architectures of target Tier A companies (e.g., Uber surge pricing).

### Daily Deliverable
- [ ] Read *DDIA* (Chapter 3: Storage and Retrieval).
- [ ] Complete the WireMock stubbing exercise.
- [ ] Implement WireMock in `order-management-api` tests.
- [ ] Complete LeetCode #1143 and #72.

---

## Day 44 — Substring DP, Replication, and REST-assured

### DSA Block (2.5 hrs)
- Problem 1: Palindromic Substrings — LeetCode #647 — Pattern: Expand Around Center
  - Hint: Treat every character (and every space between characters) as a potential center of a palindrome and expand outwards.
  - Complexity: Time O(n²) | Space O(1)
- Problem 2: Longest Palindromic Substring — LeetCode #5 — Pattern: Expand Around Center
  - Hint: Same approach as #647, but keep track of the maximum length and the start index.
  - Complexity: Time O(n²) | Space O(1)

### Theory Block (2 hrs)
- Topic: Distributed Systems (Replication)
- Subtopics covered today: Single-leader, Multi-leader, and Leaderless replication. Synchronous vs Asynchronous replication. Replication lag issues (Reading your own writes).
- Coding exercise: Write an automated API test using REST-assured that makes a POST request to create an order, extracts the ID, and makes a GET request to verify it exists.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Add REST-assured dependencies. Write a full end-to-end integration test (using `@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)`) that runs the full API lifecycle against TestContainers.
- Definition of done: `mvn verify` runs the E2E REST-assured tests successfully against the Dockerized database and Kafka instances.

### Career Block (1 hr)
- Technical Blog: Write and publish Blog Post 2 (Topic: "Why Cassandra Requires Denormalization" or "Building Resilient Systems with Resilience4j").
- LinkedIn: Share your blog post.

### Daily Deliverable
- [ ] Read *DDIA* (Chapter 4: Encoding and Evolution).
- [ ] Complete the REST-assured exercise.
- [ ] Complete E2E tests in `order-management-api`.
- [ ] Complete LeetCode #647 and #5.

---

## Day 45 — DP on Matrices, Distributed Transactions, and Kafka Streams

### DSA Block (2.5 hrs)
- Problem 1: Maximal Square — LeetCode #221 — Pattern: 2D Matrix DP
  - Hint: `dp[i][j]` represents the side length of the maximum square whose bottom right corner is the cell `(i, j)`. It equals `min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`.
  - Complexity: Time O(m×n) | Space O(m×n)
- Problem 2: Interleaving String — LeetCode #97 — Pattern: 2D String DP
  - Hint: `dp[i][j]` is true if `s1[0..i]` and `s2[0..j]` can interleave to form `s3[0..i+j]`.
  - Complexity: Time O(m×n) | Space O(m×n)

### Theory Block (2 hrs)
- Topic: Distributed Transactions & Kafka Streams
- Subtopics covered today: Two-Phase Commit (2PC). Why 2PC fails at scale. The Saga Pattern (Choreography vs Orchestration). Kafka Streams basics (KStream, KTable).
- Coding exercise: Write a basic KStream topology that reads from a `raw-events` topic, maps the values to uppercase, and writes to an `uppercase-events` topic.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Set up a basic Saga choreography flow. When an Order is created, emit `OrderCreatedEvent`. Create a dummy `PaymentService` listener that listens to this, and if payment succeeds, emits `PaymentSucceededEvent`. The Order service listens to that and updates the status to COMPLETED.
- Definition of done: The distributed transaction is completed asynchronously via Kafka events.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: **Day 45 Milestone.** Shift focus to Tier B companies (Strong Targets). Apply to 3 Tier B roles.

### Daily Deliverable
- [ ] Read *DDIA* (Chapter 5: Replication).
- [ ] Complete the KStream topology exercise.
- [ ] Implement Saga Choreography steps.
- [ ] Complete LeetCode #221 and #97.

---

## Day 46 — DP Word Break, Kubernetes Pods, and K8s Config

### DSA Block (2.5 hrs)
- Problem 1: Word Break — LeetCode #139 — Pattern: 1D DP + Set
  - Hint: `dp[i]` is true if `s[0..i]` can be segmented. For every `j < i`, if `dp[j]` is true and `s[j..i]` is in the dictionary, `dp[i]` is true.
  - Complexity: Time O(n²) | Space O(n)
- Problem 2: Decode Ways — LeetCode #91 — Pattern: 1D DP
  - Hint: Similar to Fibonacci. `dp[i] = dp[i-1]` (if single digit valid) `+ dp[i-2]` (if two digit valid).
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Kubernetes Resources Deep Dive
- Subtopics covered today: Pods vs Deployments. ReplicaSets. Liveness and Readiness Probes. Why you must use Readiness Probes for zero-downtime deployments.
- Coding exercise: Write a basic Kubernetes `deployment.yaml` and `service.yaml` for an Nginx container. Include resource limits and requests.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Write the Kubernetes manifests (`deployment.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`) for `order-management-api`.
- Definition of done: The manifest files are valid and pushed to a `k8s/` folder in the repository.

### Career Block (1 hr)
- LinkedIn: Post 14 — Resilience4j Circuit Breaker (publish at 6 PM IST).
- Networking: Follow up on applications sent on Day 45.

### Daily Deliverable
- [ ] Read *DDIA* (Chapter 6: Partitioning).
- [ ] Complete the K8s YAML exercise.
- [ ] Push K8s manifests for `order-management-api`.
- [ ] Complete LeetCode #139 and #91.

---

## Day 47 — Advanced Graph Traversals, Mongo vs Cassandra, and Minikube

### DSA Block (2.5 hrs)
- Problem 1: Minimum Height Trees — LeetCode #310 — Pattern: Topological Sort (Peeling the Onion)
  - Hint: Start with all leaf nodes (degree == 1). Remove them and update degrees. Repeat until 1 or 2 nodes are left. These are the roots of MHTs.
  - Complexity: Time O(V+E) | Space O(V+E)
- Problem 2: Evaluate Division — LeetCode #399 — Pattern: Graph DFS / Floyd-Warshall
  - Hint: Build a directed weighted graph where edge `A -> B` has weight `val` and `B -> A` has weight `1/val`. Perform DFS to find the path product.
  - Complexity: Time O((V+E)×Q) | Space O(V+E)

### Theory Block (2 hrs)
- Topic: DB Internals & Local K8s
- Subtopics covered today: MongoDB (Document store, BSON, Replica Sets) vs Cassandra (Wide-column, Peer-to-peer). Local Kubernetes clusters (Minikube / kind).
- Coding exercise: Start a Minikube cluster locally. Apply the Nginx deployment from yesterday and use `kubectl port-forward` to access it.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Apply your `order-management-api` K8s manifests to your local Minikube cluster. You will need to build the Docker image into the Minikube registry first.
- Definition of done: The API is running inside Minikube, and you can curl its health endpoint via port-forward.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Send connection requests to 3 SDE-2s at Tier A targets (Uber, Stripe).

### Daily Deliverable
- [ ] Read *Database Internals* (Chapter 1: Storage Engines).
- [ ] Complete the Minikube setup and Nginx deployment.
- [ ] Run `order-management-api` on Minikube.
- [ ] Complete LeetCode #310 and #399.

---

## Day 48 (Weekend) — Graph Cycle Detection, DP Review, and CI Enforcements

### DSA Block (3.5 hrs)
- Problem 1: Course Schedule II — LeetCode #210 — Pattern: Topological Sort
  - Hint: Same as Course Schedule I, but keep track of the processing order and return it.
  - Complexity: Time O(V+E) | Space O(V+E)
- Problem 2: Alien Dictionary — LeetCode #269 (Premium/LintCode 892) — Pattern: Graph Construction + Topological Sort
  - Hint: Compare adjacent words to find the first differing character to build a directed edge. Then run topological sort.
  - Complexity: Time O(V+E) | Space O(V+E)
- Problem 3: Coin Change II — LeetCode #518 — Pattern: DP Combinations
  - Hint: Unlike Coin Change I, order doesn't matter (combinations, not permutations). The outer loop must be the coins, and the inner loop the amounts.
  - Complexity: Time O(n×amount) | Space O(amount)

### Theory Block (1.5 hrs)
- Topic: Test Coverage and CI Quality Gates
- Subtopics covered today: Why high code coverage doesn't mean good tests. Mutation testing concepts. JaCoCo for Java code coverage.
- Coding exercise: Add the JaCoCo Maven plugin to a dummy POM. Configure it to fail the build if instruction coverage drops below 80%.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Integrate the JaCoCo plugin into the repository. Set the coverage minimum to 80%. Ensure that your GitHub Actions CI pipeline runs `mvn jacoco:check` and fails if coverage is insufficient.
- Definition of done: The CI pipeline strictly enforces test coverage requirements on every push.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Review application tracker. Prepare for Mock Interview.

### Daily Deliverable
- [ ] Read *Database Internals* (Chapter 2: B-Tree Basics).
- [ ] Complete the JaCoCo plugin exercise.
- [ ] Enforce JaCoCo gates in CI.
- [ ] Complete LeetCode #210, #269, and #518.

---

## Day 49 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate DP patterns and Kafka Streams.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post (e.g., Netflix tech blog).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 7. Evaluate your progress with Kubernetes concepts.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
