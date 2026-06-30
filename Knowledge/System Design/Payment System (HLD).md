---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 9 — Design 7 — Payment System"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks", "Distributed Systems and Messaging"]
tags: [hld, case-study, payments, idempotency, saga, event-sourcing]
---

# HLD Case Study: Payment System

## Problem Overview
Accept payments, process them, and settle funds.
- **Crucial Constraint:** Never lose money or double-charge. This system favors **strong consistency and durability** over latency or throughput.

## Idempotency (Preventing Double Charges)
If a client times out and retries a payment, it shouldn't charge them twice.
**Solution:** The client provides an `X-Idempotency-Key` (a UUID).
1. Server checks Redis/DB for the key.
2. If processing -> return 409 (conflict).
3. If completed -> return the stored result.
4. If new -> process charge and store result by idempotency key durably in the DB.

## The Saga Pattern
A single payment touches multiple systems (card network, merchant ledger, internal ledger) and cannot be wrapped in one ACID transaction.
The **Saga Pattern** breaks this into local transactions, each with a **compensating action** if a later step fails.
*Example:*
- Step 1: Reserve funds. (Compensate: release hold)
- Step 2: Charge card. (Compensate: refund)
- If Step 2 fails, run Step 1's compensating action. The user is never charged.

## Database: PostgreSQL + Event Sourcing
Instead of a single `status = COMPLETED` column that overwrites history, store every state transition as an immutable event.
*Events:* `CREATED -> FUNDS_RESERVED -> CHARGE_CAPTURED -> COMPLETED`.
This provides a complete audit trail (required for financial compliance) and eliminates race conditions from separate status and audit log writes.

## Reconciliation
Distributed systems drift (e.g. lost webhooks). A **nightly batch job** sums all `COMPLETED` transactions internally and compares against the bank's settlement report. Mismatches are flagged for manual review.

## PCI DSS & Tokenization
Raw card numbers are never stored. The card goes directly to a PCI-compliant vault (like Stripe), which returns an opaque token. Internal systems only store and reference the token.

## Common Questions
**Q: What if the compensating action itself fails (e.g., the refund fails)?**
A: Compensating actions must be retried with their own idempotency keys. If retries exhaust, it must move to a `MANUAL_REVIEW` queue. Financial systems never fail silently.
