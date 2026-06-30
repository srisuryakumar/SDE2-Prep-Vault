---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 2 — Arrays and Strings"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [dsa, strings, immutability, java]
---

# String Immutability in Java

Java `String` objects are immutable — once created, their underlying `char[]` can never change. Methods like `substring`, `toLowerCase`, `replace`, or concatenation (`+`) do not modify the existing string; they allocate a brand-new `String` object.

## The Concatenation Trap
Concatenating strings inside a loop using `+` or `+=` is a catastrophic performance bug.
```java
// BAD: O(n²) total work
String result = "";
for (int i = 0; i < n; i++) {
    result += chars[i];   // allocates and copies result each time
}
```
At each step, the entire current string is copied into a new object. The total characters copied over $n$ iterations is $0 + 1 + 2 + ... + (n-1) = n(n-1)/2$, which is $O(n^2)$. For $n=100,000$, this is 5 billion character copies.

## The Fix: StringBuilder
`StringBuilder` uses a resizable `char[]` buffer.
```java
// GOOD: O(n) total work
StringBuilder sb = new StringBuilder();
for (int i = 0; i < n; i++) {
    sb.append(chars[i]);   // O(1) amortized
}
String result = sb.toString();   // one final O(n) copy
```
The total work is $O(n)$ amortized for all appends, plus one $O(n)$ copy at the end. Total = $O(n)$.
