---
type: linkedin-post
post_number: 4
scheduled_week: 2
scheduled_day: Friday
status: drafted
---
I reproduced a race condition today. Here's the proof.

Expected output: Count = 10000
Actual output: Count = 9843 (different every run)

Why?

count++ is not atomic. It's three operations:
1. Read count from memory
2. Increment in register
3. Write back to memory

Thread 1 reads 500. Thread 2 reads 500.
Both increment to 501. Both write 501.
One increment is permanently lost.

Three fixes:
1. synchronized → mutex, one thread at a time, correct but slower
2. AtomicInteger → CAS hardware instruction, no lock, fast
3. volatile → fixes visibility only, NOT atomicity, wrong tool here

Lesson: debugging concurrency bugs is 10× harder than causing them.

Code reproducing this: [GitHub link]

#Java #Concurrency #BackendEngineering
