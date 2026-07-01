---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["[[Binary Search Tree Properties]]", ]
tags: [database, internals, index, b-tree]
---

# B-Tree Indexes and EXPLAIN ANALYZE

## Intuition
Without an index, `WHERE user_id = 1` reads every row in the table (Sequential Scan). A **B-Tree Index** organizes data hierarchically, making point queries and range queries $O(\log n)$.

PostgreSQL's B-tree nodes hold ~340 pointers. An index height of 3-4 can cover 100 million rows, meaning every row lookup requires only 3-4 disk page reads.

## Multi-Column Composite Indexes
Composite indexes must follow the **Left-Prefix Rule**.
```sql
CREATE INDEX idx_orders_composite ON orders(user_id, status, created_at DESC);
```
- **Can use index:** `user_id`, or `user_id + status`.
- **Cannot use index:** `status` alone, or `created_at` alone.
Think of it like a phone book sorted by (LastName, FirstName). You can't efficiently search just by FirstName.

## Covering Index
An index that includes all columns the query needs. PostgreSQL can answer the query entirely from the index (Index Only Scan), with zero heap access.
```sql
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total_amount);
```

## EXPLAIN ANALYZE
Use `EXPLAIN ANALYZE` to see actual execution metrics, not just estimates.
- **Seq Scan:** No usable index or returning too many rows (often >5-10%).
- **Index Scan:** Uses B-tree, then looks up the row in the heap.
- **Index Only Scan:** Fastest possible scan, no heap access.
- **Bitmap Index Scan:** Batches heap reads to reduce random I/O.

## Related Concepts
- See also [[Binary Search Tree Properties]] for binary search trees, since B-Trees are a generalization.
