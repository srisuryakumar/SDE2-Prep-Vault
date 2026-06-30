# Week 12: Mixed DSA, Final LLDs, and Google Drive Design

## Day 78 — Mixed Pattern Timed Practice and Library Management LLD

### DSA Block (2.5 hrs)
- Problem 1: Gas Station — LeetCode #134 — Pattern: Greedy
  - Hint: If the total gas < total cost, return -1. Otherwise, a solution exists. Keep a running tank; if it dips below 0, the starting point must be at least the next station.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Next Permutation — LeetCode #31 — Pattern: Array Manipulation
  - Hint: Find the first decreasing element from the right. Find the smallest element to its right that is larger than it. Swap them, then reverse the rest of the array.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: LLD Principles Revision
- Subtopics covered today: Coupling and Cohesion. The Law of Demeter. Composition over Inheritance.
- Coding exercise: Refactor a badly written class that uses inheritance for behavior sharing into one that uses composition (e.g., changing a `FlyingBird extends Bird` to `Bird` with a `FlyBehavior` component).

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **Library Management System LLD**. Focus on fine searching (by title, author, subject) and the state management of a BookItem (Available, Reserved, Loaned, Lost).
- Definition of done: The LLD compiles and cleanly separates the Catalog search logic from the Reservation logic.

### Career Block (1 hr)
- LinkedIn: Post 23 — Mock Interview Experience (publish at 8 AM IST).
- Networking: Follow up on any Tier A applications. Your resume is strong now.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 6: Ad Click Event Aggregation).
- [ ] Complete the Composition over Inheritance exercise.
- [ ] Implement Library Management LLD.
- [ ] Complete LeetCode #134 and #31.

---

## Day 79 — Mixed DSA, Chess LLD, and Search Autocomplete Design

### DSA Block (2.5 hrs)
- Problem 1: Valid Sudoku — LeetCode #36 — Pattern: HashSet
  - Hint: Use arrays of HashSets for rows, columns, and 3x3 sub-boxes. E.g., `boxes[(r/3)*3 + c/3]`.
  - Complexity: Time O(1) | Space O(1)
- Problem 2: Longest Valid Parentheses — LeetCode #32 — Pattern: Stack / DP (Hard)
  - Hint: Stack approach: store indices. DP approach: `dp[i]` represents the length of the longest valid substring ending at `i`.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: System Design — Search Autocomplete
- Subtopics covered today: Distributed Tries. Caching hot queries. Updating the Trie asynchronously (Log aggregation -> MapReduce -> Update Trie weekly/daily).
- Coding exercise: Draw the architecture for collecting search analytics and rebuilding the Autocomplete Trie offline.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **Chess Game LLD**. Focus on the object-oriented structure: `Piece` (abstract), `Board`, `Spot`, `Player`, `Move`. Implement the valid move logic for just the Knight and Pawn.
- Definition of done: The core engine is structured and the Knight's `canMove()` logic correctly calculates L-shapes.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Apply to 3 more Tier A companies. 

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 7: Hotel Reservation System).
- [ ] Complete the Autocomplete architecture sketch.
- [ ] Implement Chess LLD foundation.
- [ ] Complete LeetCode #36 and #32.

---

## Day 80 — Monotonic Queues, Food Delivery LLD, and Google Drive Design

### DSA Block (2.5 hrs)
- Problem 1: Maximum Profit in Job Scheduling — LeetCode #1235 — Pattern: DP + Binary Search (Hard)
  - Hint: Sort jobs by end time. `dp[i]` is the max profit up to job `i`. For each job, binary search to find the latest non-overlapping job.
  - Complexity: Time O(n log n) | Space O(n)
- Problem 2: Jump Game II — LeetCode #45 — Pattern: Greedy (BFS-like)
  - Hint: Keep track of the `current_jump_end` and the `farthest` you can reach. When `i == current_jump_end`, increment the jump count and update the end.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: System Design — Google Drive / Object Storage
- Subtopics covered today: Chunking files (block storage). Deduplication. Sync conflicts. Uploading large files via multipart upload to S3.
- Coding exercise: Write pseudo-code for a file chunking and hashing algorithm used by the client before uploading to check for deduplication.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **Food Delivery System LLD** (Swiggy/Zomato). Focus on the Strategy pattern for assigning delivery partners (e.g., `NearestPartnerStrategy` vs `HighestRatedPartnerStrategy`).
- Definition of done: The Strategy pattern cleanly decouples the matching algorithm from the order processing logic.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Respond to recruiters.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 8: Distributed Email Service - Prep).
- [ ] Complete the Deduplication pseudo-code exercise.
- [ ] Implement Food Delivery LLD.
- [ ] Complete LeetCode #1235 and #45.

---

## Day 81 — DP Arrays, Hotel Booking LLD, and System Design Polish

### DSA Block (2.5 hrs)
- Problem 1: Longest Palindromic Subsequence — LeetCode #516 — Pattern: 2D String DP
  - Hint: Very similar to LCS. In fact, it is the LCS of the string and its reverse.
  - Complexity: Time O(n²) | Space O(n²)
- Problem 2: Edit Distance — LeetCode #72 — Pattern: 2D String DP (Revision)
  - Target: Code flawlessly in 20 minutes.

### Theory Block (2 hrs)
- Topic: System Design — Hotel Booking System
- Subtopics covered today: Handling extreme write concurrency for room booking. Overbooking logic. Distributed Locks.
- Coding exercise: Compare the BookMyShow locking mechanism with the Hotel Booking mechanism. Write down why Hotel booking might use asynchronous inventory sync while ticketing requires strict synchronous locks.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **Hotel Booking System LLD** (Correction 6 implementation). Focus on the `Room`, `RoomBooking`, and `Search` classes.
- Definition of done: The LLD compiles and cleanly handles the booking lifecycle. All 10 major LLDs are now complete.

### Career Block (1 hr)
- LinkedIn: Post 24 — BookMyShow Seat Booking Challenge (publish at 6 PM IST).
- Networking: Engage heavily on LinkedIn. Reach out to 3 engineers.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 9: S3-like Object Storage).
- [ ] Complete the Booking lock comparison exercise.
- [ ] Implement Hotel Booking System LLD.
- [ ] Complete LeetCode #516 and #72.

---

## Day 82 — Advanced DP, Distributed Transactions Review, and OpenTelemetry

### DSA Block (2.5 hrs)
- Problem 1: Minimum Insertion Steps to Make a String Palindrome — LeetCode #1312 — Pattern: DP
  - Hint: The answer is `string.length() - length of Longest Palindromic Subsequence`.
  - Complexity: Time O(n²) | Space O(n²)
- Problem 2: Burst Balloons — LeetCode #312 — Pattern: Divide and Conquer DP (Hard)
  - Hint: Think backwards. Pick the *last* balloon to burst. `dp[i][j]` is max coins for bursting balloons between `i` and `j`.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: Observability Deep Dive
- Subtopics covered today: OpenTelemetry. The transition from vendor-specific agents to OTel standard. How metrics, logs, and traces interconnect (Exemplars).
- Coding exercise: Read the OpenTelemetry Java documentation. Write down the conceptual difference between a Metric and a Trace Span.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Ensure all services have health checks (`/actuator/health`). Update your `docker-compose.yml` to use these health checks to sequence the startup (e.g., Order service `depends_on: database` with `condition: service_healthy`).
- Definition of done: The Docker Compose stack starts reliably without services crashing due to DB unavailability.

### Career Block (1 hr)
- Technical Blog: Write and publish **Blog Post 5** on Hashnode.
  Topic: "Observability in Microservices: Metrics, Logs, and Traces"
  Content outline: (1) The three pillars. (2) Why they're different.
  (3) Prometheus scraping /actuator/prometheus. (4) Trace ID propagation
  across services. (5) What I set up in the E-Commerce platform.
  Include a screenshot of the Grafana dashboard from your own setup.
- Share on LinkedIn immediately after publishing (this becomes LinkedIn
  post material for Week 12 if needed).
- Networking: Verify all Tier A and B applications are submitted.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 10: Real-time Gaming Leaderboard - Prep).
- [ ] Complete the OpenTelemetry conceptual exercise.
- [ ] Implement robust Docker Compose health checks.
- [ ] Complete LeetCode #1312 and #312.

---

## Day 83 (Weekend) — Mixed Hard Problems, Mock Interview, and Review

### DSA Block (3.5 hrs)
- Problem 1: Largest Rectangle in Histogram — LeetCode #84 — Pattern: Monotonic Stack (Hard)
  - Hint: Maintain a stack of strictly increasing heights. If you encounter a smaller height, pop the stack and calculate the area for the popped height, as you've found its right boundary. Its left boundary is the new top of the stack.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Maximal Rectangle — LeetCode #85 — Pattern: Monotonic Stack (Hard)
  - Hint: Convert each row into a histogram (add 1 if '1', reset to 0 if '0') and apply the solution from #84.
  - Complexity: Time O(m×n) | Space O(n)
- Problem 3: Basic Calculator — LeetCode #224 — Pattern: Stack
  - Hint: Use a stack to hold previous sums and signs when encountering `(`.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (1.5 hrs)
- Topic: Month 3 Review
- Subtopics covered today: Reviewing the 5-Step System Design framework, Kafka/Saga patterns, and LLD structural principles.
- Coding exercise: None.

### Project Block (1.5 hrs)
- Mock Interview: 60-minute System Design Mock Interview. Focus on Google Drive or a high-storage system.
- Definition of done: Complete the mock. Assess your estimation skills (e.g., storage capacity sizing).

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Review progress. Month 4 is all about interviewing and finalizing skills.

### Daily Deliverable
- [ ] Read *Clean Code* (Chapter 6: Objects and Data Structures).
- [ ] Complete the System Design Mock Interview.
- [ ] Complete LeetCode #84, #85, and #224.
- [ ] Committed to GitHub.

---

## Day 84 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode. Month 3 Advanced is complete.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate all the LLD and System Design patterns.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post (e.g., Gergely Orosz's Pragmatic Engineer).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 12. 
- **Month 3 Review:** You have completed the bulk of the intense learning. The final month is dedicated to mock loops, behavioral prep, and execution.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
