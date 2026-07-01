# LinkedIn Post Calendar

```dataview
TABLE scheduled_week as Week, scheduled_day as Day, status
FROM "Career/LinkedIn Content/Posts"
WHERE type = "linkedin-post"
SORT post_number ASC
```


---

## All Posts (Explicit Index)

> This section creates graph edges for each post note so they appear in
> Obsidian's backlink panel and graph view. The Dataview table above
> handles display; these links handle graph connectivity.

**Week 1**
[[Post 01 Journey Announcement]] · [[Post 02 Java Integer Cache Trap]]

**Week 2**
[[Post 03 JVM Memory Model Diagram]] · [[Post 04 Race Condition Proof]]

**Week 3**
[[Post 05 To-Do API Launch]] · [[Post 06 DSA Pattern Visual]]

**Week 4**
[[Post 07 HashMap Internals]] · [[Post 08 LeetCode Patterns Carousel]]

**Week 5**
[[Post 09 Order Management API Architecture]] · [[Post 10 Transactional Deep Dive]]

**Week 6**
[[Post 11 Kafka Partitions]] · [[Post 12 TestContainers vs H2]]

**Week 7**
[[Post 13 Rate Limiter Algorithm Comparison]] · [[Post 14 Resilience4j Circuit Breaker]]

**Week 8**
[[Post 15 Month 2 Recap]] · [[Post 16 Poll]]

**Week 9**
[[Post 17 WhatsApp Architecture Breakdown]] · [[Post 18 LLD Parking Lot]]

**Week 10**
[[Post 19 Kubernetes Zero-Downtime Deployment]] · [[Post 20 CICD Pipeline Walkthrough]]

**Week 11**
[[Post 21 AWS Lessons]] · [[Post 22 JWT vs OAuth 2.0]]

**Week 12**
[[Post 23 Mock Interview Experience]] · [[Post 24 BookMyShow Seat Booking Challenge]]

**Week 13**
[[Post 25 Actively Interviewing Announcement]] · [[Post 26 Saga Pattern with Code]]

**Week 14**
[[Post 27 Fintech Engineering]] · [[Post 28 E-Commerce Platform Launch]]

**Week 15**
[[Post 29 Interview Experience 1]] · [[Post 30 Offer Negotiation Research]]

**Week 16**
[[Post 31 Offer Received]] · [[Post 32 Open Source Contribution]]

**Week 17**
[[Post 33 Full Journey Story]] · [[Post 34 Advice for Day 1]]
