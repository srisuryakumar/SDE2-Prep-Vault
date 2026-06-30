# Week 2: OOP Mastery, Collections, and Linked Lists

## Day 8 — Grasping OOP Core Pillars and Linked List Dummy Heads.

### DSA Block (2.5 hrs)
- Problem 1: Reverse Linked List — LeetCode #206 — Pattern: Iterative Pointer Reversal
  - Hint: Keep three pointers: `prev`, `curr`, and `next`. Before pointing `curr.next` to `prev`, save the original `curr.next` in `next`.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Merge Two Sorted Lists — LeetCode #21 — Pattern: Two Pointers with Dummy Head
  - Hint: Create a `ListNode dummy = new ListNode(-1)` to anchor the start of the merged list. This saves you from writing edge cases for an initially null list.
  - Complexity: Time O(m+n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Java Object-Oriented Programming (OOP)
- Subtopics covered today: The 4 Pillars (Encapsulation, Inheritance, Polymorphism, Abstraction), interfaces vs abstract classes, and the power of `enum` (which compile to classes with private constructors).
- Coding exercise: Write an `enum AccountType { SAVINGS, CHECKING }` with a custom `calculateInterest()` abstract method implemented differently by each constant, proving enums can hold logic, not just strings.

### Project Block (1.5 hrs)
- Repository: `java-fundamentals`
- Task: Build an `Account` class hierarchy utilizing inheritance, encapsulation, and the `AccountType` enum. 
- Definition of done: The hierarchy cannot be instantiated via an abstract base class, and instance fields are strictly private with getters/setters demonstrating encapsulation. Code compiles and is pushed.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting meaningfully on 3-5 posts from your target company list.
- Networking: Identify 5 Technical Recruiters at Tier B companies (e.g., Meesho, Swiggy) using LinkedIn search.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 1: Consider static factory methods).
- [ ] Complete the Enum logic coding exercise.
- [ ] Complete LeetCode #206 and #21.
- [ ] Committed to GitHub (`java-fundamentals` and `dsa-java`).

---

## Day 9 — Floyd's Cycle Detection and SOLID Principles.

### DSA Block (2.5 hrs)
- Problem 1: Middle of the Linked List — LeetCode #876 — Pattern: Fast/Slow Pointers
  - Hint: `fast` moves two steps, `slow` moves one step. When `fast` reaches the end, `slow` is exactly at the middle.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Linked List Cycle — LeetCode #141 — Pattern: Floyd's Cycle Detection (Tortoise & Hare)
  - Hint: If there is a cycle, the `fast` pointer will eventually "lap" and equal the `slow` pointer.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Java OOP
- Subtopics covered today: SOLID Principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion).
- Coding exercise: Write a `NotificationService` that violates Dependency Inversion by instantiating an `EmailSender` directly. Then refactor it to accept a `MessageSender` interface via constructor injection.

### Project Block (1.5 hrs)
- Repository: `java-fundamentals`
- Task: Apply SOLID to yesterday's `Account` hierarchy. Extract a `TaxCalculator` interface to satisfy the Single Responsibility and Strategy patterns.
- Definition of done: The refactored code clearly separates the core account state from the tax calculation logic, allowing new tax rules to be added without modifying `Account`.

### Career Block (1 hr)
- LinkedIn: Post 3 — JVM Memory Model Diagram (publish at 8 AM IST).
- Networking: Send the 5 connection requests identified yesterday using Template 2 (Technical Recruiters).

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 2: Consider a builder).
- [ ] Complete the SOLID refactoring exercise.
- [ ] Complete LeetCode #876 and #141.
- [ ] Committed to GitHub.

---

## Day 10 — Advanced Arrays and Modern Java OOP.

### DSA Block (2.5 hrs)
- Problem 1: 3Sum Closest — LeetCode #16 — Pattern: Sorting + Two Pointers
  - Hint: Sort the array. Iterate through the array and use two pointers for the remaining elements, tracking the minimum absolute difference between the current sum and the target.
  - Complexity: Time O(n²) | Space O(1)
- Problem 2: Trapping Rain Water — LeetCode #42 — Pattern: Two Pointers (Opposite Ends)
  - Hint: Use two pointers starting from both ends. Maintain left and right maximum heights. Always process the side with the smaller maximum height to compute trapped water accurately.
  - Complexity: Time O(n) | Space O(1)

### Theory Block (2 hrs)
- Topic: Modern Java OOP
- Subtopics covered today: Java 14+ Records (shallow immutability), Java 15+ Sealed Classes (restricted inheritance hierarchies), and Switch Pattern Matching.
- Coding exercise: Create a `sealed interface PaymentState permits Pending, Success, Failed`. Implement them as `record`s. Write a modern `switch` expression that returns a status string based on pattern matching the exact instance type.

### Project Block (1.5 hrs)
- Repository: `java-fundamentals`
- Task: Create a `ModernJava` package. Implement the state machine using the Sealed Interface and Records from the coding exercise.
- Definition of done: The code compiles on Java 17+, relies strictly on `record` syntax (no boilerplate getters), and demonstrates exhaustiveness in the `switch` statement without a `default` branch.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Identify 3 Engineering Managers at Tier A companies (Razorpay, Uber).

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 15: Minimize mutability).
- [ ] Complete the Sealed Class/Record state machine code.
- [ ] Complete LeetCode #16 and #42.
- [ ] Committed to GitHub.

---

## Day 11 — Linked List Math and Linear Collections Internals.

### DSA Block (2.5 hrs)
- Problem 1: Remove Nth Node From End of List — LeetCode #19 — Pattern: Two Pointers (Fixed Offset)
  - Hint: Use a dummy head. Advance the `fast` pointer `n+1` steps ahead, then move both `fast` and `slow` until `fast` hits null. `slow.next` is the target to drop.
  - Complexity: Time O(n) | Space O(1)
- Problem 2: Add Two Numbers — LeetCode #2 — Pattern: Math Simulation on Linked List
  - Hint: Traverse both lists simultaneously. Keep track of a `carry` variable. `sum = val1 + val2 + carry`.
  - Complexity: Time O(max(m,n)) | Space O(max(m,n))

### Theory Block (2 hrs)
- Topic: Java Collections Framework
- Subtopics covered today: `ArrayList` internals (resizing logic, cache locality), `LinkedList` overhead, and `ArrayDeque` (why it destroys `LinkedList` for Stacks and Queues).
- Coding exercise: Write a JMH (or simple `System.nanoTime()`) benchmark inserting 100,000 elements at index 0 of an `ArrayList` versus an `ArrayDeque`.

### Project Block (1.5 hrs)
- Repository: `java-fundamentals`
- Task: Add the `CollectionsBenchmark` class. Include comments explaining why the `ArrayList` requires `O(N)` memory shifting on front-insertion, while `ArrayDeque` is `O(1)` amortized using a circular array.
- Definition of done: The benchmark runs, the results are printed, and the code is pushed.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Send connection requests to the 3 EMs using Template 3 (Vision-Level).

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 17: Design and document for inheritance or else prohibit it).
- [ ] Complete the `ArrayList` vs `ArrayDeque` benchmark.
- [ ] Complete LeetCode #19 and #2.
- [ ] Committed to GitHub.

---

## Day 12 — HashMap Internals, LRU Cache, and Exceptions.

### DSA Block (2.5 hrs)
- Problem 1: Copy List with Random Pointer — LeetCode #138 — Pattern: HashMap for Deep Copy / Node Mapping
  - Hint: Pass 1: Map old nodes to new nodes in a `HashMap<Node, Node>`. Pass 2: Connect the `next` and `random` pointers of the new nodes using the map.
  - Complexity: Time O(n) | Space O(n)
- Problem 2: LRU Cache — LeetCode #146 — Pattern: HashMap + Doubly Linked List
  - Hint: A HashMap gives `O(1)` lookups. A Doubly Linked List gives `O(1)` removals and additions. Combine them by storing DLL nodes as map values.
  - Complexity: Time O(1) all ops | Space O(capacity)

### Theory Block (2 hrs)
- Topic: Collections Framework & Exception Handling
- Subtopics covered today: `HashMap` internals (Bucket array, hash shifting, treeification threshold). Checked vs Unchecked Exceptions, `try-with-resources`, and the anti-pattern of swallowing exceptions in `finally`.
- Coding exercise: Create a custom `CacheMissException` (unchecked). Write a wrapper method that throws it. Write a `try-with-resources` block simulating a file read that uses standard exception logging.

### Project Block (1.5 hrs)
- Repository: `java-fundamentals`
- Task: Implement the LRU Cache algorithm from scratch using your own generic `<K,V>` DLL nodes and a standard HashMap. Do NOT use `LinkedHashMap`. Throw your `CacheMissException` on missing keys.
- Definition of done: The custom cache implementation is fully tested locally and pushed.

### Career Block (1 hr)
- LinkedIn: Post 4 — Race Condition Proof (publish at 6 PM IST).
- Networking: Follow up on any recruiter messages from Tuesday.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 69: Use exceptions only for exceptional conditions).
- [ ] Complete the custom Exception and LRU cache implementations.
- [ ] Complete LeetCode #138 and #146.
- [ ] Committed to GitHub.

---

## Day 13 (Weekend) — PriorityQueues, TreeMaps, and Custom Sorting.

### DSA Block (3.5 hrs)
- Problem 1: Kth Largest Element in an Array — LeetCode #215 — Pattern: Min-Heap
  - Hint: Maintain a `PriorityQueue` of size `k`. When size exceeds `k`, poll the smallest element. The top of the heap is the answer.
  - Complexity: Time O(n log k) | Space O(k)
- Problem 2: Top K Frequent Elements — LeetCode #347 — Pattern: HashMap + Min-Heap / Bucket Sort
  - Hint: Count frequencies in a map. Add to a `PriorityQueue` ordered by frequency.
  - Complexity: Time O(n log k) | Space O(n)
- Problem 3: Merge k Sorted Lists — LeetCode #23 — Pattern: PriorityQueue with Custom Comparator
  - Hint: Insert the head of each list into a Min-Heap. Poll the smallest node, append it to your result, and push its `next` node back into the heap.
  - Complexity: Time O(n log k) | Space O(log k)

### Theory Block (1.5 hrs)
- Topic: Tree-based Collections and Sorting
- Subtopics covered today: `TreeMap` (Red-Black tree properties, `O(log N)` complexity) vs `PriorityQueue` (Min/Max Heap, `O(log N)` insert/poll, `O(1)` peek). `Comparable` interface vs `Comparator` functional interface.
- Coding exercise: Write a `Record` representing a `Transaction` (id, amount, timestamp). Sort a List of transactions by amount using `Collections.sort` with a lambda `Comparator`, then sort by timestamp reversed.

### Project Block (1.5 hrs)
- Repository: `dsa-java`
- Task: Review and structure all Linked List and Heap problems from Week 2. Ensure every file has the time/space complexity explicitly written at the top.
- Definition of done: The repository is clean, categorized into `/LinkedList` and `/Heaps`, and fully pushed.

### Career Block (1 hr)
- LinkedIn: Engagement target — 20 minutes commenting on 3-5 posts.
- Networking: Reach out to 1 former coworker or college peer just to catch up.

### Daily Deliverable
- [ ] Read *Effective Java* (20 min — Item 14: Consider implementing Comparable).
- [ ] Complete the `Comparator` sorting exercise.
- [ ] Complete LeetCode #215, #347, and #23.
- [ ] Committed to GitHub.

---

## Day 14 (Sunday) — Reflection, Networking, and Rest.

### DSA Block (0 hrs)
- Sunday is a strictly no-code, no-LeetCode day. Brain recovery is mandatory.

### Theory Block (0 hrs)
- Rest day. Let the brain consolidate the week's OOP and Collections learnings.

### Project Block (0 hrs)
- No repository tasks today.

### Career Block (1.5 hrs)
- **Weekly Industry Awareness Ritual (30 min):**
  - Read TLDR Newsletter backlog.
  - Read one engineering blog post (e.g., from Uber Engineering on Geospatial tracking).
  - Scan Hacker News "Ask HN" / "Show HN".
  - Log findings in the study journal.
- **Weekly Scorecard:** Fill out the scorecard for Week 2 in your tracking sheet. Assess whether you are hitting the `<25 min` target for Medium DSA problems.

### Daily Deliverable
- [ ] Complete the Weekly Industry Awareness Ritual.
- [ ] Complete the Weekly Scorecard.
- [ ] Take a full day away from the IDE.
