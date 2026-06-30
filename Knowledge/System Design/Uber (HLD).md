---
type: concept
subject: System Design
source_book: "Book 8 — High-Level System Design"
source_chapter: "Chapter 7 — Design 5 — Uber"
status: to-study
interview_frequency: high
introduced_day: 
related_concepts: ["System Design Building Blocks"]
tags: [hld, case-study, uber, geohash, redis]
---

# HLD Case Study: Uber

## Problem Overview
Match riders to nearby available drivers in real-time.
- **Scale:** 3M active drivers updating location every 4 seconds = 750,000 location updates/sec. 5M trips/day (58 trips/sec avg).
- **Throughput Bottleneck:** Location ingestion, not trip creation.

## The Geo-Indexing Problem
A naive SQL query (`WHERE distance < 2km`) requires a full table scan and math on every row. Not feasible for 3M drivers updating every 4 seconds.

### Solution 1: Geohash
Encodes a (lat, lng) into a string where nearby locations share a common prefix.
e.g. `12.97, 77.59 -> "tdr1y"`.
A 5-char geohash is a ~2.4km x 2.4km box. To find drivers within 2km, compute the rider's geohash and query that cell + its 8 neighbors.

### Solution 2: Redis GEO (Recommended)
Redis has built-in geospatial indexing (`GEOADD`, `GEORADIUS`) that uses geohashing under the hood.
- `GEOADD drivers:geo 77.59 12.97 "driver_1"` (Run every 4s)
- `GEORADIUS drivers:geo 77.60 12.97 2 km` (Run on ride request)

## Matching Algorithm
1. Compute rider's geohash; `GEORADIUS` against Redis to find candidates within 2km.
2. Filter for **available** drivers.
3. Rank candidates (distance, rating, idle time).
4. Offer trip to top-ranked driver with a timeout (10-15s).

## Surge Pricing
A **Kafka Streams** job consumes the location/request event stream and calculates the ratio of (ride requests / available drivers) per geohash cell in a rolling 5-minute window. If the ratio crosses a threshold, a surge multiplier is published for that cell.

## Handling 10x Scale
- 7.5M location updates/sec: Shard Redis GEO by geographic region (e.g. one Redis Cluster per metro area) instead of one global instance. Matching requests are inherently localized to a single shard.
