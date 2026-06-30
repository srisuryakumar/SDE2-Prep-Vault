# Week 10: Bit Manipulation, WhatsApp Design, and K8s HPA

## Day 64 — Bit Manipulation Basics, WhatsApp System Design, and BookMyShow LLD

### DSA Block (2.5 hrs)
- Problem 1: Single Number — LeetCode #136 — Pattern: Bitwise XOR
  - Hint: `A XOR A = 0`, and `A XOR 0 = A`. XOR all elements; the duplicate pairs cancel out.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Number of 1 Bits — LeetCode #191 — Pattern: Bit Manipulation
  - Hint: `n & (n - 1)` flips the least significant 1-bit to 0. Count how many times you can do this.
  - Complexity: Time O(log n) | Space O(1)

### Theory Block (2 hrs)
- Topic: System Design — WhatsApp / Chat System
- Subtopics covered today: Persistent WebSockets. Message routing. Read receipts (Ack flows). End-to-end encryption basics. Offline message storage (Cassandra).
- Coding exercise: Sketch the High-Level Design for WhatsApp, explicitly showing the WebSocket servers, the routing layer, and the Cassandra DB.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the **BookMyShow LLD**. Focus heavily on the concurrency aspect: write a test that spawns 10 threads trying to book the exact same `Seat` object simultaneously, proving your locking mechanism works.
- Definition of done: The concurrency test passes, and double-booking is prevented.

### Career Block (1 hr)
- LinkedIn: Post 19 — Kubernetes Zero-Downtime Deployment (publish at 8 AM IST).
- Networking: Apply to 2 more Tier A target companies. Follow up with recruiters.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 12: Design a Chat System).
- [ ] Complete the WhatsApp HLD sketch.
- [ ] Implement BookMyShow LLD with concurrency test.
- [ ] Complete LeetCode #136 and #191.

---

## Day 65 — Advanced Bitwise, Elevator LLD, and Kafka Schema Registry

### DSA Block (2.5 hrs)
- Problem 1: Counting Bits — LeetCode #338 — Pattern: DP + Bit Manipulation
  - Hint: `dp[i] = dp[i >> 1] + (i & 1)`. The number of 1s in `i` is the number of 1s in `i/2` plus 1 if `i` is odd.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Single Number III — LeetCode #260 — Pattern: Bitwise XOR
  - Hint: XOR all numbers to get `A XOR B`. Find the lowest set bit in this result (`diff &= -diff`). Group numbers based on this bit to isolate A and B.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Distributed Event Streaming
- Subtopics covered today: Kafka Schema Registry. Avro serialization vs JSON. Why schemas are required when multiple microservices evolve independently.
- Coding exercise: Define a simple `.avsc` Avro schema for an `OrderEvent`.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform` and `lld-java`
- Task: In `lld-java`, implement the **Elevator System LLD** using the State pattern and a dispatcher algorithm (e.g., SCAN/LOOK). In the ecommerce platform, add the Confluent Kafka Schema Registry dependency and configure serializers.
- Definition of done: Elevator LLD compiles. The ecommerce platform is prepared to use Avro.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Search for "Hiring SDE 2 Backend" on LinkedIn posts and comment/DM.

### Daily Deliverable
- [ ] Read *Clean Code* (Chapter 5: Formatting).
- [ ] Complete the Avro schema exercise.
- [ ] Implement Elevator LLD.
- [ ] Complete LeetCode #338 and #260.

---

## Day 66 — Math Algorithms, Uber Driver Tracking, and CI/CD

### DSA Block (2.5 hrs)
- Problem 1: Count Primes — LeetCode #204 — Pattern: Sieve of Eratosthenes
  - Hint: Create a boolean array. Start from 2, mark all multiples as non-prime. `O(N log log N)` time.
  - Complexity: Time O(n log log n) | Space O(n)
- Problem 2: Pow(x, n) — LeetCode #50 — Pattern: Fast Exponentiation
  - Hint: `x^n = (x^2)^(n/2)`. Handle negative `n` by inverting `x`.
  - Complexity: Time O(log n) | Space O(log n)

### Theory Block (2 hrs)
- Topic: System Design — Uber Driver Location Tracking
- Subtopics covered today: Quadtrees. Geohashing. Redis Geo features. Handling extreme write-heavy workloads (millions of drivers updating location every 5 seconds).
- Coding exercise: Spin up Redis locally and use `GEOADD` and `GEORADIUS` to add coordinates and find points within a radius.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Finalize the GitHub Actions CI/CD pipeline. Add a step to build the Docker image and push it to GitHub Container Registry (GHCR) after tests pass.
- Definition of done: The pipeline builds the image and a new package appears in your GitHub profile's Packages tab.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Send connection requests to 3 engineers at Uber.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 13: Design a Search Autocomplete System - Prep).
- [ ] Complete the Redis Geo CLI exercise.
- [ ] Finalize CI/CD pipeline for the ecommerce platform.
- [ ] Complete LeetCode #204 and #50.

---

## Day 67 — Interval Intersections, Netflix Design, and K8s HPA

### DSA Block (2.5 hrs)
- Problem 1: Interval List Intersections — LeetCode #986 — Pattern: Two Pointers on Intervals
  - Hint: The intersection is `[max(startA, startB), min(endA, endB)]`. If valid, add to result. Advance the pointer of the interval that ends earlier.
  - Complexity: Time O(m+n) | Space O(m+n)
- Problem 2: Meeting Rooms II — LeetCode #253 — Pattern: Chronological Sweepline / Min-Heap
  - Hint: Sort start times and end times separately. Use two pointers. Alternatively, use a Min-Heap of end times.
  - Complexity: Time O(n log n) | Space O(n)

### Theory Block (2 hrs)
- Topic: System Design — Netflix / Video Streaming & K8s Autoscaling
- Subtopics covered today: Video transcoding pipelines. Content Delivery Networks (CDNs). Kubernetes Horizontal Pod Autoscaler (HPA) and Metrics Server.
- Coding exercise: Write an `hpa.yaml` manifest that targets your Product service deployment, scaling up if CPU utilization exceeds 70%.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Apply the HPA manifest to your local Minikube cluster. Run an Apache Bench (`ab`) or `k6` load test against the API to artificially spike CPU.
- Definition of done: `kubectl get hpa` shows the replica count increasing from 1 to 3 under load.

### Career Block (1 hr)
- LinkedIn: Post 20 — CI/CD Pipeline Walkthrough (publish at 6 PM IST).
- Networking: Track E2E application progress. Respond to emails.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 14: Design YouTube).
- [ ] Complete the HPA configuration exercise.
- [ ] Trigger HPA scaling in Minikube.
- [ ] Complete LeetCode #986 and #253.

---

## Day 68 — Random Selection, Event Sourcing, and Platform Polish

### DSA Block (2.5 hrs)
- Problem 1: Insert Delete GetRandom O(1) — LeetCode #380 — Pattern: HashMap + ArrayList
  - Hint: HashMap stores `value -> index`. ArrayList stores `values`. To delete in O(1), swap the element to delete with the last element in the ArrayList, update the map, and remove the last element.
  - Complexity: Time O(1) | Space O(n)
- Problem 2: Linked List Random Node — LeetCode #382 — Pattern: Reservoir Sampling
  - Hint: As you iterate the list, replace the chosen value with the current node's value with probability `1/i`.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Advanced Architecture Patterns
- Subtopics covered today: Event Sourcing and CQRS (Command Query Responsibility Segregation). How Event Sourcing differs from traditional CRUD.
- Coding exercise: Write a short design doc explaining how CQRS could optimize the Product Catalog search in the ecommerce platform.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Platform polish. Ensure all 4 microservices (Product, Order, Payment, Notification) have clean structured logging (e.g., logback JSON encoder) to prepare for observability integration.
- Definition of done: Logs are output in JSON format, making them parseable by ELK/Splunk.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Schedule your next Mock Interview (focus: WhatsApp or Uber design).

### Daily Deliverable
- [ ] Read *Building Microservices* (Chapter 4: Integration).
- [ ] Complete the CQRS design doc.
- [ ] Implement JSON logging in the ecommerce platform.
- [ ] Complete LeetCode #380 and #382.

---

## Day 69 (Weekend) — Mixed DSA, Mock Interview, and Review

### DSA Block (3.5 hrs)
- Problem 1: Trapping Rain Water — LeetCode #42 — Pattern: Two Pointers (Revision)
  - Hint: Solve again under time pressure (15 minutes).
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Sliding Window Maximum — LeetCode #239 — Pattern: Monotonic Deque (Revision)
  - Hint: Implement without looking at past solutions.
  - Complexity: Time O(n) | Space O(k)
- Problem 3: Basic Calculator II — LeetCode #227 — Pattern: Stack
  - Hint: Keep a variable for the `lastSign`. If `+` or `-`, push to stack. If `*` or `/`, pop, calculate, and push back. Sum the stack at the end.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (1.5 hrs)
- Topic: Mock Interview Prep
- Subtopics covered today: Reviewing Uber and Netflix HLDs. Database sharding strategies.
- Coding exercise: None.

### Project Block (1.5 hrs)
- Mock Interview: 60-minute System Design Mock Interview focusing on a high-throughput read-heavy system (e.g., Netflix Feed or Twitter Timeline).
- Definition of done: Complete the mock, gather feedback on High-Level Design articulation and bottleneck identification.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Send a weekend update to your accountability partner.

### Daily Deliverable
- [ ] Read *Building Microservices* (Chapter 5: Splitting the Monolith).
- [ ] Complete the System Design Mock Interview.
- [ ] Complete LeetCode #42, #239, and #227.
- [ ] Committed to GitHub.

---

## Day 70 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate Bit Manipulation and HPA.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post (e.g., Netflix on Chaos Engineering).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 10. You should be seeing solid results from your CI/CD and K8s practices.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
