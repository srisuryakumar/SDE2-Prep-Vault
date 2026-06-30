---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 8 — LLD Design 4 — Splitwise"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["Observer Pattern"]
tags: [lld, case-study, algorithms, splitwise]
---

# LLD Case Study: Splitwise

## Problem Overview
Design an expense-sharing application. Users can create groups, add expenses with different split methods (Equal, Exact, Percentage), and track balances. The core algorithmic challenge is **Debt Simplification** — reducing `M` pairwise debts into the minimum number of transactions.

## Core Entities
- **User:** Represents a person.
- **Group:** Contains Users and Expenses.
- **Expense:** Details of a payment (total amount, paid by, splits).
- **Split:** Abstract class with concrete types `EqualSplit`, `ExactSplit`, `PercentageSplit`.
- **BalanceLedger:** Maps `userId -> net_balance` (positive = owed money, negative = owes money).

## Debt Simplification Algorithm
Without simplification, a group of 5 people could have O(N²) complex interlocking debts.
1. Compute the **net balance** for each person in the ledger.
2. Put all users with a positive balance (Creditors) into a **Max-Heap**.
3. Put all users with a negative balance (Debtors) into a **Min-Heap** (most negative first).
4. Pop the largest creditor and largest debtor.
5. Settle the minimum of their absolute balances (`settlement = Math.min(credit, |debt|)`).
6. Subtract the settlement from both. If either still has a balance, push them back into their respective heap.
7. Repeat until both heaps are empty.

*Result:* At most `N-1` transactions.

## Extending the Design
- **Floating Point Errors:** For financial data, avoid `double`. Use `BigDecimal` with `RoundingMode.HALF_UP` and validate that the sum of splits equals the total expense.
- **Notifications:** Use the **Observer Pattern** (`EventBus`). When `ExpenseService` saves an expense, it publishes an `ExpenseAddedEvent`. Decoupled listeners catch it and send emails or push notifications.
