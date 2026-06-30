---
type: star-story
story_id: 17
title: "Technical decision you're proud of — Architecture CRDT"
amazon_lps: []
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
We needed to implement a real-time collaborative feature (like Google Docs) on our frontend.

### Task
I had to choose the architecture to handle concurrent edits without conflicts.

### Action
Instead of trying to invent a custom WebSocket locking mechanism which is highly error-prone, I researched Operational Transformation (OT) and Conflict-free Replicated Data Types (CRDTs). I evaluated Yjs (a CRDT framework) and built a proof-of-concept integrating it with our React state. I demonstrated how it automatically resolved offline edits and concurrent merges without a central server lock.

### Result
The team adopted the CRDT architecture. It scaled flawlessly to hundreds of concurrent users per document, and I presented the architecture at an internal engineering all-hands. This deep dive into distributed state was a major catalyst for my move toward backend systems.
