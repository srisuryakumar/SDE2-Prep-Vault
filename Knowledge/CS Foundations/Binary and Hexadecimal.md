---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 1 — The Computer at Its Core"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [cs-foundations]
---

# Binary and Hexadecimal

## Binary
A computer is built from billions of transistors, which have two stable states: ON (1) or OFF (0). Every computer operation is built from these binary states.

- **Bit**: A single 1 or 0.
- **Byte**: 8 bits grouped together. This provides 256 possible combinations (0 to 255), enough to represent a single character of text.

### Binary Arithmetic
Each bit position represents a power of 2 (place value). To convert binary to decimal, sum the products of the bits and their place values.

```text
Binary: 0  1  0  0  1  0  1  0
Place:  128 64 32 16  8  4  2  1
Value = 64 + 8 + 2 = 74
```

## Hexadecimal (Base 16)
Writing binary is cumbersome, so engineers use **hexadecimal (hex)** as shorthand. It uses 16 symbols: 0-9 and A-F. 
- One hex digit represents exactly 4 bits.
- Two hex digits represent one byte (8 bits).

For example, `0100 1010` in binary becomes `4A` in hex. Hexadecimal values in code are typically prefixed with `0x` (e.g., `0x4A`, `0xFF`).

### Common Uses of Hexadecimal
- **Memory addresses**: `0x7ffd4b2a0c18`
- **Colors**: `#FF5733`
- **Hashes**: SHA-256
- **MAC addresses**: `AA:BB:CC:DD:EE:FF`
