---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 3 — Structural Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [lld, design-patterns, structural]
---

# Composite Pattern

## Intuition
File systems, menus, and UI components all share a tree structure containing individual items (leaves) and containers of items (composites). Clients should be able to treat both uniformly. 
Calling `getSize()` on a file should return its size in bytes. Calling `getSize()` on a directory should recursively sum the sizes of all its children.

## The Solution
Define a common `Component` interface.
- **Leaf** implements it by performing the direct action.
- **Composite** implements it by maintaining a list of children (which are also `Component`s) and delegating the action to them recursively.
