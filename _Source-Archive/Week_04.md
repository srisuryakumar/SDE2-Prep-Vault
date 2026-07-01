# Week 4: Concurrency Deep Dive, DB Internals, and Mocking

## Day 22 — Heaps, Thread Pools, and Mockito

### DSA Block (2.5 hrs)
- Problem 1: Find Median from Data Stream — LeetCode #295 — Pattern: Two Heaps
  - Hint: Maintain a Max-Heap for the lower half and a Min-Heap for the upper half. Balance them so their sizes differ by at most 1.
  - Complexity: Time O(log n) insert | Space O(n)
- Problem 2: Task Scheduler — LeetCode #621 — Pattern: Max-Heap + Queue
  - Hint: Use a Max-Heap ordered by task frequency. Use a Queue to track cooldowns.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Concurrency Deep Dive
- Subtopics covered today: Thread Pools (`ExecutorService`). Avoid raw `new Thread()`. The `Callable` interface vs `Runnable`. `Future` and `CompletableFuture`. Virtual Threads (Java 21): Project Loom and its impact on server-side Java.
- Coding exercise: Use an `ExecutorService` with a fixed thread pool to execute 10 instances of a `Callable` that simulates an API call (Thread.sleep). Collect and print the results using `Future.get()`.

**Additional Coding Exercise — Virtual Threads (Java 21):**
Compare three approaches to running 10,000 concurrent tasks:

```java
// Approach 1: Traditional thread pool (will likely OOM or be very slow)
ExecutorService pool = Executors.newFixedThreadPool(200);

// Approach 2: Virtual Thread executor (Java 21+)
ExecutorService vPool = Executors.newVirtualThreadPerTaskExecutor();

// Both execute the same task:
Runnable task = () -> {
    try { Thread.sleep(100); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
};

// Time both and compare. Virtual threads will complete 10,000 tasks
// in roughly 100ms. The thread pool will take ~5000ms (10000/200 * 100ms).
```

Key facts for interviews:
- Virtual threads are managed by the JVM, not the OS
- An OS thread needs ~1MB stack. A virtual thread needs ~1KB
- You can run millions of virtual threads without OOM
- They mount onto a small pool of OS carrier threads
- Perfect for I/O-bound workloads (HTTP calls, DB queries, Kafka)
- Java 21 `Thread.ofVirtual().start(runnable)` is the API
- Why this matters: reduces the need for reactive/WebFlux in I/O-heavy services
- Interview answer: "In Java 21, I'd use virtual threads via
  `Executors.newVirtualThreadPerTaskExecutor()` for any I/O-bound
  service instead of a traditional thread pool, because each virtual thread
  costs ~1KB vs ~1MB for an OS thread."

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Introduce Mockito. Write a unit test for your `TaskService` by mocking the `TaskRepository` (`@Mock` and `@InjectMocks`). Verify that repository methods are called without hitting the database.
- Definition of done: The service layer tests pass cleanly and run in milliseconds because the database layer is entirely mocked.

### Career Block (1 hr)
- LinkedIn: Post 7 — HashMap Internals (publish at 8 AM IST).
- Networking: Identify 5 Target companies (Tier C - Practice companies) for early interview practice.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 80: Prefer executors, tasks, and streams to threads).
- [ ] Complete the `ExecutorService` coding exercise.
- [ ] Complete LeetCode #295 and #621.
- [ ] Committed to GitHub.

---

## Day 23 — HashMap Grouping, Locks, and Docker Basics

### DSA Block (2.5 hrs)
- Problem 1: Subarray Sums Divisible by K — LeetCode #974 — Pattern: Prefix Sum + HashMap
  - Hint: Keep a running sum modulo k. Use a HashMap to count how many times
  - Complexity: Time O(n) | Space O(n)
    each remainder has appeared. If the same remainder appears again, the subarray
    between those positions has a sum divisible by k. Handle negative remainders
    by adding k: `remainder = ((sum % k) + k) % k`.
- Problem 2: Longest Consecutive Sequence — LeetCode #128 — Pattern: HashSet
  - Hint: Put all numbers in a HashSet. Only start counting a sequence if
  - Complexity: Time O(n) | Space O(n)
    `num - 1` is NOT in the set (confirming it's the start of a sequence).
    Walk forward counting while `num + 1` exists in the set.

### Theory Block (2 hrs)
- Topic: Advanced Concurrency & Docker
- Subtopics covered today: Explicit Locks (`ReentrantLock`, `ReadWriteLock`). Wait/Notify vs `Condition` variables. Intro to Docker (Images vs Containers, `Dockerfile`).
- Coding exercise: Write a classic Producer-Consumer problem using a `ReentrantLock` and two `Condition` variables (`notFull` and `notEmpty`).

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Dockerize the application. Write a multi-stage `Dockerfile` (Stage 1: Maven build, Stage 2: JRE slim runtime). Build the image and run it.
- Definition of done: The API runs inside a Docker container (`docker run -p 8080:8080 todo-api`) and responds successfully to HTTP requests.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Begin tailoring your resume specifically highlighting the Spring Boot, Redis, and PostgreSQL skills gained in `todo-api`.

### Daily Deliverable
- [ ] Read *Java Concurrency in Practice* (Chapter 5: Building Blocks).
- [ ] Complete the Producer-Consumer Lock exercise.
- [ ] Complete LeetCode #560 and #128.
- [ ] Committed to GitHub.

---

## Day 24 — BST Mastery, B-Trees, and Docker Compose

### DSA Block (2.5 hrs)
- Problem 1: Kth Smallest Element in a BST — LeetCode #230 — Pattern: Inorder Traversal
  - Hint: An inorder traversal of a BST visits nodes in strictly ascending order. Keep a counter and stop when you hit `k`.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Binary Tree Zigzag Level Order Traversal — LeetCode #103 — Pattern: BFS + Deque
  - Hint: Use standard BFS, but alternate appending to the front vs back of a list for each level.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: Database Internals
- Subtopics covered today: How RDBMS store data on disk. Pages/Blocks. B-Trees and B+ Trees. Why B+ Trees are ideal for disk-based storage (sequential leaf traversal).
- Coding exercise: Write a SQL script to generate 1 million rows of dummy data in PostgreSQL. Measure the time of a `SELECT` query with and without an index.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Write a `docker-compose.yml` file that orchestrates three services: your Spring Boot app, a PostgreSQL database, and a Redis instance.
- Definition of done: Running `docker-compose up -d` spins up the entire stack, fully wired together via Docker networking.

### Career Block (1 hr)
- Technical Blog: Write and publish Blog Post 1 (Topic: "TestContainers vs H2 for Spring Boot testing" or "Understanding the N+1 problem").
- LinkedIn: Share your blog post.

### Daily Deliverable
- [ ] Read *Spring in Action* (Relevant chapters on Data JPA).
- [ ] Complete the DB Index timing exercise.
- [ ] Complete LeetCode #230 and #103.
- [ ] Committed to GitHub.

---

## Day 25 — Advanced Trees, Isolation Levels, and Mockito ArgumentCaptor

### DSA Block (2.5 hrs)
- Problem 1: Lowest Common Ancestor of a Binary Tree — LeetCode #236 — Pattern: Post-order Traversal
  - Hint: Recursively search left and right. If both return non-null, the current node is the LCA. If only one returns non-null, bubble it up.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Serialize and Deserialize Binary Tree — LeetCode #297 — Pattern: Pre-order/BFS Traversal
  - Hint: Use pre-order traversal. Record nulls explicitly (e.g., with `"N"`). Split by commas for deserialization.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: Database Internals
- Subtopics covered today: ACID properties deep dive. Transaction Isolation Levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable). Phenomena (Dirty Read, Non-repeatable Read, Phantom Read).
- Coding exercise: Open two separate SQL terminals. Start a transaction in both. Replicate a "Lost Update" or "Dirty Read" depending on your DB's default isolation level.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Enhance your tests. Use Mockito's `ArgumentCaptor` to capture the exact `Task` entity being passed to `taskRepository.save()` and write AssertJ assertions against its fields.
- Definition of done: The test successfully intercepts the method argument and verifies the payload matches the expected state.

### Career Block (1 hr)
- LinkedIn: Post 8 — LeetCode Patterns Carousel (publish at 6 PM IST).
- Networking: Apply to 3 Tier C (Practice) companies. This is your first real application push.

### Daily Deliverable
- [ ] Read *Java Concurrency in Practice* (Chapter 10: Avoiding Liveness Hazards).
- [ ] Complete the SQL transaction isolation exercise.
- [ ] Complete LeetCode #236 and #297.
- [ ] Committed to GitHub.

---

## Day 26 — Trie Basics, Cache Patterns, and Pagination

### DSA Block (2.5 hrs)
- Problem 1: Implement Trie (Prefix Tree) — LeetCode #208 — Pattern: Trie
  - Hint: Each TrieNode needs an array of children (`TrieNode[26]`) and a `boolean isEndOfWord`.
  - Complexity: Time O(m) per op | Space O(n×m)
- Problem 2: Word Dictionary — LeetCode #211 — Pattern: Trie + Backtracking
  - Hint: For a `.` wildcard, you must iterate over all 26 possible children and recursively check if any path matches.
  - Complexity: Time O(m) search | Space O(n×m)

### Theory Block (2 hrs)
- Topic: System Design Basics (Caching)
- Subtopics covered today: Cache eviction policies (LRU, LFU, FIFO). Cache updating patterns (Cache-Aside, Write-Through, Write-Behind). The Thundering Herd problem.
- Coding exercise: Map out the architecture of a high-throughput read-heavy system using Draw.io, highlighting where Write-Through vs Cache-Aside is used.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Add Pagination and Sorting to the GET endpoints. Use Spring Data's `Pageable` and `PageRequest`. Update the controller to accept `page`, `size`, and `sort` query parameters.
- Definition of done: Requesting `/tasks?page=0&size=5` returns a structured page object containing only 5 items and metadata (total pages, total elements).

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Follow up on any referral requests.

### Daily Deliverable
- [ ] Read *Spring in Action* (REST APIs).
- [ ] Complete the Caching Architecture diagram.
- [ ] Complete LeetCode #208 and #211.
- [ ] Committed to GitHub.

---

## Day 27 (Weekend) — Mixed Tree/Heap, ConcurrentHashMap, and CI/CD

### DSA Block (3.5 hrs)
- Problem 1: Merge Intervals — LeetCode #56 — Pattern: Sorting + Array Sweep
  - Hint: Sort intervals by start time. Iterate, and if the current interval overlaps with the last merged interval, update the last merged interval's end time.
  - Complexity: Time O(n log n) | Space O(n)
- Problem 2: Insert Interval — LeetCode #57 — Pattern: Array Sweep
  - Hint: Add intervals before the new interval, merge the overlapping part, then add the rest.
  - Complexity: Time O(n) | Space O(n)
- Problem 3: Non-overlapping Intervals — LeetCode #435 — Pattern: Greedy
  - Hint: Sort by end time. Always keep the interval that ends earliest to leave room for the most subsequent intervals.
  - Complexity: Time O(n log n) | Space O(1)

### Theory Block (1.5 hrs)
- Topic: Concurrency Deep Dive
- Subtopics covered today: Internals of `ConcurrentHashMap` (lock striping in Java 7, CAS + synchronized node locking in Java 8+). Why you shouldn't use `Collections.synchronizedMap()`.
- Coding exercise: Write a program that attempts to modify an `ArrayList` and a `CopyOnWriteArrayList` while iterating over them, observing the `ConcurrentModificationException` in the former.

### Project Block (1.5 hrs)
- Repository: `todo-api`
- Task: Set up a basic GitHub Actions CI/CD pipeline. Create `.github/workflows/build.yml` that checks out code, sets up JDK 17, and runs `mvn test`.
- Definition of done: The GitHub Actions tab shows a green checkmark indicating tests passed automatically on your push.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Reach out to a peer to schedule a mock interview for next week.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 81: Prefer concurrency utilities to wait and notify).
- [ ] Complete the `ConcurrentModificationException` exercise.
- [ ] Complete LeetCode #56, #57, and #435.
- [ ] Committed to GitHub.

---

## Day 28 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode. Month 1 Foundation is complete.

### Theory Block (0 hrs)
- Rest day. Consolidate your understanding of DB internals and Concurrency.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post.
  - Scan Hacker News.
  - Log findings in the study journal.
- **Weekly Scorecard:** Fill out the scorecard for Week 4.
- **Month 1 Review:** Evaluate your consistency. Are you hitting the 2.5-hour DSA block targets? Are your GitHub squares solid green?

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
