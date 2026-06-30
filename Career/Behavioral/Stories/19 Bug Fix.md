---
type: star-story
story_id: 19
title: "Time you identified and fixed a bug nobody else noticed — Data Over-fetching"
amazon_lps: []
last_rehearsed:
rehearsal_count: 0
tags: [star-story]
---

### Situation
While analyzing network requests in Chrome DevTools for a routine UI task, I noticed our API was returning full user objects (including hashed passwords and internal IDs) to the frontend, even though the UI only needed the user's name and avatar.

### Task
I needed to address this data over-fetching, which was a significant security risk.

### Action
I immediately flagged the issue to the backend lead. Since they were swamped, I offered to help. I checked out the backend repository, learned enough Spring Boot routing to find the endpoint, and created a specific `UserSummaryDTO` that only mapped the safe fields. I updated the controller to return the DTO and adjusted the frontend to match.

### Result
I submitted the cross-repository PRs. The security risk was patched before it was ever exploited. This proactive approach across the stack reinforced my desire to master backend engineering.
