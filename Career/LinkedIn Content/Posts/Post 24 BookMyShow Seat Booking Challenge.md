---
type: linkedin-post
post_number: 24
scheduled_week: 12
scheduled_day: Friday
status: drafted
---
The hardest concurrency problem I've solved in production-style code.

Scenario: Coldplay tickets go on sale. 100,000 users try to book seat A5
simultaneously. How do you prevent double-booking?

Bad solution: check availability then book in two steps.
→ Thread 1 reads: A5 is available.
→ Thread 2 reads: A5 is available.
→ Both try to book. One succeeds. One corrupts data.

Solution 1: Redis atomic lock
SET seat:show123:A5 userId EX 600 NX
→ NX means "only set if key does not exist"
→ This is atomic. One thread wins. Others see key already set.
→ EX 600 means the hold expires in 10 minutes if payment doesn't complete.

Solution 2: Database SELECT FOR UPDATE
SELECT * FROM seats WHERE id = 'A5' AND show_id = 123 FOR UPDATE;
→ Row-level lock. One transaction proceeds, others wait.
→ Works, but doesn't scale to 100K concurrent users.

My implementation uses Redis for the hold, PostgreSQL SELECT FOR UPDATE
for the final booking confirmation. Two-phase: fast Redis check, then
durable database commit.

Code: [GitHub link to lld-java/bookmyshow]

#SystemDesign #LLD #Java
