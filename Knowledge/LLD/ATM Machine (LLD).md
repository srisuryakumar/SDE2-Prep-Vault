---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 9 — LLD Design 5 — ATM Machine"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["State Pattern", "Chain of Responsibility Pattern"]
tags: [lld, case-study, atm]
---

# LLD Case Study: ATM Machine

## Problem Overview
Design the software for an ATM. The primary challenges are **State Management** (handling the flow of an ATM session safely) and **Validation** (checking card, PIN, balance, and limits before dispensing). There is also an algorithmic component for dispensing cash.

## Core Entities
- **ATM:** The Context object. Holds cash inventory, current state, and the current session's card/account info.
- **ATMState:** Interface for the State pattern.
- **Card / Account:** User and financial entities.
- **CashDispenser:** Hardware simulation that handles dispensing logic.
- **Validator Chain:** Implements the validation rules before a transaction.

## Design Patterns Used

### 1. State Pattern
An ATM's behavior changes entirely based on its state.
- **States:** `IDLE`, `CARD_INSERTED`, `AUTHENTICATED`
- If a user tries to `requestWithdrawal()` in the `IDLE` state, the `IdleState` implementation rejects it.
- State transitions (`atm.setState(new AuthenticatedState())`) happen dynamically.

### 2. Chain of Responsibility Pattern
Before dispensing cash, a withdrawal request must pass multiple checks:
1. `CardValidator`: Is the card expired or blocked?
2. `PINValidator`: Is the PIN correct? (Increments failed attempts on failure).
3. `AccountValidator`: Is the account active and in good standing?
4. `TransactionAmountValidator`: Is the amount a multiple of 100? Is it within the daily limit? Does the account have sufficient balance?

Each validator checks its specific rule and calls `passToNext()`. If any fails, the chain breaks and an error is returned. This adheres to the **Open/Closed Principle** (you can easily add a `FraudValidator` later).

## Algorithmic Component: Cash Dispenser
**The Problem:** Dispense a requested amount using the fewest number of bills (e.g., ₹2000, ₹500, ₹200, ₹100).
**The Solution:** A Greedy Algorithm.
1. Iterate through denominations in descending order.
2. For each denomination, take as many as possible (`Math.min(remaining / denom, available_in_cassette)`).
3. Subtract from the remaining amount and proceed to the next denomination.
4. If `remaining == 0` at the end, commit the transaction. If `remaining > 0`, rollback and fail (cannot make exact change).
