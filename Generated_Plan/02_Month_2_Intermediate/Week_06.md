# Week 6: Kafka Architecture, TestContainers, and Backtracking

## Day 36 — Backtracking Start and Kafka Fundamentals

### DSA Block (2.5 hrs)
- Problem 1: Subsets — LeetCode #78 — Pattern: Backtracking
  - Hint: At each step, you make a choice: either include the current element in your subset or don't. Recurse for both choices.
  - Complexity: Time O(n×2ⁿ) | Space O(n)
- Problem 2: Permutations — LeetCode #46 — Pattern: Backtracking
  - Hint: Iterate through the array. Swap elements to form permutations, recurse, and then swap back (backtrack) to explore other paths.
  - Complexity: Time O(n×n!) | Space O(n)

### Theory Block (2 hrs)
- Topic: Kafka Architecture & Distributed Messaging
- Subtopics covered today: Topics, Partitions, Offsets, Producers, Consumers, Consumer Groups. Why Kafka appends to logs sequentially for high throughput.
- Coding exercise: Download Kafka (or run via Docker). Use the CLI tools to create a topic, start a console producer, and start a console consumer. Send messages and watch them arrive.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Add Spring Kafka dependencies. Configure a basic producer that sends an `OrderCreatedEvent` string to a Kafka topic when an order is successfully created.
- Definition of done: The API sends messages to local Kafka when the POST endpoint is hit, verified via the Kafka console consumer.

### Career Block (1 hr)
- LinkedIn: Post 11 — Kafka Partitions and Consumer Groups (publish at 8 AM IST).
- Networking: Begin Tier B targets preparation. Identify 3 Target Tier B companies (e.g., Flipkart, Amazon).

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 10: Heaps).
- [ ] Complete the Kafka CLI setup exercise.
- [ ] Implement Kafka Producer in `order-management-api`.
- [ ] Complete LeetCode #78 and #46.

---

## Day 37 — Backtracking Continued and Spring Kafka Consumers

### DSA Block (2.5 hrs)
- Problem 1: Combination Sum — LeetCode #39 — Pattern: Backtracking
  - Hint: Since you can reuse elements, when you recurse, do not increment the index. Only increment the index when you choose *not* to use the element.
  - Complexity: Time O(2ⁿ) | Space O(n)
- Problem 2: Letter Combinations of a Phone Number — LeetCode #17 — Pattern: Backtracking
  - Hint: Map digits to letters. Recurse down the length of the string, trying every possible letter for the current digit.
  - Complexity: Time O(4ⁿ) | Space O(n)

### Theory Block (2 hrs)
- Topic: Kafka Consumers & Spring Integration
- Subtopics covered today: Consumer Group rebalancing. Offset committing (auto vs manual). `@KafkaListener` in Spring Boot.
- Coding exercise: Write a standalone Java program using the raw `KafkaConsumer` API (no Spring) to poll a topic and print messages.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Add a `@KafkaListener` method to consume the `OrderCreatedEvent` from the topic. Implement a dummy inventory service that prints "Reserving inventory for order...".
- Definition of done: Creating an order via API logs the event creation, and milliseconds later, the listener logs the reception of the event.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Find alumni from your college working at Tier B companies.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 11: Searching).
- [ ] Complete the raw Kafka Consumer exercise.
- [ ] Implement `@KafkaListener` in the API.
- [ ] Complete LeetCode #39 and #17.

---

## Day 38 — Advanced Tries, TestContainers, and Database Migration

### DSA Block (2.5 hrs)
- Problem 1: Word Search II — LeetCode #212 — Pattern: Trie + Matrix DFS Backtracking
  - Hint: Build a Trie of all words to search for. Then do DFS from every cell in the grid. The Trie allows you to prune paths instantly if no word starts with the current path prefix.
  - Complexity: Time O(m×n×4ˡ) | Space O(k×l)
- Problem 2: Replace Words — LeetCode #648 — Pattern: Trie
  - Hint: Build a Trie from the dictionary roots. For each word in the sentence, traverse the Trie until you find an `isEndOfWord`, then replace.
  - Complexity: Time O(n×m) | Space O(n×m)

### Theory Block (2 hrs)
- Topic: Integration Testing with TestContainers
- Subtopics covered today: Why H2 fails for advanced DB testing (PostgreSQL arrays, JSONB, specific dialect features). The TestContainers library architecture.
- Coding exercise: Write a basic JUnit 5 test class annotated with `@Testcontainers` that spins up a generic PostgreSQL Docker container and asserts it is running.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Rip out H2. Add TestContainers for PostgreSQL and Kafka. Refactor your `@DataJpaTest` and Kafka integration tests to connect dynamically to the TestContainer URLs using `@DynamicPropertySource`.
- Definition of done: `mvn test` spins up real PostgreSQL and Kafka containers via Docker, runs the tests against them, and passes.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Send connection requests to the alumni identified yesterday using Template 5.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 12: Hash Tables).
- [ ] Complete the generic TestContainers exercise.
- [ ] Migrate `order-management-api` tests to TestContainers.
- [ ] Complete LeetCode #212 and #648.

---

## Day 39 — CAP Theorem, Consistency Models, and DP Recap

### DSA Block (2.5 hrs)
- Problem 1: Coin Change — LeetCode #322 — Pattern: 1D Dynamic Programming (Unbounded Knapsack)
  - Hint: `dp[i] = min(dp[i], dp[i - coin] + 1)`. Initialize the array with a dummy high value (e.g., `amount + 1`).
  - Complexity: Time O(n×amount) | Space O(amount)
- Problem 2: Maximum Product Subarray — LeetCode #152 — Pattern: 1D Dynamic Programming
  - Hint: Because multiplying by a negative flips the sign, you must track both the `max_so_far` and `min_so_far` ending at each position.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Distributed Systems Fundamentals
- Subtopics covered today: CAP Theorem (Consistency, Availability, Partition Tolerance). Eventual vs Strong Consistency. The fallacy of CP vs AP (it's really C or A *during* a P). 
- Coding exercise: Read the original CAP theorem proof summary. Write a 200-word explanation in your study journal explaining why MongoDB is CP and Cassandra is AP.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Integrate Flyway for database migrations. Create `V1__init.sql` for your initial schema. Remove Hibernate's `ddl-auto: update`.
- Definition of done: The app and tests boot up using Flyway to create the database schema on the real PostgreSQL instances (both prod and TestContainers).

### Career Block (1 hr)
- LinkedIn: Post 12 — TestContainers vs H2 (publish at 6 PM IST).
- Networking: Apply to 1 Tier B target company. 

### Daily Deliverable
- [ ] Read *DDIA* (Chapter 1: Reliable, Scalable, and Maintainable Applications).
- [ ] Complete the CAP theorem explanation.
- [ ] Integrate Flyway into `order-management-api`.
- [ ] Complete LeetCode #322 and #152.

---

## Day 40 — Partitioning, Consistent Hashing, and Advanced Backtracking

### DSA Block (2.5 hrs)
- Problem 1: N-Queens — LeetCode #51 — Pattern: Backtracking (Hard)
  - Hint: Place queens row by row. Maintain HashSets for the columns, positive diagonals (`r+c`), and negative diagonals (`r-c`) to check validity in O(1).
  - Complexity: Time O(n!) | Space O(n)
- Problem 2: Word Search — LeetCode #79 — Pattern: Matrix Backtracking
  - Hint: Standard DFS. Mark the cell as visited by temporarily modifying its character (e.g., to `#`), then restore it after the recursive call.
  - Complexity: Time O(m×n×4ˡ) | Space O(l)

### Theory Block (2 hrs)
- Topic: Distributed Systems (Partitioning)
- Subtopics covered today: Sharding strategies (Range vs Hash). The Hot Spot / Celebrity problem. Consistent Hashing (why the ring is needed when scaling nodes).
- Coding exercise: Implement a basic Consistent Hashing algorithm in Java using a `TreeMap`. Map servers to the ring, then map a key to the closest server using `treeMap.ceilingKey()`.

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Update the Kafka producer to use the `order_id` as the message key. This guarantees that all events for the same order are written to the same partition.
- Definition of done: Code verifies that Kafka events include the key.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Follow up on Tier B alumni messages.

### Daily Deliverable
- [ ] Read *DDIA* (Chapter 2: Data Models and Query Languages).
- [ ] Complete the Consistent Hashing Java exercise.
- [ ] Update Kafka Producer with keys.
- [ ] Complete LeetCode #51 and #79.

---

## Day 41 (Weekend) — DP Knapsack Patterns and Pattern Matching

### DSA Block (3.5 hrs)
- Problem 1: Partition Equal Subset Sum — LeetCode #416 — Pattern: 0/1 Knapsack DP
  - Hint: The target sum is `TotalSum / 2`. The problem reduces to: can we pick a subset that sums exactly to this target?
  - Complexity: Time O(n×sum) | Space O(sum)
- Problem 2: Target Sum — LeetCode #494 — Pattern: 0/1 Knapsack DP
  - Hint: Calculate the required subset sum using math: `Subset1 - Subset2 = Target`, `Subset1 + Subset2 = Total`. So `Subset1 = (Target + Total) / 2`. Find ways to sum to `Subset1`.
  - Complexity: Time O(n×sum) | Space O(sum)
- Problem 3: Longest Increasing Subsequence — LeetCode #300 — Pattern: DP / Binary Search
  - Hint: O(N^2) DP solution: `dp[i] = max(dp[j]) + 1` for all `j < i` where `nums[j] < nums[i]`. O(N log N) uses a tails array and binary search.
  - Complexity: Time O(n log n) | Space O(n)

### Theory Block (1.5 hrs)
- Topic: Java 21+ Pattern Matching
- Subtopics covered today: Record Patterns, Pattern Matching for `switch` (with guard conditions).
- Coding exercise: Rewrite the `PaymentState` switch from Week 2 using Java 21 Record Patterns with guard clauses (e.g., `case Success(var id, var amount) when amount > 10000 -> ...`).

### Project Block (1.5 hrs)
- Repository: `order-management-api`
- Task: Refactor data transfer objects to use Java Records. Implement the Dead Letter Queue (DLQ) pattern for your Kafka listener. If processing an event fails 3 times, route it to `order-events-dlq`.
- Definition of done: DLQ configuration is active. Simulating an error in the listener eventually pushes the message to the DLQ topic.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Review progress. Prepare for Month 2 midway assessment.

### Daily Deliverable
- [ ] Read *EPI in Java* (Chapter 13: Sorting).
- [ ] Complete the Java 21 Pattern Matching exercise.
- [ ] Complete LeetCode #416, #494, and #300.
- [ ] Committed to GitHub.

---

## Day 42 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate Backtracking and Kafka architecture.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read a post on Kafka at scale (e.g., LinkedIn engineering blog).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 6. You are halfway through Month 2.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
