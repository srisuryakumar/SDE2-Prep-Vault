# Distributed Systems and Messaging
### From CAP Theorem to Production Kafka

*A practical guide for engineers who can build a Spring Boot REST API but have never
had to think about what happens when the network between two machines disappears.*

---

## How to use this book

Every chapter follows the same shape: a **failure scenario** that motivates the concept,
the **concept itself**, **working code** where applicable, an **ASCII diagram** where it
helps, and an **interview section** you can use to check whether the idea actually stuck.

You don't need a cluster to read this book. You need to understand *why* clusters behave
the way they do — so that when production pages you at 3 a.m. with "replication lag is
climbing" or "the consumer group won't rebalance," you already know what's happening
before you open a single dashboard.

---

## Table of Contents

1. [Why Distributed Systems?](#chapter-1-why-distributed-systems)
2. [CAP Theorem](#chapter-2-cap-theorem)
3. [Consistency Models](#chapter-3-consistency-models)
4. [Replication](#chapter-4-replication)
5. [Partitioning and Sharding](#chapter-5-partitioning-and-sharding)
6. [Apache Kafka — Complete Guide](#chapter-6-apache-kafka--complete-guide)
7. [Distributed Transactions](#chapter-7-distributed-transactions)
8. [Event Sourcing and CQRS](#chapter-8-event-sourcing-and-cqrs)
9. [Spring Cloud Microservices](#chapter-9-spring-cloud-microservices)

---

# Chapter 1: Why Distributed Systems?

## 1.1 The machine you already understand

You've built a Spring Boot app. It runs on one machine. It has one JVM, one database
connection pool, one filesystem. When a request comes in, it's handled by a thread on
*that* machine, reading from memory or disk on *that* machine. If something goes wrong,
you SSH into *that* machine and look at *its* logs.

This mental model is simple because it has a property distributed systems don't have:
**everything either happens or it doesn't, and you always know which.** A method call
either returns a value or throws an exception. There's no in-between state where you're
not sure if it ran.

## 1.2 Why a single machine eventually isn't enough

Three walls show up as you grow:

**1. CPU and memory have a ceiling.** A single machine tops out — cloud providers sell
instances up to a few terabytes of RAM and a few hundred cores, but at some point you're
paying exponentially more for linear gains, and eventually the hardware simply doesn't
exist at any price.

**2. A single machine is a single point of failure.** Disks fail. Power supplies fail.
Data centers lose power. If your entire system lives on one machine, the *expected*
question isn't "will it go down" — it's "when," and "what happens to my data when it does."

**3. Your users are not all next to your data center.** A user in Singapore talking to a
server in Virginia pays for the speed of light, every request. No amount of CPU fixes
that. You need a copy of the data closer to them.

**The fix that creates the problem this whole book is about:** instead of one bigger
machine, you use more machines. This is **horizontal scaling**. It solves the three walls
above — and introduces a new category of problem that didn't exist before: now your
system's correctness depends on a *network* you don't control, connecting machines that
can each fail *independently* and *invisibly*.

## 1.3 What breaks the moment you add a second machine

Imagine the simplest possible distributed operation: Service A calls Service B over HTTP
to check if an order can be fulfilled.

```
Service A  ----HTTP request---->  Service B
Service A  <---HTTP response----  Service B
```

On one machine, a function call either returns or throws, instantly, every time. Across
a network, here is what can actually happen:

```
Case 1: Normal                  Case 2: Request lost         Case 3: Response lost
A ---req--->  B                 A ---req--->  X (dropped)    A ---req--->  B
A <--resp---  B                 A  (times out, retries)      B  (processes order!)
                                                               A <--X-------(dropped)
                                                               A  (times out, retries —
                                                                   did B already do it?)
```

In Case 3, **A cannot tell the difference between "B never got my request" and "B got it,
processed it, and the response got lost."** If A retries, and B already fulfilled the
order, you've just shipped two orders. This single fact — that failure is *ambiguous*
across a network — is the seed of almost every hard problem in this book: idempotency
keys (Chapter 7), exactly-once semantics (Chapter 6), and the entire reason consensus
systems like ZooKeeper exist (Chapter 2).

New problems that simply don't exist on a single machine:

| Problem | Single machine | Distributed system |
|---|---|---|
| **Network latency** | Memory access: ~100ns | Network round-trip: 0.5ms–200ms+, and *variable* |
| **Partial failure** | Process either runs or doesn't | One node can fail while others keep running, mid-operation |
| **Message ordering** | Instructions execute in program order | Messages can arrive out of order, or be duplicated |
| **Consistency** | One copy of the truth | Multiple copies of data that can disagree |

## 1.4 The Eight Fallacies of Distributed Computing

In the 1990s, engineers at Sun Microsystems (L Peter Deutsch and others) catalogued the
assumptions that newcomers to distributed systems make — assumptions that are each false,
and each costly when believed:

1. **The network is reliable.** It isn't — packets get dropped, links flap, switches fail.
2. **Latency is zero.** It isn't — even "fast" networks add milliseconds you must account for.
3. **Bandwidth is infinite.** It isn't — large payloads compete for finite pipe capacity.
4. **The network is secure.** It isn't — assume hostile actors can observe and inject traffic.
5. **Topology doesn't change.** It does — nodes are added, removed, and rerouted constantly.
6. **There is one administrator.** There isn't — you depend on networks, DNS providers, and
   cloud regions you don't control.
7. **Transport cost is zero.** It isn't — serialization, connection setup, and encryption all
   cost real CPU and time.
8. **The network is homogeneous.** It isn't — different links, protocols, and hardware behave
   differently under load.

Every chapter in this book is, in some sense, a strategy for surviving one or more of
these fallacies in production.

### Interview Section — Chapter 1

> **Q: Why would you choose a distributed system over scaling a single machine vertically?**
> A: Vertical scaling hits a hardware ceiling, creates a single point of failure, and can't
> reduce latency for geographically distant users. Horizontal scaling trades those problems
> for new ones — network unreliability, partial failure, and consistency — but those new
> problems are manageable with the right patterns, while "buy a bigger machine forever" is not.

> **Q: What is "partial failure" and why does it matter?**
> A: In a single process, a failure is total and immediately visible — the call throws.
> In a distributed system, one component can fail while the rest of the system keeps
> running, and the caller may not even know it happened. This is what makes failure
> *detection* in distributed systems as hard as failure *handling*.

> **Q: Give an example of a fallacy of distributed computing biting a real system.**
> A: Assuming "latency is zero" leads engineers to make chatty, synchronous calls between
> services (e.g., calling 5 downstream services sequentially per request) that work fine
> in a low-latency dev environment but collapse under real network conditions in production.

> **Q: Why can't a client tell the difference between a slow node and a dead node?**
> A: Both look identical from the outside: no response within the timeout window. This
> ambiguity is why distributed systems rely on techniques like heartbeats, timeouts tuned
> to the network's actual behavior, and consensus protocols rather than naive "did it respond" checks.

---

# Chapter 2: CAP Theorem

## 2.1 The scenario that forces the choice

You run a database with two nodes, replicating to each other, in two different data
centers. One night, the network link between the data centers goes down — a **network
partition**. Both nodes are alive. Both can still serve their local clients. They just
can't talk to each other.

```
   Data Center 1                    Data Center 2
  ┌──────────────┐                 ┌──────────────┐
  │   Node A      │   X---X---X    │   Node B      │
  │ balance=$100  │   (network     │ balance=$100  │
  │               │    partition)  │               │
  └──────────────┘                 └──────────────┘
        ▲                                 ▲
        │ withdraw $80                    │ withdraw $80
     Client 1                          Client 2
```

Both Client 1 and Client 2 try to withdraw $80 from the same account, at the same moment,
on opposite sides of the partition. Each node only sees its own request. If both nodes
say "yes, here's your money," the account just went to -$60 — the data is now
**inconsistent**. If a node instead says "I can't verify the other replica agrees, so I'm
refusing this request," it has just become **unavailable** to that client.

This is the entire CAP theorem in one scenario: **when a network partition happens, you
must choose between consistency and availability. You cannot have both.**

## 2.2 The three properties, precisely

- **Consistency (C):** every read receives the most recent write, or an error. All nodes
  see the same data at the same time.
- **Availability (A):** every request to a non-failing node receives a (non-error) response
  — without the guarantee that it contains the most recent write.
- **Partition Tolerance (P):** the system continues to operate despite an arbitrary number
  of messages being dropped or delayed between nodes.

## 2.3 The insight people miss: P isn't optional

Beginners read CAP as "pick any 2 of 3," as if you could build a CA system. You can't —
not in practice. Networks **will** partition: a switch fails, a cable gets cut, a cloud
region has a bad night. Partition tolerance isn't a design choice you opt out of; it's a
fact about networks you must design *around*. The real decision CAP forces on you is:

> **When a partition happens, do you sacrifice Consistency, or do you sacrifice Availability?**

```
                    CAP Theorem
                  ┌─────────────┐
                  │             │
            C ────┤  Pick one   ├──── A
         (Consistency)   when P happens   (Availability)
                  │             │
                  └──────┬──────┘
                         │
                         P
                 (Partition Tolerance —
                  not optional; networks
                  partition regardless
                  of what you "choose")
```

## 2.4 CP systems: refuse rather than risk being wrong

CP systems respond to a partition by **refusing requests** on the minority side (or any
side that can't confirm agreement), rather than risk serving stale or conflicting data.

**Examples:** ZooKeeper, etcd, HBase (for the operations that go through its strongly
consistent region servers).

```
Partition happens → minority side stops answering writes (sometimes reads too)
                  → majority side keeps working, requires quorum agreement
                  → once partition heals, minority resyncs
```

Use CP when being *wrong* is worse than being *unavailable* — leader election, distributed
locks, configuration that must never be split-brained (e.g., "which node is currently
the primary database").

## 2.5 AP systems: stay available, reconcile later

AP systems respond to a partition by **continuing to serve requests on both sides**,
accepting that the two sides may now hold different, conflicting versions of the data —
to be reconciled once the partition heals.

**Examples:** Cassandra, DynamoDB, CouchDB.

```
Partition happens → both sides keep accepting reads and writes independently
                  → data diverges between sides
                  → partition heals → conflict resolution (last-write-wins,
                    vector clocks, application-level merge)
```

Use AP when *availability* matters more than perfect consistency — shopping carts, social
media likes, presence/status indicators, analytics counters. A shopping cart that's
occasionally a write behind is fine; a shopping cart that refuses to load is a lost sale.

## 2.6 PACELC: the question CAP doesn't ask

CAP only describes behavior **during a partition**. But partitions are rare; most of the
time, your system is running normally, and you still face a trade-off: **consistency vs.
latency.** This is what **PACELC** adds:

> **If Partition (P), choose Availability (A) or Consistency (C); Else (E), choose Latency
> (L) or Consistency (C).**

So a full classification of a system looks like `PA/EL` (Cassandra: available during a
partition, low-latency normally) or `PC/EC` (a system like a traditionally configured
relational database with synchronous replication: consistent during a partition by
refusing, and consistent normally by paying the latency cost of confirming with replicas).

Why does the "else" branch matter? Because even with no partition at all, requiring a
write to be confirmed by a replica on another continent adds real latency on *every
single write* — that's a tax you pay constantly, not just during rare outages.

## 2.7 Real example: Cassandra's tunable consistency

Cassandra doesn't force you into a single point on the CAP spectrum — it lets you choose
per-query, via **consistency level (CL)**:

| Consistency Level | Behavior | Position on spectrum |
|---|---|---|
| `ONE` | Acknowledge as soon as **1** replica responds | Fastest, most available, weakest consistency |
| `QUORUM` | Acknowledge once **majority** of replicas respond (e.g., 2 of 3) | Balanced |
| `ALL` | Acknowledge only once **every** replica responds | Strongest consistency, least available — one slow/down replica blocks the whole write |

A common production pattern: write at `QUORUM`, read at `QUORUM`. With replication factor
3, that means 2 of 3 nodes must agree on both write and read — and because `2 + 2 > 3`,
the read and write quorums are guaranteed to overlap on at least one node, so a read is
guaranteed to see the latest acknowledged write. This is **strong consistency built out of
tunable, per-query knobs**, rather than a fixed system-wide property.

### Interview Section — Chapter 2

> **Q: "We chose a CA system." What's wrong with that statement?**
> A: Partition tolerance isn't optional in practice — networks partition regardless of
> what you design for. A system that claims to be CA either hasn't been tested under a
> real partition, or it actually becomes unavailable (sacrificing A) the moment a partition
> occurs, making it CP in disguise.

> **Q: Your team is building a distributed lock service. CP or AP, and why?**
> A: CP. A distributed lock that can be "available" but wrong (i.e., grants the same lock
> to two clients during a partition) defeats the entire purpose of a lock. Refusing to
> grant the lock during uncertainty is the correct, safe behavior — this is exactly why
> ZooKeeper and etcd are CP.

> **Q: Why does PACELC matter if your system rarely experiences partitions?**
> A: Because the consistency/latency trade-off applies during *normal* operation, which is
> nearly all the time — unlike the consistency/availability trade-off, which only applies
> during the rare partition window. PACELC captures the cost you're paying every day, not
> just during incidents.

> **Q: How does Cassandra let you move along the CAP spectrum without changing databases?**
> A: Through per-query consistency levels (`ONE`, `QUORUM`, `ALL`). Lower consistency
> levels favor availability and latency; higher levels favor consistency at the cost of
> latency and availability — letting different queries in the same application choose
> different trade-offs based on their actual requirements.

---

# Chapter 3: Consistency Models

## 3.1 The scenario: "but I just saved it!"

A user updates their profile photo. They refresh the page half a second later — and see
the *old* photo. They didn't do anything wrong; their write went to one replica, and their
read got routed to a different replica that hasn't caught up yet. They file a bug report:
"your app deletes my changes." It didn't. This is a **consistency model** problem, not a
bug — and which consistency model you chose determines whether this is expected behavior
or something you need to fix.

Consistency models exist on a spectrum from "behaves exactly like a single machine" (strong)
to "eventually agrees, with no real-time guarantee about when" (eventual). Stronger models
are easier to reason about and more expensive to provide; weaker models are cheaper and
faster but push complexity onto your application code.

## 3.2 Strong consistency (Linearizability)

**Guarantee:** every read reflects the most recent completed write, system-wide, and every
operation appears to take effect instantaneously at some point between when it was called
and when it returned. From the outside, the system behaves exactly as if there were only
one copy of the data.

```
Time:    t1          t2          t3
Write X=5 ───────────┘
                     Read X  →  must return 5 (never 4, never "stale")
                                 regardless of which replica answers
```

**Cost:** every operation typically needs to coordinate with a quorum or a single leader
before responding, which adds latency and reduces availability during partitions (this is
the "C" side of CAP).

**Use it for:** bank balances, inventory counts where overselling is unacceptable,
distributed locks, leader election.

## 3.3 Sequential consistency

**Guarantee:** weaker than linearizability. All operations from all clients appear to
happen in *some* single, agreed-upon sequential order — and each client's own operations
appear in the order that client issued them — but that order doesn't have to match
real-world (wall-clock) time. Two operations that happened at the "same time" from
different clients could be ordered either way, as long as everyone agrees on the same order.

**Use it for:** systems where global ordering matters more than that ordering matching
real time — e.g., a replicated log where every replica must process events in the same
order, even if that order isn't strictly "what happened first in physical time."

## 3.4 Causal consistency

**Guarantee:** operations that are **causally related** must be seen in the same order by
everyone; operations that are **independent (concurrent)** can be seen in different orders
by different observers.

**Concrete failure scenario without it:** User A posts a comment: "I'm pregnant!" User B
replies: "Congratulations!" A third user, due to replication lag and no causal ordering,
sees B's reply *before* A's original post — "Congratulations!" appears out of nowhere,
replying to nothing. Causal consistency prevents this: because B's reply causally depends
on having read A's post, the system guarantees no observer sees the reply without the post.

**Use it for:** social feeds, comment threads, collaborative editing — anywhere
"replies must follow the thing they reply to" matters, but unrelated updates can arrive
in any order without confusing anyone.

## 3.5 Eventual consistency

**Guarantee:** if no new writes occur, all replicas will *eventually* converge to the same
value — but there is no bound on how long "eventually" takes, and no guarantee about what
you'll see in the meantime.

```
Write X=5 to Replica A
   ↓ (replication, takes time)
Replica B still shows X=4  ← acceptable under eventual consistency
Replica C still shows X=4  ← acceptable under eventual consistency
   ... time passes ...
All replicas converge to X=5
```

This is the default model for **DynamoDB** and **Cassandra** (at lower consistency levels).
It's the cheapest model to provide — replicas don't have to coordinate before responding —
which is exactly why it scales so well horizontally.

**Use it for:** product catalog data, view counts, recommendation data — anywhere a brief
window of staleness is an acceptable trade for speed and availability.

## 3.6 Read-your-writes consistency

**Guarantee:** a specific guarantee on top of eventual consistency — after a client writes
a value, *that same client* will always see their own write on subsequent reads, even if
other clients might still see stale data.

**Concrete failure scenario without it:** a user updates their shipping address, hits
"save," and is immediately taken to "review your order" — which reads from a replica that
hasn't caught the update yet and shows the *old* address. The user assumes the save
silently failed.

**Common fix:** route a user's reads to the leader (or the replica that handled their
write) for a short window after they write — Chapter 4 covers this in the replication
context.

## 3.7 Monotonic reads

**Guarantee:** once a client has seen a particular value, it will never subsequently see
an *older* value, even on a later read.

**Concrete failure scenario without it:** a user refreshes a comment thread, sees a new
comment posted by someone else, refreshes again (request lands on a replica with more lag)
— and the comment they just saw has disappeared. To the user, this looks like the app is
"forgetting" data, even though no data loss actually occurred — it's purely a result of
which replica each request happened to hit.

**Common fix:** consistently route a single client's reads to the same replica (sticky
sessions), or use a session token that tracks "the most recent write/read version this
client has seen" and require replicas to be at least that fresh before answering.

### Interview Section — Chapter 3

> **Q: What's the difference between sequential consistency and linearizability?**
> A: Linearizability requires the agreed-upon order of operations to match real wall-clock
> time — if operation A finishes before operation B starts, A must be ordered before B.
> Sequential consistency only requires *some* global order that respects each client's own
> program order; it doesn't have to match real time, which makes it cheaper to implement.

> **Q: A user updates their bio and immediately reloads the page, only to see their old
> bio. What consistency guarantee is missing, and how would you fix it?**
> A: Read-your-writes consistency. Fix it by routing that user's subsequent reads to the
> leader (or the same replica that processed the write) for a short time window, or by
> having the client pass along a "write version" token that reads must be at least as
> fresh as.

> **Q: Why is eventual consistency acceptable for a product view counter but not for an
> account balance?**
> A: A view counter being briefly stale or even slightly wrong has no real consequence —
> nobody's harmed if it's off by a few. An account balance being wrong, even briefly,
> can let a user withdraw money that isn't there, or be denied money that is — the cost of
> staleness is asymmetric, so the use case dictates which model is appropriate.

> **Q: How does causal consistency differ from full strong consistency, and why would you
> choose it?**
> A: Strong consistency orders *all* operations system-wide, which requires expensive
> coordination on every write. Causal consistency only orders operations that are
> *causally dependent* (e.g., a reply must follow its parent post) and allows independent
> operations to be seen in any order — giving you the guarantee users actually notice
> (no out-of-order replies) at a fraction of the coordination cost.

---

# Chapter 4: Replication

## 4.1 Why replicate at all

Three independent reasons, and you usually want all three:

- **Fault tolerance:** if data lives on only one node and that node dies, the data is gone.
  Multiple copies mean the system survives losing a node.
- **Read scaling:** one node can only serve so many reads per second. Spread reads across
  multiple copies of the data and you multiply your read capacity.
- **Geographic distribution:** a copy of the data physically close to your users in Tokyo
  means Tokyo users aren't paying the latency cost of round-tripping to a server in Virginia.

## 4.2 Leader-Follower (Master-Replica) replication

The most common topology. One node — the **leader** — accepts all writes. The rest —
**followers** — replicate the leader's changes and (usually) serve reads.

```
                  WRITES
                    │
                    ▼
              ┌───────────┐
              │  Leader   │
              └─────┬─────┘
            replicate│replicate
         ┌───────────┼───────────┐
         ▼           ▼           ▼
   ┌──────────┐┌──────────┐┌──────────┐
   │Follower 1││Follower 2││Follower 3│
   └──────────┘└──────────┘└──────────┘
         ▲           ▲           ▲
        READS       READS       READS
```

This guarantees write ordering is unambiguous (there's only one place writes can happen),
which sidesteps the conflict problem entirely — at the cost of the leader being a
bottleneck for writes and a single point of failure until a new leader is elected.

### Synchronous replication

The leader waits for at least one follower to acknowledge the write before confirming
success to the client.

```
Client → Leader: write X=5
Leader → Follower: replicate X=5
Leader ← Follower: ACK
Leader → Client: write confirmed
```

- **Pro:** if the leader dies the instant after confirming, the data is *not* lost — at
  least one follower has it.
- **Con:** write latency now includes a network round trip to the follower. If that
  follower is slow or unreachable, the leader can't confirm the write at all — availability
  drops with the slowest synchronous follower.

### Asynchronous replication

The leader confirms the write to the client immediately, and replicates to followers in
the background, with no wait.

```
Client → Leader: write X=5
Leader → Client: write confirmed   (immediately)
Leader → Follower: replicate X=5   (happens after, in background)
```

- **Pro:** fast writes — client latency isn't tied to follower latency at all.
- **Con:** if the leader dies *before* the follower receives the replicated write, that
  write is lost forever, even though the client was already told it succeeded.

Most production systems use a hybrid: one synchronous follower (for durability guarantees)
and the rest asynchronous (for read scaling without the latency tax on every write).

### Replication lag and stale reads

Because followers apply changes after the leader, there's always some window — usually
milliseconds, but it can spike to seconds or more under load — where a follower's data is
behind the leader's. A read routed to a lagging follower can return stale data, which is
exactly the read-your-writes problem from Chapter 3.

**The fix:** route a user's reads to the leader (or a follower confirmed to be caught up)
for a window of time right after that user writes — typically by tracking "last write
timestamp per user" and comparing it against each follower's "last applied timestamp."

## 4.3 Multi-Leader replication

Instead of one leader, **multiple nodes can each accept writes** — typically one leader
per data center, so each region writes locally with low latency, then replicates to the
other leaders.

```
   Data Center 1                       Data Center 2
  ┌────────────┐                      ┌────────────┐
  │  Leader A   │◄──── replicates ───►│  Leader B   │
  └────────────┘                      └────────────┘
        ▲                                    ▲
     writes from                         writes from
     US users                            EU users
```

This solves the "every write has to cross an ocean" latency problem multi-region single-leader
systems suffer from — but introduces **write conflicts**: if a US user and an EU user
update the *same record* on their respective leaders before replication catches up, the
two leaders now disagree, and something has to resolve the conflict (last-write-wins by
timestamp, a custom merge function, or surfacing the conflict to the application).

## 4.4 Leaderless replication (Dynamo-style)

No leader at all. A client writes to **N** replicas directly and considers the write
successful once **W** of them acknowledge. A client reads from **R** replicas and uses
the most recent value among the responses.

```
        Client writes X=5
       /        |        \
      ▼         ▼         ▼
  Replica1   Replica2   Replica3      (N=3)
   ACK ✓      ACK ✓      (slow)       Write succeeds once W=2 ACK
```

**Tuning N, R, and W is the core decision of a leaderless system:**

| Configuration | Behavior |
|---|---|
| `W + R > N` | Read and write sets are guaranteed to overlap on at least one node → you're guaranteed to read the latest write (strong-ish consistency) |
| `W + R ≤ N` | Read and write sets might not overlap → you might read stale data, but you get more availability and lower latency |

Example: `N=3, W=2, R=2` → `2+2=4 > 3`, so reads are guaranteed to see the latest
acknowledged write, while still tolerating one node being down for either a read or a
write. This is the same idea as Cassandra's `QUORUM` consistency level from Chapter 2 —
leaderless replication is *why* Cassandra can offer tunable consistency per query.

### Interview Section — Chapter 4

> **Q: Why would you ever choose asynchronous replication, given that it can lose data?**
> A: Because synchronous replication ties your write latency (and your availability) to
> the slowest synchronous follower. For workloads where occasional data loss on a rare
> leader crash is an acceptable trade for consistently fast writes — e.g., logging,
> analytics events — async wins. For data where loss is unacceptable — payments — you pay
> the latency cost and go synchronous, at least for one replica.

> **Q: What causes replication lag, and what's a concrete user-facing symptom of it?**
> A: Lag comes from the time it takes a follower to receive and apply changes after the
> leader processes them — worse under high write load or slow network links. The
> user-facing symptom is a stale read: a user submits a change, immediately re-reads, and
> sees the old value because their read was routed to a follower that hasn't caught up.

> **Q: How does multi-leader replication solve a problem single-leader can't, and what
> does it cost you?**
> A: It lets each region accept writes locally instead of round-tripping every write to a
> single leader in one location, cutting write latency for geographically distributed
> users. The cost is conflict: two leaders can each accept a write to the same record
> before they've synced, and the system needs a conflict resolution strategy to reconcile them.

> **Q: In a leaderless system with N=3, what do W=1 and W=3 each optimize for?**
> A: W=1 optimizes for write availability and latency — only one replica has to be up and
> fast for a write to succeed, but you tolerate weaker durability and consistency. W=3
> optimizes for durability and consistency — all three replicas must acknowledge, so the
> write is well-protected, but the write fails or stalls if even one replica is slow or down.

---

# Chapter 5: Partitioning and Sharding

## 5.1 The scenario: replication alone isn't enough

Replication (Chapter 4) solves fault tolerance and read scaling — every node has a full
copy of the data. But what happens when the *entire dataset* is bigger than any single
node's disk? Replicating a 50TB dataset to a node with a 2TB disk doesn't work no matter
how many followers you add — every replica still needs to hold the *whole* dataset.

**Partitioning (sharding)** solves this differently: instead of every node holding all the
data, each node holds a *subset* of the data. Combined with replication, you get a system
where the data is both split across nodes (for size) and copied within each split (for
fault tolerance).

```
                    Full dataset (e.g., all users)
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Partition 1     Partition 2     Partition 3
        users A-H       users I-Q       users R-Z
       (own replicas)  (own replicas)  (own replicas)
```

## 5.2 Hash partitioning

The simplest approach: `partition = hash(key) % num_partitions`. A user's data always
lands on the same partition because the hash of their key never changes, and the
distribution is roughly even because a good hash function spreads keys uniformly.

**The problem:** when you add or remove a node, `num_partitions` changes — and because
it's the *denominator* in a modulo operation, **almost every key gets reassigned to a
different partition.**

```
Before (3 partitions): hash(key) % 3
Key "order-555": hash=12550 → 12550 % 3 = 1  → Partition 1

After adding a 4th partition: hash(key) % 4
Key "order-555": hash=12550 → 12550 % 4 = 2  → Partition 2  (moved!)
```

Nearly every key moves, which means a near-total data reshuffle across the cluster every
time you scale — exactly the operation you'd want to be *cheap* and frequent, but naive
hash partitioning makes it the most expensive operation you can perform.

## 5.3 Range partitioning

Instead of hashing, assign contiguous ranges of keys to partitions — e.g., by date:
"January's data on Partition 1, February's on Partition 2." Great for time-series data,
because queries like "give me last week's events" hit only one or two partitions instead
of scanning the whole cluster.

**The trade-off:** range partitioning can create **hot partitions** — if you're
partitioning by date and all of today's writes go to "today's partition," that one node
absorbs all current write traffic while yesterday's partition sits idle.

## 5.4 Consistent Hashing

Consistent hashing solves the rebalancing problem of naive hash partitioning: when you
add or remove a node, **only a fraction of keys move (roughly `1/N` of them), not nearly all of them.**

### The ring

Imagine hash output space (e.g., 0 to 2³²-1) arranged as a circle. Both **nodes** and
**keys** are hashed onto this same ring. A key belongs to the **first node found going
clockwise** from the key's position.

```
                         0 / 2³²
                          │
              Node D ─────┼───── Node A
             ╱                          ╲
            │          hash ring          │
            │     ●key1      ●key3        │
             ╲                          ╱
              Node C ─────┼───── Node B
                          │
                       (mid-point)

key1 → next clockwise node is A → stored on Node A
key3 → next clockwise node is B → stored on Node B
```

### Adding a node only moves ~1/N of the keys

```
Before adding Node E:                After adding Node E (between C and D):
... C ──────────── D ...             ... C ──── E ──── D ...
    all keys between C and D            keys between C and E now go to E
    go to D                             keys between E and D still go to D
                                        (only this slice moved — everything
                                         elsewhere on the ring is untouched)
```

This is the entire point of consistent hashing: a node join or leave only disrupts the
keys in its immediate *neighborhood* on the ring, not the entire keyspace.

### Virtual nodes

A naive ring with one position per physical node creates uneven load — a node might
randomly land on a large arc of the ring (owning a disproportionate share of keys) or a
tiny one. The fix: give each physical node **many positions on the ring** (100+ is
typical) — these are **virtual nodes**.

```
Physical Node A → hashed to ring positions: A-v1, A-v2, A-v3, ... A-v100
Physical Node B → hashed to ring positions: B-v1, B-v2, B-v3, ... B-v100
```

With virtual nodes, each physical node's "share" of the ring is the sum of 100+ small,
randomly distributed arcs instead of one large arc — averaging out to a much more even
distribution, and when one physical node fails, its load spreads across *many* other
nodes (the owners of the neighboring virtual nodes) instead of dumping entirely onto one
unlucky neighbor.

## 5.5 Hot spots

Even with perfectly even partitioning, you can still get a hot spot if your **access
pattern** — not your key distribution — is skewed. Classic example: a celebrity's account
on a social network gets 1000x the read/write traffic of an average user, and no matter
how you've partitioned, that one celebrity's partition is overwhelmed while every other
partition is idle.

**Strategies to prevent hot spots:**

- **Key salting:** append a random suffix to the hot key (e.g., `celebrity_id_1`,
  `celebrity_id_2`, ... `celebrity_id_10`) to split its writes across multiple physical
  partitions, then merge results on read.
- **Caching:** put a cache in front of hot keys so most reads never reach the partition at all.
- **Dedicated capacity:** detect known-hot keys and route them to partitions provisioned
  with extra capacity, rather than treating all partitions as equal.

### Interview Section — Chapter 5

> **Q: Why is naive `hash(key) % N` partitioning a problem when you scale the cluster?**
> A: Because `N` is the divisor, changing it (adding or removing a node) changes the
> result of the modulo for nearly every key, forcing a near-complete data reshuffle across
> the cluster — exactly when you're trying to scale, which should be a routine, low-cost operation.

> **Q: How does consistent hashing limit the data movement when a node is added?**
> A: Nodes and keys are both placed on a hash ring, and a key belongs to the next node
> clockwise from it. Adding a node only affects the contiguous arc of keys between it and
> its counter-clockwise neighbor — everywhere else on the ring is unaffected — so roughly
> `1/N` of keys move instead of nearly all of them.

> **Q: What problem do virtual nodes solve that plain consistent hashing doesn't?**
> A: Plain consistent hashing with one ring position per physical node can produce very
> uneven key distribution (one node randomly owns a large arc, another a tiny one) and
> concentrates a failed node's entire load onto a single neighbor. Virtual nodes spread
> each physical node across 100+ ring positions, evening out the distribution and
> spreading a failed node's load across many neighbors instead of one.

> **Q: A specific user's data is always queried far more than others, even though your
> partitioning is hash-based and even. What's happening, and how do you fix it?**
> A: This is a hot spot caused by access pattern skew, not key distribution skew — even
> partitioning doesn't prevent one key from being disproportionately *accessed*. Fixes
> include key salting (splitting that key's data across multiple partitions), caching in
> front of the hot key, or routing it to dedicated, over-provisioned capacity.

---

# Chapter 6: Apache Kafka — Complete Guide

## 6.1 The scenario: why Kafka exists

Service A (Order Service) needs to tell Service B (Inventory Service) that an order was
placed, via a direct HTTP call.

```
Order Service ──HTTP POST──► Inventory Service
                                    │
                              (down for deploy)
                                    ▼
                              Connection refused
                                    │
                                    ▼
                          Order Service request FAILS
                          → order placement fails too,
                            even though the order itself
                            was perfectly valid
```

This is **tight coupling disguised as a simple HTTP call**: Order Service's ability to
function now depends on Inventory Service being up, fast, and reachable, *at the exact
moment* the order is placed. Add a third consumer (Shipping Service, Analytics Service)
and Order Service now has to call all of them, synchronously, and is only as reliable as
the least reliable one.

**With Kafka in between:**

```
Order Service ──publish──► [ Kafka Topic: order-events ]
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            Inventory Service  Shipping Service  Analytics Service
            (consumes when     (consumes when     (consumes when
             ready)             ready)             ready)
```

Order Service publishes the event once and moves on — it never blocks on a downstream
service being available. If Inventory Service is down for a deploy, the message just sits
in Kafka until it comes back and consumes it. Order Service never even knows there was an
outage. This is **decoupling**: producers don't need to know who's consuming, how many
consumers there are, or whether they're currently up.

Kafka adds two more properties beyond simple decoupling: **persistence** (messages are
written to disk, not just held in memory, so a consumer that's down for hours can come
back and catch up) and **replay** (a new consumer, or one recovering from a bug, can
re-read the *entire* history of a topic from the beginning, not just see what happens from
"now" forward).

## 6.2 Kafka Architecture

```
┌──────────────────────────── Kafka Cluster ────────────────────────────┐
│                                                                         │
│   ┌─────────────── Broker 1 ───────────────┐  ┌────── Broker 2 ──────┐│
│   │  Topic: orders                          │  │  Topic: orders        ││
│   │  ┌─────────────────────────────────┐    │  │  ┌─────────────┐     ││
│   │  │ Partition 0 (LEADER)             │    │  │  │Partition 0  │     ││
│   │  │ [msg0][msg1][msg2][msg3][msg4]──►│    │  │  │ (REPLICA)   │     ││
│   │  │  offset:0  1    2    3    4      │    │  │  └─────────────┘     ││
│   │  └─────────────────────────────────┘    │  │                       ││
│   │  ┌─────────────────────────────────┐    │  │  ┌─────────────┐     ││
│   │  │ Partition 1 (REPLICA)            │    │  │  │Partition 1  │     ││
│   │  └─────────────────────────────────┘    │  │  │ (LEADER)    │     ││
│   │                                          │  │  └─────────────┘     ││
│   └──────────────────────────────────────────┘  └───────────────────────┘│
│                                                                         │
│              Cluster metadata + leader election: KRaft (or ZooKeeper) │
└─────────────────────────────────────────────────────────────────────┘
        ▲                                              │
        │ produce                                 consume│
        │                                              ▼
  ┌───────────┐                          ┌──────────────────────────┐
  │ Producers │                          │   Consumer Group: "inv"   │
  └───────────┘                          │  ┌─────────┐ ┌─────────┐ │
                                          │  │Consumer1│ │Consumer2│ │
                                          │  │(Part.0) │ │(Part.1) │ │
                                          │  └─────────┘ └─────────┘ │
                                          └──────────────────────────┘
```

**Core vocabulary:**

- **Broker:** a single Kafka server. A cluster is typically 3+ brokers. Each broker stores
  some subset of the cluster's partitions.
- **Topic:** a named stream of messages (e.g., `order-events`). Logically one stream;
  physically split into partitions for parallelism.
- **Partition:** an ordered, immutable, append-only log of messages. Once written, a
  message in a partition never changes. Each partition lives on one broker (the
  **leader** for that partition), with copies (**replicas**) on other brokers for fault
  tolerance.
- **Offset:** a message's position within its partition — an ever-increasing integer,
  like an array index. Offsets are only unique *within a partition*, not across the whole topic.
- **Consumer Group:** a set of consumers that share the work of reading a topic. Kafka
  guarantees each partition is read by **exactly one consumer within a given group** at a
  time — this is how Kafka parallelizes consumption while keeping per-partition ordering intact.
- **ZooKeeper / KRaft:** the system that tracks cluster metadata (which broker leads which
  partition, which brokers are alive) and runs leader election. ZooKeeper was Kafka's
  original dependency; **KRaft** (Kafka's own built-in Raft-based consensus, GA since Kafka
  3.x) removes the ZooKeeper dependency entirely — new Kafka deployments should use KRaft.

**Why partitions are the unit of parallelism, and the unit of ordering:** Kafka only
guarantees message order *within* a single partition, not across an entire topic. This is
a deliberate trade: a totally-ordered topic could only ever be processed by one consumer
at a time (no parallelism); splitting into partitions lets multiple consumers work in
parallel, at the cost of only guaranteeing order *per partition*.

## 6.3 Producers

A producer sends a message consisting of a **key**, a **value**, a **topic**, and
optionally an explicit **partition**.

**Partition selection:** if you don't specify a partition explicitly, Kafka computes it
from the key: `partition = hash(key) % numPartitions`. This means **messages with the
same key always land on the same partition** — which is exactly what you want, because
Kafka only guarantees order within a partition. Partitioning order updates for the same
`orderId` to the same partition guarantees those updates are processed in the order they
were sent.

```
producer.send("order-events", key="order-555", value=orderPlacedEvent)
producer.send("order-events", key="order-555", value=orderShippedEvent)
                     │
                     ▼
        Both hash to the same partition (same key)
                     │
                     ▼
        Partition 2: [orderPlacedEvent][orderShippedEvent]
        → consumer reads them in this exact order, guaranteed
```

**Acknowledgment levels (`acks`):** controls how many replicas must confirm a write
before the producer considers it successful — directly trading latency for durability,
the same trade-off you saw in Chapter 4's sync/async replication.

| `acks` | Behavior | Durability | Latency |
|---|---|---|---|
| `acks=0` | Fire-and-forget; producer doesn't wait for any confirmation | None — message can be silently lost | Fastest |
| `acks=1` | Leader writes the message to its own log and confirms; doesn't wait for replicas | Lost if leader fails before replicating | Fast |
| `acks=all` (`-1`) | Leader waits for all in-sync replicas to confirm | Strongest — survives leader failure | Slowest |

**Idempotent producer:** retries are necessary (the network can drop the ACK even though
the write succeeded — Chapter 1's ambiguity problem again) but naive retries can create
duplicate messages. Setting `enable.idempotence=true` has the producer tag each message
with a sequence number; the broker detects and silently drops duplicates from retries,
giving you exactly-once delivery *for the producer→broker hop* without you writing any
deduplication code.

### Interview Section — Producers

> **Q: Why does sending with the same key matter, beyond just "even distribution"?**
> A: It guarantees ordering. Kafka only orders messages within a partition, and hashing by
> key sends all messages for the same logical entity (e.g., the same order) to the same
> partition — so a consumer always sees that entity's events in the order they were produced.

> **Q: When would you use `acks=1` instead of `acks=all`?**
> A: When throughput and latency matter more than surviving a leader crash exactly at the
> worst moment — e.g., high-volume clickstream or metrics events where losing a rare
> message on a leader failure is an acceptable trade for significantly higher throughput.
> For anything where losing a message is a real business problem (payments, orders), use `acks=all`.

> **Q: What problem does `enable.idempotence=true` solve, and what does it NOT solve?**
> A: It solves duplicate messages caused by producer retries after an ambiguous failure
> (the write succeeded but the ACK was lost). It does **not** solve duplicates caused by
> the producer itself being restarted and re-sending application-level data, nor does it
> give you exactly-once all the way through to the consumer — that requires Kafka
> transactions, covered later in this chapter.

---

## 6.4 Consumers

Consumers don't get pushed messages — they **poll**. This is a deliberate design choice:
pull-based consumption lets each consumer control its own pace, which means a slow
consumer can't be overwhelmed the way it could be if a broker pushed messages at the
broker's pace.

```
while (true) {
    records = consumer.poll(Duration.ofMillis(500));  // pull batch
    for (record : records) {
        process(record);                              // do the work
    }
    consumer.commitSync();                             // mark as processed
}
```

**Auto commit vs. manual commit — the risk of each:**

- **Auto commit** (`enable.auto.commit=true`): Kafka periodically commits the latest
  offset automatically, on a timer, regardless of whether you've actually finished
  processing the message. **Risk:** if your app crashes *after* the auto-commit fires but
  *before* processing finishes, that message is silently skipped on restart — you've lost
  it without an error.
- **Manual commit**: you call `commitSync()` or `commitAsync()` yourself, **after**
  processing succeeds. **Risk if done wrong:** if you commit before processing instead of
  after, you have the same problem as auto-commit. Done correctly (commit *after* successful
  processing), manual commit gives you **at-least-once** delivery — a crash before commit
  means the message is re-delivered and re-processed, which is why your processing logic
  needs to be idempotent (Chapter 7).

**Consumer group rebalancing:** when a consumer joins or leaves a group (deploy, crash,
scale-up), Kafka must reassign partitions among the remaining/new consumers.

```
Before: Consumer1→[P0,P1]  Consumer2→[P2,P3]
Consumer2 crashes
Rebalance: Consumer1→[P0,P1,P2,P3]   ← Consumer1 now owns everything,
                                        until a new consumer joins
```

- **Eager rebalancing (legacy default):** *all* consumers in the group stop consuming,
  every partition is revoked, then reassigned from scratch — a brief "stop-the-world"
  pause for the entire group, even for consumers whose partition assignment doesn't change.
- **Cooperative rebalancing** (Kafka 2.4+, `CooperativeStickyAssignor`): only the
  partitions that actually need to move are revoked and reassigned; consumers keep
  processing their unaffected partitions throughout. This dramatically reduces the
  disruption of routine scaling events and deploys.

**Consumer lag** is the single most important Kafka operational metric: the difference
between the latest offset produced to a partition and the offset the consumer group has
committed.

```
Partition log: [0][1][2][3][4][5][6][7][8][9]  ← latest offset = 9
Consumer group committed offset: 4
Consumer lag = 9 - 4 = 5 messages behind
```

Rising lag means your consumer can't keep up with the producer — either it's too slow
(processing logic needs optimizing, or you need more consumer instances / partitions), or
it's down. **Alert on lag growing unboundedly**, not on lag existing at all (a small,
stable lag is completely normal); the danger signal is the trend, not the absolute number.

---

## 6.5 Spring Kafka — Complete, Working Code

**`pom.xml` dependencies:**

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

**The event we'll be sending — `OrderEvent.java`:**

```java
package com.example.orders.event;

import java.math.BigDecimal;
import java.time.Instant;

public record OrderEvent(
        String orderId,
        String customerId,
        BigDecimal amount,
        String status,
        Instant occurredAt
) {}
```

### 6.5.1 `KafkaTemplate` — sending messages (sync and async)

```java
package com.example.orders.producer;

import com.example.orders.event.OrderEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;
import org.springframework.stereotype.Service;
import org.springframework.util.concurrent.ListenableFuture;

@Service
public class OrderEventProducer {

    private static final Logger log = LoggerFactory.getLogger(OrderEventProducer.class);
    private static final String TOPIC = "order-events";

    private final KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public OrderEventProducer(KafkaTemplate<String, OrderEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    /**
     * Asynchronous send (recommended default) — does not block the calling thread.
     * Key = orderId, so all events for the same order land on the same partition
     * and are guaranteed to be processed in order.
     */
    public void sendAsync(OrderEvent event) {
        kafkaTemplate.send(TOPIC, event.orderId(), event)
                .whenComplete((result, ex) -> {
                    if (ex != null) {
                        log.error("Failed to send order event {}: {}", event.orderId(), ex.getMessage(), ex);
                    } else {
                        log.info("Sent order event {} to partition {} at offset {}",
                                event.orderId(),
                                result.getRecordMetadata().partition(),
                                result.getRecordMetadata().offset());
                    }
                });
    }

    /**
     * Synchronous send — blocks until the broker acknowledges (per the configured
     * acks setting) or the request times out. Use sparingly: this reintroduces the
     * latency coupling Kafka exists to remove, but is sometimes required when the
     * caller must know for certain the event was durably published before continuing.
     */
    public SendResult<String, OrderEvent> sendSync(OrderEvent event) throws Exception {
        return kafkaTemplate.send(TOPIC, event.orderId(), event).get(); // .get() blocks
    }
}
```

**Producer configuration — `application.yml` excerpt:**

```yaml
spring:
  kafka:
    producer:
      bootstrap-servers: localhost:9092
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.springframework.kafka.support.serializer.JsonSerializer
      acks: all                       # wait for all in-sync replicas — durability first
      properties:
        enable.idempotence: true      # dedupe on retry, prevents duplicate sends
        retries: 5
        max.in.flight.requests.per.connection: 5   # safe with idempotence enabled
```

### 6.5.2 `@KafkaListener` — consuming messages

```java
package com.example.inventory.consumer;

import com.example.orders.event.OrderEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class InventoryReservationListener {

    private static final Logger log = LoggerFactory.getLogger(InventoryReservationListener.class);

    @KafkaListener(
            topics = "order-events",
            groupId = "inventory-service",     // consumer group — see Chapter 6.2/6.4
            containerFactory = "kafkaListenerContainerFactory"
    )
    public void onOrderEvent(OrderEvent event) {
        log.info("Reserving inventory for order {}", event.orderId());
        // ... business logic ...
    }
}
```

### 6.5.3 Manual acknowledgment

Auto-commit (Section 6.4) risks silently dropping messages on a crash mid-processing.
Manual acknowledgment fixes this by only committing the offset **after** processing
completes successfully:

```yaml
spring:
  kafka:
    consumer:
      bootstrap-servers: localhost:9092
      group-id: inventory-service
      auto-offset-reset: earliest
      enable-auto-commit: false        # we control commits ourselves
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.springframework.kafka.support.serializer.JsonDeserializer
      properties:
        spring.json.trusted.packages: "com.example.orders.event"
    listener:
      ack-mode: manual_immediate       # required for manual Acknowledgment.acknowledge()
```

```java
package com.example.inventory.consumer;

import com.example.orders.event.OrderEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.support.Acknowledgment;
import org.springframework.stereotype.Component;

@Component
public class ManualAckInventoryListener {

    private static final Logger log = LoggerFactory.getLogger(ManualAckInventoryListener.class);

    @KafkaListener(topics = "order-events", groupId = "inventory-service")
    public void onOrderEvent(OrderEvent event, Acknowledgment acknowledgment) {
        try {
            reserveInventory(event);           // do the real work first
            acknowledgment.acknowledge();      // ONLY commit after success
        } catch (Exception ex) {
            log.error("Failed processing order {}, NOT acknowledging — will redeliver", event.orderId(), ex);
            // do not acknowledge: message will be redelivered on the next poll/rebalance
            throw ex; // re-throw so the error handler (Section 6.5.4/6.5.5) can route to retry/DLQ
        }
    }

    private void reserveInventory(OrderEvent event) {
        // ... business logic that can throw ...
    }
}
```

### 6.5.4 `@RetryableTopic` — automatic retry + Dead Letter Queue (full example)

Manually wiring retry topics is tedious; `@RetryableTopic` generates the retry and DLQ
topics for you and handles the redelivery scheduling.

```java
package com.example.inventory.consumer;

import com.example.orders.event.OrderEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.DltHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.annotation.RetryableTopic;
import org.springframework.kafka.retrytopic.TopicSuffixingStrategy;
import org.springframework.kafka.support.KafkaHeaders;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.retry.annotation.Backoff;
import org.springframework.stereotype.Component;

@Component
public class RetryableInventoryListener {

    private static final Logger log = LoggerFactory.getLogger(RetryableInventoryListener.class);

    @RetryableTopic(
            attempts = "4",                                   // 1 original try + 3 retries
            backoff = @Backoff(delay = 1000, multiplier = 2.0), // 1s, 2s, 4s
            topicSuffixingStrategy = TopicSuffixingStrategy.SUFFIX_WITH_INDEX_VALUE,
            dltStrategy = org.springframework.kafka.retrytopic.DltStrategy.FAIL_ON_ERROR,
            include = { java.net.ConnectException.class, java.sql.SQLTransientException.class }
            // only retry transient failures — see "what NOT to retry" note below
    )
    @KafkaListener(topics = "order-events", groupId = "inventory-service")
    public void onOrderEvent(OrderEvent event) {
        log.info("Processing order {} (attempt may be a retry)", event.orderId());
        reserveInventory(event); // throws on transient failure → triggers retry topic
    }

    /**
     * Called automatically once all retries on order-events-retry-0/1/2 are exhausted.
     * The message has been routed to order-events-dlt (Dead Letter Topic).
     */
    @DltHandler
    public void onDeadLetter(OrderEvent event,
                              @Header(KafkaHeaders.EXCEPTION_MESSAGE) String exceptionMessage,
                              @Header(KafkaHeaders.ORIGINAL_TOPIC) String originalTopic) {
        log.error("Order {} exhausted all retries from topic {}. Reason: {}. Routing to manual review.",
                event.orderId(), originalTopic, exceptionMessage);
        // e.g., persist to a "failed_orders" table for manual ops review,
        // or page an on-call engineer for high-value orders.
    }

    private void reserveInventory(OrderEvent event) {
        // ... business logic ...
    }
}
```

**What happens topic-wise:** `@RetryableTopic` automatically creates
`order-events-retry-0`, `order-events-retry-1`, `order-events-retry-2`, and
`order-events-dlt` — each failed attempt republishes to the next retry topic with the
configured backoff delay, and the final failure lands on the DLT (Dead Letter Topic).

**What to do with messages on the DLQ:** never just delete them. Options, in order of how
mature your operational maturity needs to be:
1. **Log and alert** — minimum viable: someone gets paged, looks at the message, fixes it manually.
2. **Persist to a review table/dashboard** — ops can triage a backlog of failures async.
3. **Automated reprocessing** — once the root cause (e.g., a downstream outage) is fixed,
   a tool replays DLQ messages back onto the original topic.

**What NOT to retry:** only retry **transient** failures (network blips, brief downstream
unavailability). Don't retry on **deserialization errors** or **business logic
validation failures** (e.g., "order amount is negative") — retrying those just wastes
4 attempts producing the exact same guaranteed failure before landing on the DLQ anyway;
route them to the DLQ immediately instead.

### 6.5.5 Error handling: `DeadLetterPublishingRecoverer` + `DefaultErrorHandler`

For consumers *not* using `@RetryableTopic`, you wire error handling explicitly at the
container factory level. (Note: `SeekToCurrentErrorHandler` was Spring Kafka's pre-2.8
error handler; since Spring Kafka 2.8 it has been superseded by `DefaultErrorHandler`,
which does the same "seek back and retry" job with more configuration options — shown below.)

```java
package com.example.inventory.config;

import com.example.orders.event.OrderEvent;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory;
import org.springframework.kafka.core.*;
import org.springframework.kafka.listener.DeadLetterPublishingRecoverer;
import org.springframework.kafka.listener.DefaultErrorHandler;
import org.springframework.kafka.support.serializer.JsonDeserializer;
import org.springframework.util.backoff.FixedBackOff;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaConsumerErrorHandlingConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Bean
    public ConsumerFactory<String, OrderEvent> consumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "inventory-service");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, JsonDeserializer.class);
        props.put(JsonDeserializer.TRUSTED_PACKAGES, "com.example.orders.event");
        return new DefaultKafkaConsumerFactory<>(props);
    }

    @Bean
    public KafkaTemplate<String, Object> dlqKafkaTemplate(ProducerFactory<String, Object> pf) {
        return new KafkaTemplate<>(pf);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, OrderEvent> kafkaListenerContainerFactory(
            ConsumerFactory<String, OrderEvent> consumerFactory,
            KafkaTemplate<String, Object> dlqKafkaTemplate) {

        ConcurrentKafkaListenerContainerFactory<String, OrderEvent> factory =
                new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory);

        // After exhausting retries, publish the failed record to "<topic>.DLT"
        DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(dlqKafkaTemplate);

        // Retry 3 times, 1 second apart, then hand off to the recoverer above.
        // This is the modern equivalent of the legacy SeekToCurrentErrorHandler.
        DefaultErrorHandler errorHandler =
                new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L));

        // Don't waste retries on errors that will never succeed:
        errorHandler.addNotRetryableExceptions(
                com.fasterxml.jackson.core.JsonProcessingException.class,
                IllegalArgumentException.class
        );

        factory.setCommonErrorHandler(errorHandler);
        return factory;
    }
}
```

---

## 6.6 Kafka Advanced

### Schema Registry + Avro: why schemas matter

**The failure scenario without a schema registry:** Order Service adds a new field to its
event, renames `amount` to `totalAmount`, and deploys. Every consumer that was relying on
a field called `amount` now silently gets `null` (best case) or throws a deserialization
exception (worst case) — in production, with no warning before deploy.

**Schema Registry** (Confluent's, or compatible alternatives) stores a versioned schema
(typically **Avro**, sometimes Protobuf or JSON Schema) for each topic, and enforces a
**compatibility mode** on every new schema version a producer tries to register:

| Compatibility mode | Rule | Use when |
|---|---|---|
| **Backward** | New schema can read data written with the *previous* schema | Consumers upgrade before producers |
| **Forward** | Old schema can read data written with the *new* schema | Producers upgrade before consumers |
| **Full** | Both backward AND forward compatible | You can't control upgrade order at all |

A field rename like the scenario above would be **rejected at registration time** under
backward compatibility (because old consumers can't find `amount` anymore) — the bad
deploy never happens; you get a clear registry error instead, at build/deploy time, not a
3 a.m. page.

**Avro producer config (`application.yml`):**

```yaml
spring:
  kafka:
    producer:
      bootstrap-servers: localhost:9092
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
      properties:
        schema.registry.url: http://localhost:8081
```

```java
// Avro schema (order-event.avsc)
{
  "type": "record",
  "name": "OrderEvent",
  "namespace": "com.example.orders.avro",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "customerId", "type": "string" },
    { "name": "totalAmount", "type": "string" },
    { "name": "status", "type": "string" }
  ]
}
```

### Kafka Streams: stateful stream processing

Kafka Streams is a library (not a separate cluster — it runs inside your application) for
transforming, aggregating, and joining streams of events in real time.

- **`KStream`**: a stream of independent events (e.g., every individual order placed).
- **`KTable`**: a stream interpreted as a continuously-updated **table** keyed by record key
  — each new message *replaces* the previous value for that key, like a changelog.
- **Windowed aggregation**: grouping events into time buckets (e.g., "orders per 5-minute
  window") to compute rolling metrics without needing to query an external database.

```java
package com.example.analytics.streams;

import com.example.orders.event.OrderEvent;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.kstream.*;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.support.serializer.JsonSerde;

import java.time.Duration;

@Configuration
public class OrderAnalyticsStreamsConfig {

    @Bean
    public KStream<String, OrderEvent> orderStream(StreamsBuilder builder) {
        JsonSerde<OrderEvent> orderSerde = new JsonSerde<>(OrderEvent.class);

        KStream<String, OrderEvent> stream =
                builder.stream("order-events", Consumed.with(Serdes.String(), orderSerde));

        // KTable: latest order status per customer (changelog semantics)
        KTable<String, OrderEvent> latestOrderPerCustomer =
                stream.toTable(Materialized.with(Serdes.String(), orderSerde));

        // Windowed aggregation: order count per customer, per 5-minute tumbling window
        stream.groupByKey(Grouped.with(Serdes.String(), orderSerde))
                .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(5)))
                .count()
                .toStream()
                .foreach((windowedKey, count) ->
                        System.out.printf("Customer %s placed %d orders in window %s%n",
                                windowedKey.key(), count, windowedKey.window()));

        return stream;
    }
}
```

### Consumer lag monitoring with Kafdrop

**Kafdrop** is a free, open-source browser UI for inspecting Kafka clusters: topics,
partitions, messages, and — most operationally important — **consumer group lag**, without
writing any custom tooling.

```yaml
# docker-compose.yml excerpt
kafdrop:
  image: obsidiandynamics/kafdrop
  ports:
    - "9000:9000"
  environment:
    KAFKA_BROKERCONNECT: "kafka:9092"
```

In production, pair this with an actual alerting pipeline: export the
`kafka.consumer.records-lag-max` JMX metric (or use Kafka's `kafka-consumer-groups.sh
--describe` output) into Prometheus, and alert when lag is both **non-zero and increasing
over a sustained window** — a momentary lag spike during a deploy is normal; a lag that
keeps climbing for 10+ minutes means your consumers can't keep up.

### Exactly-once semantics

Kafka's default delivery guarantee is **at-least-once**: a message will never be silently
lost, but it might be delivered (and processed) more than once after a retry or a
crash-and-recover (Section 6.4). **Exactly-once semantics (EOS)** layers two mechanisms on
top to close that gap:

1. **Idempotent producer** (Section 6.3): prevents duplicate writes *from the producer to
   the broker* caused by network retries.
2. **Transactions**: let a consume-process-produce cycle (read from one topic, do work,
   write to another topic, AND commit the consumer offset) happen **atomically** — either
   the whole cycle is visible, or none of it is, even across a crash mid-cycle.

```java
@Bean
public ProducerFactory<String, OrderEvent> transactionalProducerFactory() {
    Map<String, Object> props = new HashMap<>();
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);
    props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "inventory-service-tx-");
    DefaultKafkaProducerFactory<String, OrderEvent> factory = new DefaultKafkaProducerFactory<>(props);
    factory.setTransactionIdPrefix("inventory-service-tx-");
    return factory;
}
```

```java
@Transactional("kafkaTransactionManager")
@KafkaListener(topics = "order-events", groupId = "inventory-service")
public void processAndForward(OrderEvent event) {
    InventoryReservedEvent reservation = reserveInventory(event); // business logic
    kafkaTemplate.send("inventory-events", event.orderId(), reservation);
    // Offset commit + the send above are committed together, atomically,
    // as one Kafka transaction — both happen, or neither does.
}
```

**Important scope limit:** "exactly-once" applies *within Kafka* — consume-transform-produce
cycles entirely inside the Kafka ecosystem. The moment you call an external system (a REST
API, a non-transactional database write) inside that listener, you're back to needing
idempotency at that external system's boundary too (Chapter 7).

## 6.7 Kafka Operations

### Topic creation: partitions and replication factor

```bash
kafka-topics.sh --create \
  --bootstrap-server localhost:9092 \
  --topic order-events \
  --partitions 6 \
  --replication-factor 3
```

- **Partitions** control your *maximum* consumer parallelism within a group — you can
  never have more *active* consumers in a group than partitions (extra consumers just sit
  idle). More partitions = more parallelism, but also more open files/connections per
  broker and slightly higher end-to-end latency for ordering guarantees per partition.
  Choosing too few partitions is far easier to fix later (by adding more) than choosing
  too many; under-provision slightly and grow as needed.
- **Replication factor** controls fault tolerance: a replication factor of 3 means each
  partition has 2 extra copies and can survive 2 broker failures without data loss. 3 is
  the standard production default; replication factor 1 means **zero** fault tolerance —
  losing that one broker loses that data, permanently.

### Retention

```yaml
# Per-topic config (or broker default)
retention.ms: 604800000      # 7 days (Kafka's default) — messages older than this are deleted
retention.bytes: -1          # size-based retention; -1 = unlimited (time-based only)
```

Retention is **not** "until consumed" — Kafka keeps messages for the configured time/size
window regardless of whether any consumer has read them. This is what enables replay
(Section 6.1): a new consumer group can start from the beginning and re-read everything
still within the retention window.

### Log compaction

Time-based retention deletes *old* messages. **Log compaction** (`cleanup.policy=compact`)
instead keeps only the **most recent value for each key**, deleting older values for that
same key — useful when a topic represents *current state* rather than a history of events.

```
Before compaction:                  After compaction:
offset 0: key=user1, value=v1       offset 2: key=user1, value=v3  (latest for user1)
offset 1: key=user2, value=v1       offset 3: key=user2, value=v2  (latest for user2)
offset 2: key=user1, value=v3
offset 3: key=user2, value=v2
```

Classic use case: a topic feeding a `KTable` (Section 6.6) of "current account balance per
user" — you don't need every historical balance, just the latest one per key, and
compaction keeps that topic from growing unboundedly forever while still letting a new
consumer rebuild the full current-state table by reading it from the start.

## 6.8 Full `application.yml` — Kafka + Schema Registry

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:9092

    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: io.confluent.kafka.serializers.KafkaAvroSerializer
      acks: all
      properties:
        enable.idempotence: true
        retries: 5
        max.in.flight.requests.per.connection: 5
        schema.registry.url: http://localhost:8081
        linger.ms: 5
        compression.type: snappy

    consumer:
      group-id: inventory-service
      auto-offset-reset: earliest
      enable-auto-commit: false
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: io.confluent.kafka.serializers.KafkaAvroDeserializer
      properties:
        schema.registry.url: http://localhost:8081
        specific.avro.reader: true
        spring.json.trusted.packages: "com.example.orders.event"

    listener:
      ack-mode: manual_immediate
      concurrency: 3              # parallel listener threads within this instance

    streams:
      application-id: order-analytics
      properties:
        default.key.serde: org.apache.kafka.common.serialization.Serdes$StringSerde
        default.value.serde: org.springframework.kafka.support.serializer.JsonSerde
        schema.registry.url: http://localhost:8081

# Schema Registry server itself (if self-hosting, not Confluent Cloud)
# kafka-schema-registry.properties:
#   listeners=http://0.0.0.0:8081
#   kafkastore.bootstrap.servers=PLAINTEXT://localhost:9092
#   kafkastore.topic=_schemas
#   schema.compatibility.level=backward
```

### Interview Section — Chapter 6

> **Q: A consumer is processing slower than the producer is publishing. What metric tells
> you this, and what are your options to fix it?**
> A: Consumer lag, growing over time. Options: scale out consumers (up to the number of
> partitions — beyond that, extra consumers sit idle, so you may also need to increase
> partition count), optimize the per-message processing logic, or move expensive
> processing (e.g., synchronous external API calls) out of the hot path into an async step.

> **Q: Why does `@RetryableTopic` create separate retry topics instead of just retrying in
> place?**
> A: Retrying in place blocks the partition — Kafka guarantees per-partition order, so a
> stuck message at the head of a partition blocks every message behind it from being
> processed, even unrelated ones. Routing failed messages to a separate retry topic lets
> the main topic keep flowing while the failed message waits out its backoff elsewhere.

> **Q: What's the actual difference between "at-least-once" and "exactly-once" in Kafka,
> and why doesn't enabling idempotence alone get you exactly-once end-to-end?**
> A: At-least-once guarantees no message is lost but allows duplicates from retries.
> Idempotent producers prevent duplicate *writes to the broker*, but a full
> exactly-once guarantee across consume→process→produce requires Kafka transactions to
> atomically tie the offset commit to the downstream produce — and even then, the
> guarantee only holds within Kafka; any external system you call inside that flow needs
> its own idempotency strategy.

> **Q: Why would you choose log compaction over time-based retention for a topic?**
> A: Use compaction when the topic represents current state keyed by ID (e.g., "current
> profile per user") where only the latest value per key matters and you want a new
> consumer to be able to rebuild full current state by reading from the start, without the
> topic growing forever. Use time-based retention for topics representing a true event
> history where you need every individual event for some bounded window (e.g., 7 days of
> audit events), not just the latest one per key.

---

# Chapter 7: Distributed Transactions

## 7.1 The scenario: a single business action spans three databases

Placing an order needs to: (1) deduct payment, (2) reserve inventory, (3) create a
shipment — and each lives in a *different* service with its *own* database. On a single
machine, this would just be a database transaction: all three writes commit together, or
none do. Across three services, there is no single database to wrap a transaction around.

```
Order Service        Payment Service       Inventory Service
     │                      │                      │
     ├──── charge $80 ─────►│                      │
     │                      │ SUCCESS              │
     ├──── reserve item ────┼──────────────────────►│
     │                      │                       │ FAILS (out of stock)
     │                      │                       │
     ▼
  Customer was charged $80 for an item that was never reserved.
  No single database transaction protects this whole sequence.
```

This chapter covers two different answers to "how do you keep this correct without a
single shared database": the classical, strict answer (**2PC**) and the pattern almost
all modern microservice systems actually use instead (**Sagas**).

## 7.2 Two-Phase Commit (2PC)

2PC coordinates a true atomic commit across multiple participants, using a central
**coordinator**.

```
PHASE 1 — Prepare (vote)
  Coordinator → Participant A: "Can you commit?"
  Coordinator → Participant B: "Can you commit?"
  Coordinator → Participant C: "Can you commit?"
  Each participant locks its resources, writes the change to a durable log
  (but does NOT yet make it visible), and replies YES or NO.

PHASE 2 — Commit (or abort)
  If ALL replied YES:
    Coordinator → all: "COMMIT"   → each participant makes the change visible, releases locks
  If ANY replied NO:
    Coordinator → all: "ABORT"    → each participant discards the change, releases locks
```

**The fatal weakness: coordinator failure leaves participants blocked.** If the
coordinator crashes *after* collecting all "YES" votes but *before* sending the final
"COMMIT," every participant is stuck holding locks on resources, unable to safely
proceed — they voted "yes," so they can't unilaterally abort (the coordinator might still
say commit once it recovers), and they can't unilaterally commit either (another
participant might have failed and never voted). This is why 2PC is called a **blocking
protocol**: a single coordinator failure can freeze the whole transaction indefinitely,
holding locks (and therefore blocking other operations on that data) until the coordinator
recovers.

This is a real cost in production: it's *why* 2PC, despite giving you true atomicity, is
rarely used across microservices — it directly conflicts with the goal of decoupling
services (Chapter 6.1) by tying their availability together at the exact moment of commit.

## 7.3 The Saga Pattern

A **saga** replaces one distributed transaction with a **sequence of local transactions**,
each in a single service's own database — and for every step, a **compensating
transaction** that can semantically undo it if a later step fails.

```
Step 1: Order Service  → create order (local tx, PENDING status)
Step 2: Payment Service → charge $80   (local tx)
Step 3: Inventory Service → reserve item (local tx)  ← FAILS, out of stock

Compensate, in reverse order:
Step 2': Payment Service → refund $80  (compensating tx)
Step 1': Order Service  → mark order CANCELLED (compensating tx)
```

Crucially, there's no global lock held across all three steps — each step commits
independently and immediately. If a later step fails, you don't roll back a transaction;
you run a **new, forward-moving transaction that undoes the effect** of an earlier one.
This is fundamentally different from a database rollback, and it's why "compensating
transaction" is the right mental model: refunding a charge is a *new* charge-reversal
action, not Payment Service un-happening the original charge.

### Choreography: services react to events

No central coordinator — each service publishes an event when it finishes its step, and
the next service(s) react to that event.

```
Order Service ──"OrderCreated"──► Kafka ──► Payment Service
                                                   │
                                          "PaymentCharged"
                                                   │
                                                   ▼
                                                 Kafka ──► Inventory Service
                                                                  │
                                                        "InventoryReserveFailed"
                                                                  │
                                                                  ▼
                                                                Kafka ──► Payment Service
                                                                          (compensates: refund)
                                                                              │
                                                                              ▼
                                                                            Kafka ──► Order Service
                                                                                      (compensates: cancel)
```

**Pro:** fully decoupled — no service needs to know the others exist, just which events to
react to. **Con:** the overall saga's logic ("what happens after what") is *implicit*,
scattered across every service's event handlers — hard to see the whole flow in one place,
and hard to debug "why did this order end up cancelled" without tracing events across
multiple services' logs.

### Orchestration: a central saga orchestrator

A dedicated orchestrator explicitly tells each service what to do, step by step, and
explicitly triggers compensations on failure.

```
                    ┌─────────────────────┐
                    │  Saga Orchestrator   │
                    └──────────┬───────────┘
           ┌────────────────────┼────────────────────┐
           ▼                    ▼                    ▼
    "charge $80"        "reserve item"         (on failure)
           │                    │              "refund $80"
           ▼                    ▼                    │
   Payment Service      Inventory Service             ▼
                          FAILS, replies          Payment Service
                          "out of stock"
                                │
                                ▼
                       Orchestrator decides:
                       compensate Payment, then
                       mark Order CANCELLED
```

**Pro:** the entire saga's flow lives in one place — easy to read, easy to add steps,
easy to debug. **Con:** the orchestrator becomes a service every other service depends on
for this flow, and it needs its own state tracking ("which step is this saga currently
on") — typically persisted so a crashed orchestrator can resume in-flight sagas correctly.

## 7.4 Full example: order creation saga with compensation

**Orchestrator (Spring Boot, using a simple state machine pattern):**

```java
package com.example.orders.saga;

public enum SagaStep { ORDER_CREATED, PAYMENT_CHARGED, INVENTORY_RESERVED, COMPLETED, COMPENSATING, FAILED }

@Entity
public class OrderSagaState {
    @Id
    private String orderId;
    @Enumerated(EnumType.STRING)
    private SagaStep currentStep;
    private BigDecimal amount;
    // getters/setters omitted
}
```

```java
package com.example.orders.saga;

import com.example.orders.event.*;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
public class OrderSagaOrchestrator {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final OrderSagaStateRepository sagaRepo;

    public OrderSagaOrchestrator(KafkaTemplate<String, Object> kafkaTemplate,
                                  OrderSagaStateRepository sagaRepo) {
        this.kafkaTemplate = kafkaTemplate;
        this.sagaRepo = sagaRepo;
    }

    public void startSaga(String orderId, String customerId, java.math.BigDecimal amount) {
        OrderSagaState state = new OrderSagaState();
        state.setOrderId(orderId);
        state.setAmount(amount);
        state.setCurrentStep(SagaStep.ORDER_CREATED);
        sagaRepo.save(state);

        kafkaTemplate.send("payment-commands", orderId,
                new ChargePaymentCommand(orderId, customerId, amount));
    }

    // Reacts to Payment Service's result
    public void onPaymentResult(PaymentResultEvent event) {
        OrderSagaState state = sagaRepo.findById(event.orderId()).orElseThrow();

        if (event.success()) {
            state.setCurrentStep(SagaStep.PAYMENT_CHARGED);
            sagaRepo.save(state);
            kafkaTemplate.send("inventory-commands", event.orderId(),
                    new ReserveInventoryCommand(event.orderId()));
        } else {
            state.setCurrentStep(SagaStep.FAILED);
            sagaRepo.save(state);
            kafkaTemplate.send("order-commands", event.orderId(),
                    new CancelOrderCommand(event.orderId(), "Payment declined"));
        }
    }

    // Reacts to Inventory Service's result
    public void onInventoryResult(InventoryResultEvent event) {
        OrderSagaState state = sagaRepo.findById(event.orderId()).orElseThrow();

        if (event.success()) {
            state.setCurrentStep(SagaStep.COMPLETED);
            sagaRepo.save(state);
            kafkaTemplate.send("order-commands", event.orderId(),
                    new ConfirmOrderCommand(event.orderId()));
        } else {
            // Inventory failed AFTER payment succeeded — compensate the payment.
            state.setCurrentStep(SagaStep.COMPENSATING);
            sagaRepo.save(state);
            kafkaTemplate.send("payment-commands", event.orderId(),
                    new RefundPaymentCommand(event.orderId(), state.getAmount(),
                            "Inventory unavailable: " + event.reason()));
        }
    }

    // Reacts to the compensating refund finishing
    public void onRefundResult(RefundResultEvent event) {
        OrderSagaState state = sagaRepo.findById(event.orderId()).orElseThrow();
        state.setCurrentStep(SagaStep.FAILED);
        sagaRepo.save(state);
        kafkaTemplate.send("order-commands", event.orderId(),
                new CancelOrderCommand(event.orderId(), "Compensated: inventory unavailable"));
    }
}
```

```java
@KafkaListener(topics = "payment-events", groupId = "order-saga")
public void handlePaymentEvent(PaymentResultEvent event) {
    orchestrator.onPaymentResult(event);
}

@KafkaListener(topics = "inventory-events", groupId = "order-saga")
public void handleInventoryEvent(InventoryResultEvent event) {
    orchestrator.onInventoryResult(event);
}

@KafkaListener(topics = "payment-events", groupId = "order-saga")
public void handleRefundEvent(RefundResultEvent event) {
    orchestrator.onRefundResult(event);
}
```

Notice: every step persists `OrderSagaState` to a database **before** sending the next
command. If the orchestrator crashes mid-saga, it can recover by reading the last
persisted step for any in-flight orders and resuming — this is what makes the saga
durable across orchestrator restarts, not just across the individual services.

## 7.5 Idempotency: the property that makes retries safe

Every pattern in this chapter — and in Chapter 6 — relies on **retries** to recover from
ambiguous failures (Chapter 1.3). Retries are only safe if the operation being retried is
**idempotent**: calling it twice with the same input has the same effect as calling it once.

**Idempotency key:** the client generates a unique ID for *this specific logical
operation* (not per HTTP request — per *intent*, so a retried request reuses the same key)
and sends it along. The server checks whether it's already processed that key before doing
the work.

```java
@PostMapping("/payments/charge")
public ResponseEntity<PaymentResult> charge(
        @RequestHeader("Idempotency-Key") String idempotencyKey,
        @RequestBody ChargeRequest request) {

    Optional<PaymentResult> existing = paymentRepo.findByIdempotencyKey(idempotencyKey);
    if (existing.isPresent()) {
        return ResponseEntity.ok(existing.get()); // already processed — return the same result
    }

    PaymentResult result = processCharge(request);
    paymentRepo.save(new Payment(idempotencyKey, result));
    return ResponseEntity.ok(result);
}
```

**Enforcing it at the database level**, not just in application logic, is what actually
makes this safe under concurrency (two retries arriving at nearly the same instant):

```sql
CREATE TABLE payments (
    id              BIGSERIAL PRIMARY KEY,
    idempotency_key VARCHAR(64) NOT NULL UNIQUE,   -- DB rejects the 2nd concurrent insert
    order_id        VARCHAR(64) NOT NULL,
    amount          DECIMAL(10,2) NOT NULL,
    status          VARCHAR(20) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT now()
);
```

If two retries race past the application-level `findByIdempotencyKey` check at the same
time (a real possibility — that check-then-act isn't atomic on its own), the **unique
constraint** is the actual safety net: the second `INSERT` fails with a constraint
violation, which the application catches and treats as "already processed, fetch and
return the existing result" instead of a real error.

This is the principle that ties Chapters 6 and 7 together:

> **At-least-once delivery (Kafka's default guarantee) + an idempotent consumer =
> effectively-once processing**, without needing the heavier machinery of distributed
> transactions or even Kafka's own transactional API.

### Interview Section — Chapter 7

> **Q: Why is 2PC rarely used between microservices in practice, despite guaranteeing true
> atomicity?**
> A: It's a blocking protocol — if the coordinator fails after collecting votes but before
> sending the final commit/abort decision, every participant is stuck holding locks
> indefinitely. This directly conflicts with the availability and independence
> microservices are built for, which is why sagas (eventual consistency with
> compensation) are preferred over strict cross-service atomicity in most systems.

> **Q: What's the actual difference between a saga's "compensating transaction" and a
> database "rollback"?**
> A: A rollback undoes an uncommitted change as if it never happened, atomically, within
> one transaction. A compensating transaction is a brand new, independent transaction that
> semantically reverses an *already-committed* change (e.g., issuing a refund instead of
> un-charging a card) — the original action did happen and is visible in history; the
> compensation is a separate, forward-moving action that cancels its effect.

> **Q: When would you choose saga orchestration over choreography?**
> A: Choose orchestration when the business process has many steps, conditional branches,
> or needs to be easy to observe/debug/modify in one place — the cost is an explicit
> orchestrator service that becomes a dependency. Choose choreography for simpler flows
> with few steps where you want maximum decoupling and don't want a central service every
> participant has to know about.

> **Q: Why isn't checking "has this idempotency key been used?" in application code
> enough, on its own, to guarantee no duplicate processing?**
> A: Because two retries can race: both can pass the "does it exist?" check before either
> has written its result, since check-then-act isn't atomic. A unique database constraint
> on the idempotency key is the actual guarantee — the database rejects the second insert
> outright, regardless of timing, and the application treats that rejection as "already handled."

---

# Chapter 8: Event Sourcing and CQRS

## 8.1 The scenario: "what was the account balance last Tuesday, and why?"

A traditional system stores **current state**: `accounts` table, `balance` column. Every
update overwrites the previous value. This works fine until someone asks: "the balance is
wrong — what sequence of changes led to this number?" The answer doesn't exist anywhere —
overwriting state also overwrote the history of *how* you got there. An audit, a dispute, a
bug investigation, all hit the same wall: the system only ever knew "now."

**Event Sourcing** inverts the storage model: instead of storing current state, you store
**every event that ever changed the state**, and current state is *derived* by replaying
those events.

```
Traditional (state-only):              Event Sourcing (events as the source of truth):
┌─────────────────┐                    ┌──────────────────────────────────┐
│ accounts         │                   │ events                            │
│ id=1, balance=80 │  ← only "now"     │ id=1: AccountOpened(balance=0)    │
└─────────────────┘                    │ id=2: Deposited(amount=100)       │
                                        │ id=3: Withdrawn(amount=20)        │
                                        └──────────────────────────────────┘
                                        current balance = replay all events = 0+100-20 = 80
```

## 8.2 Event Sourcing in practice

Instead of `UPDATE orders SET status = 'SHIPPED'`, you **append** an immutable event:
`OrderShipped { orderId, timestamp }`. The events table (or, naturally, a Kafka topic — see
Chapter 6) becomes the single source of truth; current state is a *view*, computed by
folding all events for an entity in order:

```java
public OrderState replay(List<OrderEvent> events) {
    OrderState state = OrderState.empty();
    for (OrderEvent event : events) {
        state = switch (event) {
            case OrderPlaced e   -> state.withStatus("PLACED").withAmount(e.amount());
            case PaymentReceived e -> state.withStatus("PAID");
            case OrderShipped e  -> state.withStatus("SHIPPED").withTrackingId(e.trackingId());
            case OrderCancelled e -> state.withStatus("CANCELLED");
            default -> state;
        };
    }
    return state;
}
```

**Benefits:**
- **Complete audit trail, for free.** "Why is this order's status SHIPPED" has a literal
  answer: replay its events and watch.
- **Replay history.** You can reconstruct state *as of any point in time* by replaying
  events only up to that timestamp — answering "what was the balance last Tuesday" exactly.
- **Temporal queries / debugging production issues.** Found a bug that corrupted state?
  Fix the replay logic and *re-derive* correct state from the original, untouched events
  — the raw events were never wrong, only your interpretation of them was.

**Trade-offs:**
- **Eventual read complexity.** Querying "give me all orders with status SHIPPED right
  now" by replaying every order's full event history on every query is far too slow —
  this is exactly the problem CQRS (next section) solves.
- **Snapshots needed for performance.** An entity with 100,000 events behind it shouldn't
  be replayed from event #1 every time you load it. Periodically persist a **snapshot**
  (the computed state at event #N) so loading only needs to replay events *since* the last
  snapshot, not the entire history.

```java
// Snapshot-aware loading
public OrderState load(String orderId) {
    Optional<OrderSnapshot> snapshot = snapshotRepo.findLatest(orderId);
    long fromVersion = snapshot.map(OrderSnapshot::version).orElse(0L);
    OrderState state = snapshot.map(OrderSnapshot::state).orElse(OrderState.empty());

    List<OrderEvent> eventsSinceSnapshot = eventStore.findByOrderIdAfterVersion(orderId, fromVersion);
    return replay(state, eventsSinceSnapshot); // only replay the delta
}
```

## 8.3 CQRS: Command Query Responsibility Segregation

Event sourcing solves *how to store changes*; CQRS solves *how to read them efficiently*
by splitting the system into two sides that are optimized independently:

```
                  ┌─────────────────────────────────────────┐
   COMMAND        │              WRITE SIDE                  │
   "Ship order     │   Command → validate → emit event       │
    #555"  ───────►│         (Event Store / Kafka)            │
                  └──────────────────┬────────────────────────┘
                                     │ events stream
                                     ▼
                  ┌─────────────────────────────────────────┐
                  │              READ SIDE                    │
   QUERY           │   Projection consumes events, updates    │
   "all shipped    │◄──   a read-optimized view (e.g., a      │
    orders" ────────   denormalized SQL table, Elasticsearch  │
                  │   index, or in-memory cache)              │
                  └─────────────────────────────────────────┘
```

- **Write side:** receives **commands** ("ShipOrder"), validates business rules, and on
  success emits **events** ("OrderShipped") — this is the event-sourced model from 8.2.
- **Read side:** **projections** subscribe to the event stream and continuously update one
  or more **read-optimized views** — denormalized, indexed however the actual queries
  need, with zero regard for how the write side is structured.

```java
@Component
public class ShippedOrdersProjection {

    private final ShippedOrderViewRepository viewRepo; // a plain, denormalized SQL/NoSQL table

    @KafkaListener(topics = "order-events", groupId = "shipped-orders-projection")
    public void onEvent(OrderEvent event) {
        if (event instanceof OrderShipped e) {
            // Denormalized, read-optimized — exactly the shape the query needs,
            // no joins required at query time.
            viewRepo.save(new ShippedOrderView(e.orderId(), e.customerId(),
                    e.trackingId(), e.shippedAt()));
        }
    }
}

@RestController
public class OrderQueryController {
    @GetMapping("/orders/shipped")
    public List<ShippedOrderView> getShippedOrders() {
        return viewRepo.findAll(); // fast: no replay, no joins, just an indexed read
    }
}
```

**Why split them at all:** write patterns and read patterns have fundamentally different
shapes. Writes care about *correctness* — validating a command against business rules
before accepting it as truth. Reads care about *speed and shape* — returning data in
exactly the structure a specific screen or API needs, often joined and denormalized in
ways that would be wasteful to maintain on the write side. Forcing one model to serve both
means every read either pays write-side normalization costs, or every write has to keep
multiple denormalized read views in sync inline, blocking the write itself. CQRS lets each
side scale, evolve, and be optimized completely independently — at the cost of the read
side being only **eventually consistent** with the write side (Chapter 3), since
projections update *after* an event is published, not within the same transaction.

### Interview Section — Chapter 8

> **Q: What's the core difference between traditional state storage and event sourcing?**
> A: Traditional storage keeps only the current state, overwriting history with every
> update. Event sourcing stores every event that ever caused a state change, and current
> state is *derived* by replaying those events — meaning the full history of how you got
> to "now" is preserved by construction, not as an afterthought.

> **Q: Why are snapshots necessary in an event-sourced system?**
> A: Without them, loading an entity's state requires replaying its *entire* event history
> from the beginning every single time, which gets prohibitively slow as the event count
> grows. A snapshot captures computed state at a point in time so loading only needs to
> replay events since that snapshot, not from the start.

> **Q: In CQRS, why is the read side typically "eventually consistent" rather than
> immediately consistent with the write side?**
> A: Because the read-side projection updates *after* it receives the event from the write
> side (often via something like Kafka), not within the same transaction as the write.
> There's an inherent, usually small, delay between a command succeeding and the
> corresponding read view reflecting it — the same eventual consistency trade-off from
> Chapter 3, applied within a single system's own write/read split.

> **Q: When would event sourcing + CQRS be overkill?**
> A: For simple CRUD domains where you don't need an audit trail, temporal queries, or
> truly distinct read/write scaling needs — the operational complexity of an event store,
> projections, and eventual consistency between them is a real cost that should be paid
> for with a real requirement, not applied by default to every domain.

---

# Chapter 9: Spring Cloud Microservices

## 9.1 The scenario: a REST client to a service that's flaky, not down

Order Service calls Shipping Service via a simple `RestTemplate` HTTP call. Shipping
Service isn't down — it's just **slow today**, taking 8 seconds to respond instead of its
usual 100ms, because of an unrelated downstream issue.

```
Order Service ──HTTP call──► Shipping Service (taking 8s instead of 100ms)
       │
       │  Order Service's thread is now BLOCKED for 8 seconds, waiting.
       │  If 50 requests/sec are calling this endpoint, you exhaust
       ▼  your entire thread pool in under a second — and Order Service,
   THREAD POOL          which has nothing wrong with it, goes down too,
   EXHAUSTED             purely from waiting on someone else's slowness.
```

This is **cascading failure**: one slow service drags down every service that calls it,
which drags down everything that calls *those*, and so on. Spring Cloud exists to give you
infrastructure-level answers to exactly this class of problem — discovery, configuration,
routing, and especially **resilience** — instead of every team reinventing timeout and
fallback logic ad hoc.

## 9.2 Spring Cloud Gateway

A single entry point that sits in front of all your services, so clients only need to know
one address, and cross-cutting concerns (auth, rate limiting, routing) live in one place
instead of being duplicated into every service.

```
                         ┌───────────────────────┐
   Client ───────────────►   Spring Cloud Gateway  │
                         │   - JWT validation       │
                         │   - rate limiting         │
                         │   - routing                │
                         └────────────┬──────────────┘
                  ┌───────────────────┼───────────────────┐
                  ▼                   ▼                   ▼
           Order Service      Payment Service      Inventory Service
```

**Route configuration — predicates and filters:**

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service-route
          uri: lb://order-service          # lb:// = load-balanced via service discovery
          predicates:
            - Path=/api/orders/**           # which requests this route matches
          filters:
            - StripPrefix=1                 # strip "/api" before forwarding
            - name: CircuitBreaker
              args:
                name: orderServiceCB
                fallbackUri: forward:/fallback/orders

        - id: payment-service-route
          uri: lb://payment-service
          predicates:
            - Path=/api/payments/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10   # tokens/sec refilled
                redis-rate-limiter.burstCapacity: 20    # max burst above the steady rate
                key-resolver: "#{@userKeyResolver}"     # rate limit PER USER
```

**JWT validation at the gateway** — validate the token once, here, so every downstream
service can trust the request has already been authenticated, instead of every service
re-implementing JWT parsing:

```java
package com.example.gateway.filter;

import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Component
public class JwtAuthenticationFilter implements GlobalFilter, Ordered {

    private final JwtValidator jwtValidator; // wraps your JWT library of choice

    public JwtAuthenticationFilter(JwtValidator jwtValidator) {
        this.jwtValidator = jwtValidator;
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String authHeader = exchange.getRequest().getHeaders().getFirst("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        String token = authHeader.substring(7);
        if (!jwtValidator.isValid(token)) {
            exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
            return exchange.getResponse().setComplete();
        }

        // Forward validated user identity downstream as a header,
        // so services trust it without re-validating the token themselves.
        ServerWebExchange mutated = exchange.mutate()
                .request(r -> r.header("X-User-Id", jwtValidator.extractUserId(token)))
                .build();
        return chain.filter(mutated);
    }

    @Override
    public int getOrder() {
        return -1; // run before routing filters
    }
}
```

## 9.3 Resilience4j

### Circuit Breaker: the state machine

```
        failure rate exceeds threshold
   ┌──────────────────────────────────────┐
   │                                        ▼
┌───────┐                              ┌────────┐
│CLOSED │ ──(failures accumulate)────► │ OPEN   │
│(normal│                              │(reject │
│ calls │ ◄────(probe succeeds)──┐     │ calls  │
│ pass  │                        │     │ instantly,
│through)                        │     │ no real call made)
└───────┘                        │     └───┬────┘
   ▲                              │          │ after wait duration
   │                          ┌────────┐ ◄───┘
   └──(probe also succeeds)── │HALF_OPEN│
                              │(allow a │
        (probe fails)────────►│ few test│
                ▼              │ calls)  │
            back to OPEN      └────────┘
```

- **CLOSED:** normal operation — calls pass through to the real downstream service. The
  breaker tracks the recent failure rate.
- **OPEN:** failure rate crossed the configured threshold — the breaker **stops calling the
  real service entirely** and fails fast instead, for a configured wait duration. This is
  the entire point: it stops sending requests to a service that's already struggling,
  giving it room to recover instead of piling on more load.
- **HALF_OPEN:** after the wait duration, the breaker allows a small number of *test*
  calls through. If they succeed, it closes (back to normal). If they fail, it reopens.

### `@CircuitBreaker`, `@Retry`, `@RateLimiter`, `@Bulkhead`

```java
package com.example.orders.client;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.ratelimiter.annotation.RateLimiter;
import io.github.resilience4j.retry.annotation.Retry;
import io.github.resilience4j.bulkhead.annotation.Bulkhead;
import org.springframework.stereotype.Service;

@Service
public class ShippingServiceClient {

    private final ShippingFeignClient feignClient;

    public ShippingServiceClient(ShippingFeignClient feignClient) {
        this.feignClient = feignClient;
    }

    @CircuitBreaker(name = "shippingService", fallbackMethod = "fallbackShippingQuote")
    @Retry(name = "shippingService")
    @RateLimiter(name = "shippingService")
    @Bulkhead(name = "shippingService")     // limits concurrent calls — isolates this
                                             // dependency's failures from exhausting threads
                                             // shared with other downstream calls
    public ShippingQuote getQuote(String orderId) {
        return feignClient.getQuote(orderId);
    }

    // Fallback: same return type + the triggering exception as the last parameter.
    // Called when the circuit is OPEN, or all retries are exhausted.
    private ShippingQuote fallbackShippingQuote(String orderId, Throwable t) {
        return ShippingQuote.unavailable(orderId); // degrade gracefully, don't crash the caller
    }
}
```

**Why the order matters:** annotations apply outside-in as listed (CircuitBreaker wraps
Retry wraps RateLimiter wraps Bulkhead, by Resilience4j's convention) — so retries happen
*inside* a single circuit breaker decision, not as separate calls each independently
tripping the breaker.

**Monitoring circuit state via Actuator:**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, circuitbreakers, circuitbreakerevents, metrics
  health:
    circuitbreakers:
      enabled: true
```

```
GET /actuator/circuitbreakers
→ { "circuitBreakers": ["shippingService"] }

GET /actuator/circuitbreakerevents/shippingService
→ stream of state transitions: CLOSED → OPEN → HALF_OPEN → CLOSED, with timestamps
  and the failure that triggered each transition — essential for understanding
  *why* a circuit tripped during an incident review.
```

## 9.4 Spring Cloud Config

Centralizes configuration for every service in one **Git repository**, instead of each
service carrying its own scattered config files — and lets you change config **without
redeploying** the service.

```
┌───────────────────┐      ┌──────────────────────┐      ┌───────────────────┐
│  Git Repo           │◄────│  Config Server         │◄────│  Order Service      │
│  order-service.yml  │     │  (serves config over   │     │  Payment Service    │
│  payment-service.yml│     │   HTTP, per service +  │     │  (fetch their own   │
│  application.yml     │     │   per environment)     │     │   config at startup)│
│  (shared defaults)   │     └──────────────────────┘     └───────────────────┘
└───────────────────┘
```

```yaml
# Config Server's own application.yml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/example-org/config-repo
          default-label: main
server:
  port: 8888
```

```yaml
# Order Service's bootstrap.yml — points at the Config Server, not local config
spring:
  application:
    name: order-service
  config:
    import: "configserver:http://localhost:8888"
```

### `@RefreshScope` — Runtime Configuration Without Restart

The problem this solves: your feature flag is controlled by a config property. You want
to flip it in production **without restarting the service** (restart = downtime, a
potentially risky deploy). `@RefreshScope` + Spring Cloud Config + `POST /actuator/refresh`
gives you a zero-downtime config change with a full audit trail in Git.

**`pom.xml` additions:**

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-config</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**Microservice `application.yml` — points at the Config Server and exposes `/actuator/refresh`:**

```yaml
spring:
  application:
    name: order-service
  config:
    import: "optional:configserver:http://config-server:8888"
  cloud:
    config:
      fail-fast: true
      retry:
        max-attempts: 6
        initial-interval: 1000
        multiplier: 1.5

management:
  endpoints:
    web:
      exposure:
        include: refresh,health,info     # expose /actuator/refresh
  endpoint:
    refresh:
      enabled: true
```

**Config Server (a separate, minimal Spring Boot app):**

```java
@SpringBootApplication
@EnableConfigServer                       // turns this app into a Config Server
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

```yaml
# Config Server's own application.yml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://github.com/yourname/config-repo
          default-label: main
          clone-on-start: true
          timeout: 10
server:
  port: 8888
```

**Config repository file (`config-repo/order-service.yml` in Git):**

```yaml
features:
  new-payment-flow:
    enabled: false        # change this → commit → push → trigger refresh

order:
  max-retry-attempts: 3
  timeout-seconds: 30
```

**Using `@RefreshScope` in the microservice:**

```java
package com.example.orders.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RefreshScope          // this bean is DESTROYED and re-created when /actuator/refresh fires,
                       // causing Spring to re-inject @Value fields from the latest config
@Slf4j
public class OrderController {

    @Value("${features.new-payment-flow.enabled:false}")
    private boolean newPaymentFlowEnabled;    // updated on refresh, no restart

    @Value("${order.max-retry-attempts:3}")
    private int maxRetryAttempts;             // updated on refresh, no restart

    @PostMapping("/api/v1/orders/{id}/payment")
    public ResponseEntity<PaymentResultDTO> processPayment(@PathVariable Long id) {
        log.info("Processing payment for order {} (new flow enabled: {})",
                id, newPaymentFlowEnabled);

        if (newPaymentFlowEnabled) {
            return newPaymentService.process(id, maxRetryAttempts);
        }
        return legacyPaymentService.process(id);
    }
}
```

**The end-to-end workflow for a zero-downtime flag change:**

```
Step 1: Edit the property in Git
  config-repo/order-service.yml:
    features.new-payment-flow.enabled: true   ← was false
  → git commit -m "enable new payment flow"
  → git push

Step 2: Trigger refresh on the running service (no restart, no redeploy):
  curl -X POST http://your-order-service:8080/actuator/refresh \
       -H "Content-Type: application/json"

  Response: ["features.new-payment-flow.enabled"]
             ↑ lists every property that changed — empty list = nothing changed

Step 3: Verify immediately:
  The next POST /api/v1/orders/123/payment routes through the new flow.
  Zero downtime. Zero restart. Audit trail of who changed what is in Git.
```

**Refreshing all instances at once:**

One service usually runs as multiple instances behind a load balancer. Calling
`/actuator/refresh` on a single instance only refreshes *that* instance — the other
nine still have the old config. Two solutions:

```
Solution A — Spring Cloud Bus (broadcast via Kafka or RabbitMQ):
  POST /actuator/busrefresh on ANY ONE instance
  → Cloud Bus publishes a RefreshRemoteApplicationEvent to Kafka
  → every other instance subscribed to that bus topic receives it and refreshes
  → one HTTP call refreshes the entire fleet

Solution B — GitHub Webhook + scripted loop:
  GitHub Webhook fires on push to config-repo
  → your CI/CD or a small Lambda calls POST /actuator/refresh on each known instance IP
  → works fine for small fleets without the Kafka dependency
```

**What `@RefreshScope` does NOT refresh (critical to know):**

- **`DataSource` / connection pool beans** — these hold open TCP connections configured
  with the old settings. Refreshing the property doesn't close and reopen the pool;
  database connection changes still require a restart.
- **`@Configuration` classes** — beans defined in `@Configuration` classes are *not*
  refresh-scoped by default; you must explicitly annotate the individual beans with
  `@RefreshScope` if you want them to be re-created.
- **Static `final` fields** — values bound at class-load time are not injectable and are
  never updated.

The safe rule: use `@RefreshScope` for **`@Value` fields and `@ConfigurationProperties`
beans** that carry lightweight, stateless configuration (feature flags, thresholds, timeouts).
Treat anything that holds connections, threads, or heavy initialization as not
refresh-safe.

## 9.5 Feign Client: declarative HTTP between services

Instead of hand-writing `RestTemplate`/`WebClient` calls, Feign generates the HTTP client
from an interface — and integrates directly with Resilience4j annotations (Section 9.3)
and service discovery (`lb://`):

```java
package com.example.orders.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "shipping-service")   // resolved via service discovery — no hardcoded host
public interface ShippingFeignClient {

    @GetMapping("/internal/quotes/{orderId}")
    ShippingQuote getQuote(@PathVariable("orderId") String orderId);
}
```

```yaml
feign:
  client:
    config:
      shipping-service:
        connectTimeout: 2000
        readTimeout: 5000
  circuitbreaker:
    enabled: true     # wires Feign calls into Resilience4j automatically
```

## 9.6 Service Discovery in Kubernetes

When running on Kubernetes, you typically **don't** need Eureka or another standalone
service registry — Kubernetes Services already provide DNS-based discovery natively: a
call to `http://shipping-service` resolves, via cluster DNS, to a stable virtual IP that
load-balances across all healthy pods backing that Service. Feign's `lb://shipping-service`
or a plain `http://shipping-service` call both work transparently in this environment. The
full mechanics of Kubernetes-native networking, readiness probes, and how they interact
with this kind of client-side resilience are covered in **Book 6** of this series.

## 9.7 Full `application.yml` — Resilience4j

```yaml
resilience4j:
  circuitbreaker:
    instances:
      shippingService:
        sliding-window-type: COUNT_BASED
        sliding-window-size: 20            # evaluate failure rate over the last 20 calls
        minimum-number-of-calls: 10        # don't trip until at least 10 calls have happened
        failure-rate-threshold: 50         # trip if >= 50% of those calls failed
        wait-duration-in-open-state: 10s   # how long to stay OPEN before probing
        permitted-number-of-calls-in-half-open-state: 3
        automatic-transition-from-open-to-half-open-enabled: true
        record-exceptions:
          - java.net.ConnectException
          - java.util.concurrent.TimeoutException
        ignore-exceptions:
          - com.example.orders.exception.OrderValidationException  # not a downstream failure

  retry:
    instances:
      shippingService:
        max-attempts: 3
        wait-duration: 500ms
        enable-exponential-backoff: true
        exponential-backoff-multiplier: 2
        retry-exceptions:
          - java.net.ConnectException

  ratelimiter:
    instances:
      shippingService:
        limit-for-period: 50        # max calls allowed per refresh period
        limit-refresh-period: 1s
        timeout-duration: 0s        # don't wait for a permit — fail fast if over the limit

  bulkhead:
    instances:
      shippingService:
        max-concurrent-calls: 25    # caps concurrent in-flight calls to this dependency

management:
  endpoints:
    web:
      exposure:
        include: health, circuitbreakers, circuitbreakerevents, metrics, retries, ratelimiters
  health:
    circuitbreakers:
      enabled: true
```

### Interview Section — Chapter 9

> **Q: How does a circuit breaker prevent cascading failure, concretely?**
> A: Once the failure rate crosses the configured threshold, the breaker moves to OPEN and
> stops sending calls to the struggling service entirely — failing fast instead of
> queueing up slow calls that would otherwise exhaust the caller's thread pool. This both
> protects the caller from being dragged down and gives the struggling downstream service
> room to recover instead of being hit with continued load.

> **Q: Why combine `@Retry` with `@CircuitBreaker` instead of using just one?**
> A: They solve different problems. Retry handles *transient* failures (a single dropped
> packet, a momentary blip) by trying again quickly. Circuit breaker handles *sustained*
> failure by stopping calls altogether once failures cross a threshold — without it, retries
> alone would keep hammering an already-overwhelmed service, making the underlying problem worse.

> **Q: How do you change a feature flag in production without restarting the service?**
> A: With Spring Cloud Config and `@RefreshScope`. Feature flags live as `@Value`
> properties in `@RefreshScope`-annotated beans, backed by a Git repository served by
> a Config Server. To flip a flag: commit the change to Git, then POST to
> `/actuator/refresh` on each service instance (or use Spring Cloud Bus to broadcast that
> one call to the entire fleet via Kafka). The `@RefreshScope` bean is destroyed and
> re-created with the new property values — zero restart, zero downtime, and every change
> has a Git commit as its audit trail.

> **Q: What does `@RefreshScope` NOT refresh, and why?**
> A: DataSource/connection-pool beans (they hold live TCP connections opened with the old
> settings — refreshing the property doesn't close and reopen them), `@Configuration`
> beans not explicitly annotated with `@RefreshScope`, and static final fields.
> The safe scope for `@RefreshScope` is lightweight, stateless configuration:
> feature flags, numeric thresholds, timeout values. Anything that holds connections,
> threads, or heavy initialization is not safe to hot-swap and still requires a restart.

> **Q: Why might you skip Eureka entirely on Kubernetes?**
> A: Kubernetes Services already provide DNS-based service discovery and load balancing
> natively — a stable virtual IP per Service that load-balances across healthy pods —
> which covers the same core need Eureka exists to solve in non-Kubernetes environments.
> Running Eureka on top is usually redundant infrastructure rather than a requirement.

---

# Closing: How These Chapters Fit Together

You started with one machine and a clean mental model — a call either succeeds or throws.
Every chapter since has been a response to the fact that across a network, that's no
longer true:

- **CAP & Consistency Models** (Ch 2–3) gave you the vocabulary for *what guarantee* a
  system is actually making when data is copied in more than one place.
- **Replication & Partitioning** (Ch 4–5) gave you the *mechanics* of how data is copied
  and split across machines in the first place.
- **Kafka** (Ch 6) gave you a concrete, production-grade tool for *decoupling* services
  through durable, replayable, ordered messaging — built directly on the replication and
  partitioning concepts from the two chapters before it.
- **Distributed Transactions** (Ch 7) gave you patterns for keeping multi-service business
  operations correct *without* a shared database transaction.
- **Event Sourcing & CQRS** (Ch 8) gave you a way to make that same idea — events as the
  source of truth — the foundation of how a service stores and serves its own data.
- **Spring Cloud** (Ch 9) gave you the operational scaffolding — discovery, config,
  routing, and resilience — that keeps a system built from all of the above actually
  survivable in production, where individual services *will* fail, slow down, and restart,
  constantly.

None of these patterns are free — every one of them trades simplicity for some combination
of scale, availability, or fault tolerance. The skill this book is trying to build isn't
memorizing the patterns; it's recognizing, for a given problem, which trade-off you
actually need to make — and which ones you don't.
