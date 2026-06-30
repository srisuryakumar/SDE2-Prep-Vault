---
type: concept
subject: CS Foundations
source_book: "Book 0 — Computer Science and Systems Foundations"
source_chapter: "Chapter 1 — The Computer at Its Core"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: []
tags: [cs-foundations]
---

# Memory Hierarchy and Storage Types

Every storage system trades off **speed vs capacity vs cost**. The fundamental rule is: the faster the storage, the smaller and more expensive it is.

## The Memory Hierarchy
- **Registers (CPU):** <1 ns (~128-256 bytes)
- **L1/L2/L3 Caches:** 1-40 ns (~32 KB - 32 MB)
- **RAM (DRAM):** ~100 ns (~16 GB - 512 GB)
- **NVMe SSD:** ~100 μs (~500 GB - 8 TB)
- **SATA SSD:** ~500 μs (~500 GB - 8 TB)
- **HDD:** ~10 ms (~2 TB - 20 TB)

## Storage Types
### RAM (Random Access Memory)
The working memory of the computer. It is **volatile** (loses contents when powered off). It allows **Random Access**, meaning the CPU can read/write any byte in the same amount of time (~100ns).

### Storage (Persistent)
- **SSD (Solid State Drive):** Uses NAND flash memory chips. No moving parts. Great for random reads/writes.
- **HDD (Hard Disk Drive):** Uses spinning magnetic platters. The mechanical movement introduces ~10ms of latency per read. Terrible for random access, acceptable for sequential bulk reads/writes.

## Implications for Databases
- **Transaction Logs (WAL):** Sequential writes. Both HDD and SSD work well, but NVMe SSD is preferred.
- **Index files (B-trees):** Random reads. **Must** use SSDs.
- **In-Memory (Redis):** Redis stores everything in RAM (~100ns access) whereas databases like PostgreSQL read from disk (~100μs-10ms) when the buffer pool is cold. This is why Redis is 100-10,000x faster for small lookups.
