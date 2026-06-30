# Week 8: DP on Trees, Design Patterns, and Advanced K8s

## Day 50 — DP on Trees, Design Patterns Start, and K8s StatefulSets

### DSA Block (2.5 hrs)
- Problem 1: House Robber III — LeetCode #337 — Pattern: DP on Trees
  - Hint: A node returns two values: max money if robbed, and max money if NOT robbed. If robbed, children cannot be robbed. If not robbed, children CAN be robbed (take max of their robbed/not robbed states).
  - Complexity: Time O(n) | Space O(n)
- Problem 2: Binary Tree Maximum Path Sum — LeetCode #124 — Pattern: DFS / DP on Trees
  - Hint: At each node, calculate the max path sum that extends to its parent, while simultaneously updating a global max for paths that curve *through* the node.
  - Complexity: Time O(n) | Space O(n)

### Theory Block (2 hrs)
- Topic: GoF Design Patterns & Kubernetes StatefulSets
- Subtopics covered today: Creational patterns (Singleton, Factory Method, Builder). Why StatefulSets are required for databases in K8s instead of Deployments (stable network identity, persistent storage).
- Coding exercise: Write a thread-safe Singleton in Java using the Double-Checked Locking pattern, then rewrite it using the Enum Singleton pattern (Effective Java approach).

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Initialize the Low-Level Design repository. Create a `design-patterns` module and implement the Factory Method and Builder patterns comprehensively with unit tests.
- Definition of done: The LLD repository is initialized and the structural foundation for studying patterns is established.

### Career Block (1 hr)
- LinkedIn: Post 15 — Month 2 Recap (publish at 8 AM IST).
- Networking: Reply to any recruiter inbound messages. Continue applying to Tier B.

### Daily Deliverable
- [ ] Read *Head First Design Patterns* (Chapter 1: Strategy Pattern).
- [ ] Complete the Singleton pattern exercise.
- [ ] Initialize `lld-java`.
- [ ] Complete LeetCode #337 and #124.

---

## Day 51 — State Machine DP, Structural Patterns, and K8s Services

### DSA Block (2.5 hrs)
- Problem 1: Best Time to Buy and Sell Stock with Cooldown — LeetCode #309 — Pattern: State Machine DP
  - Hint: Maintain three states: `hold`, `sold`, and `rest`. Draw the state transition diagram before coding.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Best Time to Buy and Sell Stock with Transaction Fee — LeetCode #714 — Pattern: State Machine DP
  - Hint: Only two states needed: `hold` and `cash`. Subtract the fee when transitioning from `hold` to `cash` (selling).
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Structural Patterns & Kubernetes Networking
- Subtopics covered today: Structural patterns (Adapter, Decorator, Facade). K8s Service types (ClusterIP, NodePort, LoadBalancer).
- Coding exercise: Implement the Decorator pattern to calculate the cost of a coffee (Base: Espresso. Decorators: Milk, Caramel, Whip).

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the Strategy and Decorator patterns in the `design-patterns` module. Add README documentation explaining when to prefer Strategy (changing algorithms) over Decorator (adding behaviors).
- Definition of done: Code is clean, documented, and tested.

### Career Block (1 hr)
- **LinkedIn Newsletter Launch (not a blog post):** Create and launch your
  LinkedIn newsletter. Title: "120 Days to SDE-2 — Weekly Technical Insights."
  Write the first newsletter issue: "Week 8 Summary — Design Patterns That
  Changed How I Code." This is distinct from your technical blog on Hashnode.
  The newsletter is a LinkedIn-specific feature that emails all subscribers.
  Do NOT count this as a numbered blog post. Your technical blog count remains
  at 2 after this day.

### Daily Deliverable
- [ ] Read *Head First Design Patterns* (Chapter 3: Decorator Pattern).
- [ ] Complete the Coffee Decorator exercise.
- [ ] Add Strategy and Decorator to `lld-java`.
- [ ] Complete LeetCode #309 and #714.

---

## Day 52 — Advanced DSA Start, Behavioral Patterns, and DaemonSets

### DSA Block (2.5 hrs)
- Problem 1: LRU Cache — LeetCode #146 — Pattern: Custom Data Structure (Revision)
  - Hint: Code it from scratch in under 15 minutes. This is a baseline fluency check.
  - Complexity: Time O(1) all ops | Space O(capacity)
- Problem 2: LFU Cache — LeetCode #460 — Pattern: Advanced Custom DS (HashMap + DLLs)
  - Hint: Use two HashMaps. One maps `key -> Node`. The other maps `frequency -> DoublyLinkedList`. Keep track of the `minFrequency`.
  - Complexity: Time O(1) all ops | Space O(capacity)

### Theory Block (2 hrs)
- Topic: Behavioral Patterns & Kubernetes DaemonSets
- Subtopics covered today: Behavioral patterns (Observer, Command, State). DaemonSets in K8s (ensuring exactly one pod runs on every node, used for logging/monitoring agents).
- Coding exercise: Implement the Observer pattern (e.g., a Weather Station pushing updates to multiple Display screens).

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Apply TDD (Test-Driven Development) retrospectively. Write failing tests for the Observer pattern implementation, then write the code to make them pass. Add the Observer and Command patterns to the repo.
- Definition of done: TDD cycle (Red-Green-Refactor) is successfully practiced and documented.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Schedule a Mock Interview focused purely on LLD patterns for this weekend.

### Daily Deliverable
- [ ] Read *Head First Design Patterns* (Chapter 2: Observer Pattern).
- [ ] Complete the Observer pattern exercise.
- [ ] Complete TDD practice in `lld-java`.
- [ ] Complete LeetCode #146 and #460.

---

## Day 53 — Tries Advanced, ConfigMaps/Secrets, and Strategy Pattern

### DSA Block (2.5 hrs)
- Problem 1: Implement Trie II (Prefix Tree) — LeetCode #1804 (Premium) or Design Search Autocomplete System (#642) — Pattern: Advanced Trie
  - Hint: Instead of just `isEndOfWord`, store counts (`wordsStartingWith`, `wordsEndingHere`) in the TrieNode.
  - Complexity: Time O(m) per op | Space O(n×m)
- Problem 2: Design Add and Search Words Data Structure — LeetCode #211 — Pattern: Trie + DFS (Revision)
  - Hint: Solve it again, aiming for 100% bug-free execution on the first run.
  - Complexity: Time O(m) search | Space O(n×m)

### Theory Block (2 hrs)
- Topic: Kubernetes Config & Real-World Strategy
- Subtopics covered today: K8s ConfigMaps and Secrets. How to inject them as environment variables or volume mounts. Decoupling configuration from images.
- Coding exercise: Write a K8s `secret.yaml` (Base64 encoded) and a `deployment.yaml` that injects the secret as a `DB_PASSWORD` environment variable.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Implement the State pattern (e.g., Vending Machine states: HasCoin, NoCoin, Dispensing, SoldOut).
- Definition of done: The State pattern is fully implemented without giant `if-else` or `switch` blocks in the core context class.

### Career Block (1 hr)
- LinkedIn: Post 16 — Poll on Study Focus (publish at 6 PM IST).
- Networking: Continue outreach and follow up. 

### Daily Deliverable
- [ ] Read *Clean Code* (Chapter 1: Clean Code).
- [ ] Complete the K8s Secret injection exercise.
- [ ] Add State pattern to `lld-java`.
- [ ] Complete LeetCode #1804 (or #642) and #211.

---

## Day 54 — Disjoint Set Union (Union-Find) and LLD Practice

### DSA Block (2.5 hrs)
- Problem 1: Redundant Connection — LeetCode #684 — Pattern: Union-Find
  - Hint: If two nodes of an edge are already in the same set, that edge creates a cycle.
  - Complexity: Time O(n×α(n)) | Space O(n)
- Problem 2: Number of Provinces — LeetCode #547 — Pattern: Union-Find / DFS
  - Hint: Start with N sets. Iterate through the matrix, and union the sets. The answer is the number of sets remaining.
  - Complexity: Time O(n²) | Space O(n)

### Theory Block (2 hrs)
- Topic: Union-Find Optimization & LLD Approach
- Subtopics covered today: Path Compression and Union by Rank (makes Union-Find almost O(1) amortized). How to approach an LLD interview (Requirements, Core Objects, Class Diagram, Code).
- Coding exercise: Write a robust `UnionFind` class template in Java with `find()` (with path compression) and `union()` (by rank). Save this template.

### Project Block (1.5 hrs)
- Repository: `lld-java`
- Task: Prepare for the LLD Mock Interview. Review the Parking Lot LLD requirements and sketch a quick class diagram (no code yet).
- Definition of done: You have a mental model of the Vehicle, ParkingSpot, and ParkingLot classes.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Confirm time for the Mock Interview.

### Daily Deliverable
- [ ] Read *Clean Code* (Chapter 2: Meaningful Names).
- [ ] Complete the robust `UnionFind` template.
- [ ] Complete Parking Lot LLD sketch.
- [ ] Complete LeetCode #684 and #547.

---

## Day 55 (Weekend) — Advanced Graphs, Mock Interview, and Review

### DSA Block (3.5 hrs)
- Problem 1: Accounts Merge — LeetCode #721 — Pattern: Union-Find + HashMap
  - Hint: Map every email to an ID. Union the IDs of emails belonging to the same account. Then group emails by their set's root ID.
  - Complexity: Time O(n×k×α) | Space O(n×k)
- Problem 2: Minimum Spanning Tree (Kruskal's Algorithm concepts) — Premium/HackerRank
  - Hint: Sort edges by weight. Iterate and use Union-Find to add edges that don't create cycles.
- Problem 3: Evaluate Division — LeetCode #399 — Pattern: DFS/Union-Find (Revision)
  - Hint: Attempt the Union-Find approach for this problem (it requires maintaining weights during `find`).
  - Complexity: Time O((V+E)×Q) | Space O(V+E)

### Theory Block (1.5 hrs)
- Topic: Month 2 Review & LLD Synthesis
- Subtopics covered today: Reviewing DP, Graph algorithms, Kubernetes, and Design Patterns.
- Coding exercise: None today. Prepare for the mock.

### Project Block (1.5 hrs)
- Mock Interview: 60-minute LLD Mock Interview focusing on applying design patterns to a real problem (e.g., Vending Machine or Parking Lot).
- Definition of done: Receive feedback from your accountability partner. Note weak spots in class structure or pattern application.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Reflect on the mock interview feedback. 

### Daily Deliverable
- [ ] Read *Clean Code* (Chapter 3: Functions).
- [ ] Complete the LLD Mock Interview.
- [ ] Complete LeetCode #721, MST basics, and #399.
- [ ] Committed to GitHub.

---

## Day 56 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Strictly no LeetCode. Month 2 Intermediate is complete.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate advanced DSA and Design Patterns.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read an engineering blog post (e.g., Atlassian engineering).
  - Scan Hacker News.
- **Weekly Scorecard:** Fill out the scorecard for Week 8.
- **Month 2 Review:** Assess your readiness. Month 3 focuses entirely on advanced topics, System Design, and the massive E-Commerce project. Are your fundamentals solid?

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
