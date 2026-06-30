---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 8 — Design 6 — Netflix"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks"]
tags: [hld, case-study, netflix, video-streaming, cdn]
---

# HLD Case Study: Netflix

## Problem Overview
Stream video at adaptive quality to 200M subscribers worldwide.
- **Scale:** 500M streaming hours/day. Peak concurrency: ~60-80M streams.
- **Bandwidth:** ~350 Tbps of egress at global peak. This bandwidth is impossible to serve from a centralized datacenter, making the CDN the core of the architecture.

## Video Upload Pipeline (Pre-Processing)
Video isn't transcoded on the fly. When a master file is uploaded to S3, a **Transcoding Service** processes it into *many* resolution and bitrate variants (240p to 4K, multiple bitrates per resolution).
The cost of transcoding is paid upfront because the output is reused millions of times.

## Adaptive Bitrate Streaming (HLS/DASH)
Videos are split into short segments (e.g. 2-10 seconds), with each segment available at multiple bitrates.
The client dynamically chooses which segment to request next based on:
1. Recent download throughput.
2. Current buffer health.
This allows seamless quality degradation on a weak signal without stalling playback.

## The CDN Strategy: Open Connect
Instead of relying only on 3rd-party CDNs, Netflix installs its own caching appliances (**Open Connect Appliances, OCAs**) directly inside ISP data centers.
A user's stream is served from inside their own ISP's network, drastically reducing global bandwidth consumption and latency.

## Recommendations
Recommendations are **precomputed** offline/near-real-time by a batch/streaming ML pipeline (Kafka -> Feature Store -> Redis). They are cached per-user in Redis so that the home screen loads instantly on app open, without running heavy ML inference in real-time.

## Common Questions
**Q: What happens on a cache miss at the OCA?**
A: The OCA fetches the content from a regional/origin fill server, caches it locally for subsequent viewers in that ISP, and serves the requesting viewer. This is a standard pull-CDN pattern.
