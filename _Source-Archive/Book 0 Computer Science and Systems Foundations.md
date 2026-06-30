# Computer Science and Systems Foundations
## How Computers, Programs, Networks, and Web Applications Actually Work

**For:** Surya — Software Engineer (JavaScript/TypeScript, 3 years)  
**Goal:** Build the mental model that makes every advanced backend topic click  
**Duration:** Study alongside your 120-day SDE-2 preparation  

---

### A Note Before You Begin

You already know how to *use* the tools. You can open a terminal, write code, make API calls. What this book gives you is the *underneath* — the model of reality that senior engineers carry in their heads when they debug a production incident at 2 AM, when they explain why their system design handles 100,000 requests per second, when they answer "what happens inside the JVM under load?"

Every concept here connects forward to something you will encounter in Java, Spring Boot, Kafka, Kubernetes, or a system design interview. The connections are explicit. Nothing is taught as trivia.

Start at Chapter 1. Read in order. The chapters build on each other.

---

## Table of Contents

- **Chapter 1:** The Computer at Its Core — From Transistors to Programs
- **Chapter 2:** Operating Systems — The Software That Runs All Other Software
- **Chapter 3:** How Programs Run — From Source Code to Execution
- **Chapter 4:** Networking — How Computers Talk to Each Other
- **Chapter 5:** How Different Types of Software Work
- **Chapter 6:** Developer Environment, Git, and Tooling

---

# Chapter 1: The Computer at Its Core — From Transistors to Programs

Before you can reason about why your Spring Boot service slows down under load, why a HashMap lookup is O(1), or why your Kafka consumer can fall behind a producer, you need to understand what a computer physically *is*. Not in a vague, hand-wavy way — in the precise, mechanical way that lets you reason from first principles.

A computer is a machine that manipulates numbers. That is the complete description. Everything else — your operating system, your web browser, your Kafka cluster, your Java code — is numbers being manipulated according to rules. Let us trace those rules from the very bottom.

---

## 1.1 Binary — The Only Language Computers Speak

### Why Binary?

A computer is built from billions of transistors. A transistor is a tiny electronic switch. It has exactly two stable states: **current flowing** (ON) or **current not flowing** (OFF). There is no "37% on" in a reliable transistor — analog states are too sensitive to heat, voltage noise, and manufacturing variation.

Engineers mapped these two states to two symbols: **1** (ON) and **0** (OFF). Every single thing your computer does is built from these two values. Not because binary is convenient — it is not, for humans — but because it is the only scheme that maps cleanly onto the physical reality of transistors.

### The Bit and the Byte

**A bit** (binary digit) is a single 1 or 0. It is the smallest possible unit of information. One bit can represent two states: yes/no, true/false, on/off.

**A byte** is 8 bits grouped together. Why 8? Early hardware engineers found that 8 bits gave you enough range (256 values) to represent a single character of text, while fitting neatly into circuit designs. The 8-bit byte became the universal standard by the 1970s and has never changed.

With 8 bits, you have 2⁸ = **256 possible combinations** (from 00000000 to 11111111), representing the values 0 through 255.

```
One byte:

 Bit 7    Bit 6    Bit 5    Bit 4    Bit 3    Bit 2    Bit 1    Bit 0
┌────────┬────────┬────────┬────────┬────────┬────────┬────────┬────────┐
│   1    │   0    │   1    │   0    │   0    │   1    │   0    │   1    │
└────────┴────────┴────────┴────────┴────────┴────────┴────────┴────────┘
  2^7=128   2^6=64  2^5=32   2^4=16   2^3=8    2^2=4    2^1=2    2^0=1

Value = 128 + 0 + 32 + 0 + 0 + 4 + 0 + 1 = 165
```

### Storage Units and Real-World Sizes

| Unit       | Exact Size                  | Real-World Example                              |
|------------|-----------------------------|-------------------------------------------------|
| 1 Byte     | 8 bits                      | One ASCII character ('A')                       |
| 1 Kilobyte | 1,024 bytes (2¹⁰)           | A short text message (~280 chars ≈ 280 bytes)   |
| 1 Megabyte | 1,048,576 bytes (2²⁰)       | One minute of MP3 audio (~1 MB)                 |
| 1 Gigabyte | 1,073,741,824 bytes (2³⁰)   | A 90-minute HD movie (~4 GB)                    |
| 1 Terabyte | ~1 trillion bytes (2⁴⁰)     | A 4K movie at full quality (~80 GB)             |
| 1 Petabyte | ~1 quadrillion bytes (2⁵⁰)  | ~200,000 4K movies                              |

> **Note:** Disk manufacturers use decimal (1 KB = 1,000 bytes) while OSes use binary (1 KB = 1,024 bytes). This is why a "500 GB" SSD shows as ~466 GiB in your OS. This discrepancy is a frequent source of confusion in production capacity planning.

### Binary Arithmetic — How 01001010 Becomes 74

Each bit position has a **place value** — a power of 2 — just as each digit in decimal has a power of 10. The rightmost bit is 2⁰ = 1, the next is 2¹ = 2, then 2² = 4, and so on.

To convert binary to decimal, multiply each bit by its place value and sum:

```
Binary: 0  1  0  0  1  0  1  0
Place:  128 64 32 16  8  4  2  1

= 0×128 + 1×64 + 0×32 + 0×16 + 1×8 + 0×4 + 1×2 + 0×1
= 0    + 64   + 0    + 0    + 8   + 0   + 2   + 0
= 74
```

This is the **positional number system** — the same principle as decimal (base 10), just using base 2 instead of base 10.

### Hexadecimal — Binary's Shorthand

Writing binary is painful. The 32-bit integer `11111111000000001111111100000000` is hard to read and easy to miscount. Engineers adopted **hexadecimal (base 16)** as a compact representation.

Hexadecimal uses 16 symbols: **0–9** then **A–F** (where A=10, B=11, C=12, D=13, E=14, F=15).

The key insight: **one hex digit represents exactly 4 bits** (since 2⁴ = 16). Therefore **two hex digits = one byte** (8 bits = 256 values = 00 to FF).

```
Binary:  0100  1010   →  4A   in hex  →  74  in decimal
         ────  ────
           4     A

Binary:  1111  1111   →  FF   in hex  →  255 in decimal
Binary:  0000  0000   →  00   in hex  →  0   in decimal
Binary:  1000  0000   →  80   in hex  →  128 in decimal
```

Hex is conventionally prefixed with `0x` in code: `0x4A`, `0xFF`, `0x1A2B3C4D`.

**Where you see hex in real life as a backend engineer:**
- **Memory addresses:** `0x7ffd4b2a0c18` — the address where a variable lives in RAM
- **Colour codes:** `#FF5733` — 3 bytes: Red=FF(255), Green=57(87), Blue=33(51)
- **SHA-256 hashes:** `a3f1b2c9d4e5...` — 64 hex characters = 32 bytes = 256 bits
- **JWT tokens:** the header and payload are Base64 (not hex, but same idea — encoding bytes)
- **MAC addresses:** `AA:BB:CC:DD:EE:FF` — 6 bytes, each written as 2 hex digits

### How Text Is Represented

A computer only understands numbers. So text is encoded as numbers by convention.

**ASCII (American Standard Code for Information Interchange):**  
Maps 128 characters to numbers 0–127, using exactly one byte each. The uppercase letter 'A' is 65, 'B' is 66, ..., 'Z' is 90. Lowercase 'a' is 97. '0' is 48. Space is 32.

```
'A' = 65 decimal = 0x41 hex = 01000001 binary
'B' = 66 decimal = 0x42 hex = 01000010 binary
'a' = 97 decimal = 0x61 hex = 01100001 binary
'0' = 48 decimal = 0x30 hex = 00110000 binary
```

**UTF-8 (Universal Character Encoding):**  
ASCII only covers English and some punctuation. UTF-8 is a superset that encodes any Unicode character using **1 to 4 bytes**:

- Regular ASCII (A–Z, 0–9, punctuation): still 1 byte — UTF-8 is backwards-compatible with ASCII
- Latin accented characters (é, ñ, ü): 2 bytes
- Most of the world's writing systems (Arabic, Chinese, Hindi): 3 bytes
- Emoji and rare symbols (😀, 𝕳, 🎸): 4 bytes

This is why an emoji in a string can break naive `string.length` checks in JavaScript — JS counts UTF-16 code units, not characters. The emoji 😀 has `length` of 2 in JavaScript even though it is one character.

### How Numbers Are Represented

**Unsigned integers:** Store only non-negative values. 8-bit unsigned: 0 to 255.

**Signed integers (two's complement):** The most significant bit indicates sign (0=positive, 1=negative). This clever scheme means addition works the same for both positive and negative numbers, simplifying CPU circuits.

```
8-bit signed range: -128 to +127
  01111111 = +127 (highest positive)
  00000001 = +1
  00000000 =  0
  11111111 = -1
  10000000 = -128 (most negative)
```

**Integer overflow:** A 32-bit signed integer holds values from -2,147,483,648 to +2,147,483,647. Add 1 to the maximum value and it wraps around to the minimum negative value. This is not an error in hardware — it is defined behaviour. But in software, it is a common bug:

```java
int max = Integer.MAX_VALUE;  // 2,147,483,647
int overflow = max + 1;       // -2,147,483,648  ← wraps to negative!
```

This bug has caused real disasters, including a plane's avionics system resetting mid-flight (Boeing 787 software bug, 2015) and game score counters wrapping to negative values.

**Floating-point numbers (IEEE 754):**  
Real numbers like 3.14159 or 0.001 cannot be stored as exact integers. The CPU uses a scientific-notation-like format: sign bit + exponent + mantissa.

```
float (32-bit):  1 sign bit + 8 exponent bits + 23 mantissa bits
double (64-bit): 1 sign bit + 11 exponent bits + 52 mantissa bits
```

This is why `0.1 + 0.2` does not equal `0.3` in any language using IEEE 754:
```javascript
0.1 + 0.2 === 0.3  // false — gives 0.30000000000000004
```
The decimal fraction 0.1 has no exact binary representation, just as 1/3 has no exact decimal representation. **Never use float/double for money.** Use `BigDecimal` in Java or integer cents.

---

> **📌 Interviews Ask This**
>
> **"Why should you not use float for currency calculations?"**  
> IEEE 754 floating-point cannot represent most decimal fractions exactly. `0.1 + 0.2` produces `0.30000000000000004`, not `0.3`. For money, use `BigDecimal` in Java (arbitrary precision) or store values as integer cents (e.g., $12.99 stored as `1299` cents).
>
> **"What is integer overflow and how do you prevent it?"**  
> A 32-bit int has a maximum value of 2,147,483,647. Adding 1 wraps it to -2,147,483,648. Prevent by using `long` (64-bit) for large values, or using `Math.addExact()` in Java which throws `ArithmeticException` on overflow rather than silently wrapping.

---

## 1.2 The CPU — The Chip That Runs Everything

### What a CPU Is

The **Central Processing Unit (CPU)** is the chip that actually runs your program. It is a rectangular piece of silicon roughly the size of a postage stamp, containing between 1 billion (a simple chip) and 80+ billion (Apple M2 Ultra) transistors, arranged into circuits that can perform operations on numbers.

"Running a program" means: reading instructions from memory, one by one, and performing the operation each instruction describes. That is all. An extraordinarily fast, extraordinarily precise sequence of number operations.

### The Anatomy of a CPU

```
┌─────────────────────────────────────────────────────────────────┐
│                           CPU Core                               │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    Control Unit (CU)                       │  │
│  │   Reads instructions, directs other units, manages flow   │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                              │                                   │
│          ┌───────────────────┼────────────────────┐             │
│          ▼                   ▼                    ▼             │
│  ┌───────────────┐  ┌──────────────────┐  ┌────────────────┐   │
│  │      ALU      │  │    Registers     │  │  L1/L2 Cache   │   │
│  │  (Arithmetic  │  │                  │  │                │   │
│  │   Logic Unit) │  │  PC (Instr Ptr)  │  │  ~32KB L1      │   │
│  │               │  │  SP (Stack Ptr)  │  │  ~256KB L2     │   │
│  │  + - × ÷      │  │  GP regs (rax,   │  │  ~1-4ns latency│   │
│  │  AND OR NOT   │  │  rbx, rcx...)    │  │                │   │
│  │  comparisons  │  │  Flags register  │  │                │   │
│  └───────────────┘  └──────────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                       ┌──────┴───────┐
                       │   L3 Cache   │  ~8MB, shared across cores, ~30-40ns
                       └──────┬───────┘
                              │
                    ┌─────────┴──────────┐
                    │   Memory Bus       │
                    └─────────┬──────────┘
                              │
                    ┌─────────┴──────────┐
                    │   RAM (DRAM)       │  ~100ns latency
                    └────────────────────┘
```

**Control Unit (CU):** The manager of the CPU. It reads the current instruction, decodes what it means, and coordinates the ALU, registers, and memory access to execute it.

**Arithmetic Logic Unit (ALU):** The calculator. It performs mathematical operations (add, subtract, multiply, divide) and logical operations (AND, OR, NOT, XOR, comparisons). It operates entirely on values already in registers.

**Registers:** Tiny, ultra-fast storage directly inside the CPU. There are typically 16–32 general-purpose registers, each 8 bytes (64 bits) on a modern 64-bit CPU. Operations happen in registers — to add two numbers, the CPU loads them from memory into registers, adds them in the ALU, and stores the result back.

Key registers:
- **Program Counter (PC) / Instruction Pointer (IP):** Holds the memory address of the *next instruction to execute*. After each instruction executes, the PC advances automatically. A `jump` instruction changes the PC to a different address (this is how `if` statements, loops, and function calls work at the hardware level).
- **Stack Pointer (SP):** Holds the memory address of the current top of the call stack. Increments and decrements as functions are called and return.
- **General-purpose registers (rax, rbx, rcx, rdx, rsi, rdi, r8–r15 on x86-64):** Hold the values your code is currently computing with.
- **Flags register:** Holds the result of the last comparison (was it zero? was it negative? did it overflow?). Used by conditional jump instructions.

### The Fetch-Decode-Execute Cycle

Every CPU, in every computer ever made, executes this loop continuously from power-on to shutdown:

```
┌─────────────────────────────────────────────────────────────────┐
│                   The CPU Execution Loop                         │
│                                                                  │
│   ┌──────────┐                                                   │
│   │  FETCH   │  Read the instruction at address in PC from memory│
│   └────┬─────┘                                                   │
│        │                                                         │
│        ▼                                                         │
│   ┌──────────┐                                                   │
│   │  DECODE  │  Translate the instruction bytes into operation   │
│   └────┬─────┘  (is this ADD? LOAD? JUMP? CALL?)                │
│        │                                                         │
│        ▼                                                         │
│   ┌──────────┐                                                   │
│   │ EXECUTE  │  Perform the operation using ALU, registers, mem  │
│   └────┬─────┘                                                   │
│        │                                                         │
│        ▼                                                         │
│   Increment PC to next instruction address                       │
│        │                                                         │
│        └──────────────────────────► back to FETCH               │
└─────────────────────────────────────────────────────────────────┘
```

One complete cycle of this loop is called a **clock cycle**. A modern CPU running at 3.5 GHz performs 3.5 billion of these cycles per second. In practice, many CPUs complete more than one instruction per cycle using pipelining (discussed below).

### Clock Speed and Cores

**Clock speed (GHz)** measures how many cycles per second a CPU can perform. 3.0 GHz = 3 billion cycles per second. However, clock speed alone does not determine performance — the number of instructions completed per cycle also matters (IPC, instructions per cycle).

**Multiple cores:** A modern CPU chip contains multiple *complete* CPU cores, each with its own registers, ALU, L1, and L2 cache, all sharing the L3 cache and memory bus. An 8-core CPU can genuinely execute 8 independent instruction streams simultaneously.

**Why 8 cores ≠ 8× speedup — Amdahl's Law:**

If your program is 80% parallelizable and 20% must run sequentially, the maximum speedup from infinite cores is only 5× (1 ÷ 0.20 = 5). In practice:
- Thread coordination overhead consumes time
- Data must be synchronized between cores (cache coherence traffic)
- I/O waits do not benefit from more cores
- Most web service code is only partially parallelizable

This is why a 64-core Kafka broker processes more messages than a 4-core one, but not 16× more.

### CPU Caches and Cache Misses

This is one of the most practically important concepts for backend performance.

The CPU is *enormously* faster than RAM. A register operation takes under 1 nanosecond. Fetching data from RAM takes ~100 nanoseconds — a 100× difference. To bridge this gap, CPUs have **caches**: small, fast memory layers between the CPU and RAM.

```
Latency (approximate, as of 2024):
┌────────────────────────────────────────────────────┐
│  Register access           <1 ns      (always hit) │
│  L1 Cache hit              1-4 ns     ~32 KB       │
│  L2 Cache hit              4-12 ns    ~256 KB      │
│  L3 Cache hit              30-40 ns   ~8-32 MB     │
│  RAM access                ~100 ns    ~16-64 GB    │
│  NVMe SSD access           ~100,000 ns (100 μs)   │
│  HDD access                ~10,000,000 ns (10 ms) │
│  Network (same datacenter) ~500,000 ns (0.5 ms)   │
└────────────────────────────────────────────────────┘
```

When the CPU needs data, it checks L1 first. If found (cache hit), access is fast. If not (cache miss), it checks L2, then L3, then fetches from RAM, populating caches along the way. A cache miss to RAM takes 25–100× longer than a cache hit.

**Why this matters for your code:**

**ArrayList vs LinkedList for iteration:**  
An ArrayList stores elements contiguously in memory. When you iterate, each element is adjacent to the next — the CPU prefetches the next elements into cache automatically. Near-zero cache misses.

A LinkedList stores each element in a separate heap object with a pointer to the next. Elements are scattered randomly in memory. Every `node.next` traversal is a potential cache miss — the CPU must fetch a completely different memory location. At 100ns per miss for a 1-million-element list, this is ~100ms of cache-miss penalty vs ~1ms for ArrayList.

**This is why O(n) ArrayList beats O(n) LinkedList in practice by 10–100×.**

**HashMap performance:** A Java HashMap stores entries in an array of buckets, but when many entries hash to the same bucket (hash collision), entries form a linked list or TreeMap within that bucket — reintroducing cache misses. This is why HashMap performance degrades under high load factor or a poor hash function.

### Pipeline and Out-of-Order Execution

Modern CPUs do not naively execute one instruction at a time. They use two techniques that dramatically improve throughput but create subtle problems for concurrent programming:

**Pipelining:** Overlapping the fetch, decode, and execute stages of consecutive instructions. While instruction 5 is executing, instruction 6 is decoding, and instruction 7 is being fetched — all simultaneously, like an assembly line.

**Out-of-order execution:** The CPU detects when two instructions are independent (they don't use each other's results) and executes them in a different order than written, keeping the execution units busy. This happens invisibly at the hardware level.

**Why this creates problems for concurrent code:** Two threads on different cores may see the results of memory writes in a different order than the code wrote them. Thread A writes variable X then variable Y, but Thread B might see Y change before X. This is called **memory reordering** and it is why Java's `volatile` keyword and `synchronized` exist — they include **memory barriers** that force the CPU to flush and order its writes.

---

> **📌 Interviews Ask This**
>
> **"Why is ArrayList faster than LinkedList for iteration even though both are O(n)?"**  
> CPU cache locality. ArrayList stores elements contiguously in memory; the CPU prefetches them into L1 cache. LinkedList scatters nodes across the heap; every pointer traversal is a potential cache miss (~100ns vs ~1ns). The Big-O notation hides the constant factor, which is 100× here.
>
> **"What is a CPU cache miss?"**  
> When the CPU needs a value not in its L1/L2/L3 caches and must fetch it from RAM (~100ns latency, vs ~1-4ns for L1 cache). Cache-unfriendly data structures (LinkedList, many small objects with pointers) cause frequent cache misses and dramatically reduce real-world performance.

---

## 1.3 Memory — RAM, Storage, and the Hierarchy

### The Memory Hierarchy

Every storage system in a computer trades off **speed vs capacity vs cost**. The fundamental rule: the faster the storage, the smaller and more expensive it is.

```
The Memory Hierarchy (fastest → slowest, smallest → largest):

  ┌─────────────────────────────────────────────────────┐
  │  Registers (CPU)    <1 ns       ~128-256 bytes      │  fastest
  ├─────────────────────────────────────────────────────┤
  │  L1 Cache           1-4 ns      ~32 KB per core     │
  ├─────────────────────────────────────────────────────┤
  │  L2 Cache           4-12 ns     ~256 KB per core    │
  ├─────────────────────────────────────────────────────┤
  │  L3 Cache           30-40 ns    ~8-32 MB shared     │
  ├─────────────────────────────────────────────────────┤
  │  RAM (DRAM)         ~100 ns     ~16 GB – 512 GB     │
  ├─────────────────────────────────────────────────────┤
  │  NVMe SSD           ~100 μs     ~500 GB – 8 TB      │
  ├─────────────────────────────────────────────────────┤
  │  SATA SSD           ~500 μs     ~500 GB – 8 TB      │
  ├─────────────────────────────────────────────────────┤
  │  HDD                ~10 ms      ~2 TB – 20 TB       │  slowest
  └─────────────────────────────────────────────────────┘
```

### RAM — Fast, Volatile, Temporary

**RAM (Random Access Memory)** is the computer's working memory. When a program runs, its code and data live in RAM. The CPU reads from and writes to RAM millions of times per second.

**"Volatile"** means RAM loses all its contents the instant power is removed. This is why you lose unsaved work when your computer crashes — it was only in RAM, not on disk.

**"Random Access"** means the CPU can read or write any byte in RAM in the same amount of time, regardless of where in RAM it is. This contrasts with magnetic tape, where reading byte #1,000,000 requires physically advancing the tape past bytes #1 through #999,999.

**RAM addresses:** Every byte in RAM has a unique numeric address, starting from 0. On a system with 16 GB of RAM, addresses run from 0 to 17,179,869,183. The CPU accesses a specific byte by sending its address to the memory controller.

**Why RAM size matters for your applications:**

If your Spring Boot application loads 10 GB of data into a HashMap, and your server only has 8 GB of RAM, the OS is forced to move some RAM contents to disk to make room (called **swap** or **paging**). Disk I/O is 1,000–10,000× slower than RAM. Your application's performance falls off a cliff. This is why memory sizing is critical in Kubernetes pod resource specifications.

### Storage — Persistent, Slow, Permanent

**SSD (Solid State Drive):** Uses NAND flash memory chips to store data persistently. No moving parts. NVMe SSDs (connected via PCIe) are dramatically faster than older SATA SSDs.

**HDD (Hard Disk Drive):** Uses spinning magnetic platters with a read/write head that physically moves to the correct position. The mechanical movement introduces latency (~10ms). Random access on an HDD is catastrophic — seeking to a random location before every read adds 10ms repeatedly.

**Why databases choose storage carefully:**
- **Transaction logs (WAL — Write-Ahead Log):** Sequential writes. Both HDD and SSD handle sequential I/O well, but NVMe SSD is preferred for latency.
- **Index files (B-trees, etc.):** Random reads. Absolutely requires SSD — HDDs are too slow for random I/O at scale.
- **Cold/archival data:** Bulk sequential reads. HDDs are acceptable and much cheaper per GB.

### What "Loading a Program" Means

When you type `java -jar myapp.jar` in a terminal:

1. The shell finds the `java` executable on disk (via `$PATH`)
2. The OS reads the `java` binary from disk into RAM
3. The OS creates a new process with its own virtual address space (Chapter 2)
4. The `java` binary (the JVM) starts running, reads your JAR from disk into RAM
5. The JVM interprets/compiles and executes your `main()` method

The program that was bytes-on-disk becomes a living process consuming RAM. The bytes on disk are never modified during execution (unless your program writes files).

### Why Running Out of RAM Is Catastrophic

```
Normal operation:
┌──────────────────────┐     Fast path: all data in RAM
│         RAM          │     CPU reads/writes RAM at ~100ns
│  [App][App][JVM][OS] │
└──────────────────────┘

RAM full → OS uses swap (disk as slow RAM):
┌──────────────────────┐     Slow path: evicted data goes to disk
│         RAM          │     CPU waits for disk I/O at ~100,000ns
│  [App][---][JVM][OS] │     ← App's data evicted to swap
└──────────────────────┘
         ↓↑ (swap traffic)
┌──────────────────────┐
│    Disk (SSD/HDD)    │
│    [Swap: App data]  │
└──────────────────────┘
```

When a system starts swapping heavily ("thrashing"), every memory access that hits swapped-out pages requires a disk read (~100,000ns vs 100ns). Applications become thousands of times slower. This is why Kubernetes kills and restarts pods that exceed their memory limits — it is better to restart a pod cleanly than to let it thrash.

---

> **📌 Interviews Ask This**
>
> **"Why is Redis faster than a database like PostgreSQL?"**  
> Redis stores all data in RAM (~100ns access). PostgreSQL stores data on disk and reads pages from disk into a buffer pool in RAM, but cold data requires disk I/O (~100μs-10ms). Redis is 100–10,000× faster for small lookups precisely because it avoids disk entirely. (There are nuances — PostgreSQL's buffer pool keeps hot data in RAM too — but fundamentally, Redis's guarantee of in-memory storage is the source of its speed advantage.)
>
> **"What happens when a JVM runs out of heap memory?"**  
> The JVM throws `OutOfMemoryError: Java heap space`. The JVM will first attempt garbage collection to free unused objects. If GC cannot free enough space, the JVM throws the error and typically crashes the process. In Kubernetes, the container will be restarted by the kubelet if it exits with an OOM error, and a `memory.limit` on the container prevents one service from starving others.

---

## Why This Matters for Your SDE-2 Journey

Every performance problem you encounter in the next 120 days traces back to this chapter.

**Redis vs PostgreSQL:** Redis keeps everything in RAM (Chapter 1.3). PostgreSQL reads from disk when the buffer pool is cold. The hierarchy is why the in-memory tier is 100–10,000× faster.

**HashMap performance:** CPU caches (Chapter 1.2) explain why a HashMap with a bad hash function degrades — hash collisions force pointer traversal, causing cache misses.

**JVM integer overflow:** Java's `int` is a 32-bit two's complement number (Chapter 1.1). Integer overflow is a real production bug. Use `long` for IDs, counters, and timestamps.

**String encoding:** Every time you handle user input in a Spring Boot controller, the JVM is converting UTF-8 bytes (from the HTTP request body) into Java `String` objects (UTF-16 internally). Knowing this, you understand why `string.getBytes(StandardCharsets.UTF_8)` is the correct way to get the byte count, not `string.length()`.

**The JVM's JIT compiler:** The CPU only executes machine code (Chapter 1.2). Java bytecode is not machine code. The JVM interprets it initially, profiles which methods are called most (hot spots), and JIT-compiles those to native machine code. After warmup, a hot Java method executes at near-native speed because the CPU is running actual x86-64 machine code, not interpreted bytecode.

**Memory sizing in Kubernetes:** Understanding volatile vs persistent storage, and the cost of swapping (Chapter 1.3), is why Kubernetes resource requests and limits (`resources.requests.memory`, `resources.limits.memory`) exist. Without them, a memory-hungry pod can starve the entire node.

---

---

# Chapter 2: Operating Systems — The Software That Runs All Other Software

You have written JavaScript that runs in Node.js. You have used a terminal. But consider: what exactly is running your code? When you write `fs.readFile()` in Node.js, what actually reads the file? When your Spring Boot server handles 500 simultaneous HTTP requests, what is managing those concurrent tasks? The answer, in every case, is the **operating system**.

Without an OS, you would need to write code that directly controls the network card's hardware registers, the disk controller's interrupt lines, and the CPU's privilege bits — for every single application, on every single hardware configuration. This is not hypothetical: early 1970s programmers did exactly this. The OS was invented to solve the nightmare of sharing hardware between multiple programs running simultaneously.

---

## 2.1 What an Operating System Is and Why It Exists

### The Problem Without an OS

Imagine two programs running on the same hardware with no OS:

- Program A is printing a document. It sends bytes to the printer.
- Program B also decides to print. It also sends bytes to the printer.
- Result: the printer receives interleaved bytes from both programs and produces garbage.

- Program A is using memory addresses 1000–5000.
- Program B doesn't know this and also tries to use addresses 1000–5000.
- Result: they overwrite each other's data. Both programs crash or produce wrong results.

Without an OS, any two programs running simultaneously will interfere with each other. The hardware is shared, and there is no referee.

### What the OS Provides

The OS is a program that runs first and manages everything else. It provides four fundamental services:

**1. Process management:** Run multiple programs simultaneously without them interfering. The OS gives each program a slice of CPU time and isolates them from each other.

**2. Memory management:** Give each program its own private section of RAM. Program A cannot read or write Program B's memory, even though both share the same physical RAM chips.

**3. File system:** Organize persistent data on disk into files and directories. Provide a consistent API for reading and writing, regardless of whether the underlying storage is an HDD, SSD, or network drive.

**4. Device drivers:** Translate between programs and hardware. Your program calls `write()` on a file descriptor — the OS's driver for your specific SSD model handles the actual hardware I/O. Programs never need to know the hardware details.

### Examples of Operating Systems

- **Linux:** Used on virtually every server, cloud VM, container, Android phone, and most of the world's compute infrastructure. Free, open-source, enormously configurable.
- **macOS:** Built on Darwin (a BSD Unix variant). What your laptop likely runs. Familiar Unix terminal with Apple's user interface.
- **Windows:** Dominates the desktop market. Windows Server is used in enterprise environments with Microsoft stacks.

When you run a Spring Boot application "in production," it is almost certainly running on Linux inside a Docker container on a Kubernetes cluster in a cloud provider's datacenter.

---

## 2.2 The Kernel — The Core of the OS

### Kernel Space vs User Space

The OS is split into two fundamental domains:

```
┌──────────────────────────────────────────────────────────────────┐
│                         User Space                                │
│                                                                   │
│   ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│   │  Your Spring │  │   Web        │  │     Java JVM          │ │
│   │  Boot App    │  │   Browser    │  │   (java binary)       │ │
│   └──────────────┘  └──────────────┘  └───────────────────────┘ │
│                                                                   │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │              C Standard Library (libc)                   │   │
│   │    Higher-level wrappers around system calls             │   │
│   └──────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│                    System Call Interface                           │
│         (the only legal crossing point between spaces)            │
├──────────────────────────────────────────────────────────────────┤
│                         Kernel Space                              │
│                                                                   │
│   ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐ │
│   │   Process    │  │    Memory    │  │    File System        │ │
│   │   Manager    │  │    Manager   │  │    (ext4, APFS, NTFS) │ │
│   └──────────────┘  └──────────────┘  └───────────────────────┘ │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │         Device Drivers + Network Stack (TCP/IP)          │   │
│   └──────────────────────────────────────────────────────────┘   │
├──────────────────────────────────────────────────────────────────┤
│                           Hardware                                │
│         CPU │ RAM │ SSD/HDD │ Network Card │ GPU │ USB           │
└──────────────────────────────────────────────────────────────────┘
```

**User space** is where your code runs. Applications, the JVM, the browser, Node.js — all in user space. User-space code operates in a restricted mode where it cannot directly access hardware.

**Kernel space** is where the OS core runs. It has unrestricted access to all hardware and manages resources on behalf of user-space programs.

**Why separate them?** A bug in user space (a segfault, a NullPointerException) crashes only your application. A bug in kernel space corrupts shared OS data structures and can crash the entire system, taking all running programs with it. The separation limits the blast radius of bugs.

### Privilege Levels

The CPU itself enforces the boundary. Modern CPUs (x86-64) have **four privilege rings** (Ring 0 through Ring 3), though OSes typically use only two:

- **Ring 0 (Kernel mode):** Full access to all hardware instructions and memory. The kernel runs here.
- **Ring 3 (User mode):** Restricted. Cannot execute privileged instructions (like directly accessing device I/O ports). Cannot access memory outside its own address space. User-space code runs here.

If a user-space program tries to execute a privileged instruction, the CPU throws a hardware exception, the kernel handles it, and the OS kills the offending program.

### System Calls — Crossing the Boundary

The only way for a user-space program to request a kernel service is through a **system call (syscall)**. A system call is a special CPU instruction that:

1. Switches the CPU from user mode (Ring 3) to kernel mode (Ring 0)
2. Jumps to a specific entry point in the kernel
3. The kernel performs the requested service
4. Switches back to user mode and returns the result

```
User-space program                    Kernel
      │                                  │
      │  wants to read a file            │
      │                                  │
      │── syscall: read(fd, buf, count) ─►│
      │                                  │  kernel mode: access disk
      │                                  │  check permissions
      │                                  │  fetch data from disk/page cache
      │                                  │  copy data to user buffer
      │◄── return: bytes read or error ──│
      │                                  │
      │  back in user mode               │
```

**Common system calls every backend engineer should know:**

| Syscall      | What it does                                            | When you use it (indirectly) |
|--------------|---------------------------------------------------------|------------------------------|
| `read()`     | Read bytes from a file descriptor (file, socket, pipe)  | Every FileInputStream, HTTP body read |
| `write()`    | Write bytes to a file descriptor                        | Every FileOutputStream, HTTP response |
| `open()`     | Open a file, get a file descriptor                      | Every `new File()` operation |
| `close()`    | Close a file descriptor, release resources              | Every `InputStream.close()` |
| `fork()`     | Create a new process as a copy of the current           | Shell running a command, process spawning |
| `exec()`     | Replace current process image with a new program        | Shell executing `java`, `ls`, etc. |
| `socket()`   | Create a network socket                                 | Every `new ServerSocket()` in Java |
| `connect()`  | Connect a socket to a remote address (TCP handshake)    | Every JDBC connection, HTTP client call |
| `accept()`   | Accept a new incoming connection on a server socket     | Every Tomcat/Netty worker thread |
| `mmap()`     | Map a file or device into process virtual memory        | JVM memory-mapped files, some DB engines |
| `clone()`    | Create a new thread (Linux's thread creation)           | Every `new Thread()` in Java |
| `futex()`    | Fast user-space mutex (blocking/unblocking threads)     | Every `synchronized` block in Java |
| `epoll()`    | Efficient I/O event notification (I/O multiplexing)     | Netty, Node.js, reactive frameworks |

**Why system calls are relatively expensive (~1–5 microseconds each):**

Each system call requires:
1. A CPU mode switch (Ring 3 → Ring 0)
2. Context save/restore
3. Kernel validation of arguments
4. Kernel executes the actual work
5. CPU mode switch back (Ring 0 → Ring 3)

This cost is why:
- **Java NIO / Netty** batches multiple operations into fewer syscalls (using `epoll` to multiplex thousands of connections onto one syscall)
- **Java BufferedWriter** collects small writes and flushes them in one `write()` syscall instead of calling `write()` once per character
- **Database connection pooling (HikariCP)** reuses TCP connections rather than calling `socket()`, `connect()` per query

---

> **📌 Interviews Ask This**
>
> **"What is the difference between user space and kernel space?"**  
> User space is where applications run, with restricted access — they cannot directly access hardware or other processes' memory. Kernel space is where the OS core runs, with full hardware access. The CPU enforces this boundary via privilege rings. Programs cross from user to kernel space via system calls. A crash in user space kills one process; a crash in kernel space (kernel panic) crashes the entire system.
>
> **"Why is creating a new OS thread expensive?"**  
> A thread requires a stack (typically 1MB on Linux), a thread control block in the kernel, registration with the kernel scheduler, and initialization of thread-local storage. The kernel must also be invoked via syscall (`clone()` on Linux). Creation costs ~10–100 microseconds. This is why thread pools reuse threads rather than creating a new one per request — the cost of creation would dominate for short-lived tasks.

---

## 2.3 Processes — Running Programs

### What a Process Is

A **process** is a running instance of a program. The distinction matters:

- A **program** is a file on disk: `/usr/bin/java` or `myapp.jar`. It is just bytes — instructions and data, static and inert.
- A **process** is what happens when the OS loads that program into RAM and starts executing it. It has a unique identity, its own section of memory, open files, and a current execution state.

You can run the same program multiple times simultaneously — each run is a separate process with its own independent state. Two `java -jar myapp.jar` commands create two separate JVM processes, even though they run the same program bytes.

### Process Control Block (PCB)

The OS maintains a data structure for each running process called the **Process Control Block (PCB)** (called `task_struct` in the Linux kernel). This is how the OS keeps track of every process:

```
Process Control Block (PCB):
┌─────────────────────────────────────────────────────────┐
│  PID (Process ID)          │  12345                     │
│  Parent PID (PPID)         │  1234 (shell that started it)│
│  State                     │  RUNNING / READY / BLOCKED  │
│  Program Counter snapshot  │  0x7f4b2a3c (saved when     │
│  Register values snapshot  │   process was paused)       │
│  Memory maps               │  virtual→physical address map│
│  Open file descriptor table│  [0=stdin, 1=stdout, 5=db]  │
│  CPU scheduling priority   │  20 (nice value)            │
│  Signal handlers           │  SIGTERM → cleanup fn       │
│  User/group IDs (UID, GID) │  1000 / 1000               │
│  CPU time used             │  user: 2.3s, sys: 0.1s      │
│  Memory usage              │  RSS: 256MB, VSZ: 1.2GB     │
└─────────────────────────────────────────────────────────┘
```

### Process State Machine

A process is always in one of several states, transitioning between them as the OS scheduler and I/O events occur:

```
                        ┌──────────┐
                        │   NEW    │  Process being created
                        └────┬─────┘
                             │  OS admits process
                             ▼
         ┌───────────── ┌──────────┐ ◄────────────────────┐
         │   scheduler  │  READY   │    I/O complete       │
         │   dispatch   └────┬─────┘    (woken up)         │
         │                   │                             │
         ▼                   ▼                             │
   ┌──────────┐        ┌──────────┐        ┌──────────────┐│
   │  READY   │◄──────-│ RUNNING  │───────►│    BLOCKED   ││
   └──────────┘ timer  └────┬─────┘ waits  │  (WAITING)   ││
                 interrupt   │      for I/O └──────────────┘│
                             │                              │
                             │ preempted by scheduler        │
                             └──────────────────────────────┘
                             │
                             │ process calls exit()
                             ▼
                        ┌──────────┐
                        │TERMINATED│
                        └──────────┘
```

- **NEW:** The process is being created. OS is setting up PCB, allocating memory.
- **READY:** The process is loaded into memory, ready to run, waiting for its turn on the CPU.
- **RUNNING:** The process is currently executing instructions on a CPU core.
- **BLOCKED/WAITING:** The process is waiting for something — a file read to complete, a network packet to arrive, a lock to be released. It cannot use the CPU usefully, so the scheduler gives the CPU to another process.
- **TERMINATED:** The process has exited. OS is cleaning up resources.

### Context Switching

The OS creates the illusion that many processes run simultaneously, even with fewer CPU cores. It does this by **time-slicing**: running each process for a short interval (called a **time quantum**, typically 1–10ms), then pausing it and running another.

Pausing one process and resuming another is called a **context switch**:

```
Process A running                    Process B ready
      │                                    │
      │                                    │
CPU: ─────────────────[timer interrupt]───────────────►
      │                      │             │
      ▼                      │             ▼
A's registers saved to PCB-A │    B's registers restored from PCB-B
A → READY state              │    B → RUNNING state
                             │    CPU jumps to B's saved instruction
```

**Cost of a context switch:** Typically 1–10 microseconds. Includes:
- Save all CPU registers to the PCB of the pausing process
- Update the PCB state
- Run the scheduler to select the next process
- Load all CPU registers from the PCB of the resumed process
- Flush some CPU caches (L1/L2 caches contain the pausing process's data; they are now invalid for the new process)

At 1,000 context switches per second, this is 1–10ms of overhead per second — small but meaningful. At 100,000 context switches per second (common under heavy load with many threads), the overhead becomes significant.

### Process Isolation

Each process lives in its own **virtual address space** — it cannot read or write another process's memory. This isolation is enforced by the CPU's Memory Management Unit (MMU) in hardware. A process trying to access memory outside its bounds gets a **Segmentation Fault** (SIGSEGV) and is killed.

```
Physical RAM (one pool):
┌────────────────────────────────────────────────┐
│  OS Kernel  │  Process A │  Process B │  Free  │
└────────────────────────────────────────────────┘

Process A sees:             Process B sees:
┌────────────┐              ┌────────────┐
│  Its own   │              │  Its own   │
│  virtual   │              │  virtual   │
│  address   │              │  address   │
│  space     │              │  space     │
│  (private) │              │  (private) │
└────────────┘              └────────────┘
    ▲                           ▲
    │ MMU translates             │ MMU translates
    ▼                           ▼
   Physical RAM chunk          Different physical RAM chunk
```

**Why this matters:**
- **A browser tab crash** doesn't take down your whole browser — each tab is isolated (Chrome uses separate processes per tab)
- **One microservice crashing** doesn't corrupt another service's memory
- **Your application bug** doesn't corrupt the OS kernel's data
- **Different JVM instances** running the same code are completely isolated

### Creating Processes: fork() and exec()

Unix/Linux creates new processes through two system calls:

**`fork()`:** Creates an exact copy of the current process. The parent and child now have identical virtual address spaces (with copy-on-write optimization), open files, and program counters, but different PIDs.

**`exec()`:** Replaces the current process's memory image with a completely different program loaded from disk. The process ID stays the same, but the running code becomes the new program.

The two are almost always used together to spawn a new program:

```
Shell wants to run "ls -la":

Shell process
    │
    │─── fork() ─────────────────────────────────────────────►
    │                                              Child process
    │                                               (copy of shell)
    │                                                    │
    │                                                    │── exec("ls", ["-la"]) ──►
    │                                                    │
    │                                              Child process
    │                                             (now running "ls")
    │                                                    │
    │                                                    │ runs, prints output
    │                                                    │── exit(0) ──►
    │
    │◄── wait() ── (parent waits for child to finish) ──┘
    │
    │ shell prints prompt again
```

**Seeing processes:** Run `ps aux` in a Linux/macOS terminal to see all running processes with their PIDs, CPU and memory usage, and command.

---

## 2.4 Threads — Concurrent Execution Within a Process

### What a Thread Is

A thread is a unit of execution *within* a process. While a process is the container (with its own memory, files, and identity), threads are the workers inside that container.

A process starts with one thread (the main thread). It can create additional threads to do work concurrently. All threads in a process **share the same heap memory** (the same objects, the same address space), but each thread has its own **stack** and **program counter**.

### Process vs Thread Anatomy

```
One Process = One Virtual Address Space, multiple threads:

┌─────────────────────────────────────────────────────────────────┐
│                       Process (JVM process)                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            Shared Memory (one copy, all threads see it)   │   │
│  │                                                           │   │
│  │  Text Segment: compiled bytecode / JIT-compiled code      │   │
│  │  Data Segment: static variables                           │   │
│  │  Heap: all Java objects (new MyObject() lives here)       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   Thread 1   │  │   Thread 2   │  │      Thread 3        │  │
│  │  (main)      │  │  (HTTP worker│  │   (Kafka consumer)   │  │
│  │              │  │   thread)    │  │                      │  │
│  │  Stack:      │  │  Stack:      │  │  Stack:              │  │
│  │  - main()    │  │  - handle() │  │  - consume()         │  │
│  │  - init()    │  │  - service() │  │  - processRecord()   │  │
│  │              │  │              │  │                      │  │
│  │  PC: 0x1234  │  │  PC: 0x5678  │  │  PC: 0x9abc          │  │
│  │  Registers   │  │  Registers   │  │  Registers           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Why separate stacks, shared heap?**  
Each thread's stack tracks *its own* function call chain. Thread 1 is executing `main()` calling `init()` — that's Thread 1's stack. Thread 2 is executing `handle()` calling `service()` — completely separate call chain, separate stack. If stacks were shared, there would be no way to track which function each thread was in.

The heap is shared because objects in Java (any `new SomeObject()`) are meant to be accessible from multiple threads — that is the whole point of multithreading. A `HashMap` created in the main thread can be read by worker threads. The *danger* is that multiple threads modifying the same heap object simultaneously creates data corruption (race conditions).

### Types of Threads: OS Threads, Green Threads, Virtual Threads

**OS Threads (Kernel Threads):**  
Managed by the operating system kernel. Each OS thread has a real identity to the kernel — it appears in `ps` output, the scheduler gives it CPU time directly, and it can run on any CPU core. 

- Creating an OS thread calls `clone()` syscall on Linux
- Default stack size: **1 MB per thread** on Linux (configurable)
- Context switch cost: ~1–10 microseconds (same as a process context switch)
- **The maximum number of threads is limited by available RAM:** 10,000 threads × 1 MB = 10 GB of RAM just for stacks, before any actual work

Java's `Thread` class before Java 21 maps 1-to-1 with OS threads.

**Green Threads:**  
Threads managed entirely by the language runtime (JVM, Go runtime), invisible to the OS kernel. The OS sees only a small number of OS threads; the runtime multiplexes many lightweight threads on top.

- Old Java (<1.2) used green threads. Go uses "goroutines" (similar concept).
- Problem with early green threads: could not run in parallel on multiple CPU cores, because the OS only scheduled one OS thread (the runtime's thread).

**Virtual Threads (Java 21 — Project Loom):**  
The modern solution. Virtual threads are managed by the JVM, mapped to a small pool of OS carrier threads (typically equal to the number of CPU cores). When a virtual thread blocks (waiting for I/O, a database response, etc.), the JVM parks the virtual thread and puts a different virtual thread on the OS carrier thread.

```
Without virtual threads (Java <21):
┌────────────────────────────────────────────┐
│  10,000 HTTP requests → 10,000 OS threads  │
│  10,000 × 1MB stack = 10 GB RAM for stacks │
│  Massive context switch overhead            │
└────────────────────────────────────────────┘

With virtual threads (Java 21):
┌────────────────────────────────────────────────────────────────┐
│  10,000 HTTP requests → 10,000 virtual threads                  │
│  Small pool of OS carrier threads (e.g., 8 for 8-core CPU)     │
│  Each virtual thread: ~few KB of heap, not 1MB stack            │
│  When VT blocks on I/O → OS carrier thread runs another VT     │
│  10 GB RAM → a few MB; massive throughput improvement           │
└────────────────────────────────────────────────────────────────┘
```

This is why Spring Boot 3.2+ with virtual threads (`spring.threads.virtual.enabled=true`) can handle vastly more concurrent connections without the traditional thread-per-request bottleneck.

### Race Conditions

When multiple threads share memory and at least one modifies that memory, you have a **race condition** if the outcome depends on the precise timing of thread execution.

```
Classic race condition: two threads incrementing a counter

Thread 1:                          Thread 2:
1. Read counter (value: 5)
                                   1. Read counter (value: 5)
2. Add 1 (result: 6)
3. Write counter (value: 6)
                                   2. Add 1 (result: 6)
                                   3. Write counter (value: 6)

Expected result: counter = 7
Actual result:   counter = 6   ← Thread 2's read happened before Thread 1's write
```

This is a race condition because the result depends on which thread's write happened last. On a multi-core CPU, this happens constantly without synchronization.

At the hardware level: a "read-modify-write" sequence is NOT atomic — it is three separate operations, and another thread can interleave between any of them.

### Mutex (Mutual Exclusion Lock)

A **mutex** (mutual exclusion lock) is an OS primitive that allows only one thread to hold it at a time. Any other thread trying to acquire a held mutex will **block** (go into WAITING state) until the holder releases it.

```
Thread 1:          Thread 2:           Thread 3:
lock(mutex)
  [counter++]       → tries to lock → BLOCKS (waiting)
unlock(mutex)
                   → acquires lock
                     [counter++]
                     → tries to lock → BLOCKS (waiting)
                   unlock(mutex)
                                       → acquires lock
                                         [counter++]
                                       unlock(mutex)
```

Java's `synchronized` keyword is built on mutex-like primitives (specifically, it uses OS mutexes or hardware CAS — Compare-And-Swap — instructions depending on contention level).

### Deadlock

A **deadlock** occurs when two or more threads are each waiting for a lock that another thread holds, and none can proceed:

```
Thread A                           Thread B
lock(Lock1)                        lock(Lock2)
→ tries to lock Lock2 → BLOCKS     → tries to lock Lock1 → BLOCKS
  (waiting for B)                    (waiting for A)

Result: A waits for B. B waits for A. Neither ever releases. System freezes.
```

Deadlock requires four conditions (Coffman conditions): mutual exclusion, hold and wait, no preemption, circular wait. Breaking any one prevents deadlock.

**In Java:** Spring's `@Transactional` with database row locking can cause deadlock if two transactions update the same rows in opposite order. Database engines detect and resolve deadlocks by killing one transaction (which throws an exception your code must handle and retry).

---

> **📌 Interviews Ask This**
>
> **"What is a race condition? Give an example."**  
> A race condition occurs when two or more threads access shared mutable state without synchronization, and the outcome depends on their execution order. Classic example: two threads both read a counter at 5, both add 1, both write back 6. The counter should be 7 but is 6. Prevention: use `synchronized`, `AtomicInteger`, `ReentrantLock`, or design immutable shared state.
>
> **"What is a deadlock and how do you prevent it?"**  
> A deadlock occurs when Thread A holds Lock 1 and waits for Lock 2, while Thread B holds Lock 2 and waits for Lock 1. Neither can proceed. Prevention strategies: (1) always acquire locks in the same global order across threads, (2) use `tryLock()` with a timeout instead of blocking indefinitely, (3) use lock-free data structures (`ConcurrentHashMap`, `AtomicInteger`), (4) design with immutable objects that need no locking.
>
> **"What are Java virtual threads and why do they matter?"**  
> Virtual threads (Java 21) are lightweight threads managed by the JVM, mounted on a small pool of OS carrier threads. When a virtual thread blocks on I/O, the JVM unmounts it and runs another virtual thread on the same OS thread. This allows millions of virtual threads with minimal RAM (~few KB each vs ~1 MB for OS threads) and eliminates the bottleneck of OS thread limits. Spring Boot 3.2+ supports virtual threads, enabling high-concurrency servers without reactive programming.

---

## 2.5 Virtual Memory — How Every Process Gets Its Own Universe

### The Problem

Multiple processes share one physical RAM. If Process A is at physical address 5000 and Process B also tries to use address 5000, they would overwrite each other. The OS cannot dictate at compile time which exact physical addresses each program will use — it does not know what else will be running.

### The Solution: Virtual Address Spaces

**Virtual memory** gives each process the illusion that it has the entire address space to itself. Process A thinks it owns addresses 0 through 2^64. Process B also thinks it owns addresses 0 through 2^64. In reality, the OS maps these "virtual" addresses to completely different physical RAM locations.

```
Virtual Address Space           Physical RAM

Process A:                      ┌──────────────────────┐
┌──────────────┐  MMU           │  Physical Page 0     │
│Virtual pg 0  │────────────────►  (OS kernel)         │
│Virtual pg 1  │────────┐       ├──────────────────────┤
│...           │        │       │  Physical Page 1     │
└──────────────┘        │       │  (Process A data)    │
                        │       ├──────────────────────┤
Process B:              └──────►│  Physical Page 2     │
┌──────────────┐                │  (Process A code)    │
│Virtual pg 0  │────────────────►                      │
│Virtual pg 1  │──────┐        ├──────────────────────┤
│...           │      │        │  Physical Page 3     │
└──────────────┘      └────────►  (Process B data)    │
                               ├──────────────────────┤
                               │  Physical Page 4     │
                               │  (Process B code)    │
                               └──────────────────────┘
```

### Page Tables and the MMU

The OS maintains a **page table** for each process: a mapping from virtual page numbers to physical page (frame) numbers. The **Memory Management Unit (MMU)** is a hardware component inside the CPU that translates virtual addresses to physical addresses *automatically* on every memory access.

- **Page:** Fixed-size chunk of memory, typically **4 KB** (4096 bytes)
- **Page table entry:** Maps one virtual page to one physical frame, plus permission bits (read/write/execute)
- **TLB (Translation Lookaside Buffer):** A cache inside the CPU for page table lookups. Without it, every memory access would require reading the page table in RAM first — doubling all memory access costs.

### Page Faults

A **page fault** occurs when a process accesses a virtual address that is not currently backed by physical RAM:

```
Process accesses virtual address 0x7fff0000
         │
         ▼
MMU checks TLB → miss
         │
         ▼
MMU checks page table → "not present" bit set
         │
         ▼
CPU raises Page Fault exception
         │
         ▼
OS Page Fault Handler:
  - Is the address valid for this process? (In its virtual address space?)
    - No? → Segmentation Fault → kill process
    - Yes? → Continue
  - Is the page on disk (swapped out)?
    - Yes? → Find a free physical frame, load page from disk, update page table
    - No (e.g., first access, growing the heap)? → Allocate a new physical frame
         │
         ▼
Resume process from the faulting instruction (now succeeds)
```

Page faults are normal and happen constantly (e.g., whenever the heap grows, or a new file is read). They only become a problem when they require disk I/O — loading a page from swap or from a memory-mapped file — at which point the process stalls for ~100ms (disk access time).

**Thrashing** occurs when a system has too little RAM for all running processes. The OS spends more time swapping pages in and out of disk than running actual code. The system becomes nearly unresponsive. Solution: add RAM, kill processes, or reduce memory usage.

### The Virtual Address Space Layout of a Process

Every process's virtual address space has the same general layout:

```
High addresses (e.g., 0xFFFF FFFF FFFF FFFF on 64-bit)
┌─────────────────────────────────────────────────────┐
│             Kernel Space (reserved)                  │
│  OS kernel code and data mapped here for efficiency  │
│  User code cannot access this region                 │
├─────────────────────────────────────────────────────┤
│               Stack (grows downward ↓)               │
│  Local variables, function arguments, return addrs   │
│  Each thread has its own stack                       │
│                          │                           │
│                          ↓                           │
│                        (gap)                         │
│                          ↑                           │
│                          │                           │
│               Heap (grows upward ↑)                  │
│  Dynamically allocated memory (new/malloc)           │
│  Managed by JVM's GC in Java programs                │
├─────────────────────────────────────────────────────┤
│  BSS Segment                                         │
│  Uninitialized global and static variables           │
│  (zeroed by OS at process start)                     │
├─────────────────────────────────────────────────────┤
│  Data Segment                                        │
│  Initialized global and static variables             │
│  (static final String in Java)                       │
├─────────────────────────────────────────────────────┤
│  Text Segment (read-only)                            │
│  Compiled machine code instructions                  │
│  JVM bytecode or JIT-compiled native code            │
└─────────────────────────────────────────────────────┘
Low addresses (0x0000 0000 0000 0000)
```

**A critical subtlety for Java developers:**

When you write `new ArrayList<>()` in Java, that `ArrayList` object is allocated on the **JVM heap**. The JVM heap is a large chunk of physical RAM that the JVM reserves for itself at startup (controlled by `-Xmx` flag). The JVM's heap is itself located in the **heap segment** of the JVM *process's* virtual address space. There are two layers:

- The OS manages the JVM's virtual address space (the outer layer)
- The JVM's GC manages objects within the JVM heap (the inner layer)

This is why `-Xmx4g` (set JVM max heap to 4 GB) does not mean the entire process uses exactly 4 GB. The process also has memory for: the JVM itself, compiled native code, native libraries, thread stacks, off-heap buffers (used by Netty, Kafka, etc.), and OS memory mapping overhead.

---

## 2.6 File Systems — How Data Persists

### What a File System Is

A file system is the OS layer that organizes raw storage (bytes on disk) into a hierarchical structure of **files** (named byte sequences) and **directories** (named containers of files and other directories).

Without a file system, a disk is just a flat array of bytes numbered 0 through N. You would need to remember "my data starts at byte 1,237,492 and ends at byte 2,891,053." The file system gives you `/home/surya/projects/order-service/pom.xml` instead.

### Inodes — The File System's Core Data Structure

On Unix file systems (ext4, APFS), every file is represented by an **inode** (index node). An inode is a data structure stored on disk that contains:

```
Inode for a file:
┌────────────────────────────────────────────────────────────────┐
│  Inode number:      2847392                                    │
│  File type:         regular file (vs directory, symlink, etc.) │
│  Permissions:       -rwxr-xr-- (read/write/exec for owner)    │
│  Owner UID:         1000 (surya)                               │
│  Group GID:         1000                                       │
│  Size:              48,291 bytes                               │
│  Created:           2024-03-15 09:23:11                        │
│  Modified:          2024-03-20 14:55:03                        │
│  Accessed:          2024-03-21 08:12:44                        │
│  Hard link count:   1                                          │
│  Data block pointers: → disk blocks where file content lives  │
│    Block 0: physical disk sector 7291                          │
│    Block 1: physical disk sector 7292                          │
│    Block 2: physical disk sector 8500 (not contiguous)         │
│    ...                                                         │
└────────────────────────────────────────────────────────────────┘
```

**Critical insight:** The inode does NOT contain the filename. Filenames live in **directory entries**. A directory is itself a file that maps filenames to inode numbers. This is why:

- You can have a file with no name (after `unlink()` is called but the file is still open)
- Hard links work: two directory entries pointing to the same inode = one file, two names
- Renaming a file in the same filesystem is instant: just update the directory entry, no data copying

### Everything Is a File in Unix

Unix makes all I/O resources look like files:

| Type | Example | How it behaves |
|------|---------|----------------|
| Regular file | `/etc/hosts` | Contains bytes you can read/write/seek |
| Directory | `/home/surya/` | Contains directory entries |
| Character device | `/dev/null` | Read returns nothing; writes are discarded |
| Block device | `/dev/sda` | Raw access to disk sectors |
| Named pipe (FIFO) | `/tmp/mypipe` | One process writes, another reads |
| Unix socket | `/run/postgresql/.s.PGSQL.5432` | Local IPC channel (faster than TCP) |
| Symbolic link | `/usr/bin/python → python3.11` | Pointer to another path |

Your Spring Boot app uses TCP sockets for HTTP (network files), regular files for logs, and potentially Unix sockets for talking to a local database.

### File Descriptors

When a process opens a file, the OS returns an **integer** called a **file descriptor (fd)**. The process uses this integer for all subsequent operations on the file. The OS maintains a table mapping each file descriptor to an open file object:

```
Process's File Descriptor Table:
┌──────┬─────────────────────────────────────────────────────────┐
│  fd  │  Open File Object                                       │
├──────┼─────────────────────────────────────────────────────────┤
│  0   │  stdin  (keyboard input) ← always open at process start │
│  1   │  stdout (terminal output) ← always open at process start│
│  2   │  stderr (error output) ← always open at process start   │
│  3   │  /home/surya/app.log (opened with open())              │
│  4   │  /etc/config.properties                                 │
│  5   │  TCP socket (connection to PostgreSQL at :5432)         │
│  6   │  TCP socket (incoming HTTP connection from client)      │
│  ...  │  ...                                                   │
│  100 │  TCP socket (Kafka broker connection)                   │
└──────┴─────────────────────────────────────────────────────────┘
```

Every `read(fd, ...)`, `write(fd, ...)`, and `close(fd)` system call references the file descriptor number. Java's `FileInputStream`, `FileOutputStream`, `Socket`, and `ServerSocket` all wrap file descriptors under the hood.

**File descriptor limits and "too many open files":**  
The OS limits how many file descriptors one process can have open simultaneously (default is often 1024 or 65535 on Linux, configured via `ulimit -n`). A Spring Boot server under high load that opens:
- 200 HTTP connections
- 20 database connections (via HikariCP)
- 100 Kafka consumer/producer connections
- Hundreds of log files

...can approach this limit. Exceeding it causes `java.io.IOException: Too many open files`. Always close file/socket resources, always use try-with-resources, and configure `ulimit` appropriately in production.

### Buffered I/O

Reading or writing one byte at a time from disk or network is catastrophically slow — each byte would require a system call. Instead, the OS and Java standard library use **buffering**:

```
Naive: write 1000 bytes one at a time
→ 1000 system calls → significant overhead

Buffered: collect bytes in an 8KB buffer
→ when buffer is full (or flush() is called) → ONE system call with 8KB

Java:
FileOutputStream raw = new FileOutputStream("file.txt"); // NOT buffered
BufferedOutputStream buf = new BufferedOutputStream(raw); // adds a buffer
PrintWriter writer = new PrintWriter(buf);                // higher-level
```

This is why `BufferedOutputStream` wrapping `FileOutputStream` (or the equivalent `BufferedWriter` wrapping `FileWriter`) is almost always the right choice for file writing in Java. The buffer batches small writes into large, efficient OS calls.

---

> **📌 Interviews Ask This**
>
> **"What happens when a server throws 'Too many open files'?"**  
> The process has exceeded the OS file descriptor limit (`ulimit -n`). Every TCP connection (incoming HTTP, database, Kafka) consumes one fd. Every open file consumes one fd. Solutions: (1) configure ulimit higher (`ulimit -n 65535` in production), (2) ensure connections are properly closed (try-with-resources), (3) reduce connection counts via pooling. Diagnosis: `lsof -p <pid> | wc -l` counts fds in use by a process.

---

## Why This Matters for Your SDE-2 Journey

**Kubernetes and process isolation (Section 2.3):**  
Each container in Kubernetes runs a process in its own isolated namespace. The OS's process isolation guarantees that a memory bug in Service A cannot corrupt Service B's memory — even if they share the same Linux kernel on the same node. This is the security and reliability foundation that makes containerized microservices safe to run alongside each other.

**Thread limits and reactive/virtual threads (Section 2.4):**  
Traditional Spring MVC uses one OS thread per HTTP request. At 10,000 concurrent connections, that's 10,000 OS threads × 1 MB stack = 10 GB RAM just for stacks, plus enormous context-switching overhead. Spring WebFlux (reactive) solves this by using event loops with a tiny thread pool. Java 21 virtual threads solve it by making threads cheap. Understanding OS thread costs explains *why* these alternatives were invented.

**JVM heap and GC (Section 2.5):**  
The JVM heap (controlled by `-Xmx`) is a region of virtual memory. The JVM's garbage collector manages objects within it. When GC runs, it pauses all threads (stop-the-world), scans object graphs, and reclaims unused memory. Long GC pauses (seconds) in production are a real cause of latency spikes and `504 Gateway Timeout` errors. Understanding virtual memory and heap layout helps you tune GC parameters intelligently.

**File descriptors and connection pools (Section 2.6):**  
HikariCP, Spring's database connection pool, reuses TCP connections to PostgreSQL (each connection = one file descriptor) instead of creating a new TCP connection per query. Each TCP connection requires: a socket fd, a TCP handshake (~50ms RTT), TLS negotiation (~100ms), and PostgreSQL authentication. Connection pooling collapses all of that to near-zero overhead for subsequent queries.

**System calls and performance (Section 2.2):**  
Kafka's producer batches messages before calling `write()` to the network socket. This amortizes system call overhead across many messages, dramatically increasing throughput. This same principle explains why Kafka's performance degrades when you set `linger.ms=0` (no batching) and improves dramatically with `linger.ms=5` (5ms batching window).

---

---

# Chapter 3: How Programs Run — From Source Code to Execution

In Chapter 1 you learned that a CPU executes machine code — binary instructions specific to one hardware architecture. In Chapter 2 you learned that the OS runs programs as processes with isolated memory. Now the question becomes: how does the JavaScript or Java you write — human-readable text — become the machine code the CPU executes? And once it is machine code, how exactly does it start running?

This chapter traces that complete journey.

---

## 3.1 What Source Code Actually Is

### Source Code Is Text

Source code is a plain text file. Your `OrderController.java` or `server.js` is no different from a `.txt` file — it is bytes on disk, with each byte representing one character of text (encoded in UTF-8). The only thing that makes it "code" is that it follows a grammar (syntax rules) that a compiler or interpreter can translate into instructions.

```
"Hello World in Java" on disk:
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

On disk, this is bytes:
70 75 62 6c 69 63 20 63 6c 61 73 73 20 48 65 6c 6c 6f ...
 p  u  b  l  i  c  _  c  l  a  s  s  _  H  e  l  l  o

The computer does not "see" Java. It sees bytes.
A compiler converts those bytes into machine code bytes.
```

### The Abstraction Ladder

From the hardware's perspective, there is exactly one language: **machine code** — binary numbers that represent specific CPU operations. Everything else is an abstraction:

```
Abstraction Ladder (highest to lowest):

  ┌─────────────────────────────────────────────────────────────┐
  │  High-Level Language (Java, Python, JavaScript, TypeScript)  │
  │  Human-readable, platform-independent, type-safe             │
  │  OrderService.java, server.ts                                │
  ├─────────────────────────────────────────────────────────────┤
  │  Assembly Language                                           │
  │  One-to-one with machine instructions, human-readable names  │
  │  MOV RAX, 1 / ADD RBX, RAX / JMP 0x401234                   │
  ├─────────────────────────────────────────────────────────────┤
  │  Machine Code (Binary)                                       │
  │  Raw bytes the CPU fetches and executes                      │
  │  48 B8 01 00 00 00 00 00 00 00 / 48 01 D8 / E9 2C 00 00 00  │
  ├─────────────────────────────────────────────────────────────┤
  │  Electrical Signals                                          │
  │  Transistors switching on and off at billions of times/sec   │
  └─────────────────────────────────────────────────────────────┘
```

Each level is a translation of the level above into something closer to what the hardware actually executes.

### Three Approaches to Execution

Different languages take different paths from source code to running instructions:

**Compiled Languages (C, C++, Rust, Go):**  
The compiler translates your source code *before you run it* into machine code specific to one CPU architecture. The result is a native binary — a file of CPU instructions that the OS can load and execute directly.

```
Source code (.c / .rs / .go)
         │
         │  compiler runs ONCE before deployment
         ▼
Native Binary (.exe on Windows, no extension on Linux)
(machine code specific to x86-64, or ARM, etc.)
         │
         │  OS loads and runs at full CPU speed
         ▼
Running process
```

Advantages: Maximum runtime performance (no translation overhead), small deployment artifact.  
Disadvantages: Must recompile for each target OS/CPU architecture. A binary compiled for x86-64 Linux will not run on ARM macOS.

**Interpreted Languages (Python, Ruby, Shell scripts):**  
An interpreter reads the source code at runtime, line by line (or statement by statement), and executes each statement by calling its own built-in functions. The interpreter itself is a compiled native program.

```
Source code (.py / .rb)
         │
         │  stays as text files, shipped as-is
         ▼
Interpreter (Python, Ruby — these are compiled C programs)
reads + executes source line by line at runtime
         │
         ▼
Running process (but with interpretation overhead)
```

Advantages: Write once, run anywhere an interpreter exists. Easy to iterate (no compile step).  
Disadvantages: Significantly slower than compiled code — every statement requires the interpreter to figure out what to do, every time it is executed, even after running the same line 1,000,000 times.

**Just-In-Time Compiled (Java, C#, JavaScript V8):**  
A hybrid approach. The language first compiles to an **intermediate representation** (bytecode for Java, CIL for C#, bytecode for V8). At runtime, a virtual machine (JVM, CLR, V8 engine) initially interprets the bytecode. As it runs, it profiles which code is "hot" (executed frequently). It then **JIT-compiles** (Just-In-Time compiles) those hot methods directly to native machine code. After warmup, those methods run at near-native speed.

```
Source code (.java / .cs / .js)
         │
         │  compiler step (javac / tsc / Babel)
         ▼
Intermediate bytecode (.class files / .js bundles)
Platform-independent, not yet native machine code
         │
         │  JVM / V8 / CLR loads at runtime
         ▼
Interpreter: cold code runs in interpreter mode (slow)
         │
         │  profiler identifies "hot" methods
         ▼
JIT Compiler: hot methods compiled to native machine code
         │
         ▼
Hot code now executes as native code (near-native speed)
Cold code still interpreted
```

This is why Java application performance improves after "warmup." The first few minutes, the JVM is interpreting. After warmup, the JVM has compiled all hot paths to native code, and the application runs fast.

---

## 3.2 Compilation — Source Code to Executable

### The Compiler Pipeline

A compiler is a multi-stage transformation pipeline. Whether it produces native machine code (C compiler) or bytecode (Java compiler), the stages are similar:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Compiler Pipeline                         │
│                                                                  │
│  Source Code (.java file)                                        │
│        │                                                         │
│        ▼                                                         │
│  ┌──────────────────┐                                           │
│  │ Lexer/Tokenizer  │  Splits text into tokens:                 │
│  │                  │  "public", "class", "Hello", "{", "}"     │
│  │  "public class   │  Removes whitespace and comments          │
│  │  Hello { ... }"  │  Recognizes keywords vs identifiers       │
│  └──────────┬───────┘  Flags: "publik" is not a valid token     │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────┐                                           │
│  │     Parser       │  Builds Abstract Syntax Tree (AST)        │
│  │                  │  from the token stream                    │
│  │  Tokens →        │  Validates grammar structure              │
│  │  AST             │  "method must have a body" etc.           │
│  └──────────┬───────┘                                           │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────┐                                           │
│  │ Semantic Analyser│  Type checking: String + int → error      │
│  │                  │  Scope resolution: is "x" defined here?   │
│  │  AST → Annotated │  Method resolution: which overload?       │
│  │  AST             │  Access control: is this field public?     │
│  └──────────┬───────┘                                           │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────┐                                           │
│  │  Optimizer       │  Constant folding: 2+2 → 4 at compile time│
│  │  (optional)      │  Dead code elimination: remove unused code │
│  │                  │  Inlining: replace method call with body   │
│  └──────────┬───────┘                                           │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────┐                                           │
│  │  Code Generator  │  Emits JVM bytecode instructions          │
│  │                  │  (for javac) or native CPU instructions    │
│  │  AST →           │  (for C/Rust compilers)                   │
│  │  Bytecode /      │                                           │
│  │  Machine Code    │                                           │
│  └──────────┬───────┘                                           │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────┐                                           │
│  │  Linker          │  Combines multiple compiled files          │
│  │  (native only)   │  Resolves references between files         │
│  │                  │  Links in library code (libc.so etc.)      │
│  └──────────────────┘                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Java's Specific Compilation Process

Java has a two-stage compilation process:

**Stage 1: javac (ahead-of-time to bytecode):**  
```bash
javac OrderService.java
# Produces: OrderService.class (bytecode file)
```

The `.class` file contains **JVM bytecode** — a stack-based intermediate instruction set defined by the JVM specification. It is NOT machine code for any specific CPU. It is platform-independent.

You can inspect bytecode with `javap -c OrderService.class`:
```
public void processOrder(java.lang.String);
  Code:
     0: aload_0
     1: getfield     #2  // Field service
     4: aload_1
     5: invokevirtual #3  // Method execute:(Ljava/lang/String;)V
     8: return
```

These are JVM instructions (aload = load a reference, invokevirtual = call a method), not CPU instructions.

**Stage 2: JVM (interpretation + JIT at runtime):**  
When you run `java OrderService`, the JVM:

1. Loads `OrderService.class`
2. Interprets bytecode in the "interpreter mode" initially
3. The JVM's profiler (C1 compiler) monitors execution counts
4. Methods called more than ~10,000 times are JIT-compiled (C2 compiler) to native x86-64 or ARM code
5. Native compiled code runs at CPU-native speed

This is why the **JVM is called HotSpot** — it identifies the "hot spots" in your code and compiles only those, spending compilation effort where it matters most.

**Why GraalVM native image changes this:**  
GraalVM can perform the JIT compilation *ahead of time*, producing a native binary from your Java code with no JVM required at runtime. The result: instant startup (no JVM warmup), lower memory (no JVM overhead). Tradeoff: longer build time, some dynamic Java features break (reflection, class loading at runtime). Spring Native uses GraalVM for this.

---

## 3.3 How a Program Loads Into Memory and Starts Running

### Complete Step-by-Step: Running `java -jar myapp.jar`

This is every step, from the moment you press Enter:

```
You type: java -jar myapp.jar
                │
                ▼
1. Shell (bash/zsh) receives the command
   Shell calls fork() → creates a child process (copy of shell)
                │
                ▼
2. Child process calls exec("java", ["-jar", "myapp.jar"])
   - OS replaces child's memory image with the "java" binary from disk
   - OS reads /usr/bin/java (or wherever it is) into physical RAM
   - OS sets up virtual address space with text/data/bss/stack segments
                │
                ▼
3. JVM binary starts executing (it is a native C++ program)
   - JVM parses command-line arguments: "-jar myapp.jar"
   - JVM initializes subsystems:
     - GC: selects garbage collector (G1 by default), allocates heap
     - JIT compiler: initializes C1/C2 compiler threads
     - Class loader: prepares to load .class files
     - Thread system: creates main thread + GC threads + JIT threads
                │
                ▼
4. JVM locates and opens myapp.jar
   - A JAR is a ZIP file containing .class files
   - JVM reads the manifest (META-INF/MANIFEST.MF) to find Main-Class
   - ClassLoader loads the specified main class's .class file
                │
                ▼
5. JVM locates the main() method in the main class
   - By convention: public static void main(String[] args)
                │
                ▼
6. JVM executes main() in bytecode interpreter
   - Spring Boot: SpringApplication.run() triggers auto-configuration
   - Component scan discovers @Service, @Controller, @Repository classes
   - Spring loads configuration from application.yml / application.properties
   - Embedded Tomcat starts, binds to port 8080 (or configured port)
   - Connection pools initialize (HikariCP connects to PostgreSQL)
   - Spring context finishes: "Started MyApp in 3.142 seconds"
                │
                ▼
7. JVM enters an event loop (running Tomcat's acceptor threads)
   - Waiting for incoming HTTP connections
   - JIT compiler working in background, compiling hot methods
   - GC running in background, managing heap
```

**Why Java startup is slow:** Steps 3–6 involve loading thousands of classes, initializing frameworks, establishing database connections, and JIT-compiling. A production Spring Boot app can take 5–30 seconds to start.

**Why this matters for Kubernetes:** Kubernetes liveness and readiness probes must account for startup time. A pod that is killed and restarted takes 5–30 seconds before it can serve traffic. This startup delay is a significant operational concern for rolling deployments.

---

## 3.4 The Call Stack — How Function Calls Work

### What the Stack Is

When a function is called, the CPU needs to track:
- Where to return when the function finishes (the return address)
- The function's local variables
- The arguments passed to the function

These are stored in a **stack frame** — a region of memory allocated on the **call stack** (a LIFO data structure in the process's memory). Each function call pushes a new frame onto the stack; each return pops a frame off.

### Stack Frame Contents

```
One stack frame, for a method call in Java:

High address
┌──────────────────────────────────────────────────────┐
│  Caller's frame (above, higher address)              │
├──────────────────────────────────────────────────────┤
│  Return Address                                      │ ← where to jump when this method returns
├──────────────────────────────────────────────────────┤
│  Saved Registers                                     │ ← caller's registers we need to preserve
├──────────────────────────────────────────────────────┤
│  Function Arguments                                  │ ← int orderId, String customerId
├──────────────────────────────────────────────────────┤
│  Local Variables                                     │ ← int total, boolean isValid
├──────────────────────────────────────────────────────┤  ← Stack Pointer (SP) points here
│  (empty / next frame goes here)                      │
└──────────────────────────────────────────────────────┘
Low address (stack grows downward, toward lower addresses)
```

### How Function Calls Actually Work

```
Code:
  void main() {
      int result = calculateTax(100);
  }
  int calculateTax(int amount) {
      int rate = 20;
      return amount * rate / 100;
  }

Execution trace (stack grows downward):

BEFORE main() calls calculateTax():
  ┌─────────────────┐
  │   main() frame  │  ← SP (Stack Pointer)
  │   result: ???   │
  └─────────────────┘

AFTER call: calculateTax(100) is called
  ┌─────────────────┐
  │   main() frame  │
  │   result: ???   │
  ├─────────────────┤
  │calculateTax()   │  ← SP
  │  return addr    │  = address of "result = ..." in main
  │  amount: 100    │
  │  rate: 20       │
  └─────────────────┘

DURING EXECUTION: calculateTax computes 100 * 20 / 100 = 20

AFTER calculateTax() returns:
  ┌─────────────────┐
  │   main() frame  │  ← SP
  │   result: 20    │  ← return value stored here
  └─────────────────┘
```

The Stack Pointer register (SP) tracks the current top of the stack. Calling a function decrements SP (moves it to lower address = more stack space). Returning from a function increments SP (pops the frame).

### StackOverflowError — When the Stack Runs Out

The stack for each thread has a fixed size (default: 512 KB in Java, configurable with `-Xss`). Deep recursion adds a frame for each call. When the stack is full, the next function call cannot allocate a frame and the JVM throws `java.lang.StackOverflowError`.

```java
// This will StackOverflow:
int recurse(int n) {
    return recurse(n + 1);  // infinite recursion, no base case
}
```

Each call to `recurse()` pushes a new frame. After ~5,000–20,000 calls (depending on frame size and stack size), the stack is exhausted.

**Why local variables are fast:**  
Allocation on the stack is a single subtraction of the Stack Pointer. No heap allocation, no GC involvement. Stack allocation is effectively free compared to heap allocation.

**Why objects allocated with `new` are slower:**  
`new MyObject()` allocates on the JVM heap. This requires the JVM's allocator to find free space, possibly trigger GC, update GC metadata, and initialize the object. Modern JVMs are extremely fast at this (bump pointer allocation), but it is never as fast as stack allocation.

### Stack vs Heap for Local Variables

A key JVM optimization called **escape analysis** detects when an object allocated with `new` never "escapes" the method that created it — it is never returned, stored in a field, or passed to another thread. In that case, the JVM can allocate it on the stack (or in a CPU register) instead of the heap, entirely avoiding GC overhead.

```java
void processOrder(Order order) {
    // This point is never returned, never stored, never escapes
    StringBuilder sb = new StringBuilder();
    sb.append(order.getId());
    log.info(sb.toString());
    // sb goes out of scope here
    // JVM can allocate sb on the stack — no GC needed
}
```

---

## 3.5 Dynamic Linking and Libraries

### The Problem: Reusing Code Across Programs

Many programs use the same code — the C standard library functions (`printf`, `malloc`), cryptography routines, image decoding, etc. If every program contained a full copy of the standard library, every executable would be enormous, and you would have thousands of identical copies of the same library in RAM.

### Static vs Dynamic Linking

**Static linking:** The linker copies all required library code into the final executable at build time.

```
myapp.exe = myapp.o + libssl.o + libcrypto.o + libc.o (all embedded)
Size: 25 MB (includes entire libraries)
Runtime: no dependency on external files
Cost: each app has its own copy of the library in RAM
```

**Dynamic linking:** The executable contains *references* to library functions, but not the code itself. The OS loads the library separately and connects them at runtime.

```
myapp (small)  ─── depends on ──►  libc.so (shared library in RAM)
browser (small) ─── depends on ──►  libc.so (SAME copy in RAM)
server (small)  ─── depends on ──►  libc.so (SAME copy in RAM)

One copy of libc.so shared between all programs that need it.
```

On Linux, shared libraries have `.so` extension (Shared Object). On macOS: `.dylib`. On Windows: `.dll` (Dynamic Link Library).

### How Dynamic Linking Works at Runtime

1. The OS loader reads the executable's list of required dynamic libraries
2. For each library, the OS checks if it is already loaded in memory
3. If not, the OS reads the library from disk into memory (one copy, shared)
4. The OS connects the executable's function references to the actual addresses in the library
5. The program starts executing

```
Program starts:
OS reads ELF header: "requires libssl.so.3, libcrypto.so.3, libc.so.6"
                │
                ▼
OS dynamic linker (ld.so / ld-linux.so):
  - libssl.so.3 already in memory? No → load from /usr/lib/
  - libcrypto.so.3 in memory? No → load from /usr/lib/
  - libc.so.6 in memory? Yes → reuse (another program loaded it already)
                │
                ▼
Resolve symbols: program references "SSL_connect" →
  set program's pointer to actual address of SSL_connect in libssl.so.3
                │
                ▼
Program starts executing
```

### What This Means for Java

Java's JAR files are Java's equivalent of shared libraries — they contain compiled `.class` files that can be shared across programs. The JVM's ClassLoader is the equivalent of the dynamic linker.

The JVM itself (`libjvm.so`) is a native shared library that the `java` binary loads dynamically. When you run `java`, it:
1. Is a small native binary
2. Loads `libjvm.so` (the JVM implementation) dynamically
3. The JVM then loads your JAR's class files

This layered structure is why you can have multiple Java versions installed simultaneously on one system (each with its own `libjvm.so`) and switch between them with SDKMAN.

---

> **📌 Interviews Ask This**
>
> **"Why is Java's startup time slow and how does GraalVM native image fix it?"**  
> Java startup involves: JVM initialization (allocating heap, initializing GC), loading thousands of class files via ClassLoader, running Spring's component scanning and auto-configuration, JIT-compiling nothing yet (cold start). GraalVM native image eliminates this by performing all of the above at build time and producing a native binary. The native binary starts in milliseconds, uses less memory (no JVM overhead), but loses runtime JIT advantages and some dynamic Java features (reflection needs AOT configuration).
>
> **"What is a StackOverflowError and what causes it?"**  
> Each thread has a fixed-size stack (default 512KB-1MB in Java). Every method call adds a stack frame. Unbounded recursion (or very deep call chains) fills the stack. When no space remains for a new frame, the JVM throws `java.lang.StackOverflowError`. Fix: find the base case in recursive logic, convert recursion to iteration, or increase stack size with `-Xss` (rarely the right fix).
>
> **"What does the JVM's JIT compiler do and why does Java performance improve over time?"**  
> The JVM initially interprets bytecode (slow). As the program runs, its profiler counts method invocations. Methods called more than ~10,000 times ("hot methods") are compiled by the JIT to native machine code. After this warmup period, hot methods execute as fast as C code — the JVM is running real CPU instructions, not interpreting bytecode. This is why benchmarking Java code requires warming up the JVM first, and why Kubernetes deployments should expect reduced performance during the first minutes after a pod restart.

---

## Why This Matters for Your SDE-2 Journey

**Java's compilation model (Section 3.1):**  
You will explain in interviews: "Java compiles to platform-independent bytecode. The JVM then JIT-compiles hot bytecode to native code. After warmup, hot paths run at native speed." This is the answer to "Why use Java over C++ for high-throughput systems?"

**JVM startup and Kubernetes (Section 3.3):**  
Kubernetes liveness probes must set `initialDelaySeconds` high enough to account for Spring Boot startup (typically 15–60 seconds). Readiness probes should not send traffic until the application is fully initialized. Spring Boot Actuator's `/actuator/health` endpoint returns `DOWN` until all components are ready — that is what readiness probes should check.

**StackOverflowError root cause (Section 3.4):**  
Every senior Java engineer has debugged a StackOverflow in production. The fix is never `-Xss` (increasing stack size just delays the inevitable). The fix is finding the unbounded recursion — often in serialization/deserialization code with circular object references, or in framework code that calls your code which calls framework code in a loop.

**JARs as dynamic libraries (Section 3.5):**  
Understanding ClassLoaders explains some of the most mystifying Java errors: `ClassNotFoundException` (the JAR is not on the classpath), `NoClassDefFoundError` (the class existed at compile time but not at runtime), and `ClassCastException: X cannot be cast to X` (two different ClassLoaders loaded the same class — same class name, different class identity). Spring Boot's fat JAR bundling and its nested ClassLoader architecture solve these issues for application JARs.

---

---

# Chapter 4: Networking — How Computers Talk to Each Other

Your backend service does not live in isolation. It talks to databases, to other microservices, to Kafka brokers, to cloud APIs, to clients sending HTTP requests. All of that communication travels through networks — systems of cables, routers, protocols, and abstractions that let a packet originating in a browser in Chennai reach a server in a Mumbai datacenter and return a response in 20 milliseconds.

This chapter builds your mental model of how that actually works, from the physical signal to the HTTP response.

---

## 4.1 The Physical Reality

At the very bottom of all networking are physical signals:

- **Electrical signals** on copper cables (Ethernet)
- **Light pulses** through glass fibers (fiber optic)
- **Radio waves** through air (WiFi, 4G/5G)

These signals carry **bits** — 1s and 0s encoded as voltage levels, light presence/absence, or radio wave properties. A gigabit Ethernet cable transmits 1 billion bits per second.

**Network Interface Card (NIC):** Every device (laptop, server, router) has a NIC — a hardware chip that converts bits from your computer's internal bus into signals on the physical medium (and vice versa). When your Java app calls `socket.write()`, the OS ultimately tells the NIC to send those bytes as electrical/optical signals on the wire.

**MAC Address (Media Access Control):**  
Every NIC has a unique 48-bit identifier burned in at the factory. Written as 6 pairs of hex digits: `AA:BB:CC:DD:EE:FF`. These identify hardware devices on the *local* network and are used by switches.

**Switch:**  
A device that connects multiple computers on the same local network. It learns which MAC addresses are connected to which ports and forwards packets only to the correct destination port. A switch operates at Layer 2 (the Data Link layer) — it uses MAC addresses, not IP addresses.

**Router:**  
A device that connects *different* networks and forwards packets between them. Your home router connects your local network (192.168.1.0/24) to your ISP's network (public internet). Routers operate at Layer 3 (the Network layer) using IP addresses. Each router consults its **routing table** to decide which network interface to send each packet on.

```
[Your laptop]──────[Home Switch]──────[Home Router]──────[ISP Router]──────[Internet]
192.168.1.5          (Layer 2)          (Layer 3)           (Layer 3)
                    MAC-based           IP-based            IP-based
                    local only          first hop           backbone routing
```

---

## 4.2 The Network Models — OSI and TCP/IP

Networking is complex. Engineers manage this complexity by dividing it into **layers**, where each layer provides services to the layer above and uses services from the layer below. This modularity means HTTP does not need to know whether the physical layer is fiber or WiFi — the layers below handle it.

### The OSI Model (7 Layers — Conceptual)

The Open Systems Interconnection (OSI) model is a conceptual reference framework used to describe networking concepts. Every interview question about "which layer does X operate at?" uses this model.

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 7: Application  │ HTTP, HTTPS, SMTP, DNS, FTP, WebSocket │
│                        │ The protocols your code works with      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 6: Presentation │ TLS/SSL encryption, data encoding,     │
│                        │ compression (gzip, zlib)               │
├─────────────────────────────────────────────────────────────────┤
│  Layer 5: Session      │ Session establishment and teardown,     │
│                        │ authentication sessions                 │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: Transport    │ TCP, UDP — port numbers, reliability,   │
│                        │ flow control, error recovery            │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Network      │ IP (v4 and v6) — addressing, routing,  │
│                        │ fragmentation, packet forwarding        │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Data Link    │ Ethernet, WiFi — MAC addresses,        │
│                        │ frame creation, error detection         │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Physical     │ Electrical/optical/radio signals,       │
│                        │ cables, bit transmission                │
└─────────────────────────────────────────────────────────────────┘
```

Memory aid: **"Please Do Not Throw Sausage Pizza Away"** (Physical, Data Link, Network, Transport, Session, Presentation, Application).

### The TCP/IP Model (4 Layers — What Engineers Actually Use)

The TCP/IP model is simpler and maps to actual implementations:

```
┌─────────────────────────────────────────────────────────────────┐
│  Application    │ HTTP, HTTPS, WebSocket, SMTP, DNS, gRPC       │
│  (OSI 5-7)      │ Your Spring Boot code operates here           │
├─────────────────────────────────────────────────────────────────┤
│  Transport      │ TCP (reliable), UDP (unreliable)              │
│  (OSI 4)        │ OS provides via socket API                    │
├─────────────────────────────────────────────────────────────────┤
│  Internet       │ IP (v4/v6) — routing between networks         │
│  (OSI 3)        │ Handled by OS and routers                     │
├─────────────────────────────────────────────────────────────────┤
│  Network Access │ Ethernet, WiFi, fiber — physical delivery      │
│  (OSI 1-2)      │ Handled by NIC and device drivers             │
└─────────────────────────────────────────────────────────────────┘
```

### Encapsulation — How Layers Wrap Each Other

Each layer wraps the data from the layer above with its own **header** (and sometimes a footer). This is called **encapsulation**:

```
Your HTTP request travels through these transformations:

Application layer:  [HTTP Header][HTTP Body: {"orderId": 123}]

Transport layer:    [TCP Header: src_port=52341, dst_port=443, seq=1000]
                    [HTTP Header][HTTP Body]

Network layer:      [IP Header: src=10.0.0.5, dst=203.0.113.1]
                    [TCP Header][HTTP Header][HTTP Body]

Data Link layer:    [Ethernet Header: src_MAC, dst_MAC]
                    [IP Header][TCP Header][HTTP Header][HTTP Body]
                    [Ethernet Trailer: CRC checksum]

Physical layer:     01011010110001010110101010110... (bits on wire)
```

At the destination, each layer strips its header, processes it, and passes the payload up. The receiving HTTP server gets back `{"orderId": 123}` — the original data, without knowing anything about the IP routing or Ethernet framing that carried it.

**Why this matters:** This layering allows HTTP to work identically over wired Ethernet, WiFi, fiber optic, or cellular data — the physical and data link layers change, but HTTP sees no difference.

---

## 4.3 IP Addresses — The Network's Coordinate System

### IPv4 — The Current Dominant Standard

An IPv4 address is a 32-bit number, conventionally written as four decimal octets separated by dots:

`192.168.1.100`

Each octet is 8 bits (0–255). So `192.168.1.100` is:

```
192       168       1         100
11000000  10101000  00000001  01100100
```

2^32 = 4,294,967,296 possible addresses — fewer than the number of internet-connected devices today.

### IPv6 — The 128-bit Solution

IPv6 uses 128-bit addresses, written as 8 groups of 4 hexadecimal digits:

`2001:0db8:85a3:0000:0000:8a2e:0370:7334`

Consecutive groups of zeros can be shortened with `::`:

`2001:db8:85a3::8a2e:370:7334`

2^128 ≈ 340 undecillion addresses — enough for every atom on Earth to have its own address. IPv6 adoption is growing but IPv4 (with NAT) still dominates.

### Public vs Private IP Addresses

**Private IP ranges** (defined by RFC 1918) are not routed on the public internet. They are used inside homes, offices, and cloud VPCs:

| Range | CIDR | # of addresses |
|-------|------|----------------|
| 10.0.0.0 to 10.255.255.255 | 10.0.0.0/8 | 16 million |
| 172.16.0.0 to 172.31.255.255 | 172.16.0.0/12 | 1 million |
| 192.168.0.0 to 192.168.255.255 | 192.168.0.0/16 | 65,536 |

Your home has one public IP (assigned by your ISP) and your devices have private IPs like 192.168.1.5. **NAT (Network Address Translation)** lets multiple devices share one public IP by rewriting the source IP on outgoing packets and routing responses back correctly.

**Kubernetes:** Each pod gets an IP in a private range (e.g., 10.244.0.0/16 with Flannel CNI). These are private to the cluster. External traffic reaches them through NodePort, LoadBalancer, or Ingress resources.

### CIDR Notation

`192.168.1.0/24` means: "the first 24 bits of the address are the network identifier, the remaining 8 bits are for hosts."

With /24, there are 2^8 = 256 addresses (.0 to .255). Typically .0 is the network address and .255 is the broadcast address, leaving 254 usable host addresses.

```
CIDR    Hosts       Example
/8      16M         10.0.0.0/8 (Class A private)
/16     65,536      192.168.0.0/16
/24     256         192.168.1.0/24 (your home network)
/28     16          typical cloud subnet
/32     1           a single IP address
```

### Ports — Identifying Applications Within a Host

An IP address identifies a *machine*. A **port** (16-bit number, 0–65535) identifies which *application* on that machine should receive the packet.

```
Incoming packet: IP=203.0.113.5, Port=80
→ OS looks up which process is listening on port 80
→ Routes packet to that process (e.g., Nginx)

Incoming packet: IP=203.0.113.5, Port=443
→ OS routes to HTTPS server

Incoming packet: IP=203.0.113.5, Port=5432
→ OS routes to PostgreSQL
```

**Well-known ports (reserved, require root to bind):**

| Port | Protocol/Service |
|------|-----------------|
| 22 | SSH |
| 25, 587 | SMTP (email) |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 5432 | PostgreSQL |
| 3306 | MySQL |
| 6379 | Redis |
| 9092 | Kafka |
| 2181 | ZooKeeper |
| 8080 | Common default for app servers |

**Ephemeral ports (49152–65535):** When your laptop connects to a server, your OS assigns a random high-numbered port for the *outgoing* side of the connection. The server sees your connection as `(your_ip, 52341) → (server_ip, 443)`. When the response comes back to `your_ip:52341`, your OS routes it back to the browser tab that originated the connection.

---

## 4.4 DNS — Translating Names to Addresses

### The Problem DNS Solves

Humans remember names. Computers communicate via IP addresses. The Domain Name System (DNS) is a globally distributed database that maps one to the other.

When you type `api.example.com` in a browser, the OS has no idea what IP address that is. It must ask DNS.

### DNS Resolution — Step by Step

```
Browser on your laptop wants to reach api.shop.com:

Step 1: Check local cache
  ─────────────────────────────────────────────────────────────
  OS DNS cache: has it been resolved recently? TTL not expired?
    ─► YES → use cached IP, skip to connection
    ─► NO  → continue

Step 2: Ask the recursive resolver (your ISP or 8.8.8.8)
  ─────────────────────────────────────────────────────────────
  Your OS → Resolver (configured in /etc/resolv.conf)
  "What is the IP for api.shop.com?"

  Resolver checks its own cache:
    ─► Found → return cached IP
    ─► Not found → must do full recursive resolution

Step 3: Root name servers (13 clusters worldwide)
  ─────────────────────────────────────────────────────────────
  Resolver → Root server (addresses hardcoded in every resolver)
  "I need api.shop.com"
  Root: "I don't know api.shop.com, but for .com, ask 192.5.6.30"

Step 4: TLD (.com) name server
  ─────────────────────────────────────────────────────────────
  Resolver → TLD server for .com
  "I need api.shop.com"
  TLD: "I don't know, but shop.com's nameservers are ns1.shop.com"

Step 5: Authoritative name server for shop.com
  ─────────────────────────────────────────────────────────────
  Resolver → ns1.shop.com
  "I need the A record for api.shop.com"
  Authoritative: "api.shop.com → 203.0.113.5, TTL=300"

Step 6: Resolver caches and returns
  ─────────────────────────────────────────────────────────────
  Resolver caches "api.shop.com → 203.0.113.5" for 300 seconds
  Returns 203.0.113.5 to your browser

Step 7: Browser connects to 203.0.113.5:443
  ─────────────────────────────────────────────────────────────
```

This entire process typically takes 20–200ms the first time (round trips to multiple servers). After caching, it is instant (0ms — answered from local cache).

### DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| A | IPv4 address | `api.shop.com → 203.0.113.5` |
| AAAA | IPv6 address | `api.shop.com → 2001:db8::1` |
| CNAME | Alias to another name | `www.shop.com → shop.com` |
| MX | Mail server for the domain | `shop.com → mail.shop.com (priority 10)` |
| TXT | Arbitrary text | Used for SPF, DKIM (email verification), domain ownership |
| NS | Authoritative name servers | `shop.com → ns1.shop.com, ns2.shop.com` |
| PTR | Reverse DNS (IP → name) | `203.0.113.5 → api.shop.com` |
| SRV | Service location (port + weight) | Used by Kubernetes, SIP, XMPP |

### TTL (Time To Live)

Every DNS record has a TTL value (in seconds) that tells resolvers how long to cache it before asking again.

- `TTL = 60` (1 minute): changes propagate within 1 minute, but each query generates more DNS traffic. Use during migrations or when you need fast failover.
- `TTL = 86400` (24 hours): minimal DNS traffic, but changes take up to 24 hours to propagate globally. Use for stable, rarely-changed records.

**Kubernetes and DNS:** Every Kubernetes Service gets a DNS entry. Within a cluster, `order-service.default.svc.cluster.local` resolves to the Service's ClusterIP. This is how microservices find each other without hardcoding IPs. The DNS server in Kubernetes is **CoreDNS**, running as a Deployment in the `kube-system` namespace.

---

> **📌 Interviews Ask This**
>
> **"How does DNS work? Walk through what happens when a browser resolves a domain."**  
> (Walk through the 7 steps above: local cache → recursive resolver → root server → TLD server → authoritative server → cache → return.) Key points: DNS is hierarchical and distributed. Caching (TTL) reduces load. The recursive resolver (your ISP or 8.8.8.8) does the heavy lifting.
>
> **"How does Kubernetes service discovery work?"**  
> Kubernetes assigns each Service a ClusterIP (stable virtual IP) and creates a DNS record in CoreDNS: `<service>.<namespace>.svc.cluster.local`. Pods use this DNS name to communicate with services. When a Pod makes a request to `order-service`, CoreDNS resolves it to the ClusterIP, and kube-proxy routes the request to one of the healthy Pod endpoints behind the Service.

---

## 4.5 TCP — Reliable, Ordered Delivery

### UDP First — The Simple Baseline

Before TCP, understand its simpler sibling. **UDP (User Datagram Protocol)** is a minimal transport protocol:

- Send a packet: it either arrives or it doesn't. UDP does not know and does not care.
- No ordering: packets may arrive out of order. UDP does not reorder them.
- No connection: just send packets to an IP:port, no prior negotiation.
- No flow control: you can flood the receiver faster than it can process.

UDP's advantages: minimal overhead, lowest possible latency, no connection setup cost.  
Use cases: DNS queries (fast; retrying if no response is acceptable), video streaming (a dropped frame is better than a delayed one), online gaming (low latency more important than perfect reliability), IoT sensors.

### TCP — The Reliable Protocol

**TCP (Transmission Control Protocol)** adds reliability, ordering, and flow control on top of IP:

- **Reliable:** Every byte sent is acknowledged. If the acknowledgment does not arrive within a timeout, the sender retransmits.
- **Ordered:** Packets arrive out of order due to routing variations. TCP numbers each byte with a sequence number and reorders them before delivering to the application.
- **Flow control:** The receiver advertises a "window size" — how many bytes it can buffer. The sender never sends more than the receiver can accept.
- **Congestion control:** If the network is dropping packets (a sign of congestion), TCP slows down. Algorithms: CUBIC, BBR.

### The Three-Way Handshake — Establishing a TCP Connection

Before any data flows, TCP requires both parties to agree that a connection exists. This is done via a three-way handshake:

```
Client (initiating)                    Server (listening on port 443)
        │                                          │
        │  SYN (seq=x)                             │
        │─────────────────────────────────────────►│
        │  "I want to connect. My initial          │
        │   sequence number is x"                  │
        │                                          │
        │◄─────────────────────────────────────────│
        │  SYN-ACK (seq=y, ack=x+1)                │
        │  "OK. My seq number is y.                │
        │   I acknowledge yours: I expect byte x+1 next" │
        │                                          │
        │  ACK (ack=y+1)                           │
        │─────────────────────────────────────────►│
        │  "Acknowledged. I expect byte y+1 next"  │
        │                                          │
        │◄═══════════════ DATA FLOWS ══════════════│
        │                                          │
```

Each arrow represents one round trip. On a server in the same city, one RTT (Round Trip Time) ≈ 5–10ms. To a server on another continent, one RTT ≈ 100–300ms. The handshake costs **one full RTT** before any data can flow.

This is why:
- **Connection pooling** exists: HikariCP keeps connections to PostgreSQL open and reuses them, avoiding a new handshake per query
- **HTTP Keep-Alive** exists: reuse the TCP connection for multiple HTTP requests
- **HTTP/2** is faster: one TCP connection for many parallel requests

### TCP Four-Way Termination — Closing a Connection

Closing a TCP connection requires both sides to independently signal they are done sending:

```
Initiator (e.g., client)               Responder (e.g., server)
        │                                        │
        │  FIN (seq=u)                           │
        │───────────────────────────────────────►│  "I'm done sending"
        │                                        │
        │◄───────────────────────────────────────│
        │  ACK (ack=u+1)                         │  "Got it"
        │                                        │
        │  (Server may still be sending data)    │
        │◄───────────────────────────────────────│
        │  FIN (seq=v)                           │  "I'm also done sending"
        │                                        │
        │  ACK (ack=v+1)                         │
        │───────────────────────────────────────►│  "Got it. Connection closed."
        │                                        │
```

### TIME_WAIT State

After the initiator sends the final ACK, it enters `TIME_WAIT` for 2× MSL (Maximum Segment Lifetime, typically 30–120 seconds). This ensures:
1. The final ACK reaches the server (if it is lost, the server will retransmit its FIN and the client can re-send the ACK)
2. Packets from the old connection are flushed from the network before the same port is reused

**Production issue:** Under heavy load, a server that closes many short-lived connections accumulates thousands of sockets in `TIME_WAIT`. With a limit of ~65,535 ephemeral ports, the server can exhaust available ports and reject new connections. Solutions: reuse connections (`SO_REUSEPORT`), reduce `TIME_WAIT` duration (kernel tuning), use connection pooling to keep connections open.

### Sockets — The OS Abstraction for TCP Connections

A **socket** is the OS abstraction representing one endpoint of a TCP connection. It is identified by a 4-tuple:

```
Socket = (source_IP, source_port, destination_IP, destination_port)

Example:
(10.0.0.5, 52341, 203.0.113.100, 443)
 my laptop   random  api server    HTTPS
```

This 4-tuple uniquely identifies one TCP connection across the entire internet.

**Server socket vs connection socket:**

```
Server creates a listening socket:
ServerSocket server = new ServerSocket(8080);
→ OS opens a socket listening on port 8080

Client connects:
Socket client = server.accept();
→ OS creates a NEW socket for this specific connection
→ The listening socket remains open, continues accepting new connections

Multiple simultaneous connections:
Socket conn1 = (my_ip, 43215, server_ip, 8080)
Socket conn2 = (my_ip, 43216, server_ip, 8080)  ← same server port, different client port
Socket conn3 = (my_ip, 43217, server_ip, 8080)
→ Three separate connections, three separate sockets
→ All use the same server port 8080 (that is legal — src port differentiates them)
```

---

## 4.6 TLS/HTTPS — Encrypted Communication

### Why Plain HTTP Is Dangerous

HTTP sends all data as plain text. Any router, ISP, or attacker with access to the network between you and the server can read every byte you send (passwords, tokens, credit card numbers). This is a **man-in-the-middle attack**: the attacker sits between client and server, reading all traffic.

**TLS (Transport Layer Security)** solves this by encrypting all data between the client and server. HTTPS = HTTP over TLS.

### The TLS Handshake — How Encryption Is Established

TLS runs *before* any HTTP bytes are sent:

```
Client (Browser)                               Server (api.shop.com)
        │                                              │
        │─── ClientHello ─────────────────────────────►│
        │  TLS version: 1.3                            │
        │  Supported cipher suites: [AES-256-GCM, ...]│
        │  Client random nonce (32 bytes of randomness)│
        │                                              │
        │◄── ServerHello ──────────────────────────────│
        │  Chosen cipher suite: TLS_AES_256_GCM_SHA384 │
        │  Server random nonce                         │
        │  Server's digital certificate                │
        │    (contains: domain, public key, CA sig)    │
        │                                              │
        │  [Client verifies certificate:]              │
        │  ✓ Is it signed by a trusted CA?             │
        │  ✓ Does the domain match api.shop.com?       │
        │  ✓ Is it expired? (check Not Before/After)   │
        │  ✓ Is it revoked? (OCSP check)               │
        │                                              │
        │─── Key Exchange ────────────────────────────►│
        │  Client generates ephemeral key pair         │
        │  Sends public key to server                  │
        │  (TLS 1.3 uses Diffie-Hellman; no pre-master │
        │   secret encrypted with server's public key) │
        │                                              │
        │  [Both sides derive the same session keys]   │
        │  [from: client random + server random +      │
        │   shared DH secret — using agreed hash fn]   │
        │                                              │
        │◄══════ Encrypted Application Data ═══════════│
        │   Now all data is symmetric-encrypted        │
        │   with session keys (AES-256-GCM)            │
```

### Symmetric vs Asymmetric Encryption

**Asymmetric (public-key) cryptography:**  
Two mathematically linked keys: a **public key** (share with everyone) and a **private key** (keep secret). Data encrypted with the public key can only be decrypted with the private key. Used for: secure key exchange, digital signatures.

*Downside:* Computationally expensive (~1,000× slower than symmetric encryption). Cannot encrypt large amounts of data.

**Symmetric cryptography:**  
One shared key. Both sides encrypt and decrypt with the same key. Fast (AES hardware acceleration in modern CPUs). Problem: how do you share the key securely if the channel is not yet secure?

**TLS's elegant solution:**  
Use asymmetric cryptography *just for key exchange* (the handshake). Derive a symmetric session key that both sides know. Use symmetric encryption for all actual data.

```
Handshake: Asymmetric (slow but only for key exchange)
    → Both sides derive: symmetric session key (AES-256-GCM)

Data transfer: Symmetric (fast, uses hardware AES)
    → All HTTP data encrypted and decrypted with session key
```

### Certificate Authorities (CAs)

A **digital certificate** contains:
- The server's domain name (e.g., `api.shop.com`)
- The server's public key
- A digital signature from a Certificate Authority (CA)
- Validity period (Not Before, Not After)

A **Certificate Authority** is a trusted organization (DigiCert, Let's Encrypt, GlobalSign) whose public key is pre-installed in every browser and OS. When the CA signs a certificate, it is cryptographically guaranteeing: "I have verified that the entity presenting this certificate controls the domain api.shop.com."

The browser trusts certificates signed by any root CA in its trust store — typically 100+ CAs. This is a single point of failure: if a CA is compromised, attackers can issue fake certificates for any domain.

**Certificate chain:**

```
Root CA certificate (self-signed, pre-installed in browser)
     │ signs
     ▼
Intermediate CA certificate
     │ signs
     ▼
Server certificate (api.shop.com)
```

Your certificate must be accompanied by the intermediate CA certificates during the TLS handshake, so the browser can build the chain up to a trusted root.

**Self-signed certificates:** Certificates signed by yourself, not by a trusted CA. No browser trusts them by default → browser shows "Your connection is not private" warning. Used in development/testing environments only.

**Let's Encrypt:** A free CA that automates certificate issuance and renewal (90-day certificates, auto-renewed via ACME protocol). Powers HTTPS for a significant fraction of the internet.

---

## 4.7 HTTP — The Language of the Web

### HTTP Is a Text Protocol

HTTP (HyperText Transfer Protocol) is a request-response protocol that runs over TCP. Despite handling sophisticated web applications, at its core it is remarkably simple: text messages exchanged over a TCP connection.

### HTTP Request Structure

```
POST /api/v1/orders HTTP/1.1
Host: api.shop.com
Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2...
Content-Type: application/json
Accept: application/json
Content-Length: 52
X-Request-ID: 4f5a2b1c-8e3d-4a9f-b6c1-7d8e9f0a1b2c

{"customerId": "cust_123", "items": [{"productId": "p_456", "qty": 2}]}
```

Components:
- **Request line:** Method (`POST`), path (`/api/v1/orders`), HTTP version (`HTTP/1.1`)
- **Headers:** Key-value metadata. `Host` is mandatory in HTTP/1.1 (allows virtual hosting — multiple sites on one IP). `Authorization` carries the JWT.
- **Empty line:** Mandatory separator between headers and body (`\r\n`)
- **Body:** Only for methods that carry a body (POST, PUT, PATCH). For GET/DELETE, no body.

### HTTP Response Structure

```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/v1/orders/order_789
X-Request-ID: 4f5a2b1c-8e3d-4a9f-b6c1-7d8e9f0a1b2c
Cache-Control: no-cache

{"orderId": "order_789", "status": "PENDING", "total": 49.99}
```

Components:
- **Status line:** HTTP version, status code (201), reason phrase (Created)
- **Response headers:** Content-Type, custom headers (X-Request-ID for tracing)
- **Body:** The response data (JSON in this case)

### HTTP Status Code Categories

| Range | Category | Meaning |
|-------|----------|---------|
| 2xx | Success | Request succeeded |
| 3xx | Redirection | Client should request a different URL |
| 4xx | Client Error | The client made a bad request |
| 5xx | Server Error | The server failed to fulfill a valid request |

**Key codes every backend engineer must know:**

| Code | Name | When to use |
|------|------|-------------|
| 200 | OK | GET/PUT/PATCH succeeded, returning data |
| 201 | Created | POST succeeded, resource was created |
| 204 | No Content | DELETE succeeded, nothing to return |
| 400 | Bad Request | Invalid input (validation failed) |
| 401 | Unauthorized | Not authenticated (no/invalid token) |
| 403 | Forbidden | Authenticated but not authorized (wrong role) |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource, optimistic lock conflict |
| 422 | Unprocessable Entity | Semantic validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Generic server error (should not expose internals) |
| 502 | Bad Gateway | Load balancer got an error from upstream server |
| 503 | Service Unavailable | Server overloaded or in maintenance mode |
| 504 | Gateway Timeout | Load balancer's upstream server timed out |

### HTTP Methods (Verbs) and Their Semantics

| Method | Idempotent? | Safe? | Use |
|--------|-------------|-------|-----|
| GET | Yes | Yes | Retrieve resource |
| POST | No | No | Create new resource, submit data |
| PUT | Yes | No | Replace entire resource |
| PATCH | No | No | Partial update of a resource |
| DELETE | Yes | No | Delete a resource |
| HEAD | Yes | Yes | GET but no body (check existence, headers) |
| OPTIONS | Yes | Yes | Ask server what methods are allowed |

**Idempotent:** Calling the same operation multiple times with the same inputs produces the same result as calling it once. GET, PUT, DELETE are idempotent. POST is not — POST `/orders` twice creates two orders.

**Safe:** No side effects — does not modify server state. GET and HEAD are safe.

### HTTP/1.1 vs HTTP/2 vs HTTP/3

**HTTP/1.1:**  
- One request at a time per TCP connection (in HTTP/1.0) or one at a time with persistent connections (HTTP/1.1 Keep-Alive)
- **Head-of-line blocking:** Request 2 cannot begin sending until Request 1's response is fully received, even if they are independent
- Browsers open 6 parallel TCP connections per domain to work around this limitation
- Headers sent as plain text, repeated verbatim for every request (redundant)

**HTTP/2:**  
- **Multiplexing:** Multiple requests and responses interleaved on the same TCP connection simultaneously. No head-of-line blocking at the HTTP layer.
- **Header compression (HPACK):** Headers are compressed using a shared dictionary, dramatically reducing repetitive header bytes
- **Server push:** Server can proactively send resources the client will need
- **Binary framing:** No longer text-based; uses a binary frame format (more efficient)
- Used by gRPC (which runs over HTTP/2 for all communication)

```
HTTP/1.1 on one connection:
  ──[Req1]──[Resp1]──[Req2]──[Resp2]──[Req3]──[Resp3]──►
  Requests must wait for previous response

HTTP/2 on one connection:
  ──[Req1 frame]──[Req2 frame]──[Req3 frame]──►
  ◄─[Resp3 frame]──[Resp1 frame]──[Resp2 frame]──
  Requests and responses freely interleaved
```

**HTTP/3:**  
- Built on **QUIC** (a new transport protocol from Google) running over **UDP** instead of TCP
- Eliminates TCP-level head-of-line blocking (TCP's HOL blocking persists even with HTTP/2 multiplexing when a TCP packet is lost — all streams stall waiting for the retransmit)
- Faster connection establishment: combines TLS and QUIC handshakes
- Connection migration: your connection survives switching from WiFi to 4G (phone handover)

### WebSocket — Persistent Bidirectional Communication

HTTP is request-response: the client initiates every communication. For real-time applications (chat, live dashboards, collaborative editing), the server needs to push data to the client without the client requesting it.

**WebSocket** starts as an HTTP request but upgrades the connection to a persistent bidirectional channel:

```
Client                                Server
    │                                     │
    │── GET /ws HTTP/1.1 ────────────────►│
    │   Upgrade: websocket                │
    │   Connection: Upgrade               │
    │   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ== │
    │                                     │
    │◄── HTTP/1.1 101 Switching Protocols ─│
    │   Upgrade: websocket                │
    │   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo= │
    │                                     │
    │◄══════ WebSocket Frames ════════════►│
    │  (bidirectional, any time, either   │
    │   side can send without asking)     │
```

After the upgrade, the connection is no longer HTTP. It is a raw bidirectional frame stream over TCP, with the WebSocket framing protocol. Either side can send a message at any time.

---

> **📌 Interviews Ask This**
>
> **"What is the TCP three-way handshake and why does it matter for performance?"**  
> SYN → SYN-ACK → ACK. Establishes synchronized sequence numbers and proves both sides are reachable. Costs one full RTT before any data can flow. At 100ms RTT to a distant server, every new TCP connection costs 100ms before your first byte. This is why connection pooling (HikariCP, gRPC connection reuse, HTTP Keep-Alive) is critical — avoiding repeated handshakes dramatically reduces latency.
>
> **"What is TLS and how does HTTPS work?"**  
> TLS adds a handshake before HTTP data flows. The server presents a certificate (signed by a trusted CA) proving its identity and containing its public key. Client and server use asymmetric crypto to negotiate a symmetric session key. All subsequent data is encrypted with that session key using AES. The result: an eavesdropper who can intercept packets sees only encrypted bytes.
>
> **"What is the difference between HTTP/1.1, HTTP/2, and gRPC?"**  
> HTTP/1.1: one request at a time per connection, text headers. HTTP/2: multiplexed requests over one connection, binary framing, header compression. gRPC: uses HTTP/2 as its transport, Protocol Buffers as its serialization format (binary, type-safe, smaller than JSON), and supports four communication patterns: unary, server-streaming, client-streaming, bidirectional streaming.

---

## Why This Matters for Your SDE-2 Journey

**DNS and Kubernetes service discovery (Section 4.4):**  
When your OrderService calls PaymentService inside a Kubernetes cluster, the name `payment-service` is resolved by CoreDNS to the ClusterIP of the payment-service Kubernetes Service. kube-proxy then routes the TCP connection to one of the healthy Pods. Understanding DNS explains the entire service-to-service communication model.

**TCP handshake and HikariCP (Section 4.5):**  
HikariCP, Spring's default connection pool, maintains a pool of pre-established TCP connections to PostgreSQL (default pool size: 10). Without connection pooling, each database query would cost: DNS resolution + TCP handshake + TLS (if configured) + PostgreSQL authentication = ~50-200ms of overhead before the query even starts. Connection pooling reduces this to ~0ms.

**TLS and Spring Boot HTTPS (Section 4.6):**  
To serve HTTPS in Spring Boot, you configure a `server.ssl.*` block in `application.yml` with a keystore containing your certificate and private key. In Kubernetes, TLS is typically terminated at the Ingress controller (Nginx Ingress, Traefik), and internal service-to-service calls use plain HTTP (the cluster network is trusted). Understanding TLS is also essential for configuring SSL on Kafka brokers and your database connections.

**HTTP semantics and REST API design (Section 4.7):**  
Your SDE-2 portfolio projects must demonstrate correct HTTP usage: GET for retrieval (no side effects), POST for creation (returns 201 + Location header), PUT/PATCH for updates, DELETE for deletion. Status codes must be accurate: 401 vs 403, 404 vs 400. These are tested in system design interviews and code reviews.

**HTTP/2 and gRPC (Section 4.7):**  
Microservices that require high-throughput, low-latency service-to-service calls often use gRPC (Google Remote Procedure Call). gRPC runs over HTTP/2 (multiplexing + header compression) and uses Protocol Buffers instead of JSON. Spring Boot 3 has native gRPC support. Kafka's internal broker-to-broker and client-to-broker communication is also binary protocol, not HTTP.

---

---

# Chapter 5: How Different Types of Software Work

So far you have studied hardware, operating systems, compilation, and networking. Now you can see how these foundations combine to produce the different *kinds* of software that exist. You will build backend services that talk to databases, message queues, and frontend clients. Understanding how each type of software works — and how they communicate — rounds out your mental model.

---

## 5.1 Web Applications — The Client-Server Model

### The Fundamental Architecture

A web application consists of two separate programs:

- **The client (frontend):** Runs in the user's browser. Displays the UI, handles user input, makes network requests to the server.
- **The server (backend):** Runs on remote hardware. Handles business logic, data storage, security, and integration with other services.

These two programs communicate exclusively through a network interface — usually HTTP/HTTPS requests and JSON responses. The client cannot directly access the server's database or files; it can only send HTTP requests.

### The Complete Request Lifecycle

Here is everything that happens when a user clicks "Place Order" in a web app:

```
[Browser]                  [Network]            [Your Backend]       [Data Layer]
    │                          │                      │                    │
    │  1. User clicks "Order"  │                      │                    │
    │──────────────────────────────────────────────────────────────────► │
    │                          │                      │                    │
    │  2. JavaScript handler:  │                      │                    │
    │     fetch('/api/orders', │                      │                    │
    │       { method: 'POST',  │                      │                    │
    │         body: JSON })    │                      │                    │
    │                          │                      │                    │
    │  3. OS: DNS resolve api.shop.com → 203.0.113.5  │                    │
    │  4. OS: TCP handshake to 203.0.113.5:443        │                    │
    │  5. TLS handshake, certificate verification     │                    │
    │                          │                      │                    │
    │─── HTTP POST /api/orders ──────────────────────►│                    │
    │    Authorization: Bearer <JWT>                  │                    │
    │    Content-Type: application/json               │                    │
    │    {"customerId":"c1","items":[...]}             │                    │
    │                          │                      │                    │
    │                          │  6. Load Balancer receives request        │
    │                          │     (L4 or L7, selects one of N servers)  │
    │                          │     Forwards to: server-instance-3        │
    │                          │                      │                    │
    │                          │  7. Spring Boot:     │                    │
    │                          │     OncePerRequest   │                    │
    │                          │     Filter Chain:    │                    │
    │                          │     JwtFilter→Auth   │                    │
    │                          │     →Controller      │                    │
    │                          │                      │                    │
    │                          │  8. OrderController: │                    │
    │                          │     validate input   │                    │
    │                          │     → OrderService   │                    │
    │                          │                      │                    │
    │                          │  9. Check inventory: │                   │
    │                          │     Redis GET stock   │◄───────────────────│
    │                          │     (if miss: DB read)│────────────────────►
    │                          │                      │                    │
    │                          │  10. Save order:     │                    │
    │                          │     @Transactional   │                    │
    │                          │     INSERT order +   │                    │
    │                          │     UPDATE inventory ─────────────────────►
    │                          │     (PostgreSQL)     │◄───────────────────│
    │                          │                      │                    │
    │                          │  11. Publish event:  │                    │
    │                          │     Kafka producer   │                    │
    │                          │     OrderCreated {   │                    │
    │                          │       orderId: "o1"} ─────────────────────►
    │                          │                      │  (Kafka broker)    │
    │                          │                      │                    │
    │◄── HTTP 201 Created ─────────────────────────── │                    │
    │    Location: /orders/o1  │                      │                    │
    │    {"orderId":"o1", ...} │                      │                    │
    │                          │                      │                    │
    │  12. Browser updates UI: │                      │                    │
    │      shows confirmation  │                      │                    │
    │                          │                      │                    │
    │                          │  (async, later):     │                    │
    │                          │  Notification Service│                    │
    │                          │  consumes Kafka event│                    │
    │                          │  sends email/push    │                    │
```

This is the lifecycle you describe in every system design interview. Knowing each step — why a load balancer exists, what the filter chain does, why Kafka is asynchronous — is what separates a junior engineer from an SDE-2.

### What the Frontend Is

The frontend is three technologies working together:

- **HTML (HyperText Markup Language):** Describes the *structure* of the page — which elements exist and their hierarchy. `<div>`, `<button>`, `<input>`, `<table>`.
- **CSS (Cascading Style Sheets):** Describes the *presentation* — colors, fonts, layout, animations.
- **JavaScript:** Describes the *behavior* — what happens when you click, what data to fetch, how to update the DOM.

When your browser receives HTML from a server, it:
1. Parses HTML into a **DOM (Document Object Model)** — a tree of objects in memory
2. Parses CSS and applies styles to DOM nodes
3. Parses and executes JavaScript
4. **Renders** the page: computes layout, paints pixels to screen

TypeScript is JavaScript with a type system, compiled to plain JavaScript by the `tsc` compiler before it runs in the browser.

### REST vs GraphQL vs gRPC

These are the three main protocols for client-server communication:

**REST (Representational State Transfer):**  
Resource-based design. Each URL represents a resource. HTTP verbs indicate the action. Response format is JSON (usually). What you will build for your SDE-2 portfolio.

```
GET    /api/v1/orders          → list orders
GET    /api/v1/orders/123      → get order 123
POST   /api/v1/orders          → create an order
PUT    /api/v1/orders/123      → replace order 123
PATCH  /api/v1/orders/123      → partially update order 123
DELETE /api/v1/orders/123      → delete order 123
```

Advantages: simple, universally understood, works with any HTTP client, easy to cache.  
Disadvantages: over-fetching (GET /users returns all fields even if you only need the name) and under-fetching (need to make multiple requests to get related data).

**GraphQL:**  
A query language where the client specifies exactly which fields it needs. Single endpoint (`/graphql`). The client sends a query document describing the data shape it wants.

```graphql
# Client asks for exactly what it needs — no more, no less
query {
  order(id: "123") {
    id
    status
    customer {
      name
      email
    }
    items {
      product { name }
      quantity
    }
  }
}
```

Advantages: eliminates over-fetching and under-fetching. Strongly typed schema. Excellent for mobile clients with limited bandwidth.  
Disadvantages: complex backend implementation, N+1 query problems if not handled with DataLoader, difficult caching, overkill for simple APIs.

**gRPC (Google Remote Procedure Call):**  
Binary protocol using Protocol Buffers (protobuf) for serialization. Runs over HTTP/2. Generates type-safe client and server code from a `.proto` schema definition.

```protobuf
// orders.proto
service OrderService {
  rpc GetOrder (GetOrderRequest) returns (OrderResponse);
  rpc CreateOrder (CreateOrderRequest) returns (OrderResponse);
  rpc StreamOrders (StreamOrdersRequest) returns (stream OrderResponse);
}
message GetOrderRequest { string order_id = 1; }
message OrderResponse {
  string id = 1;
  string status = 2;
  double total = 3;
}
```

Advantages: binary (3–10× smaller than JSON), strongly typed with compile-time safety, HTTP/2 multiplexing, supports streaming, language-agnostic code generation.  
Disadvantages: not human-readable, requires tooling, not natively supported by browsers (need grpc-web proxy).

**When to use what:**  
- REST: external-facing APIs, public APIs, simple CRUD services
- gRPC: high-performance internal microservice-to-microservice calls
- GraphQL: client-driven APIs where different clients need different data shapes

### Stateless vs Stateful — A Critical Architecture Decision

**Stateful server:** The server stores session information in memory for each connected client. To handle the client's next request correctly, the same server that handled the previous request must receive this one (sticky sessions).

```
Stateful: client must always hit the same server

Client ──────► Server A (remembers: "user X is logged in")
Client ──────► Server A (only this server knows about user X!)
Client ──────► Server B (Server B has no session → "Not logged in!")
```

**Stateless server:** The server stores NO session state. Every request must be self-contained — it must include everything the server needs to process it. JWT (JSON Web Token) is the standard mechanism: the token itself contains the user's identity and permissions, signed by the server's private key.

```
Stateless: any server can handle any request

Client ──────► Server A (reads JWT → user X with ADMIN role)
Client ──────► Server B (reads JWT → user X with ADMIN role)
Client ──────► Server C (reads JWT → user X with ADMIN role)
→ Any server can verify the JWT's signature and know who the user is
```

**Why stateless scales better:** A load balancer can send any request to any server. You add servers to handle more load without session synchronization. This is why modern production systems (including your SDE-2 projects) use JWT instead of server-side sessions.

---

## 5.2 Web Servers and Application Servers

### The Difference Between a Web Server and an Application Server

These two terms are often confused. The distinction matters for your Spring Boot architecture.

**Web server (Nginx, Apache HTTP Server):**  
Handles HTTP requests. Specializes in:
- Serving static files (HTML, CSS, JS, images) directly from disk — very fast
- Reverse proxying: forwarding requests to backend application servers
- Load balancing across multiple application servers
- SSL/TLS termination (decrypting HTTPS before forwarding to app)
- Rate limiting, caching, compression, access control

Nginx is written in C and handles tens of thousands of concurrent connections with a small footprint. It does not run Java code.

**Application server (Tomcat, Jetty, Undertow):**  
Executes your application code (Java servlets, Spring MVC controllers). Handles the HTTP request lifecycle, thread management, connection management. Converts raw HTTP bytes into Java objects your code can work with.

### How Spring Boot Embeds Tomcat

Traditional Java web applications required a separate Tomcat (or Jetty) installation, and you would deploy your WAR file into it. Spring Boot changed this: it bundles a complete, runnable Tomcat (or Undertow or Jetty) *inside* your JAR file.

```
Traditional (pre-Spring Boot):
/opt/tomcat/webapps/myapp.war  ← deploy into running Tomcat
                └── Tomcat starts, loads, runs your code

Spring Boot:
myapp.jar  ← single fat JAR (Spring Boot + Tomcat embedded inside)
  └── java -jar myapp.jar
        └── JVM starts
            └── Tomcat starts inside the JVM
                └── Your Spring code starts
```

The `spring-boot-starter-web` dependency pulls in `spring-boot-starter-tomcat`, which includes `tomcat-embed-core` — Tomcat compiled as a library, not a standalone server. This is why you can run your Spring Boot app with `java -jar` and it is immediately an HTTP server.

### Why Nginx Sits In Front of Spring Boot in Production

```
Internet
   │
   ▼
[Nginx / Load Balancer]
   │  SSL termination (decrypt HTTPS once)
   │  Serve static files (images/CSS/JS) without hitting Spring Boot
   │  Rate limiting
   │  Route /api/* to Spring Boot, /static/* to CDN
   │
   ├──► [Spring Boot Instance 1] port 8080
   ├──► [Spring Boot Instance 2] port 8080
   └──► [Spring Boot Instance 3] port 8080
```

**SSL termination at Nginx:** Instead of each Spring Boot instance handling TLS, Nginx decrypts HTTPS and forwards plain HTTP to your Spring instances over the private network. This simplifies certificate management (only Nginx needs the cert) and reduces CPU overhead on application servers.

**Static file serving:** Nginx serves CSS/JS/images directly from disk at hardware speed without waking up your JVM. Spring Boot serving a 1MB image requires: thread allocation, JVM memory allocation, file reading, HTTP response construction. Nginx: a few syscalls to read and send the file.

### CDN (Content Delivery Network)

A CDN is a geographically distributed network of cache servers. Instead of all users fetching your static assets from your single origin server (in Mumbai, say), users fetch from the CDN node nearest to them:

```
Without CDN:
User in Tokyo ──────────► Origin server in Mumbai (150ms RTT)

With CDN:
User in Tokyo ──► CDN node in Tokyo (5ms RTT)
                  (CDN node fetched from Mumbai once, now cached)
```

CDNs (Cloudflare, Akamai, AWS CloudFront) cache your static assets at hundreds of locations worldwide. Users experience much lower latency for all static content. Your origin server only receives requests for cache misses or dynamic content.

For your SDE-2 portfolio projects, the architecture diagram should show: Internet → Nginx/ALB → Spring Boot → PostgreSQL + Redis + Kafka. CDN sits between users and your static assets.

---

## 5.3 Desktop Applications — Native and Electron

You will use VS Code, IntelliJ IDEA, and Docker Desktop constantly. Understanding how these work helps you reason about performance and understand their architecture.

### Native Desktop Applications

A native desktop application is compiled to machine code for a specific operating system:

- **macOS native:** Written in Swift or Objective-C, compiled to ARM64 or x86-64 binary. Uses Apple's Cocoa/AppKit UI framework. Xcode, Final Cut Pro, Figma (desktop).
- **Windows native:** Written in C++ or C#. Uses Win32 API or .NET WPF/WinForms. Visual Studio, Microsoft Office.
- **Linux native (GTK/Qt):** Written in C/C++ or Python with GTK or Qt bindings. GIMP, Inkscape.

Native apps have direct access to OS APIs: file system, GPU, camera, microphone, system notifications, accessibility APIs. They are compiled to machine code, so they are fast and have minimal overhead.

Distributed as:
- macOS: `.app` bundle (actually a directory), distributed via App Store or `.dmg` disk image
- Windows: `.exe` installer, distributed via Microsoft Store or website
- Linux: `.deb` / `.rpm` package, distributed via distro package managers or Snap/Flatpak

### Electron Applications

Electron bundles a full **Chromium browser engine** (the same engine in Chrome) and **Node.js** into a single package. Your application is a web app (HTML/CSS/JS) running inside this embedded browser.

```
Electron Application Architecture:

┌──────────────────────────────────────────────────────────────────┐
│                     Your Application Package                      │
│                                                                   │
│  ┌─────────────────────────┐  ┌───────────────────────────────┐  │
│  │    Main Process          │  │    Renderer Process(es)        │  │
│  │    (Node.js)             │  │    (Chromium)                 │  │
│  │                         │  │                               │  │
│  │  OS API access:          │  │  Your HTML/CSS/JS UI          │  │
│  │  - File system          │  │  Runs web technologies        │  │
│  │  - System notifications  │  │  Cannot access OS directly   │  │
│  │  - Window management    │  │  Each window = one renderer   │  │
│  │  - Native menus         │◄─►│  process                    │  │
│  │  - Auto-update          │IPC│  Communicates to main via    │  │
│  │                         │  │  IPC (ipcMain / ipcRenderer) │  │
│  └─────────────────────────┘  └───────────────────────────────┘  │
│                                                                   │
│  Bundled dependencies:                                            │
│  - Chromium (~100MB)                                              │
│  - Node.js (~30MB)                                                │
│  - Your app code (~10MB)                                          │
│  Total: 130-200MB minimum                                         │
└──────────────────────────────────────────────────────────────────┘
```

**Electron applications you use daily:** VS Code, Slack, Discord, Notion, Postman, 1Password (macOS version), GitHub Desktop.

**Why Electron is large:** Every Electron app bundles its own Chromium. If you have VS Code, Slack, and Postman installed, you have three separate Chromium engines on your disk, each ~100MB. This is why Electron apps are 150-300MB when a native equivalent might be 5-20MB.

**Why Electron apps use lots of RAM:** Each Electron app has a main process + one Chromium renderer process per window. Chromium is a multi-process browser engine. VS Code with several windows and extensions can easily use 500MB-2GB of RAM.

**The tradeoff:** Cross-platform from a single web codebase vs. the overhead of bundling a full browser engine. For VS Code (Microsoft), the development velocity of one TypeScript codebase across macOS, Windows, and Linux was worth the RAM cost.

---

## 5.4 Mobile Applications

Mobile context matters because your backend serves mobile clients. Understanding how mobile apps work informs your API design decisions.

### Native Mobile Applications

**iOS (Swift/Objective-C):**
- Compiled to ARM64 machine code
- Submitted to Apple's App Store as a `.ipa` archive
- The App Store reviews and signs the code; only signed apps can run on non-jailbroken iOS devices
- Access to iOS APIs: UIKit (UI), CoreLocation (GPS), AVFoundation (camera/audio), HealthKit

**Android (Kotlin/Java):**
- Compiled to DEX (Dalvik Executable) bytecode, then ART (Android RunTime) AOT-compiles it to native ARM code at install time
- ART is conceptually similar to the JVM: runs bytecode, manages memory with a GC
- Distributed via Google Play Store as a `.apk` or `.aab` (Android App Bundle)
- Access to Android APIs: Activities, Services, ContentProviders, BroadcastReceivers

### Cross-Platform Approaches

**React Native:**  
JavaScript code (React) runs in a JavaScript engine (JavaScriptCore/Hermes). Native bridge translates JavaScript calls into native UI components. Your React component renders as a real iOS `UIView` or Android `View`.

- Advantage: one JavaScript codebase for both iOS and Android
- Disadvantage: the JavaScript bridge has performance overhead; complex animations and gestures can stutter
- Used by: Meta, Microsoft (Teams mobile), Shopify

**Flutter:**  
Dart language compiles to ARM native code. Flutter draws its own UI using the Skia/Impeller graphics engine — it does not use iOS or Android's native UI components. Every pixel is painted by Flutter itself.

- Advantage: pixel-perfect consistency across platforms, no bridge overhead
- Disadvantage: larger app size (bundles Dart runtime + Flutter engine), some platform-specific integrations require writing native code

### Your Backend Serves Mobile Clients

Your Spring Boot REST API is the backend for both web frontends and mobile apps. Considerations when designing APIs for mobile:

- **Bandwidth:** Mobile networks are slower and less reliable than wired connections. Minimize response sizes (avoid returning all fields when you only need a few).
- **Offline support:** Mobile apps need to work without a connection. They cache API responses locally (SQLite, Room, Core Data). Your API needs `Last-Modified` and `ETag` headers for cache validation.
- **Push notifications:** You do not use HTTP polling. Mobile devices use Firebase Cloud Messaging (FCM) for Android and Apple Push Notification service (APNs) for iOS. Your backend publishes a notification event to Kafka, a notification service consumes it and calls FCM/APNs APIs.
- **Authentication:** Mobile apps send JWTs (stored in the device's secure keychain) with every request, identical to web browsers.

---

## 5.5 Background Services and Daemons

Most of the software you will build is not interactive — it runs permanently in the background without a UI.

### What a Daemon Is

A **daemon** (pronounced "dee-mun") is a background process that starts automatically, runs continuously, has no user interface, and provides services to other programs or the system.

On Linux, daemons conventionally have names ending in `d`: `sshd` (SSH server), `nginx` (web server/daemon), `postgresql` (database server), `dockerd` (Docker daemon), `systemd` (the init system that manages all other daemons).

### systemd — Managing Daemons on Linux

**systemd** is the init system on most modern Linux distributions. It is the first process started by the kernel (PID 1) and is responsible for starting, stopping, and monitoring all other system services.

You interact with it via `systemctl`:

```bash
# Start your Spring Boot app as a service
sudo systemctl start myapp

# Enable auto-start at boot
sudo systemctl enable myapp

# Check status (shows if running, recent log output)
sudo systemctl status myapp

# View logs
journalctl -u myapp -f

# Stop the service
sudo systemctl stop myapp
```

Your Spring Boot service in production likely runs as a systemd unit with a unit file like:

```ini
[Unit]
Description=My Spring Boot Order Service
After=network.target postgresql.service

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/java -Xmx2g -jar /opt/myapp/order-service.jar
Restart=always
RestartSec=10
Environment=SPRING_PROFILES_ACTIVE=production

[Install]
WantedBy=multi-user.target
```

In Kubernetes, systemd is replaced by the kubelet — Kubernetes' node-level daemon that starts, monitors, and restarts pods.

### Scheduled Jobs — Cron and Spring's @Scheduled

**Cron:** A Unix daemon that executes commands on a schedule defined by a crontab:

```bash
# Crontab format: minute hour day month weekday command
# Run database backup every day at 2:30 AM:
30 2 * * * /opt/scripts/backup-db.sh

# Run report generation every Monday at 9:00 AM:
0 9 * * 1 /opt/scripts/generate-weekly-report.sh
```

**Spring Boot's @Scheduled:**  
For in-process scheduling (the task runs within your Spring Boot JVM), Spring provides `@Scheduled`:

```java
@Component
public class CleanupTask {
    
    // Run every 24 hours (24 * 60 * 60 * 1000 milliseconds)
    @Scheduled(fixedRate = 86400000)
    public void cleanExpiredSessions() {
        // runs in a separate thread pool within the JVM
    }
    
    // Cron expression: every day at 2:30 AM
    @Scheduled(cron = "0 30 2 * * *")
    public void generateDailyReport() {
        // runs at the specified time
    }
}
```

`@Scheduled` is simple but has a critical limitation: **it only runs in one instance of your application.** If you deploy 3 instances of your service in Kubernetes, all 3 run the scheduled task simultaneously. For distributed scheduling (run once across all instances), use `ShedLock` (a library that uses your database as a distributed lock) or a dedicated job scheduler (Quartz, Spring Batch).

### Kafka Consumers — The Long-Running Daemon Pattern

A Kafka consumer is a daemon: it starts, connects to Kafka brokers, and then loops forever — polling for new messages, processing each one, committing offsets:

```
Kafka Consumer lifecycle:

Application start
     │
     ▼
Consumer.subscribe(["order-created-topic"])
     │
     ▼
┌─────────────────────────────────────────────┐
│  while (running) {                          │
│    records = consumer.poll(Duration.ofMs(100)) │
│    for (record : records) {                  │
│      processMessage(record);                 │
│      // update inventory, send email, etc.  │
│    }                                         │
│    consumer.commitSync(); // mark as processed│
│  }                                           │
└─────────────────────────────────────────────┘
     │
     ▼
Application shutdown (SIGTERM received)
  consumer.wakeup() → poll() throws WakeupException → exit loop
  consumer.close()   → commits final offsets, releases partition assignment
```

In Spring Boot, `@KafkaListener` hides this loop behind an annotation, but the underlying daemon thread structure is the same.

---

## 5.6 CLI Tools and Scripts

As a backend engineer, you spend significant time in the terminal. Understanding how CLI tools work makes you more effective.

### How CLI Tools Work

A CLI tool is an ordinary process with no GUI. It reads from **stdin** (standard input, file descriptor 0), writes output to **stdout** (standard output, fd 1), and writes errors to **stderr** (fd 2).

When you run `java -jar myapp.jar --port=8080`:
1. The shell calls `fork()` and `exec("java", ["-jar", "myapp.jar", "--port=8080"])`
2. The OS provides the arguments as an array of strings in the new process
3. Java's `main(String[] args)` receives `["-jar", "myapp.jar", "--port=8080"]`
4. Your code parses these arguments (Spring Boot auto-parses `--key=value` as properties)
5. The tool runs, writes output to stdout, exits with code 0 (success) or non-zero (error)

The **exit code** is how a CLI tool signals success or failure to the shell. `0` = success, any other value = error. In scripts, `$?` holds the exit code of the last command.

### Unix Pipes — Composing Tools

Unix philosophy: write tools that do one thing well, connected with pipes.

A **pipe** (`|`) connects one command's stdout to the next command's stdin:

```bash
# Count error lines in a log file, sorted by frequency
cat /var/log/myapp.log | grep "ERROR" | sort | uniq -c | sort -rn | head -20

# Steps:
# cat          → read file, send to stdout
# grep "ERROR" → filter: only pass lines containing "ERROR"
# sort         → sort lines alphabetically
# uniq -c      → count consecutive duplicate lines
# sort -rn     → sort by count, descending, numerically
# head -20     → show only first 20 lines

# Output: "     127 ERROR Failed to connect to database"
#         "      45 ERROR NullPointerException in OrderService"
```

Each command is a separate process. The OS connects their file descriptors: command1's stdout fd → command2's stdin fd. Data flows as byte streams between processes.

### Essential Backend Engineering CLI Commands

```bash
# Process management
ps aux                          # list all running processes
ps aux | grep java              # find Java processes
top / htop                      # live CPU/memory usage per process
kill -15 <pid>                  # graceful shutdown (SIGTERM)
kill -9 <pid>                   # force kill (SIGKILL, use as last resort)

# File descriptors (debug "too many open files")
lsof -p <pid>                   # list all open files/sockets for a process
lsof -p <pid> | wc -l           # count open file descriptors
lsof -i :8080                   # which process is using port 8080?

# Network debugging
netstat -tlnp                   # listening ports and their PIDs
ss -tlnp                        # same, faster than netstat
curl -v https://api.example.com # verbose HTTP request (see headers, TLS)
curl -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"key":"value"}' https://api.example.com/endpoint

# jq — JSON processor (essential for API testing)
curl https://api.example.com/orders/123 | jq '.'        # pretty-print JSON
curl https://api.example.com/orders | jq '.[].id'       # extract all IDs
curl https://api.example.com/orders | jq '.[] | select(.status=="PENDING")'

# Grep for log analysis
grep "ERROR" /var/log/app.log | tail -50        # last 50 errors
grep -n "OrderService" /var/log/app.log          # with line numbers
grep -A 5 "StackOverflow" /var/log/app.log       # 5 lines after match
grep -B 3 "NullPointer" /var/log/app.log         # 3 lines before match

# Find and disk usage
find /var/log -name "*.log" -mtime +7            # logs older than 7 days
du -sh /var/log/*                                # disk usage per subdirectory
df -h                                            # disk space on all filesystems

# System info
uname -a                                         # OS and kernel version
free -h                                          # RAM usage
vmstat 1                                         # CPU/memory/IO stats every 1s
iostat -x 1                                      # disk I/O stats every 1s
```

### Docker CLI

Docker is central to your workflow. Every command maps to OS operations under the hood:

```bash
# Image management
docker pull openjdk:21-slim          # download image from Docker Hub
docker build -t myapp:1.0 .          # build image from Dockerfile
docker images                         # list local images
docker rmi myapp:1.0                  # remove image

# Container lifecycle (each container is an isolated process)
docker run -d -p 8080:8080 myapp:1.0                   # start container (daemon)
docker run -it ubuntu bash                              # interactive container
docker ps                                               # list running containers
docker ps -a                                            # include stopped containers
docker stop <container_id>                              # graceful stop (SIGTERM → SIGKILL)
docker rm <container_id>                                # remove stopped container

# Debugging running containers
docker logs <container_id>                              # view stdout/stderr
docker logs -f <container_id>                           # follow live
docker exec -it <container_id> bash                     # shell inside container
docker stats                                            # live CPU/memory per container

# Docker Compose (for local multi-service dev)
docker-compose up -d                                    # start all services
docker-compose down                                     # stop and remove containers
docker-compose logs -f order-service                    # follow one service's logs
```

---

## 5.7 Microservices — Independent Deployable Units

Understanding microservices is mandatory for SDE-2 interviews and for your portfolio projects. This section explains the architecture, not as a buzzword, but from first principles.

### The Monolith First

A **monolith** is an application where all the code runs in one process, deployed as one unit:

```
Monolith (one JVM process):
┌────────────────────────────────────────────────────────────────┐
│                   order-management-service                       │
│                                                                  │
│  OrderController  ←→  OrderService  ←→  OrderRepository        │
│  UserController   ←→  UserService   ←→  UserRepository         │
│  ProductController ←→ ProductService ←→ ProductRepository      │
│  PaymentController ←→ PaymentService ←→ PaymentRepository      │
│                                                                  │
│  All in ONE JAR, ONE process, ONE database schema               │
└────────────────────────────────────────────────────────────────┘
```

**Monolith advantages:**
- Simple deployment (one artifact)
- Simple development (one IDE, one codebase, in-process function calls)
- No network overhead between components
- Simple transactions (one database, ACID transactions span all components)
- Simple debugging (one stack trace, one log stream)

**Monolith disadvantages at scale:**
- Scaling: must scale the entire application even if only the order component needs more capacity
- Deployment: changing the payment component requires deploying the entire application → higher risk
- Technology: entire codebase must use the same language/framework/version
- Team coupling: OrderTeam and PaymentTeam both edit the same codebase → merge conflicts, coordination overhead

### Microservices Architecture

**Microservices** decompose the monolith into separate services, each:
- A separate OS process (usually a separate container)
- Deployed independently on its own schedule
- Responsible for one business domain
- Owning its own database (no shared database)
- Communicating with other services via network (HTTP, gRPC, or message queue)

```
Microservices (each is a separate JVM process / container):

[API Gateway / Load Balancer]
         │
         ├──────────────► [order-service]  → PostgreSQL (orders DB)
         │                    │ publishes events
         │                    ▼
         │               [Kafka]  ← consumed by:
         │                    ├──► [notification-service] → email/push
         │                    └──► [inventory-service]  → MySQL (inventory DB)
         │
         ├──────────────► [user-service]   → PostgreSQL (users DB)
         │
         ├──────────────► [payment-service] → PostgreSQL (payments DB)
         │                    │
         │                    └──► calls [fraud-detection-service] via gRPC
         │
         └──────────────► [product-service] → MongoDB (products DB)
```

### Microservice Communication Patterns

**Synchronous communication (HTTP/gRPC):**  
Service A sends a request and waits for Service B's response before proceeding.

```
OrderService → HTTP POST → PaymentService
OrderService waits...
PaymentService processes, returns {status: "APPROVED"}
OrderService continues with confirmed payment
```

When to use: when you need the response immediately to make a decision (order cannot be confirmed without payment approval).  
Tradeoff: OrderService is now **coupled** to PaymentService's availability. If PaymentService is down, orders cannot be placed. Circuit breakers (Resilience4j) mitigate this.

**Asynchronous communication (Kafka/RabbitMQ):**  
Service A publishes a message to a message broker and immediately continues. Service B reads and processes the message later, independently.

```
OrderService publishes: {"event":"OrderCreated", "orderId":"o1"}
→ Kafka stores the message in topic "order-events"
→ OrderService continues: returns 201 Created to the user immediately

(Later, independently):
NotificationService reads "OrderCreated" from Kafka
→ sends confirmation email
→ takes 2 seconds but user already got their 201

InventoryService reads "OrderCreated" from Kafka
→ reserves inventory items
→ happens in the background
```

When to use: for side effects that do not need to happen before responding (notifications, analytics, audit logs, updating read models, triggering workflows).  
Tradeoff: eventual consistency (the email goes out a few seconds after the order is created, not instantly). Debugging across async flows requires distributed tracing (Jaeger, Zipkin).

### Service Discovery — How Services Find Each Other

With microservices, each service has a network address (IP:port). But IPs change constantly in Kubernetes (pods are ephemeral). How does OrderService find PaymentService?

**DNS-based discovery (Kubernetes):**  
Kubernetes assigns a **Service** (a stable virtual IP + DNS name) to each microservice. The DNS name is stable even as pod IPs change:

```bash
# Inside a Kubernetes cluster, this DNS name always works:
curl http://payment-service.default.svc.cluster.local:8080/api/payments/process
      └──────────────────────────────────┘
      stable DNS name (regardless of pod IPs)
      Kubernetes routes it to one of the healthy pods

# Often just the service name works within the same namespace:
curl http://payment-service:8080/api/payments/process
```

**Service registry (Consul, Eureka):**  
Each service registers itself (its IP:port) with a central registry on startup and deregisters on shutdown. Clients query the registry to find the current address of the service they want to call.

### Data Isolation — No Shared Databases

One of the most important microservice rules: **each service owns its own database**. No other service can directly query that database.

```
WRONG (monolith database shared):
order-service ──────────────────► orders schema
payment-service ────────────────► orders schema (!!!cross-service query)
user-service ────────────────────► orders schema (!!!cross-service query)

RIGHT (database-per-service):
order-service   → orders_db    (PostgreSQL, only order-service can touch it)
payment-service → payments_db  (PostgreSQL, only payment-service can touch it)
user-service    → users_db     (PostgreSQL, only user-service can touch it)

Cross-service data access: via API calls or events, never direct DB access
```

**Why this matters:**  
- PaymentService can migrate or replace its database without asking OrderService
- OrderService cannot accidentally break PaymentService's data
- Each service can use the database technology best suited to its data (SQL, MongoDB, Redis)

---

> **📌 Interviews Ask This**
>
> **"What is the difference between a monolith and microservices? When would you choose each?"**  
> Monolith: one process, simple development, ACID transactions, easy debugging. Microservices: separate processes, independent deployment, polyglot persistence, team autonomy, better fault isolation — but much higher operational complexity (service discovery, distributed tracing, eventual consistency, deployment pipelines per service).
>
> Choose a monolith for a new product/small team (simplicity wins early on). Choose microservices when team/scale/deployment-independence needs force the split. Common antipattern: microservices from day one, before you know your domain boundaries.
>
> **"How do microservices communicate?"**  
> Two patterns: (1) Synchronous: HTTP REST or gRPC — service waits for response, tight coupling, use when the caller needs the result immediately. (2) Asynchronous: message broker (Kafka, RabbitMQ) — publisher fires and continues, consumer processes later, loose coupling, use for side effects and eventual consistency. Most real systems use both.

---

## Why This Matters for Your SDE-2 Journey

**The complete HTTP lifecycle (Section 5.1):**  
In every system design interview, you walk through this: user clicks → DNS → TCP + TLS → HTTP → load balancer → filter chain → controller → service → database/cache/Kafka → response. Knowing each step, and why it exists, is what distinguishes an SDE-2 answer from a junior answer.

**JWT and stateless design (Section 5.1):**  
Your portfolio's Order Management API uses JWT for authentication. The stateless design (JWT carries identity in the token) means any of your service's instances can process any request. This is what enables horizontal scaling — just add more pods.

**Nginx + Spring Boot (Section 5.2):**  
Your system design diagrams should show an Nginx or API Gateway layer in front of Spring Boot. SSL terminates at the edge. Static assets go to CDN. Dynamic API calls reach Spring Boot. This layered architecture is standard and will be questioned in interviews.

**Kafka consumers as daemons (Section 5.5):**  
Your notification service and inventory service in your portfolio e-commerce project run as @KafkaListener beans — long-lived daemon threads within their respective Spring Boot processes, consuming events published by the order service. Understanding the consumer lifecycle helps you handle shutdown gracefully and understand consumer group rebalancing.

**Docker CLI mastery (Section 5.6):**  
All your development is containerized. `docker-compose up -d` to start PostgreSQL + Kafka + Redis for local development. `docker exec -it postgres psql -U admin` to debug database state. `docker logs -f notification-service` to follow a service's output. These are daily operations, not occasional ones.

**Microservice architecture for your portfolio (Section 5.7):**  
Your "Scalable E-Commerce Platform" portfolio project should be a microservices system: order-service, payment-service, inventory-service, notification-service — each a separate Spring Boot app, communicating via Kafka for async events and REST/gRPC for synchronous calls. This is the architecture senior engineers design, and discussing it intelligently in interviews is the goal.

---

---

# Chapter 6: Developer Environment, Git, and Tooling

The previous five chapters built your mental model. This chapter translates that model into a working environment — the tools you will use every day for 120 days of SDE-2 preparation. Set this up correctly once and never think about it again.

Every tool recommendation here is justified. Nothing is installed for fashion. You will use everything.

---

## 6.1 Setting Up the Java Development Environment

### The Tools You Need and Why

| Tool | Version | Why |
|------|---------|-----|
| JDK 21 | 21.0.x (Temurin) | Java 21 LTS — virtual threads, records, pattern matching, sealed classes. All new Spring Boot projects. |
| Maven | 3.9.x | Build system, dependency management. The default for Spring Boot projects. |
| IntelliJ IDEA | Latest Community | Best Java IDE in existence. Free community edition is enough for everything in this plan. |
| Docker Desktop | Latest | Run PostgreSQL, Kafka, Redis locally without installing them natively. |
| Git | 2.x | Version control. Required for everything. |
| Postman | Latest | API testing during development. |

### Installing JDK 21 via SDKMAN

**SDKMAN** is a version manager for JVM-based tools — the Java equivalent of `nvm` for Node.js. It lets you install multiple Java versions and switch between them instantly.

**Step 1: Install SDKMAN**

```bash
# macOS / Linux / WSL2 (Windows):
curl -s "https://get.sdkman.io" | bash

# Open a new terminal (or source the init script):
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Verify:
sdk version
# SDKMAN 5.18.x
```

**Step 2: Install JDK 21 (Eclipse Temurin — the recommended open-source distribution)**

```bash
# List available Java 21 versions:
sdk list java | grep 21

# Install Eclipse Temurin 21 (LTS, open-source, production-safe):
sdk install java 21.0.3-tem

# Set as default:
sdk default java 21.0.3-tem

# Verify:
java -version
# openjdk version "21.0.3" 2024-04-16 LTS
# OpenJDK Runtime Environment Temurin-21.0.3 (build 21.0.3+9)
# OpenJDK 64-Bit Server VM Temurin-21.0.3 (build 21.0.3+9, mixed mode)

javac -version
# javac 21.0.3
```

**Step 3: Set JAVA_HOME**

Add to your `~/.zshrc` (macOS) or `~/.bashrc` (Linux):

```bash
# SDKMAN auto-exports JAVA_HOME when you switch versions.
# If you need it explicitly for other tools (Maven, IntelliJ):
export JAVA_HOME="$HOME/.sdkman/candidates/java/current"

# Verify:
echo $JAVA_HOME
# /Users/surya/.sdkman/candidates/java/21.0.3-tem
```

**Why Temurin, not Oracle JDK?**  
Oracle JDK requires a commercial license for production use since Java 17. Eclipse Temurin (from the Adoptium project) is OpenJDK built by the Eclipse Foundation with no license restrictions. Amazon Corretto, Microsoft Build of OpenJDK, and Azul Zulu are other license-free alternatives — all functionally equivalent for your purposes.

**Installing multiple versions (you will need this):**

```bash
# Install Java 17 LTS for legacy project compatibility:
sdk install java 17.0.11-tem

# Switch temporarily:
sdk use java 17.0.11-tem

# Switch back:
sdk use java 21.0.3-tem

# Check current:
sdk current java
```

### Installing Maven via SDKMAN

```bash
sdk install maven 3.9.6

# Verify:
mvn -version
# Apache Maven 3.9.6 (bc0240f3c744dd6b6ec2920b3cd08dcc295161ae)
# Maven home: /Users/surya/.sdkman/candidates/maven/3.9.6
# Java version: 21.0.3, vendor: Eclipse Adoptium
```

**Understand what Maven is:** Maven is a build tool and dependency manager. Its primary jobs:
1. Download your project's dependencies (JARs from Maven Central) and cache them in `~/.m2/repository`
2. Compile your code
3. Run tests
4. Package your code into a JAR
5. Provide lifecycle hooks for plugins (Spring Boot Maven plugin, Surefire for tests, Jacoco for coverage)

### Installing IntelliJ IDEA Community Edition

1. Go to [jetbrains.com/idea/download](https://www.jetbrains.com/idea/download/)
2. Select **Community Edition** (free, not Ultimate)
3. Download for your OS (macOS `.dmg`, Windows `.exe`, Linux `.tar.gz`)
4. Install normally

**First-launch configuration:**

```
On first run:
1. Select "Do not import settings" (fresh install)
2. Choose color theme: Darcula (dark) or IntelliJ Light
3. Click "Start using IntelliJ IDEA"

Configure these settings immediately (⌘ Comma / Ctrl+Alt+S):

Editor → General → Auto Import:
  ✓ Add unambiguous imports on the fly
  ✓ Optimize imports on the fly

Editor → Code Style → Java:
  - Scheme: Default
  - Tab size: 4 (Java convention)
  - Continuation indent: 8

Editor → General → Editor Tabs:
  - Tab placement: None (show no tabs — use Cmd+E for recent files instead)

Build, Execution, Deployment → Build Tools → Maven:
  - Maven home path: (point to your SDKMAN Maven location)
  - JDK for importer: 21 (your installed JDK)

Appearance → System Settings:
  - Font: JetBrains Mono (download from jetbrains.com/lp/mono if not installed)
  - Font size: 14
```

**Recommended plugins to install (Settings → Plugins):**

| Plugin | Why |
|--------|-----|
| Lombok | Support for `@Data`, `@Builder` etc. (you will use these constantly) |
| SonarLint | Real-time code quality and security warnings |
| GitToolBox | Shows git blame inline, branch info in status bar |
| Rainbow Brackets | Different colors for nested brackets — saves your sanity |
| CheckStyle-IDEA | Enforce code style (if your team uses Checkstyle) |
| PlantUML integration | Render UML diagrams in the IDE |
| HTTP Client | Built-in REST client (alternative to Postman for quick tests) |

### Installing Docker Desktop

1. Download from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
2. Install for your OS
3. Start Docker Desktop (it runs in the background)

```bash
# Verify:
docker --version
# Docker version 26.x.x

docker-compose --version
# Docker Compose version 2.x.x

# Quick test:
docker run hello-world
# Pulls the hello-world image and prints a message
```

**What Docker Desktop is doing:** It runs a lightweight Linux VM (using HyperKit on macOS, Hyper-V on Windows) that hosts the Docker daemon. When you run `docker run postgres`, it downloads the PostgreSQL image into the VM and starts a container inside that VM. The `-p 5432:5432` flag makes the container's port accessible on your host machine.

**Why use Docker instead of native installs?** 
- Clean: each project gets its own database, no conflicts
- Reproducible: everyone on the team has the same versions
- Disposable: `docker rm` removes it completely, nothing left on your system
- Consistent: exactly what runs in production (same PostgreSQL version, same Kafka version)

**Docker Compose file for local development (save as `docker-compose.yml`):**

```yaml
version: '3.8'

services:
  # PostgreSQL 16
  postgres:
    image: postgres:16-alpine
    container_name: dev-postgres
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis 7
  redis:
    image: redis:7-alpine
    container_name: dev-redis
    ports:
      - "6379:6379"
    command: redis-server --requirepass devpassword

  # Apache Kafka (with embedded Zookeeper via KRaft mode)
  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: dev-kafka
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CLUSTER_ID: MkU3OEVBNTcwNTJENDM2Qk
    ports:
      - "9092:9092"

volumes:
  postgres_data:
```

Start everything with `docker-compose up -d`. Stop with `docker-compose down`.

### Installing Git

```bash
# macOS (via Homebrew):
brew install git

# Ubuntu/Debian:
sudo apt update && sudo apt install git

# Verify:
git --version
# git version 2.45.x
```

**First-time Git configuration (required before first commit):**

```bash
git config --global user.name "Surya"
git config --global user.email "surya@example.com"
git config --global core.editor "vim"  # or "nano" or "code --wait" for VS Code
git config --global init.defaultBranch main
git config --global pull.rebase true   # rebase instead of merge on pull
git config --global push.autoSetupRemote true  # auto-set upstream on first push

# Verify:
git config --list
```

---

## 6.2 Maven — Understanding the Build System

### The Standard Maven Project Structure

Every Java project you create or encounter follows this exact layout:

```
order-service/                          ← project root
├── pom.xml                             ← Project Object Model: the build definition
├── .gitignore                          ← files Git should not track
├── README.md
└── src/
    ├── main/
    │   ├── java/
    │   │   └── com/
    │   │       └── surya/
    │   │           └── orderservice/
    │   │               ├── OrderServiceApplication.java   ← main class
    │   │               ├── controller/
    │   │               │   └── OrderController.java
    │   │               ├── service/
    │   │               │   └── OrderService.java
    │   │               ├── repository/
    │   │               │   └── OrderRepository.java
    │   │               ├── model/
    │   │               │   └── Order.java
    │   │               └── config/
    │   │                   └── SecurityConfig.java
    │   └── resources/
    │       ├── application.yml          ← Spring Boot configuration
    │       ├── application-dev.yml      ← dev environment overrides
    │       ├── application-prod.yml     ← production overrides
    │       └── db/
    │           └── migration/
    │               ├── V1__create_orders_table.sql    ← Flyway migration
    │               └── V2__add_order_status_index.sql
    └── test/
        ├── java/
        │   └── com/
        │       └── surya/
        │           └── orderservice/
        │               ├── controller/
        │               │   └── OrderControllerTest.java
        │               ├── service/
        │               │   └── OrderServiceTest.java
        │               └── integration/
        │                   └── OrderIntegrationTest.java
        └── resources/
            ├── application-test.yml     ← test-specific config
            └── test-data.sql            ← test fixture data
```

This structure is **not optional** — Maven enforces it. Source code must be under `src/main/java`. Test code under `src/test/java`. Resources (YAML, SQL, etc.) under `src/main/resources` and `src/test/resources`. Deviation requires explicit Maven configuration.

### pom.xml Anatomy — Every Element Explained

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <!-- POM file format version. Always 4.0.0. -->
    <modelVersion>4.0.0</modelVersion>

    <!-- Parent POM: inherit Spring Boot's dependency management and plugin config -->
    <!-- This is how Spring Boot manages all dependency versions consistently -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.3.0</version>
        <relativePath/> <!-- look in Maven Central, not local filesystem -->
    </parent>

    <!-- Your project's unique identity: groupId:artifactId:version (GAV coordinates) -->
    <groupId>com.surya</groupId>          <!-- usually your reverse domain name -->
    <artifactId>order-service</artifactId> <!-- your project name, used in JAR filename -->
    <version>1.0.0-SNAPSHOT</version>      <!-- SNAPSHOT = in-development, not released -->
    <name>Order Service</name>
    <description>Order Management Microservice</description>

    <!-- Java version properties -->
    <properties>
        <java.version>21</java.version>  <!-- tells Maven compiler to use Java 21 -->
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!-- Dependencies: libraries your code needs to compile and run -->
    <dependencies>

        <!-- Spring Web MVC + embedded Tomcat: makes your app an HTTP server -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <!-- No <version> here! Inherited from spring-boot-starter-parent -->
        </dependency>

        <!-- Spring Data JPA + Hibernate: database access via JPA -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- PostgreSQL JDBC driver: connect to PostgreSQL -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>  <!-- only needed at runtime, not compile time -->
        </dependency>

        <!-- Spring Security: authentication and authorization -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>

        <!-- JWT library for token parsing and validation -->
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-api</artifactId>
            <version>0.12.5</version>  <!-- version explicitly specified: not managed by Spring -->
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-impl</artifactId>
            <version>0.12.5</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>io.jsonwebtoken</groupId>
            <artifactId>jjwt-jackson</artifactId>
            <version>0.12.5</version>
            <scope>runtime</scope>
        </dependency>

        <!-- Spring Kafka: produce and consume Kafka messages -->
        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
        </dependency>

        <!-- Spring Data Redis: Redis client (uses Lettuce under the hood) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>

        <!-- Flyway: database migration management -->
        <dependency>
            <groupId>org.flywaydb</groupId>
            <artifactId>flyway-core</artifactId>
        </dependency>

        <!-- Actuator: exposes /actuator/health, /actuator/metrics etc. -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- Lombok: reduces boilerplate (@Data, @Builder, @Slf4j, etc.) -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>  <!-- not propagated to dependents -->
        </dependency>

        <!-- Validation API: @NotNull, @NotBlank, @Size etc. on request DTOs -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- ========= TEST SCOPE DEPENDENCIES =========== -->
        <!-- Only available during test compilation and execution, not in the final JAR -->

        <!-- Spring Boot test utilities: @SpringBootTest, MockMvc, etc. -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <!-- Spring Security test helpers: @WithMockUser etc. -->
        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>

        <!-- Testcontainers: spin up real PostgreSQL/Kafka containers in tests -->
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>kafka</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-testcontainers</artifactId>
            <scope>test</scope>
        </dependency>

    </dependencies>

    <!-- Build configuration: how to compile, test, and package -->
    <build>
        <plugins>
            <!-- Spring Boot plugin: creates the executable fat JAR -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <!-- Exclude Lombok from the final JAR (it's compile-only) -->
                    <excludes>
                        <exclude>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                        </exclude>
                    </excludes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### The Maven Build Lifecycle

Maven builds proceed through **phases** in a fixed order. Running a phase runs all preceding phases:

```
clean  →  validate  →  compile  →  test  →  package  →  verify  →  install  →  deploy

clean:     Delete target/ directory (remove previous build artifacts)
validate:  Check pom.xml is valid and all required information is present
compile:   Compile src/main/java → target/classes/
test:      Compile src/test/java, run tests via JUnit + Surefire plugin
           (Tests FAIL → build FAILS)
package:   Create JAR/WAR in target/ (e.g., target/order-service-1.0.0-SNAPSHOT.jar)
verify:    Run integration tests, code coverage checks (Jacoco)
install:   Copy JAR to local Maven repository (~/.m2/repository/)
           (makes it available as a dependency to other LOCAL Maven projects)
deploy:    Upload JAR to a remote repository (Artifactory, Nexus, GitHub Packages)
```

**Commands you will use daily:**

```bash
# Compile and package (skip tests for speed during development):
mvn clean package -DskipTests

# Run tests only:
mvn test

# Run a specific test class:
mvn test -Dtest=OrderServiceTest

# Run a specific test method:
mvn test -Dtest=OrderServiceTest#shouldCreateOrderSuccessfully

# Run the app (uses Spring Boot Maven plugin):
mvn spring-boot:run

# Run with a specific profile:
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# Full clean build including tests and coverage:
mvn clean verify

# Show dependency tree (diagnose version conflicts):
mvn dependency:tree

# Show effective pom.xml (after parent inheritance):
mvn help:effective-pom

# Update dependencies to latest versions (be careful with this):
mvn versions:display-dependency-updates
```

### Finding Dependencies — Maven Central

All public Java libraries are hosted on Maven Central ([search.maven.org](https://search.maven.org)).

**How to add a dependency:**
1. Go to [search.maven.org](https://search.maven.org)
2. Search for the library (e.g., "resilience4j")
3. Click the version you want
4. Copy the Maven XML snippet
5. Paste into your pom.xml `<dependencies>` section

**Example — adding Resilience4j:**
```xml
<!-- search.maven.org → resilience4j-spring-boot3 → copy XML -->
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-spring-boot3</artifactId>
    <version>2.2.0</version>
</dependency>
```

**Dependency scopes:**

| Scope | Available at compile time? | In final JAR? | Use case |
|-------|---------------------------|---------------|---------|
| (none/compile) | Yes | Yes | Default. Regular dependencies. |
| runtime | No | Yes | JDBC drivers, Lombok implementations |
| test | Yes (test only) | No | JUnit, Mockito, Testcontainers |
| provided | Yes | No | Servlet API (container provides it) |
| optional | Yes | No | Lombok (annotation processor only) |

---

## 6.3 Git at Senior Engineer Level

### Git's Internal Model — What a Commit Actually Is

Understanding Git's internals prevents you from being afraid of it. Git stores four types of objects, all content-addressed (named by SHA-1 hash of their contents):

```
Git Object Types:

BLOB:    File content (no filename, just bytes)
         SHA: a3f2b1... → "public class Order { ... }"

TREE:    A directory — maps filenames to blob/tree SHA hashes
         SHA: c8d4e2... → {
           "OrderService.java" → blob(a3f2b1...),
           "controller/"      → tree(d5f9c1...)
         }

COMMIT:  A snapshot — points to a tree (root directory snapshot)
         SHA: 7f1a3c... → {
           tree:    c8d4e2...  (the root tree)
           parent:  6b2d4f...  (previous commit SHA)
           author:  Surya <surya@email.com>
           date:    2024-03-15 14:32:01 +0530
           message: "feat: add order validation with @Validated"
         }

TAG:     A named pointer to a commit (for releases: v1.0.0)
```

A **branch** is just a file containing a commit SHA. `main` is a file with the SHA of the latest commit on main. When you commit, Git creates a commit object and updates the branch file to point to the new commit.

```
Git history as a linked list of commits:

    A ← B ← C ← D (main)
                  ↑
                  └── HEAD (what you currently have checked out)

    A ← B ← E ← F (feature/order-events)
              ↑
              shared history with main
```

### The Three States and Staging

Git has three places your changes can be:

```
Working Directory         Staging Area (Index)         Repository (.git/)
     │                          │                            │
     │  (files on disk)         │  (changes ready           │  (committed
     │                          │   to commit)              │   history)
     │                          │                            │
     │ ── git add ──────────────►                           │
     │                          │ ── git commit ────────────►
     │ ◄── git checkout ────────────────────────────────────│
     │ ◄── git restore --staged │ (unstage without losing work)
     │
     │ git status: shows what is in each area
     │ git diff:   shows unstaged changes (Working Dir vs Staging)
     │ git diff --staged: shows staged changes (Staging vs last commit)
```

**Why staging exists:** It lets you craft precise, logical commits even when you have changed many files. `git add -p` (patch staging) lets you stage specific *hunks* within a file, leaving other changes unstaged for a separate commit.

### The Complete Git Workflow

```bash
# Start work on a new feature:
git checkout main
git pull                                    # get latest main
git checkout -b feature/add-order-search   # create and switch to new branch

# Make changes, then stage precisely:
git add -p                                 # interactively stage hunks (recommended)
git add src/main/java/OrderService.java    # or stage a whole file

# Review what you are about to commit:
git diff --staged                          # see the exact diff going into the commit
git status                                 # see which files are staged/unstaged

# Commit with a meaningful message (Conventional Commits format):
git commit -m "feat(order): add full-text search by customer name and product

Adds OrderSearchService with JPA Specification-based dynamic queries.
Supports filtering by customerId, status, and date range.
Adds GET /api/v1/orders/search endpoint with pagination.

Closes #142"

# Push to remote (first push sets upstream):
git push -u origin feature/add-order-search

# Go to GitHub and open a Pull Request

# After PR is approved and merged, clean up:
git checkout main
git pull
git branch -d feature/add-order-search
```

---

#### `git push --force-with-lease` — The Safe Force Push

When you rewrite history on a branch (via interactive rebase or commit amending),
the branch diverges from the remote — you cannot do a normal push. You must
force-push. But `git push --force` is dangerous because it blindly overwrites
the remote regardless of what is there. If a teammate pushed commits after
your last fetch, `--force` silently destroys their work.

`git push --force-with-lease` solves this. It checks that the remote branch
is exactly at the commit you last fetched before pushing. If anyone pushed
since your last fetch, the push is rejected with a clear error.

```bash
# NEVER use --force on any branch (destroys teammates' commits silently):
git push --force origin feature/payment-refactor

# ALWAYS use --force-with-lease when force-pushing is necessary:
git push --force-with-lease origin feature/payment-refactor

# The error message you see when someone else pushed since your fetch:
# error: failed to push some refs to 'github.com:username/repo.git'
# hint: Updates were rejected because the tip of your current branch
#       is behind the remote. Fetch the remote changes and rebase.

# Safe workflow before force-with-lease:
git fetch origin feature/payment-refactor   # check what's on remote first
git log origin/feature/payment-refactor     # see if anyone pushed
git push --force-with-lease                 # safe: only pushes if remote unchanged
```

**When force-with-lease is acceptable:**
- After interactive rebase on your own feature branch (no one else works on it)
- After amending the last commit on a branch only you use
- After squashing commits before opening a PR

**When force-with-lease is never acceptable:**
- On `main`, `develop`, or any shared team branch
- After another person has pushed commits to the branch
- After a CI system has added commits (e.g., auto-formatting bots)

**Why this matters for your portfolio repositories:**
Every one of your six portfolio repositories uses `main` as the default branch.
Set a rule for yourself: `--force` is banned; `--force-with-lease` only on
feature branches after a clean `git fetch` confirms you are the only author.

**Interview answer:** "I never use `git push --force`. I use
`git push --force-with-lease` which only succeeds if the remote tip matches
what I last fetched — protecting against silently overwriting a teammate's
work. I only use it on my own feature branches after an interactive rebase,
never on shared branches."

---

### Conventional Commits — Writing Meaningful Commit Messages

Conventional Commits is a specification for structured commit messages that enables:
- Automatic changelog generation
- Semantic versioning
- Clear communication about the type and scope of change

**Format:** `<type>(<scope>): <short description>`

```
feat(order): add Kafka event publishing on order creation
fix(auth): prevent JWT reuse after user password change
docs(api): add OpenAPI annotations to all OrderController endpoints
chore(deps): upgrade Spring Boot from 3.2.5 to 3.3.0
refactor(service): extract order validation into OrderValidator
test(integration): add Testcontainers integration tests for OrderRepository
style: apply Google Java Style formatting to order package
perf(cache): add Redis caching to product catalog lookups
ci: add Jacoco coverage gate (minimum 80% line coverage)
```

| Type | When to use |
|------|-------------|
| `feat` | A new feature visible to users or API consumers |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `chore` | Build process, dependency updates, tooling |
| `refactor` | Code restructuring with no behavior change |
| `test` | Adding or modifying tests |
| `perf` | Performance improvement |
| `style` | Formatting, whitespace — no logic change |
| `ci` | CI/CD configuration |
| `revert` | Reverting a previous commit |

### Interactive Staging — The Essential Skill

`git add -p` (patch mode) is the most important Git command for writing clean commits:

```bash
git add -p

# Git shows each changed "hunk" (contiguous block of changes) one at a time:
diff --git a/src/main/java/OrderService.java b/src/main/java/OrderService.java
@@ -45,6 +45,12 @@ public class OrderService {
     }
 
+    public List<Order> searchOrders(OrderSearchCriteria criteria) {
+        return orderRepository.findAll(
+            OrderSpecification.build(criteria), criteria.getPageable()
+        );
+    }
+
     @Transactional
     public Order cancelOrder(String orderId) {

Stage this hunk [y,n,q,a,d,s,?]?

# Options:
# y = yes, stage this hunk
# n = no, skip this hunk
# s = split into smaller hunks
# e = manually edit this hunk
# q = quit (stage what you have so far)
# ? = help
```

This lets you commit the `searchOrders` method separately from the `cancelOrder` change — clean, logical commits even when you changed many things at once.

### The Complete Undo Toolkit

Never fear Git once you understand undo:

```bash
# ─── UNDO UNCOMMITTED CHANGES ───────────────────────────────────────────────

# Discard all unstaged changes in a file (DANGEROUS: cannot be recovered):
git restore OrderService.java

# Unstage a file (move back to Working Directory, keep changes):
git restore --staged OrderService.java

# Discard ALL unstaged changes everywhere (DANGEROUS):
git restore .


# ─── UNDO THE LAST COMMIT (keep changes in Working Directory) ───────────────

# "Undo commit, keep changes unstaged":
git reset HEAD~1

# "Undo commit, keep changes staged":
git reset --soft HEAD~1

# "Undo commit AND discard all changes" (DANGEROUS — data loss):
git reset --hard HEAD~1


# ─── UNDO A PUSHED COMMIT (safe way) ─────────────────────────────────────────

# Creates a NEW commit that reverses the changes (history preserved):
git revert abc1234          # revert a specific commit by SHA
git revert HEAD             # revert the latest commit


# ─── FIX THE LAST COMMIT WITHOUT CREATING A NEW ONE ───────────────────────

# Amend the commit message:
git commit --amend -m "feat(order): improved message"

# Add forgotten file to last commit:
git add forgotten-file.java
git commit --amend --no-edit  # amend but keep existing message


# ─── RESCUE LOST WORK ──────────────────────────────────────────────────────

# If you reset --hard and want changes back:
git reflog                    # shows all recent HEAD movements
# Output: abc1234 HEAD@{1}: commit: the commit you lost
git checkout abc1234          # go back to it
# or:
git reset --hard abc1234      # restore to that state

# Stash work in progress when you need to switch branches:
git stash                     # save current changes to stash
git checkout main             # do urgent hotfix
git stash pop                 # restore your in-progress work
```

### Rebase — Keeping History Clean

**Merge** creates a merge commit that shows the parallel development:
```
    A ← B ← C ← D (main)
              ↑
    A ← B ← E ← F (feature)
              ↕ (merge point)
    A ← B ← C ← D ← M (merge commit) (main after merge)
                      ↑↗
                      F
```

**Rebase** rewrites your branch's commits *on top of* the current main, as if you had started from the latest main:
```
    A ← B ← C ← D (main)
    A ← B ← E ← F (feature, original)
    
    After: git rebase main (from feature branch)
    A ← B ← C ← D (main)
                  ↖
                   E' ← F' (feature, rebased — commits reapplied on top of D)
```

Rebased history is linear and cleaner. Use **interactive rebase** to clean up commits before a PR:

```bash
# Rewrite the last 3 commits interactively:
git rebase -i HEAD~3

# Editor opens with:
pick 7f1a3c feat: add order search
pick 8d2b4e fix typo in OrderService
pick 9c3d5f add missing test

# Change to:
pick 7f1a3c feat: add order search
squash 8d2b4e fix typo in OrderService    ← squash into previous commit
reword 9c3d5f add missing test            ← keep but edit the message

# Git combines the two commits and prompts for a new message
```

---

#### Branch Protection Rules — Engineering Process at the Repository Level

Branch protection rules prevent direct pushes to important branches and enforce
quality gates before code can be merged. They are a signal of engineering
process maturity — when a hiring manager views your GitHub profile, enabled
branch protection rules communicate that you work like a professional team,
not a solo developer pushing raw commits to main.

**Setting up branch protection:**
Navigate to: Repository → Settings → Branches → Branch protection rules → Add rule

**Recommended configuration for all portfolio repositories:**

```
Branch name pattern: main

PULL REQUEST SETTINGS:
☑ Require a pull request before merging
   ☑ Required number of approvals: 1
   ☑ Dismiss stale PR approvals when new commits are pushed
   ☑ Require review from code owners (optional for solo repos)

STATUS CHECK SETTINGS:
☑ Require status checks to pass before merging
   ☑ Require branches to be up to date before merging
   Required status checks:
     ci/test                    ← your GitHub Actions job name
     ci/build                   ← your Docker build job name

CONVERSATION SETTINGS:
☑ Require conversation resolution before merging

PUSH SETTINGS:
☑ Restrict who can push to matching branches
   ☑ Do not allow bypassing the above settings (applies to admins too)
   ☐ Allow force pushes (leave unchecked — always)
   ☐ Allow deletions (leave unchecked)
```

**What each setting protects against:**

| Setting | What breaks without it |
|---------|----------------------|
| Require PR before merging | Direct push to main — skips all code review |
| Require CI to pass | Broken code can be merged (tests fail silently) |
| Dismiss stale approvals | Approve PR, then push breaking change — approval stays |
| Resolve conversations | Review comments ignored — issues never addressed |
| No force pushes | History can be rewritten, losing accountability |

**Solo repository exception:**
For `dsa-java` and `java-fundamentals`, where you are the sole contributor,
a lighter configuration is acceptable:
```
☑ Require status checks (CI must pass — still enforces test quality)
☐ Require PR (solo repo — branch from main, push directly is acceptable)
☑ Do not allow force pushes (protect history)
```

**Adding protection via GitHub CLI:**
```bash
# Install GitHub CLI: brew install gh
gh auth login

# Set branch protection on your repository:
gh api repos/USERNAME/REPO/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci/test"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null
```

**Interview answer:** "All our shared branches have branch protection enabled.
CI must pass, at least one reviewer must approve, and stale approvals are
dismissed when new commits are pushed. This means broken code cannot be merged
by accident, and every line of code on main has been reviewed. For my personal
portfolio repositories, I enforce at minimum the CI gate — nothing that fails
tests gets merged to main."

---

### Resolving Merge Conflicts

A conflict occurs when two branches changed the same lines of a file:

```
<<<<<<< HEAD (your current branch: main)
    public Order createOrder(CreateOrderRequest request) {
        validateRequest(request);
        Order order = orderMapper.toEntity(request);
=======
    public Order createOrder(CreateOrderRequest request, String requestId) {
        validateRequest(request);
        checkIdempotency(requestId);
        Order order = orderMapper.toEntity(request, requestId);
>>>>>>> feature/idempotency
```

**Resolving in IntelliJ:**
1. Open the conflicted file
2. Click "Resolve conflicts" in the notification
3. IntelliJ shows a three-panel view: your version | result | incoming version
4. Click the arrow buttons to accept changes from either side
5. Edit the result panel manually if neither side is exactly right
6. Click "Apply"
7. `git add` the resolved file, then `git commit`

**Resolving in terminal:**
```bash
# Edit the file to remove the conflict markers and choose the correct code:
vim OrderService.java
# Delete <<<<<<, =======, >>>>>>> markers
# Keep the correct code (or combine both)

git add OrderService.java
git commit    # Git creates a merge commit automatically
```

### .gitignore for Java/Spring Boot

Create this as `.gitignore` in your project root:

```gitignore
# ─── Compiled output ───────────────────────────────────────────────────────
target/                     # Maven build output (contains .class files, JARs)
*.class                     # compiled Java bytecode

# ─── IDE files (not project configuration) ─────────────────────────────────
.idea/                      # IntelliJ workspace files
*.iml                       # IntelliJ module file (auto-generated)
.eclipse/                   # Eclipse workspace
.settings/                  # Eclipse project settings
.classpath                  # Eclipse classpath
.project                    # Eclipse project
*.swp                       # Vim swap files
.DS_Store                   # macOS Finder metadata (useless to others)

# ─── Spring Boot / Java ────────────────────────────────────────────────────
*.jar                       # JAR files (built artifacts, not source)
*.war                       # WAR files
*.ear                       # EAR files
spring.log                  # Spring Boot default log file

# ─── Environment and secrets (NEVER commit these) ──────────────────────────
.env                        # Local environment variables
.env.local
application-local.yml       # local-only Spring config with real passwords
application-secrets.yml
*.p12                       # PKCS12 keystore files (contain private keys)
*.jks                       # Java KeyStore files

# ─── Docker ────────────────────────────────────────────────────────────────
docker-volumes/             # local Docker volume data

# ─── Logs ──────────────────────────────────────────────────────────────────
logs/
*.log
*.log.*

# ─── Maven ─────────────────────────────────────────────────────────────────
.mvn/wrapper/maven-wrapper.jar   # Maven wrapper JAR (large binary, auto-downloaded)
# Note: keep .mvn/wrapper/maven-wrapper.properties (just a config file, small)

# ─── OS files ──────────────────────────────────────────────────────────────
Thumbs.db                   # Windows thumbnail cache
```

---

## 6.4 IntelliJ IDEA Productivity

### Essential Keyboard Shortcuts

Mastering these shortcuts will make you 3–5× faster in the IDE. Learn 5 per week until they are muscle memory.

**Navigation (the most important category):**

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Go to any file (by name) | Cmd+Shift+O | Ctrl+Shift+N |
| Go to any class | Cmd+O | Ctrl+N |
| Go to any symbol (method/field) | Cmd+Alt+O | Ctrl+Shift+Alt+N |
| Find anything (double Shift) | Shift Shift | Shift Shift |
| Go to declaration (jump to definition) | Cmd+B | Ctrl+B |
| Go back / Go forward | Cmd+[ / Cmd+] | Ctrl+Alt+Left/Right |
| Recent files | Cmd+E | Ctrl+E |
| Recent locations | Cmd+Shift+E | Ctrl+Shift+E |
| Go to line number | Cmd+L | Ctrl+G |
| Jump to last edited location | Cmd+Shift+Backspace | Ctrl+Shift+Backspace |

**Code generation:**

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Generate (constructor, getters, etc.) | Cmd+N | Alt+Insert |
| Override/implement methods | Ctrl+O | Ctrl+O |
| Smart code completion | Ctrl+Shift+Space | Ctrl+Shift+Space |
| Basic completion | Ctrl+Space | Ctrl+Space |
| Show intention actions (quick fixes) | Alt+Enter | Alt+Enter |
| Surround with (try-catch, if, etc.) | Cmd+Alt+T | Ctrl+Alt+T |

**Refactoring:**

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Rename (file/class/method/variable) | Shift+F6 | Shift+F6 |
| Extract method | Cmd+Alt+M | Ctrl+Alt+M |
| Extract variable | Cmd+Alt+V | Ctrl+Alt+V |
| Extract constant | Cmd+Alt+C | Ctrl+Alt+C |
| Extract field | Cmd+Alt+F | Ctrl+Alt+F |
| Extract interface | | Refactor → Extract → Interface |
| Move class to different package | F6 | F6 |
| Safe delete (check usages first) | Cmd+Delete | Alt+Delete |

**Search and analysis:**

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Find usages of symbol | Alt+F7 | Alt+F7 |
| Find in path (search all files) | Cmd+Shift+F | Ctrl+Shift+F |
| Replace in path | Cmd+Shift+R | Ctrl+Shift+R |
| Highlight all usages in file | Cmd+Shift+F7 | Ctrl+Shift+F7 |
| Show all implementations | Cmd+Alt+B | Ctrl+Alt+B |
| Show call hierarchy | Ctrl+Alt+H | Ctrl+Alt+H |

**Running and debugging:**

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Run current file/config | Ctrl+R | Shift+F10 |
| Debug current file/config | Ctrl+D | Shift+F9 |
| Run tests in class/method | Ctrl+Shift+R | Ctrl+Shift+F10 |
| Toggle breakpoint | Cmd+F8 | Ctrl+F8 |
| Step over (next line) | F8 | F8 |
| Step into (enter method) | F7 | F7 |
| Step out (return from method) | Shift+F8 | Shift+F8 |
| Resume until next breakpoint | F9 | F9 |
| Evaluate expression | Alt+F8 | Alt+F8 |

**Code editing:**

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Delete line | Cmd+Delete | Ctrl+Y |
| Duplicate line/selection | Cmd+D | Ctrl+D |
| Move line up/down | Shift+Alt+Up/Down | Shift+Alt+Up/Down |
| Format code | Cmd+Alt+L | Ctrl+Alt+L |
| Optimize imports | Ctrl+Alt+O | Ctrl+Alt+O |
| Comment/uncomment line | Cmd+/ | Ctrl+/ |
| Expand/collapse code block | Cmd++/- | Ctrl++/- |

### Debugging — Step by Step

Setting a breakpoint and debugging is one of the most powerful skills in your toolkit.

**Setting a conditional breakpoint:**
```java
// You want to pause ONLY when orderId equals "order-123":
public void processOrder(String orderId, Order order) {
    // Right-click the breakpoint dot → Add condition:
    // Condition: orderId.equals("order-123")
    validateOrder(order);  // ← breakpoint here
}
```

**Debugging a Spring Boot app:**
1. Click the green debug icon (bug icon) next to your `main()` method
2. Spring Boot starts in debug mode
3. When code hits your breakpoint, execution pauses
4. The Debug panel shows: current variable values in the current scope, the call stack
5. Use step-over (F8) to go to the next line
6. Use step-into (F7) to enter a method call
7. Use "Evaluate Expression" (Alt+F8) to run any Java expression in the current context

```
Debug panel shows:
Frames:                          Variables:
  ▶ processOrder:85              ▸ this = OrderService@1a2b3c
    createOrder:42               ▸ orderId = "order-123"
    OrderController.post:31      ▸ order = Order{id=null, items=[...]}
    ...                          ▸ currentUser = User{id="user-456"}
                                 ▸ order.total = 149.99
```

---

## 6.5 Reading Java Stack Traces

### The Anatomy of a Stack Trace

When a Java exception is thrown and not caught, the JVM prints the stack trace to stderr. Reading it correctly is a critical daily skill.

```
Exception in thread "http-nio-8080-exec-1" org.springframework.web.util.NestedServletException: Request processing failed; nested exception is java.lang.NullPointerException: Cannot invoke "com.surya.model.Order.getCustomerId()" because "order" is null
    at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1022)
    at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:925)
    at javax.servlet.http.HttpServlet.service(HttpServlet.java:681)
    at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)
    ...
    at java.lang.Thread.run(Thread.java:833)
Caused by: java.lang.NullPointerException: Cannot invoke "com.surya.model.Order.getCustomerId()" because "order" is null
    at com.surya.orderservice.service.OrderService.validateOrder(OrderService.java:78)
    at com.surya.orderservice.service.OrderService.createOrder(OrderService.java:45)
    at com.surya.orderservice.controller.OrderController.createOrder(OrderController.java:32)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
```

**Reading rules:**

1. **Read the last "Caused by:" first** — that is the root cause. Everything above it is the propagation chain. In this case: `NullPointerException: Cannot invoke "...Order.getCustomerId()" because "order" is null`

2. **Find your code in the stack trace** — look for `com.surya` lines. Framework lines (Spring, Tomcat, JDK) are noise. The root cause is in *your* code: `OrderService.java:78`

3. **The stack reads from innermost (top) to outermost (bottom)** — method at the top threw the exception, it propagated up through the methods below. Call order: `OrderController.createOrder()` called `OrderService.createOrder()` called `OrderService.validateOrder()` where the NPE occurred.

### The Most Common Exceptions and What They Mean

**`NullPointerException`**  
A method was called on a null reference, or a null value was used where a non-null was required.  
*What to look for:* The JVM's message now tells you exactly what was null (Java 17+): "because 'order' is null". Check why `order` is null at the point of the failing method call.

**`ClassCastException`**  
A value was cast to a type it is not actually an instance of.  
*Common cause:* Incorrect deserialization, generic type erasure, two ClassLoaders loaded the same class.

**`ArrayIndexOutOfBoundsException`**  
Array access with an index ≥ array length or < 0.  
*What to look for:* Off-by-one in loop bounds, or array is shorter than expected.

**`StackOverflowError`**  
Stack is exhausted, usually from infinite recursion.  
*What to look for:* A method that calls itself with no base case, or a circular call chain between two methods.

**`OutOfMemoryError: Java heap space`**  
JVM heap is full. GC could not free enough space.  
*What to look for:* Memory leak (objects accumulating in a long-lived collection), cache growing unbounded, bulk data processing without streaming.

**`OutOfMemoryError: Metaspace`**  
Class metadata area is full (usually from loading too many classes, often in frameworks that generate classes at runtime like CGLIB for Spring proxies).

**`LazyInitializationException`** (Hibernate-specific)  
A lazy-loaded relationship was accessed after the Hibernate session was closed.  
*What to look for:* Accessing `order.getItems()` outside of a `@Transactional` method after the session was closed. Fix: add `@Transactional`, use `JOIN FETCH` in the query, or use a DTO projection.

**`DataIntegrityViolationException`**  
A database constraint was violated (unique key, foreign key, not-null constraint).  
*What to look for:* The nested cause (look in `Caused by:`) will contain the SQL constraint name. Map it to a 409 Conflict response in your `@ExceptionHandler`.

### Reading a Complete Spring Boot Stack Trace

Here is a realistic 40-line Spring Boot trace with full annotation:

```
2024-03-15 14:32:01.234 ERROR 12345 --- [nio-8080-exec-3] o.a.c.c.C.[.[.[/].[dispatcherServlet]: 
Servlet.service() for servlet [dispatcherServlet] in context with path [] 
threw exception [Request processing failed: 
  com.surya.exception.OrderNotFoundException: Order not found with id: order-999
]

com.surya.exception.OrderNotFoundException: Order not found with id: order-999
    at com.surya.orderservice.service.OrderService.getOrder(OrderService.java:63)
    ↑ ROOT CAUSE: your code, line 63 of OrderService
    
    at com.surya.orderservice.controller.OrderController.getOrderById(OrderController.java:47)
    ↑ Your controller called the service
    
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:498)
    ↑ Spring uses reflection to call your controller method (skip these)
    
    at org.springframework.web.method.support.InvocableHandlerMethod.doInvoke(InvocableHandlerMethod.java:260)
    at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:190)
    at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(...)
    ↑ Spring MVC framework calling your handler (skip these)
    
    at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(...)
    at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(...)
    at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1089)
    at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:979)
    ↑ Spring DispatcherServlet routing logic (skip these)
    
    at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:166)
    at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:142)
    ↑ Tomcat filter chain and request processing (skip these)
    
    at java.lang.Thread.run(Thread.java:833)
    ↑ The thread that was running when the exception occurred

KEY FINDING: OrderService.java line 63 threw OrderNotFoundException.
ACTION: Check if your repository.findById() is returning Optional.empty()
        and whether your orElseThrow() message matches the actual order ID.
```

**The pattern:** ignore framework lines, find your package (`com.surya`), read the root cause message, jump to the file:line indicated.

---

## 6.6 Terminal Productivity

### Shell Configuration (~/.zshrc or ~/.bashrc)

Add these to your shell configuration file for a productive terminal environment:

```bash
# ─── SDKMAN (add to end of .zshrc, as SDKMAN instructs) ───────────────────
export SDKMAN_DIR="$HOME/.sdkman"
[[ -s "$HOME/.sdkman/bin/sdkman-init.sh" ]] && \
  source "$HOME/.sdkman/bin/sdkman-init.sh"

# ─── PATH additions ──────────────────────────────────────────────────────────
export PATH="$HOME/bin:$PATH"                     # personal scripts
export JAVA_HOME="$HOME/.sdkman/candidates/java/current"

# ─── Backend engineering aliases ─────────────────────────────────────────────

# Maven shortcuts
alias mci='mvn clean install -DskipTests'         # fast build
alias mcp='mvn clean package -DskipTests'         # package only
alias mt='mvn test'                                # run tests
alias mrun='mvn spring-boot:run'                  # run app
alias mrundev='mvn spring-boot:run -Dspring-boot.run.profiles=dev'

# Docker shortcuts
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dlog='docker logs -f'                        # follow logs: dlog <name>
alias dexec='docker exec -it'                      # shell into container: dexec <name> bash
alias dcu='docker-compose up -d'                  # start all services
alias dcd='docker-compose down'                   # stop all services
alias dclog='docker-compose logs -f'              # follow all services' logs

# Kubernetes shortcuts (for when you get there)
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kl='kubectl logs -f'

# Git shortcuts
alias gs='git status'
alias gd='git diff'
alias gds='git diff --staged'
alias gl="git log --oneline --graph --decorate -20"
alias gla="git log --oneline --graph --decorate --all"
alias gp='git push'
alias gpl='git pull'
alias gco='git checkout'
alias gcob='git checkout -b'
alias gaa='git add -A'

# PostgreSQL via Docker
alias psql-local='docker exec -it dev-postgres psql -U admin -d appdb'

# Redis CLI via Docker
alias redis-cli-local='docker exec -it dev-redis redis-cli -a devpassword'

# Kafka tools via Docker
alias kafka-topics-local='docker exec -it dev-kafka kafka-topics --bootstrap-server localhost:9092'
alias kafka-console-consumer='docker exec -it dev-kafka kafka-console-consumer --bootstrap-server localhost:9092'

# ─── Utility functions ────────────────────────────────────────────────────────

# Find which process is listening on a port:
listening_on() {
  lsof -i ":$1" | grep LISTEN
}
# Usage: listening_on 8080

# Watch a Spring Boot log with colored output:
watch_log() {
  tail -f "$1" | grep --color=always -E "ERROR|WARN|INFO|DEBUG|$"
}

# Quick HTTP test with JWT:
http_get() {
  curl -s -H "Authorization: Bearer $JWT_TOKEN" "$1" | jq '.'
}
http_post() {
  curl -s -X POST -H "Authorization: Bearer $JWT_TOKEN" \
       -H "Content-Type: application/json" \
       -d "$2" "$1" | jq '.'
}
# Usage: JWT_TOKEN="eyJ..." http_get http://localhost:8080/api/orders/123
```

### API Testing with curl and jq

**curl** is the standard CLI HTTP client. Learn to use it for testing your APIs without Postman:

```bash
# Basic GET request:
curl http://localhost:8080/api/v1/orders

# GET with authentication header:
curl -H "Authorization: Bearer eyJhbGc..." http://localhost:8080/api/v1/orders

# GET with pretty-printed JSON output (pipe to jq):
curl -s http://localhost:8080/api/v1/orders | jq '.'

# POST with JSON body:
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT" \
  -d '{"customerId": "cust_123", "items": [{"productId": "p_456", "qty": 2}]}' \
  http://localhost:8080/api/v1/orders

# See request and response headers:
curl -v http://localhost:8080/api/v1/orders

# See only the HTTP status code:
curl -o /dev/null -s -w "%{http_code}" http://localhost:8080/api/v1/orders/123

# Test with timing information:
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTotal: %{time_total}s\n" \
  http://localhost:8080/api/v1/orders

# Follow redirects:
curl -L http://localhost:8080

# Save response to file:
curl -o response.json http://localhost:8080/api/v1/orders
```

**jq** is an indispensable JSON processor for the terminal:

```bash
# Pretty-print JSON:
echo '{"id":"123","status":"PENDING","total":49.99}' | jq '.'

# Extract a specific field:
curl -s http://localhost:8080/api/v1/orders/123 | jq '.status'
# Output: "PENDING"

# Extract from array — get all order IDs:
curl -s http://localhost:8080/api/v1/orders | jq '.[].id'

# Filter array by condition:
curl -s http://localhost:8080/api/v1/orders | jq '.[] | select(.status == "PENDING")'

# Count elements:
curl -s http://localhost:8080/api/v1/orders | jq 'length'

# Extract nested field:
curl -s http://localhost:8080/api/v1/orders/123 | jq '.customer.email'

# Build a new JSON object from response:
curl -s http://localhost:8080/api/v1/orders/123 | jq '{id: .id, amount: .total}'

# Sort array by field:
curl -s http://localhost:8080/api/v1/orders | jq 'sort_by(.createdAt)'

# Get first N elements:
curl -s http://localhost:8080/api/v1/orders | jq '.[0:5]'

# Compact (minified) output:
curl -s http://localhost:8080/api/v1/orders/123 | jq -c '.'
```

### Process Investigation Commands

These are the commands you use when debugging a production issue or investigating a misbehaving service:

```bash
# ─── Find a Java process ─────────────────────────────────────────────────────
ps aux | grep java
# Shows: PID, CPU%, MEM%, command

jps -v
# Java-specific: shows only JVM processes with JVM arguments
# Requires JDK installed (use jps from JDK bin)

# ─── Memory and CPU ──────────────────────────────────────────────────────────
# See memory and CPU usage for PID 12345:
top -p 12345           # Linux
# or just: top, then press 'u', type username

# Java-specific memory analysis:
jmap -heap 12345       # JVM heap summary
jstack 12345           # thread dump (show all threads and their stack traces)
jstat -gc 12345 1000   # GC statistics every 1000ms

# ─── Network connections ──────────────────────────────────────────────────────
# What ports is my app listening on?
ss -tlnp | grep java
netstat -tlnp | grep java

# How many connections on port 8080?
ss -an | grep :8080 | wc -l

# Connections by state (ESTABLISHED, TIME_WAIT, etc.):
ss -an | grep :8080 | awk '{print $2}' | sort | uniq -c

# ─── File descriptors ─────────────────────────────────────────────────────────
# How many file descriptors does PID 12345 have open?
ls /proc/12345/fd | wc -l     # Linux

# What are they?
ls -la /proc/12345/fd          # Linux
lsof -p 12345                  # macOS / Linux

# ─── Disk I/O ─────────────────────────────────────────────────────────────────
iotop -o              # real-time I/O per process (requires root)
iostat -x 1           # device-level I/O statistics every 1 second

# ─── Log analysis ──────────────────────────────────────────────────────────────
# Count errors per minute in a Spring Boot log:
grep "ERROR" /var/log/myapp.log | \
  awk '{print $1, $2}' | \
  cut -c1-16 | \
  sort | uniq -c | sort -rn | head -20

# Find the most common exceptions:
grep "Exception" /var/log/myapp.log | \
  grep -oP '(?<=: )\w+Exception' | \
  sort | uniq -c | sort -rn

# Follow live log with highlighting:
tail -f /var/log/myapp.log | \
  grep --line-buffered --color=always -E "ERROR|WARN|Exception|$"
```

---

## Why This Matters for Your SDE-2 Journey

**SDKMAN and environment consistency (Section 6.1):**  
Different projects use different Java versions. SDKMAN lets you switch instantly. CI/CD pipelines declare the required Java version in `.sdkman/tool-versions` or `Dockerfile`. Understanding SDKMAN prevents the "works on my machine" problem caused by wrong JDK versions.

**Maven lifecycle mastery (Section 6.2):**  
In interviews and on the job, you need to be able to: run specific tests by name, skip tests when doing a quick build, check the dependency tree for version conflicts, and understand what `mvn clean install` does at each phase. The `mvn dependency:tree` command is essential when diagnosing classpath conflicts (two transitive dependencies pulling in different versions of the same library).

**Git hygiene as an SDE-2 signal (Section 6.3):**  
Senior engineers write atomic, well-scoped commits with Conventional Commits messages. They use `git add -p` for precise staging. They use interactive rebase to clean up history before PR review. They know the difference between `reset`, `revert`, and `restore` and choose the right tool. A messy commit history in your portfolio project is a red flag to reviewers.

**Debugging skills (Section 6.4):**  
Every SDE-2 interview includes "tell me about a hard bug you debugged." Conditional breakpoints, evaluate-expression, and watching variables in the debug panel are how you tell a story about systematic debugging rather than `System.out.println()` spray.

**Stack trace fluency (Section 6.5):**  
The ability to look at a 50-line Spring Boot stack trace and immediately identify the relevant line in your code (ignoring Spring/Tomcat/JDK frames) and the root cause exception is a senior engineer's reflex. In production incidents, this skill separates engineers who fix problems quickly from those who spend 30 minutes reading the wrong part of the trace.

**curl + jq mastery (Section 6.6):**  
In a technical interview, being asked to "show me how you'd test this endpoint" and smoothly typing `curl -s -X POST -H "Authorization: Bearer $TOKEN" -d '{"key":"value"}' http://localhost:8080/api/v1/orders | jq '.id'` is more impressive than opening Postman. More importantly, in production debugging (where you often only have a terminal), `curl` and `jq` are your primary tools for API investigation.

---

---

# Appendix A: Quick Reference — Numbers Every Engineer Should Know

Keep these numbers in your head. They come up constantly in system design discussions.

## Latency Numbers

```
Operation                          Approximate Latency
─────────────────────────────────────────────────────────────────────
L1 cache hit                       ~1 nanosecond (ns)
Branch misprediction               ~5 ns
L2 cache hit                       ~4 ns
L3 cache hit                       ~10-40 ns
Mutex lock/unlock                  ~25 ns
RAM access (main memory)           ~100 ns
Compress 1KB with Snappy           ~3,000 ns = 3 microseconds (μs)
Send 2KB over 1Gbps network        ~20 μs (within same datacenter)
Redis GET (in-memory, localhost)   ~0.5-1 ms
Read 4KB randomly from SSD         ~150 μs
Read 1MB sequentially from SSD     ~1 ms
Round-trip in same datacenter      ~0.5 ms
MySQL SELECT with index (cached)   ~1-2 ms
MySQL SELECT with index (cold)     ~5-10 ms
Disk seek (HDD)                    ~10 ms
Read 1MB sequentially from HDD     ~20 ms
Kafka publish + consumer receive   ~5-15 ms (within same DC)
Send packet: EU → US               ~150 ms
TCP handshake (same region)        ~1-5 ms
TCP handshake (cross-continent)    ~100-300 ms
TLS handshake (on top of TCP)      +1-2 RTTs (double the TCP cost)
DNS resolution (cold)              ~20-200 ms
DNS resolution (cached)            ~0 ms
```

## Storage and Throughput Numbers

```
Storage type       Read throughput      Write throughput     IOPS (random 4KB)
─────────────────────────────────────────────────────────────────────────────
NVMe SSD           ~3,500 MB/s           ~3,000 MB/s          ~700,000
SATA SSD           ~550 MB/s             ~520 MB/s            ~100,000
HDD (7200 RPM)     ~150 MB/s            ~150 MB/s            ~100
Network (1 GbE)    ~125 MB/s             ~125 MB/s            N/A
Network (10 GbE)   ~1,250 MB/s          ~1,250 MB/s          N/A
RAM (DDR4)         ~50,000 MB/s          ~50,000 MB/s         N/A (not block)
```

## Common System Limits

```
Quantity                            Typical Value
──────────────────────────────────────────────────────────────────
Default OS file descriptor limit   1,024 (adjust to 65,535+ in prod)
Default Linux thread stack size    512 KB – 8 MB (JVM default: 512KB)
Max TCP connections (client)       ~65,535 per (src_ip, dst_ip, dst_port)
Max ports per socket               65,535 (16-bit port number)
Max IPv4 addresses                 ~4.3 billion (32-bit)
JVM default heap size              256 MB (adjust with -Xmx)
JVM metaspace default              unlimited (set -XX:MaxMetaspaceSize)
PostgreSQL default max connections 100 (adjust in postgresql.conf)
HikariCP default pool size         10 connections
Kafka default max message size     1 MB (adjust max.message.bytes)
Redis max memory (no limit set)    No limit (will use all RAM)
Default Linux max process count    32,768 (kernel.pid_max)
```

---

# Appendix B: Quick Reference — The SDE-2 Interview Concept Checklist

Use this to track your understanding of each foundational concept.

## Binary and Data Representation
- [ ] Convert binary ↔ decimal ↔ hexadecimal
- [ ] Explain why floating-point is imprecise and when to use BigDecimal
- [ ] Explain integer overflow and Java's types (int vs long)
- [ ] Explain UTF-8 vs UTF-16 and why string.length() can mislead

## CPU and Memory
- [ ] Walk through the Fetch-Decode-Execute cycle
- [ ] Explain CPU cache hierarchy and cache miss cost
- [ ] Explain why ArrayList beats LinkedList for iteration (cache locality)
- [ ] Explain the memory hierarchy and latency numbers

## Operating Systems
- [ ] Explain kernel space vs user space and why the separation exists
- [ ] Explain what a system call is and why it has overhead
- [ ] Walk through a process's state machine (NEW → READY → RUNNING → BLOCKED → TERMINATED)
- [ ] Explain context switching and its cost
- [ ] Explain the difference between a process and a thread
- [ ] Explain race conditions with a concrete example
- [ ] Explain mutex and deadlock, with prevention strategies
- [ ] Explain virtual threads (Java 21) and why they improve throughput
- [ ] Explain virtual memory and page tables
- [ ] Explain file descriptors and why "too many open files" happens

## Programs and Execution
- [ ] Explain compiled vs interpreted vs JIT-compiled languages
- [ ] Explain what the JVM's JIT compiler does and the warmup concept
- [ ] Walk through what happens when you run `java -jar myapp.jar`
- [ ] Explain the call stack, stack frames, and StackOverflowError
- [ ] Explain why GraalVM native image fixes Java's startup time

## Networking
- [ ] Name the 7 OSI layers and their purpose
- [ ] Explain the TCP 3-way handshake and why it matters for performance
- [ ] Walk through a DNS resolution from browser to authoritative server
- [ ] Explain what a socket is and identify it by its 4-tuple
- [ ] Explain TLS: what it protects against, symmetric vs asymmetric, CA role
- [ ] Explain HTTP verbs, status codes, and idempotency
- [ ] Explain the difference between HTTP/1.1, HTTP/2, and HTTP/3
- [ ] Explain WebSocket and when to use it vs HTTP

## Application Architecture
- [ ] Walk through a complete HTTP request lifecycle end-to-end
- [ ] Explain stateless vs stateful and why JWT supports stateless
- [ ] Explain the role of a load balancer, Nginx, and Spring Boot in the stack
- [ ] Explain synchronous vs asynchronous microservice communication
- [ ] Explain database-per-service and why shared databases violate microservice principles
- [ ] Explain Kubernetes service discovery (DNS-based via CoreDNS)

## Tooling
- [ ] Explain the Maven build lifecycle phases and what each does
- [ ] Read a Java stack trace to find the root cause quickly
- [ ] Write a curl command to test a POST endpoint with JWT
- [ ] Use jq to filter and extract fields from a JSON response
- [ ] Explain git rebase vs merge and when to use each

---

# Appendix C: Glossary

**ALU (Arithmetic Logic Unit):** The component of the CPU that performs mathematical and logical operations.

**Asymmetric Encryption:** Encryption using a public/private key pair. Slow but solves the key distribution problem. Used in TLS handshake.

**Cache Hit/Miss:** A cache hit occurs when requested data is found in a faster (closer) cache layer. A cache miss requires fetching from a slower (further) layer.

**Certificate Authority (CA):** A trusted organization that cryptographically signs digital certificates, vouching for the identity of the certificate holder.

**CIDR (Classless Inter-Domain Routing):** Notation for IP address ranges: `192.168.1.0/24` means 24 bits are the network prefix, 8 bits are host addresses.

**Context Switch:** Pausing one process or thread and resuming another. Requires saving and restoring CPU register state.

**Daemon:** A background process with no UI that runs continuously and provides services.

**DNS (Domain Name System):** A distributed hierarchical database mapping domain names to IP addresses.

**Ephemeral Port:** A temporary, high-numbered port (49152–65535) assigned by the OS for outgoing connections.

**File Descriptor (fd):** An integer handle representing an open file, socket, or other I/O resource in a process.

**Fork:** A system call that creates a copy of the current process.

**Green Thread:** A thread managed by the language runtime rather than the OS kernel.

**Heap:** The dynamic memory area where objects are allocated with `new` and managed by the garbage collector.

**HTTP (HyperText Transfer Protocol):** A text-based request-response application protocol running over TCP.

**HTTPS:** HTTP secured with TLS encryption.

**Inode:** A Unix data structure containing file metadata (size, permissions, timestamps, data block pointers) but not the filename.

**IPC (Inter-Process Communication):** Mechanisms for processes to communicate: pipes, shared memory, sockets, message queues.

**JIT (Just-In-Time) Compilation:** Compiling code to native machine code at runtime rather than ahead of time.

**JVM (Java Virtual Machine):** The runtime that executes Java bytecode, provides memory management (GC), and JIT compiles hot code to native.

**Kernel:** The core of an OS that has privileged hardware access and manages processes, memory, and devices.

**Kernel Space:** The protected memory region where OS kernel code runs with full hardware access.

**MAC Address:** A 48-bit hardware address burned into a network interface card, used for local network delivery.

**Mutex (Mutual Exclusion Lock):** A synchronization primitive allowing only one thread to hold it at a time.

**NAT (Network Address Translation):** Technique allowing multiple devices with private IPs to share one public IP.

**NIC (Network Interface Card):** Hardware that connects a computer to a network and converts data to/from physical signals.

**Page Fault:** An exception when a process accesses a virtual address not currently in physical RAM.

**Page Table:** OS data structure mapping virtual page addresses to physical frame addresses.

**PCB (Process Control Block):** OS data structure tracking a process's state, registers, memory maps, and open files.

**Pipeline:** CPU technique overlapping instruction fetch/decode/execute stages for multiple instructions.

**Port:** A 16-bit number identifying which application on a host should receive a packet.

**Process:** A running instance of a program with isolated memory, file descriptors, and process ID.

**Race Condition:** Incorrect behavior arising when the outcome depends on the relative timing of concurrent operations.

**Router:** A device that forwards packets between different IP networks.

**Socket:** An OS abstraction representing one endpoint of a network connection, identified by (src_IP, src_port, dst_IP, dst_port).

**Stack:** The LIFO memory region storing function call frames (local variables, return addresses).

**Stack Frame:** A region of stack memory allocated for one function call.

**Switch (Network):** A device that connects devices on the same local network using MAC addresses.

**Symmetric Encryption:** Encryption where both parties use the same key. Fast; used for bulk data transfer in TLS.

**Syscall (System Call):** The mechanism for user-space code to request kernel services.

**Thread:** A unit of execution within a process sharing the process's memory but with its own stack and registers.

**TLS (Transport Layer Security):** Protocol providing encrypted communication over a network.

**TTL (Time To Live):** In DNS, how long a resolver should cache a record before re-querying.

**User Space:** The memory region where application code runs with restricted hardware access.

**Virtual Memory:** An abstraction giving each process the illusion of a private address space, mapped to physical RAM by the MMU.

**Virtual Thread (Java 21):** A lightweight thread managed by the JVM, multiplexed over a small pool of OS threads.

---

*End of "Computer Science and Systems Foundations: How Computers, Programs, Networks, and Web Applications Actually Work"*

*Word count: approximately 60,000 words | Chapters: 6 | Appendices: 3*

*Next in your preparation: LLD and Design Patterns (Book 1) → Spring Boot and Backend Engineering Internals (Book 2)*

