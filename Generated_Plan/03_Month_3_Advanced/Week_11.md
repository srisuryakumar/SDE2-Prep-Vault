# Week 11: System Design Vol 2 Start, AWS, and Observability

## Day 71 — Timed DSA Practice, Splitwise LLD, and AWS Fundamentals

### DSA Block (2.5 hrs)
- Start of strictly timed practice. 20 minutes for Mediums, 40 minutes for Hards.
- Problem 1: LRU Cache — LeetCode #146 (Revision)
  - Target: Code it flawlessly in 15 minutes.
- Problem 2: K Closest Points to Origin — LeetCode #973 — Pattern: Max-Heap
  - Hint: Maintain a Max-Heap of size `k`. If the current point is closer than the root of the heap, `poll()` and `offer()`.
  - Complexity: Time O(n log k) | Space O(k)

### Theory Block (2 hrs)
- Topic: AWS Fundamentals
- Subtopics covered today: VPCs, Subnets (Public vs Private), Internet Gateways, NAT Gateways, EC2, Security Groups.
- Coding exercise: Draw an AWS architecture diagram showing an EC2 web server in a public subnet communicating with an RDS database in a private subnet.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **Splitwise LLD**. Focus on the exact balance algorithm: creating a graph of debts, minimizing cash flow using a greedy approach (Heap-based settling).
- Definition of done: The algorithm successfully minimizes a complex web of transactions into the fewest possible settlements.

### Career Block (1 hr)
- LinkedIn: Post 21 — AWS Lessons (publish at 8 AM IST).
- Networking: Reach out to 3 engineers at Tier A targets asking specific, technical questions about their recent blog posts.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 1: Proximity Service - Prep).
- [ ] Complete the AWS Architecture diagram.
- [ ] Implement Splitwise LLD.
- [ ] Complete LeetCode timed practice.

---

## Day 72 — Hard Intervals, Payment System Design, and IAM

### DSA Block (2.5 hrs)
- Problem 1: Employee Free Time — LeetCode #759 (Premium) — Pattern: Line Sweep / Min-Heap
  - Hint: Flatten all employee intervals. Sort by start time. Iterate and find gaps where the `max_end_time_so_far` is less than the current interval's start time.
  - Complexity: Time O(n log k) | Space O(k)
- Problem 2: Minimum Number of Arrows to Burst Balloons — LeetCode #452 — Pattern: Greedy Interval
  - Hint: Sort balloons by end coordinate. If the next balloon starts after the current arrow's position, you need a new arrow.
  - Complexity: Time O(n log n) | Space O(1)

### Theory Block (2 hrs)
- Topic: System Design — Payment System & AWS IAM
- Subtopics covered today: Designing a Payment Gateway (Idempotency keys, distributed locks, double-entry ledger). AWS IAM (Roles vs Users, Least Privilege).
- Coding exercise: Write an idempotency wrapper pseudo-code utilizing a Redis `SETNX` lock to prevent double charging.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **ATM Machine LLD** using the State Design Pattern and Chain of Responsibility for cash dispensing (dispense 2000s, then 500s, then 100s).
- Definition of done: Code compiles and correctly dispenses cash or throws an insufficient funds exception.

### Career Block (1 hr)
- Technical Blog: Write and publish **Blog Post 4** on Hashnode.
  Topic: "Minimizing Cash Flow: The Splitwise Debt Algorithm in Java"
  Content outline: (1) The problem — N people, M debts, minimize transactions.
  (2) Naive approach: pay everyone directly. (3) Better approach: net each
  person's balance. (4) Optimal: two-heap greedy matching of max creditor
  with max debtor. (5) Java implementation with code snippet.
  Share on LinkedIn as you publish. Tag it with #Java #Algorithms #LLD.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 11: Payment System).
- [ ] Complete the Idempotency pseudo-code exercise.
- [ ] Implement ATM Machine LLD.
- [ ] Complete LeetCode #759 and #452.

---

## Day 73 — Subarray Sums, Job Scheduler Design, and S3/RDS

### DSA Block (2.5 hrs)
- Problem 1: Continuous Subarray Sum — LeetCode #523 — Pattern: Prefix Sum + HashMap
  - Hint: If `prefixSum % k` has been seen before, the subarray between those two indices is a multiple of `k`. Store `(prefixSum % k)` mapped to its index.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Find Pivot Index — LeetCode #724 — Pattern: Prefix Sum
  - Hint: `left_sum == total_sum - left_sum - nums[i]`.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: System Design — Distributed Job Scheduler & AWS Data
- Subtopics covered today: Quartz Scheduler concepts. Delayed message queues (SQS Visibility Timeout, Redis Sorted Sets). AWS S3 vs EBS. Amazon RDS Multi-AZ.
- Coding exercise: Write a Redis Lua script snippet that polls a Sorted Set for delayed jobs where `score (timestamp) < now`.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Add a background worker component (or a scheduled task) that simulates a nightly reconciliation job (e.g., verifying all Orders mapped to successful Payments).
- Definition of done: A `@Scheduled` task executes successfully, simulating the cron job behavior.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Follow up on application tracker. You should have 10-15 active applications now.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 2: Nearby Friends).
- [ ] Complete the Redis delayed queue exercise.
- [ ] Implement the Scheduled reconciliation job.
- [ ] Complete LeetCode #523 and #724.

---

## Day 74 — Binary Search on Answer, Instagram Feed, and Observability

### DSA Block (2.5 hrs)
- Problem 1: Koko Eating Bananas — LeetCode #875 — Pattern: Binary Search on Answer
  - Hint: The minimum speed is 1, maximum is `max(piles)`. Binary search the speed `k`, calculating if Koko can finish within `H` hours at that speed.
  - Complexity: Time O(n log m) | Space O(1)
- Problem 2: Minimum Size Subarray Sum — LeetCode #209 — Pattern: Sliding Window
  - Hint: Expand right pointer to increase sum. Shrink left pointer to minimize the window while `sum >= target`.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: System Design — Instagram Feed & Observability
- Subtopics covered today: News Feed generation (Push/Fan-out vs Pull models). Hybrid fan-out for celebrities. Intro to Prometheus (Metrics) and Grafana (Dashboards).
- Coding exercise: Write a Prometheus `prometheus.yml` configuration to scrape a Spring Boot `/actuator/prometheus` endpoint.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Enable Spring Boot Actuator and Micrometer Prometheus registry in your microservices. Start a local Prometheus and Grafana instance using Docker Compose.
- Definition of done: Grafana dashboard is accessible locally, showing real-time JVM metrics (memory, CPU, HTTP request rates) from your microservices.

### Career Block (1 hr)
- LinkedIn: Post 22 — JWT vs OAuth 2.0 (publish at 6 PM IST).
- Networking: Research and identify the HM for a role you've applied to and send a direct message.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 3: Google Maps - Prep).
- [ ] Complete the Prometheus config exercise.
- [ ] Set up Prometheus and Grafana for the platform.
- [ ] Complete LeetCode #875 and #209.

---

## Day 75 — Matrix Searches, AWS CloudWatch, and Distributed Tracing

### DSA Block (2.5 hrs)
- Problem 1: Search a 2D Matrix II — LeetCode #240 — Pattern: Staircase Search
  - Hint: Start at the top-right corner. If the target is smaller, move left. If larger, move down.
  - Complexity: Time O(m+n) | Space O(1)
- Problem 2: Spiral Matrix — LeetCode #54 — Pattern: Matrix Simulation
  - Hint: Maintain four boundaries (top, bottom, left, right) and shrink them as you spiral inwards.
  - Complexity: Time O(m×n) | Space O(1)

### Theory Block (2 hrs)
- Topic: AWS CloudWatch & Distributed Tracing
- Subtopics covered today: AWS CloudWatch Logs, Metrics, and Alarms. Distributed Tracing with Jaeger/Zipkin. The concept of Trace ID and Span ID passing through microservices.
- Coding exercise: Configure logback to inject the Spring Cloud Sleuth/Micrometer Tracing Trace ID into every log line.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Integrate Micrometer Tracing (formerly Sleuth) and Zipkin into the microservices.
- Definition of done: Hitting the Gateway generates a Trace ID that propagates through to the Product and Order services, viewable in the Zipkin UI as a complete distributed trace.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Update CRM. Secure a referral for a Tier A company if possible.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 4: Distributed Message Queue).
- [ ] Complete the Trace ID logging exercise.
- [ ] Integrate Distributed Tracing (Zipkin).
- [ ] Complete LeetCode #240 and #54.

---

## Day 76 (Weekend) — Advanced Graphs, Mock Interview, and Review

### DSA Block (3.5 hrs)
- Problem 1: Word Search II — LeetCode #212 — Pattern: Trie + Backtracking (Revision)
  - Target: Code flawlessly in 25 minutes.
- Problem 2: Minimum Deletions to Make Character Frequencies Unique — LeetCode #1647 — Pattern: Greedy + HashSet
  - Hint: Count frequencies. Use a HashSet to track seen frequencies. If a frequency is seen, decrement it until it's unique or zero, keeping a count of deletions.
  - Complexity: Time O(n) | Space O(n)
- Problem 3: Bus Routes — LeetCode #815 — Pattern: BFS on Sets
  - Hint: The graph nodes are the *routes* (buses), not the stops. Build a map of `stop -> list of routes`. BFS over the routes.
  - Complexity: Time O(n×m) | Space O(n×m)

### Theory Block (1.5 hrs)
- Topic: Mock Interview Prep
- Subtopics covered today: Payment Gateway idempotency, AWS architecture, Splitwise algorithm.
- Coding exercise: None.

### Project Block (1.5 hrs)
- Mock Interview: 60-minute System Design Mock Interview focusing on a Payment/Transactional System.
- Definition of done: Complete the mock. Take notes on your handling of race conditions and ACID compliance during the discussion.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Consolidate feedback from the mock interview.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 5: Metrics Monitoring).
- [ ] Complete the System Design Mock Interview.
- [ ] Complete LeetCode #212, #1647, and #815.
- [ ] Committed to GitHub.

---

## Day 77 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate Observability and Tracing concepts.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post (e.g., Stripe engineering).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 11. You should have a fully observable, scalable microservice platform.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
