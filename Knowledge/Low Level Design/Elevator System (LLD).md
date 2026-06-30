---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 7 — LLD Design 3 — Elevator System"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["State Pattern"]
tags: [lld, case-study, algorithms, scheduling, elevator]
---

# LLD Case Study: Elevator System

## Problem Overview
Design a system for multiple elevators in a building. The primary challenges are **State Management** of individual elevators and the **Scheduling Algorithm** for the dispatcher.

## Core Entities
- **ElevatorSystem:** Singleton managing the overall state and the Dispatcher.
- **Elevator:** Has a state (`IDLE`, `MOVING_UP`, `MOVING_DOWN`, `MAINTENANCE`), current floor, and pending stops.
- **ElevatorRequest:** Encapsulates the floor requested from and the direction (or the target floor for internal requests).
- **Dispatcher:** Analyzes requests and assigns them to the "best" available elevator.

## The Scheduling Algorithm (SCAN)
The industry standard is the **SCAN (Elevator) algorithm**:
1. An elevator moves continuously in one direction (e.g., UP).
2. It stops at all requested floors in that direction.
3. Once it reaches the highest requested floor, it reverses direction (or goes `IDLE` if no pending requests exist).
*Why not FCFS?* First-Come-First-Serve causes the elevator to bounce wildly between floor 1 and 20, leading to terrible throughput.

### Implementation Details
Maintain two `TreeSet`s per elevator: `floorsGoingUp` (sorted naturally) and `floorsGoingDown` (sorted in reverse). The elevator pops the first element of the active tree set and travels to it.

## The Dispatcher Logic
When a user presses "UP" on Floor 5, which of the 3 elevators takes it?
The Dispatcher calculates a heuristic cost for each elevator (excluding those in `MAINTENANCE`):
- If Elevator 1 is at Floor 2, `MOVING_UP`, the cost is just distance `(5 - 2 = 3)`.
- If Elevator 2 is at Floor 8, `MOVING_UP`, it has passed Floor 5. The cost is `distance + (pending stops * 2)` because it must finish its upward journey and come back down.
- Dispatcher assigns the request to the elevator with the minimum cost.
