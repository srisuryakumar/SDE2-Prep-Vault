# Revision Tracker

## LeetCode Revisions Due
```dataview
TABLE difficulty, next_review_due, review_count, last_reviewed
FROM "Practice/LeetCode"
WHERE type = "leetcode-problem" AND next_review_due <= date(today) AND status != "mastered"
SORT next_review_due ASC
```

## Knowledge Needs Review
```dataview
TABLE subject, interview_frequency
FROM "Knowledge"
WHERE type = "concept" AND status = "needs-review"
```
