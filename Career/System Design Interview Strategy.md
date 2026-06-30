# System Design Interview Strategy

### The 45-minute framework

| Phase | Time | Focus |
|---|---|---|
| Requirements | 5 min | Functional + non-functional requirements, explicit scope |
| Estimation | 5 min | Back-of-envelope scale numbers (QPS, storage, bandwidth) |
| High-level design | 10 min | Major components and how data flows between them |
| Deep dive | 15 min | Interviewer-directed or self-selected deep dive into 1–2 components |
| Trade-offs & wrap-up | 10 min | Bottlenecks, failure modes, what you'd revisit with more time |

### Driving the conversation

Treat the interviewer as the client and yourself as the architect presenting a proposal, not as an examiner administering a test. Check in periodically: *"Before I go further into the data model, does this high-level approach match what you had in mind, or should I explore a different direction?"* This single habit prevents the common failure mode of confidently designing the wrong thing for 30 minutes.

### When to go deep vs. stay high-level

Stay high-level on components that are well-understood and not the interesting part of the problem (e.g., "a standard load balancer in front of stateless app servers" doesn't need elaboration). Go deep exactly where the interesting trade-off actually lives — usually the data model, the consistency strategy, or whichever component the interviewer leans into with follow-up questions. If you're not sure where to go deep, ask: *"Is there a part of this you'd like me to go deeper on?"*

### How to present trade-offs

Use a consistent structure for every non-trivial decision: *"I chose [X] because [reason tied to the actual requirements], the downside is [Y], and I'd mitigate that with [Z]."* For example: *"I chose eventual consistency for the like-count here because strict consistency would add latency to every read for a number that doesn't need to be perfectly accurate in real time — the downside is a user might briefly see a stale count, which I'd mitigate by converging it within a few seconds via the event stream."* This single sentence structure, repeated for each real decision, is most of what separates a strong system design answer from a weak one.

### Common mistakes

- **Not scoping:** diving into a full design before agreeing on what's actually in scope (e.g., designing global multi-region failover for a problem that only asked for single-region reliability).
- **Over-engineering:** reaching for Kafka, sharding, and a CDN for a system that, given the stated scale, doesn't need any of them yet — naming why a simpler approach is *sufficient* is as strong a signal as naming why a complex one is *necessary*.
- **Ignoring non-functional requirements:** designing only for "it works" without addressing availability, latency targets, or consistency needs explicitly.

### Handling "design X that you've never heard of"

Don't panic or pretend familiarity. Say so plainly, then use first principles: *"I haven't worked with this specific type of system before, so let me reason through it from the core requirements — what does it need to do, at what scale, with what consistency guarantees — and build up from there."* Interviewers are testing your reasoning process under novelty, not your trivia knowledge of a specific product; an honest, structured first-principles walkthrough consistently outperforms a nervous guess at "the right answer."
