---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 8 — Graphs"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, pattern, graphs, bfs, shortest-path]
---

# BFS for Shortest Paths Pattern

## Intuition
BFS explores nodes strictly level by level, ensuring that the first time a node is reached, it is reached by the shortest possible path (in terms of number of edges). **This guarantees shortest paths in unweighted graphs.**

## Problem: Word Ladder
Find the shortest transformation sequence from `beginWord` to `endWord`, changing one letter at a time, where all intermediate words are in a `wordList`.

**Why this is BFS:** Treat every word as a node. An edge exists between words differing by exactly one letter. "Shortest transformation sequence" is literally "shortest path in an unweighted graph".

**The Trick (Implicit Graph Generation):**
Don't compare against every word in `wordList` ($O(L^2 \cdot W)$). Instead, **generate** every possible one-letter-changed variant of the current word ($O(W \cdot 26)$) and check if it exists in the `wordSet` ($O(1)$).

```java
public int ladderLength(String beginWord, String endWord, List<String> wordList) {
    Set<String> wordSet = new HashSet<>(wordList);
    if (!wordSet.contains(endWord)) return 0;

    Queue<String> queue = new ArrayDeque<>();
    queue.offer(beginWord);
    Set<String> visited = new HashSet<>();
    visited.add(beginWord); // ALWAYS mark visited BEFORE queueing
    int steps = 1;

    while (!queue.isEmpty()) {
        int levelSize = queue.size();
        for (int i = 0; i < levelSize; i++) {
            String word = queue.poll();
            if (word.equals(endWord)) return steps;

            char[] chars = word.toCharArray();
            for (int pos = 0; pos < chars.length; pos++) {
                char original = chars[pos];
                for (char c = 'a'; c <= 'z'; c++) {
                    if (c == original) continue;
                    chars[pos] = c;
                    String candidate = new String(chars);
                    if (wordSet.contains(candidate) && !visited.contains(candidate)) {
                        visited.add(candidate);
                        queue.offer(candidate);
                    }
                }
                chars[pos] = original; // Restore!
            }
        }
        steps++;
    }
    return 0;
}
```
**Complexity:** $O(L \cdot W^2 \cdot 26)$ time, where $L$ is wordList length and $W$ is word length.
