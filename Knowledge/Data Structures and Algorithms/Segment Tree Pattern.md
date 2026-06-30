---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [dsa, pattern, segment-tree, range-queries, hard]
---

# Segment Tree Pattern

## Intuition
What does it solve? **Range queries** (sum/min/max over a sub-range) **with point updates** (changing a single element).
- **Prefix sums** answer range-sums in $O(1)$ but require $O(n)$ to update a single element.
- **Segment trees** answer range queries in $O(\log n)$ and handle point updates in $O(\log n)$.

Use this when you have a static array with **frequent updates interleaved with queries**.

## Structure
A binary tree where each node represents a *range* of the original array and stores an aggregate (e.g. sum) over that range. The root covers the entire array, and each node's two children split its range in half.
It is conventionally stored as an array of size `4n`.

## Template (Range Sum with Updates)
```java
class SegmentTree {
    int[] tree;
    int n;

    SegmentTree(int[] nums) {
        n = nums.length;
        tree = new int[4 * n];
        build(nums, 0, 0, n - 1);
    }

    private void build(int[] nums, int node, int start, int end) {
        if (start == end) {
            tree[node] = nums[start];
            return;
        }
        int mid = (start + end) / 2;
        build(nums, 2 * node + 1, start, mid);
        build(nums, 2 * node + 2, mid + 1, end);
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2]; // Combine
    }

    void update(int index, int value) {
        update(0, 0, n - 1, index, value);
    }

    private void update(int node, int start, int end, int index, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }
        int mid = (start + end) / 2;
        if (index <= mid) {
            update(2 * node + 1, start, mid, index, value);
        } else {
            update(2 * node + 2, mid + 1, end, index, value);
        }
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2]; // Recombine
    }

    int query(int left, int right) {
        return query(0, 0, n - 1, left, right);
    }

    private int query(int node, int start, int end, int left, int right) {
        if (right < start || end < left) return 0; // No overlap
        if (left <= start && end <= right) return tree[node]; // Fully covered
        int mid = (start + end) / 2;
        int leftSum = query(2 * node + 1, start, mid, left, right);
        int rightSum = query(2 * node + 2, mid + 1, end, left, right);
        return leftSum + rightSum; // Partial overlap
    }
}
```
**Complexity:** Build $O(n)$, Update $O(\log n)$, Query $O(\log n)$. Space $O(n)$.
