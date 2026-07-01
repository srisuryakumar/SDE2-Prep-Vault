---
type: concept
tags: [moc, star-stories, behavioral]
---
# STAR Stories — Map of Content

## By Amazon Leadership Principle

See [[Amazon LP Mapping]] for the full LP-to-story cross-reference.

## All Stories

```dataview
TABLE story_id as "ID", title as "Story", amazon_lps as "LP", rehearsal_count as "Times Rehearsed", last_rehearsed as "Last Rehearsed"
FROM "Career/Behavioral/Stories"
WHERE type = "star-story"
SORT story_id ASC
```

## Rehearsal Status

```dataview
TABLE title, rehearsal_count, last_rehearsed
FROM "Career/Behavioral/Stories"
WHERE type = "star-story" AND (rehearsal_count = 0 OR last_rehearsed < date(today) - dur(7 days))
SORT last_rehearsed ASC
```
