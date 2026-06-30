# 04 — Reading and Resources

### SECTION 1: BOOKS — WHAT EACH COVERS AND HOW TO READ THEM

**Priority 1 — Must Read (read 20 min/evening, every day)**

---

**A Mind for Numbers** by Barbara Oakley | Read: Week 1
What it covers: The neuroscience of effective learning. Explains why
cramming fails, how spaced repetition works, why sleep consolidates memory,
and how to switch between "focused" and "diffuse" thinking modes.
How to read: Cover-to-cover in Week 1. Chapters 1–4 are the most important.
Why essential: Reading this first changes how you study everything else.
Specifically, it explains why the 120-day plan has rest days, why the
study journal works, and why you should practice problems before reading
solutions. Candidates who understand how learning works prepare 30–40%
more efficiently than those who don't.

---

**Effective Java** 3rd Edition by Joshua Bloch | Read: Weeks 2–6
What it covers: 90 "items" each explaining one Java best practice with the
correct code, the wrong code, and the reasoning. Covers generics, lambdas,
collections, concurrency, serialization, and API design.
Critical items to NOT skip: Item 1 (static factories), Item 17 (immutability),
Item 69 (exceptions for exceptional conditions), Item 78–81 (concurrency),
Item 50 (defensive copies), Items 26–31 (generics).
How to read: 1–2 items per evening. Do not read straight through — absorb one
item deeply then go to sleep.
Why essential: Interviewers at companies like Atlassian and Amazon cite
Effective Java directly. "How would you design an immutable class in Java?"
"Why prefer composition over inheritance?" Every answer is in this book.

---

**Java Concurrency in Practice** by Brian Goetz | Read: Weeks 3–5
What it covers: Thread safety, sharing objects, composing objects, the Java
Memory Model, performance, and testing concurrent programs.
Critical chapters: 1 (Introduction), 2 (Thread Safety), 3 (Sharing Objects),
10 (Avoiding Liveness Hazards), 15 (Atomic Variables and Non-Blocking Synchronization).
How to read: Read alongside the concurrency theory days in the plan.
When studying synchronized on Day 18, read Chapter 2 the same evening.
Why essential: Every SDE-2 Java concurrency question traces back to this book.
"What is the Java Memory Model?" "What is a race condition?" "Why is volatile
not sufficient for atomicity?" — all answered here with the authoritative explanation.

---

**Cracking the Coding Interview** by Gayle McDowell | Read: Weeks 1–4
What it covers: Part I (The Interview Process), Part II (Behind the Scenes,
company-specific), Part III (Special Situations), Part IV–VI (Interview Questions).
How to read: Read ONLY Parts I–VI (the mindset sections) — NOT the solutions.
Skip the solution chapters. The value is in understanding what interviewers
look for, how to handle silence, how to handle wrong answers, and how companies
differ. Re-read Part II (Behind the Scenes) before applying to each company type.
Why essential: The mindset chapters change how you behave in an interview
room, which affects outcomes more than knowing one extra algorithm.

---

**Elements of Programming Interviews in Java** by Aziz, Lee, Prakash | Weeks 5–8
What it covers: 250 problems with full Java solutions, organized by data
structure. More concise than CTCI. Harder problems. Better for SDE-2 level.
How to read: Use as supplementary to NeetCode 150. When you encounter a topic
week (trees, graphs, DP), read the corresponding EPI chapter. Don't read front
to back — use it as a reference when your weekly problems feel too easy.
Why essential: EPI problems appear at companies like Google and Stripe, which
ask harder problems than typical product companies. If you target global remote
roles at Series B–C startups, EPI prepares you for the hard tier.

---

**Designing Data-Intensive Applications** by Martin Kleppmann | Weeks 6–14
What it covers: Part I (Foundations of Data Systems), Part II (Distributed Data),
Part III (Derived Data). Covers replication, partitioning, transactions, the
trouble with distributed systems, consistency, consensus.
Critical chapters: Chapter 5 (Replication), Chapter 6 (Partitioning), Chapter 7
(Transactions), Chapter 8 (The Trouble with Distributed Systems), Chapter 9
(Consistency and Consensus).
How to read: Read one chapter per week from Week 6. Do NOT try to read it fast.
Each chapter is dense. Read Chapter 5 during Kafka/replication week. Read
Chapter 7 during distributed transactions week.
Why essential: Called "DDIA" by engineers. It is the single most cited book
in distributed systems system design interviews. Every system design answer
about replication, consistency, and partitioning is in here. Companies like
PhonePe and Razorpay ask about these concepts directly.

---

**Database Internals** by Alex Petrov | Read: Week 7 (after DDIA Chapters 5–9)
What it covers: Part I (Storage Engines) covers B-Trees, immutable storage,
log-structured merge-trees (LSM-Trees). Part II (Distributed Systems) covers
consensus algorithms (Raft, Paxos), distributed transactions.
How to read: Read Part I (Chapters 1–8) only in Week 7. Part II is optional
depth for very senior roles. Focus on Chapter 2 (B-Tree Basics) and Chapter 6
(B-Tree variants).
Why essential: Deepens your understanding of WHY database indexes behave the
way they do. "How does a B-Tree index enable range queries?" becomes a
first-principles answer rather than a memorised response.

---

**Clean Code** by Robert C. Martin | Weeks 8–9
What it covers: Meaningful names, functions (small, do one thing), comments,
formatting, objects vs data structures, error handling, boundaries, unit tests,
classes, systems.
How to read: Read while doing the LLD design pattern weeks. After writing each
pattern, re-read the relevant Clean Code chapter to critique your own code.
Why essential: LLD interviews penalise messy code. "Your Parking Lot code
works, but I notice your method is 50 lines and does 3 things." Clean Code
changes how you write in the interview room.

---

**Head First Design Patterns** by Freeman & Freeman | Weeks 8–9
What it covers: All GoF patterns explained with cartoons, dialogues, and exercises.
Strategy, Observer, Decorator, Factory, Singleton, Command, Adapter, Facade,
Template Method, Iterator, Composite, State, Proxy.
How to read: Read alongside LLD phase. One chapter = one pattern. Read the
Strategy chapter on the same day you implement the Strategy LLD exercise.
Why essential: The most accessible design patterns book. Better to actually
understand 10 patterns deeply than to memorise 23 shallowly. LLD interviewers
reward candidates who can NAME the pattern and explain WHY it applies here.

---

**System Design Interview Vol 1** by Alex Xu | Weeks 9–11
What it covers: Chapter 1 (Scale from Zero to Millions), Chapter 4 (Rate Limiter),
Chapter 6 (Key-Value Store), Chapter 7 (Unique ID), Chapter 8 (URL Shortener),
Chapter 10 (Notification System), Chapter 12 (Chat System), Chapter 13 (Autocomplete),
Chapter 14 (YouTube).
How to read: Read each chapter the evening BEFORE the corresponding system design
day in the plan. Read Rate Limiter chapter before Day 59. Read Notification chapter
before Day 60. This gives you the theory the night before you practice it.
Why essential: The format of Alex Xu's explanations mirrors exactly what
interviewers want: requirements → estimation → design → deep dive → bottlenecks.
Reading this book trains your mental template to match interviewer expectations.

---

**System Design Interview Vol 2** by Alex Xu | Weeks 12+
What it covers: Proximity Service, Nearby Friends, Google Maps, Distributed Message
Queue, Metrics Monitoring, Ad Click Event Aggregation, Hotel Reservation, Distributed
Email Service, S3-like Object Storage, Real-Time Gaming Leaderboard.
How to read: Read Hotel Reservation chapter before Week 12 Day 81 (Hotel Booking LLD
day). Read Leaderboard chapter before Week 13 Day 87.

---

**Spring in Action** 6th Edition by Craig Walls | Weeks 4–6
What it covers: Part 1 (Spring foundations: MVC, REST), Part 2 (Integrated Spring:
persistence, security), Part 3 (Reactive Spring), Part 4 (Cloud-native Spring:
configuration, service discovery, Circuit Breaker).
How to read: Read Part 1 (Chapters 1–7) during Spring Boot weeks. Skip Chapter 11+
(Reactive) unless you specifically need WebFlux. Use it as a reference, not a
cover-to-cover read.
Why essential: Best practical Spring Boot book. When something in Spring behaves
unexpectedly, check Craig Walls' explanation first.

---

**Building Microservices** 2nd Edition by Sam Newman | Weeks 9–11
What it covers: How to model services, splitting the monolith, communication,
deployment, testing, security, resilience, scalability, organizational factors.
How to read: Read Chapter 1 (Microservices), Chapter 4 (Integration), Chapter 5
(Splitting the Monolith) during the E-Commerce platform build weeks.
Why essential: The scalable-ecommerce-platform's architectural decisions (why 4
services, why Kafka between them, why API Gateway) become much clearer with Sam
Newman's reasoning. You can then JUSTIFY those decisions in interviews.

---

**The Pragmatic Programmer** by Hunt & Thomas | Week 13
What it covers: Career philosophy, software craftsmanship, pragmatic approaches
to problems, team dynamics, project management. Classic software engineering wisdom.
How to read: Read during interview season. One chapter per day. It reinforces
the engineering mindset interviewers want to see at SDE-2 level.

---

### SECTION 2: DSA CHEAT SHEETS — EXACT RESOURCES WITH DESCRIPTIONS

**Resource 1: NeetCode 150 (neetcode.io/practice)**
What it contains: 150 curated LeetCode problems organized into 17 categories
(Arrays, Two Pointers, Sliding Window, Stack, Binary Search, Linked List, Trees,
Tries, Heap, Backtracking, Graphs, Advanced Graphs, 1D DP, 2D DP, Greedy,
Intervals, Math & Geometry, Bit Manipulation).
Why to use it: The problems are the best quality-to-effort ratio of any DSA
resource. All 150 have free video explanations. The organization by pattern (not
difficulty) trains pattern recognition, which is the actual interview skill.
How to use in this plan: Your plan targets NeetCode 150 completion by Day 80.
Bookmark neetcode.io/practice on Day 1. Track your completion there.
Session length: Solve 2–3 problems, then watch the explanation video ONLY if
you cannot solve it within 25 minutes. Never watch before attempting.

---

**Resource 2: Blind 75 (leetcode.com/discuss/general-discussion/460599)**
What it contains: 75 curated problems considered the minimum set to prepare for
FAANG. Subset of NeetCode 150. Array, Binary, Dynamic Programming, Graph,
Interval, Linked List, Matrix, String, Tree, Heap.
Why to use it: These 75 problems represent the 20% that gives you 80% of
coverage. Complete Blind 75 by Day 45 to establish baseline confidence.
How to use in this plan: Day 1 action: open the Blind 75 list, bookmark it,
check it off as you complete problems across Weeks 1–6.

---

**Resource 3: Striver's SDE Sheet (takeuforward.org/interviews/strivers-sde-sheet)**
What it contains: 191 problems organized into 30 days, covering arrays, math,
hashing, linked lists, recursion, bit manipulation, stack, queue, sliding window,
heaps, greedy, binary search, BST, trees, graphs, and DP.
Why to use it: Best structured resource for systematic coverage with step-by-step
explanations. All explanations in Java. Strong Indian engineering interview focus.
How to use in this plan: Use Striver's sheet as a REFERENCE when a topic feels
weak, not as a primary resource. If Heaps feel shaky after Week 2, open Striver's
Heap section and work through his problems alongside your plan's problems.

---

**Resource 4: LeetCode Company Tags (leetcode.com/problemset/)**
What it contains: Every LeetCode problem tagged by the company that has asked it.
Filter by company name to see problems Amazon, Razorpay, Meesho, etc. have asked.
How to use in this plan: From Week 13 onward, use company tags to build your
warm-up routine. Weeks 13–14 already specify which company tags to use on each day.
Before any interview, solve 5 problems with that company's tag at your target difficulty.

---

**Resource 5: NeetCode DSA Roadmap (neetcode.io/roadmap)**
What it contains: Visual dependency map showing which DSA topics to learn in
which order, with all NeetCode problems linked at each node.
Why to use it: Confirms the learning order in your plan. If you ever feel lost
about what to study next, this roadmap gives you the dependency-ordered answer.

---

### SECTION 3: SYSTEM DESIGN RESOURCES — SPECIFIC AND DESCRIBED

**Resource 1: ByteByteGo Newsletter (bytebytego.substack.com)**
What it covers: Weekly system design deep-dives with diagrams. Past issues cover
URL Shortener, Rate Limiter, API Gateway, Notification System, WhatsApp, YouTube,
Twitter, distributed caching, Kafka internals.
How to use: Subscribe on Day 1. Read every Sunday as part of the industry
awareness ritual. Archive by topic (save Rate Limiter issue to your Rate Limiter
notes folder).
Why essential: Many interview system design questions appear in ByteByteGo first.
Interviewers often reference the same design patterns ByteByteGo teaches.

---

**Resource 2: ByteByteGo (System Design Interview book companion site)**
Access: All free diagrams and supplementary content at bytebytego.com/intro
What it covers: Visual explanations of every system in Alex Xu's books.
How to use: Open the relevant ByteByteGo visual while reading the Alex Xu book
chapter. The visual + book combination is much more effective than either alone.

---

**Resource 3: Gaurav Sen YouTube (youtube.com/c/GauravSensei)**
What it covers: System Design playlist (25+ videos covering URL Shortener, Rate
Limiter, Tinder, YouTube, Netflix, Uber, Consistent Hashing, Load Balancing,
CQRS, Microservices, CAP Theorem).
How to use: Watch each video AFTER reading the corresponding chapter in Alex Xu
and writing your own design. Use Gaurav Sen to check your thinking, not to copy.
Why essential: Gaurav Sen explains trade-offs conversationally, which is exactly
how you should explain them in an interview. His video style trains your verbal
system design communication.

---

**Resource 4: High Scalability Blog (highscalability.com)**
What it covers: Real-world architecture teardowns of actual production systems
(Slack, Twitter, Amazon, Netflix, Discord, WhatsApp at scale). Each post is a
case study of a company's actual engineering decisions with reasons.
How to use: Part of the weekly industry awareness ritual. Read one post every
Sunday. Search by company name before interviewing at that company.
Why essential: Real architecture > theoretical architecture. "Discord migrated from
MongoDB to Cassandra because..." is a much stronger answer than a textbook answer.

---

**Resource 5: Martin Fowler's Blog (martinfowler.com)**
What it covers: Canonical definitions and explanations of: Microservices, CQRS,
Event Sourcing, Strangler Fig pattern, Feature Toggles, Branch by Abstraction,
Continuous Integration, Refactoring. Written by the original author of these terms.
How to use: When the plan introduces Event Sourcing or CQRS, read Martin Fowler's
original post on that topic the same evening. His definitions are authoritative.
Why essential: Using Martin Fowler's original vocabulary and framing in interviews
signals that you understand the concepts at source-level, not via summaries.

---

### SECTION 4: SPRING BOOT AND JAVA BACKEND RESOURCES

**Resource 1: Baeldung (baeldung.com)**
What it covers: 3,000+ Java and Spring Boot tutorials. Topics include Spring
Security, JWT, OAuth2, Spring Data JPA, Spring Batch, Kafka, Redis, Docker,
Testing, Hibernate, REST APIs. Every tutorial has working code.
How to use: Use as a first-stop reference when implementing anything in Spring.
"How to implement JWT authentication in Spring Boot 3" → search Baeldung first.
Why essential: Baeldung code is production-quality and up-to-date with modern
Spring Boot versions. Using Baeldung code in your portfolio projects (with
modifications) is acceptable and common in the industry.

---

**Resource 2: Spring Official Documentation (docs.spring.io)**
What it covers: Complete reference for Spring Boot, Spring Security, Spring Data,
Spring Cloud. The authoritative source for all Spring configurations.
How to use: When a Baeldung article references a Spring concept, follow the link
to the official docs. The official docs have the complete parameter reference
that tutorials abbreviate.
Specific sections: Spring Boot Reference → Core Features → Spring Application
(for understanding auto-configuration). Spring Security Reference → Servlet
Applications → OAuth2 (for understanding OAuth 2.0 resource server setup).

---

### SECTION 5: KUBERNETES AND INFRASTRUCTURE RESOURCES

**Resource 1: TechWorld with Nana YouTube (youtube.com/c/TechWorldwithNana)**
What it covers: Complete Kubernetes tutorial series (5+ hours), Docker tutorial,
Helm tutorial, Terraform basics, CI/CD with GitLab/GitHub Actions.
How to use: Watch the full Kubernetes series during Weeks 5–8 alongside the
theoretical K8s study in the plan. Nana demonstrates every concept in a live
cluster, which cements the theory.
Specific playlist: "Kubernetes Tutorial for Beginners" (4 hours) and
"Complete Kubernetes Course" — watch in order.

---

**Resource 2: Kubernetes Official Documentation (kubernetes.io/docs)**
What it covers: Complete reference for all Kubernetes resources (Pod, Deployment,
Service, Ingress, HPA, PodDisruptionBudget, NetworkPolicy, RBAC, StorageClass).
How to use: Every YAML you write should be validated against the official API
reference. When your HPA config doesn't work, check
kubernetes.io/docs/reference/kubernetes-api/workload-resources/horizontal-pod-autoscaler-v2.

---

**Resource 3: Anton Putra YouTube (youtube.com/c/AntonPutra)**
What it covers: Production Kubernetes patterns — HPA with custom metrics, 
Kubernetes networking deep-dives, Prometheus and Grafana setup in K8s, EKS.
How to use: Watch Anton Putra during the advanced K8s weeks (Weeks 10–11) after
the basics from TechWorld with Nana are solid.

---

### SECTION 6: INTERVIEW PREPARATION COMMUNITIES

**Resource 1: r/developersIndia (reddit.com/r/developersIndia)**
What it covers: Indian tech job market discussions, company reviews, salary
data, interview experience posts from Indian software engineers.
How to use: Read daily during Month 3 and 4. Filter by "interview experience"
to find company-specific posts. Search "[Company Name] SDE 2 interview" monthly.
Salary data here is more accurate for Indian market than US-focused Glassdoor.

---

**Resource 2: Blind App (teamblind.com)**
What it covers: Anonymous posts from software engineers at specific companies.
Very accurate salary data (self-reported by employees). Interview difficulty
assessments. Offers received and negotiation outcomes.
How to use: Before applying to any company, search the company name on Blind.
Read the last 10 posts about that company. Filter for "interview" tag.
Use salary data to anchor your negotiation (more accurate than Glassdoor).
Caution: Blind can be demoralizing. Use it for data collection, not emotional
support. 20 minutes maximum per session.

---

**Resource 3: LeetCode Discuss (leetcode.com/discuss)**
What it covers: Interview experience reports filed by candidates. Company
interview questions, OA questions, system design topics asked.
How to use: Search "[Company] SDE2 interview" before applying to any company.
Filter by "last 6 months" for relevance. The company-specific interview
experience posts are the best source of actual question data available.

---

**Resource 4: Levels.fyi (levels.fyi)**
What it covers: Crowdsourced compensation data for software engineers at
specific companies, roles, and levels. Total comp (base + bonus + RSU/ESOP).
Searchable by company, location, and level.
How to use: Before any negotiation, look up the company + "SDE 2" + "India".
Find the P50 (median) total comp. That is your minimum anchor. Negotiate from
P75 as your initial ask.
