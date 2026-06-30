# Week 13: Interview Season Kickoff and Load Testing

## Day 85 — Warm-ups, Distributed Cache Design, and k6 Intro

### DSA Block (2.5 hrs)
- Goal: Shift from learning new patterns to executing known patterns flawlessly under time pressure. 
- Problem 1: Two Sum — LeetCode #1 (Amazon Tag) — Pattern: HashMap (Warm-up)
- Problem 2: Valid Parentheses — LeetCode #20 (Amazon Tag) — Pattern: Stack (Warm-up)
- Problem 3: Copy List with Random Pointer — LeetCode #138 (Amazon/Meesho Tag) — Pattern: HashMap/LL

### Theory Block (2 hrs)
- Topic: System Design Deep Dive — Distributed Cache
- Subtopics covered today: Memcached vs Redis. Consistent Hashing in caching layer. Thundering Herd mitigation (Mutex/Promises).
- Coding exercise: Verbally walk through the architecture of a global distributed cache in 15 minutes.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Install `k6` locally. Write a basic `load-test.js` script that simulates 50 virtual users (VUs) constantly hitting the `/products` endpoint for 30 seconds.
- Definition of done: The script runs and outputs a summary showing Request Rate and p95 latency.

### Career Block (1 hr)
- LinkedIn: Post 25 — The "Why" Behind Consistent Hashing (publish at 8 AM IST).
- Networking: Push hard on applications. Apply to 5 Tier A/B companies today.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 2* (Chapter 10: Real-time Gaming Leaderboard).
- [ ] Complete the Distributed Cache verbal walkthrough.
- [ ] Complete the basic k6 load test script.
- [ ] Complete 3 LeetCode warm-ups.

---

## Day 86 — Tagged Mediums, API Gateway Deep Dive, and Load Test Scripting

### DSA Block (2.5 hrs)
- Problem 1: Word Search — LeetCode #79 (Amazon Tag) — Pattern: DFS
- Problem 2: Number of Islands — LeetCode #200 (Amazon Tag) — Pattern: DFS/BFS
- Problem 3: Maximum Subarray — LeetCode #53 (Amazon Tag) — Pattern: Kadane's Algorithm

### Theory Block (2 hrs)
- Topic: System Design Deep Dive — API Gateways
- Subtopics covered today: TLS Termination. Rate Limiting strategies (Local vs Global). Auth validation at the edge. Routing logic.
- Coding exercise: Draw the sequence diagram for an unauthenticated request being rejected by the Gateway without hitting backend services.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Expand your `k6` script to simulate a complete user journey: Get Token -> List Products -> Create Order. Use dynamic variables to pass the token.
- Definition of done: The `k6` script accurately simulates the read/write load of a real user session.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Apply to 5 Tier A/B companies today.

### Daily Deliverable
- [ ] Read *The Pragmatic Programmer* (Chapter 1: A Pragmatic Philosophy).
- [ ] Complete the API Gateway sequence diagram.
- [ ] Complete the E2E k6 script.
- [ ] Complete 3 LeetCode warm-ups.

---

## Day 87 — Razorpay Tags, Leaderboard System, and Load Execution

### DSA Block (2.5 hrs)
- Problem 1: LRU Cache — LeetCode #146 (Razorpay Tag) — Pattern: Custom Data Structure
- Problem 2: Next Permutation — LeetCode #31 (Razorpay Tag) — Pattern: Array 
- Problem 3: Spiral Matrix — LeetCode #54 (Razorpay Tag) — Pattern: Matrix Simulation

### Theory Block (2 hrs)
- Topic: System Design Deep Dive — Leaderboard System
- Subtopics covered today: Redis Sorted Sets underneath the hood (Skip Lists). Scaling Redis (Redis Cluster). Handling ties.
- Coding exercise: Practice explaining why a standard RDBMS B-Tree index struggles with real-time rank updates compared to a Skip List.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Execute the load test. Run the `k6` E2E script against your Minikube cluster with HPA enabled. Observe the scaling behavior and capture the terminal output.
- Definition of done: You have raw data showing how your system handles a sudden spike of 200 VUs.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Apply to 5 Tier A/B companies today. Target reached: 15+ applications this week.

### Daily Deliverable
- [ ] Read *The Pragmatic Programmer* (Chapter 2: A Pragmatic Approach).
- [ ] Complete the Redis Skip List explanation.
- [ ] Execute the load test.
- [ ] Complete 3 LeetCode warm-ups.

---

## Day 88 — Meesho Tags, DB Revision, and Documentation

### DSA Block (2.5 hrs)
- Problem 1: Search in Rotated Sorted Array — LeetCode #33 (Meesho Tag) — Pattern: Binary Search
- Problem 2: Merge Intervals — LeetCode #56 (Meesho Tag) — Pattern: Array Sweep
- Problem 3: Kth Largest Element in an Array — LeetCode #215 (Meesho Tag) — Pattern: Min-Heap

### Theory Block (2 hrs)
- Topic: System Design Deep Dive — Database Revision
- Subtopics covered today: Partitioning vs Replication. ACID compliance. B-Trees vs LSM Trees. When to use NoSQL vs SQL.
- Coding exercise: No code. Do a 20-minute whiteboard review of database scaling techniques.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Begin drafting `docs/load-test-results.md`. Structure it: Methodology, Baseline Results, Auto-scaling Observations, Bottlenecks Identified.
- Definition of done: The skeleton of the document is ready and the baseline results are populated.

### Career Block (1 hr)
- LinkedIn: Post 26 — Load Testing Microservices with k6 (publish at 8 AM IST).
- Technical Blog: Write and publish **Blog Post 6** on Hashnode.
  Topic: "Load Testing My Microservices with k6: What I Found"
  Content: Share your actual load test results from `docs/load-test-results.md`.
  Include real numbers: P99 latency, error rate, throughput.
  Show the bottleneck you discovered and how you fixed it (or plan to).
  Real data from real systems is 10× more valuable than tutorials.
- Networking: Follow up on all Monday applications.

### Daily Deliverable
- [ ] Read *The Pragmatic Programmer* (Chapter 3: The Basic Tools).
- [ ] Complete the DB whiteboard review.
- [ ] Draft load test results document.
- [ ] Complete 3 LeetCode warm-ups.

---

## Day 89 — Amazon Tags, Distributed Systems Revision, and Bottleneck Analysis

### DSA Block (2.5 hrs)
- Problem 1: Letter Combinations of a Phone Number — LeetCode #17 (Amazon Tag) — Pattern: Backtracking
- Problem 2: Group Anagrams — LeetCode #49 (Amazon Tag) — Pattern: HashMap
- Problem 3: Binary Tree Level Order Traversal — LeetCode #102 (Amazon Tag) — Pattern: BFS

### Theory Block (2 hrs)
- Topic: System Design Deep Dive — Distributed Systems Revision
- Subtopics covered today: CAP Theorem, Consistent Hashing, Vector Clocks, Gossip Protocol.
- Coding exercise: Explain the Gossip Protocol as if you were talking to a Junior Developer.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Analyze the bottlenecks from your load test. Did the DB CPU max out? Did the Gateway throttle? Add this analysis to `docs/load-test-results.md`.
- Definition of done: The bottleneck analysis section is complete with clear hypotheses.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: First round interviews should be getting scheduled. Prep for HR screens.

### Daily Deliverable
- [ ] Read *The Pragmatic Programmer* (Chapter 4: Pragmatic Paranoia).
- [ ] Complete the Gossip Protocol explanation.
- [ ] Complete bottleneck analysis in the load test doc.
- [ ] Complete 3 LeetCode warm-ups.

---

## Day 90 (Weekend) — Mock Loop, Load Test Finalization, and System Design Review

### DSA Block (3.5 hrs)
- Problem 1: Word Break — LeetCode #139 (Amazon Tag) — Pattern: DP
- Problem 2: Course Schedule — LeetCode #207 (Amazon Tag) — Pattern: Topological Sort
- Problem 3: Lowest Common Ancestor of a Binary Tree — LeetCode #236 (Amazon/Meesho Tag) — Pattern: Tree DFS

### Theory Block (1.5 hrs)
- Topic: System Design Mock
- Subtopics covered today: System Design framework review.
- Coding exercise: None.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Finalize `docs/load-test-results.md`. Add graphs (screenshots from Grafana/k6). Commit and push.
- Definition of done: The repository now proves you know how to validate system scalability empirically.

### Career Block (1 hr)
- Mock Interview: 60-minute DSA Mock Interview. Do 2 Mediums back-to-back with your accountability partner.
- **Day 90 Open Source Milestone:** You should have at least 1 merged PR
  on TheAlgorithms/Java or a comparable popular Java repo by now.
  If merged: add the repository URL to your LinkedIn "Projects" section
  and your GitHub profile README "Open Source" subsection.
  If still pending: this is the last push before interview season peak.
  Comment on the PR asking for maintainer review with: "Happy to make
  any requested changes — would love to get this merged before I start
  interviewing next week."
  Target: 1–2 merged PRs visible on your GitHub contribution graph by Day 100.
- Networking: Review interview schedules.

### Daily Deliverable
- [ ] Read *The Pragmatic Programmer* (Chapter 5: Bend, or Break).
- [ ] Complete the DSA Mock Interview.
- [ ] Finalize `load-test-results.md`.
- [ ] Complete 3 LeetCode warm-ups.

---

## Day 91 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Rest day. Mentally prepare for the final sprint of interviews.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post.
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 13. Your E-Commerce project is now elite-tier.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
