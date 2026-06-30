---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 1 — The Computer at Its Core"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: []
tags: [cs-foundations]
---

# Character Encoding (ASCII vs UTF-8)

A computer only understands numbers, so text is encoded as numbers by convention.

## ASCII (American Standard Code for Information Interchange)
Maps 128 characters to numbers 0-127, using exactly one byte each. 
- `A` = 65 (0x41)
- `a` = 97 (0x61)
- `0` = 48 (0x30)

## UTF-8 (Universal Character Encoding)
ASCII only covers English and some punctuation. UTF-8 is a superset that encodes any Unicode character using 1 to 4 bytes:
- Regular ASCII: 1 byte (backwards-compatible with ASCII)
- Latin accented characters: 2 bytes
- Most writing systems (Arabic, Chinese, Hindi): 3 bytes
- Emoji and rare symbols: 4 bytes

This is why an emoji in a string can break naive `string.length` checks in languages like JavaScript, as it counts UTF-16 code units, not individual characters.
