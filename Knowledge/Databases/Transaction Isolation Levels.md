---
type: concept
subject: Databases and Caching
source_book: "Book 3 — Databases and Caching"
source_chapter: "Chapter 2 — Database Internals"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [database, isolation, transactions, acid]
---

# Transaction Isolation Levels

## Intuition
Three anomalies can occur when transactions run concurrently. Four isolation levels trade performance for protection against them.

## Anomalies
1. **Dirty Read:** Reading uncommitted changes from another transaction. (Prevented at Read Committed).
2. **Non-Repeatable Read:** Re-reading the same row returns a different value within the same transaction. (Prevented at Repeatable Read).
3. **Phantom Read:** Re-executing a range query returns additional rows inserted by another transaction. (Prevented at Serializable).

## Isolation Levels
| Level | Dirty Read | Non-Repeatable | Phantom Read |
| :--- | :--- | :--- | :--- |
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** (Default) | Prevented | Possible | Possible |
| **Repeatable Read** | Prevented | Prevented | Possible* |
| **Serializable** | Prevented | Prevented | Prevented |

*Note: PostgreSQL's MVCC implementation actually prevents phantoms at Repeatable Read as well.*

## Using Isolation Levels
```sql
-- Repeatable Read: Transaction sees a frozen snapshot from its start.
BEGIN ISOLATION LEVEL REPEATABLE READ;

-- Serializable: May abort with an error if a conflict is detected. 
-- The application MUST catch this and retry.
BEGIN ISOLATION LEVEL SERIALIZABLE;
```
