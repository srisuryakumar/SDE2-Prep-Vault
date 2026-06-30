---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 10 — LLD Design 6 — Library Management System"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Strategy Pattern", "Observer Pattern"]
tags: [lld, case-study, library]
---

# LLD Case Study: Library Management System

## Problem Overview
Design a system to search books, checkout physical copies, handle returns, manage waitlists for unavailable books, and calculate overdue fines.

## Core Entities
- **Book:** The abstract metadata (ISBN, Title, Author).
- **BookCopy:** A physical instance of a Book. Holds a unique ID and `CopyStatus` (`AVAILABLE`, `BORROWED`).
- **Member:** A user who borrows books. Has a limit on `activeBorrows`.
- **BorrowRecord:** Tracks the transaction (Who, What Copy, Borrow Date, Due Date, Return Date).
- **BookWaitlist:** A queue of Members waiting for a specific ISBN.

## Design Patterns Used

### 1. Strategy Pattern (Fines)
Fines calculation policies can change (e.g., flat rate per day vs. flat rate per week vs. grace periods).
Create a `FineCalculationStrategy` interface:
- `PerDayFineStrategy`
- `PerWeekFineStrategy`
- `GracePeriodFineStrategy` (This can actually act as a Decorator over another strategy).

### 2. Observer Pattern (Waitlist Notifications)
When a `BookCopy` is returned:
1. `LibraryService` publishes a `BookReturnedEvent` to an `EventBus`.
2. `WaitlistNotificationListener` catches the event, checks the waitlist for that ISBN, dequeues the next `Member`, and sends an email.
*Benefit:* The core library checkout/return logic knows nothing about email services or waitlist implementations.

## Concurrency
If two members try to borrow the last copy simultaneously:
Make `borrowBook` synchronized (or use lock on the specific ISBN's list of copies). The first thread marks the copy as `BORROWED`. The second thread finds 0 available copies and is automatically added to the `BookWaitlist`.
