---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 7 — Heaps and Priority Queues"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, heaps, greedy, scheduling]
---

# Greedy Scheduling with Heaps

## Intuition
Problems like "Task Scheduler" ask you to execute tasks with a cooldown period. This requires greedy simulation: at every time slot, run the most frequent *currently available* task.

- A **Max-Heap** of task frequencies gives $O(1)$ access to "which available task should run next."
- A separate **Cooldown Queue** holds `[remainingCount, timeAvailableAgain]` for tasks that are resting.

## Template (Task Scheduler)
```java
public int leastInterval(char[] tasks, int n) {
    Map<Character, Integer> freq = new HashMap<>();
    for (char task : tasks) freq.merge(task, 1, Integer::sum);

    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    maxHeap.addAll(freq.values());

    Queue<int[]> cooldown = new ArrayDeque<>();   // [count, timeAvailableAgain]
    int time = 0;

    while (!maxHeap.isEmpty() || !cooldown.isEmpty()) {
        time++; // Even idle slots count toward total time
        
        if (!maxHeap.isEmpty()) {
            int count = maxHeap.poll() - 1; // Run most frequent task
            if (count > 0) cooldown.offer(new int[]{count, time + n});
        }
        
        // Re-admit EVERY task whose cooldown expires exactly now
        // MUST be a `while`, not an `if`, to handle simultaneous expirations
        while (!cooldown.isEmpty() && cooldown.peek()[1] == time) {
            maxHeap.offer(cooldown.poll()[0]);
        }
    }
    return time;
}
```
**Common Mistakes:** 
- Forgetting that an idle slot still counts towards elapsed time.
- Using an `if` instead of a `while` to re-admit from the cooldown queue. Simultaneous expirations will be permanently lost if you only readmit one per tick.
