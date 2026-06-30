# Week 9: Segment Trees, LLD Implementations, and System Design Start

## Day 57 — Segment Trees, Parking Lot LLD, and Microservices Init

### DSA Block (2.5 hrs)
- Problem 1: Range Sum Query - Mutable — LeetCode #307 — Pattern: Segment Tree
  - Hint: Build a tree where each node stores the sum of a range. Updating a leaf takes `O(log N)` as you bubble the sum up to the root.
  - Complexity: Time O(log n) | Space O(n)
- Problem 2: Count of Smaller Numbers After Self — LeetCode #315 — Pattern: Segment Tree / Fenwick Tree
  - Hint: Traverse the array from right to left. Insert the element into a Segment/Fenwick tree and query the count of elements smaller than it.
  - Complexity: Time O(n log n) | Space O(n)

### Theory Block (2 hrs)
- Topic: System Design Framework & Microservices
- Subtopics covered today: The 5-Step System Design Framework (Requirements, Estimation, High-Level Design, Detailed Design, Bottlenecks). Principles of Microservices (Domain-Driven Design, Bounded Contexts).
- Coding exercise: Read through the 5-Step framework in your notes. Outline the High-Level Design for a URL Shortener.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform` and `lld-java`
- Task: Initialize `scalable-ecommerce-platform` with a multi-module Maven setup (Product, Order, Payment). In `lld-java`, implement the **Parking Lot LLD** from your weekend sketch, ensuring thread-safety on the `assignSpot` method.
- Definition of done: Maven modules are created. Parking Lot implementation compiles with unit tests.

### Additional Day 57 Task: Add Feign Client for Service-to-Service Communication
- In the Order Service pom.xml, add: `spring-cloud-starter-openfeign`
- Add @EnableFeignClients to the main application class
- Create ProductServiceClient interface:
  ```java
  @FeignClient(name = "product-service",
               fallback = ProductServiceFallback.class)
  public interface ProductServiceClient {

      @GetMapping("/api/v1/products/{id}")
      ProductDTO getProduct(@PathVariable Long id);

      @PostMapping("/api/v1/products/{id}/reserve")
      void reserveStock(@PathVariable Long id, @RequestParam int quantity);
  }

  @Component
  public class ProductServiceFallback implements ProductServiceClient {
      public ProductDTO getProduct(Long id) {
          return ProductDTO.placeholder(id); // cached/default response
      }
      public void reserveStock(Long id, int quantity) {
          log.warn("Product service unavailable. Queuing stock reservation via Kafka.");
      }
  }
  ```
- Definition of done: The Order Service can call the Product Service through
  Feign with zero HTTP boilerplate. The fallback handles Product Service
  unavailability gracefully.
- Interview answer: "How do microservices call each other in your platform?"
  → "Synchronous calls use Feign Client — declarative HTTP, similar to
  Spring Data repositories. It integrates with Resilience4j for circuit
  breaking and with Eureka/K8s for load balancing. Async calls use Kafka."

### Career Block (1 hr)
- LinkedIn: Post 17 — WhatsApp Architecture Breakdown (publish at 8 AM IST).
- Networking: Target Tier A SDE-2s on LinkedIn. Send 5 connection requests.

### Daily Deliverable
- [ ] Read *Clean Code* (Chapter 4: Comments).
- [ ] Complete the URL Shortener HLD sketch.
- [ ] Implement Parking Lot LLD.
- [ ] Complete LeetCode #307 and #315.

---

## Day 58 — String Algorithms, URL Shortener, and API Gateways

### DSA Block (2.5 hrs)
- Problem 1: Longest Substring Without Repeating Characters — LeetCode #3 — Pattern: Sliding Window (Revision)
  - Hint: Execute under 10 minutes. Use a `HashSet` or `int[]` array for character mapping.
  - Complexity: Time O(n) | Space O(min(m,n))
- Problem 2: Find All Anagrams in a String — LeetCode #438 — Pattern: Sliding Window + HashMap
  - Hint: Maintain a sliding window of size `p.length()`. Compare frequency maps (or arrays).
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: System Design — URL Shortener & API Gateways
- Subtopics covered today: URL Shortener detailed design (Base62 encoding, Hash collisions, Key Generation Service). Spring Cloud Gateway vs Kong.
- Coding exercise: Write a simple Base62 encoder/decoder in Java.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Set up Spring Cloud Gateway as the entry point for your microservices. Configure routes in `application.yml` to forward `/products/**` to the Product service.
- Definition of done: Hitting the Gateway routes the request to the underlying microservice correctly.

### Career Block (1 hr)
- Technical Blog: Write and publish Blog Post 3 (Topic: "System Design: The 5-Step Framework" or "Microservices API Gateway setup").
- LinkedIn: Share your blog post.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 1: Scale From Zero to Millions).
- [ ] Complete the Base62 Encoder exercise.
- [ ] Implement API Gateway.
- [ ] Complete LeetCode #3 and #438.

---

## Day 59 — KMP Algorithm, Vending Machine LLD, and Rate Limiter

### DSA Block (2.5 hrs)
- Problem 1: Implement strStr() — LeetCode #28 — Pattern: String Matching (KMP)
  - Hint: Learn the KMP algorithm. Build the LPS (Longest Prefix Suffix) array first. `O(N + M)` time.
  - Complexity: Time O(n+m) | Space O(m)
- Problem 2: Repeated Substring Pattern — LeetCode #459 — Pattern: KMP / String Manipulation
  - Hint: If a string is composed of a repeated substring, `(s + s).substring(1, 2*s.length() - 1)` will contain `s`.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: System Design — Rate Limiter & Token Buckets
- Subtopics covered today: Token Bucket, Leaking Bucket, Fixed Window, Sliding Window Log. Rate limiting in a distributed environment (Redis Lua scripts).
- Coding exercise: Implement a basic Token Bucket algorithm locally in Java.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform` and `lld-java`
- Task: In `lld-java`, implement the **Vending Machine LLD** using the State Design Pattern. In `scalable-ecommerce-platform`, apply a Request Rate Limiter filter in your Spring Cloud Gateway using Redis.
- Definition of done: Vending Machine code compiles. The Gateway returns HTTP 429 Too Many Requests when limits are exceeded.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Track application responses. Reach out to internal recruiters for roles you applied to last week.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 4: Design a Rate Limiter).
- [ ] Complete the Token Bucket exercise.
- [ ] Implement Vending Machine LLD.
- [ ] Complete LeetCode #28 and #459.

---

## Day 60 — Rabin-Karp, Notification System, and Service Registry

### DSA Block (2.5 hrs)
- Problem 1: Longest Duplicate Substring — LeetCode #1044 — Pattern: Rabin-Karp + Binary Search
  - Hint: Binary search for the length of the substring. Use a rolling hash (Rabin-Karp) to check if a substring of that length appears twice.
  - Complexity: Time O(n log n) | Space O(n)
- Problem 2: Repeated DNA Sequences — LeetCode #187 — Pattern: Rolling Hash / HashSet
  - Hint: Use a HashSet to track seen 10-letter sequences. A rolling hash optimizes the window sliding.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: System Design — Notification System
- Subtopics covered today: Designing a Notification System (Push, Email, SMS). Deduplication using Redis. Retry queues (DLQ). Priority messaging.
- Coding exercise: Design the database schema for the Notification System tracking user preferences and message status.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Add a Eureka Service Registry (or use Kubernetes native DNS). Register the Product and Order services so they can discover each other without hardcoded IPs.
- Definition of done: The Eureka dashboard displays the registered services, or K8s CoreDNS routes internal `.svc.cluster.local` traffic successfully.

### Career Block (1 hr)
- LinkedIn: Post 18 — LLD Parking Lot (publish at 6 PM IST).
- Networking: **Day 60 Milestone.** You are now ready to apply to Tier A companies. Submit 3 Tier A applications today.
- **Day 60 Open Source Check-in:** Follow up on the PR you opened on Day 30.
  If it was merged: find a second issue, slightly harder this time.
  If it's still open: respond to reviewer comments and push an update.
  A PR in "Changes Requested" state that you actively respond to is better
  than no PR at all — maintainers notice responsiveness.
  If you haven't opened the Day 30 PR yet: do it today before the
  applications. GitHub contribution graph has a 30-day lag where this
  still helps.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 10: Design a Notification System).
- [ ] Complete the Notification DB schema exercise.
- [ ] Implement Service Registry.
- [ ] Complete LeetCode #1044 and #187.

---

## Day 61 — Trie Revision, BookMyShow System Design, and JWT

### DSA Block (2.5 hrs)
- Problem 1: Palindrome Pairs — LeetCode #336 — Pattern: Trie
  - Hint: Insert all reversed words into a Trie. For each word, check if a prefix exists in the Trie and the rest of the word is a palindrome.
  - Complexity: Time O(n×k²) | Space O(n×k)
- Problem 2: Maximum XOR of Two Numbers in an Array — LeetCode #421 — Pattern: Bit Trie
  - Hint: Insert binary representations into a Trie. To maximize XOR, always try to traverse the opposite bit path.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: System Design — BookMyShow (Ticket Booking)
- Subtopics covered today: Handling high concurrency for seat selection. Database locks (`SELECT FOR UPDATE`). Redis distributed locks.
- Coding exercise: Draw the sequence diagram for a user booking a seat, highlighting the locking mechanism.

### Project Block (1.5 hrs)
- Repository: `scalable-ecommerce-platform`
- Task: Implement JWT Authentication at the API Gateway level. Validate the token before routing to microservices.
- Definition of done: Requests without a valid Bearer token are rejected by the Gateway with HTTP 401 Unauthorized.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Connect with SDE-2s at the Tier A companies you applied to yesterday.

### Daily Deliverable
- [ ] Read *System Design Interview Vol 1* (Chapter 12: Design a Chat System - Prep).
- [ ] Complete the BookMyShow sequence diagram.
- [ ] Implement JWT at the Gateway.
- [ ] Complete LeetCode #336 and #421.

---

## Day 62 (Weekend) — String Hard Problems, Mock Interview, and K8s Refine

### DSA Block (3.5 hrs)
- Problem 1: Minimum Window Substring — LeetCode #76 — Pattern: Sliding Window (Hard)
  - Hint: Expand the right pointer until the window has all required characters. Then shrink the left pointer to minimize the window while remaining valid.
  - Complexity: Time O(n+m) | Space O(n+m)
- Problem 2: Sliding Window Maximum — LeetCode #239 — Pattern: Monotonic Deque
  - Hint: Maintain a deque of indices. Ensure elements in the deque are in decreasing order of their values. Remove elements outside the window.
  - Complexity: Time O(n) | Space O(k)
- Problem 3: Wildcard Matching — LeetCode #44 — Pattern: 2D DP
  - Hint: `dp[i][j]` is true if `s[0..i]` matches `p[0..j]`. Handle the `*` character carefully (it can match empty or extend previous match).
  - Complexity: Time O(m×n) | Space O(m×n)

### Theory Block (1.5 hrs)
- Topic: System Design Mock Preparation
- Subtopics covered today: Reviewing Rate Limiter, Notification System, and URL Shortener architectures. 
- Coding exercise: Verbally walk through the URL Shortener design in 15 minutes, timing yourself.

### Project Block (1.5 hrs)
- Mock Interview: 60-minute System Design Mock Interview with your accountability partner. Design a Rate Limiter.
- Definition of done: Receive feedback. Ensure you spent at least 5 minutes on requirement gathering and 10 minutes on bottleneck analysis.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Review application tracker. Note any auto-rejections and look for referral paths.

### Daily Deliverable
- [ ] Read *Building Microservices* (Chapter 1: Microservices).
- [ ] Complete the System Design Mock Interview.
- [ ] Complete LeetCode #76, #239, and #44.
- [ ] Committed to GitHub.

---

## Day 63 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate System Design concepts.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post (e.g., WhatsApp engineering on Erlang/concurrency).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 9. Month 3 is intense; ensure burnout prevention rules are followed.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
