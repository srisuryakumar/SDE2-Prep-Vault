---
type: concept
subject: Low Level Design
source_book: "Book 7 — Low Level Design"
source_chapter: "Chapter 11 — LLD Design 7 — Chess Game"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["Template Method Pattern", "State Pattern", "Strategy Pattern"]
tags: [lld, case-study, chess]
---

# LLD Case Study: Chess Game

## Problem Overview
Model a full chess game. This tests deep object-oriented inheritance, grid/matrix data structures, and state validation (e.g., ensuring a move doesn't leave the King in check).

## Core Entities
- **Game:** The Context object managing the Board, Player Turns, and Game Status.
- **Board:** An 8x8 grid of `Optional<Piece>`.
- **Piece (Abstract):** Base class for all pieces with properties like Color, Position, and `hasMoved`.
- **Position:** Represents `(row, col)`.
- **Move:** Tracks from/to positions and move type (Normal, Castling, Promotion).

## Design Patterns Used

1. **Composite Pattern:** The `Board` is composed of an 8x8 grid of `Cells`/`Positions`.
2. **Template Method Pattern:** The abstract `Piece` class provides a `collectRayMoves` method. Subclasses like `Rook`, `Bishop`, and `Queen` call this with their specific directional vectors.
3. **Strategy Pattern / Polymorphism:** Each `Piece` subclass implements its own `getValidMoves()` logic.
4. **State Pattern:** The Game's `GameStatus` (`ACTIVE`, `CHECK`, `CHECKMATE`, `STALEMATE`) dictates if moves are even allowed to be processed.

## Move Validation (King in Check)
How do you validate if a move is legal (i.e., it doesn't leave the King in check)?
1. Create a deep copy of the `Board`.
2. Execute the proposed move on the copy.
3. Find the current player's King on the copied board.
4. Scan all opponent pieces and ask: "Does any opponent piece's `getAttackSquares()` contain the King's position?"
5. If yes, the move is invalid.

## Special Moves
- **Castling:** Check if the King or Rook has moved (`hasMoved == true`). Check if the squares between them are empty and not under attack by the opponent. Move both pieces simultaneously.
- **En Passant:** Track an `enPassantTarget` `Position` in the `Game` state. When a pawn moves 2 squares, set this target to the skipped square. On the very next turn, if an adjacent enemy pawn moves to the target, allow it, capture the original pawn, and clear the target.
- **Pawn Promotion:** If a pawn reaches the opposite end of the board (`row == 0` or `row == 7`), immediately swap it out for a `Queen` (or user-selected piece).
