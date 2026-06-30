---
type: concept
subject: Data Structures and Algorithms
source_book: "Book 2 — Data Structures and Algorithms"
source_chapter: "Chapter 12 — Advanced Patterns"
status: to-study
interview_frequency: low
introduced_day: 
related_concepts: []
tags: [dsa, pattern, math, number-theory]
---

# Math Patterns (GCD, Primes, Modulo)

## GCD (Greatest Common Divisor) - Euclidean Algorithm
```java
public int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}
```
**LCM (Least Common Multiple):**
```java
public long lcm(int a, int b) {
    return (long) a / gcd(a, b) * b; // Divide before multiplying to prevent overflow
}
```

## Sieve of Eratosthenes (Find all primes up to $n$)
Find all primes up to $n$ in $O(n \log \log n)$.
**Trick:** For each prime `i`, start marking multiples as non-prime starting at `i * i` (because smaller multiples like `2i` or `3i` were already marked by earlier primes 2, 3).
```java
public int countPrimes(int n) {
    boolean[] composite = new boolean[n]; // default false
    int count = 0;
    for (int i = 2; i < n; i++) {
        if (!composite[i]) {
            count++;
            for (long j = (long) i * i; j < n; j += i) {
                composite[(int) j] = true;
            }
        }
    }
    return count;
}
```

## Modular Arithmetic
When true answers could be astronomically large, you are often asked to return the answer "modulo $10^9 + 7$".
- **Addition:** `(a + b) % m = ((a % m) + (b % m)) % m`
- **Multiplication:** `(a * b) % m = ((a % m) * (b % m)) % m`
- **Subtraction:** `(a - b) % m = ((a % m) - (b % m) + m) % m`
**CRITICAL FIX FOR SUBTRACTION:** In Java/C++, `%` can return a negative number if the left operand is negative. You MUST add `m` before applying the final modulo to shift the result back into the positive range `[0, m-1]`.
