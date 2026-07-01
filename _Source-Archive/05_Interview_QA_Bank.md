# 05 — Interview Q&A Bank

## Java (20 Questions)

**Q1: Explain how HashMap works internally in Java.**
*Beginner:* A HashMap stores key-value pairs and gives you O(1) average lookup time. You put a key in, it figures out where to store it, and when you ask for that key back, it finds it instantly without searching through everything.
*SDE-2:* Internally it's an array of buckets. The key's hashCode() is passed through a spreading function (XOR-ing the hash with itself shifted right 16 bits) to reduce clustering, then masked against (capacity-1) to get a bucket index. Collisions within a bucket are handled with a linked list, which converts to a red-black tree once a bucket exceeds 8 entries (Java 8+). The map resizes — doubling capacity and rehashing everything — once size exceeds capacity × 0.75 (the load factor).
*Senior:* The treeification trade-off matters because tree nodes carry more memory overhead per entry, so it's a deliberate worst-case mitigation, not a default behavior — it only kicks in when a single bucket is pathologically overloaded, which usually signals a poor hashCode() implementation upstream. I'd also discuss why this isn't thread-safe (no synchronization on the bucket array or size counter) and contrast it with ConcurrentHashMap's approach in Java 8+, which uses CAS operations on individual bins rather than segment locking, giving much better write concurrency than the Java 7 segment-lock design. At scale, if hash collisions become an attack vector (hash flooding), I'd bring up Java's randomized hash seed defense.

**Q2: How does the JVM handle Garbage Collection for short-lived objects?**
*Beginner:* The JVM automatically cleans up objects you don't use anymore. It does this by running a Garbage Collector in the background so your program doesn't run out of memory.
*SDE-2:* The heap is split into Young and Old generations. Short-lived objects are allocated in the Eden space of the Young generation. When Eden fills up, a Minor GC triggers, copying surviving objects into one of the Survivor spaces (S0/S1). This is very fast because it only traces live objects and ignores dead ones, and memory is compacted by copying.
*Senior:* The copy collection approach is highly efficient for the Young generation because the weak generational hypothesis states most objects die young. However, JVM tuning is critical here; if the Survivor space is too small, objects prematurely promote to the Old generation (premature tenuring), leading to expensive Full GCs. Using G1GC or ZGC mitigates long pauses by operating concurrently, but tuning `-XX:MaxGCPauseMillis` and ensuring adequate allocation rates remains essential for high-throughput backends.

**Q3: What is the difference between `synchronized` and `ReentrantLock`?**
*Beginner:* Both are used to stop multiple threads from running the same code at the same time. You use them when you want to avoid race conditions.
*SDE-2:* `synchronized` is a language keyword that locks intrinsically on an object monitor and must be released in the same block. `ReentrantLock` is an API class that requires explicit `lock()` and `unlock()` (usually in a finally block) but provides advanced features like `tryLock(timeout)`, fairness settings, and the ability to lock/unlock across different methods.
*Senior:* The real power of `ReentrantLock` comes from `Condition` objects. With an intrinsic monitor, you only get one wait-set (`wait()`/`notifyAll()`). With a `ReentrantLock`, you can create multiple `Condition` variables (e.g., `notEmpty` and `notFull` for a bounded queue), dramatically reducing context switching by only waking up the specific threads that can proceed, thus solving the thundering herd problem.

**Q4: How does `volatile` work, and when should you use it?**
*Beginner:* It's a keyword you put on variables so that all threads always see the most recent value.
*SDE-2:* `volatile` guarantees visibility by ensuring reads and writes go straight to main memory rather than being cached in CPU registers or L1/L2 caches. It also prevents the compiler from reordering instructions across the volatile read/write. However, it does not guarantee atomicity for compound operations like `count++`.
*Senior:* `volatile` establishes a happens-before relationship in the Java Memory Model. A write to a volatile field happens-before every subsequent read of that same field. This is heavily leveraged in lock-free algorithms and patterns like Double-Checked Locking for Singletons (post-Java 1.5). I strictly use it for simple flags (like a shutdown signal) or single-writer/multiple-reader scenarios where `AtomicReference` or locks would introduce unnecessary overhead.

**Q5: What is the difference between `Callable` and `Runnable`?**
*Beginner:* Both define code that can be run on a separate thread, but `Callable` can return a result and throw an exception, while `Runnable` cannot.
*SDE-2:* `Runnable` has a `run()` method returning `void`, making it difficult to extract results or handle checked exceptions without shared variables. `Callable` has a `call()` method returning a generic `<T>` and declares `throws Exception`. You submit a `Callable` to an `ExecutorService` and get a `Future<T>` to retrieve the result.
*Senior:* While `Callable` is an improvement, `Future` is inherently blocking if you call `get()`. Modern Java (since 8) prefers `CompletableFuture` combined with `Supplier` to build reactive, non-blocking asynchronous pipelines, completely bypassing the need to block on a `Callable`'s Future and avoiding thread starvation in bounded thread pools.

**Q6: Explain the N+1 query problem in Spring Data JPA.**
*Beginner:* It happens when your code makes one database query to get a list of items, and then makes another separate query for each item in that list, slowing down the app.
*SDE-2:* It occurs when you fetch a collection of entities (like Authors) and then access a lazily-loaded association (like Books) while iterating. JPA executes 1 query for N Authors, and then N separate queries for their Books. I fix this by using `JOIN FETCH` in a custom `@Query` or by defining an `@EntityGraph` to eagerly fetch the association in a single SQL join.
*Senior:* While `JOIN FETCH` solves the database round-trips, it can cause memory issues if fetching massive Cartesian products. A more scalable approach for multiple collections is configuring `@BatchSize` (e.g., to 50), which changes the N separate queries into `N/50` queries using SQL `IN` clauses. Alternatively, CQRS patterns suggest skipping JPA entirely for complex read models and using JOOQ or native SQL mapping directly to DTOs.

**Q7: How does `@Transactional` work under the hood?**
*Beginner:* It tells Spring to wrap your method in a database transaction. If an error happens, it rolls back all the changes so the database isn't left in a bad state.
*SDE-2:* Spring uses AOP to create a dynamic proxy around the bean. When another class calls the method, the proxy intercepts the call, opens the transaction, invokes the actual method, and then either commits or rolls back based on whether a RuntimeException (by default) was thrown.
*Senior:* The proxy architecture causes the "self-invocation" gotcha: calling a `@Transactional` method from another method within the same class bypasses the proxy, so the transaction is completely ignored. To fix this, you must inject the service into itself or refactor the transactional method into a separate class. Also, understanding isolation levels (like `REPEATABLE_READ`) and propagation behaviors (`REQUIRES_NEW`) is crucial for nested transaction scenarios.

**Q8: Explain the difference between `ArrayList` and `LinkedList`.**
*Beginner:* `ArrayList` uses an array inside and is good for getting items quickly. `LinkedList` uses nodes pointing to each other and is better if you add/remove items a lot.
*SDE-2:* `ArrayList` provides O(1) random access but O(n) worst-case insertions in the middle due to shifting elements. `LinkedList` provides O(1) insertions but O(n) random access. In 99% of cases, `ArrayList` is faster because CPU cache locality makes array iteration lightning fast compared to chasing node pointers in heap memory.
*Senior:* `LinkedList` is almost an anti-pattern in modern Java due to object overhead (one node object per element) and devastating cache misses. Even for queue operations, `ArrayDeque` vastly outperforms `LinkedList` because it uses a circular array. The only niche for `LinkedList` is when you need O(1) element removal using an active `ListIterator`.

**Q9: What happens when an Exception is thrown inside a `finally` block?**
*Beginner:* The program will crash and show the error from the finally block, but it might hide the original error that happened in the try block.
*SDE-2:* If a `try` block throws Exception A, and the `finally` block throws Exception B while trying to clean up, Exception A is completely swallowed and lost. The caller only sees Exception B, making debugging a nightmare.
*Senior:* This is exactly why Java 7 introduced `try-with-resources`. Objects implementing `AutoCloseable` are automatically closed, and if `close()` throws an exception, it is automatically added to the original exception as a "suppressed exception" via `Throwable.addSuppressed()`. I never manually close resources in `finally` anymore.

**Q10: What is Type Erasure in Generics?**
*Beginner:* Generics are only used by the compiler to check your code. When the program actually runs, Java forgets the generic types, treating everything like an Object.
*SDE-2:* The compiler ensures type safety at compile-time and inserts necessary casts, but removes generic type parameters (like `<String>`) in the bytecode, replacing them with `Object` (or bounds like `Number`). This is why you cannot do `new T()` or `if (obj instanceof List<String>)` at runtime.
*Senior:* Type erasure was a necessary evil for backwards compatibility with pre-Java 5 bytecode. However, it severely limits runtime reflection. For instance, when serializing generics with Jackson, you must pass a `TypeReference` object because the generic type information of a class instance is erased. Interestingly, generic types defined on a *Class signature* or *Method signature* are preserved in the classfile metadata and can be retrieved via reflection (`ParameterizedType`), which is exactly how Spring resolves generic injection.

**Q11: Explain String Immutability and the String Pool.**
*Beginner:* Once a String is created, it cannot be changed. The String Pool is an area in memory where Java stores String values to reuse them and save memory.
*SDE-2:* Immutability makes Strings inherently thread-safe and allows caching their hash codes, which makes them perfect HashMap keys. The String Pool (in the heap) reuses literal strings. `String s1 = "hello"` uses the pool, but `String s2 = new String("hello")` forces a new object on the heap, bypassing the pool unless `.intern()` is called.
*Senior:* Pre-Java 9, Strings used a `char[]` (UTF-16, 2 bytes per char). Java 9 introduced Compact Strings, dynamically switching to a `byte[]` (Latin-1) if the string only contains ASCII, cutting memory usage in half. For heavy string manipulation, `StringBuilder` is mandatory to avoid O(n^2) garbage generation in loops, though the JIT compiler actually optimizes simple concatenations (`a + b`) into `invokedynamic` calls (Java 9+) using `StringConcatFactory`.

**Q12: How do Java Streams `filter()` and `map()` execute internally?**
*Beginner:* They let you process a list in a functional way. `filter` removes items, and `map` transforms them.
*SDE-2:* Streams are evaluated lazily. Intermediate operations like `filter` and `map` don't do anything until a terminal operation like `collect` is called. The stream pipeline fuses the operations together, so it iterates through the underlying collection exactly once, applying the filter and map to each element in a single pass.
*Senior:* The lazy evaluation is powered by a `Spliterator`. When parallel streams are used, the spliterator recursively chunks the source data and feeds it to the ForkJoinPool. However, using parallel streams on an I/O bound task or a stateful operation is disastrous. Furthermore, `peek()` should only be used for debugging, as the API allows the implementation to skip executing it entirely if the final result doesn't require it (e.g., `count()` on a sized stream).

**Q13: What is the `Double-Checked Locking` pattern and why is it tricky in Java?**
*Beginner:* It's a way to create a Singleton object where you first check if it exists, then lock, then check again to make sure another thread didn't just create it.
*SDE-2:* It's used for lazy initialization while minimizing synchronization overhead. The trick is that without the `volatile` keyword on the instance variable, instruction reordering by the JIT or CPU can cause a thread to see a non-null reference to a partially constructed object.
*Senior:* Prior to Java 1.5, the Java Memory Model was flawed, making DCL fundamentally broken even with `volatile`. Since JSR-133, `volatile` enforces a happens-before edge, preventing the reordering of object initialization. However, modern Java provides much better alternatives: the Initialization-on-Demand Holder idiom (using an inner static class) or simply using a single-element `enum`, which the JVM inherently guarantees is thread-safe and serializable.

**Q14: Explain `ConcurrentHashMap` vs `Collections.synchronizedMap()`.**
*Beginner:* `synchronizedMap` locks the entire map, so only one thread can use it at a time. `ConcurrentHashMap` is much faster because it allows many threads to access it simultaneously.
*SDE-2:* `synchronizedMap` puts an intrinsic lock over every method. `ConcurrentHashMap` (in Java 8) uses node-level locking via `synchronized` blocks on the first node of each bucket, combined with non-blocking CAS operations for reads and tree node updates.
*Senior:* The transition from Java 7 to Java 8's `ConcurrentHashMap` replaced segment locking (which capped concurrency to 16 by default) with fine-grained bucket locking and CAS. Furthermore, CHM provides powerful atomic methods like `computeIfAbsent()`. However, developers often misinterpret it: while individual operations are thread-safe, compound operations like `if (!map.containsKey(k)) map.put(k,v)` are not atomic unless you use the provided atomic methods.

**Q15: How does ThreadLocal work and what are the memory leak risks?**
*Beginner:* `ThreadLocal` gives you a variable that is only visible to the current thread, like a private stash.
*SDE-2:* It stores the variable in a `ThreadLocalMap` attached to the current `Thread` instance, where the key is the `ThreadLocal` object itself. Since the thread owns the map, no synchronization is needed. The risk occurs in application servers using thread pools: if a thread completes a web request but doesn't call `remove()`, the object stays in memory forever because the thread is recycled, causing memory leaks.
*Senior:* The `ThreadLocalMap` keys are `WeakReference`s, which helps prevent classloader leaks, but the values are strong references. If you deploy a WAR file, a left-over value can prevent the entire webapp classloader from being garbage collected. This is why it is mandatory to wrap usage in a `try-finally` block to call `remove()`. Looking forward, Java 21's Scoped Values provide a safer, immutable, structured concurrency alternative to `ThreadLocal`.

**Q16: What is an `AtomicInteger` and what problem does it solve?**
*Beginner:* It's an integer that is safe to use across multiple threads without needing a `synchronized` lock.
*SDE-2:* It solves the check-then-act/read-modify-write race condition of `count++`. It relies on the CPU's Compare-And-Swap (CAS) hardware instruction to update the value optimistically in a non-blocking loop. If another thread modified the value in the meantime, CAS fails, and it retries.
*Senior:* CAS suffers from contention overhead under high write loads, where threads constantly spin-retrying, burning CPU cycles. It also historically faced the ABA problem (solved via `AtomicStampedReference`). Under extremely high contention, Java 8's `LongAdder` or `LongAccumulator` is vastly superior to `AtomicLong`, as it stripes the updates across an array of variables (cells) to reduce contention, summing them up only when read.

**Q17: Describe Spring's Bean Lifecycle.**
*Beginner:* Spring creates an object, injects its dependencies, lets you run startup code, manages it while the app runs, and then destroys it when the app shuts down.
*SDE-2:* The container instantiates the bean, populates properties, and resolves DI. Then it invokes `BeanNameAware`/`BeanFactoryAware` interfaces. Before initialization, `BeanPostProcessor.postProcessBeforeInitialization` runs. Then `@PostConstruct` or `InitializingBean.afterPropertiesSet()` runs. Then `postProcessAfterInitialization` runs (where AOP proxies are created). Finally, on shutdown, `@PreDestroy` runs.
*Senior:* Understanding `BeanPostProcessor` is the key to mastering Spring. It's the hook where Spring proxies beans for `@Transactional`, `@Async`, or `@Cacheable`. If you try to inject a bean into a `BeanPostProcessor` itself, it might cause premature initialization, bypassing other processors and breaking proxying. Debugging circular dependencies often traces back to constructor injection forcing the lifecycle to resolve too early.

**Q18: What is the JVM ClassLoader and what are its principles?**
*Beginner:* The ClassLoader is the part of the JVM that reads your .class files and loads them into memory so they can be executed.
*SDE-2:* There are three main loaders: Bootstrap, Extension (Platform in Java 9+), and Application (System). They follow the Delegation principle (ask the parent first before trying to load), Visibility (children can see parent classes, but not vice-versa), and Uniqueness (a class is loaded exactly once by a specific loader).
*Senior:* The parent-delegation model is intentionally broken by web servers like Tomcat. A WAR needs its own `/WEB-INF/lib` to load its specific versions of libraries without conflicting with the server's or other apps' libraries, so WebAppClassLoaders check their local context *first* before delegating. In modern Java, the Module system (Project Jigsaw) revolutionized this by enforcing explicit `requires` and `exports` at the JVM level, largely superseding classpath hell.

**Q19: Explain Java's Pass-by-Value vs Pass-by-Reference.**
*Beginner:* Java always passes everything by value. If you pass a primitive, it copies the value. If you pass an object, it copies the reference to the object.
*SDE-2:* Because it copies the reference, if you pass an object to a method and modify its fields (`user.setName("John")`), the original object is changed. However, if you reassign the parameter entirely (`user = new User()`), the original reference in the calling method remains completely unchanged.
*Senior:* This distinction is crucial when analyzing the JVM stack. Every method invocation pushes a frame. Primitives and references are stored in the local variable array of that frame. Reassigning a reference merely overwrites the local stack slot, having zero effect on the heap or the caller's stack frame. This is also why creating defensive copies is mandatory when returning mutable objects (like arrays or Dates) from encapsulated classes.

**Q20: What are Java Records (Java 14/16+)?**
*Beginner:* They are a quick way to create data-holding classes without having to write getters, `equals()`, `hashCode()`, and `toString()`.
*SDE-2:* They are shallowly immutable, transparent data carriers. The compiler automatically generates the canonical constructor, accessors, and standard methods. You can still define custom methods, implement interfaces, and write compact constructors for validation without redefining parameters.
*Senior:* Records fundamentally change serialization security. Unlike regular classes where serialization uses reflection to bypass constructors (a massive security vulnerability), records are deserialized exclusively through their canonical constructor, guaranteeing that validation logic is always executed. Jackson's latest versions natively support deserializing JSON into Java Records without requiring a no-args constructor or annotations.

---

## System Design (15 Questions)

**Q1: How do you design a scalable URL Shortener?**
*Beginner:* You take a long URL, map it to a short random string, and save it in a database. When a user visits the short link, you look it up and redirect them.
*SDE-2:* I'd use Base62 encoding on a unique integer ID to generate the short string (e.g., ID 1000 becomes "g8"). To ensure uniqueness in a distributed system, I'd use ZooKeeper to hand out ranges of IDs to application servers. I'd add Redis for aggressive read caching and return HTTP 302 for redirects to allow analytics tracking.
*Senior:* The debate between 301 and 302 redirects is key: 301 caches in the browser (saves server load but loses analytics), while 302 hits the server every time. For database, Cassandra or DynamoDB is ideal due to heavy reads and simple KV lookups. I'd also design an offline cleanup job for expired URLs (using Cassandra TTL or a sweeping job) and add rate limiting per IP to prevent malicious shortening storms.

**Q2: Design a Rate Limiter.**
*Beginner:* You keep a counter in a cache like Redis. Every time a user makes a request, you increment the counter. If it goes over the limit, you block them.
*SDE-2:* I'd evaluate Token Bucket, Leaky Bucket, and Sliding Window algorithms. A Sliding Window with Redis Sorted Sets is accurate but memory-intensive. For most APIs, a Redis-based Token Bucket using a Lua script ensures atomic check-and-decrement. I'd place this logic in the API Gateway.
*Senior:* A strict Redis architecture fails under massive scale due to network latency. I'd advocate for a hybrid approach: local in-memory rate limiting on the API gateway nodes synchronized via a gossip protocol, or batching async updates to Redis. Also, distinguishing between IP limits (DDoS protection) and User ID limits (business logic) is critical, and you must return standard `429 Too Many Requests` with `X-RateLimit-Reset` headers.

**Q3: How do you guarantee Idempotency in a Payment System?**
*Beginner:* You make sure that if a user clicks the "Pay" button twice, they only get charged once. You check if the payment was already made.
*SDE-2:* Clients generate a unique Idempotency Key (UUID) for each POST request. The server attempts to insert this key into a database table with a UNIQUE constraint. If it succeeds, the payment is processed. If it violates the constraint, the server knows it's a duplicate and returns the previous result stored against that key.
*Senior:* A simple DB unique constraint isn't enough; you need a multi-state machine (STARTED, PENDING, SUCCESS, FAILED). If a second request arrives while the first is PENDING, you must return a 409 Conflict or block. Furthermore, the idempotency key must expire after 24 hours to prevent table bloat, and the caller's payload must be hashed and verified against the stored request to prevent them from reusing the key for a different payment amount.

**Q4: Explain the Saga Pattern for distributed transactions.**
*Beginner:* When a transaction spans multiple microservices, you can't use a standard database lock. Saga breaks it into steps, and if one step fails, it runs undo steps.
*SDE-2:* It's a sequence of local transactions. Each service updates its DB and publishes an event. If an event fails (e.g., Payment failed after Inventory was reserved), a compensating transaction is fired (Restore Inventory). It operates via Choreography (services listen to each other) or Orchestration (a central coordinator manages the flow).
*Senior:* Choreography gets wildly complex (cyclic dependencies) beyond 3 services; Orchestration using state machines (like AWS Step Functions or temporal.io) is vastly superior for complex sagas. The hardest part is ensuring compensating transactions are strictly idempotent and cannot fail, because if a compensation fails, the system requires manual intervention or dead-letter queue processing to reconcile the eventual consistency.

**Q5: Design a Notification System.**
*Beginner:* You need a service that receives events, figures out who needs to be notified, and sends emails, SMS, or push notifications.
*SDE-2:* The system has a dispatcher that pushes events to Kafka. Consumer groups pick up events, resolve user preferences (e.g., "mute email, push only"), and send to third-party APIs (SendGrid, Twilio). I'd use Redis to deduplicate messages and rate-limit notifications per user to prevent spamming.
*Senior:* The critical failure mode here is third-party API latency/outages. I'd implement independent Kafka topics per channel (Email, SMS) and priority levels (OTP vs Marketing) to prevent bulk marketing from delaying critical OTPs. I'd use Resilience4j circuit breakers around third-party calls, and push failed deliveries to a Retry Topic with exponential backoff, eventually dumping to a Dead Letter Queue.

**Q6: How do you handle High-Read vs High-Write traffic (CQRS)?**
*Beginner:* You separate the code that reads data from the code that writes data, so they can be optimized differently.
*SDE-2:* CQRS separates Command (Write) models from Query (Read) models. In practice, a write hits a transactional database (PostgreSQL), emits an event, and asynchronously updates a highly optimized read store (like Elasticsearch or Redis) designed specifically for the UI's exact query format.
*Senior:* The absolute hardest part of CQRS is handling Eventual Consistency on the UI layer. When a user submits a write, the read replica isn't updated yet. To prevent the "I saved it but it's not there" bug, you must implement "Read-Your-Writes" consistency, often by having the frontend artificially update the local state, or by passing a version token to the backend that forces the read query to wait until the replica catches up.

**Q7: Explain Consistent Hashing.**
*Beginner:* When distributing data across many servers, consistent hashing ensures that if you add or remove a server, you don't have to move all the data around.
*SDE-2:* Standard hashing `hash(key) % N` causes a massive reshuffle if N changes. Consistent hashing maps both the servers and the keys onto a circular hash space (0 to 2^32-1). A key is stored on the first server found moving clockwise. Adding a node only moves keys from its immediate clockwise neighbor, minimizing data transfer.
*Senior:* The classic circle suffers from non-uniform data distribution (hot spots). To fix this, you add "Virtual Nodes" — hashing each physical server multiple times (e.g., server1_0, server1_1) with different hash functions. This balances the load. When designing a distributed cache or Dynamo-style DB, you also replicate keys clockwise to N distinct physical nodes for fault tolerance.

**Q8: Design WhatsApp (Chat System).**
*Beginner:* Users connect to a server. When User A sends a message to User B, the server receives it and forwards it to User B.
*SDE-2:* Clients maintain persistent WebSocket connections to Chat Servers. A user's active WebSocket server is tracked in a Redis cache. When A messages B, the Chat Server looks up B's server in Redis and routes the message via a pub/sub bus. Messages are persisted in a wide-column store like Cassandra for fast writes and time-series querying.
*Senior:* Offline message delivery requires an inbox model. For scale, I'd use the "Push" model for active connections and "Pull" for offline users syncing upon reconnect. To guarantee message ordering, you generate a monotonic sequence ID (using a distributed generator like Snowflake or a local counter per chat room) on the server, not the client. E2E encryption means the server stores encrypted blobs, relying entirely on client-side key management.

**Q9: Design Uber (Driver Location Tracking).**
*Beginner:* Drivers send their GPS coordinates to the server every few seconds. The server saves it, and the rider's app asks the server for nearby drivers.
*SDE-2:* High frequency writes demand an in-memory spatial index. I'd use Redis Geospatial (GEOADD/GEORADIUS) or a quadtree implementation. Drivers push location to Kafka, consumers update Redis. Riders query Redis for drivers within a radius. The matching service calculates ETA.
*Senior:* Real-time location updates (millions per second) require batching. Drivers batch points client-side and push via UDP/WebSocket. Redis GEO is single-threaded, so I'd shard the spatial index geographically (e.g., one shard for Manhattan, one for Brooklyn). For historical analytics and routing ML, the Kafka stream dumps to a data lake (S3/Hadoop) using Parquet.

**Q10: What is Event Sourcing?**
*Beginner:* Instead of saving the current state of an object, you save every single action that happened to it. You read the state by replaying the actions.
*SDE-2:* State is derived by folding a stream of immutable events (e.g., AccountCreated, MoneyDeposited, MoneyWithdrawn). This provides a perfect audit log and allows time-travel debugging. The events are stored in an append-only log (like Kafka or EventStoreDB).
*Senior:* Replaying millions of events on every read is unscalable, so you must implement snapshots (saving the aggregated state every N events). Furthermore, evolving the schema of historical events requires complex upcasting patterns. Event sourcing is powerful for financial ledgers, but adds immense operational complexity and mandates CQRS for querying.

**Q11: How do you prevent Cache Stampedes?**
*Beginner:* A stampede is when a cache expires and 1000 users ask the database for the data at the same time, crashing it. You prevent it by staggering the expiration times.
*SDE-2:* Adding a random jitter to TTLs prevents simultaneous expiration. For heavily accessed keys, I'd implement a distributed lock: when a cache miss occurs, only the first thread acquires the lock, queries the DB, and repopulates the cache. The other threads wait and re-check the cache.
*Senior:* Distributed locks can block the thread pool entirely. The optimal pattern is Probabilistic Early Expiration (XFetch): the background logic calculates a probability of early expiration that approaches 100% as the true TTL nears. One lucky thread is told "cache missed" slightly early, updating the cache asynchronously in the background while other threads continue receiving the stale (but immediately available) cached data.

**Q12: Design an API Gateway.**
*Beginner:* It's the front door to all microservices. It receives all client requests, routes them to the right service, and handles security.
*SDE-2:* It handles cross-cutting concerns: SSL termination, JWT validation, rate limiting, and routing. I'd use an asynchronous, non-blocking tech stack (like Spring Cloud Gateway or Kong) to handle high concurrent connections.
*Senior:* The Gateway must not contain business logic. A common anti-pattern is doing complex data aggregation in the gateway, which tightly couples it to backend deployments. Aggregation belongs in a Backend-For-Frontend (BFF) layer. At massive scale, you run multiple Gateways behind an L4 load balancer (AWS NLB), and the gateway nodes use a highly optimized eBPF or Envoy proxy data plane.

**Q13: How do you design an E-Commerce Flash Sale?**
*Beginner:* Millions of people try to buy a limited item at once. You put them in a queue so the servers don't crash.
*SDE-2:* The database will melt under concurrent writes. I'd load inventory counts into Redis. A Lua script atomically checks if inventory > 0 and decrements it. If successful, the order is dropped into a Kafka queue for asynchronous DB processing. The UI polls for the order status.
*Senior:* Bots and unfair access are the biggest threats. A CDN edge layer with WAF blocks malicious traffic. A virtual waiting room using token buckets controls the ingress rate to the application layer. Furthermore, if a user reserves an item but abandons the cart, a delayed message queue (e.g., Kafka with pause/resume or Redis expired events) must reliably restore the inventory count exactly 15 minutes later.

**Q14: Explain the CAP Theorem.**
*Beginner:* In a distributed database, you can only pick two out of three: Consistency, Availability, and Partition Tolerance.
*SDE-2:* Partitions (network failures) will inevitably happen. Therefore, you must choose between Consistency (CP) and Availability (AP). A CP system (like HBase or MongoDB in strict mode) will refuse writes if nodes cannot communicate. An AP system (like Cassandra or Dynamo) will accept writes locally, allowing temporary data inconsistency but high availability.
*Senior:* CAP is a massive oversimplification. Systems aren't strictly CP or AP; they allow configurable trade-offs per operation (e.g., tunable consistency via Quorum reads/writes). Furthermore, the PACELC theorem is more practical: "If there is a Partition (P), how does the system trade off A and C? Else (E), when running normally, how does it trade off Latency (L) and Consistency (C)?" Cassandra chooses A and L; Spanner chooses C and C.

**Q15: Design a Search Autocomplete System.**
*Beginner:* As the user types, you query a database for words starting with those letters. You show the top 10 most popular ones.
*SDE-2:* A DB `LIKE 'prefix%'` query is too slow. I'd use a Trie data structure stored in memory, where each node stores the top 5 historical searches passing through it. The Trie is precomputed from analytical logs and updated periodically.
*Senior:* For true global scale, the Trie is massive and must be sharded by the prefix (e.g., 'a-m' on server 1, 'n-z' on server 2). Real-time frequency updates require a streaming pipeline (Kafka + Flink) that aggregates searches and updates the Trie asynchronously. To optimize network latency on mobile, the client fetches the top 50 suggestions for the first few characters and caches them locally, doing local filtering for subsequent keystrokes.

---

## Kubernetes (10 Questions)

**Q1: Explain the Kubernetes Control Plane.**
*Beginner:* It's the brain of Kubernetes. It decides where to run your apps and makes sure they stay running.
*SDE-2:* It consists of the API Server (the single entry point), etcd (distributed key-value store for state), Scheduler (assigns Pods to nodes), and Controller Manager (runs loops that reconcile desired state vs actual state).
*Senior:* The architecture is fundamentally declarative and asynchronous. The API server does not push commands to worker nodes. Instead, the `kubelet` on each node constantly watches the API server for Pods assigned to its node. Because etcd relies on the Raft consensus algorithm, control planes require 3 or 5 nodes to tolerate failures, and high-performance clusters must deploy etcd on fast NVMe drives to prevent control-loop starvation.

**Q2: What is the difference between a Deployment and a StatefulSet?**
*Beginner:* Deployments run stateless apps where any pod can be replaced easily. StatefulSets are for databases or apps that need to save data safely.
*SDE-2:* Pods in a Deployment get random hashes (web-8f7x), share storage, and update all at once or via rolling updates. StatefulSets guarantee stable, sticky network identities (db-0, db-1) and stable storage; each pod gets its own PersistentVolume. StatefulSets also start and stop strictly in order.
*Senior:* The ordered startup guarantees of StatefulSets are critical for distributed database bootstrapping (e.g., MongoDB replica sets, where db-0 must become primary before db-1 joins). Furthermore, when a node fails, Deployments aggressively reschedule pods to other nodes, but StatefulSets will refuse to reschedule a pod if it cannot confirm the old pod is truly dead, protecting against split-brain data corruption.

**Q3: How does Kubernetes Service Discovery work?**
*Beginner:* Services act as a load balancer. You hit a Service name, and it sends the traffic to one of your healthy pods.
*SDE-2:* CoreDNS automatically creates DNS records for every Service (`my-svc.my-namespace.svc.cluster.local`). The `kube-proxy` component on every node watches the API server and sets up iptables or IPVS rules to intercept traffic meant for the Service IP and load-balance it to the actual Pod IPs.
*Senior:* Using iptables for large clusters becomes an O(N) bottleneck, taking minutes to apply routing rules if you have thousands of services. High-scale clusters switch `kube-proxy` to IPVS mode, or drop `kube-proxy` entirely in favor of eBPF-based CNI plugins like Cilium. eBPF bypasses the kernel's network stack entirely, providing massive performance gains and deeper L7 observability.

**Q4: Explain Liveness, Readiness, and Startup Probes.**
*Beginner:* They are checks K8s uses to see if your app is healthy. If it's broken, K8s restarts it.
*SDE-2:* `livenessProbe` checks if the app is deadlocked; if it fails, K8s kills and restarts the pod. `readinessProbe` checks if the app can handle traffic; if it fails, K8s removes the pod from the Service endpoints, but doesn't kill it. `startupProbe` is used for slow-starting legacy apps; it disables the other two probes until the app has successfully started.
*Senior:* A common disaster is putting database dependency checks in the `livenessProbe`. If the DB goes down temporarily, all application pods fail their liveness checks and get simultaneously killed by K8s, causing a massive recovery storm. DB checks belong *only* in the `readinessProbe`. The `livenessProbe` should solely test if the HTTP thread pool is responsive.

**Q5: How does a Rolling Update guarantee zero downtime?**
*Beginner:* K8s brings up new pods and slowly turns off old ones, so there are always some running to handle traffic.
*SDE-2:* A Deployment creates a new ReplicaSet. It honors `maxSurge` (how many extra pods can be created) and `maxUnavailable` (how many can be offline). It brings up a new pod, waits for its `readinessProbe` to pass, adds it to the Service load balancer, and only then terminates an old pod.
*Senior:* To achieve true zero-downtime, readiness probes aren't enough. When an old pod receives SIGTERM, the application must catch it, refuse new connections, finish processing in-flight requests (graceful shutdown), and sleep for 10-15 seconds before exiting. This sleep allows the asynchronous `kube-proxy` iptables updates to propagate across all nodes, ensuring no packets are dropped in transit to the dying pod.

**Q6: What are Resource Requests and Limits?**
*Beginner:* Requests are what your pod needs to start, and limits are the maximum CPU and memory it's allowed to use.
*SDE-2:* The Scheduler uses Requests to find a node with enough capacity. Limits enforce cgroup constraints. If a pod exceeds Memory Limit, it is OOMKilled instantly. If it exceeds CPU Limit, it is throttled but not killed.
*Senior:* Java applications historically misread container limits, assuming they had access to the host node's total memory, leading to instant OOMKills. Java 10+ fixes this with `UseContainerSupport`. CPU throttling is notoriously aggressive in Linux CFS; setting CPU limits on latency-sensitive backend services often causes unpredictable latency spikes. Many high-performance platforms enforce memory limits but entirely remove CPU limits, relying instead on Requests for scheduling.

**Q7: Explain the Horizontal Pod Autoscaler (HPA).**
*Beginner:* It automatically adds more pods when your application gets busy and scales down when it's quiet.
*SDE-2:* It queries the Metrics Server periodically. The algorithm calculates `desiredReplicas = ceil(currentReplicas * (currentMetric / desiredMetric))`. It scales based on CPU/Memory or custom metrics. It has a stabilization window to prevent thrashing (scaling up and down wildly).
*Senior:* CPU is often a terrible metric for scaling an asynchronous backend or Kafka consumer. I implement Custom Metrics using Prometheus Adapter to scale HPA based on "Kafka Consumer Lag" or "HTTP Requests Per Second." Scaling based on lag ensures you bring up new consumer pods exactly when the queue depth justifies it, regardless of CPU utilization.

**Q8: How do Network Policies work?**
*Beginner:* They are like a firewall for your pods, letting you block traffic between different apps in your cluster.
*SDE-2:* By default, all pods can talk to all pods. NetworkPolicies use pod selectors and namespace selectors to explicitly allow ingress/egress traffic. A best practice is to deploy a "default-deny-all" policy per namespace, and explicitly allow only what is necessary.
*Senior:* Implementing a default-deny policy late in a project breaks everything. It must be foundational. Furthermore, standard NetworkPolicies only operate at L3/L4 (IPs and Ports). If you need L7 filtering (e.g., Service A can GET `/users` on Service B but cannot POST), you must implement a Service Mesh like Istio or use an advanced CNI like Cilium.

**Q9: What is the role of an Ingress Controller?**
*Beginner:* It manages external access to the cluster, routing HTTP/HTTPS traffic to the right services based on URLs.
*SDE-2:* While a LoadBalancer Service provisions an expensive cloud load balancer per app, an Ingress resource defines path-based rules (e.g., `/api` -> api-svc, `/web` -> web-svc). The Ingress Controller (like Nginx) reads these rules and implements the reverse proxy, sharing a single external IP. It also handles SSL/TLS termination.
*Senior:* Managing TLS certificates manually is an anti-pattern. You pair the Ingress Controller with `cert-manager` to automatically provision and rotate Let's Encrypt certificates via ACME protocols. Kubernetes is now transitioning from the Ingress API to the new Gateway API, which provides a much richer, role-oriented model for defining L4/L7 routing, delegating cluster-level routing to infra teams and app-level routing to developers.

**Q10: Describe your debugging workflow for a crash-looping pod.**
*Beginner:* I look at the logs using `kubectl logs <pod-name>` to see what the error is.
*SDE-2:* `kubectl get events` to check for scheduling/pull issues. `kubectl describe pod` to see probe failures or OOMKilled statuses. `kubectl logs --previous` to see what happened before it crashed. If needed, I `kubectl exec` into a running pod to test network connectivity.
*Senior:* If the pod crashes instantly, `exec` won't work. In modern secure environments, images are "distroless" and contain no shell or debug tools anyway. I use `kubectl debug`, which attaches an ephemeral container (like an Ubuntu image with curl, tcpdump, and netcat) to the same network namespace as the crashing pod, allowing me to deep-dive network connectivity and filesystem mounts without altering the production image.

---

## Low-Level Design (10 Questions)

**Q1: How do you design a Parking Lot (Class Structure)?**
*Beginner:* Create a ParkingLot class with an array of Spots. Create a Vehicle class. When a vehicle arrives, find an empty spot and save it.
*SDE-2:* I'd define abstract `Vehicle` (Car, Truck, Bike) and `ParkingSpot` classes. The `ParkingLot` contains `Level`s, which contain `ParkingSpot`s. An `EntryPanel` assigns a `Ticket`, and an `ExitPanel` calculates the fee using a `PricingStrategy` interface (allowing different rates for hourly vs flat).
*Senior:* The hardest part is concurrency when 5 cars enter simultaneously. Using a coarse-grained lock on the whole parking lot crushes throughput. I'd use a `ConcurrentHashMap` for active tickets and fine-grained locking or optimistic concurrency for the specific `Level` or `ParkingSpot`. The `ParkingLot` itself should be a Thread-Safe Singleton initialized via a thread-safe enum or double-checked locking.

**Q2: How do you handle concurrency in a Ticket Booking System (BookMyShow)?**
*Beginner:* I'd lock the database row so two people can't buy the same seat at the same time.
*SDE-2:* I'd implement Optimistic Locking using a `@Version` field in JPA. Both users read the seat status. When User A buys it, the version increments. When User B tries, JPA throws an `OptimisticLockException`. To handle the 5-minute hold timer during checkout, I'd cache the temporary lock in Redis with a TTL.
*Senior:* Database-level optimistic locking causes database churn during flash sales. I'd use Redis as the gatekeeper. When a user selects a seat, a Lua script atomically attempts to SET the key `seat:123` with `NX EX 300` (Not Exists, Expire 300s). Only the winner proceeds to the database. If they don't buy, the TTL naturally releases the seat.

**Q3: Apply Design Patterns to an Elevator System.**
*Beginner:* I'd use a loop to check if the elevator needs to go up or down, and arrays to track button presses.
*SDE-2:* The `Elevator` itself uses the **State Pattern** (Idle, MovingUp, MovingDown, DoorsOpen). The internal and external button presses are queued. A **Strategy Pattern** is used for the dispatching algorithm (e.g., SCAN algorithm vs Shortest Seek Time First) so it can be swapped out easily.
*Senior:* For a multi-elevator system, the external panels use the **Observer Pattern** or an EventBus to broadcast requests to a centralized `Dispatcher`. The Dispatcher requires a highly concurrent thread-safe design (like `PriorityBlockingQueue`) to sort floors dynamically. Threading is critical: one thread per elevator simulating physical movement, and listener threads for asynchronous button interrupts.

**Q4: Design an ATM Machine.**
*Beginner:* The ATM checks the card, asks for a PIN, connects to the bank, and gives cash if the balance is high enough.
*SDE-2:* The core of the ATM is the **State Pattern** (HasCard, AwaitingPIN, ReadyForTx, Dispensing). To handle dispensing different denominations (100s, 50s, 20s), I'd use the **Chain of Responsibility Pattern**. The $100 handler dispenses what it can and passes the remainder to the $50 handler.
*Senior:* Network reliability and transaction rollbacks are critical. The ATM acts as a client in a two-phase commit or uses compensating transactions. If cash jams while dispensing, the hardware emits an error event. The ATM's `DispenseState` must catch this hardware interrupt, initiate an immediate reversal API call to the bank, and transition to `OutOfServiceState`.

**Q5: Design a Splitwise algorithm (Debt Simplification).**
*Beginner:* Keep a list of all transactions. When you want to settle, calculate the total each person owes and create payments.
*SDE-2:* You model the users and debts as a directed graph. A owes B 10, B owes C 10. To simplify, you calculate the net balance for every user. You split users into two lists: Net Creditors and Net Debtors. You sort both lists by amount and greedily match the largest debtor with the largest creditor until all balances are 0.
*Senior:* The greedy matching algorithm operates in O(N log N) due to sorting, ensuring minimal transaction routing. For the domain model, `Expense` must support exact amounts, percentages, and equal splits via a `SplitStrategy` pattern. Concurrency matters when multiple group members add expenses simultaneously; I'd use optimistic locking on the `Group` entity to recalculate the materialized view of balances safely.

**Q6: What is the Singleton Pattern and how do you break it?**
*Beginner:* It's a way to write a class so that you can only ever create one object of it.
*SDE-2:* It ensures a class has one instance and provides a global point of access. You implement it by making the constructor private and providing a static `getInstance()` method. You break a standard singleton using Reflection (`setAccessible(true)` on the constructor) or Serialization (deserializing creates a new instance).
*Senior:* The safest implementation in Java is a single-element `enum`. The JVM inherently protects enums from reflection attacks and handles serialization safely without requiring `readResolve()`. If lazy loading is strictly required, the Initialization-on-Demand Holder idiom is preferred over Double-Checked Locking, as it leverages the classloader's innate thread-safety without `volatile` overhead.

**Q7: How do you use the Strategy Pattern in an E-Commerce system?**
*Beginner:* Instead of using massive if/else statements for different payment methods (Credit Card, PayPal), you create separate classes for each.
*SDE-2:* You define a `PaymentStrategy` interface with a `pay()` method. `CreditCardStrategy` and `PayPalStrategy` implement it. The `OrderProcessor` (the context) holds a reference to the interface. At runtime, you inject the specific strategy based on user selection, satisfying the Open/Closed Principle.
*Senior:* In a Spring Boot application, I implement the Strategy Pattern dynamically. I create an Enum for payment types. Each strategy implements a `supports(PaymentType)` method. I inject `List<PaymentStrategy>` into a Factory class. When a request arrives, the Factory streams through the list, finds the matching strategy, and executes it, meaning adding Crypto payments requires zero changes to core logic.

**Q8: Design a Vending Machine.**
*Beginner:* You need classes for Items, Coins, and the Machine itself. The machine checks if enough money is inserted and drops the item.
*SDE-2:* This is the textbook use case for the **State Pattern**. States include `NoCoinState`, `HasCoinState`, `DispensingState`. This prevents illegal operations (like trying to dispense before paying). Inventory is managed with a Map.
*Senior:* You must model the `Inventory` generically to hold an `Item` interface. Thread safety is irrelevant here as physical vending machines are inherently single-threaded per session. The critical design point is the `DispenseStrategy` for giving change, which mirrors the ATM's Chain of Responsibility to calculate coins efficiently while throwing custom `InsufficientChangeException`s to transition the machine back to `NoCoinState`.

**Q9: Design a Game of Chess.**
*Beginner:* Create an 8x8 grid. Create classes for Pawn, Knight, King, etc. Each piece knows how it is allowed to move.
*SDE-2:* The `Board` holds `Spot`s. Pieces extend an abstract `Piece` class with an abstract `boolean isValidMove(Board, Start, End)`. A `Game` class maintains the `Move` history and active `Player`. The logic loops, validating moves and updating state.
*Senior:* Move validation is highly complex due to board-state dependencies (e.g., castling requires knowing if the King has moved previously; en passant requires knowing the exact previous move). I'd use the **Command Pattern** for `Move` objects, making undo functionality trivial. The `Game` state machine must calculate "Check" after every command execution by simulating all opponent moves against the King's coordinate.

**Q10: Design a Library Management System.**
*Beginner:* You have Books, Users, and a system to track who borrowed what. If a book is returned late, charge a fine.
*SDE-2:* I separate `Book` (the abstract concept, "Harry Potter") from `BookItem` (the physical barcode copy). Users can place a `Reservation`. I'd use the **Observer Pattern** to notify users when a reserved `BookItem` is returned and becomes available.
*Senior:* Handling concurrency on `Reservation` is key. When a popular book is returned, 5 waitlisted users get notified. The first to click "checkout" wins. The checkout API must use optimistic locking or a distributed lock on the `BookItem` ID. Fines should be calculated dynamically via an asynchronous scheduled job running nightly, not synchronously at checkout.
