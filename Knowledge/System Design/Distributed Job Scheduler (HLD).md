---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 13 — Design 11 — Distributed Job Scheduler"
status: to-study
interview_frequency: medium
introduced_day: 
related_concepts: ["System Design Trade-offs"]
tags: [hld, case-study, job-scheduler, cron, locking]
---

# HLD Case Study: Distributed Job Scheduler

## Problem Overview
Schedule one-time and recurring jobs.
- **Constraints:** No job should silently never run. No job should run twice simultaneously. Must survive node crashes.
- **Scale:** 1M total jobs, up to 10k jobs executing per minute at peak.

## Leader Election
If multiple schedulers run concurrently, they might both dispatch the same job.
**Solution:** ZooKeeper leader election.
- All instances try to create an ephemeral node (`/scheduler/leader`).
- The one that succeeds is the active dispatcher. The others stand by.
- If the leader crashes, its session times out, the ephemeral node is deleted, and the standbys race to become the new leader.

## Distributed Worker Locking
Once the leader marks a job as `DUE`, workers need to pick it up without two workers grabbing the same job.
**Solution:** `SELECT FOR UPDATE SKIP LOCKED`
```sql
SELECT * FROM jobs WHERE status = 'DUE' AND run_at <= NOW()
LIMIT 1 FOR UPDATE SKIP LOCKED;
UPDATE jobs SET status = 'RUNNING', worker_id = ? WHERE id = ?;
```
`SKIP LOCKED` allows many workers to poll the same table. Instead of blocking each other, they skip past rows locked by other workers, achieving natural parallelism.

## Exactly-Once vs At-Least-Once
**The Problem:** A worker executes a job but crashes *before* marking it `COMPLETED` in the DB. The heartbeat monitor times out, and the job is marked `DUE` again. It will execute twice.
**The Solution:** The system can only guarantee **at-least-once** execution. To solve this, **require job handlers to be idempotent**. (e.g. "charge $10" becomes "ensure a $10 charge exists for idempotency-key X").

## Handling 10x Scale
A single PostgreSQL `jobs` table becomes a bottleneck for polling.
- Shard the `jobs` table (e.g., by `job_id` hash) across multiple DB instances.
- If polling overhead is too high, move to a push-based model (leader publishes due jobs to a Kafka topic, workers consume).
